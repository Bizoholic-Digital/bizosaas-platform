#!/bin/bash

# CoreLDove E-commerce Website Startup Script
# This script starts the complete CoreLDove e-commerce platform

set -e

echo "🚀 Starting CoreLDove E-commerce Platform..."
echo "==============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a service is running
check_service() {
    local url=$1
    local name=$2
    echo -n "Checking $name... "
    if curl -s --connect-timeout 5 "$url" >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Running${NC}"
        return 0
    else
        echo -e "${RED}✗ Not running${NC}"
        return 1
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local name=$2
    local max_attempts=30
    local attempt=1

    echo -n "Waiting for $name to be ready..."
    while [ $attempt -le $max_attempts ]; do
        if curl -s --connect-timeout 2 "$url" >/dev/null 2>&1; then
            echo -e " ${GREEN}✓ Ready${NC}"
            return 0
        fi
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    echo -e " ${RED}✗ Timeout${NC}"
    return 1
}

echo -e "\n${BLUE}Step 1: Checking Prerequisites${NC}"
echo "-----------------------------------"

# Check if Node.js is installed
if command -v node >/dev/null 2>&1; then
    NODE_VERSION=$(node --version)
    echo -e "Node.js: ${GREEN}$NODE_VERSION${NC}"
else
    echo -e "${RED}Error: Node.js is not installed${NC}"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if command -v npm >/dev/null 2>&1; then
    NPM_VERSION=$(npm --version)
    echo -e "npm: ${GREEN}$NPM_VERSION${NC}"
else
    echo -e "${RED}Error: npm is not installed${NC}"
    exit 1
fi

echo -e "\n${BLUE}Step 2: Checking Backend Services${NC}"
echo "------------------------------------"

# Check Saleor GraphQL API
SALEOR_RUNNING=false
if check_service "http://localhost:8020/graphql/" "Saleor GraphQL API"; then
    SALEOR_RUNNING=true
fi

# Check Saleor Dashboard
DASHBOARD_RUNNING=false
if check_service "http://localhost:9020" "Saleor Dashboard"; then
    DASHBOARD_RUNNING=true
fi

# Check AI Agents Service
AI_RUNNING=false
if check_service "http://localhost:8000/health" "AI Agents Service"; then
    AI_RUNNING=true
fi

# Check Redis (for caching)
REDIS_RUNNING=false
if check_service "http://localhost:6379" "Redis Cache" || nc -z localhost 6379 2>/dev/null; then
    REDIS_RUNNING=true
    echo -e "Redis Cache: ${GREEN}✓ Running${NC}"
else
    echo -e "Redis Cache: ${YELLOW}⚠ Not running (optional)${NC}"
fi

# Check PostgreSQL (for Saleor)
POSTGRES_RUNNING=false
if nc -z localhost 5432 2>/dev/null; then
    POSTGRES_RUNNING=true
    echo -e "PostgreSQL: ${GREEN}✓ Running${NC}"
else
    echo -e "PostgreSQL: ${YELLOW}⚠ Not detected${NC}"
fi

echo -e "\n${BLUE}Step 3: Environment Configuration${NC}"
echo "------------------------------------"

# Check if .env.local exists
if [ -f ".env.local" ]; then
    echo -e "Environment file: ${GREEN}✓ Found${NC}"
else
    echo -e "Environment file: ${YELLOW}⚠ Creating from template${NC}"
    if [ -f ".env.local.example" ]; then
        cp .env.local.example .env.local
        echo -e "${YELLOW}Please edit .env.local with your configuration${NC}"
    else
        echo -e "${RED}Error: No environment template found${NC}"
        exit 1
    fi
fi

echo -e "\n${BLUE}Step 4: Installing Dependencies${NC}"
echo "-------------------------------------"

# Check if node_modules exists
if [ ! -d "node_modules" ] || [ ! -f "package-lock.json" ]; then
    echo "Installing npm dependencies..."
    npm install
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Dependencies installed${NC}"
    else
        echo -e "${RED}✗ Failed to install dependencies${NC}"
        exit 1
    fi
else
    echo -e "Dependencies: ${GREEN}✓ Already installed${NC}"
fi

echo -e "\n${BLUE}Step 5: Building Application${NC}"
echo "--------------------------------"

# Build the Next.js application
echo "Building CoreLDove frontend..."
npm run build
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Build successful${NC}"
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi

echo -e "\n${BLUE}Step 6: Service Status Summary${NC}"
echo "-------------------------------------"

echo -e "Required Services:"
echo -e "  Saleor GraphQL API: $([ $SALEOR_RUNNING = true ] && echo "${GREEN}✓ Running${NC}" || echo "${RED}✗ Not running${NC}")"
echo -e "  Saleor Dashboard:   $([ $DASHBOARD_RUNNING = true ] && echo "${GREEN}✓ Running${NC}" || echo "${RED}✗ Not running${NC}")"

echo -e "\nOptional Services:"
echo -e "  AI Agents Service:  $([ $AI_RUNNING = true ] && echo "${GREEN}✓ Running${NC}" || echo "${YELLOW}⚠ Not running${NC}")"
echo -e "  Redis Cache:        $([ $REDIS_RUNNING = true ] && echo "${GREEN}✓ Running${NC}" || echo "${YELLOW}⚠ Not running${NC}")"
echo -e "  PostgreSQL:         $([ $POSTGRES_RUNNING = true ] && echo "${GREEN}✓ Running${NC}" || echo "${YELLOW}⚠ Not detected${NC}")"

# Show warnings for missing services
if [ $SALEOR_RUNNING = false ]; then
    echo -e "\n${YELLOW}Warning: Saleor GraphQL API is not running${NC}"
    echo "The website will use fallback data. To start Saleor:"
    echo "  cd /path/to/saleor && docker-compose up -d"
fi

if [ $AI_RUNNING = false ]; then
    echo -e "\n${YELLOW}Warning: AI Agents Service is not running${NC}"
    echo "AI recommendations will use fallback data. To start AI agents:"
    echo "  cd /path/to/ai-agents && python main.py"
fi

echo -e "\n${BLUE}Step 7: Starting CoreLDove Frontend${NC}"
echo "-------------------------------------"

echo -e "Starting development server on ${BLUE}http://localhost:3002${NC}"
echo -e "Access points:"
echo -e "  🏠 Main Website:     ${BLUE}http://localhost:3002${NC}"
echo -e "  📊 AI Dashboard:     ${BLUE}http://localhost:3002/dashboard${NC}"
echo -e "  🛍️  Product Catalog:  ${BLUE}http://localhost:3002/catalog${NC}"

if [ $DASHBOARD_RUNNING = true ]; then
    echo -e "  ⚙️  Saleor Dashboard: ${BLUE}http://localhost:9020${NC}"
fi

echo -e "\n${GREEN}🎉 CoreLDove E-commerce Platform is ready!${NC}"
echo "==============================================="

# Start the development server
echo -e "\nStarting Next.js development server..."
exec npm run dev