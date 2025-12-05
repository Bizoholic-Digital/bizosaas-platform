#!/bin/bash
# Frontend Container Deployment Script
# BizOSaaS Platform - Production Frontend Stack
# Tests containerized deployment one service at a time

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="BizOSaaS Frontend Stack"
COMPOSE_FILE="docker-compose.frontend-apps.yml"
SERVICES=("bizosaas-coreldove-frontend" "bizosaas-bizoholic-frontend" "bizosaas-client-portal" "bizosaas-admin-dashboard")
PORTS=("3012" "3008" "3006" "3009")
TIMEOUT=300  # 5 minutes per build

echo -e "${BLUE}🚀 ${PROJECT_NAME} - Container Deployment${NC}"
echo "======================================================"

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1  # Port is in use
    else
        return 0  # Port is available
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local service_name=$1
    local port=$2
    local max_attempts=60
    local attempt=1
    
    echo -e "${BLUE}⏳ Waiting for ${service_name} to be ready on port ${port}...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:$port >/dev/null 2>&1; then
            print_status "${service_name} is ready on port ${port}!"
            return 0
        fi
        
        if [ $((attempt % 10)) -eq 0 ]; then
            echo -e "${YELLOW}   Still waiting... (${attempt}/${max_attempts})${NC}"
        fi
        
        sleep 5
        attempt=$((attempt + 1))
    done
    
    print_error "${service_name} failed to start within ${max_attempts} attempts"
    return 1
}

# Function to test service endpoints
test_service() {
    local service_name=$1
    local port=$2
    
    echo -e "${BLUE}🧪 Testing ${service_name} endpoints...${NC}"
    
    # Test main page
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:$port | grep -q "200\|301\|302"; then
        print_status "Main page accessible"
    else
        print_warning "Main page returned non-200 status"
    fi
    
    # Test health endpoint if available
    if curl -s http://localhost:$port/api/health >/dev/null 2>&1; then
        print_status "Health endpoint responding"
    else
        print_warning "Health endpoint not available (may be normal)"
    fi
    
    # Test next.js specific endpoint
    if curl -s http://localhost:$port/_next/static >/dev/null 2>&1; then
        print_status "Next.js static assets accessible"
    else
        print_warning "Next.js static assets not accessible"
    fi
}

# Check prerequisites
echo -e "${BLUE}📋 Checking Prerequisites${NC}"
echo "================================"

# Check Docker
if ! command -v docker >/dev/null 2>&1; then
    print_error "Docker is not installed"
    exit 1
else
    print_status "Docker is installed"
fi

# Check Docker Compose
if ! command -v docker-compose >/dev/null 2>&1; then
    print_error "Docker Compose is not installed"
    exit 1
else
    print_status "Docker Compose is installed"
fi

# Check if compose file exists
if [ ! -f "$COMPOSE_FILE" ]; then
    print_error "Compose file $COMPOSE_FILE not found"
    exit 1
else
    print_status "Compose file found: $COMPOSE_FILE"
fi

# Check network
if ! docker network ls | grep -q "bizosaas-platform-network"; then
    print_error "BizOSaaS platform network not found"
    echo "Please create the network first:"
    echo "  docker network create bizosaas-platform-network"
    exit 1
else
    print_status "BizOSaaS platform network exists"
fi

echo ""

# Stop any existing containers
echo -e "${BLUE}🛑 Stopping Existing Containers${NC}"
echo "==================================="
docker-compose -f $COMPOSE_FILE down --remove-orphans 2>/dev/null || true
print_status "Stopped existing containers"

echo ""

# Build and deploy each service
for i in "${!SERVICES[@]}"; do
    service="${SERVICES[$i]}"
    port="${PORTS[$i]}"
    
    echo -e "${BLUE}🔨 Building and Deploying: ${service}${NC}"
    echo "============================================="
    
    # Check if port is available
    if ! check_port $port; then
        print_warning "Port $port is in use, stopping conflicting process..."
        # Try to stop any process using the port
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
    
    # Build and start the service
    echo -e "${YELLOW}Building ${service}... (this may take 5+ minutes)${NC}"
    if timeout $TIMEOUT docker-compose -f $COMPOSE_FILE up --build -d $service; then
        print_status "Built and started ${service}"
        
        # Wait for service to be ready
        if wait_for_service $service $port; then
            # Test the service
            test_service $service $port
            print_status "${service} deployment successful!"
        else
            print_error "${service} failed to become ready"
            echo -e "${YELLOW}Checking logs:${NC}"
            docker-compose -f $COMPOSE_FILE logs --tail=20 $service
        fi
    else
        print_error "Failed to build/start ${service}"
        echo -e "${YELLOW}Checking logs:${NC}"
        docker-compose -f $COMPOSE_FILE logs --tail=20 $service || true
    fi
    
    echo ""
done

# Final status check
echo -e "${BLUE}📊 Final Status Check${NC}"
echo "======================="

echo -e "${BLUE}Container Status:${NC}"
docker-compose -f $COMPOSE_FILE ps

echo ""
echo -e "${BLUE}Port Status:${NC}"
for i in "${!SERVICES[@]}"; do
    service="${SERVICES[$i]}"
    port="${PORTS[$i]}"
    
    if check_port $port; then
        print_error "Port $port (${service}) - NOT ACCESSIBLE"
    else
        print_status "Port $port (${service}) - ACCESSIBLE"
    fi
done

echo ""
echo -e "${BLUE}Service URLs:${NC}"
echo "Client Portal:    http://localhost:3006"
echo "Bizoholic:        http://localhost:3008" 
echo "BizOSaaS Admin:   http://localhost:3009"
echo "CoreLDove:        http://localhost:3012"

echo ""
echo -e "${GREEN}🎉 Frontend containerization deployment complete!${NC}"
echo -e "${YELLOW}Note: Services may take additional time to fully initialize.${NC}"
echo ""
echo -e "${BLUE}Useful Commands:${NC}"
echo "View logs:        docker-compose -f $COMPOSE_FILE logs -f [service-name]"
echo "Stop services:    docker-compose -f $COMPOSE_FILE down"
echo "Restart service:  docker-compose -f $COMPOSE_FILE restart [service-name]"
echo "Check status:     docker-compose -f $COMPOSE_FILE ps"