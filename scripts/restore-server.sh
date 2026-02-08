#!/bin/bash
# Complete Server Restoration Script
# Run this on the NEW server

set -e

echo "=== BizOSaaS Server Restoration Script ==="
echo "Started: $(date)"
echo ""

# Check if backup directory is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <path-to-backup-directory>"
  echo "Example: $0 /root/server-migration-backup-20231123-120000"
  exit 1
fi

BACKUP_DIR="$1"

if [ ! -d "$BACKUP_DIR" ]; then
  echo "Error: Backup directory not found: $BACKUP_DIR"
  exit 1
fi

echo "Backup Directory: $BACKUP_DIR"
echo ""

# ============================================================================
# PHASE 0: Prerequisites Check
# ============================================================================
echo "Phase 0: Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
  echo "❌ Docker not installed. Please install Docker first."
  exit 1
fi

# Check Docker Swarm
if ! docker info | grep -q "Swarm: active"; then
  echo "⚠️  Docker Swarm not initialized. Initializing..."
  docker swarm init
fi

# Check Dokploy
if ! docker ps | grep -q dokploy; then
  echo "⚠️  Dokploy not installed. Please install Dokploy first:"
  echo "   curl -sSL https://dokploy.com/install.sh | sh"
  read -p "Press Enter after installing Dokploy..."
fi

echo "✅ Prerequisites OK"
echo ""

# ============================================================================
# PHASE 1: Restore Dokploy Configuration
# ============================================================================
echo "Phase 1: Restoring Dokploy configuration..."

if [ -f "$BACKUP_DIR/dokploy-config.tar.gz" ]; then
  # Stop Dokploy temporarily
  docker service scale dokploy=0 || true
  sleep 5
  
  # Backup existing config (if any)
  if [ -d "/etc/dokploy" ]; then
    mv /etc/dokploy /etc/dokploy.backup.$(date +%Y%m%d-%H%M%S)
  fi
  
  # Restore configuration
  tar -xzf "$BACKUP_DIR/dokploy-config.tar.gz" -C /etc/
  
  # Restart Dokploy
  docker service scale dokploy=1
  
  echo "✅ Dokploy configuration restored"
else
  echo "⚠️  Dokploy configuration backup not found"
fi

echo ""

# ============================================================================
# PHASE 2: Restore Docker Volumes
# ============================================================================
echo "Phase 2: Restoring Docker volumes..."

