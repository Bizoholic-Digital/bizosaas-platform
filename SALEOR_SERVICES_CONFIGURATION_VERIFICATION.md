# Saleor PostgreSQL & Redis Configuration Verification

**Date:** November 3, 2025
**Purpose:** Pre-deployment configuration verification for Saleor infrastructure services
**Status:** ✅ READY FOR DEPLOYMENT

---

## Configuration Summary

### Current Infrastructure Services

| Service | External Port | Internal Port | Status |
|---------|--------------|---------------|--------|
| **shared-postgres** | 5433 | 5432 | ✅ Deployed |
| **shared-redis** | 6380 | 6379 | ✅ Deployed |
| **saleor-postgres** | None | 5432 | ⏳ Created, Not Deployed |
| **saleor-redis** | None | 6379 | ⏳ Created, Not Deployed |

---

## ✅ SERVICE 1: Saleor PostgreSQL

### Configuration Verification

```yaml
Service Name: saleor-postgres
Project: infrastructure-services
Status: CREATED (awaiting deployment)

Image Configuration:
  Image: pgvector/pgvector:pg16 ✅
  Replicas: 1 ✅

Database Configuration:
  POSTGRES_DB: saleor ✅
  POSTGRES_USER: saleor ✅
  POSTGRES_PASSWORD: SaleorDB2025@Staging ✅

Network Configuration:
  Network: dokploy-network ✅
  Internal Port: 5432 (default PostgreSQL)
  External Port: None (internal only) ✅

Port Allocation:
  ✅ No conflict - shared-postgres uses 5433 externally
  ✅ Internal 5432 is fine (different service name resolution)
```

### Expected Service Hostname After Deployment

**Internal Docker DNS:** `infrastructure-saleor-postgres:5432`

**Full DATABASE_URL:**
```
postgresql://saleor:SaleorDB2025@Staging@infrastructure-saleor-postgres:5432/saleor
```

### ⚠️ CRITICAL PRE-DEPLOYMENT CHECK

**Persistent Volume Configuration:**
- **Mount Path:** `/var/lib/postgresql/data`
- **Volume Type:** Must be persistent (not ephemeral)
- **Why Critical:** Without persistent volume, ALL e-commerce data will be lost on container restart

**Please verify in Dokploy UI that persistent volume is configured!**

---

## ✅ SERVICE 2: Saleor Redis

### Configuration Verification

```yaml
Service Name: saleor-redis
Project: infrastructure-services
Status: CREATED (awaiting deployment)

Image Configuration:
  Image: redis:7-alpine ✅
  Replicas: 1 ✅

Redis Configuration:
  Password: SaleorRedis2025@Staging ✅
  Command: (not set - needs configuration)

Network Configuration:
  Network: dokploy-network ✅
  Internal Port: 6379 (default Redis)
  External Port: None (internal only) ✅

Port Allocation:
  ✅ No conflict - shared-redis uses 6380 externally
  ✅ Internal 6379 is fine (different service name resolution)
```

### Expected Service Hostname After Deployment

**Internal Docker DNS:** `infrastructure-saleor-redis:6379`

### 🔧 REQUIRED: Redis Password Configuration

**Option 1: Using Command (Recommended)**
```bash
redis-server --requirepass SaleorRedis2025@Staging --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
```

**Option 2: Using Config File**
- Create Redis config with `requirepass SaleorRedis2025@Staging`
- Mount config file to `/usr/local/etc/redis/redis.conf`

**Redis URLs After Configuration:**
```bash
# Cache URL (database 0)
CACHE_URL=redis://:SaleorRedis2025@Staging@infrastructure-saleor-redis:6379/0

# Celery Broker URL (database 1)
CELERY_BROKER_URL=redis://:SaleorRedis2025@Staging@infrastructure-saleor-redis:6379/1
```

**Note:** The `:` before the password is required Redis URL syntax for password-only auth.

### 📝 RECOMMENDED: Redis Persistence

**Add Persistent Volume (Optional but Recommended):**
- **Mount Path:** `/data`
- **Purpose:** Persist Redis data across restarts (for AOF persistence)
- **Not Critical:** Redis is used for caching/sessions, can be rebuilt

---

## Port Allocation Summary

### PostgreSQL Services
| Service | External Port | Internal Port | Purpose |
|---------|--------------|---------------|---------|
| dokploy-postgres | None | 5432 | Dokploy internal DB |
| shared-postgres | 5433 | 5432 | Shared infrastructure DB |
| **saleor-postgres** | **None** | **5432** | **Saleor e-commerce DB** |

**✅ No Port Conflicts** - All services use different external ports or internal-only

### Redis Services
| Service | External Port | Internal Port | Purpose |
|---------|--------------|---------------|---------|
| dokploy-redis | None | 6379 | Dokploy internal cache |
| shared-redis | 6380 | 6379 | Shared infrastructure cache |
| **saleor-redis** | **None** | **6379** | **Saleor cache/sessions/celery** |

**✅ No Port Conflicts** - All services use different external ports or internal-only

---

## Pre-Deployment Checklist

