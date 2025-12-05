#!/bin/bash
set -e
export DOCKER_BUILDKIT=0

echo "🔄 Smart Brand Switcher - QuantTrade"
echo "===================================="
echo ""
echo "This script intelligently manages services:"
echo "  ✓ Keeps shared services running"
echo "  ✓ Stops brand-specific services from other brands"
echo "  ✓ Starts only QuantTrade-specific services"
echo ""

# 1. Ensure network exists
docker network create bizosaas-network 2>/dev/null || true

# 2. Start Infrastructure (if not already running)
echo "📦 Ensuring Infrastructure is running..."
docker compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres redis

# 3. Stop other brand frontends (but keep shared services running)
echo "🛑 Stopping other brand frontends..."
docker compose -f brands/docker-compose.brands.yml stop bizoholic-frontend coreldove-frontend coreldove-backend thrillring-frontend 2>/dev/null || true
docker compose -f portals/docker-compose.portals.yml stop client-portal admin-portal business-directory 2>/dev/null || true

# 4. Start QuantTrade Services
echo "📈 Starting QuantTrade Frontend & Backend..."
docker compose -f brands/docker-compose.brands.yml up -d quanttrade-frontend quanttrade-backend

echo ""
echo "✅ QuantTrade Environment Ready!"
echo ""
echo "📊 Running Services:"
echo "   Infrastructure:"
echo "     - Postgres:    localhost:5432"
echo "     - Redis:       localhost:6379"
echo ""
echo "   QuantTrade:"
echo "     - Frontend:    http://localhost:3006"
echo "     - Backend:     localhost:8006"
echo ""
echo "💡 Tip: Switch to another brand with:"
echo "   ./scripts/smart-start-bizoholic.sh"
echo "   (Shared services will stay running)"
