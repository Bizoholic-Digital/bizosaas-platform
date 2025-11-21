#!/bin/bash

# Supplier Validation Workflow [P9] Deployment Script
# This script sets up and deploys the Supplier Validation service

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SERVICE_NAME="supplier-validation"
SERVICE_PORT="8027"
DOCKER_IMAGE="bizosaas/supplier-validation:latest"
NETWORK_NAME="bizosaas-network"

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Check if Docker is installed and running
check_docker() {
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    log "Docker is installed and running"
}

# Check if Docker Compose is available
check_docker_compose() {
    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
    elif docker compose version &> /dev/null; then
        COMPOSE_CMD="docker compose"
    else
        error "Docker Compose is not available. Please install Docker Compose."
        exit 1
    fi
    
    log "Docker Compose is available: $COMPOSE_CMD"
}

# Create necessary directories
create_directories() {
    log "Creating necessary directories..."
    
    mkdir -p uploads
    mkdir -p logs
    mkdir -p data/postgres
    mkdir -p data/redis
    mkdir -p data/minio
    
    # Set permissions
    chmod 755 uploads logs
    chmod 777 data/postgres data/redis data/minio
    
    log "Directories created successfully"
}

# Copy environment file if it doesn't exist
setup_environment() {
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            log "Copying .env.example to .env"
            cp .env.example .env
            warning "Please update .env file with your configuration before starting the service"
        else
            error ".env.example file not found"
            exit 1
        fi
    else
        log "Environment file (.env) already exists"
    fi
}

# Build Docker image
build_image() {
    log "Building Docker image..."
    
    docker build -t $DOCKER_IMAGE . || {
        error "Failed to build Docker image"
        exit 1
    }
    
    log "Docker image built successfully: $DOCKER_IMAGE"
}

# Create Docker network if it doesn't exist
create_network() {
    if ! docker network ls | grep -q $NETWORK_NAME; then
        log "Creating Docker network: $NETWORK_NAME"
        docker network create $NETWORK_NAME || {
            warning "Failed to create network $NETWORK_NAME (it might already exist)"
        }
    else
        log "Docker network $NETWORK_NAME already exists"
    fi
}

# Start services with Docker Compose
start_services() {
    log "Starting services with Docker Compose..."
    
    $COMPOSE_CMD up -d || {
        error "Failed to start services"
        exit 1
    }
    
    log "Services started successfully"
}

# Wait for services to be healthy
wait_for_services() {
    log "Waiting for services to be healthy..."
    
    # Wait for database
    info "Waiting for PostgreSQL..."
    for i in {1..30}; do
        if docker exec supplier-validation-postgres pg_isready -U postgres &> /dev/null; then
            log "PostgreSQL is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            error "PostgreSQL failed to start within timeout"
            exit 1
        fi
        sleep 2
    done
    
    # Wait for Redis
    info "Waiting for Redis..."
    for i in {1..30}; do
        if docker exec supplier-validation-redis redis-cli ping &> /dev/null; then
            log "Redis is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            error "Redis failed to start within timeout"
            exit 1
        fi
        sleep 2
    done
    
    # Wait for main service
    info "Waiting for Supplier Validation service..."
    for i in {1..60}; do
        if curl -f http://localhost:$SERVICE_PORT/health &> /dev/null; then
            log "Supplier Validation service is ready"
            break
        fi
        if [ $i -eq 60 ]; then
            error "Supplier Validation service failed to start within timeout"
            exit 1
        fi
        sleep 3
    done
}

# Run database migrations/initialization
run_migrations() {
    log "Running database initialization..."
    
    # Wait a bit more for database to be fully ready
    sleep 5
    
    # The init.sql should be automatically executed by PostgreSQL container
    log "Database initialization completed"
}

# Show service status
show_status() {
    log "Service Status:"
    $COMPOSE_CMD ps
    
    echo ""
    log "Service URLs:"
    echo "  - Supplier Validation API: http://localhost:$SERVICE_PORT"
    echo "  - API Documentation: http://localhost:$SERVICE_PORT/docs"
    echo "  - Health Check: http://localhost:$SERVICE_PORT/health"
    echo "  - PgAdmin: http://localhost:8080 (admin@bizosaas.com / admin)"
    echo "  - MinIO Console: http://localhost:9001 (minioadmin / minioadmin)"
}

# Test the service
test_service() {
    log "Testing service endpoints..."
    
    # Test health endpoint
    if curl -f http://localhost:$SERVICE_PORT/health &> /dev/null; then
        log "Health check passed"
    else
        error "Health check failed"
        return 1
    fi
    
    # Test API documentation
    if curl -f http://localhost:$SERVICE_PORT/docs &> /dev/null; then
        log "API documentation accessible"
    else
        warning "API documentation not accessible"
    fi
    
    log "Service tests completed"
}

# Cleanup function
cleanup() {
    if [ "$1" == "full" ]; then
        log "Performing full cleanup..."
        $COMPOSE_CMD down -v
        docker rmi $DOCKER_IMAGE 2>/dev/null || true
        docker network rm $NETWORK_NAME 2>/dev/null || true
        rm -rf data/
    else
        log "Stopping services..."
        $COMPOSE_CMD down
    fi
}

# Main deployment function
deploy() {
    log "Starting Supplier Validation Workflow [P9] deployment..."
    
    check_docker
    check_docker_compose
    create_directories
    setup_environment
    create_network
    build_image
    start_services
    wait_for_services
    run_migrations
    test_service
    show_status
    
    log "Deployment completed successfully!"
    echo ""
    info "Next steps:"
    echo "1. Update the .env file with your API keys and configuration"
    echo "2. Access the API documentation at http://localhost:$SERVICE_PORT/docs"
    echo "3. Monitor logs with: $COMPOSE_CMD logs -f $SERVICE_NAME"
    echo "4. Stop services with: $COMPOSE_CMD down"
}

# Handle command line arguments
case "${1:-deploy}" in
    "deploy")
        deploy
        ;;
    "start")
        start_services
        wait_for_services
        show_status
        ;;
    "stop")
        cleanup
        ;;
    "restart")
        cleanup
        deploy
        ;;
    "cleanup")
        cleanup full
        ;;
    "status")
        show_status
        ;;
    "logs")
        $COMPOSE_CMD logs -f
        ;;
    "test")
        test_service
        ;;
    "build")
        build_image
        ;;
    *)
        echo "Usage: $0 {deploy|start|stop|restart|cleanup|status|logs|test|build}"
        echo ""
        echo "Commands:"
        echo "  deploy   - Full deployment (default)"
        echo "  start    - Start services"
        echo "  stop     - Stop services"
        echo "  restart  - Restart services"
        echo "  cleanup  - Full cleanup (removes volumes and images)"
        echo "  status   - Show service status"
        echo "  logs     - Show service logs"
        echo "  test     - Test service endpoints"
        echo "  build    - Build Docker image only"
        exit 1
        ;;
esac