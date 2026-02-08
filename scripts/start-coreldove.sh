#!/bin/bash
# Start CoreLDove E-commerce Platform - Updated with build support

set -e

echo "🚀 Starting CoreLDove E-commerce Platform..."
echo ""

cd "$(dirname "$0")/bizosaas"

# Create network if it doesn't exist
echo "🔧 Ensuring Docker network exists..."
docker network inspect bizosaas-platform-network >/dev/null 2>&1 || \
  docker network create bizosaas-platform-network

echo "🛑 Stopping Bizoholic-specific services (if running)..."
docker-compose -f docker-compose.unified.yml stop bizoholic-frontend 2>/dev/null || true

echo ""
echo "📦 Starting/Verifying infrastructure services..."
docker-compose -f docker-compose.unified.yml up -d postgres redis vault

echo "⏳ Waiting for infrastructure to be ready (10 seconds)..."
sleep 10

echo "🧠 Building and starting Brain API and Auth Service..."
docker-compose -f docker-compose.unified.yml up -d --build bizosaas-brain auth-service

echo "⏳ Waiting for core services (15 seconds)..."
sleep 15

echo "🛒 Starting Saleor E-commerce Backend..."
docker-compose -f docker-compose.unified.yml up -d saleor-backend

echo "⏳ Waiting for Saleor to initialize (30 seconds)..."
sleep 30

echo "📝 Building and starting Wagtail CMS..."
docker-compose -f docker-compose.unified.yml up -d --build wagtail-cms

echo "⏳ Waiting for Wagtail (20 seconds)..."
sleep 20

echo "🎨 Building and starting CoreLDove Frontend..."
docker-compose -f docker-compose.unified.yml up -d --build coreldove-frontend

echo ""
echo "✅ CoreLDove Platform Started!"
echo ""
echo "📊 Service Status:"
docker-compose -f docker-compose.unified.yml ps | grep -E "(postgres|redis|vault|brain|auth|saleor|wagtail|coreldove)"

echo ""
echo "🌐 Access Points:"
echo "  - CoreLDove Storefront: http://localhost:3002"
echo "  - Saleor GraphQL API: http://localhost:8000/graphql/"
echo "  - Saleor Dashboard: http://localhost:8000/dashboard/"
echo "  - Brain API Docs: http://localhost:8001/docs"
echo "  - Wagtail CMS Admin: http://localhost:8006/admin"
echo ""
echo "📝 View logs:"
echo "  docker-compose -f bizosaas/docker-compose.unified.yml logs -f coreldove-frontend"
echo ""
echo "🔄 Switch to Bizoholic:"
echo "  ./start-bizoholic.sh"
echo ""
echo "🛑 Stop all services:"
echo "  ./stop-all.sh"
echo ""
