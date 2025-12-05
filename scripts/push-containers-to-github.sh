#!/bin/bash

# Push Local Docker Containers to GitHub Container Registry
# Usage: ./push-containers-to-github.sh

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
echo -e "${BLUE}Pushing Local Containers to GitHub CR${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Registry: $REGISTRY"
echo "Repository: $REPO"
echo "Tag: $TAG"
echo ""

# Function to tag and push container
push_container() {
    local local_image=$1
    local service_name=$2

    echo -e "${YELLOW}Processing: $service_name${NC}"
    echo "Local image: $local_image"

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
    docker push "$new_image"

    # Push latest tag
    docker push "$latest_image"

    echo -e "${GREEN}✓ Successfully pushed: $service_name${NC}"
    echo ""
}

# Login to GitHub Container Registry
echo -e "${YELLOW}Logging into GitHub Container Registry...${NC}"
echo "$GITHUB_TOKEN" | docker login ghcr.io -u USERNAME --password-stdin

echo ""
echo -e "${BLUE}Starting container push process...${NC}"
echo ""

# Infrastructure Services (6 containers)
echo -e "${BLUE}=== Infrastructure Services ===${NC}"
push_container "postgres:15-alpine" "postgres"
push_container "redis:7-alpine" "redis"
push_container "hashicorp/vault:1.15" "vault"
push_container "temporalio/auto-setup:1.22.0" "temporal-server"
push_container "temporalio/ui:2.21.0" "temporal-ui"
push_container "bizosaas-platform-temporal-integration:latest" "temporal-integration"

# Backend Services (8 containers)
echo -e "${BLUE}=== Backend Services ===${NC}"
push_container "bizosaas-brain-gateway:latest" "brain-api"
push_container "bizosaas-wagtail-cms:latest" "wagtail-cms"
push_container "django-crm-django-crm" "django-crm"
push_container "bizosaas-business-directory-backend:latest" "directory-api"
push_container "coreldove-backend-coreldove-backend:latest" "coreldove-backend"
push_container "bizosaas-platform-bizosaas-brain-enhanced:latest" "ai-agents"
push_container "bizosaas/amazon-sourcing:latest" "amazon-sourcing"
push_container "ghcr.io/saleor/saleor:3.20" "saleor"

# Frontend Services (6 containers)
echo -e "${BLUE}=== Frontend Services ===${NC}"
push_container "bizoholic-frontend:dev" "bizoholic-frontend"
push_container "bizosaas-client-portal:latest" "client-portal"
push_container "bizosaas-coreldove-frontend:latest" "coreldove-frontend"
push_container "bizosaas-business-directory:latest" "business-directory"
push_container "node:20-alpine" "thrillring-gaming"
push_container "bizosaas-bizosaas-admin:latest" "admin-dashboard"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}All containers pushed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Images are now available at:"
echo "https://github.com/Bizoholic-Digital/bizosaas-platform/pkgs/container"
echo ""
echo "Tagged versions:"
echo "- $TAG (timestamped)"
echo "- latest (always current)"
echo ""
echo -e "${BLUE}Next step: Update Dokploy to use these images${NC}"

# Generate Dokploy configuration with new images
echo ""
echo -e "${YELLOW}Generating updated Dokploy configurations...${NC}"

# Update infrastructure config
sed "s|image: postgres:15-alpine|image: $REGISTRY/$REPO/postgres:latest|g" dokploy-infrastructure-staging.yml > dokploy-infrastructure-from-github.yml
sed -i "s|image: redis:7-alpine|image: $REGISTRY/$REPO/redis:latest|g" dokploy-infrastructure-from-github.yml
sed -i "s|image: hashicorp/vault:1.15|image: $REGISTRY/$REPO/vault:latest|g" dokploy-infrastructure-from-github.yml
sed -i "s|image: temporalio/auto-setup:1.22.0|image: $REGISTRY/$REPO/temporal-server:latest|g" dokploy-infrastructure-from-github.yml
sed -i "s|image: temporalio/ui:2.21.0|image: $REGISTRY/$REPO/temporal-ui:latest|g" dokploy-infrastructure-from-github.yml

echo -e "${GREEN}✓ Generated: dokploy-infrastructure-from-github.yml${NC}"

# Update backend config
sed "s|build:|# build:|g" dokploy-backend-staging.yml > dokploy-backend-from-github.yml
sed -i "s|context: .*|image: $REGISTRY/$REPO/brain-api:latest|g" dokploy-backend-from-github.yml
sed -i "s|dockerfile: .*||g" dokploy-backend-from-github.yml

echo -e "${GREEN}✓ Generated: dokploy-backend-from-github.yml${NC}"

# Update frontend config
sed "s|build:|# build:|g" dokploy-frontend-staging.yml > dokploy-frontend-from-github.yml
sed -i "s|context: .*|image: $REGISTRY/$REPO/bizoholic-frontend:latest|g" dokploy-frontend-from-github.yml
sed -i "s|dockerfile: .*||g" dokploy-frontend-from-github.yml

echo -e "${GREEN}✓ Generated: dokploy-frontend-from-github.yml${NC}"

echo ""
echo -e "${BLUE}Ready for Dokploy deployment!${NC}"