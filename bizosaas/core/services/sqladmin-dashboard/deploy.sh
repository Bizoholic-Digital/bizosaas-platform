#!/bin/bash

# BizOSaaS SQLAdmin Dashboard Deployment Script
# Comprehensive platform management interface setup

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SERVICE_NAME="sqladmin-dashboard"
PORT=8010
DOCKER_IMAGE="bizosaas/sqladmin-dashboard"
DATABASE_NAME="bizosaas"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  BizOSaaS SQLAdmin Dashboard Setup    ${NC}"
echo -e "${BLUE}========================================${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is required but not installed"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is required but not installed"
        exit 1
    fi
    
    # Check PostgreSQL client
    if ! command -v psql &> /dev/null; then
        print_warning "PostgreSQL client not found. Database initialization may require manual setup."
    fi
    
    print_status "Prerequisites check completed"
}

# Setup environment
setup_environment() {
    print_status "Setting up environment..."
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            print_status "Created .env file from template"
            print_warning "Please update .env file with your configuration before proceeding"
        else
            print_error ".env.example file not found"
            exit 1
        fi
    else
        print_status ".env file already exists"
    fi
    
    # Create necessary directories
    mkdir -p logs data static uploads exports reports
    print_status "Created necessary directories"
}

# Database setup
setup_database() {
    print_status "Setting up database..."
    
    # Check if database is accessible
    if command -v psql &> /dev/null; then
        # Source environment variables
        if [ -f .env ]; then
            source .env
        fi
        
        # Extract database connection details from DATABASE_URL
        DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
        DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
        DB_USER=$(echo $DATABASE_URL | sed -n 's/.*:\/\/\([^:]*\):.*/\1/p')
        DB_NAME=$(echo $DATABASE_URL | sed -n 's/.*\/\([^?]*\).*/\1/p')
        
        # Test database connection
        if pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER &> /dev/null; then
            print_status "Database is accessible"
            
            # Run database schema initialization
            if [ -f database_schema.sql ]; then
                print_status "Initializing database schema..."
                PGPASSWORD=$POSTGRES_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f database_schema.sql
                print_status "Database schema initialized"
            else
                print_warning "database_schema.sql not found, skipping schema initialization"
            fi
        else
            print_warning "Cannot connect to database. Please ensure PostgreSQL is running and accessible."
        fi
    else
        print_warning "PostgreSQL client not available. Skipping database setup."
        print_warning "Please run database_schema.sql manually on your PostgreSQL instance."
    fi
}

# Build Docker image
build_image() {
    print_status "Building Docker image..."
    
    # Build with BuildKit for better performance
    DOCKER_BUILDKIT=1 docker build \
        --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
        --build-arg VERSION=$(git describe --tags --always 2>/dev/null || echo "latest") \
        --build-arg VCS_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown") \
        -t $DOCKER_IMAGE:latest \
        .
    
    print_status "Docker image built successfully"
}

# Deploy service
deploy_service() {
    print_status "Deploying service..."
    
    # Stop existing container if running
    if docker ps -q -f name=$SERVICE_NAME &> /dev/null; then
        print_status "Stopping existing container..."
        docker stop $SERVICE_NAME
        docker rm $SERVICE_NAME
    fi
    
    # Run new container
    docker run -d \
        --name $SERVICE_NAME \
        --restart unless-stopped \
        -p $PORT:8010 \
        --env-file .env \
        -v $(pwd)/logs:/app/logs \
        -v $(pwd)/data:/app/data \
        -v $(pwd)/static:/app/static \
        -v $(pwd)/uploads:/app/uploads \
        -v $(pwd)/exports:/app/exports \
        -v $(pwd)/reports:/app/reports \
        $DOCKER_IMAGE:latest
    
    print_status "Service deployed successfully"
}

