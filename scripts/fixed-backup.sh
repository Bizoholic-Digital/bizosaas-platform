#!/bin/bash
# Fixed Database Backup Commands
# Run these on the server: 72.60.219.244

echo "=== Corrected Database Backup Commands ==="
echo ""

# Get container names
DOKPLOY_PG=$(docker ps --filter "name=dokploy-postgres" --format "{{.Names}}" | head -1)
SALEOR_PG=$(docker ps --filter "name=saleorpostgres" --format "{{.Names}}" | head -1)
SHARED_PG=$(docker ps --filter "name=shared-postgres" --format "{{.Names}}" | head -1)
DOKPLOY_REDIS=$(docker ps --filter "name=dokploy-redis" --format "{{.Names}}" | head -1)
SALEOR_REDIS=$(docker ps --filter "name=saleorredis" --format "{{.Names}}" | head -1)
SHARED_REDIS=$(docker ps --filter "name=shared-redis" --format "{{.Names}}" | head -1)

echo "Found containers:"
echo "  Dokploy PostgreSQL: $DOKPLOY_PG"
echo "  Saleor PostgreSQL: $SALEOR_PG"
echo "  Shared PostgreSQL: $SHARED_PG"
echo "  Dokploy Redis: $DOKPLOY_REDIS"
echo "  Saleor Redis: $SALEOR_REDIS"
echo "  Shared Redis: $SHARED_REDIS"
echo ""

# Backup Dokploy PostgreSQL
if [ -n "$DOKPLOY_PG" ]; then
  echo "Backing up Dokploy PostgreSQL..."
  docker exec "$DOKPLOY_PG" sh -c 'PGPASSWORD=$POSTGRES_PASSWORD pg_dumpall -U postgres' > /root/dokploy-db.sql
  echo "✅ Dokploy database backed up: $(ls -lh /root/dokploy-db.sql | awk '{print $5}')"
else
  echo "⚠️  Dokploy PostgreSQL container not found"
fi

# Backup Saleor PostgreSQL
if [ -n "$SALEOR_PG" ]; then
  echo "Backing up Saleor PostgreSQL..."
  docker exec "$SALEOR_PG" sh -c 'PGPASSWORD=$POSTGRES_PASSWORD pg_dump -U saleor saleor' > /root/saleor-db.sql
  echo "✅ Saleor database backed up: $(ls -lh /root/saleor-db.sql | awk '{print $5}')"
else
  echo "⚠️  Saleor PostgreSQL container not found"
fi

# Backup Shared PostgreSQL
if [ -n "$SHARED_PG" ]; then
  echo "Backing up Shared PostgreSQL..."
  docker exec "$SHARED_PG" sh -c 'PGPASSWORD=$POSTGRES_PASSWORD pg_dumpall -U postgres' > /root/shared-postgres-db.sql
  echo "✅ Shared PostgreSQL backed up: $(ls -lh /root/shared-postgres-db.sql | awk '{print $5}')"
else
  echo "⚠️  Shared PostgreSQL container not found"
fi

# Backup Dokploy Redis (already done)
if [ -n "$DOKPLOY_REDIS" ]; then
  echo "Backing up Dokploy Redis..."
  docker exec "$DOKPLOY_REDIS" redis-cli SAVE
  docker cp "$DOKPLOY_REDIS:/data/dump.rdb" /root/dokploy-redis.rdb
  echo "✅ Dokploy Redis backed up: $(ls -lh /root/dokploy-redis.rdb | awk '{print $5}')"
fi

# Backup Saleor Redis
if [ -n "$SALEOR_REDIS" ]; then
  echo "Backing up Saleor Redis..."
  docker exec "$SALEOR_REDIS" redis-cli SAVE
  docker cp "$SALEOR_REDIS:/data/dump.rdb" /root/saleor-redis.rdb
  echo "✅ Saleor Redis backed up: $(ls -lh /root/saleor-redis.rdb | awk '{print $5}')"
fi

# Backup Shared Redis
if [ -n "$SHARED_REDIS" ]; then
  echo "Backing up Shared Redis..."
  docker exec "$SHARED_REDIS" redis-cli SAVE
  docker cp "$SHARED_REDIS:/data/dump.rdb" /root/shared-redis.rdb
  echo "✅ Shared Redis backed up: $(ls -lh /root/shared-redis.rdb | awk '{print $5}')"
fi

echo ""
echo "Creating final compressed archive..."
cd /root
tar -czf bizosaas-backup-$(date +%Y%m%d).tar.gz \
  server-migration-backup-* \
  dokploy-db.sql \
  saleor-db.sql \
  shared-postgres-db.sql \
  dokploy-redis.rdb \
  saleor-redis.rdb \
  shared-redis.rdb \
  2>/dev/null

BACKUP_FILE=$(ls -t bizosaas-backup-*.tar.gz | head -1)
echo ""
echo "✅ Backup Complete!"
echo "Archive: /root/$BACKUP_FILE"
echo "Size: $(ls -lh /root/$BACKUP_FILE | awk '{print $5}')"
echo ""
echo "Download with:"
echo "  scp root@72.60.219.244:/root/$BACKUP_FILE ."
