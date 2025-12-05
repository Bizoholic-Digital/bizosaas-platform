#!/bin/bash

# BizOSaaS Complete Platform Startup Script
# Starts all required services in proper order with dependency management

set -e

echo "=========================================="
echo "BizOSaaS Platform Startup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if container is running
check_container() {
    local container_name=$1
    if docker ps --format '{{.Names}}' | grep -q "^${container_name}$"; then
        return 0
    else
        return 1
    fi
}

# Function to wait for container health
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
    echo -e " ${YELLOW}⚠ Timeout${NC}"
    return 1
}

# Phase 1: Core Infrastructure
echo -e "${YELLOW}Phase 1: Starting Core Infrastructure${NC}"
echo "--------------------------------------"

# PostgreSQL
if ! check_container "bizosaas-postgres-unified"; then
    echo "Starting PostgreSQL..."
    docker start bizosaas-postgres-unified || echo "PostgreSQL already running"
    sleep 5
else
    echo -e "PostgreSQL: ${GREEN}Already Running${NC}"
fi

# Redis
if ! check_container "bizosaas-redis-unified"; then
    echo "Starting Redis..."
    docker start bizosaas-redis-unified || echo "Redis already running"
    sleep 2
else
    echo -e "Redis: ${GREEN}Already Running${NC}"
fi

# Vault
if ! check_container "bizosaas-vault"; then
    echo "Starting Vault..."
    docker start bizosaas-vault || echo "Vault already running"
    wait_for_health "bizosaas-vault"
else
    echo -e "Vault: ${GREEN}Already Running${NC}"
fi

echo ""

# Phase 2: Backend Services
echo -e "${YELLOW}Phase 2: Starting Backend Services${NC}"
echo "--------------------------------------"

# Central AI Brain Gateway (Port 8001)
if ! check_container "bizosaas-brain-unified"; then
    echo "Starting Central AI Brain Gateway..."
    docker start bizosaas-brain-unified || echo "Brain Gateway already running"
    wait_for_health "bizosaas-brain-unified"
else
    echo -e "Central AI Brain Gateway: ${GREEN}Already Running${NC}"
fi

# Temporal Server
if ! check_container "bizosaas-temporal-server"; then
    echo "Starting Temporal Server..."
    docker start bizosaas-temporal-server || echo "Temporal already running"
    sleep 5
else
    echo -e "Temporal Server: ${GREEN}Already Running${NC}"
fi

# Temporal UI
if ! check_container "bizosaas-temporal-ui-server"; then
    echo "Starting Temporal UI..."
    docker start bizosaas-temporal-ui-server || echo "Temporal UI already running"
    sleep 2
else
    echo -e "Temporal UI: ${GREEN}Already Running${NC}"
fi

# Temporal Integration Service
if ! check_container "bizosaas-temporal-unified"; then
    echo "Starting Temporal Integration..."
    docker start bizosaas-temporal-unified || echo "Temporal Integration already running"
    wait_for_health "bizosaas-temporal-unified"
else
    echo -e "Temporal Integration: ${GREEN}Already Running${NC}"
fi

# Business Directory Backend (Port 8004)
if ! check_container "bizosaas-business-directory-backend-8004"; then
    echo "Starting Business Directory Backend..."
    docker start bizosaas-business-directory-backend-8004 || echo "Business Directory already running"
    wait_for_health "bizosaas-business-directory-backend-8004"
else
    echo -e "Business Directory Backend: ${GREEN}Already Running${NC}"
fi

# Django CRM (Port 8003)
if ! check_container "bizosaas-django-crm-8003"; then
    echo "Starting Django CRM..."
    docker start bizosaas-django-crm-8003 || echo "CRM already running"
    sleep 3
else
    echo -e "Django CRM: ${GREEN}Already Running${NC}"
fi

# Wagtail CMS (Port 8002)
if ! check_container "bizosaas-wagtail-cms-8002"; then
    echo "Starting Wagtail CMS..."
    docker start bizosaas-wagtail-cms-8002 || echo "Wagtail already running"
    sleep 3
else
    echo -e "Wagtail CMS: ${GREEN}Already Running${NC}"
fi

# Saleor E-commerce (Port 8000)
if ! check_container "bizosaas-saleor-unified"; then
    echo "Starting Saleor E-commerce..."
    docker start bizosaas-saleor-unified || echo "Saleor already running"
    sleep 5
