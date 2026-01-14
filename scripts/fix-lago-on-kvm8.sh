#!/bin/bash
# This script will be executed ON the KVM8 server to fix Lago

echo "🔧 Fixing Lago on KVM8 Server..."

# Navigate to the project directory
cd /home/alagiri/projects/bizosaas-platform

# Check if the RSA key is still in the compose file
if grep -q "LAGO_RSA_PRIVATE_KEY" docker-compose.lago.yml; then
    echo "⚠️  RSA key still present in compose file, removing it..."
    sed -i.backup '/LAGO_RSA_PRIVATE_KEY/d' docker-compose.lago.yml
    echo "✅ Removed RSA key from compose file"
else
    echo "✅ RSA key already removed from compose file"
fi

# Stop all Lago containers
echo "🛑 Stopping Lago containers..."
docker-compose -f docker-compose.lago.yml down

# Start fresh
echo "🚀 Starting Lago with updated configuration..."
docker-compose -f docker-compose.lago.yml up -d

# Wait for services to initialize
echo "⏳ Waiting for services to start..."
sleep 20

# Check status
echo "📊 Current status:"
docker ps --filter name=lago

echo ""
echo "🔍 Checking lago-api logs:"
docker logs lago-api --tail 20

echo ""
echo "🔍 Checking lago-worker logs:"
docker logs lago-worker --tail 20
