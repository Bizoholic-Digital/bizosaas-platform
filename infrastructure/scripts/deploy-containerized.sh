#!/bin/bash

# BizOSaaS Enhanced Containerized Deployment Script
# Deploys the complete Autonomous AI Agents Platform with Docker Compose

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if Docker and Docker Compose are installed
check_dependencies() {
    log "Checking dependencies..."
    
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    success "Dependencies check passed"
}

# Create database initialization script
create_db_init() {
    log "Creating database initialization script..."
    
    mkdir -p database
    
    cat > database/init-databases.sql << EOF
-- BizOSaaS Database Initialization Script
-- Creates all required databases with proper extensions

-- Main BizOSaaS database
CREATE DATABASE bizoholic;
\c bizoholic;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Wagtail CMS database
CREATE DATABASE wagtail;
\c wagtail;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Saleor E-commerce database
CREATE DATABASE saleor;
\c saleor;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "hstore";

-- Grant permissions
\c bizoholic;
GRANT ALL PRIVILEGES ON DATABASE bizoholic TO admin;
\c wagtail;
GRANT ALL PRIVILEGES ON DATABASE wagtail TO admin;
\c saleor;
GRANT ALL PRIVILEGES ON DATABASE saleor TO admin;

-- Create default tenant for demo
\c bizoholic;
INSERT INTO tenants (id, name, tier, created_at) 
VALUES ('00000000-0000-4000-8000-000000000001', 'Default Tenant', 'tier_1', NOW())
ON CONFLICT (id) DO NOTHING;
EOF
    
    success "Database initialization script created"
}

# Build all Docker images
build_images() {
    log "Building Docker images..."
    
    # Build images with better caching
    docker-compose -f docker-compose.enhanced.yml build --parallel --progress=plain
    
    success "Docker images built successfully"
}

# Start services in proper order
start_services() {
    log "Starting BizOSaaS services..."
    
    # Start infrastructure services first
    log "Starting infrastructure services..."
    docker-compose -f docker-compose.enhanced.yml up -d \
        bizosaas-postgres \
        bizosaas-redis \
        bizosaas-vault
    
    # Wait for infrastructure to be ready
    log "Waiting for infrastructure services to be healthy..."
    sleep 30
    
    # Start core services
    log "Starting core services..."
    docker-compose -f docker-compose.enhanced.yml up -d \
        bizosaas-event-bus \
        bizosaas-domain-repository \
        bizosaas-vault-service \
        bizosaas-temporal
    
    # Wait for core services
    sleep 20
    
    # Start application services
    log "Starting application services..."
    docker-compose -f docker-compose.enhanced.yml up -d \
        bizosaas-ai-agents \
        bizosaas-crm \
        bizosaas-wagtail-cms
    
    # Wait for application services
    sleep 15
    
    # Start API Gateway (depends on all backend services)
    log "Starting API Gateway..."
    docker-compose -f docker-compose.enhanced.yml up -d bizosaas-api-gateway
    
    # Wait for API Gateway
    sleep 10
    
    # Start frontend services
    log "Starting frontend services..."
    docker-compose -f docker-compose.enhanced.yml up -d \
        bizosaas-dashboard \
        bizosaas-saleor \
        bizosaas-business-directory
    
    # Start reverse proxy last
    log "Starting reverse proxy..."
    docker-compose -f docker-compose.enhanced.yml up -d bizosaas-traefik
    
    success "All services started successfully"
}

# Check service health
check_health() {
    log "Checking service health..."
    
    # Wait a bit more for all services to fully initialize
    sleep 30
    
    # Check critical service endpoints
    services=(
        "API Gateway:http://localhost:8080/health"
        "AI Agents:http://localhost:8001/health"
        "CRM Service:http://localhost:8007/health"
        "Event Bus:http://localhost:8009/health"
        "Domain Repository:http://localhost:8011/health"
        "Vault Service:http://localhost:8201/health"
        "Dashboard:http://localhost:3001"
        "Traefik:http://localhost:8888"
    )
    
    healthy_count=0
    total_services=${#services[@]}
    
    for service_info in "${services[@]}"; do
        name=$(echo "$service_info" | cut -d: -f1)
        url=$(echo "$service_info" | cut -d: -f2-)
        
        if curl -f -s --max-time 10 "$url" >/dev/null 2>&1; then
            success "$name is healthy"
            ((healthy_count++))
        else
            warning "$name is not responding at $url"
        fi
    done
    
    log "Health check complete: $healthy_count/$total_services services healthy"
    
    if [ $healthy_count -eq $total_services ]; then
        success "All services are healthy!"
    else
        warning "Some services may need more time to start up"
    fi
}

# Display service URLs
display_urls() {
    log "BizOSaaS Platform Services:"
    echo
    echo -e "${GREEN}=== Core Services ===${NC}"
    echo "API Gateway:         http://localhost:8080"
    echo "AI Agents:          http://localhost:8001"
    echo "CRM Service:        http://localhost:8007"
    echo "Event Bus:          http://localhost:8009"
    echo "Domain Repository:  http://localhost:8011"
    echo "Vault Service:      http://localhost:8201"
    echo
    echo -e "${GREEN}=== Frontend Services ===${NC}"
    echo "Unified Dashboard:  http://localhost:3001"
    echo "Wagtail CMS:       http://localhost:8006/admin/"
    echo "Saleor GraphQL:    http://localhost:8020/graphql/"
    echo "Business Directory: http://localhost:8003"
    echo
    echo -e "${GREEN}=== Infrastructure ===${NC}"
    echo "Traefik Dashboard:  http://localhost:8888"
    echo "Vault UI:          http://localhost:8200/ui/"
    echo "PostgreSQL:        localhost:5433"
    echo "Redis:             localhost:6379"
    echo
    echo -e "${GREEN}=== Credentials ===${NC}"
    echo "Database: admin / BizoholicSecure2025"
    echo "Vault Token: myroot"
    echo "Default Tenant ID: 00000000-0000-4000-8000-000000000001"
    echo
    echo -e "${BLUE}Access the unified dashboard at: http://localhost:3001/dashboard${NC}"
}

# Clean up function
cleanup() {
    log "Stopping all services..."
    docker-compose -f docker-compose.enhanced.yml down
    success "Cleanup complete"
}

# Main execution
main() {
    log "Starting BizOSaaS Enhanced Containerized Deployment"
    
    # Parse arguments
    case "${1:-deploy}" in
        "deploy")
            check_dependencies
            create_db_init
            build_images
            start_services
            check_health
            display_urls
            ;;
        "stop")
            cleanup
            ;;
        "restart")
            cleanup
            sleep 5
            main deploy
            ;;
        "logs")
            docker-compose -f docker-compose.enhanced.yml logs -f "${2:-}"
            ;;
        "status")
            docker-compose -f docker-compose.enhanced.yml ps
            ;;
        "health")
            check_health
            ;;
        *)
            echo "Usage: $0 {deploy|stop|restart|logs|status|health}"
            echo
            echo "Commands:"
            echo "  deploy   - Deploy the complete platform"
            echo "  stop     - Stop all services"
            echo "  restart  - Restart the platform"
            echo "  logs     - View logs (optional: specify service name)"
            echo "  status   - Show service status"
            echo "  health   - Check service health"
            exit 1
            ;;
    esac
}

# Trap to handle cleanup on script exit
trap 'error "Deployment interrupted"' INT TERM

# Run main function
main "$@"