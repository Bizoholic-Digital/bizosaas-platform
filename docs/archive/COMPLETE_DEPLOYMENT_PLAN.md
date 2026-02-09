# BizOSaaS Complete Deployment & Optimization Plan

**Created:** 2026-01-21 05:16 UTC  
**Strategy:** Fix ALL services together with optimized configurations

---

## 🎯 Executive Summary

**Current Issue:** 522 errors due to Traefik routing conflicts  
**Root Cause:** Dokploy auto-generated labels conflicting with manual labels  
**Solution:** Standardize ALL compose files with Dokploy best practices

**Key Decision:** We will fix ALL services TOGETHER because:
1. The root cause (Traefik conflicts) affects ALL services
2. We need to standardize the approach across all compose files
3. Individual fixes will take longer and may introduce new conflicts
4. We have all credentials and can configure everything at once

---

## 📋 Services to Deploy & Optimize

### External Cloud Services (Already Configured)
✅ **Neon PostgreSQL** - `postgresql://neondb_owner:npg_puEbTnkSO9F8@ep-gentle-flower-a15rdh2r-pooler.ap-southeast-1.aws.neon.tech/neondb`
✅ **Redis Cloud** - `redis://default:Gt7QxXA4ybMzYzD9e6KIBULfnv1IU6f9@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690`
✅ **Temporal Cloud** - `ap-south-2.aws.api.temporal.io:7233` (with mTLS certs)
✅ **Grafana Cloud** - Monitoring & Logging (token configured)

### Services to Deploy on KVM2
1. **Core Stack** (brain-gateway + MCPs)
2. **Vault** (secrets management)
3. **Lago** (billing engine)
4. **Client Portal** (Next.js)
5. **Admin Portal** (Next.js)
6. **Business Directory** (Next.js)

---

## 🔧 Standardization Requirements

### Every docker-compose.yml MUST have:

1. **Traefik Labels Pattern** (following Dokploy templates):
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.docker.network=dokploy-network"
  # Dokploy will auto-generate these based on domain configuration:
  # - HTTP router (web entrypoint with redirect)
  # - HTTPS router (websecure entrypoint with Let's Encrypt)
  # - Service with correct port
```

2. **Network Configuration**:
```yaml
networks:
  dokploy-network:
    external: true
    name: dokploy-network
  # Service-specific networks as needed
```

3. **Resource Limits** (prevent conflicts):
```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'  # Adjust per service
      memory: 512M  # Adjust per service
    reservations:
      cpus: '0.25'
      memory: 256M
