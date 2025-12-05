#!/bin/bash

# BizOSaaS Container Cleanup Script
# Removes old containers, images, and networks that don't follow the new naming convention

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

echo "🧹 BizOSaaS Container Cleanup"
echo "============================="

# Stop and remove old containers that don't follow naming convention
print_status "Stopping and removing old containers..."

old_containers=(
    "shared-postgres" "shared-dragonfly" "shared-redis" "shared-vault" "shared-traefik" "shared-n8n"
    "bizoholic-postgres" "bizoholic-redis" "bizoholic-strapi" "bizoholic-byok-manager" 
    "bizoholic-wagtail-cms" "bizoholic-auth-service" "bizoholic-coreldove-workflow-sync"
    "strapi-latest-bizosaas" "coreldove-nginx" "coreldove-api" "coreldove-wordpress"
    "bizosaas-temporal-web-1" "bizosaas-temporal-1" "bizosaas-adminer-1" "bizosaas-temporal-elasticsearch-1"
    "shared-n8n-dev" "shared-redis-dev" "shared-postgres-dev"
)

for container in "${old_containers[@]}"; do
    if docker ps -aq -f name="^${container}$" >/dev/null 2>&1; then
        print_status "Removing container: $container"
        docker stop "$container" 2>/dev/null || true
        docker rm "$container" 2>/dev/null || true
    fi
done

# Remove old images
print_status "Removing old images..."

old_images=(
    "bizoholic-byok-manager"
    "bizoholic-coreldove-workflow-sync"  
    "bizoholic-auth-service"
    "coreldove-wordpress"
    "coreldove-api"
    "strapi/strapi"
)

for image in "${old_images[@]}"; do
    if docker images -q "$image" >/dev/null 2>&1; then
        print_status "Removing image: $image"
        docker rmi "$image" 2>/dev/null || true
    fi
done

# Clean up orphaned volumes
print_status "Cleaning up orphaned volumes..."
docker volume prune -f >/dev/null 2>&1

# Clean up orphaned networks  
print_status "Cleaning up orphaned networks..."
docker network prune -f >/dev/null 2>&1

# Remove old networks that don't match our naming
old_networks=(
    "shared-development_default"
    "bizoholic_default" 
    "bizosaas_default"
    "shared-network"
)

for network in "${old_networks[@]}"; do
    if docker network ls -q -f name="^${network}$" >/dev/null 2>&1; then
        print_status "Removing network: $network"
        docker network rm "$network" 2>/dev/null || true
    fi
done

# Clean up dangling images
print_status "Removing dangling images..."
docker image prune -f >/dev/null 2>&1

# Show current containers with our naming convention
print_status "Current BizOSaaS containers:"
if docker ps -a --filter "label=bizosaas.service.category" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null; then
    echo ""
else
    print_warning "No BizOSaaS containers found with proper labels"
fi

# Show current images with our naming convention
print_status "Current BizOSaaS images:"
docker images --filter "reference=bizosaas/*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" 2>/dev/null || print_warning "No BizOSaaS images found"

print_success "Cleanup completed!"
echo ""
echo "📊 Docker system overview:"
echo "========================="
docker system df

echo ""
echo "🚀 To start the clean BizOSaaS environment:"
echo "./start-bizosaas-production.sh"