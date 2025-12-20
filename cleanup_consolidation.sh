#!/bin/bash
set -e

echo "Starting Authentik Consolidation & Cleanup..."

# 1. Redeploy Authentik with new Redis DB configuration
echo "Re-deploying Authentik..."
cd /root/bizosaas-platform
docker compose -f dokploy-authentik-staging.yml down
docker compose -f dokploy-authentik-staging.yml up -d

echo "Authentik redeployed. Verifying Redis connection..."
# Wait a brief moment for startup
sleep 5
docker logs bizosaas-authentik-server --tail 20

# 2. Cleanup unused images and volumes
echo "Cleaning up..."
# Remove old Authentik image
docker rmi ghcr.io/goauthentik/server:2024.10.1 || echo "Old image not found or already removed."

# Remove dangling images (optional, safe)
# docker image prune -f

echo "Consolidation and cleanup complete!"
echo "Please manually verify that Authentik is working and check Redis keys in DB 1:"
echo "docker exec bizosaas-redis-staging redis-cli -n 1 KEYS *"
