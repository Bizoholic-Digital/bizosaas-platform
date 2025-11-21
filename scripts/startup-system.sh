#!/bin/bash
# BizOSaaS Platform Startup Script
# Ensures all required containers are up and running with proper dependencies
# Author: Claude AI Assistant
# Created: 2025-09-29

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

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configuration
COMPOSE_FILE="/home/alagiri/projects/bizoholic/bizosaas/docker-compose.bizosaas-platform.yml"
PROJECT_NAME="bizosaas-platform"
HEALTH_CHECK_TIMEOUT=300  # 5 minutes
HEALTH_CHECK_INTERVAL=10  # 10 seconds

# Required external services (should be running on host)
EXTERNAL_SERVICES=(
    "postgresql:5432"
    "redis:6379"
)

# Core infrastructure services (start first)
CORE_SERVICES=(
    "bizosaas-saleor-db"
    "bizosaas-saleor-redis"
    "bizosaas-superset-db"
)

# Backend services (start after core)
BACKEND_SERVICES=(
    "bizosaas-brain"
    "bizosaas-auth-v2"
    "bizosaas-django-crm"
    "bizosaas-crm-celery-worker"
    "bizosaas-crm-celery-beat"
    "bizosaas-wagtail-cms"
    "bizosaas-saleor-api"
    "bizosaas-saleor-worker"
    "bizosaas-superset"
    "bizosaas-vault"
    "bizosaas-data-sync"
)

# Frontend services (start last)
FRONTEND_SERVICES=(
    "bizosaas-client-portal"
    "bizosaas-coreldove-frontend"
    "bizosaas-bizoholic-frontend"
    "bizosaas-admin"
)

# Development services (optional)
DEV_SERVICES=(
    "bizosaas-client-portal-3000"
    "bizosaas-coreldove-frontend-dev-3002"
    "bizosaas-bizoholic-frontend-dev-3001"
    "bizosaas-business-directory-frontend-3004"
    "bizosaas-business-directory-backend-8004"
    "amazon-sourcing-8085"
    "bizosaas-ai-agents-8010"
    "bizosaas-admin-3009-ai"
)

# Function to check if external service is available
check_external_service() {
    local service=$1
    local host=$(echo $service | cut -d: -f1)
    local port=$(echo $service | cut -d: -f2)
    
    if nc -z localhost $port 2>/dev/null; then
        log_success "External service $service is available"
        return 0
    else
        log_error "External service $service is not available at localhost:$port"
        return 1
    fi
}

# Function to check container health
check_container_health() {
    local container_name=$1
    local timeout=$2
    local interval=$3
    
    log "Checking health of $container_name..."
    
    local elapsed=0
    while [ $elapsed -lt $timeout ]; do
        if docker ps --filter "name=$container_name" --filter "status=running" | grep -q $container_name; then
            # Check if container has health check
            local health_status=$(docker inspect --format='{{.State.Health.Status}}' $container_name 2>/dev/null || echo "none")
            
            if [ "$health_status" = "healthy" ]; then
                log_success "$container_name is healthy"
                return 0
            elif [ "$health_status" = "none" ]; then
                log_success "$container_name is running (no health check)"
                return 0
            elif [ "$health_status" = "unhealthy" ]; then
                log_warning "$container_name is unhealthy, continuing..."
                return 1
            else
                log "Waiting for $container_name to become healthy... ($health_status)"
            fi
        else
            log "Waiting for $container_name to start..."
        fi
        
        sleep $interval
        elapsed=$((elapsed + interval))
    done
    
    log_error "$container_name failed to become healthy within $timeout seconds"
    return 1
}

# Function to start service group
start_service_group() {
    local group_name=$1
    shift
    local services=("$@")
    
    log "Starting $group_name services..."
    
    for service in "${services[@]}"; do
        log "Starting $service..."
        
        # Check if container exists
        if docker ps -a --filter "name=$service" | grep -q $service; then
            # Container exists, restart it
            docker restart $service
        else
            # Container doesn't exist, try to create from compose
            docker-compose -f $COMPOSE_FILE up -d $service 2>/dev/null || {
                log_warning "Could not start $service from compose file"
                continue
            }
        fi
        
        # Wait for container to be healthy
        check_container_health $service 60 5 || {
            log_warning "Service $service may not be fully healthy, continuing..."
        }
    done
    
    log_success "$group_name services startup completed"
}

