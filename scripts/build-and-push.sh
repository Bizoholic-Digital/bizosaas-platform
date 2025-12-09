#!/bin/bash
# Build and push all BizOSaaS images to Docker Registry

set -e

# Configuration
REGISTRY="${REGISTRY:-localhost:5000}"
VERSION="${1:-latest}"
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  BizOSaaS - Build & Push Images       ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Registry: ${GREEN}$REGISTRY${NC}"
echo -e "Version:  ${GREEN}$VERSION${NC}"
echo -e "Commit:   ${GREEN}$GIT_COMMIT${NC}"
echo ""

# Function to build and push image
build_and_push() {
    local SERVICE_NAME=$1
    local CONTEXT_PATH=$2
    local DOCKERFILE=${3:-Dockerfile}
    
    echo -e "${YELLOW}Building $SERVICE_NAME...${NC}"
    
    IMAGE_NAME="$REGISTRY/bizosaas/$SERVICE_NAME"
    
    docker build \
        --build-arg BUILD_DATE="$BUILD_DATE" \
        --build-arg GIT_COMMIT="$GIT_COMMIT" \
        --build-arg VERSION="$VERSION" \
        -t "$IMAGE_NAME:$VERSION" \
        -t "$IMAGE_NAME:latest" \
        -f "$CONTEXT_PATH/$DOCKERFILE" \
        "$CONTEXT_PATH"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Build successful: $SERVICE_NAME${NC}"
        
        echo -e "${YELLOW}Pushing $SERVICE_NAME to registry...${NC}"
        docker push "$IMAGE_NAME:$VERSION"
        docker push "$IMAGE_NAME:latest"
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Push successful: $SERVICE_NAME${NC}"
        else
            echo -e "${RED}✗ Push failed: $SERVICE_NAME${NC}"
            return 1
        fi
    else
        echo -e "${RED}✗ Build failed: $SERVICE_NAME${NC}"
        return 1
    fi
    
    echo ""
}

# Build Brain Gateway
build_and_push "brain-gateway" "./bizosaas-brain-core/brain-gateway" "Dockerfile"

# Build Auth Service
build_and_push "auth-service" "./bizosaas-brain-core/auth" "Dockerfile"

# Build Client Portal
build_and_push "client-portal" "./portals/client-portal" "Dockerfile.prod"

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}  All images built and pushed!         ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Images available at:"
echo -e "  - ${GREEN}$REGISTRY/bizosaas/brain-gateway:$VERSION${NC}"
echo -e "  - ${GREEN}$REGISTRY/bizosaas/auth-service:$VERSION${NC}"
echo -e "  - ${GREEN}$REGISTRY/bizosaas/client-portal:$VERSION${NC}"
echo ""
echo -e "To deploy locally:"
echo -e "  ${YELLOW}docker-compose -f docker-compose.registry.yml up -d${NC}"
echo ""
