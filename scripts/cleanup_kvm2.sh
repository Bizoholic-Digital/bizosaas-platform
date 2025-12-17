#!/bin/bash

# KVM2 Infrastructure Cleanup Script
# USE WITH CAUTION: This stops and removes containers to free up resources.

echo "⚠️  WARNING: This will STOP and REMOVE the following container groups:"
echo "   - lago-* (Broken/Old stack)"
echo "   - brain-* (Old unoptimized stack)"
echo "   - authentik-* (Old Auth stack)"
echo ""
echo "It will NOT touch:"
echo "   - dokploy-*"
echo "   - wordpress/mysql (Client sites)"
echo "   - traefik"
echo ""
read -p "Are you sure you want to proceed? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

echo "🚀 Starting Cleanup..."

# 1. Stop Containers
echo "Stopping redundant containers..."
docker stop \
  lago-api lago-worker lago-front lago-db lago-redis lago-migrate \
  brain-gateway brain-auth brain-postgres brain-redis brain-vault \
  brain-temporal brain-temporal-ui \
  brain-prometheus brain-grafana brain-loki brain-jaeger \
  authentik-server authentik-worker authentik-postgres authentik-redis \
  bizosaas-admin-dashboard || true

# 2. Remove Containers
echo "Removing redundant containers..."
docker rm \
  lago-api lago-worker lago-front lago-db lago-redis lago-migrate \
  brain-gateway brain-auth brain-postgres brain-redis brain-vault \
  brain-temporal brain-temporal-ui \
  brain-prometheus brain-grafana brain-loki brain-jaeger \
  authentik-server authentik-worker authentik-postgres authentik-redis \
  bizosaas-admin-dashboard || true

# 3. Prune Systems (Optional, recovers disk space)
# echo "Pruning unused networks and volumes..."
# docker network prune -f
# docker volume prune -f

echo "✅ Cleanup Complete!"
echo "Current running containers:"
docker ps --format "table {{.Names}}\t{{.Status}}"
