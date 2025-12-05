#!/bin/bash
set -e
export DOCKER_BUILDKIT=0

echo "🔄 Smart Brand Switcher - ThrillRing"
echo "===================================="
echo ""
echo "This script intelligently manages services:"
echo "  ✓ Keeps shared services running"
echo "  ✓ Stops brand-specific services from other brands"
echo "  ✓ Starts only ThrillRing-specific services"
echo ""

# 1. Ensure network exists
docker network create bizosaas-network 2>/dev/null || true

# 2. Start Infrastructure (if not already running)
echo "📦 Ensuring Infrastructure is running..."
docker compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres redis

# 3. Start Shared Services needed by ThrillRing
echo "🧠 Ensuring Brain Gateway is running..."
docker compose -f shared/services/docker-compose.services.yml up -d brain-gateway

# 4. Stop other brand frontends (but keep shared services running)
echo "🛑 Stopping other brand frontends..."
docker compose -f brands/docker-compose.brands.yml stop bizoholic-frontend coreldove-frontend coreldove-backend quanttrade-frontend quanttrade-backend 2>/dev/null || true
docker compose -f portals/docker-compose.portals.yml stop client-portal admin-portal business-directory 2>/dev/null || true

# 5. Start ThrillRing Frontend
echo "🎮 Starting ThrillRing Frontend..."
docker compose -f brands/docker-compose.brands.yml up -d thrillring-frontend

echo ""
echo "✅ ThrillRing Environment Ready!"
echo ""
echo "📊 Running Services:"
echo "   Infrastructure:"
echo "     - Postgres:    localhost:5432"
echo "     - Redis:       localhost:6379"
echo ""
echo "   Shared Services:"
echo "     - Brain API:   localhost:8001"
echo ""
echo "   ThrillRing:"
echo "     - Frontend:    http://localhost:3005"
echo ""
echo "💡 Tip: Switch to another brand with:"
echo "   ./scripts/smart-start-bizoholic.sh"
echo "   (Shared services will stay running)"