# Function to stop all services
stop_all_services() {
    log "Stopping all BizOSaaS services..."
    docker-compose -f $COMPOSE_FILE down
    
    # Stop any remaining containers
    docker stop $(docker ps -a --filter "name=bizosaas-" --format "{{.Names}}") 2>/dev/null || true
    docker stop $(docker ps -a --filter "name=amazon-sourcing" --format "{{.Names}}") 2>/dev/null || true
    
    log_success "All services stopped"
}

# Function to show service status
show_status() {
    log "Current service status:"
    echo
    docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}" --filter "name=bizosaas-"
    echo
    docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}" --filter "name=amazon-sourcing"
}

# Function to check logs
check_logs() {
    local service=$1
    if [ -z "$service" ]; then
        log "Available services for log checking:"
        docker ps --format "{{.Names}}" --filter "name=bizosaas-" | head -10
        return
    fi
    
    log "Showing logs for $service..."
    docker logs --tail 50 $service
}

# Main startup function
start_platform() {
    log "=== BizOSaaS Platform Startup ==="
    
    # Check external dependencies
    log "Checking external dependencies..."
    local external_ok=true
    for service in "${EXTERNAL_SERVICES[@]}"; do
        check_external_service $service || external_ok=false
    done
    
    if [ "$external_ok" = false ]; then
        log_error "Some external services are not available. Please ensure PostgreSQL and Redis are running."
        log "You can start them with:"
        log "  sudo systemctl start postgresql"
        log "  sudo systemctl start redis"
        exit 1
    fi
    
    # Create docker network if it doesn't exist
    docker network create bizosaas-platform-network 2>/dev/null || true
    
    # Start services in dependency order
    start_service_group "Core Infrastructure" "${CORE_SERVICES[@]}"
    sleep 10  # Allow core services to fully initialize
    
    start_service_group "Backend Services" "${BACKEND_SERVICES[@]}"
    sleep 15  # Allow backend services to initialize
    
    start_service_group "Frontend Services" "${FRONTEND_SERVICES[@]}"
    
    # Optionally start development services
    if [ "$1" = "--with-dev" ]; then
        log "Starting development services..."
        start_service_group "Development Services" "${DEV_SERVICES[@]}"
    fi
    
    log_success "=== Platform startup completed ==="
    show_status
}

# Main script logic
case "${1:-start}" in
    "start")
        start_platform
        ;;
    "start-dev")
        start_platform --with-dev
        ;;
    "stop")
        stop_all_services
        ;;
    "restart")
        stop_all_services
        sleep 5
        start_platform
        ;;
    "status")
        show_status
        ;;
    "logs")
        check_logs $2
        ;;
    "health")
        log "Performing health check..."
        ALL_HEALTHY=true
        
        # Check core services
        for service in "${BACKEND_SERVICES[@]}"; do
            if ! check_container_health $service 30 5; then
                ALL_HEALTHY=false
            fi
        done
        
        if [ "$ALL_HEALTHY" = true ]; then
            log_success "All services are healthy"
            exit 0
        else
            log_error "Some services are unhealthy"
            exit 1
        fi
        ;;
    "help"|"-h"|"--help")
        echo "BizOSaaS Platform Startup Script"
        echo
        echo "Usage: $0 [COMMAND] [OPTIONS]"
        echo
        echo "Commands:"
        echo "  start       Start the platform (default)"
        echo "  start-dev   Start platform with development services"
        echo "  stop        Stop all services"
        echo "  restart     Restart all services"
        echo "  status      Show current service status"
        echo "  health      Perform health check"
        echo "  logs [SERVICE]  Show logs for a service"
        echo "  help        Show this help message"
        echo
        echo "Examples:"
        echo "  $0 start           # Start core platform"
        echo "  $0 start-dev       # Start with development services"
        echo "  $0 logs bizosaas-brain-8001  # Show brain service logs"
        ;;
    *)
        log_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac