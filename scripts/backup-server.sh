#!/bin/bash
# Complete Server Backup Script
# Run this on the OLD server (72.60.219.244)

set -e

BACKUP_DIR="/root/server-migration-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "=== BizOSaaS Server Complete Backup ==="
echo "Backup Directory: $BACKUP_DIR"
echo "Started: $(date)"
echo ""

# ============================================================================
# PHASE 1: Dokploy Configuration Backup
# ============================================================================
echo "Phase 1: Backing up Dokploy configuration..."
tar -czf "$BACKUP_DIR/dokploy-config.tar.gz" -C /etc dokploy
echo "✅ Dokploy configuration backed up"
echo ""

# ============================================================================
# PHASE 2: Database Backups
# ============================================================================
echo "Phase 2: Backing up databases..."

# Dokploy PostgreSQL
echo "  - Dokploy database..."
DOKPLOY_PG_CONTAINER=$(docker ps --filter "name=dokploy-postgres" --format "{{.Names}}" | head -1)
if [ -n "$DOKPLOY_PG_CONTAINER" ]; then
  docker exec "$DOKPLOY_PG_CONTAINER" pg_dumpall -U postgres > "$BACKUP_DIR/dokploy-database.sql"
  echo "    ✅ Dokploy database backed up"
else
  echo "    ⚠️  Dokploy PostgreSQL container not found"
fi

# Saleor PostgreSQL
echo "  - Saleor database..."
SALEOR_PG_CONTAINER=$(docker ps --filter "name=saleorpostgres" --format "{{.Names}}" | head -1)
if [ -n "$SALEOR_PG_CONTAINER" ]; then
  docker exec "$SALEOR_PG_CONTAINER" pg_dump -U saleor saleor > "$BACKUP_DIR/saleor-database.sql"
  echo "    ✅ Saleor database backed up"
else
  echo "    ⚠️  Saleor PostgreSQL container not found"
fi

# Shared PostgreSQL
echo "  - Shared PostgreSQL database..."
SHARED_PG_CONTAINER=$(docker ps --filter "name=shared-postgres" --format "{{.Names}}" | head -1)
if [ -n "$SHARED_PG_CONTAINER" ]; then
  docker exec "$SHARED_PG_CONTAINER" pg_dumpall -U postgres > "$BACKUP_DIR/shared-postgres-database.sql"
  echo "    ✅ Shared PostgreSQL database backed up"
else
  echo "    ⚠️  Shared PostgreSQL container not found"
fi

echo ""

# ============================================================================
# PHASE 3: Redis Data Backups
# ============================================================================
echo "Phase 3: Backing up Redis data..."

# Dokploy Redis
echo "  - Dokploy Redis..."
DOKPLOY_REDIS_CONTAINER=$(docker ps --filter "name=dokploy-redis" --format "{{.Names}}" | head -1)
if [ -n "$DOKPLOY_REDIS_CONTAINER" ]; then
  docker exec "$DOKPLOY_REDIS_CONTAINER" redis-cli SAVE
  docker cp "$DOKPLOY_REDIS_CONTAINER:/data/dump.rdb" "$BACKUP_DIR/dokploy-redis.rdb"
  echo "    ✅ Dokploy Redis backed up"
else
  echo "    ⚠️  Dokploy Redis container not found"
fi

# Saleor Redis
echo "  - Saleor Redis..."
SALEOR_REDIS_CONTAINER=$(docker ps --filter "name=saleorredis" --format "{{.Names}}" | head -1)
if [ -n "$SALEOR_REDIS_CONTAINER" ]; then
  docker exec "$SALEOR_REDIS_CONTAINER" redis-cli SAVE
  docker cp "$SALEOR_REDIS_CONTAINER:/data/dump.rdb" "$BACKUP_DIR/saleor-redis.rdb"
  echo "    ✅ Saleor Redis backed up"
else
  echo "    ⚠️  Saleor Redis container not found"
fi

# Shared Redis
echo "  - Shared Redis..."
SHARED_REDIS_CONTAINER=$(docker ps --filter "name=shared-redis" --format "{{.Names}}" | head -1)
if [ -n "$SHARED_REDIS_CONTAINER" ]; then
  docker exec "$SHARED_REDIS_CONTAINER" redis-cli SAVE
  docker cp "$SHARED_REDIS_CONTAINER:/data/dump.rdb" "$BACKUP_DIR/shared-redis.rdb"
  echo "    ✅ Shared Redis backed up"
else
  echo "    ⚠️  Shared Redis container not found"
fi

echo ""

# ============================================================================
# PHASE 4: Docker Volumes Backup
# ============================================================================
echo "Phase 4: Backing up Docker volumes..."

CRITICAL_VOLUMES=(
  "dokploy-postgres-database"
  "dokploy-docker-config"
  "infrastructureservices-saleorpostgres-h7eayh-data"
  "infrastructureservices-saleorredis-nzd5pv-data"
  "redis-data-volume"
)

for volume in "${CRITICAL_VOLUMES[@]}"; do
  if docker volume inspect "$volume" >/dev/null 2>&1; then
    echo "  - Backing up volume: $volume..."
    docker run --rm \
      -v "$volume:/source:ro" \
      -v "$BACKUP_DIR:/backup" \
      alpine tar -czf "/backup/${volume}.tar.gz" -C /source .
    echo "    ✅ Volume $volume backed up"
  else
    echo "    ⚠️  Volume $volume not found"
  fi
done

echo ""

# ============================================================================
# PHASE 5: Service Configurations Export
# ============================================================================
echo "Phase 5: Exporting service configurations..."

mkdir -p "$BACKUP_DIR/service-configs"

docker service ls --format '{{.Name}}' | while read service; do
  docker service inspect "$service" > "$BACKUP_DIR/service-configs/${service}.json"
done

echo "✅ Service configurations exported"
echo ""

# ============================================================================
# PHASE 6: Network Configurations Export
# ============================================================================
echo "Phase 6: Exporting network configurations..."

mkdir -p "$BACKUP_DIR/network-configs"

docker network ls --format '{{.Name}}' | while read network; do
  if [ "$network" != "bridge" ] && [ "$network" != "host" ] && [ "$network" != "none" ]; then
    docker network inspect "$network" > "$BACKUP_DIR/network-configs/${network}.json" 2>/dev/null || true
  fi
done

echo "✅ Network configurations exported"
echo ""

# ============================================================================
# PHASE 7: Environment Variables and Secrets
# ============================================================================
echo "Phase 7: Documenting environment variables..."

mkdir -p "$BACKUP_DIR/env-configs"

# Export service environment variables
docker service ls --format '{{.Name}}' | while read service; do
  docker service inspect "$service" --format '{{json .Spec.TaskTemplate.ContainerSpec.Env}}' > "$BACKUP_DIR/env-configs/${service}-env.json"
done

echo "✅ Environment variables documented"
echo ""

# ============================================================================
# PHASE 8: Vault Secrets (if accessible)
# ============================================================================
echo "Phase 8: Attempting to backup Vault secrets..."

VAULT_CONTAINER=$(docker ps --filter "name=vault" --format "{{.Names}}" | head -1)
if [ -n "$VAULT_CONTAINER" ]; then
  echo "  ⚠️  Manual Vault backup required:"
  echo "     1. Unseal Vault"
  echo "     2. Run: docker exec $VAULT_CONTAINER vault kv export -format=json secret/ > $BACKUP_DIR/vault-secrets.json"
  echo "     3. Encrypt the file immediately!"
else
  echo "  ⚠️  Vault container not found"
fi

echo ""

# ============================================================================
# PHASE 9: System Information
# ============================================================================
echo "Phase 9: Collecting system information..."

cat > "$BACKUP_DIR/system-info.txt" <<EOF
Backup Date: $(date)
Hostname: $(hostname)
OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)
Kernel: $(uname -r)
Docker Version: $(docker --version)
Docker Swarm: $(docker info | grep "Swarm:" | awk '{print $2}')

Running Services:
$(docker service ls)

Running Containers:
$(docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}")

Volumes:
$(docker volume ls)

Networks:
$(docker network ls)
EOF

echo "✅ System information collected"
echo ""

# ============================================================================
# PHASE 10: Create Inventory
# ============================================================================
echo "Phase 10: Creating backup inventory..."

cat > "$BACKUP_DIR/INVENTORY.md" <<EOF
# Backup Inventory

**Backup Date**: $(date)  
**Server**: $(hostname) ($(hostname -I | awk '{print $1}'))

## Contents

### Configuration Files
- \`dokploy-config.tar.gz\` - Complete Dokploy configuration from /etc/dokploy

### Database Backups
- \`dokploy-database.sql\` - Dokploy PostgreSQL database
- \`saleor-database.sql\` - Saleor PostgreSQL database
- \`shared-postgres-database.sql\` - Shared PostgreSQL database

### Redis Backups
- \`dokploy-redis.rdb\` - Dokploy Redis data
- \`saleor-redis.rdb\` - Saleor Redis data
- \`shared-redis.rdb\` - Shared Redis data

### Volume Backups
$(for vol in "${CRITICAL_VOLUMES[@]}"; do echo "- \`${vol}.tar.gz\` - Docker volume backup"; done)

### Service Configurations
- \`service-configs/\` - All Docker service definitions (JSON)
- \`network-configs/\` - All Docker network definitions (JSON)
- \`env-configs/\` - Environment variables for all services (JSON)

### System Information
- \`system-info.txt\` - System and Docker information

## Docker Images (Already in GHCR)

All custom images are already pushed to GitHub Container Registry:
- ghcr.io/bizoholic-digital/bizosaas-admin:latest
- ghcr.io/bizoholic-digital/bizosaas-client-portal:latest
- ghcr.io/bizoholic-digital/bizosaas-business-directory:latest
- ghcr.io/bizoholic-digital/bizosaas-ai-agents:staging
- ghcr.io/bizoholic-digital/bizosaas-brain:latest
- ghcr.io/bizoholic-digital/django-crm:vault-integration
- ghcr.io/bizoholic-digital/bizosaas-wagtail-cms:staging
- ghcr.io/bizoholic-digital/bizosaas-agent-workers:latest

## Next Steps

1. **Compress backup**: \`tar -czf server-backup-$(date +%Y%m%d).tar.gz $BACKUP_DIR\`
2. **Upload to cloud storage** (S3, Google Drive, etc.)
3. **Verify backup integrity**
4. **Keep backup secure** (contains sensitive data!)

## Restoration

See \`restore-new-server.sh\` for complete restoration procedure.
EOF

echo "✅ Inventory created"
echo ""

# ============================================================================
# PHASE 11: Create Compressed Archive
# ============================================================================
echo "Phase 11: Creating compressed archive..."

cd /root
ARCHIVE_NAME="bizosaas-server-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
tar -czf "$ARCHIVE_NAME" "$(basename $BACKUP_DIR)"

echo "✅ Compressed archive created: $ARCHIVE_NAME"
echo ""

# ============================================================================
# Summary
# ============================================================================
echo "=== Backup Complete ==="
echo ""
echo "Backup Location: $BACKUP_DIR"
echo "Archive: /root/$ARCHIVE_NAME"
echo "Archive Size: $(du -h /root/$ARCHIVE_NAME | cut -f1)"
echo ""
echo "Next Steps:"
echo "1. Download the archive: scp root@72.60.219.244:/root/$ARCHIVE_NAME ."
echo "2. Upload to secure cloud storage"
echo "3. Verify backup integrity"
echo "4. Proceed with new server setup"
echo ""
echo "⚠️  IMPORTANT:"
echo "- Keep this backup secure (contains sensitive data!)"
echo "- Don't delete old server until new server is verified"
echo "- Backup Vault secrets manually if needed"
echo ""
echo "Completed: $(date)"
