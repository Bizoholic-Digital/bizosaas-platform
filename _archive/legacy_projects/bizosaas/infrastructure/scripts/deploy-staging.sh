#!/bin/bash
# BizOSaaS Platform - Staging Deployment Script
set -e

echo "🚀 BizOSaaS Platform - Staging Deployment"
echo "=========================================="

# Check if running from correct directory
if [ ! -f "docker-compose.staging.yml" ]; then
    echo "❌ Error: Please run this script from the bizosaas directory"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📄 Creating .env from staging template..."
    cp .env.staging .env
    echo "⚠️  Please edit .env file with your actual API keys before proceeding"
    echo "   Required: OPENAI_API_KEY"
    read -p "Press Enter to continue or Ctrl+C to exit..."
fi

echo "🔄 Stopping existing containers..."
docker-compose -f docker-compose.staging.yml down --remove-orphans

echo "🗑️  Cleaning up old images (optional)..."
read -p "Remove old Docker images? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker system prune -f
    docker image prune -f
fi

echo "🏗️  Building BizOSaaS services..."
docker-compose -f docker-compose.staging.yml build --no-cache

echo "📦 Starting infrastructure services..."
docker-compose -f docker-compose.staging.yml up -d postgres redis

echo "⏳ Waiting for infrastructure to be ready..."
sleep 15

echo "🌐 Starting application services..."
docker-compose -f docker-compose.staging.yml up -d

echo "⏳ Waiting for all services to start..."
sleep 30

echo "🔍 Checking service health..."
docker-compose -f docker-compose.staging.yml ps

echo "🧪 Running health checks..."
services=("postgres:5432" "redis:6379" "api-gateway:8080" "ai-agents:8001")

for service in "${services[@]}"; do
    IFS=':' read -r name port <<< "$service"
    if nc -z localhost "$port"; then
        echo "✅ $name is responding on port $port"
    else
        echo "❌ $name is NOT responding on port $port"
    fi
done

echo "📋 Service URLs:"
echo "  🌐 API Gateway: http://localhost:8080/health"
echo "  🤖 AI Agents: http://localhost:8001/health"
echo "  📊 Django CRM: http://localhost:8007/health/"
echo "  📝 Wagtail CMS: http://localhost:8010/admin/"
echo "  🗂️  Business Directory: http://localhost:8003/health"
echo "  🖥️  Frontend: http://localhost:3000"
echo "  📈 Monitoring: http://localhost:3001"

echo "📊 View logs:"
echo "  docker-compose -f docker-compose.staging.yml logs -f [service-name]"

echo "🛑 Stop all services:"
echo "  docker-compose -f docker-compose.staging.yml down"

echo ""
echo "✅ BizOSaaS Staging Deployment Complete!"
echo "🎯 Next: Test the services and then deploy to production VPS"