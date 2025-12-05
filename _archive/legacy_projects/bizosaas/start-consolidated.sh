#!/bin/bash

# BizOSaaS Platform - Consolidated Stack Management Script
# Manages single unified Docker Compose stack for optimal resource usage

set -e

COMPOSE_FILE="docker-compose.consolidated.yml"
PROJECT_NAME="bizosaas-consolidated"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Stop any conflicting containers from other compose files
stop_conflicting_containers() {
    print_status "Stopping conflicting containers..."
    
    # List of containers that might conflict
    CONFLICTING_CONTAINERS=(
        "bizosaas-postgres-5432"
        "bizosaas-redis-6379" 
        "bizosaas-saleor-db-5433"
        "bizosaas-saleor-redis-6380"
        "bizosaas-auth-v2-8007"
        "bizosaas-brain-8001"
        "wagtail-cms-8006"
        "bizosaas-admin-3000"
        "bizosaas-traefik-80"
        "sqladmin-dashboard"
    )
    
    for container in "${CONFLICTING_CONTAINERS[@]}"; do
        if docker ps -a --format '{{.Names}}' | grep -q "^${container}$"; then
            print_warning "Stopping conflicting container: $container"
            docker stop "$container" 2>/dev/null || true
            docker rm "$container" 2>/dev/null || true
        fi
    done
}

# Function to start the consolidated stack
start_stack() {
    print_status "Starting BizOSaaS Consolidated Platform..."
    
    # Stop conflicting containers first
    stop_conflicting_containers
    
    # Start the consolidated stack
    print_status "Launching consolidated services..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up -d
    
    # Wait for health checks
    print_status "Waiting for services to become healthy..."
    sleep 10
    
    # Check service status
    check_services
}

# Function to stop the stack
stop_stack() {
    print_status "Stopping BizOSaaS Consolidated Platform..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" down
    print_success "All services stopped"
}

# Function to check service health
check_services() {
    print_status "Checking service health..."
    
    SERVICES=(
        "postgres:5432"
        "redis:6379" 
        "bizosaas-brain:8001"
        "auth-service:8007"
        "wagtail-cms:8006"
        "saleor-api:8003"
        "temporal:7233"
        "temporal-ui:8082"
        "elasticsearch:9200"
        "superset:8088"
        "admin-dashboard:3000"
    )
    
    echo ""
    echo "=== SERVICE STATUS ==="
    
    for service in "${SERVICES[@]}"; do
        name="${service%:*}"
        port="${service#*:}"
        
        if curl -s --max-time 5 "localhost:$port" > /dev/null 2>&1; then
            print_success "$name (localhost:$port) - HEALTHY"
        else
            print_error "$name (localhost:$port) - UNHEALTHY"
        fi
    done
    
    echo ""
    echo "=== QUICK ACCESS URLS ==="
    echo "🧠 BizOSaaS Brain API:     http://localhost:8001"
    echo "🔐 Authentication:         http://localhost:8007"
    echo "📝 Wagtail CMS:           http://localhost:8006/admin"
    echo "🛒 Saleor E-commerce:     http://localhost:8003/graphql/"
    echo "⏱️  Temporal UI:           http://localhost:8082"
    echo "🔍 Elasticsearch:         http://localhost:9200"
    echo "📊 Apache Superset:       http://localhost:8088"
    echo "👨‍💼 Admin Dashboard:        http://localhost:3000"
    echo ""
}

# Function to show logs
show_logs() {
    if [ -n "$1" ]; then
        docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" logs -f "$1"
    else
        docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" logs -f
    fi
}

# Function to restart a specific service
restart_service() {
    if [ -n "$1" ]; then
        print_status "Restarting service: $1"
        docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" restart "$1"
        print_success "Service $1 restarted"
    else
        print_error "Please specify a service name"
        exit 1
    fi
}

# Main command handling
case "$1" in
    start)
        start_stack
        ;;
    stop)
        stop_stack
        ;;
    restart)
        stop_stack
        sleep 3
        start_stack
        ;;
    status)
        check_services
        ;;
    logs)
        show_logs "$2"
        ;;
    restart-service)
        restart_service "$2"
        ;;
    cleanup)
        print_warning "This will remove all containers and volumes. Are you sure? (y/N)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" down -v
            print_success "Cleanup completed"
        fi
        ;;
    *)
        echo "BizOSaaS Consolidated Platform Management"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|logs|restart-service|cleanup}"
        echo ""
        echo "Commands:"
        echo "  start              Start the consolidated platform"
        echo "  stop               Stop all services"
        echo "  restart            Restart the entire platform"
        echo "  status             Check service health"
        echo "  logs [service]     Show logs (all services or specific service)"
        echo "  restart-service    Restart a specific service"
        echo "  cleanup            Remove all containers and volumes (destructive)"
        echo ""
        echo "Examples:"
        echo "  $0 start"
        echo "  $0 logs postgres"
        echo "  $0 restart-service auth-service"
        exit 1
        ;;
esac