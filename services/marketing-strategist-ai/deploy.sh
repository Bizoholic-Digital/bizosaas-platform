#!/bin/bash

# BizOSaaS Marketing Strategist AI [P10] Deployment Script
# Comprehensive AI-Powered Marketing Strategy and Campaign Management System

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SERVICE_NAME="Marketing Strategist AI"
SERVICE_PORT="8029"
CONTAINER_NAME="bizosaas-marketing-strategist-ai"
NETWORK_NAME="bizosaas-network"

# Function to print colored output
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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check dependencies
check_dependencies() {
    print_status "Checking dependencies..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "All dependencies are installed"
}

# Function to create environment file if it doesn't exist
setup_environment() {
    print_status "Setting up environment configuration..."
    
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            print_warning "Created .env file from .env.example. Please update with your actual values."
        else
            print_error ".env.example file not found"
            exit 1
        fi
    fi
    
    print_success "Environment configuration ready"
}

# Function to create Docker network if it doesn't exist
create_network() {
    print_status "Setting up Docker network..."
    
    if ! docker network inspect $NETWORK_NAME >/dev/null 2>&1; then
        docker network create $NETWORK_NAME
        print_success "Created Docker network: $NETWORK_NAME"
    else
        print_status "Docker network $NETWORK_NAME already exists"
    fi
}

