#!/bin/bash
# Brain Gateway Deployment Script
# Run this on the server: bash deploy_brain_gateway.sh
# Ensure you have your environment variables set or passed to this script.

set -e

echo "🚀 Deploying Brain Gateway..."

# Clone latest code
cd /tmp
rm -rf bizosaas-platform
git clone -b staging https://github.com/Bizoholic-Digital/bizosaas-platform.git
cd bizosaas-platform

# Export environment variables (Set these on your server environment)
export DATABASE_URL="${DATABASE_URL}"
export REDIS_URL="${REDIS_URL}"
export JWT_SECRET="${JWT_SECRET}"
export TEMPORAL_HOST="${TEMPORAL_HOST}"
export OPENAI_API_KEY="${OPENAI_API_KEY}"
export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}"
export GOOGLE_API_KEY="${GOOGLE_API_KEY}"
export OPENROUTER_API_KEY="${OPENROUTER_API_KEY}"
export GITHUB_TOKEN="${GITHUB_TOKEN}"

echo "✅ Environment variables set"

# Deploy Brain Gateway
echo "📦 Deploying Brain Gateway container..."
docker compose -f docker-compose.core.yml up -d brain-gateway

echo "⏳ Waiting for container to start..."
sleep 5

# Check status
echo "🔍 Checking container status..."
docker ps | grep brain-gateway

echo "📋 Checking logs..."
docker logs brain-gateway --tail 20

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🧪 Testing health endpoint..."
sleep 3
curl -I https://api.bizoholic.net/health

echo ""
echo "📊 To view logs: docker logs brain-gateway -f"
echo "🔍 To check status: docker ps | grep brain-gateway"