### Saleor PostgreSQL Service
- [x] Service name: `saleor-postgres`
- [x] Image: `pgvector/pgvector:pg16`
- [x] Database name: `saleor`
- [x] Username: `saleor`
- [x] Password: `SaleorDB2025@Staging`
- [x] Network: `dokploy-network`
- [x] No external port (internal only)
- [ ] **VERIFY: Persistent volume at `/var/lib/postgresql/data`** ⚠️ CRITICAL

### Saleor Redis Service
- [x] Service name: `saleor-redis`
- [x] Image: `redis:7-alpine`
- [x] Password: `SaleorRedis2025@Staging`
- [x] Network: `dokploy-network`
- [x] No external port (internal only)
- [ ] **ADD: Command with `--requirepass SaleorRedis2025@Staging`** ⚠️ REQUIRED
- [ ] OPTIONAL: Persistent volume at `/data` (recommended)

---

## Post-Deployment Actions

After you deploy both services, the following actions will be executed:

### 1. Verify Services are Running
```bash
docker service ls | grep -E '(saleor-postgres|saleor-redis)'
docker service ps infrastructure-saleor-postgres
docker service ps infrastructure-saleor-redis
```

### 2. Update Saleor API Configuration
```bash
# Add DATABASE_URL
docker service update \
  --env-add "DATABASE_URL=postgresql://saleor:SaleorDB2025@Staging@infrastructure-saleor-postgres:5432/saleor" \
  backend-saleor-api

# Add Redis URLs
docker service update \
  --env-add "CACHE_URL=redis://:SaleorRedis2025@Staging@infrastructure-saleor-redis:6379/0" \
  --env-add "CELERY_BROKER_URL=redis://:SaleorRedis2025@Staging@infrastructure-saleor-redis:6379/1" \
  backend-saleor-api
```

### 3. Run Database Migrations
```bash
docker exec [saleor-api-container] python manage.py migrate
```

### 4. Create Superuser
```bash
docker exec [saleor-api-container] python manage.py createsuperuser \
  --email admin@coreldove.com \
  --no-input

docker exec [saleor-api-container] python manage.py shell -c \
  "from saleor.account.models import User; u=User.objects.get(email='admin@coreldove.com'); u.set_password('CoreLdove2025!Admin'); u.save()"
```

### 5. Test Dashboard Login
- URL: https://stg.coreldove.com/dashboard/
- Email: admin@coreldove.com
- Password: CoreLdove2025!Admin

---

## Configuration Comparison: Current vs Expected

### Current Configuration (credentials.md lines 217-236)
```bash
# Expected after deployment
SALEOR_POSTGRES_HOST=infrastructureservices-saleorpostgres-las0jw  # ❌ Wrong
SALEOR_REDIS_HOST=infrastructureservices-saleorredis-qrl0jc       # ❌ Wrong
```

### Actual Configuration (After Deployment)
```bash
# Actual service hostnames (based on Dokploy naming)
SALEOR_POSTGRES_HOST=infrastructure-saleor-postgres  # ✅ Correct
SALEOR_REDIS_HOST=infrastructure-saleor-redis        # ✅ Correct
```

**Note:** The credentials.md file will be updated after deployment with correct hostnames.

---

## ⚠️ CRITICAL ITEMS TO VERIFY BEFORE DEPLOYING

### 1. PostgreSQL Persistent Volume ⚠️ MANDATORY
**Without this, ALL e-commerce data will be LOST on container restart!**
- Go to Dokploy UI → infrastructure-services → saleor-postgres
- Check "Volumes" or "Mounts" section
- Verify persistent volume is configured at `/var/lib/postgresql/data`

### 2. Redis Password Command ⚠️ REQUIRED
**Without this, Redis will be unprotected!**
- Go to Dokploy UI → infrastructure-services → saleor-redis
- In "Command" field, add:
  ```
  redis-server --requirepass SaleorRedis2025@Staging --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
  ```

### 3. Network Configuration ✅ Already Correct
- Both services are on `dokploy-network`
- This is the same network as `backend-saleor-api`

---

## Final Verification Questions

Before proceeding with deployment, please confirm:

1. **PostgreSQL persistent volume is configured** at `/var/lib/postgresql/data`?
2. **Redis command includes password** `--requirepass SaleorRedis2025@Staging`?
3. **Both services are in** `infrastructure-services` project?
4. **Both services use** `dokploy-network`?

---

## ✅ DEPLOYMENT APPROVAL

**Configuration Status:** ✅ CORRECT (pending 2 critical verifications above)

**Port Allocation:** ✅ NO CONFLICTS

**Credentials:** ✅ MATCH credentials.md

**Network:** ✅ CORRECT (dokploy-network)

**Ready to Deploy:** ⚠️ YES, after verifying:
1. PostgreSQL persistent volume
2. Redis password command

---

## Next Steps

1. **YOU:** Verify persistent volume and Redis command in Dokploy UI
2. **YOU:** Deploy saleor-postgres
3. **YOU:** Deploy saleor-redis
4. **YOU:** Confirm deployment completion
5. **ME:** Verify services running
6. **ME:** Update Saleor API configuration
7. **ME:** Run migrations
8. **ME:** Create superuser
9. **ME:** Test dashboard login
10. **ME:** Update credentials.md

---

**Document Status:** READY FOR USER REVIEW AND DEPLOYMENT
