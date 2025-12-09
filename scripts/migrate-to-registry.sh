#!/bin/bash
# Migrate from CLI-based deployment to Registry-based deployment

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  BizOSaaS - Migration to Registry      ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Step 1: Stop existing containers
echo -e "${YELLOW}[1/4] Stopping existing containers...${NC}"

# Stop containers started by start-bizosaas-core-full.sh
cd bizosaas-brain-core
docker-compose down 2>/dev/null || true
docker-compose -f docker-compose.observability.yml down 2>/dev/null || true
cd ..

# Stop any remaining brain-* containers
docker stop $(docker ps -q --filter "name=brain-*") 2>/dev/null || true

echo -e "${GREEN}✓ Existing containers stopped${NC}"

# Step 2: Preserve data volumes
echo -e "${YELLOW}[2/4] Checking data volumes...${NC}"

VOLUMES=$(docker volume ls -q | grep -E "bizosaas|brain" || true)

if [ -n "$VOLUMES" ]; then
    echo -e "${GREEN}✓ Found existing data volumes (will be preserved):${NC}"
    echo "$VOLUMES" | while read vol; do
        echo -e "  - ${BLUE}$vol${NC}"
    done
else
    echo -e "${YELLOW}⚠ No existing volumes found${NC}"
fi

# Step 3: Deploy with registry
echo -e "${YELLOW}[3/4] Deploying with registry-based configuration...${NC}"

./scripts/deploy-local.sh

# Step 4: Verify migration
echo -e "${YELLOW}[4/4] Verifying migration...${NC}"

sleep 5

# Check if services are running
RUNNING=$(docker ps --filter "label=com.bizosaas.service" --format "{{.Names}}" | wc -l)

if [ "$RUNNING" -gt 0 ]; then
    echo -e "${GREEN}✓ Migration successful! $RUNNING services running${NC}"
else
    echo -e "${RED}✗ Migration failed. No services running.${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}  Migration Complete!                  ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Your services are now managed via:"
echo -e "  - ${GREEN}Docker Registry${NC} (localhost:5000)"
echo -e "  - ${GREEN}Local Domains${NC} (*.bizosaas.local)"
echo -e "  - ${GREEN}Portainer${NC} (https://localhost:9443)"
echo ""
echo -e "Access your portal at:"
echo -e "  ${GREEN}http://portal.bizosaas.local${NC}"
echo ""
echo -e "Old deployment method:"
echo -e "  ${RED}✗ ./scripts/start-bizosaas-core-full.sh${NC} (deprecated)"
echo ""
echo -e "New deployment method:"
echo -e "  ${GREEN}✓ ./scripts/deploy-local.sh${NC} (recommended)"
echo ""
