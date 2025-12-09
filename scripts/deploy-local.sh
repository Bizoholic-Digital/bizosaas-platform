#!/bin/bash
# Deploy BizOSaaS to local development environment

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  BizOSaaS - Local Deployment          ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Step 1: Check prerequisites
echo -e "${YELLOW}[1/6] Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed${NC}"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo -e "${RED}Docker daemon is not running${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker is ready${NC}"

# Step 2: Check /etc/hosts
echo -e "${YELLOW}[2/6] Checking local domains...${NC}"

if ! grep -q "bizosaas.local" /etc/hosts; then
    echo -e "${YELLOW}Adding local domains to /etc/hosts...${NC}"
    echo -e "${YELLOW}This requires sudo access${NC}"
    
    sudo tee -a /etc/hosts > /dev/null << EOF

# BizOSaaS Local Development
127.0.0.1    bizosaas.local
127.0.0.1    portal.bizosaas.local
127.0.0.1    api.bizosaas.local
127.0.0.1    auth.bizosaas.local
127.0.0.1    vault.bizosaas.local
127.0.0.1    temporal.bizosaas.local
127.0.0.1    grafana.bizosaas.local
127.0.0.1    prometheus.bizosaas.local
127.0.0.1    jaeger.bizosaas.local
EOF
    
    echo -e "${GREEN}✓ Local domains added${NC}"
else
    echo -e "${GREEN}✓ Local domains already configured${NC}"
fi

# Step 3: Create network
echo -e "${YELLOW}[3/6] Creating Docker network...${NC}"
docker network create brain-network 2>/dev/null || echo -e "${GREEN}✓ Network already exists${NC}"

# Step 4: Build and push images
echo -e "${YELLOW}[4/6] Building Docker images...${NC}"
./scripts/build-and-push.sh latest

# Step 5: Stop existing containers
echo -e "${YELLOW}[5/6] Stopping existing containers...${NC}"
docker-compose -f docker-compose.registry.yml down 2>/dev/null || true
echo -e "${GREEN}✓ Existing containers stopped${NC}"

# Step 6: Deploy
echo -e "${YELLOW}[6/6] Deploying services...${NC}"
docker-compose -f docker-compose.registry.yml --env-file .env.local up -d

# Wait for services to be healthy
echo -e "${YELLOW}Waiting for services to be healthy...${NC}"
sleep 10

# Check health
echo -e "${YELLOW}Checking service health...${NC}"

SERVICES=(
    "bizosaas-postgres:PostgreSQL"
    "bizosaas-redis:Redis"
    "bizosaas-vault:Vault"
    "bizosaas-temporal:Temporal"
    "bizosaas-brain-gateway:Brain Gateway"
    "bizosaas-auth:Auth Service"
    "bizosaas-client-portal:Client Portal"
)

ALL_HEALTHY=true

for SERVICE in "${SERVICES[@]}"; do
    CONTAINER="${SERVICE%%:*}"
    NAME="${SERVICE##*:}"
    
    if docker ps --filter "name=$CONTAINER" --filter "status=running" | grep -q "$CONTAINER"; then
        echo -e "${GREEN}✓ $NAME is running${NC}"
    else
        echo -e "${RED}✗ $NAME is not running${NC}"
        ALL_HEALTHY=false
    fi
done

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}  Deployment Complete!                 ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Access your services at:"
echo -e "  - Portal:      ${GREEN}http://portal.bizosaas.local${NC}"
echo -e "  - API Docs:    ${GREEN}http://api.bizosaas.local/docs${NC}"
echo -e "  - Auth:        ${GREEN}http://auth.bizosaas.local/docs${NC}"
echo -e "  - Vault:       ${GREEN}http://vault.bizosaas.local${NC}"
echo -e "  - Temporal UI: ${GREEN}http://temporal.bizosaas.local${NC}"
echo -e "  - Grafana:     ${GREEN}http://grafana.bizosaas.local${NC} (admin/admin)"
echo -e "  - Prometheus:  ${GREEN}http://prometheus.bizosaas.local${NC}"
echo -e "  - Jaeger:      ${GREEN}http://jaeger.bizosaas.local${NC}"
echo ""
echo -e "To view logs:"
echo -e "  ${YELLOW}docker-compose -f docker-compose.registry.yml logs -f${NC}"
echo ""
echo -e "To stop all services:"
echo -e "  ${YELLOW}docker-compose -f docker-compose.registry.yml down${NC}"
echo ""

if [ "$ALL_HEALTHY" = false ]; then
    echo -e "${YELLOW}⚠ Some services are not running. Check logs for details.${NC}"
    exit 1
fi
