#!/bin/bash

# Saleor Infrastructure Management Script
# Manages the complete Saleor infrastructure for CoreLDove storefront development

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIZOSAAS_DIR="$(dirname "$SCRIPT_DIR")"
SERVICES_DIR="$BIZOSAAS_DIR/services"
STOREFRONT_DIR="$SERVICES_DIR/saleor-storefront"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🚀 $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${NC}"
}

print_section() {
    echo -e "${PURPLE}"
    echo "▶ $1"
    echo -e "${NC}"
}

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Function to check if a service is running
check_service() {
    local port=$1
    local service_name=$2
    
    if timeout 2 bash -c "</dev/tcp/localhost/$port" 2>/dev/null; then
        print_status "$service_name is running on port $port"
        return 0
    else
        print_warning "$service_name is not running on port $port"
        return 1
    fi
}

# Function to start the development API
start_dev_api() {
    print_section "Starting Development Saleor API"
    
    # Check if already running
    if check_service 8024 "Saleor API"; then
        print_info "Development API is already running"
        return 0
    fi
    
    # Start the development API
    print_info "Starting Saleor-compatible API server..."
    cd "$BIZOSAAS_DIR"
    
    if [ -f "saleor-api-complete.py" ]; then
        nohup python3 saleor-api-complete.py > "$BIZOSAAS_DIR/logs/saleor-api.log" 2>&1 &
        echo $! > "$BIZOSAAS_DIR/logs/saleor-api.pid"
        
        # Wait for startup
        sleep 3
        
        if check_service 8024 "Saleor API"; then
            print_status "Development Saleor API started successfully"
            print_info "GraphQL endpoint: http://localhost:8024/graphql/"
            print_info "Logs: $BIZOSAAS_DIR/logs/saleor-api.log"
            return 0
        else
            print_error "Failed to start development API"
            return 1
        fi
    else
        print_error "saleor-api-complete.py not found"
        return 1
    fi
}

# Function to stop the development API
stop_dev_api() {
    print_section "Stopping Development Saleor API"
    
    if [ -f "$BIZOSAAS_DIR/logs/saleor-api.pid" ]; then
        local pid=$(cat "$BIZOSAAS_DIR/logs/saleor-api.pid")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            print_status "Stopped development API (PID: $pid)"
        fi
        rm -f "$BIZOSAAS_DIR/logs/saleor-api.pid"
    fi
    
    # Kill any remaining processes
    pkill -f "saleor-api-complete.py" 2>/dev/null || true
    print_status "Development API stopped"
}

# Function to start full Docker infrastructure
start_docker_infrastructure() {
    print_section "Starting Full Docker Saleor Infrastructure"
    
    # Check if Docker is available
    if ! command -v docker >/dev/null 2>&1; then
        print_error "Docker is not installed"
        return 1
    fi
    
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker daemon is not running"
        return 1
    fi
    
    # Check if PostgreSQL is running
    if ! check_service 5432 "PostgreSQL"; then
        print_error "PostgreSQL must be running before starting Saleor infrastructure"
        print_info "Please start PostgreSQL and try again"
        return 1
    fi
    
    # Use the working configuration with modifications
    cd "$BIZOSAAS_DIR"
    
    if [ -f "docker-compose.saleor-working.yml" ]; then
        print_info "Starting Saleor services with Docker Compose..."
        
        # Stop development API first
        stop_dev_api
        
        # Start Docker services
        docker-compose -f docker-compose.saleor-working.yml up -d
        
        # Wait for services to start
        print_info "Waiting for services to initialize..."
        sleep 10
        
        # Check services
        if check_service 8024 "Saleor API"; then
            print_status "Docker Saleor API started successfully"
            
            # Check dashboard
            if check_service 9020 "Saleor Dashboard"; then
                print_status "Saleor Dashboard started successfully"
            fi
            
            # Run database migrations
            print_info "Running database migrations..."
            docker exec coreldove-saleor-working python manage.py migrate 2>/dev/null || print_warning "Migration may have failed"
            
            # Create sample data
            print_info "Creating sample data..."
            docker exec coreldove-saleor-working python manage.py populatedb --createsuperuser 2>/dev/null || print_warning "Sample data creation may have failed"
            
            print_status "Full Saleor infrastructure is ready!"
            return 0
        else
            print_error "Failed to start Docker Saleor infrastructure"
            docker-compose -f docker-compose.saleor-working.yml logs --tail=20
            return 1
        fi
    else
        print_error "docker-compose.saleor-working.yml not found"
        return 1
    fi
}

# Function to stop Docker infrastructure
stop_docker_infrastructure() {
    print_section "Stopping Docker Saleor Infrastructure"
    
    cd "$BIZOSAAS_DIR"
    
    if [ -f "docker-compose.saleor-working.yml" ]; then
        docker-compose -f docker-compose.saleor-working.yml down
        print_status "Docker Saleor infrastructure stopped"
    fi
}