# Function to build the Docker image
build_image() {
    print_status "Building Docker image for $SERVICE_NAME..."
    
    docker build -t $CONTAINER_NAME:latest .
    
    if [ $? -eq 0 ]; then
        print_success "Successfully built Docker image"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Function to stop existing containers
stop_existing() {
    print_status "Stopping existing containers..."
    
    if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
        docker-compose down
        print_success "Stopped existing containers"
    else
        print_status "No existing containers to stop"
    fi
}

# Function to start the services
start_services() {
    print_status "Starting $SERVICE_NAME services..."
    
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        print_success "Successfully started all services"
    else
        print_error "Failed to start services"
        exit 1
    fi
}

# Function to wait for service to be healthy
wait_for_health() {
    print_status "Waiting for $SERVICE_NAME to be healthy..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:$SERVICE_PORT/health >/dev/null 2>&1; then
            print_success "$SERVICE_NAME is healthy and ready"
            return 0
        fi
        
        print_status "Attempt $attempt/$max_attempts - waiting for service to be ready..."
        sleep 10
        attempt=$((attempt + 1))
    done
    
    print_error "Service failed to become healthy after $max_attempts attempts"
    return 1
}

# Function to run database initialization
init_database() {
    print_status "Initializing database schema..."
    
    # Wait a bit for PostgreSQL to be ready
    sleep 5
    
    # The init.sql script will be automatically executed by PostgreSQL container
    print_success "Database initialization completed"
}

# Function to test the deployment
test_deployment() {
    print_status "Testing deployment..."
    
    # Test health endpoint
    if curl -f http://localhost:$SERVICE_PORT/health >/dev/null 2>&1; then
        print_success "Health check passed"
    else
        print_error "Health check failed"
        return 1
    fi
    
    # Test main dashboard
    if curl -f http://localhost:$SERVICE_PORT/ >/dev/null 2>&1; then
        print_success "Dashboard endpoint accessible"
    else
        print_error "Dashboard endpoint not accessible"
        return 1
    fi
    
    print_success "All deployment tests passed"
}

# Function to show deployment information
show_info() {
    print_success "=== $SERVICE_NAME Deployment Complete ==="
    echo ""
    echo "Service Information:"
    echo "  Name: $SERVICE_NAME"
    echo "  Port: $SERVICE_PORT"
    echo "  Container: $CONTAINER_NAME"
    echo ""
    echo "Access URLs:"
    echo "  Dashboard: http://localhost:$SERVICE_PORT"
    echo "  Health Check: http://localhost:$SERVICE_PORT/health"
    echo "  API Documentation: http://localhost:$SERVICE_PORT/docs"
    echo "  Interactive API: http://localhost:$SERVICE_PORT/redoc"
    echo ""
    echo "Key Features:"
    echo "  ✓ AI-Powered Campaign Strategy Generation"
    echo "  ✓ Multi-Platform Campaign Management"
    echo "  ✓ Automated Client Communication"
    echo "  ✓ Performance Analytics & Optimization"
    echo "  ✓ Budget Optimization & Allocation"
    echo "  ✓ Competitor Analysis & Market Intelligence"
    echo "  ✓ Content Strategy & Creative Recommendations"
    echo "  ✓ Predictive Performance Modeling"
    echo ""
    echo "API Endpoints:"
    echo "  POST /api/v1/strategy/generate - Generate campaign strategy"
    echo "  POST /api/v1/campaign/optimize - Optimize existing campaigns"
    echo "  POST /api/v1/communication/send - Send client communications"
    echo "  POST /api/v1/reports/generate - Generate performance reports"
    echo "  POST /api/v1/budget/optimize - Optimize budget allocation"
    echo "  POST /api/v1/competitor-analysis - Analyze competitors"
    echo "  GET  /api/v1/campaigns/{id}/insights - Get campaign insights"
    echo "  GET  /api/v1/analytics/dashboard - Get analytics dashboard"
    echo ""
    echo "Integration URLs:"
    echo "  Brain API: http://localhost:8001 (Central Intelligence)"
    echo "  API Key Management: http://localhost:8026 (Platform Credentials)"
    echo "  Admin AI Assistant: http://localhost:8028 (Platform Monitoring)"
    echo ""
    echo "Database:"
    echo "  PostgreSQL: localhost:5434 (bizosaas database)"
    echo "  Redis Cache: localhost:6380"
    echo ""
    echo "Next Steps:"
    echo "  1. Configure .env file with your API keys"
    echo "  2. Test campaign strategy generation"
    echo "  3. Set up client communication templates"
    echo "  4. Configure marketing platform integrations"
    echo "  5. Test automated reporting features"
    echo ""
}

# Function to show logs
show_logs() {
    print_status "Showing recent logs..."
    docker-compose logs --tail=50 marketing-strategist-ai
}

# Main deployment function
main() {
    echo ""
    print_status "Starting $SERVICE_NAME deployment..."
    echo ""
    
    check_dependencies
    setup_environment
    create_network
    stop_existing
    build_image
    start_services
    init_database
    
    if wait_for_health; then
        test_deployment
        show_info
    else
        print_error "Deployment failed - service not healthy"
        print_status "Showing logs for troubleshooting:"
        show_logs
        exit 1
    fi
}

# Handle command line arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "start")
        print_status "Starting $SERVICE_NAME..."
        docker-compose up -d
        wait_for_health
        ;;
    "stop")
        print_status "Stopping $SERVICE_NAME..."
        docker-compose down
        ;;
    "restart")
        print_status "Restarting $SERVICE_NAME..."
        docker-compose restart
        wait_for_health
        ;;
    "logs")
        show_logs
        ;;
    "status")
        print_status "Service status:"
        docker-compose ps
        ;;
    "health")
        if curl -f http://localhost:$SERVICE_PORT/health >/dev/null 2>&1; then
            print_success "$SERVICE_NAME is healthy"
        else
            print_error "$SERVICE_NAME is not healthy"
            exit 1
        fi
        ;;
    "clean")
        print_status "Cleaning up $SERVICE_NAME..."
        docker-compose down -v
        docker rmi $CONTAINER_NAME:latest 2>/dev/null || true
        ;;
    *)
        echo "Usage: $0 {deploy|start|stop|restart|logs|status|health|clean}"
        echo ""
        echo "Commands:"
        echo "  deploy  - Full deployment (default)"
        echo "  start   - Start services"
        echo "  stop    - Stop services"
        echo "  restart - Restart services"
        echo "  logs    - Show service logs"
        echo "  status  - Show service status"
        echo "  health  - Check service health"
        echo "  clean   - Clean up containers and images"
        exit 1
        ;;
esac