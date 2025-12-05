#!/bin/bash

# BizOSaaS Platform - Migration Script
# Fixes port allocation and integrates with existing services

set -e

echo "🔄 BizOSaaS Platform - Port Migration & Integration"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "📋 Current running containers:"
docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}" | head -15

echo ""
echo "🔄 MIGRATION PLAN:"
echo "=================="
echo "❌ STOP: tailadmin-v2-unified (currently on wrong port 3001)"
echo "❌ STOP: bizosaas-bizoholic-frontend (currently on wrong port 3000)" 
echo "✅ KEEP: bizosaas-coreldove-frontend (correct port 3002)"
echo "✅ KEEP: All infrastructure services (postgres, redis, vault, traefik)"
echo "✅ KEEP: wagtail-cms (port 8006)"
echo "🆕 ADD: bizosaas-brain (port 8001)"
echo "🆕 ADD: bizosaas-auth-v2 (port 8007)"
echo "🆕 ADD: apache-superset (port 8088)"
echo "🔧 FIX: Correct port allocation:"
echo "    - Port 3000: TailAdmin v2 (BizOSaaS Admin)"
echo "    - Port 3001: Bizoholic Marketing"  
echo "    - Port 3002: CoreLDove E-commerce (unchanged)"

read -p "🤔 Do you want to proceed with the migration? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Migration cancelled."
    exit 0
fi

echo ""
echo "🛑 Step 1: Stopping incorrectly configured containers..."

# Stop containers with wrong port allocation
echo "⏹️ Stopping tailadmin-v2-unified (wrong port)..."
docker stop tailadmin-v2-unified 2>/dev/null || echo "Already stopped"

echo "⏹️ Stopping bizosaas-bizoholic-frontend (wrong port)..."
docker stop bizosaas-bizoholic-frontend 2>/dev/null || echo "Already stopped"

# Remove the incorrectly configured containers
echo "🗑️ Removing incorrectly configured containers..."
docker rm tailadmin-v2-unified 2>/dev/null || echo "Already removed"
docker rm bizosaas-bizoholic-frontend 2>/dev/null || echo "Already removed"

echo ""
echo "🔧 Step 2: Load environment variables..."

# Load environment variables
if [ -f .env ]; then
    echo "📋 Loading environment variables from .env"
    export $(cat .env | grep -v '#' | xargs)
else
    echo "⚠️ No .env file found. Using default values."
    cp .env.unified.example .env
    echo "📋 Created .env from template. Please edit with your API keys."
fi

# Set default environment variables
export OPENAI_API_KEY=${OPENAI_API_KEY:-dummy-key}
export JWT_SECRET=${JWT_SECRET:-dev-jwt-secret-key-change-in-production}
export STRIPE_PUBLISHABLE_KEY=${STRIPE_PUBLISHABLE_KEY:-pk_test_dummy}

echo ""
echo "🚀 Step 3: Starting integrated stack with correct port allocation..."

# Start missing backend services first
echo "🧠 Starting FastAPI Brain Gateway (port 8001)..."
docker-compose -f docker-compose.integration.yml up -d bizosaas-brain

echo "🔐 Starting Auth Service v2 (port 8007)..."
docker-compose -f docker-compose.integration.yml up -d bizosaas-auth-v2

echo "🛍️ Starting Saleor Backend (port 8010)..."
docker-compose -f docker-compose.integration.yml up -d saleor-backend

echo "📊 Starting Apache Superset (port 8088)..."
docker-compose -f docker-compose.integration.yml up -d apache-superset

echo ""
echo "⏳ Waiting for backend services to be ready..."
sleep 15

echo ""
echo "🎨 Step 4: Starting frontend services with correct ports..."

echo "🔧 Starting BizOSaaS Admin Dashboard (port 3000)..."
docker-compose -f docker-compose.integration.yml up -d bizosaas-admin

echo "📈 Starting Bizoholic Marketing (port 3001)..."
docker-compose -f docker-compose.integration.yml up -d bizoholic-marketing

echo "🛒 Starting CoreLDove E-commerce (port 3002)..."
docker-compose -f docker-compose.integration.yml up -d coreldove-ecommerce

echo ""
echo "⏳ Waiting for frontend services to be ready..."
sleep 10

echo ""
echo "✅ MIGRATION COMPLETED SUCCESSFULLY!"
echo "===================================="
echo ""
echo "🌐 Correct Frontend Applications:"
echo "   🔧 BizOSaaS Admin Dashboard (TailAdmin v2): http://localhost:3000"
echo "   📈 Bizoholic Marketing: http://localhost:3001" 
echo "   🛒 CoreLDove E-commerce: http://localhost:3002"
echo ""
echo "🔧 Backend Services:"
echo "   🧠 FastAPI Brain Gateway: http://localhost:8001"
echo "   🔐 Auth Service v2: http://localhost:8007"
echo "   📝 Wagtail CMS: http://localhost:8006 (existing)"
echo "   🛍️ Saleor Backend: http://localhost:8010"
echo "   📊 Apache Superset: http://localhost:8088"
echo "   🗄️ SQL Admin: http://localhost:5000 (if available)"
echo ""
echo "💡 Authentication Flow:"
echo "   1. Visit http://localhost:3000 → Login page"
echo "   2. Authenticate → TailAdmin v2 dashboard with analytics"
echo "   3. Navigate between platforms using platform tabs"
echo ""
echo "🐳 Current Container Status:"
docker-compose -f docker-compose.integration.yml ps

echo ""
echo "📋 All running containers:"
docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"

echo ""
echo "🎉 Platform is ready with correct port allocation!"
echo "💡 To stop: docker-compose -f docker-compose.integration.yml down"