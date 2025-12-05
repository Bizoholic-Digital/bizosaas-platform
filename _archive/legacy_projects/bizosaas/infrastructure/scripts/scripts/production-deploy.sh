#!/bin/bash

# BizOSaaS Production Deployment Script
# Automated deployment with health checks and rollback capabilities

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
COMPOSE_FILE="docker-compose.production.optimized.yml"
ENV_FILE=".env.production"
BACKUP_DIR="/opt/bizosaas/backups"
LOG_FILE="/var/log/bizosaas-deploy.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root for production deployment"
        exit 1
    fi
}

# Validate environment
validate_environment() {
    log "Validating production environment..."
    
    # Check required files
    if [[ ! -f "$PROJECT_DIR/$ENV_FILE" ]]; then
        error "Environment file $ENV_FILE not found"
        exit 1
    fi
    
    if [[ ! -f "$PROJECT_DIR/$COMPOSE_FILE" ]]; then
        error "Docker compose file $COMPOSE_FILE not found"
        exit 1
    fi
    
    # Check Docker and Docker Compose
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed"
        exit 1
    fi
    
    # Check Docker daemon
    if ! docker info &> /dev/null; then
        error "Docker daemon is not running"
        exit 1
    fi
    
    # Load environment variables
    source "$PROJECT_DIR/$ENV_FILE"
    
    # Check critical environment variables
    local required_vars=("DOMAIN" "API_DOMAIN" "POSTGRES_PASSWORD" "JWT_SECRET")
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            error "Required environment variable $var is not set"
            exit 1
        fi
    done
    
    success "Environment validation completed"
}

# Pre-deployment checks
pre_deployment_checks() {
    log "Running pre-deployment checks..."
    
    # Check disk space (require at least 10GB free)
    local available_space=$(df / | awk 'NR==2 {print $4}')
    local required_space=10485760  # 10GB in KB
    
    if [[ $available_space -lt $required_space ]]; then
        error "Insufficient disk space. Required: 10GB, Available: $(($available_space / 1024 / 1024))GB"
        exit 1
    fi
    
    # Check memory (require at least 8GB)
    local total_memory=$(free -m | awk 'NR==2{print $2}')
    local required_memory=8192  # 8GB in MB
    
    if [[ $total_memory -lt $required_memory ]]; then
        warning "System has less than 8GB RAM. Performance may be affected."
    fi
    
    # Check network connectivity
    if ! curl -f -s --connect-timeout 5 https://registry-1.docker.io/v2/ > /dev/null; then
        error "Cannot connect to Docker registry"
        exit 1
    fi
    
    success "Pre-deployment checks completed"
}

# Create backup before deployment
create_backup() {
    log "Creating pre-deployment backup..."
    
    mkdir -p "$BACKUP_DIR"
    local backup_timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$BACKUP_DIR/pre_deploy_backup_$backup_timestamp.tar.gz"
    
    # Backup database if running
    if docker-compose -f "$PROJECT_DIR/$COMPOSE_FILE" ps | grep -q "bizosaas-postgres.*Up"; then
        log "Backing up database..."
        docker-compose -f "$PROJECT_DIR/$COMPOSE_FILE" exec -T bizosaas-postgres \
            pg_dumpall -U "${POSTGRES_USER:-bizosaas_prod}" > "$BACKUP_DIR/postgres_$backup_timestamp.sql"
        gzip "$BACKUP_DIR/postgres_$backup_timestamp.sql"
    fi
    
    # Backup Docker volumes
    log "Backing up Docker volumes..."
    cd "$PROJECT_DIR"
    tar -czf "$backup_file" \
        --exclude='.git' \
        --exclude='node_modules' \
        --exclude='*.log' \
        --exclude='tmp' \
        .
    
    success "Backup created: $backup_file"
    echo "$backup_file" > "$BACKUP_DIR/latest_backup.txt"
}

