#!/bin/bash

# BizOSaaS Data Synchronization Service Deployment Script

set -e

echo "🚀 Deploying BizOSaaS Data Synchronization Service..."

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SERVICE_NAME="bizosaas-data-sync"
SERVICE_PORT="8025"
DOCKER_IMAGE="bizosaas/data-sync:latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed or not in PATH"
        exit 1
    fi
    
    # Check if PostgreSQL is accessible
    if ! docker exec bizosaas-postgres-dev pg_isready -U admin -d bizosaas &> /dev/null; then
        log_warning "PostgreSQL container not found or not ready. Please ensure the database is running."
    fi
    
    # Check if Redis is accessible
    if ! docker exec bizosaas-redis-dev redis-cli ping &> /dev/null; then
        log_warning "Redis container not found or not ready. Please ensure Redis is running."
    fi
    
    log_success "Prerequisites check completed"
}

# Build Docker image
build_image() {
    log_info "Building Docker image for Data Sync service..."
    
    cd "$SCRIPT_DIR"
    
    # Build the image
    docker build -t "$DOCKER_IMAGE" .
    
    if [ $? -eq 0 ]; then
        log_success "Docker image built successfully: $DOCKER_IMAGE"
    else
        log_error "Failed to build Docker image"
        exit 1
    fi
}

# Setup environment file
setup_environment() {
    log_info "Setting up environment configuration..."
    
    ENV_FILE="$SCRIPT_DIR/.env"
    
    if [ ! -f "$ENV_FILE" ]; then
        log_info "Creating .env file from template..."
        cp "$SCRIPT_DIR/.env.example" "$ENV_FILE"
        
        # Update with platform-specific values
        sed -i "s|DATABASE_URL=.*|DATABASE_URL=postgresql://admin:securepassword@host.docker.internal:5432/bizosaas|g" "$ENV_FILE"
        sed -i "s|REDIS_URL=.*|REDIS_URL=redis://host.docker.internal:6379/6|g" "$ENV_FILE"
        sed -i "s|ENVIRONMENT=.*|ENVIRONMENT=production|g" "$ENV_FILE"
        
        log_success "Environment file created: $ENV_FILE"
        log_warning "Please review and update the .env file with your specific configuration"
    else
        log_info "Environment file already exists: $ENV_FILE"
    fi
}

# Create database tables
setup_database() {
    log_info "Setting up database tables..."
    
    # Wait for database to be ready
    log_info "Waiting for database to be ready..."
    timeout=60
    while [ $timeout -gt 0 ] && ! docker exec bizosaas-postgres-dev pg_isready -U admin -d bizosaas &> /dev/null; do
        sleep 2
        timeout=$((timeout - 2))
    done
    
    if [ $timeout -le 0 ]; then
        log_error "Database not ready after waiting. Please check PostgreSQL container."
        exit 1
    fi
    
    # Create database extensions if needed
    log_info "Ensuring required database extensions..."
    docker exec bizosaas-postgres-dev psql -U admin -d bizosaas -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";" || true
    docker exec bizosaas-postgres-dev psql -U admin -d bizosaas -c "CREATE EXTENSION IF NOT EXISTS \"pgcrypto\";" || true
    
    log_success "Database setup completed"
}

# Deploy service
deploy_service() {
    log_info "Deploying Data Synchronization service..."
    
    cd "$PROJECT_ROOT"
    
    # Deploy using Docker Compose
    docker-compose -f docker-compose.bizosaas-platform.yml up -d "$SERVICE_NAME"
    
    if [ $? -eq 0 ]; then
        log_success "Data Sync service deployed successfully"
    else
        log_error "Failed to deploy Data Sync service"
        exit 1
    fi
}

# Wait for service to be healthy
wait_for_health() {
    log_info "Waiting for service to be healthy..."
    
    max_attempts=30
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f "http://localhost:$SERVICE_PORT/health" &> /dev/null; then
            log_success "Service is healthy and ready"
            return 0
        fi
        
        log_info "Attempt $attempt/$max_attempts - waiting for service..."
        sleep 5
        attempt=$((attempt + 1))
    done
    
    log_error "Service did not become healthy within expected time"
    return 1
}

# Test service endpoints
test_service() {
    log_info "Testing service endpoints..."
    
    # Test health endpoint
    if curl -f "http://localhost:$SERVICE_PORT/health" &> /dev/null; then
        log_success "Health endpoint is working"
    else
        log_error "Health endpoint is not responding"
        return 1
    fi
    
    # Test API documentation
    if curl -f "http://localhost:$SERVICE_PORT/docs" &> /dev/null; then
        log_success "API documentation is accessible"
    else
        log_warning "API documentation endpoint is not responding"
    fi
    
    # Test metrics endpoint
    if curl -f "http://localhost:$SERVICE_PORT/sync/status" &> /dev/null; then
        log_success "Status endpoint is working"
    else
        log_warning "Status endpoint is not responding"
    fi
    
    log_success "Service testing completed"
}

