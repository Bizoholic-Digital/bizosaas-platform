#!/bin/bash

# Start Complete Saleor E-commerce Platform
# Quick deployment script for CoreLDove storefront integration

set -e

echo "🚀 Starting Complete Saleor E-commerce Platform"
echo "============================================"

# Kill any existing simplified API processes
echo "💭 Stopping simplified API processes..."
pkill -f "saleor-api-complete.py" 2>/dev/null || true
pkill -f "saleor-proxy.py" 2>/dev/null || true
echo "✓ Existing processes stopped"

# Start Docker Compose services
echo "💭 Starting Saleor services..."
docker-compose -f docker-compose.saleor-complete.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to initialize..."
sleep 30

# Check service health
echo "🏅 Checking service health..."
docker-compose -f docker-compose.saleor-complete.yml ps

# Test API connectivity
echo "🗾 Testing API connectivity..."
for i in {1..10}; do
    if curl -s -f http://localhost:8024/graphql/ > /dev/null 2>&1; then
        echo "✓ Saleor API is accessible at http://localhost:8024/graphql/"
        break
    fi
    echo "Attempt $i/10: Waiting for API to be ready..."
    sleep 5
done

# Display access information
echo
echo "✅ Saleor Platform Ready!"
echo "========================="
echo "🌍 API Endpoint: http://localhost:8024/graphql/"
echo "📋 Admin Dashboard: http://localhost:9020/"
echo "🔍 GraphQL Playground: http://localhost:8024/graphql/"
echo "📢 Database: localhost:5433/saleor_coreldove"
echo "📊 Redis: localhost:6380"
echo
echo "📅 Next Steps:"
echo "1. Update CoreLDove storefront API endpoint to: http://localhost:8024/graphql/"
echo "2. Test the complete GraphQL schema with: python3 validate-saleor-schema.py"
echo "3. Configure admin settings at: http://localhost:9020/"
echo
echo "🔧 Management Commands:"
echo "  - View logs: docker-compose -f docker-compose.saleor-complete.yml logs -f"
echo "  - Stop services: docker-compose -f docker-compose.saleor-complete.yml down"
echo "  - Restart: docker-compose -f docker-compose.saleor-complete.yml restart"

echo "✓ Saleor deployment complete!"