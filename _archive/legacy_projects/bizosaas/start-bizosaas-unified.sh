#!/bin/bash

# BizOSaaS Platform - Unified Stack Startup Script
# Starts all services with correct port allocation and TailAdmin v2 integration

set -e

echo "🚀 Starting BizOSaaS Platform - Unified Stack"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose > /dev/null 2>&1; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

# Create network if it doesn't exist
echo "📡 Creating BizOSaaS network..."
docker network create bizosaas-network 2>/dev/null || echo "Network already exists"

# Load environment variables
if [ -f .env ]; then
    echo "📋 Loading environment variables from .env"
    export $(cat .env | grep -v '#' | xargs)
else
    echo "⚠️ No .env file found. Using default values."
    echo "💡 Create .env file with required API keys for full functionality"
fi

# Set default environment variables if not provided
export OPENAI_API_KEY=${OPENAI_API_KEY:-dummy-key}
export JWT_SECRET=${JWT_SECRET:-dev-jwt-secret-key-change-in-production}
export STRIPE_PUBLISHABLE_KEY=${STRIPE_PUBLISHABLE_KEY:-pk_test_dummy}
export ADMIN_SECRET=${ADMIN_SECRET:-super-admin-secret-change-in-production}

echo "🏗️ Building and starting services..."
echo ""
echo "Port Allocation:"
echo "=================="
echo "🔧 Port 3000: BizOSaaS Admin Dashboard (TailAdmin v2 + Apache Superset)"
echo "📈 Port 3001: Bizoholic Marketing Frontend (Wagtail CMS)"
echo "🛒 Port 3002: CoreLDove E-commerce Frontend (Saleor)"
echo "🧠 Port 8001: FastAPI Brain Gateway"
echo "🔐 Port 8007: Auth Service v2"
echo "📝 Port 8082: Wagtail CMS"
echo "🛍️ Port 8010: Saleor Backend"
echo "📊 Port 8088: Apache Superset Analytics"
echo "🗄️ Port 5000: SQL Admin Dashboard (SuperAdmin only)"
echo "🐘 Port 5432: PostgreSQL Database"
echo "🔴 Port 6379: Redis Cache"
echo ""

# Start infrastructure services first
echo "🏗️ Starting infrastructure services..."
docker-compose -f docker-compose.unified.yml up -d postgres redis

# Wait for infrastructure to be ready
echo "⏳ Waiting for infrastructure services to be ready..."
sleep 10

# Start backend services
echo "🔧 Starting backend services..."
docker-compose -f docker-compose.unified.yml up -d bizosaas-brain auth-service-v2 wagtail-cms saleor-backend apache-superset sqladmin-dashboard

# Wait for backend services to be ready
echo "⏳ Waiting for backend services to be ready..."
sleep 15

# Start frontend services
echo "🎨 Starting frontend services..."
docker-compose -f docker-compose.unified.yml up -d bizosaas-admin bizoholic-marketing coreldove-ecommerce

# Start reverse proxy
echo "🔀 Starting reverse proxy..."
docker-compose -f docker-compose.unified.yml up -d traefik

# Show status
echo ""
echo "✅ BizOSaaS Platform Started Successfully!"
echo "==========================================="
echo ""
echo "🌐 Frontend Applications:"
echo "   🔧 BizOSaaS Admin Dashboard: http://localhost:3000"
echo "   📈 Bizoholic Marketing: http://localhost:3001" 
echo "   🛒 CoreLDove E-commerce: http://localhost:3002"
echo ""
echo "🔧 Backend Services:"
echo "   🧠 FastAPI Brain Gateway: http://localhost:8001"
echo "   🔐 Auth Service v2: http://localhost:8007"
echo "   📝 Wagtail CMS: http://localhost:8082"
echo "   🛍️ Saleor Backend: http://localhost:8010"
echo "   📊 Apache Superset: http://localhost:8088"
echo "   🗄️ SQL Admin (SuperAdmin): http://localhost:5000"
echo ""
echo "🔀 Reverse Proxy:"
echo "   📊 Traefik Dashboard: http://localhost:8080"
echo ""
echo "💡 Login Flow:"
echo "   1. Visit http://localhost:3000 for BizOSaaS Admin login"
echo "   2. After login → TailAdmin v2 dashboard with Apache Superset analytics"
echo "   3. Navigate between platforms using the platform tabs"
echo ""
echo "🐳 Container Status:"
docker-compose -f docker-compose.unified.yml ps
echo ""
echo "📋 To view logs: docker-compose -f docker-compose.unified.yml logs -f [service-name]"
echo "🛑 To stop: ./stop-bizosaas-unified.sh"
echo ""
echo "🎉 Platform is ready for development and testing!"