# Health check
health_check() {
    print_status "Performing health check..."
    
    # Wait for service to start
    sleep 10
    
    # Check if container is running
    if docker ps -q -f name=$SERVICE_NAME &> /dev/null; then
        print_status "Container is running"
        
        # Check service health endpoint
        max_attempts=30
        attempt=1
        
        while [ $attempt -le $max_attempts ]; do
            if curl -f http://localhost:$PORT/api/system/health &> /dev/null; then
                print_status "Service is healthy and responding"
                break
            else
                if [ $attempt -eq $max_attempts ]; then
                    print_error "Service health check failed after $max_attempts attempts"
                    print_error "Check container logs: docker logs $SERVICE_NAME"
                    exit 1
                fi
                
                print_status "Waiting for service to be ready... (attempt $attempt/$max_attempts)"
                sleep 5
                ((attempt++))
            fi
        done
    else
        print_error "Container failed to start"
        print_error "Check container logs: docker logs $SERVICE_NAME"
        exit 1
    fi
}

# Display access information
show_access_info() {
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}     Deployment Completed Successfully  ${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo -e "\n${BLUE}Access Information:${NC}"
    echo -e "• Admin Interface: ${YELLOW}http://localhost:$PORT/admin${NC}"
    echo -e "• Dashboard Switcher: ${YELLOW}http://localhost:$PORT/dashboard-switcher${NC}"
    echo -e "• API Documentation: ${YELLOW}http://localhost:$PORT/docs${NC}"
    echo -e "• Health Check: ${YELLOW}http://localhost:$PORT/api/system/health${NC}"
    
    echo -e "\n${BLUE}Authentication:${NC}"
    echo -e "• Requires SUPER_ADMIN role in BizOSaaS platform"
    echo -e "• Integrates with unified authentication system"
    
    echo -e "\n${BLUE}Management Commands:${NC}"
    echo -e "• View logs: ${YELLOW}docker logs -f $SERVICE_NAME${NC}"
    echo -e "• Stop service: ${YELLOW}docker stop $SERVICE_NAME${NC}"
    echo -e "• Start service: ${YELLOW}docker start $SERVICE_NAME${NC}"
    echo -e "• Restart service: ${YELLOW}docker restart $SERVICE_NAME${NC}"
    
    echo -e "\n${BLUE}Features Available:${NC}"
    echo -e "• Complete CRUD operations for all platform data"
    echo -e "• Advanced filtering and search capabilities"
    echo -e "• Real-time monitoring and analytics"
    echo -e "• Security and compliance management"
    echo -e "• Integration and webhook management"
    echo -e "• Billing and subscription management"
    echo -e "• CRM, E-commerce, and CMS administration"
    
    echo -e "\n${GREEN}Ready for production use!${NC}"
}

# Main deployment function
main() {
    echo -e "${BLUE}Starting deployment process...${NC}\n"
    
    check_prerequisites
    setup_environment
    setup_database
    build_image
    deploy_service
    health_check
    show_access_info
    
    echo -e "\n${GREEN}Deployment completed successfully!${NC}"
}

# Command line options
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "build")
        check_prerequisites
        build_image
        ;;
    "start")
        docker start $SERVICE_NAME
        print_status "Service started"
        ;;
    "stop")
        docker stop $SERVICE_NAME
        print_status "Service stopped"
        ;;
    "restart")
        docker restart $SERVICE_NAME
        print_status "Service restarted"
        ;;
    "logs")
        docker logs -f $SERVICE_NAME
        ;;
    "health")
        curl -s http://localhost:$PORT/api/system/health | python -m json.tool
        ;;
    "clean")
        print_status "Cleaning up..."
        docker stop $SERVICE_NAME 2>/dev/null || true
        docker rm $SERVICE_NAME 2>/dev/null || true
        docker rmi $DOCKER_IMAGE:latest 2>/dev/null || true
        print_status "Cleanup completed"
        ;;
    "help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  deploy    Full deployment (default)"
        echo "  build     Build Docker image only"
        echo "  start     Start the service"
        echo "  stop      Stop the service"
        echo "  restart   Restart the service"
        echo "  logs      View service logs"
        echo "  health    Check service health"
        echo "  clean     Remove service and image"
        echo "  help      Show this help message"
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for available commands"
        exit 1
        ;;
esac