for volume_backup in "$BACKUP_DIR"/*.tar.gz; do
  if [ -f "$volume_backup" ]; then
    volume_name=$(basename "$volume_backup" .tar.gz)
    
    # Skip dokploy-config (already restored)
    if [ "$volume_name" == "dokploy-config" ]; then
      continue
    fi
    
    echo "  - Restoring volume: $volume_name..."
    
    # Create volume if it doesn't exist
    docker volume create "$volume_name" || true
    
    # Restore data
    docker run --rm \
      -v "$volume_name:/target" \
      -v "$BACKUP_DIR:/backup" \
      alpine tar -xzf "/backup/$(basename $volume_backup)" -C /target
    
    echo "    ✅ Volume $volume_name restored"
  fi
done

echo ""

# ============================================================================
# PHASE 3: Restore Databases
# ============================================================================
echo "Phase 3: Restoring databases..."

# Wait for database containers to be ready
echo "  - Waiting for database containers to start..."
sleep 30

# Dokploy PostgreSQL
if [ -f "$BACKUP_DIR/dokploy-database.sql" ]; then
  echo "  - Restoring Dokploy database..."
  DOKPLOY_PG_CONTAINER=$(docker ps --filter "name=dokploy-postgres" --format "{{.Names}}" | head -1)
  if [ -n "$DOKPLOY_PG_CONTAINER" ]; then
    docker exec -i "$DOKPLOY_PG_CONTAINER" psql -U postgres < "$BACKUP_DIR/dokploy-database.sql"
    echo "    ✅ Dokploy database restored"
  else
    echo "    ⚠️  Dokploy PostgreSQL container not found"
  fi
fi

# Saleor PostgreSQL
if [ -f "$BACKUP_DIR/saleor-database.sql" ]; then
  echo "  - Restoring Saleor database..."
  SALEOR_PG_CONTAINER=$(docker ps --filter "name=saleorpostgres" --format "{{.Names}}" | head -1)
  if [ -n "$SALEOR_PG_CONTAINER" ]; then
    docker exec -i "$SALEOR_PG_CONTAINER" psql -U saleor saleor < "$BACKUP_DIR/saleor-database.sql"
    echo "    ✅ Saleor database restored"
  else
    echo "    ⚠️  Saleor PostgreSQL container not found"
  fi
fi

# Shared PostgreSQL
if [ -f "$BACKUP_DIR/shared-postgres-database.sql" ]; then
  echo "  - Restoring Shared PostgreSQL database..."
  SHARED_PG_CONTAINER=$(docker ps --filter "name=shared-postgres" --format "{{.Names}}" | head -1)
  if [ -n "$SHARED_PG_CONTAINER" ]; then
    docker exec -i "$SHARED_PG_CONTAINER" psql -U postgres < "$BACKUP_DIR/shared-postgres-database.sql"
    echo "    ✅ Shared PostgreSQL database restored"
  else
    echo "    ⚠️  Shared PostgreSQL container not found"
  fi
fi

echo ""

# ============================================================================
# PHASE 4: Restore Redis Data
# ============================================================================
echo "Phase 4: Restoring Redis data..."

# Dokploy Redis
if [ -f "$BACKUP_DIR/dokploy-redis.rdb" ]; then
  echo "  - Restoring Dokploy Redis..."
  DOKPLOY_REDIS_CONTAINER=$(docker ps --filter "name=dokploy-redis" --format "{{.Names}}" | head -1)
  if [ -n "$DOKPLOY_REDIS_CONTAINER" ]; then
    docker cp "$BACKUP_DIR/dokploy-redis.rdb" "$DOKPLOY_REDIS_CONTAINER:/data/dump.rdb"
    docker restart "$DOKPLOY_REDIS_CONTAINER"
    echo "    ✅ Dokploy Redis restored"
  else
    echo "    ⚠️  Dokploy Redis container not found"
  fi
fi

# Saleor Redis
if [ -f "$BACKUP_DIR/saleor-redis.rdb" ]; then
  echo "  - Restoring Saleor Redis..."
  SALEOR_REDIS_CONTAINER=$(docker ps --filter "name=saleorredis" --format "{{.Names}}" | head -1)
  if [ -n "$SALEOR_REDIS_CONTAINER" ]; then
    docker cp "$BACKUP_DIR/saleor-redis.rdb" "$SALEOR_REDIS_CONTAINER:/data/dump.rdb"
    docker restart "$SALEOR_REDIS_CONTAINER"
    echo "    ✅ Saleor Redis restored"
  else
    echo "    ⚠️  Saleor Redis container not found"
  fi
fi

# Shared Redis
if [ -f "$BACKUP_DIR/shared-redis.rdb" ]; then
  echo "  - Restoring Shared Redis..."
  SHARED_REDIS_CONTAINER=$(docker ps --filter "name=shared-redis" --format "{{.Names}}" | head -1)
  if [ -n "$SHARED_REDIS_CONTAINER" ]; then
    docker cp "$BACKUP_DIR/shared-redis.rdb" "$SHARED_REDIS_CONTAINER:/data/dump.rdb"
    docker restart "$SHARED_REDIS_CONTAINER"
    echo "    ✅ Shared Redis restored"
  else
    echo "    ⚠️  Shared Redis container not found"
  fi
fi

echo ""

# ============================================================================
# PHASE 5: Deploy Services from Dokploy
# ============================================================================
echo "Phase 5: Deploying services..."

echo "  ⚠️  Services should be deployed through Dokploy UI or compose files"
echo "     Navigate to Dokploy and redeploy applications"
echo ""

# ============================================================================
# PHASE 6: Verification
# ============================================================================
echo "Phase 6: Verification..."

echo "  - Docker Services:"
docker service ls

echo ""
echo "  - Running Containers:"
docker ps --format "table {{.Names}}\t{{.Status}}"

echo ""
echo "  - Volumes:"
docker volume ls | grep -E "(dokploy|saleor|redis)"

echo ""

# ============================================================================
# Summary
# ============================================================================
echo "=== Restoration Complete ==="
echo ""
echo "Next Steps:"
echo "1. Verify Dokploy UI is accessible"
echo "2. Check all service health in Dokploy dashboard"
echo "3. Verify database connectivity"
echo "4. Test application endpoints"
echo "5. Update DNS records to point to new server"
echo "6. Monitor for 24 hours before deleting old server"
echo ""
echo "Verification Commands:"
echo "  - Check Dokploy: curl http://localhost:3000"
echo "  - Check services: docker service ls"
echo "  - Check logs: docker service logs <service-name>"
echo ""
echo "Completed: $(date)"
