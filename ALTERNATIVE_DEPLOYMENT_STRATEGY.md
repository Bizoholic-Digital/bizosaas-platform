# Alternative Deployment Strategy - No Registry Required

**Current Blocker**: Registry authentication prevents pushing images
**Solution**: Deploy Superset by building directly on VPS from GitHub

---

## ✅ IMMEDIATE ACTION: Deploy Superset Without Registry

### Option 1: Build on VPS Directly (RECOMMENDED)

Since Superset Dockerfile and config exist in GitHub repository, Dokploy can build it directly:

**Step 1: Create Infrastructure Config with Build Context**

File: `dokploy-infrastructure-staging-build.yml`

```yaml
services:
  # ... existing postgres, redis, vault, temporal services ...

  superset:
    build:
      context: https://github.com/Bizoholic-Digital/bizosaas-platform.git#main:bizosaas/analytics/services/apache-superset
      dockerfile: Dockerfile
    container_name: bizosaas-superset-staging
    ports:
      - "8088:8088"
    environment:
      - SUPERSET_CONFIG_PATH=/app/pythonpath/superset_config.py
      - SUPERSET_SECRET_KEY=staging-secret-key-superset-bizosaas-2025
      - SUPERSET_ADMIN_PASSWORD=Bizoholic2024Admin
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=BizOSaaS2025!StagingDB
      - POSTGRES_HOST=bizosaas-postgres-staging
      - POSTGRES_PORT=5432
      - DATABASE_URL=postgresql://admin:BizOSaaS2025!StagingDB@bizosaas-postgres-staging:5432/bizosaas_staging
      - REDIS_HOST=bizosaas-redis-staging
      - REDIS_PORT=6379
      - REDIS_URL=redis://bizosaas-redis-staging:6379/2
      - BIZOSAAS_BRAIN_API_URL=http://bizosaas-brain-staging:8001
      - DEFAULT_TENANT_ID=bizosaas
    depends_on:
      - postgres
      - redis
    networks:
      - dokploy-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8088/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 120s
    volumes:
      - superset_home:/app/superset_home
```

**Step 2: Deploy in Dokploy**
1. Go to: `https://dk.bizoholic.com`
2. Navigate to: Projects → Infrastructure
3. Settings → Compose File: Paste the build-based config above
4. Click: **Deploy**
5. Wait: 5-7 minutes (Superset is large image ~5GB)

---

### Option 2: Transfer Local Image to VPS

If Option 1 fails, transfer the already-built local image:

```bash
# On local machine
docker save bizosaas-platform-apache-superset:latest | gzip > superset.tar.gz

# Transfer to VPS
scp superset.tar.gz root@194.238.16.237:/tmp/

# On VPS
ssh root@194.238.16.237
cd /tmp
gunzip -c superset.tar.gz | docker load
docker tag bizosaas-platform-apache-superset:latest bizosaas-superset-staging:latest

# Then update Dokploy config to use local image:
# image: bizosaas-superset-staging:latest
```

---

## 🔧 For Remaining Services: Build vs Registry Strategy

### Services That Can Build from GitHub (9 services)
These have Dockerfiles in repository and can build directly:

**Backend (4 services):**
1. Brain API ✅ Already building
2. Wagtail CMS ✅ Already building
3. Django CRM ✅ Already building
4. Saleor ✅ Already building

**Backend (5 need Dockerfiles confirmed):**
5. Business Directory Backend
6. CorelDove Backend
7. Temporal Integration
8. AI Agents
9. Amazon Sourcing

### Services That Need Local Images (6 services)
Frontend services built with Next.js:

1. Bizoholic Frontend (3000)
2. Client Portal (3001)
3. CorelDove Frontend (3002)
4. Business Directory Frontend (3003)
5. ThrillRing Gaming (3005)
6. Admin Dashboard (3009)

---

## 📋 Verification Checklist

### Backend Services - Check for Dockerfiles
```bash
# Check which backend services have Dockerfiles in GitHub
curl -s -H "Authorization: token YOUR_GITHUB_TOKEN" \
  "https://api.github.com/repos/Bizoholic-Digital/bizosaas-platform/git/trees/main?recursive=1" | \
  grep -E "Dockerfile" | grep -E "backend/services"
```

### Frontend Services - Check Next.js Configs
```bash
# Check frontend services structure
curl -s -H "Authorization: token YOUR_GITHUB_TOKEN" \
  "https://api.github.com/repos/Bizoholic-Digital/bizosaas-platform/contents/bizosaas-platform/frontend/apps"
```

---

## 🎯 Priority Deployment Order

### Phase 1: Infrastructure Complete (IMMEDIATE)
- Deploy Superset using build-from-GitHub strategy
- Expected time: 7-10 minutes
- Result: All 6 infrastructure services running

### Phase 2: Backend Build from GitHub
- Check which 5 backend services have Dockerfiles
- Deploy those that can build directly
- Expected time: 15-20 minutes per service

### Phase 3: Frontend Local Image Strategy
- Build all 6 frontend images locally
- Save and transfer to VPS (faster than registry)
- Expected time: 30-45 minutes total

---

## ✅ Success Metrics

**Infrastructure Complete:**
- [ ] Superset container running
- [ ] Accessible at http://194.238.16.237:8088
- [ ] Can login with admin/Bizoholic2024Admin
- [ ] All 6 infrastructure services healthy

**Backend Complete:**
- [ ] All 9 backend services running
- [ ] Health checks passing
- [ ] APIs responding on respective ports

**Frontend Complete:**
- [ ] All 6 frontend apps running
- [ ] Traefik routing configured
- [ ] Domain resolution working

---

## 🚨 If GitHub Build Fails

**Common Issues:**
1. **Missing files in subdirectory**: Check exact path in repository
2. **Dockerfile references external files**: May need to adjust COPY paths
3. **Build context too large**: Repository is large, build may timeout

**Workaround:**
Use local image transfer method (Option 2 above) for problematic services.

---

**Next Immediate Action**: Deploy Superset using GitHub build strategy in Dokploy UI.
