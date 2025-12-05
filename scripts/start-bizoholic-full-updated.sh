#!/bin/bash
# Start all Bizoholic services with proper resource limits
# Updated: Always show running services at the end

set -e

echo "🚀 Starting Bizoholic Full Stack"
echo "================================="

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Step 1: Infrastructure
echo -e "\n${YELLOW}Step 1/5: Starting Infrastructure (Postgres, Redis, Vault)...${NC}"
docker-compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres redis vault
echo -e "${GREEN}✓ Infrastructure started${NC}"
sleep 5

# Step 2: Backend
echo -e "\n${YELLOW}Step 2/5: Starting Backend Services (Brain API, Auth, CRM, Wagtail)...${NC}"
RUNNING_SERVICES=$(docker ps --filter "name=bizosaas-brain-unified\|bizosaas-auth-unified\|bizosaas-django-crm\|bizosaas-wagtail-unified" --format "{{.Names}}" | wc -l)

if [ "$RUNNING_SERVICES" -gt 0 ]; then
    echo -e "${YELLOW}Restarting existing backend services...${NC}"
    docker-compose -f shared/services/docker-compose.services.yml restart brain-gateway auth crm cms
else
    echo "Starting fresh backend services..."
    docker-compose -f shared/services/docker-compose.services.yml up -d brain-gateway auth crm cms
fi
echo -e "${GREEN}✓ Backend services started${NC}"
sleep 35

# Step 3: Frontend
echo -e "\n${YELLOW}Step 3/5: Starting Frontend (Bizoholic)...${NC}"
cd brands/bizoholic/frontend
if lsof -Pi :3001 -sTCP:LISTEN -t > /dev/null ; then
    EXISTING_PID=$(lsof -Pi :3001 -sTCP:LISTEN -t)
    kill -9 $EXISTING_PID 2>/dev/null || true
    sleep 2
fi
PORT=3001 npm run dev > /tmp/bizoholic-frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > /tmp/bizoholic-frontend.pid
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
cd ../../..

# Step 4: Verify Services
echo -e "\n${YELLOW}Step 4/5: Verifying Services...${NC}"
sleep 15

check_service() {
    local name=$1
    local url=$2
    local max_retries=5
    local retry=0
    while [ $retry -lt $max_retries ]; do
        if curl -s --max-time 3 "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ $name: Running${NC}"
            return 0
        fi
        retry=$((retry + 1))
        sleep 3
    done
    echo -e "${RED}✗ $name: Not responding${NC}"
}

check_service "Frontend (3001)" "http://localhost:3001"
check_service "Brain API (8000)" "http://localhost:8000/health"
check_service "Auth (8007)" "http://localhost:8007/health"
check_service "CRM (8005)" "http://localhost:8005/health"
check_service "Wagtail CMS (8002)" "http://localhost:8002/health/"

# Step 5: Show All Running Services
echo -e "\n${YELLOW}Step 5/5: Container Status...${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "NAME|bizosaas|postgres|redis|vault"

echo -e "\n${GREEN}=================================${NC}"
echo -e "${GREEN}✓ Bizoholic Full Stack Started!${NC}"
echo -e "${GREEN}=================================${NC}"
