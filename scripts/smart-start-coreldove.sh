#!/bin/bash
set -e
export DOCKER_BUILDKIT=0

echo "🔄 Smart Brand Switcher - CoreLDove"
echo "===================================="
echo ""
echo "This script intelligently manages services:"
echo "  ✓ Keeps shared services running"
echo "  ✓ Stops brand-specific services from other brands"
echo "  ✓ Starts only CoreLDove-specific services"
echo ""

# 1. Ensure network exists
docker network create bizosaas-network 2>/dev/null || true

# 2. Start Infrastructure (if not already running)
echo "📦 Ensuring Infrastructure is running..."
docker compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres redis

# 3. Start Shared Services needed by CoreLDove
echo "🛒 Ensuring Saleor is running..."
docker compose -f shared/services/docker-compose.services.yml up -d saleor

# 4. Stop other brand frontends (but keep shared services running)
echo "🛑 Stopping other brand frontends..."
docker compose -f brands/docker-compose.brands.yml stop bizoholic-frontend thrillring-frontend quanttrade-frontend quanttrade-backend 2>/dev/null || true
docker compose -f portals/docker-compose.portals.yml stop client-portal admin-portal business-directory 2>/dev/null || true

# 5. Start CoreLDove Services
echo "🌐 Starting CoreLDove Frontend & Backend..."
docker compose -f brands/docker-compose.brands.yml up -d coreldove-frontend coreldove-backend

echo ""
echo "✅ CoreLDove Environment Ready!"
echo ""
echo "📊 Running Services:"
echo "   Infrastructure:"
echo "     - Postgres:    localhost:5432"
echo "     - Redis:       localhost:6379"
echo ""
echo "   Shared Services:"
echo "     - Saleor:      localhost:8010"
echo ""
echo "   CoreLDove:"
echo "     - Frontend:    http://localhost:3002"
echo "     - Backend:     localhost:8005"
echo ""
echo "💡 Tip: Switch to another brand with:"
echo "   ./scripts/smart-start-bizoholic.sh"
echo "   (Shared services will stay running)"
