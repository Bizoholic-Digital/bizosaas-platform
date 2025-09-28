#!/bin/bash

# BizOSaaS Secure Authentication Deployment Script
# Deploys comprehensive authentication and security system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"
DOCKER_COMPOSE_FILE="${SCRIPT_DIR}/docker-compose.auth-security.yml"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if .env file exists
    if [[ ! -f "$ENV_FILE" ]]; then
        log_warning ".env file not found. Creating from template..."
        create_env_file
    fi
    
    log_success "Prerequisites check completed"
}

create_env_file() {
    cat > "$ENV_FILE" << 'EOF'
# BizOSaaS Security Configuration
# Production values should be properly secured

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-here-change-in-production-minimum-32-characters-long

# Encryption Configuration
ENCRYPTION_KEY=your-32-byte-base64-encoded-encryption-key-for-sensitive-data-encryption

# Database Configuration
POSTGRES_HOST=host.docker.internal
POSTGRES_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=securepassword123!
POSTGRES_DB=bizosaas

# Redis Configuration  
REDIS_HOST=host.docker.internal
REDIS_PORT=6379

# Saleor Configuration
SALEOR_API_URL=http://localhost:8024
SALEOR_DASHBOARD_URL=http://localhost:9020

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://bizosaas.local

# Security Settings
SESSION_TIMEOUT=3600
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION=900

# Vault Configuration
VAULT_TOKEN=myroot
VAULT_URL=http://localhost:8200

# Monitoring
GRAFANA_ADMIN_PASSWORD=admin123
ELASTIC_PASSWORD=elasticpass123
EOF
    
    log_success "Created .env file with default values"
    log_warning "Please review and update the .env file with secure values before deployment"
}

generate_ssl_certificates() {
    log_info "Generating SSL certificates for development..."
    
    SSL_DIR="${SCRIPT_DIR}/infrastructure/nginx/ssl"
    mkdir -p "$SSL_DIR"
    
    if [[ ! -f "${SSL_DIR}/bizosaas.crt" ]]; then
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout "${SSL_DIR}/bizosaas.key" \
            -out "${SSL_DIR}/bizosaas.crt" \
            -subj "/C=US/ST=State/L=City/O=BizOSaaS/CN=bizosaas.local/subjectAltName=DNS:*.bizosaas.local,DNS:localhost" \
            2>/dev/null
        
        log_success "SSL certificates generated"
    else
        log_info "SSL certificates already exist"
    fi
}

create_directories() {
    log_info "Creating required directories..."
    
    # Create infrastructure directories
    mkdir -p "${SCRIPT_DIR}/infrastructure/nginx/ssl"
    mkdir -p "${SCRIPT_DIR}/infrastructure/redis"
    mkdir -p "${SCRIPT_DIR}/infrastructure/vault"
    mkdir -p "${SCRIPT_DIR}/infrastructure/monitoring"
    mkdir -p "${SCRIPT_DIR}/infrastructure/grafana/provisioning/datasources"
    mkdir -p "${SCRIPT_DIR}/infrastructure/grafana/provisioning/dashboards"
    mkdir -p "${SCRIPT_DIR}/infrastructure/grafana/dashboards"
    mkdir -p "${SCRIPT_DIR}/infrastructure/logstash"
    
    log_success "Directories created"
}

create_redis_config() {
    cat > "${SCRIPT_DIR}/infrastructure/redis/redis-security.conf" << 'EOF'
# Redis Security Configuration for BizOSaaS

# Network security
bind 0.0.0.0
protected-mode yes
port 6379

# Memory and performance
maxmemory 512mb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000

# Security
# requirepass your_redis_password_here
# rename-command FLUSHDB ""
# rename-command FLUSHALL ""
# rename-command DEBUG ""
# rename-command CONFIG ""
# rename-command SHUTDOWN ""
# rename-command EVAL ""

# Logging
loglevel notice
logfile /var/log/redis.log

# Slow log
slowlog-log-slower-than 10000
slowlog-max-len 128

# Client management
timeout 300
tcp-keepalive 300
tcp-backlog 511
EOF
    
    log_success "Redis configuration created"
}

