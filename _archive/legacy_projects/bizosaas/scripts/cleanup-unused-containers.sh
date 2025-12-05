#!/bin/bash

# BizOSaaS Platform - Container Cleanup Script
# Removes stopped/unnecessary containers for clean setup

set -e

echo "=========================================="
echo "BizOSaaS Platform Container Cleanup"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Step 1: Identifying Stopped Containers${NC}"
echo "--------------------------------------"

# List stopped containers to be removed
STOPPED_CONTAINERS=$(docker ps -a --filter "status=exited" --format "{{.Names}}" | grep -E "bizosaas|bizoholic|coreldove|thrillring" || true)

if [ -z "$STOPPED_CONTAINERS" ]; then
    echo -e "${GREEN}No stopped containers to remove${NC}"
else
    echo "Stopped containers found:"
    echo "$STOPPED_CONTAINERS"
    echo ""

    read -p "Remove these containers? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "$STOPPED_CONTAINERS" | xargs docker rm -f
        echo -e "${GREEN}✓ Stopped containers removed${NC}"
    else
        echo -e "${YELLOW}Skipped container removal${NC}"
    fi
fi

echo ""
echo -e "${YELLOW}Step 2: Identifying Duplicate/Redundant Containers${NC}"
echo "--------------------------------------"

# Specific containers to check and potentially remove
DUPLICATE_CONTAINERS=(
    "thrillring-gaming-3005-final"
    "bizoholic-frontend-3000"
    "bizosaas-sqladmin-comprehensive-fixed"
    "bizosaas-superset-8088"
)

for container in "${DUPLICATE_CONTAINERS[@]}"; do
    if docker ps -a --format "{{.Names}}" | grep -q "^${container}$"; then
        STATUS=$(docker inspect --format='{{.State.Status}}' "$container" 2>/dev/null || echo "not found")
        if [ "$STATUS" != "running" ]; then
            echo -e "${YELLOW}Found duplicate/stopped: $container (Status: $STATUS)${NC}"
            read -p "Remove $container? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                docker rm -f "$container" 2>/dev/null && echo -e "${GREEN}✓ Removed $container${NC}" || echo -e "${RED}Failed to remove $container${NC}"
            fi
        fi
    fi
done

echo ""
echo -e "${YELLOW}Step 3: Removing Unused Docker Images${NC}"
echo "--------------------------------------"

echo "Current disk usage:"
docker system df

echo ""
read -p "Prune unused images? This will remove dangling images. (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker image prune -f
    echo -e "${GREEN}✓ Pruned unused images${NC}"
else
    echo -e "${YELLOW}Skipped image pruning${NC}"
fi

echo ""
echo -e "${YELLOW}Step 4: Removing Unused Volumes${NC}"
echo "--------------------------------------"

echo "WARNING: This will remove all unused volumes!"
read -p "Prune unused volumes? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker volume prune -f
    echo -e "${GREEN}✓ Pruned unused volumes${NC}"
else
    echo -e "${YELLOW}Skipped volume pruning${NC}"
fi

echo ""
echo -e "${YELLOW}Step 5: Removing Unused Networks${NC}"
echo "--------------------------------------"

docker network prune -f
echo -e "${GREEN}✓ Pruned unused networks${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}Cleanup Complete!${NC}"
echo "=========================================="
echo ""

echo "Current resource usage:"
docker system df

echo ""
echo "Running containers:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Size}}"

echo ""
echo -e "${GREEN}Platform is now optimized and clean!${NC}"
echo ""
