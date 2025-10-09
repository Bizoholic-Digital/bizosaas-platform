#!/bin/bash

# Docker Optimization and Cleanup Script
# Reclaim space while keeping active containers running

echo "=========================================="
echo "Docker Cleanup & Optimization"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Current Docker Disk Usage:${NC}"
docker system df
echo ""

echo -e "${YELLOW}Cleanup Plan:${NC}"
echo "  1. Remove stopped containers"
echo "  2. Remove unused images"
echo "  3. Remove unused volumes"
echo "  4. Clean build cache"
echo ""

read -p "Proceed with cleanup? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo -e "${BLUE}Step 1: Removing Stopped Containers${NC}"
STOPPED=$(docker ps -a -q --filter "status=exited" | wc -l)
if [ "$STOPPED" -gt 0 ]; then
    docker ps -a -q --filter "status=exited" | xargs docker rm 2>/dev/null
    echo -e "${GREEN}✓ Removed $STOPPED stopped containers${NC}"
else
    echo -e "${GREEN}✓ No stopped containers to remove${NC}"
fi

echo ""
echo -e "${BLUE}Step 2: Removing Unused Images${NC}"
echo "  Keeping images used by running containers..."
BEFORE_IMAGES=$(docker images -q | wc -l)
docker image prune -a -f --filter "until=24h" 2>/dev/null
AFTER_IMAGES=$(docker images -q | wc -l)
REMOVED_IMAGES=$((BEFORE_IMAGES - AFTER_IMAGES))
echo -e "${GREEN}✓ Removed $REMOVED_IMAGES unused images${NC}"

echo ""
echo -e "${BLUE}Step 3: Removing Unused Volumes${NC}"
BEFORE_VOLUMES=$(docker volume ls -q | wc -l)
docker volume prune -f 2>/dev/null
AFTER_VOLUMES=$(docker volume ls -q | wc -l)
REMOVED_VOLUMES=$((BEFORE_VOLUMES - AFTER_VOLUMES))
echo -e "${GREEN}✓ Removed $REMOVED_VOLUMES unused volumes${NC}"

echo ""
echo -e "${BLUE}Step 4: Cleaning Build Cache${NC}"
docker builder prune -a -f 2>/dev/null
echo -e "${GREEN}✓ Build cache cleaned${NC}"

echo ""
echo -e "${BLUE}Step 5: Removing Unused Networks${NC}"
docker network prune -f 2>/dev/null
echo -e "${GREEN}✓ Unused networks removed${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}Cleanup Complete!${NC}"
echo "=========================================="
echo ""

echo -e "${BLUE}New Docker Disk Usage:${NC}"
docker system df
echo ""

echo -e "${YELLOW}Summary:${NC}"
echo "  • Stopped containers removed: $STOPPED"
echo "  • Unused images removed: $REMOVED_IMAGES"
echo "  • Unused volumes removed: $REMOVED_VOLUMES"
echo "  • Build cache cleaned"
echo ""

echo -e "${GREEN}Active Containers Still Running:${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "bizosaas|bizoholic|coreldove|business|thrillring"
echo ""

echo -e "${BLUE}Space reclaimed! Platform continues running normally.${NC}"
