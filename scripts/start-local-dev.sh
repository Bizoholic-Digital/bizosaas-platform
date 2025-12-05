#!/bin/bash
set -e

echo "🚀 BizOSaaS Platform - Local Development Mode"
echo "=============================================="
echo ""
echo "This script starts all services locally (NO Docker) for development."
echo "You can test everything before building containers."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to start a service in the background
start_service() {
    local name=$1
    local dir=$2
    local command=$3
    
    echo -e "${BLUE}Starting $name...${NC}"
    cd "$dir"
    $command &
    echo $! > "/tmp/bizosaas-$name.pid"
    cd - > /dev/null
}

# 1. Start Infrastructure (Docker - these need to run in containers)
echo -e "${GREEN}Step 1: Starting Infrastructure (Docker)${NC}"
docker compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres redis vault

# 2. Start Shared Packages (if they need building)
echo -e "${GREEN}Step 2: Building Shared Packages${NC}"
if [ -d "shared/packages/frontend" ]; then
    cd shared/packages/frontend
    for pkg in */; do
        if [ -f "$pkg/package.json" ]; then
            echo "Building $pkg..."
            cd "$pkg"
            npm install 2>/dev/null || true
            npm run build 2>/dev/null || true
            cd ..
        fi
    done
    cd ../../..
fi

# 3. Start Backend Services (Local Python/Node processes)
echo -e "${GREEN}Step 3: Starting Backend Services (Local)${NC}"

# Note: These would need to be started manually or with proper virtual envs
# For now, we'll document what needs to run

echo "⚠️  Backend services need to be started manually:"
echo "   - Brain Gateway: cd shared/services/brain-gateway && python -m uvicorn main:app --port 8001"
echo "   - Auth Service: cd shared/services/auth && npm run dev"
echo "   - CMS: cd shared/services/cms && python manage.py runserver 8002"
echo "   - CRM: cd shared/services/crm && python manage.py runserver 8000"
echo ""

# 4. Start Frontend Services (npm run dev)
echo -e "${GREEN}Step 4: Starting Frontend Services (npm run dev)${NC}"

# Client Portal
if [ -d "portals/client-portal" ]; then
    echo "Starting Client Portal on port 3003..."
    cd portals/client-portal
    PORT=3003 npm run dev > /tmp/client-portal.log 2>&1 &
    echo $! > /tmp/bizosaas-client-portal.pid
    cd ../..
fi

# Admin Portal
if [ -d "portals/admin-portal" ]; then
    echo "Starting Admin Portal on port 3009..."
    cd portals/admin-portal
    PORT=3009 npm run dev > /tmp/admin-portal.log 2>&1 &
    echo $! > /tmp/bizosaas-admin-portal.pid
    cd ../..
fi

# Business Directory
if [ -d "portals/business-directory" ]; then
    echo "Starting Business Directory on port 3004..."
    cd portals/business-directory
    PORT=3004 npm run dev > /tmp/business-directory.log 2>&1 &
    echo $! > /tmp/bizosaas-business-directory.pid
    cd ../..
fi

# Bizoholic Frontend
if [ -d "brands/bizoholic/frontend" ]; then
    echo "Starting Bizoholic Frontend on port 3001..."
    cd brands/bizoholic/frontend
    PORT=3001 npm run dev > /tmp/bizoholic.log 2>&1 &
    echo $! > /tmp/bizosaas-bizoholic.pid
    cd ../../..
fi

# CoreLDove Frontend
if [ -d "brands/coreldove/frontend" ]; then
    echo "Starting CoreLDove Frontend on port 3002..."
    cd brands/coreldove/frontend
    PORT=3002 npm run dev > /tmp/coreldove.log 2>&1 &
    echo $! > /tmp/bizosaas-coreldove.pid
    cd ../../..
fi

# ThrillRing Frontend
if [ -d "brands/thrillring/frontend" ]; then
    echo "Starting ThrillRing Frontend on port 3005..."
    cd brands/thrillring/frontend
    PORT=3005 npm run dev > /tmp/thrillring.log 2>&1 &
    echo $! > /tmp/bizosaas-thrillring.pid
    cd ../../..
fi

# QuantTrade Frontend
if [ -d "brands/quanttrade/frontend" ]; then
    echo "Starting QuantTrade Frontend on port 3006..."
    cd brands/quanttrade/frontend
    PORT=3006 npm run dev > /tmp/quanttrade.log 2>&1 &
    echo $! > /tmp/bizosaas-quanttrade.pid
    cd ../../..
fi

echo ""
echo -e "${GREEN}✅ Local Development Environment Started!${NC}"
echo ""
echo "📊 Access Points:"
echo "   Client Portal:        http://localhost:3003"
echo "   Admin Portal:         http://localhost:3009"
echo "   Business Directory:   http://localhost:3004"
echo "   Bizoholic:            http://localhost:3001"
echo "   CoreLDove:            http://localhost:3002"
echo "   ThrillRing:           http://localhost:3005"
echo "   QuantTrade:           http://localhost:3006"
echo ""
echo "📝 Logs are in /tmp/*.log"
echo "🛑 To stop: ./scripts/stop-local-dev.sh"