# Function to check infrastructure status
check_infrastructure_status() {
    print_header "SALEOR INFRASTRUCTURE STATUS"
    
    print_section "Service Status Check"
    
    # Check core services
    check_service 5432 "PostgreSQL Database"
    check_service 6379 "Redis Cache"
    
    # Check Saleor services
    local api_running=false
    local dashboard_running=false
    
    if check_service 8024 "Saleor GraphQL API"; then
        api_running=true
    fi
    
    if check_service 9020 "Saleor Dashboard" || check_service 9001 "Saleor Dashboard (Alt)"; then
        dashboard_running=true
    fi
    
    # Test GraphQL endpoint
    print_section "GraphQL Endpoint Test"
    if curl -f -s -X POST http://localhost:8024/graphql/ \
        -H "Content-Type: application/json" \
        -d '{"query":"{ shop { name } }"}' > /dev/null; then
        print_status "GraphQL endpoint is responding"
    else
        print_warning "GraphQL endpoint test failed"
    fi
    
    # Check storefront
    print_section "Storefront Status"
    if [ -d "$STOREFRONT_DIR" ]; then
        print_status "Storefront directory exists"
        if [ -f "$STOREFRONT_DIR/.env.local" ]; then
            print_status "Storefront configuration found"
        else
            print_warning "Storefront .env.local not found"
        fi
    else
        print_error "Storefront directory not found"
    fi
    
    # Summary
    print_section "Infrastructure Summary"
    if [ "$api_running" = true ]; then
        print_status "✅ Core infrastructure is operational"
        print_info "🌐 GraphQL API: http://localhost:8024/graphql/"
        if [ "$dashboard_running" = true ]; then
            print_info "🎨 Admin Dashboard: http://localhost:9020/ or http://localhost:9001/"
        fi
        print_info "🔗 Ready for storefront development"
    else
        print_warning "⚠️  Saleor API is not running"
        print_info "Use './scripts/saleor-infrastructure-manager.sh start-dev' to start development API"
        print_info "Use './scripts/saleor-infrastructure-manager.sh start-docker' for full infrastructure"
    fi
}

# Function to test storefront integration
test_storefront_integration() {
    print_header "STOREFRONT INTEGRATION TEST"
    
    # Check if storefront exists
    if [ ! -d "$STOREFRONT_DIR" ]; then
        print_error "Storefront directory not found at $STOREFRONT_DIR"
        return 1
    fi
    
    cd "$STOREFRONT_DIR"
    
    # Check API connectivity
    print_section "Testing API Connectivity"
    if ! check_service 8024 "Saleor API"; then
        print_error "Saleor API is not running"
        print_info "Start the API first using: ./scripts/saleor-infrastructure-manager.sh start-dev"
        return 1
    fi
    
    # Test GraphQL codegen
    print_section "Testing GraphQL Code Generation"
    if pnpm run generate 2>/dev/null; then
        print_status "GraphQL code generation successful"
    else
        print_warning "GraphQL code generation failed - this is expected with the minimal development API"
        print_info "The development API provides basic functionality for initial development"
        print_info "For full schema compatibility, use: ./scripts/saleor-infrastructure-manager.sh start-docker"
    fi
    
    # Try to start storefront
    print_section "Testing Storefront Startup"
    print_info "Attempting to start storefront (will timeout after 10 seconds)..."
    
    timeout 10 pnpm dev 2>/dev/null || true
    
    if check_service 3001 "Storefront"; then
        print_status "Storefront started successfully"
        print_info "🌐 Storefront: http://localhost:3001"
    else
        print_warning "Storefront did not start in test mode"
        print_info "This might be normal - try starting manually: cd $STOREFRONT_DIR && pnpm dev"
    fi
}

# Function to create startup script
create_startup_script() {
    print_section "Creating Quick Startup Script"
    
    cat > "$BIZOSAAS_DIR/start-saleor-dev.sh" << 'EOF'
#!/bin/bash
# Quick Saleor Development Startup
cd "$(dirname "$0")"
./scripts/saleor-infrastructure-manager.sh start-dev
echo ""
echo "🚀 Saleor development environment is ready!"
echo "🌐 GraphQL API: http://localhost:8024/graphql/"
echo "🛍️ Start storefront: cd services/saleor-storefront && pnpm dev"
EOF
    
    chmod +x "$BIZOSAAS_DIR/start-saleor-dev.sh"
    print_status "Created quick startup script: $BIZOSAAS_DIR/start-saleor-dev.sh"
}

# Function to show help
show_help() {
    print_header "SALEOR INFRASTRUCTURE MANAGER"
    
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start-dev     Start development API server (lightweight)"
    echo "  start-docker  Start full Docker Saleor infrastructure"
    echo "  stop-dev      Stop development API server"
    echo "  stop-docker   Stop Docker infrastructure"
    echo "  status        Check infrastructure status"
    echo "  test          Test storefront integration"
    echo "  setup         Create quick startup script"
    echo "  help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start-dev    # Quick development setup"
    echo "  $0 status       # Check what's running"
    echo "  $0 test         # Test storefront connection"
    echo ""
    echo "Development Workflow:"
    echo "  1. ./$(basename "$0") start-dev"
    echo "  2. cd services/saleor-storefront"
    echo "  3. pnpm dev"
    echo ""
}

# Create logs directory if it doesn't exist
mkdir -p "$BIZOSAAS_DIR/logs"

# Main command handling
case "${1:-help}" in
    "start-dev")
        print_header "STARTING DEVELOPMENT ENVIRONMENT"
        start_dev_api
        echo ""
        print_info "🎯 Next steps:"
        print_info "   cd $STOREFRONT_DIR"
        print_info "   pnpm dev"
        ;;
    "start-docker")
        print_header "STARTING DOCKER INFRASTRUCTURE"
        start_docker_infrastructure
        ;;
    "stop-dev")
        stop_dev_api
        ;;
    "stop-docker")
        stop_docker_infrastructure
        ;;
    "status")
        check_infrastructure_status
        ;;
    "test")
        test_storefront_integration
        ;;
    "setup")
        create_startup_script
        ;;
    "help"|*)
        show_help
        ;;
esac