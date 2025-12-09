#!/bin/bash
# cleanup-docker-resources.sh
# Comprehensive cleanup of unused Docker resources

set -e

echo "🧹 BizOSaaS Docker Cleanup Script"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Stop and remove dead/exited containers
echo -e "${YELLOW}[1/6] Removing dead and exited containers...${NC}"
docker ps -a --filter "status=dead" --filter "status=exited" --format "{{.Names}}" | while read container; do
    if [[ ! "$container" =~ ^(brain-|authentik-|portainer|registry).*$ ]]; then
        echo "  Removing: $container"
        docker rm -f "$container" 2>/dev/null || true
    fi
done

# Remove unused volumes
echo -e "${YELLOW}[2/6] Removing unused volumes...${NC}"
KEEP_VOLUMES=(
    "bizosaas-brain-core_postgres-data"
    "bizosaas-brain-core_redis-data"
    "portainer_data"
    "brain-network"
)

docker volume ls -q | while read volume; do
    KEEP=false
    for keep_vol in "${KEEP_VOLUMES[@]}"; do
        if [[ "$volume" == "$keep_vol" ]]; then
            KEEP=true
            break
        fi
    done
    
    if [[ "$KEEP" == false ]]; then
        # Check if volume is in use
        if ! docker ps -a --filter "volume=$volume" --format "{{.Names}}" | grep -q .; then
            echo "  Removing unused volume: $volume"
            docker volume rm "$volume" 2>/dev/null || true
        fi
    fi
done

# Remove dangling images
echo -e "${YELLOW}[3/6] Removing dangling images...${NC}"
docker image prune -f

# Remove unused networks
echo -e "${YELLOW}[4/6] Removing unused networks...${NC}"
KEEP_NETWORKS=(
    "brain-network"
    "bridge"
    "host"
    "none"
)

docker network ls --format "{{.Name}}" | while read network; do
    KEEP=false
    for keep_net in "${KEEP_NETWORKS[@]}"; do
        if [[ "$network" == "$keep_net" ]]; then
            KEEP=true
            break
        fi
    done
    
    if [[ "$KEEP" == false ]]; then
        echo "  Removing unused network: $network"
        docker network rm "$network" 2>/dev/null || true
    fi
done

# Remove old/unused images (keep only latest and current versions)
echo -e "${YELLOW}[5/6] Removing old image versions...${NC}"
# Keep only images used by running containers and core services
docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>" | while read image; do
    # Skip if image is used by a running container
    if docker ps --format "{{.Image}}" | grep -q "$image"; then
        continue
    fi
    
    # Skip core images
    if [[ "$image" =~ ^(bizosaas-brain-core|ghcr.io/goauthentik|portainer|redis|postgres|vault|temporal|grafana|prom|jaeger|registry).*$ ]]; then
        continue
    fi
    
    # Remove old versions
    echo "  Removing unused image: $image"
    docker rmi "$image" 2>/dev/null || true
done

# System prune (removes all unused data)
echo -e "${YELLOW}[6/6] Final system cleanup...${NC}"
docker system prune -f --volumes

echo ""
echo -e "${GREEN}✅ Cleanup complete!${NC}"
echo ""
echo "Current resource usage:"
docker system df