else
    echo -e "Saleor E-commerce: ${GREEN}Already Running${NC}"
fi

# AI Agents Service (Port 8010)
if ! check_container "bizosaas-ai-agents-8010"; then
    echo "Starting AI Agents Service..."
    docker start bizosaas-ai-agents-8010 || echo "AI Agents already running"
    sleep 3
else
    echo -e "AI Agents Service: ${GREEN}Already Running${NC}"
fi

# Amazon Sourcing Service (Port 8085)
if ! check_container "amazon-sourcing-8085"; then
    echo "Starting Amazon Sourcing Service..."
    docker start amazon-sourcing-8085 || echo "Amazon Sourcing already running"
    sleep 3
else
    echo -e "Amazon Sourcing Service: ${GREEN}Already Running${NC}"
fi

echo ""

# Phase 3: Frontend Applications
echo -e "${YELLOW}Phase 3: Starting Frontend Applications${NC}"
echo "--------------------------------------"

# Client Portal (Port 3001)
if ! check_container "client-portal-3001"; then
    echo "Starting Client Portal..."
    docker start client-portal-3001 || echo "Client Portal already running"
    sleep 3
else
    echo -e "Client Portal: ${GREEN}Already Running${NC}"
fi

# CorelDove E-commerce Frontend (Port 3002)
if ! check_container "coreldove-frontend-3002"; then
    echo "Starting CorelDove Frontend..."
    docker start coreldove-frontend-3002 || echo "CorelDove already running"
    sleep 3
else
    echo -e "CorelDove Frontend: ${GREEN}Already Running${NC}"
fi

# Bizoholic Frontend (Port 3000)
if check_container "bizoholic-frontend-3000-final"; then
    echo -e "Bizoholic Frontend: ${GREEN}Already Running${NC}"
else
    echo "Bizoholic Frontend not running - needs separate startup"
fi

# Business Directory Frontend (Port 3004)
if ! check_container "business-directory-3004"; then
    echo "Starting Business Directory Frontend..."
    docker start business-directory-3004 || echo "Business Directory Frontend already running"
    sleep 3
else
    echo -e "Business Directory Frontend: ${GREEN}Already Running${NC}"
fi

# Thrillring Gaming (Port 3005)
if ! check_container "thrillring-gaming-3005"; then
    echo "Starting Thrillring Gaming Frontend..."
    docker start thrillring-gaming-3005 || echo "Thrillring Gaming already running"
    sleep 3
else
    echo -e "Thrillring Gaming: ${GREEN}Already Running${NC}"
fi

# BizOSaaS Admin (Port 3009)
if ! check_container "bizosaas-admin-3009"; then
    echo "Starting BizOSaaS Admin..."
    docker start bizosaas-admin-3009 || echo "Admin already running"
    sleep 3
else
    echo -e "BizOSaaS Admin: ${GREEN}Already Running${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}Platform Startup Complete!${NC}"
echo "=========================================="
echo ""
echo "Service Status:"
echo "--------------------------------------"
echo "Core Infrastructure:"
echo "  • PostgreSQL:        localhost:5432"
echo "  • Redis:             localhost:6379"
echo "  • Vault:             localhost:8200"
echo ""
echo "Backend Services (via AI Gateway):"
echo "  • AI Brain Gateway:  localhost:8001 ⭐"
echo "  • Saleor E-commerce: localhost:8000"
echo "  • Wagtail CMS:       localhost:8002"
echo "  • Django CRM:        localhost:8003"
echo "  • Business Dir API:  localhost:8004"
echo "  • Temporal Server:   localhost:7233"
echo "  • Temporal UI:       localhost:8082"
echo "  • Temporal Integration: localhost:8009"
echo "  • AI Agents:         localhost:8010"
echo "  • Amazon Sourcing:   localhost:8085"
echo ""
echo "Frontend Applications:"
echo "  • Bizoholic:         localhost:3000"
echo "  • Client Portal:     localhost:3001"
echo "  • CorelDove Store:   localhost:3002"
echo "  • Business Directory: localhost:3004"
echo "  • Thrillring Gaming: localhost:3005"
echo "  • BizOSaaS Admin:    localhost:3009"
echo ""
echo -e "${YELLOW}⭐ All services route through AI Gateway (8001)${NC}"
echo ""
