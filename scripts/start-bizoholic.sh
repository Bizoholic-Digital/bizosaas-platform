#!/bin/bash
# Start Bizoholic Marketing Platform - Updated with build support

set -e

echo "🚀 Starting Bizoholic Marketing Platform..."
echo ""

cd "$(dirname "$0")/bizosaas"

# Create network if it doesn't exist
echo "🔧 Ensuring Docker network exists..."
docker network inspect bizosaas-platform-network >/dev/null 2>&1 || \
  docker network create bizosaas-platform-network

echo "🛑 Stopping CoreLDove-specific services (if running)..."
docker-compose -f docker-compose.unified.yml stop coreldove-frontend saleor-backend 2>/dev/null || true

echo ""
echo "📦 Starting/Verifying infrastructure services..."
DOCKER_BUILDKIT=0 docker-compose -f docker-compose.unified.yml up -d postgres redis vault

echo "⏳ Waiting for infrastructure to be ready (10 seconds)..."
sleep 10

echo "🧠 Starting Brain API and Auth Service..."
DOCKER_BUILDKIT=0 docker-compose -f docker-compose.unified.yml up -d bizosaas-brain auth-service

echo "⏳ Waiting for core services (15 seconds)..."
sleep 15

# Skip Wagtail for now - not needed for auth testing
# echo "📝 Starting Wagtail CMS..."
# DOCKER_BUILDKIT=0 docker-compose -f docker-compose.unified.yml up -d wagtail-cms
# echo "⏳ Waiting for Wagtail (20 seconds)..."
# sleep 20

echo "🎨 Starting Bizoholic Frontend..."
DOCKER_BUILDKIT=0 docker-compose -f docker-compose.unified.yml up -d bizoholic-frontend

echo ""
echo "✅ Bizoholic Platform Started!"
echo ""
echo "📊 Service Status:"
docker-compose -f docker-compose.unified.yml ps | grep -E "(postgres|redis|vault|brain|auth|wagtail|bizoholic)"

echo ""
echo "🌐 Access Points:"
echo "  - Bizoholic Frontend: http://localhost:3001"
echo "  - Brain API Docs: http://localhost:8001/docs"
echo "  - Wagtail CMS Admin: http://localhost:8006/admin"
echo "  - Auth Service Docs: http://localhost:8007/docs"
echo ""
echo "📝 View logs:"
echo "  docker-compose -f bizosaas/docker-compose.unified.yml logs -f bizoholic-frontend"
echo ""
echo "🔄 Switch to CoreLDove:"
echo "  ./start-coreldove.sh"
echo ""
echo "🛑 Stop all services:"
echo "  ./stop-all.sh"
echo ""
