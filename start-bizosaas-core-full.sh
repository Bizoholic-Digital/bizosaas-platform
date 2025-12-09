#!/bin/bash
# Start BizOSaaS Platform (Full Core + Portal)

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}Starting BizOSaaS Platform (Full Stack)...${NC}"

# Check docker compose command
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

# 1. Stop existing containers to prevent port conflicts
echo -e "\n${BLUE}Step 1: Cleanup - Stopping existing containers...${NC}"
docker stop client-portal brain-gateway brain-auth brain-temporal brain-temporal-ui brain-vault brain-redis brain-postgres bizosaas-registry 2>/dev/null || true
# We don't necessarily need to RM them, up -d will recreate if changed.

# 2. Start Core Infrastructure + Backend + Frontend
echo -e "\n${YELLOW}Step 2: Starting Platform Services (Infrastructure, Backend, Frontend)...${NC}"
cd bizosaas-brain-core

# Use standard docker-compose without forced build to leverage existing images
# Disable BuildKit as buildx is missing
DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0 $DOCKER_COMPOSE up -d

# Start Authentik (Identity Provider)
echo -e "\n${YELLOW}Step 2b: Starting Authentik Identity Provider...${NC}"
DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0 $DOCKER_COMPOSE -f docker-compose.authentik.yml up -d

EXIT_CODE=$?
cd ..

# 3. Check status
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "\n${GREEN}✅ BizOSaaS Platform Started Successfully!${NC}"
    echo -e "\nAccess Points:"
    echo -e "  - Client Portal:      ${BLUE}http://localhost:3003${NC}"
    echo -e "  - API Gateway (REST): ${BLUE}http://localhost:8000/docs${NC}"
    echo -e "  - GraphQL Playground: ${BLUE}http://localhost:8000/graphql${NC}"
    echo -e "  - Authentik IdP:      ${BLUE}http://localhost:9000/if/flow/initial-setup/${NC}"
    echo -e "  - Temporal Workflow:  ${BLUE}http://localhost:8082${NC}"
    echo -e "  - Auth Service:       ${BLUE}Deprecated (Using Authentik)${NC}"
    
    echo -e "\n${BLUE}Logs: cd bizosaas-brain-core && docker-compose logs -f${NC}"
else
    echo -e "\n${RED}❌ Error starting platform. Check logs above.${NC}"
    exit 1
fi
