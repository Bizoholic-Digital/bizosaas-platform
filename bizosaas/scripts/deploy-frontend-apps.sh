#!/bin/bash

# BizOSaaS Frontend Applications - Deployment Script
# Deploys all 4 frontend applications with the platform services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Configuration
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.bizosaas-platform.yml}"
PROJECT_NAME="${PROJECT_NAME:-bizosaas-platform}"
BUILD_IMAGES="${BUILD_IMAGES:-true}"
HEALTH_CHECK_TIMEOUT="${HEALTH_CHECK_TIMEOUT:-300}"

# Frontend applications to deploy
declare -A FRONTEND_APPS=(
    ["bizosaas-client-portal"]="3006"
    ["bizosaas-coreldove-frontend"]="3007"
    ["bizosaas-bizoholic-frontend"]="3008"
    ["bizosaas-admin-dashboard"]="3009"
)

log "Starting BizOSaaS Frontend Applications Deployment"
log "Compose file: $COMPOSE_FILE"
log "Project name: $PROJECT_NAME"

# Check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Check if Docker Compose file exists
check_compose_file() {
    if [ ! -f "$COMPOSE_FILE" ]; then
        error "Docker Compose file $COMPOSE_FILE not found"
        exit 1
    fi
}

# Check environment file
check_environment() {
    if [ ! -f ".env" ]; then
        warn ".env file not found. Using default environment variables."
        info "Consider copying .env.example to .env and configuring your settings."
    else
        log "Using environment variables from .env file"
    fi
}

# Build frontend images if needed
build_images() {
    if [ "$BUILD_IMAGES" = "true" ]; then
        log "Building frontend application images"
        
        if [ -f "scripts/build-frontend-apps.sh" ]; then
            info "Running build script"
            ./scripts/build-frontend-apps.sh
        else
            info "Building with Docker Compose"
            docker-compose -f "$COMPOSE_FILE" build \
                bizosaas-client-portal \
                bizosaas-coreldove-frontend \
                bizosaas-bizoholic-frontend \
                bizosaas-admin-dashboard
        fi
    else
        log "Skipping image build (BUILD_IMAGES=false)"
    fi
}

# Create required networks
create_networks() {
    log "Creating required networks"
    
    if ! docker network ls | grep -q "bizosaas-platform-network"; then
        docker network create bizosaas-platform-network
        log "Created bizosaas-platform-network"
    else
        info "Network bizosaas-platform-network already exists"
    fi
}

# Check service health
check_service_health() {
    local service_name=$1
    local port=$2
    local max_attempts=30
    local attempt=1
    
    log "Checking health of $service_name on port $port"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "http://localhost:$port/api/health" >/dev/null 2>&1; then
            log "$service_name is healthy"
            return 0
        fi
        
        info "Attempt $attempt/$max_attempts: $service_name not ready yet..."
        sleep 10
        ((attempt++))
    done
    
    error "$service_name failed health check after $max_attempts attempts"
    return 1
}