```

4. **Health Checks**:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:PORT/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

5. **Restart Policy**:
```yaml
restart: unless-stopped
```

---

## 📝 Implementation Plan

### Phase 1: Optimize All Compose Files (30 mins)

#### 1.1 Core Stack (`docker-compose.core.yml`)
- ✅ Remove ALL manual Traefik routing labels
- ✅ Keep only `traefik.enable=true` and `traefik.docker.network=dokploy-network`
- ✅ Update to use Neon DB (already configured)
- ✅ Update to use Redis Cloud (already configured)
- ✅ Update to use Temporal Cloud (add mTLS certs)
- ✅ Add resource limits for brain-gateway and all MCPs
- ✅ Add health checks
- ✅ Ensure Vault connectivity

#### 1.2 Vault (`docker-compose.vault.yml`)
- Create new optimized compose file
- Remove manual labels
- Add resource limits
- Connect to dokploy-network and brain-network

#### 1.3 Lago (`docker-compose.lago.yml`)
- ✅ Remove manual labels (already done)
- Add resource limits for all services
- Configure with Neon DB
- Configure with Redis Cloud
- Add health checks

#### 1.4 Client Portal (`docker-compose.client-portal.yml`)
- Remove manual labels
- Add resource limits
- Configure API URL to brain-gateway
- Add Clerk credentials from Vault
- Add health checks

#### 1.5 Admin Portal (`docker-compose.admin-portal.yml`)
- Remove manual labels
- Add resource limits
- Configure API URL to brain-gateway
- Add Clerk credentials from Vault
- Add health checks

#### 1.6 Business Directory (`docker-compose.directory.yml`)
- ✅ Remove manual labels (already done)
- Add resource limits
- Configure API URL to brain-gateway
- Add health checks

### Phase 2: Configure Dokploy Domains (10 mins)

Create domains in Dokploy UI for each service:

1. **brain-gateway**: `api.bizoholic.net` → port 8000
2. **vault**: `vault.bizoholic.net` → port 8200
3. **lago-front**: `billing.bizoholic.net` → port 80
4. **lago-api**: `billing-api.bizoholic.net` → port 3000
5. **client-portal**: `app.bizoholic.net` → port 3000
6. **admin-portal**: `admin.bizoholic.net` → port 3000
7. **business-directory**: `directory.bizoholic.net` → port 3000

### Phase 3: Deploy All Services (20 mins)

Deploy in this order:
1. Vault (foundation for secrets)
2. Core Stack (brain-gateway + MCPs)
3. Lago (billing engine)
4. Client Portal
5. Admin Portal
6. Business Directory

### Phase 4: Verification (10 mins)

Test each domain:
- [ ] `https://api.bizoholic.net/health` → 200 OK
- [ ] `https://vault.bizoholic.net` → Vault UI
- [ ] `https://billing.bizoholic.net` → Lago Front
- [ ] `https://billing-api.bizoholic.net` → Lago API
- [ ] `https://app.bizoholic.net` → Client Portal
- [ ] `https://admin.bizoholic.net` → Admin Portal
- [ ] `https://directory.bizoholic.net` → Business Directory

---

## 🔐 Environment Variables Strategy

### Use Vault for ALL secrets:
- AI API Keys (OpenAI, Anthropic, Google)
- Clerk credentials
- JWT secrets
- Database passwords (if not using Neon)

### Use Environment Variables for:
- External service URLs (Neon, Redis Cloud, Temporal Cloud)
- Non-sensitive configuration
- Feature flags

---

## 📊 Resource Allocation (8GB RAM Total)

| Service | CPU Limit | Memory Limit | Priority |
|---------|-----------|--------------|----------|
| Traefik | 0.5 | 256M | Critical |
| Dokploy | - | 512M | Critical |
| Vault | 0.25 | 256M | High |
| Brain Gateway | 1.0 | 1024M | High |
| MCPs (6x) | 0.25 each | 128M each | Medium |
| Lago API | 0.5 | 512M | Medium |
| Lago Front | 0.25 | 256M | Medium |
| Lago Worker | 0.25 | 256M | Medium |
| Client Portal | 0.5 | 512M | Medium |
| Admin Portal | 0.5 | 512M | Medium |
| Business Directory | 0.25 | 256M | Low |
| **Total** | ~5.5 CPUs | ~5.5GB | |

**Buffer:** 2.5GB for system + overhead

---

## ✅ Success Criteria

1. **No 522 Errors** - All domains respond with 200 OK
2. **SSL Certificates** - All domains have valid Let's Encrypt certs
3. **No Traefik Conflicts** - Clean Traefik logs
4. **Resource Compliance** - All services within limits
5. **Health Checks** - All services report healthy
6. **External Services** - Neon, Redis Cloud, Temporal Cloud all connected
7. **Portability** - Can redeploy to another server without issues

---

## 🚀 Execution Timeline

**Total Time:** ~70 minutes

1. **Optimize Compose Files** - 30 mins
2. **Configure Dokploy Domains** - 10 mins
3. **Deploy All Services** - 20 mins
4. **Verification & Testing** - 10 mins

---

## 🎯 Next Steps

**Immediate Action:**
1. Start optimizing `docker-compose.core.yml`
2. Create optimized compose files for all services
3. Push all changes to GitHub
4. Configure Dokploy domains via API
5. Deploy all services
6. Verify and test

**Ready to proceed?** This approach will fix everything at once and ensure consistency across all services.
