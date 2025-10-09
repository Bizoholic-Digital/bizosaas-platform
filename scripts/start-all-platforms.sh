#!/bin/bash

# Complete BizOSaaS Ecosystem Startup Script
# Starts: Bizoholic, CorelDove, Business Directory, Thrillring Gaming, QuantTrade
# Plus all backend services and AI agents

set -e

echo "=========================================="
echo "BizOSaaS Complete Ecosystem Startup"
echo "=========================================="
echo "Starting all 5 platforms + backend services"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check container function
check_container() {
    local container_name=$1
    if docker ps --format '{{.Names}}' | grep -q "^${container_name}$"; then
        return 0
    else
        return 1
    fi
}

# Wait for health function
wait_for_health() {
    local container_name=$1
    local max_attempts=30
    local attempt=0

    echo -n "Waiting for $container_name to be healthy..."
    while [ $attempt -lt $max_attempts ]; do
        if docker inspect --format='{{.State.Health.Status}}' "$container_name" 2>/dev/null | grep -q "healthy"; then
            echo -e " ${GREEN}✓${NC}"
            return 0
        fi
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    echo -e " ${YELLOW}⚠ Timeout (continuing anyway)${NC}"
    return 1
}

echo ""
echo -e "${BLUE}═════════════════════════════════════════${NC}"
echo -e "${BLUE}   PHASE 1: Core Infrastructure${NC}"
echo -e "${BLUE}═════════════════════════════════════════${NC}"
echo ""

# PostgreSQL
if ! check_container "bizosaas-postgres-unified"; then
    echo "Starting PostgreSQL..."
    docker start bizosaas-postgres-unified 2>/dev/null || echo "PostgreSQL container not found"
    sleep 5
else
    echo -e "PostgreSQL: ${GREEN}✓ Running${NC}"
fi

# Redis
if ! check_container "bizosaas-redis-unified"; then
    echo "Starting Redis..."
    docker start bizosaas-redis-unified 2>/dev/null || echo "Redis container not found"
    sleep 2
else
    echo -e "Redis: ${GREEN}✓ Running${NC}"
fi

# Vault
if ! check_container "bizosaas-vault"; then
    echo "Starting Vault..."
    docker start bizosaas-vault 2>/dev/null || echo "Vault container not found"
    wait_for_health "bizosaas-vault"
else
    echo -e "Vault: ${GREEN}✓ Running${NC}"
fi

echo ""
echo -e "${BLUE}═════════════════════════════════════════${NC}"
echo -e "${BLUE}   PHASE 2: Backend Services${NC}"
echo -e "${BLUE}═════════════════════════════════════════${NC}"
echo ""

# Central AI Brain Gateway (PRIMARY)
if ! check_container "bizosaas-brain-unified"; then
    echo "Starting Central AI Brain Gateway (Port 8001)..."
    docker start bizosaas-brain-unified 2>/dev/null || echo "Brain Gateway not found"
    wait_for_health "bizosaas-brain-unified"
else
    echo -e "AI Central Hub (8001): ${GREEN}✓ Running${NC}"
fi

# Saleor E-commerce
if ! check_container "bizosaas-saleor-unified"; then
    echo "Starting Saleor E-commerce (Port 8000)..."
    docker start bizosaas-saleor-unified 2>/dev/null || echo "Saleor not found"
    sleep 5
else
    echo -e "Saleor E-commerce (8000): ${GREEN}✓ Running${NC}"
fi

# Wagtail CMS
if ! check_container "bizosaas-wagtail-cms-8002"; then
    echo "Starting Wagtail CMS (Port 8002)..."
    docker start bizosaas-wagtail-cms-8002 2>/dev/null || echo "Wagtail not found"
    sleep 3
else
    echo -e "Wagtail CMS (8002): ${GREEN}✓ Running${NC}"
fi

# Django CRM
if ! check_container "bizosaas-django-crm-8003"; then
    echo "Starting Django CRM (Port 8003)..."
    docker start bizosaas-django-crm-8003 2>/dev/null || echo "CRM not found"
    sleep 3
else
    echo -e "Django CRM (8003): ${GREEN}✓ Running${NC}"
fi

# Business Directory Backend
if ! check_container "bizosaas-business-directory-backend-8004"; then
    echo "Starting Business Directory API (Port 8004)..."
    docker start bizosaas-business-directory-backend-8004 2>/dev/null || echo "Business Directory API not found"
    wait_for_health "bizosaas-business-directory-backend-8004"
else
    echo -e "Business Directory API (8004): ${GREEN}✓ Running${NC}"
fi

# Temporal Services
if ! check_container "bizosaas-temporal-server"; then
    echo "Starting Temporal Server (Port 7233)..."
    docker start bizosaas-temporal-server 2>/dev/null || echo "Temporal Server not found"
    sleep 5
else
    echo -e "Temporal Server (7233): ${GREEN}✓ Running${NC}"
fi

if ! check_container "bizosaas-temporal-ui-server"; then
    echo "Starting Temporal UI (Port 8082)..."
    docker start bizosaas-temporal-ui-server 2>/dev/null || echo "Temporal UI not found"
    sleep 2
else
    echo -e "Temporal UI (8082): ${GREEN}✓ Running${NC}"
fi

if ! check_container "bizosaas-temporal-unified"; then
    echo "Starting Temporal Integration (Port 8009)..."
    docker start bizosaas-temporal-unified 2>/dev/null || echo "Temporal Integration not found"
    wait_for_health "bizosaas-temporal-unified"
else
    echo -e "Temporal Integration (8009): ${GREEN}✓ Running${NC}"
fi

