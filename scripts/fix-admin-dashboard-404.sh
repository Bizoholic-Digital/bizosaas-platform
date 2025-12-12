#!/bin/bash
# Quick Fix Script for Admin Dashboard 404
# Run this on your VPS

set -e

echo "🔧 Admin Dashboard 404 Quick Fix"
echo "=================================="
echo ""

# Step 1: Stop and remove the container
echo "1. Stopping existing container..."
docker stop bizosaas-admin-dashboard 2>/dev/null || true
docker rm bizosaas-admin-dashboard 2>/dev/null || true
echo "✅ Container stopped and removed"
echo ""

# Step 2: Ensure networks exist
echo "2. Ensuring networks exist..."
docker network create bizosaas-network 2>/dev/null || echo "bizosaas-network already exists"
docker network inspect dokploy-network >/dev/null 2>&1 || echo "⚠️  WARNING: dokploy-network doesn't exist!"
echo "✅ Networks checked"
echo ""

# Step 3: Pull latest code
echo "3. Pulling latest code..."
cd /etc/dokploy/compose/bizosaasadmindashboard-bizosaasadmindashboard-clo6cl/code
git pull origin staging
echo "✅ Code updated"
echo ""

# Step 4: Rebuild and start with docker compose
echo "4. Rebuilding and starting container..."
docker compose -f docker-compose.admin-dashboard.yml up -d --build --force-recreate
echo "✅ Container started"
echo ""

# Step 5: Wait for container to be healthy
echo "5. Waiting for container to be healthy (max 60 seconds)..."
COUNTER=0
while [ $COUNTER -lt 20 ]; do
    HEALTH=$(docker inspect bizosaas-admin-dashboard --format='{{.State.Health.Status}}' 2>/dev/null || echo "none")
    if [ "$HEALTH" = "healthy" ]; then
        echo "✅ Container is healthy!"
        break
    fi
    echo "   Status: $HEALTH (attempt $((COUNTER+1))/20)"
    sleep 3
    COUNTER=$((COUNTER+1))
done
echo ""

# Step 6: Check if app is responding
echo "6. Testing health endpoint..."
sleep 5
docker exec bizosaas-admin-dashboard wget -qO- http://localhost:3004/api/health && echo "✅ Health endpoint responding" || echo "❌ Health endpoint not responding"
echo ""

# Step 7: Check Traefik routing
echo "7. Checking Traefik routing..."
docker logs traefik 2>&1 | grep -i "admin-dashboard" | tail -5 || echo "No Traefik logs found for admin-dashboard"
echo ""

# Step 8: Verify networks
echo "8. Verifying container networks..."
docker inspect bizosaas-admin-dashboard --format='{{range $key, $value := .NetworkSettings.Networks}}{{$key}}{{"\n"}}{{end}}'
echo ""

# Step 9: Show container logs
echo "9. Container logs (last 20 lines):"
echo "-----------------------------------"
docker logs bizosaas-admin-dashboard --tail 20
echo ""

echo "=================================="
echo "✅ Fix script complete!"
echo ""
echo "Next steps:"
echo "1. Test: curl https://admin.bizoholic.net/api/health"
echo "2. Visit: https://admin.bizoholic.net"
echo "3. If still 404, run: bash diagnose-admin-dashboard.sh"
echo ""
