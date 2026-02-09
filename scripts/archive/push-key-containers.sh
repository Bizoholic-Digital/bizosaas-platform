#!/bin/bash

# Push Key Local Docker Containers to GitHub Container Registry
# This script pushes the most important containers first

set -e

REGISTRY="ghcr.io"
REPO="bizoholic-digital/bizosaas-platform"
TAG="staging-$(date +%Y%m%d-%H%M%S)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Pushing Key Containers to GitHub CR${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if we have the GitHub token
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}Error: GITHUB_TOKEN environment variable not set${NC}"
    echo "Please set your GitHub token:"
    echo "export GITHUB_TOKEN=ghp_your_token_here"
    echo ""
    echo "Or run with token:"
    echo "GITHUB_TOKEN=ghp_your_token_here ./push-key-containers.sh"
    exit 1
fi

# Function to tag and push container
push_container() {
    local local_image=$1
    local service_name=$2

    echo -e "${YELLOW}Processing: $service_name${NC}"
    echo "Local image: $local_image"

    # Check if local image exists
    if ! docker image inspect "$local_image" >/dev/null 2>&1; then
        echo -e "${RED}✗ Local image not found: $local_image${NC}"
        return 1
    fi

    # New image name in GitHub Container Registry
    local new_image="$REGISTRY/$REPO/$service_name:$TAG"
    local latest_image="$REGISTRY/$REPO/$service_name:latest"

    echo "Tagging as: $new_image"

    # Tag for versioned push
    docker tag "$local_image" "$new_image"

    # Tag for latest
    docker tag "$local_image" "$latest_image"

    echo "Pushing to GitHub Container Registry..."

    # Push versioned tag
    if docker push "$new_image"; then
        echo -e "${GREEN}✓ Pushed versioned: $new_image${NC}"
    else
        echo -e "${RED}✗ Failed to push versioned: $new_image${NC}"
        return 1
    fi

    # Push latest tag
    if docker push "$latest_image"; then
        echo -e "${GREEN}✓ Pushed latest: $latest_image${NC}"
    else
        echo -e "${RED}✗ Failed to push latest: $latest_image${NC}"
        return 1
    fi

    echo -e "${GREEN}✓ Successfully pushed: $service_name${NC}"
    echo ""
    return 0
}

# Login to GitHub Container Registry
echo -e "${YELLOW}Logging into GitHub Container Registry...${NC}"
if echo "$GITHUB_TOKEN" | docker login ghcr.io -u token --password-stdin; then
    echo -e "${GREEN}✓ Successfully logged in to GitHub Container Registry${NC}"
else
    echo -e "${RED}✗ Failed to login to GitHub Container Registry${NC}"
    echo "Please check your GITHUB_TOKEN"
    exit 1
fi

echo ""
echo -e "${BLUE}Starting container push process...${NC}"
echo ""

# Track success/failure
SUCCESSFUL_PUSHES=0
FAILED_PUSHES=0

# Push key containers first (most critical ones)
echo -e "${BLUE}=== Critical Infrastructure ===${NC}"
if push_container "bizosaas-brain-gateway:latest" "brain-api"; then
    ((SUCCESSFUL_PUSHES++))
else
    ((FAILED_PUSHES++))
fi

if push_container "redis:7-alpine" "redis"; then
    ((SUCCESSFUL_PUSHES++))
else
    ((FAILED_PUSHES++))
fi

if push_container "postgres:15-alpine" "postgres"; then
    ((SUCCESSFUL_PUSHES++))
else
    ((FAILED_PUSHES++))
fi

echo -e "${BLUE}=== Key Backend Services ===${NC}"
if push_container "coreldove-backend-coreldove-backend:latest" "coreldove-backend"; then
    ((SUCCESSFUL_PUSHES++))
else
    ((FAILED_PUSHES++))
fi

if push_container "bizosaas-business-directory-backend:latest" "directory-api"; then
    ((SUCCESSFUL_PUSHES++))
else
    ((FAILED_PUSHES++))
fi

echo -e "${BLUE}=== Key Frontend Services ===${NC}"
if push_container "bizoholic-frontend:dev" "bizoholic-frontend"; then
    ((SUCCESSFUL_PUSHES++))
else
    ((FAILED_PUSHES++))
fi

if push_container "bizosaas-coreldove-frontend:latest" "coreldove-frontend"; then
    ((SUCCESSFUL_PUSHES++))
else
    ((FAILED_PUSHES++))
fi

if push_container "bizosaas-client-portal:latest" "client-portal"; then
    ((SUCCESSFUL_PUSHES++))
else
    ((FAILED_PUSHES++))
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Container Push Summary${NC}"
echo -e "${GREEN}========================================${NC}"
echo "Successful pushes: $SUCCESSFUL_PUSHES"
echo "Failed pushes: $FAILED_PUSHES"
echo ""

if [ $FAILED_PUSHES -eq 0 ]; then
    echo -e "${GREEN}✓ All containers pushed successfully!${NC}"
    echo ""
    echo "Images are now available at:"
    echo "https://github.com/Bizoholic-Digital/bizosaas-platform/pkgs/container"
    echo ""
    echo "Next steps:"
    echo "1. Update Dokploy configurations to use these images"
    echo "2. Deploy to Dokploy staging environment"
    echo "3. Test the deployment"
else
    echo -e "${YELLOW}⚠ Some containers failed to push${NC}"
    echo "Check the errors above and retry if needed"
fi

echo ""
echo -e "${BLUE}Tagged with:${NC}"
echo "- $TAG (timestamped)"
echo "- latest (always current)"