#!/bin/bash

# BizOSaaS Frontend Applications - Build Script
# Builds all 4 frontend applications for production deployment

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

# Build configuration
REGISTRY="${DOCKER_REGISTRY:-bizosaas}"
TAG="${BUILD_TAG:-latest}"
PLATFORM="${DOCKER_PLATFORM:-linux/amd64}"

# Frontend applications to build
declare -A FRONTEND_APPS=(
    ["client-portal"]="3006"
    ["coreldove-frontend"]="3007"
    ["bizoholic-frontend"]="3008"
    ["bizosaas-admin"]="3009"
)

log "Starting BizOSaaS Frontend Applications Build Process"
log "Registry: $REGISTRY"
log "Tag: $TAG"
log "Platform: $PLATFORM"

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Create build directory if it doesn't exist
mkdir -p logs

# Function to build a single frontend app
build_frontend_app() {
    local app_name=$1
    local port=$2
    local context_path="./frontend/apps/$app_name"
    local image_name="$REGISTRY/$app_name:$TAG"
    
    log "Building $app_name (Port: $port)"
    
    if [ ! -d "$context_path" ]; then
        error "Directory $context_path does not exist"
        return 1
    fi
    
    # Check if Dockerfile exists
    if [ ! -f "$context_path/Dockerfile" ]; then
        error "Dockerfile not found in $context_path"
        return 1
    fi
    
    # Check if package.json exists
    if [ ! -f "$context_path/package.json" ]; then
        error "package.json not found in $context_path"
        return 1
    fi
    
    # Build the Docker image
    info "Building Docker image: $image_name"
    if docker build \
        --platform "$PLATFORM" \
        --tag "$image_name" \
        --build-arg NODE_ENV=production \
        --build-arg PORT="$port" \
        --file "$context_path/Dockerfile" \
        "$context_path" 2>&1 | tee "logs/build-$app_name.log"; then
        log "Successfully built $app_name"
        
        # Get image size
        local image_size=$(docker images --format "table {{.Size}}" "$image_name" | tail -n 1)
        info "$app_name image size: $image_size"
        
        return 0
    else
        error "Failed to build $app_name"
        return 1
    fi
}

# Function to push image to registry
push_image() {
    local app_name=$1
    local image_name="$REGISTRY/$app_name:$TAG"
    
    if [ "$PUSH_TO_REGISTRY" = "true" ]; then
        log "Pushing $image_name to registry"
        if docker push "$image_name"; then
            log "Successfully pushed $app_name"
        else
            error "Failed to push $app_name"
            return 1
        fi
    fi
}

# Function to validate environment
validate_environment() {
    log "Validating build environment"
    
    # Check for required files
    if [ ! -f ".env" ]; then
        warn ".env file not found. Using default environment variables."
    fi
    
    # Check Node.js version in Docker
    local node_version=$(docker run --rm node:18-alpine node --version)
    info "Using Node.js version: $node_version"
    
    # Check available disk space
    local available_space=$(df -h . | awk 'NR==2 {print $4}')
    info "Available disk space: $available_space"
}

# Main build process
main() {
    local failed_builds=()
    local successful_builds=()
    
    validate_environment
    
    # Build each frontend application
    for app_name in "${!FRONTEND_APPS[@]}"; do
        local port=${FRONTEND_APPS[$app_name]}
        
        if build_frontend_app "$app_name" "$port"; then
            successful_builds+=("$app_name")
            push_image "$app_name"
        else
            failed_builds+=("$app_name")
        fi
    done
    
    # Report results
    log "Build Summary:"
    
    if [ ${#successful_builds[@]} -gt 0 ]; then
        log "Successful builds:"
        for app in "${successful_builds[@]}"; do
            info "  ✓ $app"
        done
    fi
    
    if [ ${#failed_builds[@]} -gt 0 ]; then
        error "Failed builds:"
        for app in "${failed_builds[@]}"; do
            error "  ✗ $app"
        done
        
        log "Check build logs in the logs/ directory for details"
        exit 1
    else
        log "All frontend applications built successfully!"
        
        # Display final images
        log "Built images:"
        for app_name in "${!FRONTEND_APPS[@]}"; do
            local image_name="$REGISTRY/$app_name:$TAG"
            if docker images --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}" "$image_name" | tail -n 1; then
                continue
            fi
        done
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --registry)
            REGISTRY="$2"
            shift 2
            ;;
        --tag)
            TAG="$2"
            shift 2
            ;;
        --push)
            PUSH_TO_REGISTRY="true"
            shift
            ;;
        --platform)
            PLATFORM="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --registry REGISTRY    Docker registry (default: bizosaas)"
            echo "  --tag TAG              Image tag (default: latest)"
            echo "  --push                 Push images to registry"
            echo "  --platform PLATFORM   Build platform (default: linux/amd64)"
            echo "  --help                 Show this help message"
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run main build process
main