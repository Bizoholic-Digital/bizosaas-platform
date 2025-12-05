#!/bin/bash
set -e
export DOCKER_BUILDKIT=0

echo "🔄 Smart Brand Switcher - Bizoholic"
echo "===================================="
echo ""
echo "This script intelligently manages services:"
echo "  ✓ Keeps shared services running"
echo "  ✓ Stops brand-specific services from other brands"
echo "  ✓ Starts only Bizoholic-specific services"
echo ""

# 1. Ensure network exists
docker network create bizosaas-network 2>/dev/null || true

# 2. Start Infrastructure (if not already running)
echo "📦 Ensuring Infrastructure is running..."
docker compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres redis vault

# 3. Start Shared Services (if not already running)
echo "🧠 Ensuring Shared Services are running..."
docker compose -f shared/services/docker-compose.services.yml up -d brain-gateway auth cms crm

# 4. Stop other brand frontends (but keep shared services running)
echo "🛑 Stopping other brand frontends..."
docker compose -f brands/docker-compose.brands.yml stop coreldove-frontend coreldove-backend thrillring-frontend quanttrade-frontend quanttrade-backend 2>/dev/null || true
docker compose -f portals/docker-compose.portals.yml stop client-portal admin-portal business-directory 2>/dev/null || true

# 5. Start Bizoholic Frontend
echo "🌐 Starting Bizoholic Frontend..."
docker compose -f brands/docker-compose.brands.yml up -d bizoholic-frontend

echo ""
echo "✅ Bizoholic Environment Ready!"
echo ""
echo "📊 Running Services:"
echo "   Infrastructure:"
echo "     - Postgres:    localhost:5432"
echo "     - Redis:       localhost:6379"
echo "     - Vault:       localhost:8200"
echo ""
echo "   Shared Services:"
echo "     - Brain API:   localhost:8001"
echo "     - Auth:        localhost:8007"
echo "     - CMS:         localhost:8002"
echo "     - CRM:         localhost:8000"
echo ""
echo "   Bizoholic:"
echo "     - Frontend:    http://localhost:3001"
echo ""
echo "💡 Tip: Switch to another brand with:"
echo "   ./scripts/smart-start-coreldove.sh"
echo "   (Shared services will stay running)"
