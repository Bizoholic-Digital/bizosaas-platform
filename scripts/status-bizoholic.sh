#!/bin/bash
# Check status of all Bizoholic services

echo "🔍 Bizoholic Services Status"
echo "============================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Frontend
echo -e "\n${YELLOW}Frontend (Port 3001):${NC}"
if lsof -Pi :3001 -sTCP:LISTEN -t > /dev/null 2>&1; then
    PID=$(lsof -Pi :3001 -sTCP:LISTEN -t | head -1)
    echo -e "${GREEN}✓ Running (PID: $PID)${NC}"
    
    # Check if it's responding
    if curl -s --max-time 2 http://localhost:3001 > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Responding to HTTP requests${NC}"
    else
        echo -e "${YELLOW}⚠ Process running but not responding yet (may still be compiling)${NC}"
    fi
    
    # Show recent logs
    if [ -f /tmp/bizoholic-frontend.log ]; then
        echo "Recent logs:"
        tail -5 /tmp/bizoholic-frontend.log | sed 's/^/  /'
    fi
else
    echo -e "${RED}✗ Not running${NC}"
fi

# Check Backend Services
echo -e "\n${YELLOW}Backend Services:${NC}"

check_service() {
    local name=$1
    local port=$2
    local health_path=$3
    
    echo -n "  $name (Port $port): "
    
    # Check if container is running
    CONTAINER=$(docker ps --filter "name=$name" --format "{{.Names}}" | head -1)
    if [ -z "$CONTAINER" ]; then
        echo -e "${RED}✗ Container not running${NC}"
        return 1
    fi
    
    # Check if port is listening
    if ! lsof -Pi :$port -sTCP:LISTEN -t > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠ Container running but port not listening${NC}"
        return 1
    fi
    
    # Check health endpoint
    if curl -s --max-time 2 "http://localhost:$port$health_path" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Running and healthy${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ Running but health check failed${NC}"
        return 1
    fi
}

check_service "bizosaas-brain-unified" "8000" "/health"
check_service "bizosaas-auth-unified" "8007" "/health"
check_service "bizosaas-django-crm-8000" "8005" "/health"
check_service "bizosaas-wagtail-unified" "8002" "/health/"

# Check Infrastructure
echo -e "\n${YELLOW}Infrastructure:${NC}"

check_infra() {
    local name=$1
    local port=$2
    
    echo -n "  $name (Port $port): "
    
    CONTAINER=$(docker ps --filter "name=$name" --format "{{.Names}}" | head -1)
    if [ -z "$CONTAINER" ]; then
        echo -e "${RED}✗ Not running${NC}"
        return 1
    fi
    
    if lsof -Pi :$port -sTCP:LISTEN -t > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Running${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ Container running but port not listening${NC}"
        return 1
    fi
}

check_infra "bizosaas-postgres-unified" "5432"
check_infra "bizosaas-redis-unified" "6379"
check_infra "bizosaas-vault-unified" "8200"

# Summary
echo -e "\n${YELLOW}Quick Access URLs:${NC}"
echo "  Frontend:     http://localhost:3001"
echo "  Brain API:    http://localhost:8000"
echo "  Auth:         http://localhost:8007"
echo "  CRM:          http://localhost:8005"
echo "  Wagtail CMS:  http://localhost:8002"
echo ""
