#!/bin/bash
# Complete cleanup and fix for port conflicts and orphan containers

set -e

echo "🧹 Complete Environment Cleanup and Fix"
echo "========================================"
echo ""

# Stop old saleor-platform containers (using ports 5432, 6379)
echo "🛑 Stopping old saleor-platform containers..."
docker stop saleor-platform-db-1 saleor-platform-redis-1 2>/dev/null || true

# Stop orphan bizosaas containers
echo "🛑 Stopping orphan bizosaas containers..."
docker stop bizosaas-postgres-primary bizosaas-redis-primary 2>/dev/null || true

# Stop any bizosaas-unified containers
echo "🛑 Stopping bizosaas-unified containers..."
cd "$(dirname "$0")/bizosaas"
docker-compose -f docker-compose.unified.yml down 2>/dev/null || true

# Remove orphan containers
echo "🗑️  Removing stopped containers..."
docker rm -f saleor-platform-db-1 saleor-platform-redis-1 2>/dev/null || true
docker rm -f bizosaas-postgres-primary bizosaas-redis-primary 2>/dev/null || true
docker rm -f bizosaas-postgres-unified bizosaas-redis-unified 2>/dev/null || true

# Create network if it doesn't exist
echo "🔧 Creating Docker network..."
docker network inspect bizosaas-platform-network >/dev/null 2>&1 || \
  docker network create bizosaas-platform-network

# Create volumes if they don't exist
echo "💾 Ensuring Docker volumes exist..."
docker volume inspect bizosaas-postgres-data >/dev/null 2>&1 || \
  docker volume create bizosaas-postgres-data

docker volume inspect bizosaas-redis-data >/dev/null 2>&1 || \
  docker volume create bizosaas-redis-data

# Verify ports are free
echo ""
echo "🔍 Verifying ports are free..."
if sudo netstat -tulpn | grep -q ":5432"; then
  echo "⚠️  WARNING: Port 5432 still in use!"
  sudo netstat -tulpn | grep ":5432"
else
  echo "✅ Port 5432 is free"
fi

if sudo netstat -tulpn | grep -q ":6379"; then
  echo "⚠️  WARNING: Port 6379 still in use!"
  sudo netstat -tulpn | grep ":6379"
else
  echo "✅ Port 6379 is free"
fi

echo ""
echo "✅ Cleanup complete! Environment ready."
echo ""
echo "🚀 Now you can run:"
echo "  ./start-bizoholic.sh"
echo "  ./start-coreldove.sh"
echo ""
