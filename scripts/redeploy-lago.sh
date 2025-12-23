#!/bin/bash
# Fix Lago Deployment - Use docker compose (v2) instead of docker-compose

echo "🔧 Redeploying Lago with health checks..."

# Navigate to project directory
cd /home/alagiri/projects/bizosaas-platform

# Stop current Lago containers
echo "Stopping current Lago containers..."
ssh root@72.60.98.213 "docker stop lago-api lago-worker lago-front lago-migrate 2>/dev/null || true"

# Remove old containers
echo "Removing old containers..."
ssh root@72.60.98.213 "docker rm lago-api lago-worker lago-front lago-migrate 2>/dev/null || true"

# Copy updated compose file
echo "Copying updated docker-compose.lago.yml..."
scp docker-compose.lago.yml root@72.60.98.213:/root/lago-compose.yml

# Deploy with docker compose (v2)
echo "Deploying Lago stack..."
ssh root@72.60.98.213 "cd /root && docker compose -f lago-compose.yml up -d"

# Wait for services to start
echo "Waiting for services to start..."
sleep 10

# Check status
echo "Checking Lago services status..."
ssh root@72.60.98.213 "docker ps | grep lago"

echo ""
echo "✅ Lago redeployment complete!"
echo ""
echo "Check logs with:"
echo "  ssh root@72.60.98.213 'docker logs lago-api --tail 50'"
echo "  ssh root@72.60.98.213 'docker logs lago-worker --tail 50'"
