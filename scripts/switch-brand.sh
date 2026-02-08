#!/bin/bash
# Smart Brand Switching Script
# Usage: ./scripts/switch-brand.sh <brand_name>

BRAND=$1
COMPOSE_FILE=".devcontainer/docker-compose.dev.yml"

# Validate input
if [ -z "$BRAND" ]; then
    echo "❌ Usage: $0 <brand_name>"
    echo "   Available brands: bizoholic, coreldove, thrillring, quanttrade"
    exit 1
fi

# Check if valid brand
case $BRAND in
    "bizoholic"|"coreldove"|"thrillring"|"quanttrade")
        ;;
    *)
        echo "❌ Unknown brand: $BRAND"
        echo "   Available: bizoholic, coreldove, thrillring, quanttrade"
        exit 1
        ;;
esac

echo "🔄 Switching to brand: $BRAND"
echo "================================="

# 1. Stop ALL brand-specific services (to free up resources)
echo "🛑 Stopping other brand services..."
docker-compose -f $COMPOSE_FILE stop \
    bizoholic-frontend \
    coreldove-frontend coreldove-backend \
    thrillring-frontend \
    quanttrade-frontend quanttrade-backend

# 2. Start shared services (ensure they are up)
echo "✅ Verifying shared infrastructure..."
docker-compose -f $COMPOSE_FILE up -d postgres redis vault brain-gateway auth

# 3. Start target brand services
echo "🚀 Starting $BRAND services..."
docker-compose -f $COMPOSE_FILE --profile $BRAND up -d

echo ""
echo "✅ Switched to $BRAND successfully!"
echo "📊 Current Status:"
docker-compose -f $COMPOSE_FILE ps | grep "Up"
