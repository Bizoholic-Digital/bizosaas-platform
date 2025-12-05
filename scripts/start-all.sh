#!/bin/bash
export COMPOSE_DOCKER_CLI_BUILD=0
export DOCKER_BUILDKIT=0

echo "🚀 Starting BizOSaaS Platform..."

# Create network if it doesn't exist
docker network create bizosaas-network 2>/dev/null || true

# Start infrastructure
echo "📦 Starting Infrastructure..."
cd ../shared/infrastructure
docker-compose -f docker-compose.infrastructure.yml up -d

# Wait for infrastructure
echo "⏳ Waiting for infrastructure (30s)..."
sleep 30

# Start shared services
echo "🔧 Starting Shared Services (Brain Gateway + 93 Agents)..."
cd ../services
docker-compose -f docker-compose.services.yml up -d

# Wait for services
echo "⏳ Waiting for services (30s)..."
sleep 30

# Start brands
echo "🎨 Starting Brand Frontends..."
cd ../../brands
docker-compose -f docker-compose.brands.yml up -d

# Start portals
echo "🏢 Starting Portals..."
cd ../portals
docker-compose -f docker-compose.portals.yml up -d

echo ""
echo "✅ BizOSaaS Platform Started!"
echo ""
echo "📊 Access URLs:"
echo "  - Dokploy Dashboard: http://localhost:3000 (Dokploy UI)"
echo "  - Bizoholic: http://localhost:3001"
echo "  - CoreLDove: http://localhost:3002"
echo "  - Client Portal: http://localhost:3003"
echo "  - Business Directory: http://localhost:3004"
echo "  - ThrillRing: http://localhost:3005"
echo "  - Admin Dashboard: http://localhost:3009"
echo ""
echo "🔧 Backend Services:"
echo "  - Brain Gateway (93 Agents): http://localhost:8001"
echo "  - Django CRM: http://localhost:8000"
echo "  - Wagtail CMS: http://localhost:8002"
echo "  - Business Directory API: http://localhost:8003"
echo "  - CoreLDove Backend: http://localhost:8005"
echo "  - Auth Service: http://localhost:8007"
echo "  - AI Agents: http://localhost:8008"
echo "  - Temporal Integration: http://localhost:8009"
echo "  - Saleor E-commerce: http://localhost:8010"