# Build production images
build_images() {
    log "Building production images..."
    
    cd "$PROJECT_DIR"
    
    # Set build environment
    export DOCKER_BUILDKIT=1
    export COMPOSE_DOCKER_CLI_BUILD=1
    
    # Build all images
    docker-compose -f "$COMPOSE_FILE" build --no-cache --parallel
    
    # Tag images with timestamp
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local images=("bizosaas/brain-api" "bizosaas/ai-agents" "bizosaas/crm" "bizosaas/wagtail-cms" 
                  "bizosaas/admin-frontend" "bizosaas/bizoholic-frontend" "bizosaas/coreldove-frontend" "bizosaas/client-portal")
    
    for image in "${images[@]}"; do
        if docker images | grep -q "$image"; then
            docker tag "$image:latest" "$image:$timestamp"
            docker tag "$image:latest" "$image:stable"
        fi
    done
    
    success "Images built successfully"
}

# Deploy infrastructure services first
deploy_infrastructure() {
    log "Deploying infrastructure services..."
    
    cd "$PROJECT_DIR"
    
    # Start infrastructure services
    docker-compose -f "$COMPOSE_FILE" up -d \
        bizosaas-postgres \
        bizosaas-redis \
        bizosaas-traefik
    
    # Wait for services to be ready
    log "Waiting for infrastructure services to be ready..."
    
    # Wait for PostgreSQL
    local postgres_ready=false
    for i in {1..30}; do
        if docker-compose -f "$COMPOSE_FILE" exec -T bizosaas-postgres pg_isready -U "${POSTGRES_USER:-bizosaas_prod}" -d "${POSTGRES_DB:-bizosaas_production}" &> /dev/null; then
            postgres_ready=true
            break
        fi
        sleep 2
    done
    
    if [[ "$postgres_ready" != true ]]; then
        error "PostgreSQL failed to start within timeout"
        exit 1
    fi
    
    # Wait for Redis
    local redis_ready=false
    for i in {1..15}; do
        if docker-compose -f "$COMPOSE_FILE" exec -T bizosaas-redis redis-cli ping | grep -q "PONG"; then
            redis_ready=true
            break
        fi
        sleep 2
    done
    
    if [[ "$redis_ready" != true ]]; then
        error "Redis failed to start within timeout"
        exit 1
    fi
    
    success "Infrastructure services deployed"
}

# Run database migrations
run_migrations() {
    log "Running database migrations..."
    
    cd "$PROJECT_DIR"
    
    # Ensure vector extension is installed
    docker-compose -f "$COMPOSE_FILE" exec -T bizosaas-postgres \
        psql -U "${POSTGRES_USER:-bizosaas_prod}" -d "${POSTGRES_DB:-bizosaas_production}" \
        -c "CREATE EXTENSION IF NOT EXISTS vector;" || true
    
    # Start application services temporarily for migrations
    docker-compose -f "$COMPOSE_FILE" up -d bizosaas-crm bizosaas-wagtail-cms
    
    # Wait for services to start
    sleep 10
    
    # Run CRM migrations
    docker-compose -f "$COMPOSE_FILE" exec -T bizosaas-crm \
        python manage.py migrate --noinput
    
    # Run CMS migrations
    docker-compose -f "$COMPOSE_FILE" exec -T bizosaas-wagtail-cms \
        python manage.py migrate --noinput
    
    # Collect static files
    docker-compose -f "$COMPOSE_FILE" exec -T bizosaas-wagtail-cms \
        python manage.py collectstatic --noinput
    
    success "Database migrations completed"
}

# Deploy application services
deploy_application() {
    log "Deploying application services..."
    
    cd "$PROJECT_DIR"
    
    # Deploy all services
    docker-compose -f "$COMPOSE_FILE" up -d
    
    success "Application services deployed"
}

