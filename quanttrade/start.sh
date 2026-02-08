#!/bin/bash
# QuantTrade Quick Start Script (Simplified)
# Deploys QuantTrade using existing BizOSaaS infrastructure

set -e

echo "🚀 QuantTrade Quick Start"
echo "=========================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if running from correct directory
if [ ! -f "docker-compose.yml" ]; then
    echo "Error: Please run this script from the quanttrade directory"
    exit 1
fi

echo -e "${BLUE}Step 1: Initialize Vault Secrets${NC}"
echo "=================================="
if [ -f "scripts/init-vault.sh" ]; then
    bash scripts/init-vault.sh
else
    echo -e "${YELLOW}Warning: init-vault.sh not found, skipping...${NC}"
fi

echo ""
echo -e "${BLUE}Step 2: Create BizOSaaS Network (if not exists)${NC}"
echo "================================================"
docker network create bizosaas-network 2>/dev/null && echo -e "${GREEN}✓ Network created${NC}" || echo -e "${YELLOW}Network already exists${NC}"

echo ""
echo -e "${BLUE}Step 3: Build QuantTrade Services${NC}"
echo "=================================="
echo "Building backend..."
docker build -t quanttrade-backend:latest ./backend

echo ""
echo "Building frontend..."
docker build -f ./frontend/Dockerfile.prod -t quanttrade-frontend:latest ./frontend

echo ""
echo -e "${BLUE}Step 4: Start QuantTrade Services${NC}"
echo "=================================="
docker compose up -d

echo ""
echo -e "${BLUE}Step 5: Wait for Services to be Ready${NC}"
echo "======================================"
echo "Waiting for backend to start..."
sleep 15

# Check backend health
echo "Checking backend health..."
for i in {1..20}; do
    if curl -s http://localhost:8012/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend is healthy${NC}"
        BACKEND_HEALTHY=true
        break
    fi
    echo -n "."
    sleep 3
done

if [ -z "$BACKEND_HEALTHY" ]; then
    echo -e "${YELLOW}⚠ Backend health check timeout (this is normal on first run)${NC}"
    echo "Check logs with: docker-compose logs quanttrade-backend"
fi

echo ""
echo ""
echo -e "${GREEN}✅ QuantTrade Deployment Complete!${NC}"
echo "===================================="
echo ""
echo "📊 Access Points:"
echo "  • Frontend:    http://localhost:3010"
echo "  • Backend API: http://localhost:8012"
echo "  • API Docs:    http://localhost:8012/docs"
echo "  • Temporal UI: http://localhost:8082"
echo "  • Vault:       http://localhost:8200"
echo ""
echo "🔐 Using Existing Infrastructure:"
echo "  • Vault:       bizosaas-vault-unified"
echo "  • PostgreSQL:  bizosaas-postgres-unified"
echo "  • Redis:       bizosaas-redis-unified"
echo "  • Temporal:    bizosaas-temporal"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Check logs:"
echo "   docker compose logs -f quanttrade-backend"
echo ""
echo "2. Update Vault secrets with real API keys:"
echo "   docker exec bizosaas-vault-unified sh -c 'VAULT_TOKEN=root vault kv patch secret/quanttrade/exchanges/deribit api_key=\"YOUR_KEY\"'"
echo ""
echo "3. Initialize AI agents (after backend is healthy):"
echo "   docker exec -it quanttrade-backend python -c \"from app.agents.trading_agents import initialize_agents; import asyncio; asyncio.run(initialize_agents())\""
echo ""
echo "4. View all services:"
echo "   docker compose ps"
echo ""
echo -e "${GREEN}Happy Trading! 📈${NC}"
