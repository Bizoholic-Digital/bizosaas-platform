# Modular Enhancement Pattern for BizOSaaS Platform

## Philosophy

**Use official Docker images as the foundation**  
**Add custom features as modular enhancements**  
**Never modify official images directly**

This ensures:
- ✅ Easy upgrades when official images update
- ✅ No breaking changes from upstream
- ✅ Clear separation of concerns
- ✅ Maintainability and portability

---

## Pattern: Sidecar Services

### Example: Adding Custom Features to Lago

```yaml
# Official Lago (unchanged)
lago-api:
  image: getlago/api:v1.16.0  # Official - never modify
  environment:
    - DATABASE_URL=...
    - REDIS_URL=...

# Custom Enhancement (sidecar)
lago-webhook-processor:
  image: bizosaas/lago-webhook-processor:latest  # Our custom service
  environment:
    - LAGO_API_URL=http://lago-api:3000
    - BRAIN_GATEWAY_URL=http://brain-gateway:8000
  depends_on:
    - lago-api
```

**Benefits**:
- Lago updates don't break our webhooks
- Clear separation of official vs custom
- Easy to disable/enable enhancements

---

## Pattern: Volume Mounts for Configuration

### Example: Custom Temporal Configuration

```yaml
temporal:
  image: temporalio/server:1.22.0  # Official
  volumes:
    - ./config/temporal/dynamicconfig.yaml:/etc/temporal/config/dynamicconfig/production.yaml:ro
    # Mount custom config without modifying image
```

**Benefits**:
- Official image stays pristine
- Configuration is version-controlled
- Easy to update Temporal version

---

## Pattern: Init Containers

### Example: Database Initialization

```yaml
# Official Postgres
postgres:
  image: postgres:15-alpine  # Official

# Custom init (runs once)
postgres-init:
  image: postgres:15-alpine
  command: |
    psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS pgvector;"
  depends_on:
    postgres:
      condition: service_healthy
  restart: "no"  # Run once only
```

**Benefits**:
- Postgres updates work seamlessly
- Custom extensions managed separately
- Idempotent initialization

---

## Pattern: API Gateway for Custom Logic

### Example: Adding Custom Billing Logic

```yaml
# Official Lago API
lago-api:
  image: getlago/api:v1.16.0

# Our API Gateway (intercepts requests)
brain-gateway:
  image: bizosaas/brain-gateway:latest
  environment:
    - LAGO_API_URL=http://lago-api:3000
  # Adds: usage tracking, custom pricing, tenant isolation
```

**Benefits**:
- Lago stays official and upgradable
- Custom logic in our gateway
- Can disable gateway for debugging

---

## Current Implementation

### ✅ Already Following Pattern

1. **Lago**: Using official `getlago/api:v1.16.0`
2. **Redis**: Using official `redis:7-alpine`
3. **Postgres**: Using official `postgres:15-alpine` (with pgvector variant)

### 🔧 Custom Services (Modular)

1. **brain-gateway**: Our custom API (doesn't modify official images)
2. **brain-auth**: Our custom auth (uses official Postgres/Redis)
3. **portals**: Our custom UIs (independent)

### 📦 Enhancement Modules

```
bizosaas-platform/
├── docker-compose.infrastructure.yml  # Official images only
├── docker-compose.core.yml            # Our custom services
├── docker-compose.lago.yml            # Official Lago
├── docker-compose.authentik.yml       # Official Authentik
└── enhancements/                      # Modular add-ons
    ├── lago-webhooks/                 # Lago webhook processor
    ├── temporal-workflows/            # Custom workflows
    └── monitoring/                    # Custom dashboards
```

---

## Upgrade Process

### When Official Image Updates

```bash
# Example: Lago releases v1.17.0

# 1. Update docker-compose
sed -i 's/getlago\/api:v1.16.0/getlago\/api:v1.17.0/g' docker-compose.lago.yml

# 2. Test in staging
docker-compose -f docker-compose.lago.yml up -d

# 3. Verify enhancements still work
curl http://lago-api:3000/health
curl http://brain-gateway:8000/api/billing/status

# 4. Deploy to production
```

**No code changes needed** - enhancements are modular!

---

## Best Practices

### DO ✅

- Use official images as-is
- Add features via sidecar services
- Mount configuration files
- Use environment variables for customization
- Document which features are custom

### DON'T ❌

- Fork official images
- Modify official Dockerfiles
- Hardcode custom logic into official services
- Create custom variants of official images

---

## Migration Checklist

- [x] Lago: Using official images ✅
- [x] Redis: Using official images ✅
- [x] Postgres: Using official images ✅
- [x] brain-gateway: Custom service (modular) ✅
- [x] brain-auth: Custom service (modular) ✅
- [ ] Temporal: Migrate to official `temporalio/server`
- [x] Authentik: Deploy with official `ghcr.io/goauthentik/server`

---

## Example: Adding Custom Feature

### Scenario: Add usage tracking to Lago

**❌ Wrong Way** (modifying official image):
```dockerfile
FROM getlago/api:v1.16.0
COPY custom_tracking.rb /app/lib/
# Breaks on Lago updates!
```

**✅ Right Way** (sidecar service):
```yaml
lago-usage-tracker:
  image: bizosaas/usage-tracker:latest
  environment:
    - LAGO_API_URL=http://lago-api:3000
    - WEBHOOK_URL=http://lago-api:3000/webhooks
  # Listens to Lago events, adds tracking
  # Lago updates don't affect this
```

---

## Summary

**Foundation**: Official Docker images  
**Enhancements**: Modular sidecar services  
**Result**: Upgradable, maintainable, portable platform

This pattern ensures you can:
- Update official images anytime
- Migrate to k3s/Kubernetes easily
- Maintain custom features separately
- Never break on upstream updates