# Update Brain API integration
update_brain_integration() {
    log_info "Updating Brain API integration..."
    
    BRAIN_SERVICE_DIR="$PROJECT_ROOT/ai/services/bizosaas-brain-simple"
    
    if [ -f "$BRAIN_SERVICE_DIR/main.py" ]; then
        # Check if data sync integration already exists
        if grep -q "data-sync" "$BRAIN_SERVICE_DIR/main.py"; then
            log_info "Brain API integration already exists"
        else
            log_info "Adding data sync integration to Brain API..."
            
            # Backup original file
            cp "$BRAIN_SERVICE_DIR/main.py" "$BRAIN_SERVICE_DIR/main.py.backup"
            
            # Add import and router inclusion
            cat << 'EOF' >> "$BRAIN_SERVICE_DIR/main.py"

# ===========================================
# DATA SYNCHRONIZATION API GATEWAY ROUTES
# ===========================================

def create_data_sync_router():
    """Create Data Synchronization proxy router"""
    router = APIRouter(prefix="/api/brain/data-sync", tags=["Data Synchronization"])
    
    @router.get("/health")
    async def get_data_sync_health(request: Request):
        """Proxy to Data Sync health endpoint"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://bizosaas-data-sync:8025/health",
                    headers=dict(request.headers)
                )
                return response.json()
        except Exception as e:
            logger.error(f"Data Sync health proxy error: {e}")
            raise HTTPException(status_code=503, detail="Data Sync service unavailable")
    
    @router.get("/status")
    async def get_sync_status(request: Request):
        """Proxy to Data Sync status endpoint"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://bizosaas-data-sync:8025/sync/status",
                    headers=dict(request.headers)
                )
                return response.json()
        except Exception as e:
            logger.error(f"Data Sync status proxy error: {e}")
            raise HTTPException(status_code=503, detail="Data Sync service unavailable")
    
    @router.get("/metrics")
    async def get_sync_metrics(request: Request):
        """Proxy to Data Sync metrics endpoint"""
        try:
            query_params = str(request.url.query)
            url = "http://bizosaas-data-sync:8025/sync/metrics"
            if query_params:
                url += f"?{query_params}"
                
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=dict(request.headers))
                return response.json()
        except Exception as e:
            logger.error(f"Data Sync metrics proxy error: {e}")
            raise HTTPException(status_code=503, detail="Data Sync service unavailable")
    
    return router
EOF
            
            # Add router inclusion to startup event
            sed -i '/logger.info("✅ Billing & Subscription proxy router initialized")/a\\n    # Include Data Sync router\n    data_sync_router = create_data_sync_router()\n    app.include_router(data_sync_router)\n    logger.info("✅ Data Synchronization proxy router initialized")' "$BRAIN_SERVICE_DIR/main.py"
            
            log_success "Brain API integration added"
        fi
    else
        log_warning "Brain API main.py not found at expected location"
    fi
}

# Show service information
show_service_info() {
    log_info "Service Information:"
    echo ""
    echo "Service Name: $SERVICE_NAME"
    echo "Service Port: $SERVICE_PORT"
    echo "Docker Image: $DOCKER_IMAGE"
    echo ""
    echo "🌐 Service URLs:"
    echo "  Health Check: http://localhost:$SERVICE_PORT/health"
    echo "  API Documentation: http://localhost:$SERVICE_PORT/docs"
    echo "  WebSocket: ws://localhost:$SERVICE_PORT/ws/sync"
    echo ""
    echo "🔗 Brain API Integration:"
    echo "  Health: http://localhost:8001/api/brain/data-sync/health"
    echo "  Status: http://localhost:8001/api/brain/data-sync/status"
    echo "  Metrics: http://localhost:8001/api/brain/data-sync/metrics"
    echo ""
    echo "📊 Monitoring:"
    echo "  Service Status: docker-compose -f docker-compose.bizosaas-platform.yml ps $SERVICE_NAME"
    echo "  Service Logs: docker-compose -f docker-compose.bizosaas-platform.yml logs -f $SERVICE_NAME"
    echo ""
}

# Show usage information
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --build-only    Only build the Docker image"
    echo "  --deploy-only   Only deploy (skip build)"
    echo "  --test-only     Only run tests"
    echo "  --help          Show this help message"
    echo ""
}

# Main deployment function
main() {
    local build_only=false
    local deploy_only=false
    local test_only=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --build-only)
                build_only=true
                shift
                ;;
            --deploy-only)
                deploy_only=true
                shift
                ;;
            --test-only)
                test_only=true
                shift
                ;;
            --help)
                show_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Execute based on options
    if [ "$test_only" = true ]; then
        wait_for_health
        test_service
        exit 0
    fi
    
    if [ "$build_only" = true ]; then
        check_prerequisites
        build_image
        exit 0
    fi
    
    if [ "$deploy_only" = true ]; then
        check_prerequisites
        setup_environment
        deploy_service
        wait_for_health
        test_service
        show_service_info
        exit 0
    fi
    
    # Full deployment
    check_prerequisites
    build_image
    setup_environment
    setup_database
    deploy_service
    update_brain_integration
    wait_for_health
    test_service
    show_service_info
    
    log_success "🎉 Data Synchronization service deployment completed successfully!"
    log_info "Next steps:"
    echo "  1. Review the .env file and update configuration as needed"
    echo "  2. Test the service endpoints using the URLs provided above"
    echo "  3. Set up monitoring and alerting for production use"
    echo "  4. Configure platform-specific API keys for full functionality"
}

# Run main function
main "$@"