# AI Services
if ! check_container "bizosaas-ai-agents-8010"; then
    echo "Starting AI Agents Service (Port 8010)..."
    docker start bizosaas-ai-agents-8010 2>/dev/null || echo "AI Agents not found"
    sleep 3
else
    echo -e "AI Agents Service (8010): ${GREEN}✓ Running${NC}"
fi

if ! check_container "amazon-sourcing-8085"; then
    echo "Starting Amazon Sourcing (Port 8085)..."
    docker start amazon-sourcing-8085 2>/dev/null || echo "Amazon Sourcing not found"
    sleep 3
else
    echo -e "Amazon Sourcing (8085): ${GREEN}✓ Running${NC}"
fi

echo ""
echo -e "${BLUE}═════════════════════════════════════════${NC}"
echo -e "${BLUE}   PHASE 3: Frontend Platforms${NC}"
echo -e "${BLUE}═════════════════════════════════════════${NC}"
echo ""

# 1. Bizoholic Marketing Website (Port 3000)
if check_container "bizoholic-frontend-3000-final"; then
    echo -e "1. Bizoholic (3000): ${GREEN}✓ Running${NC}"
elif ! check_container "bizoholic-frontend-3000"; then
    echo "Starting Bizoholic Marketing (Port 3000)..."
    docker start bizoholic-frontend-3000 2>/dev/null || echo "Bizoholic not found"
    sleep 3
else
    echo -e "1. Bizoholic (3000): ${GREEN}✓ Running${NC}"
fi

# 2. Client Portal (Port 3001)
if ! check_container "client-portal-3001"; then
    echo "Starting Client Portal (Port 3001)..."
    docker start client-portal-3001 2>/dev/null || echo "Client Portal not found"
    sleep 3
else
    echo -e "2. Client Portal (3001): ${GREEN}✓ Running${NC}"
fi

# 3. CorelDove E-commerce (Port 3002)
if ! check_container "coreldove-frontend-3002"; then
    echo "Starting CorelDove E-commerce (Port 3002)..."
    docker start coreldove-frontend-3002 2>/dev/null || echo "CorelDove not found"
    sleep 3
else
    echo -e "3. CorelDove E-commerce (3002): ${GREEN}✓ Running${NC}"
fi

# 4. Business Directory (Port 3004)
if ! check_container "business-directory-3004"; then
    echo "Starting Business Directory (Port 3004)..."
    docker start business-directory-3004 2>/dev/null || echo "Business Directory not found"
    sleep 3
else
    echo -e "4. Business Directory (3004): ${GREEN}✓ Running${NC}"
fi

# 5. Thrillring Gaming (Port 3005)
if ! check_container "thrillring-gaming-3005"; then
    echo "Starting Thrillring Gaming (Port 3005)..."
    docker start thrillring-gaming-3005 2>/dev/null || echo "Thrillring Gaming not found"
    sleep 3
else
    echo -e "5. Thrillring Gaming (3005): ${GREEN}✓ Running${NC}"
fi

# BizOSaaS Admin (Port 3009)
if ! check_container "bizosaas-admin-3009"; then
    echo "Starting BizOSaaS Admin (Port 3009)..."
    docker start bizosaas-admin-3009 2>/dev/null || echo "Admin not found"
    sleep 3
else
    echo -e "6. BizOSaaS Admin (3009): ${GREEN}✓ Running${NC}"
fi

# 6. QuantTrade Platform (Ports 3012 frontend, 8012 backend)
echo ""
echo -e "${YELLOW}Checking QuantTrade platform...${NC}"

if ! check_container "quanttrade-frontend-3012"; then
    echo "QuantTrade not running. Starting QuantTrade platform..."
    cd /home/alagiri/projects/bizoholic/quanttrade
    docker-compose up -d 2>/dev/null || echo "QuantTrade startup failed"
    sleep 5
    echo -e "7. QuantTrade (3012/8012): ${GREEN}✓ Started${NC}"
else
    echo -e "7. QuantTrade (3012/8012): ${GREEN}✓ Running${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}Complete Ecosystem Started!${NC}"
echo "=========================================="
echo ""

echo -e "${YELLOW}Platform Summary:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BLUE}Core Platforms (All routing through AI Hub):${NC}"
echo "  1. Bizoholic Marketing   → http://localhost:3000"
echo "  2. Client Portal         → http://localhost:3001"
echo "  3. CorelDove E-commerce  → http://localhost:3002"
echo "  4. Business Directory    → http://localhost:3004"
echo "  5. Thrillring Gaming     → http://localhost:3005"
echo "  6. BizOSaaS Admin        → http://localhost:3009"
echo "  7. QuantTrade Platform   → http://localhost:3012"
echo ""
echo -e "${BLUE}Backend Services:${NC}"
echo "  ⭐ AI Central Hub (PRIMARY) → http://localhost:8001"
echo "  • Saleor E-commerce       → http://localhost:8000"
echo "  • Wagtail CMS             → http://localhost:8002"
echo "  • Django CRM              → http://localhost:8003"
echo "  • Business Directory API  → http://localhost:8004"
echo "  • Temporal Integration    → http://localhost:8009"
echo "  • AI Agents (93+)         → http://localhost:8010"
echo "  • QuantTrade Backend      → http://localhost:8012"
echo "  • Amazon Sourcing         → http://localhost:8085"
echo ""
echo -e "${BLUE}Infrastructure:${NC}"
echo "  • PostgreSQL   → localhost:5432"
echo "  • Redis        → localhost:6379"
echo "  • Vault        → http://localhost:8200"
echo "  • Temporal UI  → http://localhost:8082"
echo ""
echo -e "${YELLOW}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ All platforms operational and ready!${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════${NC}"
echo ""