# Deploy services
deploy_services() {
    log "Deploying BizOSaaS platform with frontend applications"
    
    # Pull latest images
    if [ "$BUILD_IMAGES" != "true" ]; then
        log "Pulling latest images"
        docker-compose -f "$COMPOSE_FILE" pull
    fi
    
    # Deploy services
    log "Starting services"
    docker-compose -f "$COMPOSE_FILE" up -d
    
    # Wait for services to be ready
    log "Waiting for services to be ready..."
    sleep 30
    
    # Check health of backend services first
    log "Checking backend services health"
    check_service_health "Brain API" "8001" || true
    check_service_health "Auth Service" "8007" || true
    
    # Check health of frontend applications
    log "Checking frontend applications health"
    local failed_services=()
    
    for service_name in "${!FRONTEND_APPS[@]}"; do
        local port=${FRONTEND_APPS[$service_name]}
        if check_service_health "$service_name" "$port"; then
            log "✓ $service_name is healthy"
        else
            error "✗ $service_name failed health check"
            failed_services+=("$service_name")
        fi
    done
    
    if [ ${#failed_services[@]} -gt 0 ]; then
        error "Some services failed health checks: ${failed_services[*]}"
        log "Check service logs with: docker-compose -f $COMPOSE_FILE logs <service-name>"
        return 1
    fi
    
    log "All frontend applications are healthy!"
}

# Display service information
show_service_info() {
    log "BizOSaaS Frontend Applications Deployment Summary"
    echo
    info "Frontend Applications:"
    echo "┌─────────────────────────────┬──────┬─────────────────────────────────┐"
    echo "│ Service                     │ Port │ URL                             │"
    echo "├─────────────────────────────┼──────┼─────────────────────────────────┤"
    echo "│ Client Portal               │ 3006 │ http://localhost:3006           │"
    echo "│ CoreLDove E-commerce        │ 3007 │ http://localhost:3007           │"
    echo "│ Bizoholic Marketing         │ 3008 │ http://localhost:3008           │"
    echo "│ BizOSaaS Admin Dashboard    │ 3009 │ http://localhost:3009           │"
    echo "└─────────────────────────────┴──────┴─────────────────────────────────┘"
    echo
    
    info "Backend Services:"
    echo "┌─────────────────────────────┬──────┬─────────────────────────────────┐"
    echo "│ Service                     │ Port │ URL                             │"
    echo "├─────────────────────────────┼──────┼─────────────────────────────────┤"
    echo "│ Brain API Gateway           │ 8001 │ http://localhost:8001           │"
    echo "│ Auth Service v2             │ 8007 │ http://localhost:8007           │"
    echo "│ Django CRM                  │ 8008 │ http://localhost:8008           │"
    echo "│ Wagtail CMS                 │ 8006 │ http://localhost:8006           │"
    echo "│ Saleor E-commerce API       │ 8024 │ http://localhost:8024           │"
    echo "│ Apache Superset Analytics   │ 8088 │ http://localhost:8088           │"
    echo "│ HashiCorp Vault             │ 8200 │ http://localhost:8200           │"
    echo "└─────────────────────────────┴──────┴─────────────────────────────────┘"
    echo
    
    info "Useful Commands:"
    echo "  View logs:           docker-compose -f $COMPOSE_FILE logs <service-name>"
    echo "  View all logs:       docker-compose -f $COMPOSE_FILE logs -f"
    echo "  Restart service:     docker-compose -f $COMPOSE_FILE restart <service-name>"
    echo "  Stop all services:   docker-compose -f $COMPOSE_FILE down"
    echo "  Service status:      docker-compose -f $COMPOSE_FILE ps"
    echo
    
    info "Health Check URLs:"
    for service_name in "${!FRONTEND_APPS[@]}"; do
        local port=${FRONTEND_APPS[$service_name]}
        echo "  $service_name: http://localhost:$port/api/health"
    done
}

# Clean up function
cleanup_on_error() {
    error "Deployment failed. Cleaning up..."
    docker-compose -f "$COMPOSE_FILE" down
    exit 1
}

# Main deployment process
main() {
    # Set trap for cleanup on error
    trap cleanup_on_error ERR
    
    check_docker
    check_compose_file
    check_environment
    create_networks
    
    if [ "$BUILD_IMAGES" = "true" ]; then
        build_images
    fi
    
    deploy_services
    show_service_info
    
    log "BizOSaaS Frontend Applications deployed successfully!"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --compose-file)
            COMPOSE_FILE="$2"
            shift 2
            ;;
        --project-name)
            PROJECT_NAME="$2"
            shift 2
            ;;
        --no-build)
            BUILD_IMAGES="false"
            shift
            ;;
        --timeout)
            HEALTH_CHECK_TIMEOUT="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --compose-file FILE    Docker Compose file (default: docker-compose.bizosaas-platform.yml)"
            echo "  --project-name NAME    Project name (default: bizosaas-platform)"
            echo "  --no-build             Skip building images"
            echo "  --timeout SECONDS      Health check timeout (default: 300)"
            echo "  --help                 Show this help message"
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run main deployment process
main