create_monitoring_config() {
    # Prometheus configuration
    cat > "${SCRIPT_DIR}/infrastructure/monitoring/prometheus-security.yml" << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert-rules.yml"

scrape_configs:
  - job_name: 'auth-service'
    static_configs:
      - targets: ['auth-service:8003']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'saleor-proxy'
    static_configs:
      - targets: ['saleor-proxy:9021']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'security-dashboard'
    static_configs:
      - targets: ['security-dashboard:8004']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']
    scrape_interval: 60s

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
    scrape_interval: 60s
EOF

    # Alert rules
    cat > "${SCRIPT_DIR}/infrastructure/monitoring/alert-rules.yml" << 'EOF'
groups:
  - name: security-alerts
    rules:
      - alert: HighFailedLoginRate
        expr: rate(failed_logins_total[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High failed login rate detected"
          description: "Failed login rate is {{ $value }} per second"

      - alert: SuspiciousActivity
        expr: security_risk_score > 75
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Suspicious security activity detected"
          description: "Security risk score is {{ $value }}"

      - alert: AuthServiceDown
        expr: up{job="auth-service"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Authentication service is down"
          description: "Auth service has been down for more than 1 minute"
EOF

    # Grafana datasource
    cat > "${SCRIPT_DIR}/infrastructure/grafana/provisioning/datasources/prometheus.yml" << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false
EOF

    # Grafana dashboard provisioning
    cat > "${SCRIPT_DIR}/infrastructure/grafana/provisioning/dashboards/security.yml" << 'EOF'
apiVersion: 1

providers:
  - name: 'security-dashboards'
    orgId: 1
    folder: 'Security'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
EOF
    
    log_success "Monitoring configuration created"
}

update_hosts_file() {
    log_info "Updating hosts file for local development..."
    
    # Check if entries already exist
    if ! grep -q "bizosaas.local" /etc/hosts 2>/dev/null; then
        log_info "Adding entries to /etc/hosts (requires sudo)..."
        
        if command -v sudo &> /dev/null; then
            echo "127.0.0.1 bizosaas.local" | sudo tee -a /etc/hosts > /dev/null
            echo "127.0.0.1 saleor.bizosaas.local" | sudo tee -a /etc/hosts > /dev/null
            echo "127.0.0.1 dashboard.bizosaas.local" | sudo tee -a /etc/hosts > /dev/null
            log_success "Hosts file updated"
        else
            log_warning "sudo not available. Please manually add these entries to /etc/hosts:"
            echo "127.0.0.1 bizosaas.local"
            echo "127.0.0.1 saleor.bizosaas.local" 
            echo "127.0.0.1 dashboard.bizosaas.local"
        fi
    else
        log_info "Hosts file entries already exist"
    fi
}

deploy_services() {
    log_info "Deploying BizOSaaS security services..."
    
    # Pull latest images
    docker-compose -f "$DOCKER_COMPOSE_FILE" pull
    
    # Build and start services
    docker-compose -f "$DOCKER_COMPOSE_FILE" up --build -d
    
    log_success "Services deployed successfully"
}

wait_for_services() {
    log_info "Waiting for services to be ready..."
    
    # Wait for database
    log_info "Waiting for PostgreSQL..."
    until docker-compose -f "$DOCKER_COMPOSE_FILE" exec -T postgres pg_isready -U admin -d bizosaas; do
        sleep 2
    done
    
    # Wait for Redis
    log_info "Waiting for Redis..."
    until docker-compose -f "$DOCKER_COMPOSE_FILE" exec -T redis redis-cli ping | grep -q PONG; do
        sleep 2
    done
    
    # Wait for auth service
    log_info "Waiting for Auth Service..."
    until curl -f http://localhost:8003/health &>/dev/null; do
        sleep 5
    done
    
    # Wait for Saleor proxy
    log_info "Waiting for Saleor Proxy..."
    until curl -f http://localhost:9021/health &>/dev/null; do
        sleep 5
    done
    
    # Wait for security dashboard
    log_info "Waiting for Security Dashboard..."
    until curl -f http://localhost:8004/health &>/dev/null; do
        sleep 5
    done
    
    log_success "All services are ready"
}

run_security_tests() {
    log_info "Running basic security tests..."
    
    # Test auth endpoints
    log_info "Testing authentication endpoints..."
    
    # Health checks
    if curl -f http://localhost:8003/health &>/dev/null; then
        log_success "✓ Auth service health check passed"
    else
        log_error "✗ Auth service health check failed"
    fi
    
    if curl -f http://localhost:9021/health &>/dev/null; then
        log_success "✓ Saleor proxy health check passed"
    else
        log_error "✗ Saleor proxy health check failed"
    fi
    
    if curl -f http://localhost:8004/health &>/dev/null; then
        log_success "✓ Security dashboard health check passed"
    else
        log_error "✗ Security dashboard health check failed"
    fi
    
    log_success "Security tests completed"
}

show_access_info() {
    log_success "🛡️ BizOSaaS Security System Deployed Successfully!"
    echo
    echo -e "${GREEN}Access Points:${NC}"
    echo "🔐 Authentication API:    http://localhost:8003/api/auth/"
    echo "🛡️ Saleor Proxy:         http://localhost:9021/saleor/"
    echo "📊 Security Dashboard:   http://localhost:8004/"
    echo "🖥️  Grafana:             http://localhost:3001/ (admin:admin123)"
    echo "📈 Prometheus:           http://localhost:9090/"
    echo "🔒 Vault:               http://localhost:8200/ (token:myroot)"
    echo
    echo -e "${GREEN}HTTPS Access (Development):${NC}"
    echo "🌐 Main Site:            https://bizosaas.local/"
    echo "🛒 Saleor:              https://saleor.bizosaas.local/"
    echo "🛡️ Security Dashboard:   https://dashboard.bizosaas.local/"
    echo
    echo -e "${GREEN}Key Features:${NC}"
    echo "✓ Multi-factor authentication (TOTP)"
    echo "✓ Role-based access control (RBAC)"  
    echo "✓ Session management with hijacking protection"
    echo "✓ Password policy enforcement"
    echo "✓ Rate limiting and brute force protection"
    echo "✓ Comprehensive security audit logging"
    echo "✓ Real-time threat detection"
    echo "✓ Secure Saleor dashboard proxy"
    echo "✓ API key management for service-to-service auth"
    echo "✓ Security monitoring and alerting"
    echo
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "1. Update .env file with secure production values"
    echo "2. Create user accounts via API: POST http://localhost:8003/api/auth/register"
    echo "3. Configure MFA for admin users"
    echo "4. Review security dashboard for any alerts"
    echo "5. Set up proper SSL certificates for production"
    echo
    echo -e "${BLUE}Documentation:${NC}"
    echo "📚 API Documentation: http://localhost:8003/docs (when available)"
    echo "🔧 Admin Guide: Check the README.md for detailed usage instructions"
}

cleanup_on_error() {
    log_error "Deployment failed. Cleaning up..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" down --remove-orphans
    exit 1
}

# Main execution
main() {
    echo -e "${BLUE}🚀 BizOSaaS Secure Authentication System Deployment${NC}"
    echo "=================================================="
    echo
    
    # Set error trap
    trap cleanup_on_error ERR
    
    check_prerequisites
    create_directories
    generate_ssl_certificates
    create_redis_config
    create_monitoring_config
    update_hosts_file
    deploy_services
    wait_for_services
    run_security_tests
    show_access_info
    
    log_success "🎉 Deployment completed successfully!"
}

# Handle script arguments
case "${1:-}" in
    "stop")
        log_info "Stopping BizOSaaS security services..."
        docker-compose -f "$DOCKER_COMPOSE_FILE" down
        log_success "Services stopped"
        ;;
    "restart")
        log_info "Restarting BizOSaaS security services..."
        docker-compose -f "$DOCKER_COMPOSE_FILE" restart
        log_success "Services restarted"
        ;;
    "logs")
        docker-compose -f "$DOCKER_COMPOSE_FILE" logs -f "${2:-}"
        ;;
    "status")
        docker-compose -f "$DOCKER_COMPOSE_FILE" ps
        ;;
    "clean")
        log_warning "This will remove all containers, volumes, and data. Are you sure? (y/N)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            docker-compose -f "$DOCKER_COMPOSE_FILE" down --volumes --remove-orphans
            docker system prune -f
            log_success "Cleanup completed"
        else
            log_info "Cleanup cancelled"
        fi
        ;;
    *)
        main
        ;;
esac