# Health checks
health_checks() {
    log "Running health checks..."
    
    local max_attempts=30
    local attempt=1
    
    # Health check endpoints
    local endpoints=(
        "http://localhost:${BRAIN_API_PORT:-8002}/health"
        "http://localhost:${AI_AGENTS_PORT:-8001}/health"
        "http://localhost:${CRM_PORT:-8007}/health/"
        "http://localhost:${ADMIN_FRONTEND_PORT:-3005}/api/health"
        "http://localhost:${BIZOHOLIC_FRONTEND_PORT:-3000}/api/health"
    )
    
    for endpoint in "${endpoints[@]}"; do
        log "Checking $endpoint..."
        local healthy=false
        
        for ((i=1; i<=max_attempts; i++)); do
            if curl -f -s --connect-timeout 5 "$endpoint" > /dev/null; then
                healthy=true
                break
            fi
            sleep 5
        done
        
        if [[ "$healthy" != true ]]; then
            error "Health check failed for $endpoint"
            return 1
        fi
    done
    
    # Check service status
    local unhealthy_services=$(docker-compose -f "$PROJECT_DIR/$COMPOSE_FILE" ps --services --filter "status=exited")
    if [[ -n "$unhealthy_services" ]]; then
        error "Some services are not running: $unhealthy_services"
        return 1
    fi
    
    success "All health checks passed"
}

# Post-deployment setup
post_deployment_setup() {
    log "Running post-deployment setup..."
    
    cd "$PROJECT_DIR"
    
    # Clean up old images
    docker image prune -f
    
    # Update monitoring dashboards
    if docker-compose -f "$COMPOSE_FILE" ps | grep -q "bizosaas-grafana.*Up"; then
        log "Updating Grafana dashboards..."
        # Import dashboards if available
        if [[ -d "monitoring/grafana/dashboards" ]]; then
            docker-compose -f "$COMPOSE_FILE" restart bizosaas-grafana
        fi
    fi
    
    # Set up log rotation
    cat > /etc/logrotate.d/bizosaas << EOF
/var/log/bizosaas-*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
EOF
    
    success "Post-deployment setup completed"
}

# Rollback function
rollback() {
    error "Deployment failed. Starting rollback..."
    
    # Get latest backup
    if [[ -f "$BACKUP_DIR/latest_backup.txt" ]]; then
        local backup_file=$(cat "$BACKUP_DIR/latest_backup.txt")
        if [[ -f "$backup_file" ]]; then
            log "Restoring from backup: $backup_file"
            
            # Stop current services
            docker-compose -f "$PROJECT_DIR/$COMPOSE_FILE" down
            
            # Extract backup
            cd "$PROJECT_DIR"
            tar -xzf "$backup_file"
            
            # Start services
            docker-compose -f "$COMPOSE_FILE" up -d
            
            success "Rollback completed"
        else
            error "Backup file not found: $backup_file"
        fi
    else
        error "No backup file information found"
    fi
}

# Main deployment function
main() {
    log "Starting BizOSaaS production deployment..."
    
    # Set error trap for rollback
    trap rollback ERR
    
    check_root
    validate_environment
    pre_deployment_checks
    create_backup
    build_images
    deploy_infrastructure
    run_migrations
    deploy_application
    
    # Allow services to start before health checks
    log "Waiting for services to stabilize..."
    sleep 30
    
    health_checks
    post_deployment_setup
    
    # Remove error trap
    trap - ERR
    
    success "🎉 BizOSaaS production deployment completed successfully!"
    log "Platform is available at:"
    log "  - Main website: https://${DOMAIN}"
    log "  - Admin panel: https://admin.${DOMAIN}"
    log "  - Client portal: https://portal.${DOMAIN}"
    log "  - CoreLDove e-commerce: https://coreldove.${DOMAIN}"
    log "  - API endpoints: https://${API_DOMAIN}"
    log "  - Monitoring: https://monitoring.${DOMAIN}"
}

# Script execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi