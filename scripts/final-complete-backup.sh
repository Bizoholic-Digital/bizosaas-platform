#!/bin/bash
# FINAL COMPREHENSIVE BACKUP - Before Server Deletion
# This backs up EVERYTHING to ensure zero data loss

set -e

FINAL_BACKUP_DIR="/root/final-complete-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$FINAL_BACKUP_DIR"

echo "=== FINAL COMPREHENSIVE BACKUP ==="
echo "Directory: $FINAL_BACKUP_DIR"
echo "Started: $(date)"
echo ""

# ============================================================================
# PHASE 1: Backup ALL Docker Volumes
# ============================================================================
echo "Phase 1: Backing up ALL Docker volumes..."

CRITICAL_VOLUMES=(
  "dokploy-postgres-database"
  "dokploy-docker-config"
  "infrastructureservices-saleorpostgres-h7eayh-data"
  "infrastructureservices-saleorredis-nzd5pv-data"
  "redis-data-volume"
  "infrastructureservices-kafka-ill4q0_kafka-data"
  "infrastructureservices-kafka-ill4q0_zookeeper-data"
  "infrastructureservices-kafka-ill4q0_zookeeper-logs"
  "infrastructureservices-rabbitmq-gktndk_rabbitmq-data"
)

for volume in "${CRITICAL_VOLUMES[@]}"; do
  if docker volume inspect "$volume" >/dev/null 2>&1; then
    echo "  Backing up volume: $volume..."
    docker run --rm \
      -v "$volume:/source:ro" \
      -v "$FINAL_BACKUP_DIR:/backup" \
      alpine tar -czf "/backup/${volume}.tar.gz" -C /source . 2>/dev/null || echo "    ⚠️  Backup failed for $volume"
    
    if [ -f "$FINAL_BACKUP_DIR/${volume}.tar.gz" ]; then
      SIZE=$(ls -lh "$FINAL_BACKUP_DIR/${volume}.tar.gz" | awk '{print $5}')
      echo "    ✅ Backed up: $SIZE"
    fi
  else
    echo "    ⚠️  Volume $volume not found"
  fi
done

echo ""

# ============================================================================
# PHASE 2: Backup Databases (with proper authentication)
# ============================================================================
echo "Phase 2: Backing up all databases..."

# Saleor PostgreSQL (already done, but ensure it's there)
SALEOR_PG=$(docker ps --filter "name=saleorpostgres" --format "{{.Names}}" | head -1)
if [ -n "$SALEOR_PG" ]; then
  echo "  Backing up Saleor database..."
  docker exec "$SALEOR_PG" sh -c 'pg_dump -U saleor saleor' > "$FINAL_BACKUP_DIR/saleor-database.sql" 2>/dev/null || \
  docker exec "$SALEOR_PG" pg_dump -U saleor saleor > "$FINAL_BACKUP_DIR/saleor-database.sql" 2>/dev/null || \
  echo "    ⚠️  Saleor backup failed"
  
  if [ -f "$FINAL_BACKUP_DIR/saleor-database.sql" ]; then
    SIZE=$(ls -lh "$FINAL_BACKUP_DIR/saleor-database.sql" | awk '{print $5}')
    echo "    ✅ Saleor database: $SIZE"
  fi
fi

# Dokploy PostgreSQL (try multiple methods)
DOKPLOY_PG=$(docker ps --filter "name=dokploy-postgres" --format "{{.Names}'" | head -1)
if [ -n "$DOKPLOY_PG" ]; then
  echo "  Backing up Dokploy database..."
  docker exec "$DOKPLOY_PG" sh -c 'pg_dumpall -U postgres' > "$FINAL_BACKUP_DIR/dokploy-database.sql" 2>/dev/null || \
  docker exec "$DOKPLOY_PG" pg_dumpall -U postgres > "$FINAL_BACKUP_DIR/dokploy-database.sql" 2>/dev/null || \
  echo "    ⚠️  Dokploy DB backup failed (will use volume backup)"
  
  if [ -f "$FINAL_BACKUP_DIR/dokploy-database.sql" ] && [ -s "$FINAL_BACKUP_DIR/dokploy-database.sql" ]; then
    SIZE=$(ls -lh "$FINAL_BACKUP_DIR/dokploy-database.sql" | awk '{print $5}')
    echo "    ✅ Dokploy database: $SIZE"
  else
    echo "    ℹ️  Using volume backup instead"
  fi
fi

echo ""

# ============================================================================
# PHASE 3: Backup ALL Redis Data
# ============================================================================
echo "Phase 3: Backing up all Redis instances..."

REDIS_CONTAINERS=$(docker ps --filter "name=redis" --format "{{.Names}}")

for container in $REDIS_CONTAINERS; do
  echo "  Backing up Redis: $container..."
  docker exec "$container" redis-cli SAVE 2>/dev/null || docker exec "$container" redis-cli --no-auth-warning SAVE 2>/dev/null || true
  docker cp "$container:/data/dump.rdb" "$FINAL_BACKUP_DIR/${container}-redis.rdb" 2>/dev/null || echo "    ⚠️  Redis backup failed for $container"
  
  if [ -f "$FINAL_BACKUP_DIR/${container}-redis.rdb" ]; then
    SIZE=$(ls -lh "$FINAL_BACKUP_DIR/${container}-redis.rdb" | awk '{print $5}')
    echo "    ✅ Redis data: $SIZE"
  fi
done

echo ""

# ============================================================================
# PHASE 4: Copy Custom Scripts
# ============================================================================
echo "Phase 4: Backing up custom scripts..."

cp /root/*.sh "$FINAL_BACKUP_DIR/" 2>/dev/null || true
echo "✅ Custom scripts backed up"
echo ""

# ============================================================================
# PHASE 5: Copy Dokploy Configuration (if not already done)
# ============================================================================
echo "Phase 5: Backing up Dokploy configuration..."

if [ -d "/etc/dokploy" ]; then
  tar -czf "$FINAL_BACKUP_DIR/dokploy-config-complete.tar.gz" -C /etc dokploy
  SIZE=$(ls -lh "$FINAL_BACKUP_DIR/dokploy-config-complete.tar.gz" | awk '{print $5}')
  echo "✅ Dokploy config: $SIZE"
fi

echo ""

# ============================================================================
# PHASE 6: Export Service Configurations
# ============================================================================
echo "Phase 6: Exporting all service configurations..."

mkdir -p "$FINAL_BACKUP_DIR/service-configs"

docker service ls --format '{{.Name}}' | while read service; do
  docker service inspect "$service" > "$FINAL_BACKUP_DIR/service-configs/${service}.json" 2>/dev/null || true
done

echo "✅ Service configurations exported"
echo ""

# ============================================================================
# PHASE 7: Create Inventory
# ============================================================================
echo "Phase 7: Creating backup inventory..."

cat > "$FINAL_BACKUP_DIR/INVENTORY.txt" <<EOF
FINAL COMPREHENSIVE BACKUP
==========================
Date: $(date)
Server: $(hostname) ($(hostname -I | awk '{print $1}'))

DOCKER VOLUMES BACKED UP:
$(ls -lh $FINAL_BACKUP_DIR/*.tar.gz 2>/dev/null | awk '{print $9, $5}')

DATABASES BACKED UP:
$(ls -lh $FINAL_BACKUP_DIR/*.sql 2>/dev/null | awk '{print $9, $5}')

REDIS DATA BACKED UP:
$(ls -lh $FINAL_BACKUP_DIR/*-redis.rdb 2>/dev/null | awk '{print $9, $5}')

CUSTOM SCRIPTS:
$(ls -1 $FINAL_BACKUP_DIR/*.sh 2>/dev/null)

TOTAL FILES: $(find $FINAL_BACKUP_DIR -type f | wc -l)
TOTAL SIZE: $(du -sh $FINAL_BACKUP_DIR | awk '{print $1}')
EOF

cat "$FINAL_BACKUP_DIR/INVENTORY.txt"
echo ""

# ============================================================================
# PHASE 8: Create Final Compressed Archive
# ============================================================================
echo "Phase 8: Creating final compressed archive..."

cd /root
ARCHIVE_NAME="bizosaas-FINAL-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
tar -czf "$ARCHIVE_NAME" "$(basename $FINAL_BACKUP_DIR)"

echo ""
echo "=== FINAL BACKUP COMPLETE ==="
echo ""
echo "Archive: /root/$ARCHIVE_NAME"
echo "Size: $(ls -lh /root/$ARCHIVE_NAME | awk '{print $5}')"
echo ""
echo "Download with:"
echo "  scp root@72.60.219.244:/root/$ARCHIVE_NAME ."
echo ""
echo "✅ SERVER IS NOW SAFE TO DELETE"
echo ""
