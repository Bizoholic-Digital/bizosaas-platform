#!/bin/bash

# CoreLDove Frontend Containerization Script
# This script automates the containerization process once Docker is working

set -e

echo "🚀 CoreLDove Frontend Containerization Script"
echo "=============================================="

# Configuration
CONTAINER_NAME="coreldove-frontend-3012"
IMAGE_NAME="bizosaas/coreldove-frontend"
IMAGE_TAG="latest"
PORT="3012"
DOCKERFILE="Dockerfile.production"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to check if Docker is working
check_docker() {
    echo "🔍 Checking Docker daemon status..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker not installed"
        exit 1
    fi
    
    if ! timeout 10 docker version &> /dev/null; then
        print_error "Docker daemon not responding"
        print_warning "Please ensure Docker Desktop is running and try again"
        exit 1
    fi
    
    print_status "Docker daemon is running"
}

# Function to stop existing container if running
stop_existing_container() {
    echo "🛑 Checking for existing container..."
    
    if docker ps -q -f name=$CONTAINER_NAME &> /dev/null; then
        print_warning "Stopping existing container: $CONTAINER_NAME"
        docker stop $CONTAINER_NAME || true
        docker rm $CONTAINER_NAME || true
    fi
    
    print_status "No conflicting containers running"
}

# Function to check if npm dev is running and stop it
stop_npm_dev() {
    echo "🔍 Checking for npm dev processes on port $PORT..."
    
    local npm_pid=$(pgrep -f "next dev --port $PORT" || true)
    if [ ! -z "$npm_pid" ]; then
        print_warning "Stopping npm dev process (PID: $npm_pid)"
        kill $npm_pid || true
        sleep 3
    fi
    
    print_status "Port $PORT is ready for container"
}

# Function to build Docker image
build_image() {
    echo "🏗️ Building Docker image..."
    
    if [ ! -f "$DOCKERFILE" ]; then
        print_error "Dockerfile not found: $DOCKERFILE"
        exit 1
    fi
    
    print_status "Building image: $IMAGE_NAME:$IMAGE_TAG"
    docker build -f $DOCKERFILE -t $IMAGE_NAME:$IMAGE_TAG .
    
    print_status "Image built successfully"
}

# Function to run container
run_container() {
    echo "🚀 Starting container..."
    
    docker run -d \
        --name $CONTAINER_NAME \
        --restart unless-stopped \
        -p $PORT:$PORT \
        --network bizosaas-network \
        -e NODE_ENV=production \
        -e PORT=$PORT \
        -e NEXT_PUBLIC_API_BASE_URL=http://localhost:8001 \
        -e NEXT_PUBLIC_BRAIN_API_URL=http://bizosaas-brain-core-8001:8001 \
        -e NEXT_PUBLIC_SALEOR_API_URL=http://bizosaas-saleor-api-8003:8000 \
        $IMAGE_NAME:$IMAGE_TAG
    
    print_status "Container started: $CONTAINER_NAME"
}

# Function to check container health
check_health() {
    echo "🏥 Checking container health..."
    
    sleep 10
    
    if docker ps | grep -q $CONTAINER_NAME; then
        print_status "Container is running"
        
        # Test HTTP response
        local retries=0
        local max_retries=12
        
        while [ $retries -lt $max_retries ]; do
            if curl -sf http://localhost:$PORT > /dev/null 2>&1; then
                print_status "Frontend is responding on http://localhost:$PORT"
                return 0
            fi
            
            retries=$((retries + 1))
            echo "Waiting for frontend to start... ($retries/$max_retries)"
            sleep 5
        done
        
        print_error "Frontend not responding after 60 seconds"
        docker logs $CONTAINER_NAME
        return 1
    else
        print_error "Container failed to start"
        docker logs $CONTAINER_NAME
        return 1
    fi
}

# Function to show container information
show_info() {
    echo ""
    echo "📊 Container Information"
    echo "======================="
    echo "Container Name: $CONTAINER_NAME"
    echo "Image: $IMAGE_NAME:$IMAGE_TAG"
    echo "Port: $PORT"
    echo "URL: http://localhost:$PORT"
    echo ""
    echo "🔧 Management Commands:"
    echo "View logs: docker logs $CONTAINER_NAME"
    echo "Stop container: docker stop $CONTAINER_NAME"
    echo "Restart container: docker restart $CONTAINER_NAME"
    echo "Remove container: docker rm -f $CONTAINER_NAME"
    echo ""
}

# Main execution
main() {
    echo "Starting containerization process..."
    
    check_docker
    stop_npm_dev
    stop_existing_container
    build_image
    run_container
    check_health
    show_info
    
    print_status "CoreLDove frontend successfully containerized!"
    print_status "Visit: http://localhost:$PORT"
}

# Handle interruption
trap 'print_error "Script interrupted"; exit 1' INT

# Run main function
main "$@"