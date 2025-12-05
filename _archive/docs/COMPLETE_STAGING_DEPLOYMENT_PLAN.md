# Complete BizOSaaS Staging Deployment Plan

## Complete Local Container Inventory (What We Need to Deploy)

### Infrastructure Services (10 containers locally running/stopped)
1. ✅ **bizosaas-postgres-unified** (postgres:15-alpine) - Port 5432
2. ✅ **bizosaas-redis-unified** (redis:7-alpine) - Port 6379
3. ✅ **bizosaas-vault** (hashicorp/vault:1.15) - Port 8200
4. ✅ **bizosaas-temporal-server** (temporalio/auto-setup:1.22.0) - Port 7233
5. ✅ **bizosaas-temporal-ui-server** (temporalio/ui:2.21.0) - Port 8082→8080

### Backend Services (9 containers locally)
6. ✅ **bizosaas-brain-unified** (bizosaas-brain-gateway:latest) - Port 8001
7. ✅ **bizosaas-saleor-unified** (ghcr.io/saleor/saleor:3.20) - Port 8000
8. ✅ **bizosaas-wagtail-cms** (bizosaas-wagtail-cms:latest) - Port 8002
9. ✅ **bizosaas-django-crm-8003** (django-crm-django-crm) - Port 8003
10. ✅ **bizosaas-business-directory-backend-8004** (bizosaas-business-directory-backend:latest) - Port 8004
11. ✅ **coreldove-backend-8005** (coreldove-backend-coreldove-backend) - Port 8005
12. ✅ **bizosaas-temporal-unified** (bizosaas-platform-temporal-integration:latest) - Port 8009
13. ✅ **bizosaas-ai-agents-8010** (bizosaas-platform-bizosaas-brain-enhanced:latest) - Port 8010→8000
14. ✅ **amazon-sourcing-8085** (bizosaas/amazon-sourcing:latest) - Port 8085→8080

### Frontend Services (5 containers locally)
15. ✅ **bizoholic-frontend-3000** (bizoholic-frontend:dev) - Port 3000
16. ✅ **bizosaas-client-portal-3001** (bizosaas-client-portal:latest) - Port 3001→3000
17. ✅ **coreldove-frontend-3002** (bizosaas-coreldove-frontend:latest) - Port 3002
18. ✅ **business-directory-3004** (bizosaas-business-directory:latest) - Port 3004
19. ✅ **bizosaas-admin-3009** (bizosaas-bizosaas-admin:latest) - Port 3009

**Total: 19 containers to deploy to staging**

---

## Current Staging Deployment Status

### ✅ Infrastructure Project (5/5 services) - COMPLETE
- ✅ bizosaas-postgres-staging (Port 5433→5432)
- ✅ bizosaas-redis-staging (Port 6380→6379)
- ✅ bizosaas-vault-staging (Port 8201→8200)
- ❌ **MISSING: Temporal Server** (Port 7234→7233)
- ❌ **MISSING: Temporal UI** (Port 8083→8080)

### ⚠️ Backend Project (2/9 services working) - INCOMPLETE
- ✅ bizosaas-brain-staging (Port 8001) - **HEALTHY**
- ✅ bizosaas-saleor-staging (Port 8000) - **HEALTHY**
- ⚠️ bizosaas-wagtail-staging - **CRASHING** (settings.staging not found)
- ⚠️ bizosaas-django-crm-staging - **CRASHING** (settings.staging not found)
- ❌ **MISSING: Business Directory Backend** (Port 8004)
- ❌ **MISSING: CorelDove Backend** (Port 8005)
- ❌ **MISSING: Temporal Integration** (Port 8009)
- ❌ **MISSING: AI Agents Service** (Port 8010)
- ❌ **MISSING: Amazon Sourcing** (Port 8085)

### ❌ Frontend Project (0/5 services) - NOT DEPLOYED
- ❌ **MISSING: Bizoholic Frontend** (Port 3000)
- ❌ **MISSING: Client Portal** (Port 3001)
- ❌ **MISSING: CorelDove Frontend** (Port 3002)
- ❌ **MISSING: Business Directory Frontend** (Port 3004)
- ❌ **MISSING: Admin Dashboard** (Port 3009)

---

## Deployment Strategy: 3 Dokploy Projects

### PROJECT 1: Infrastructure Services (dokploy-infrastructure-staging.yml)
**Status**: Partially deployed, needs Temporal services

```yaml
services:
  postgres:        # ✅ DEPLOYED (Port 5433)
  redis:           # ✅ DEPLOYED (Port 6380)
  vault:           # ✅ DEPLOYED (Port 8201)
  temporal-server: # ❌ NEEDS DEPLOYMENT (Port 7234)
  temporal-ui:     # ❌ NEEDS DEPLOYMENT (Port 8083)
```

**Action**: Update existing config to add Temporal services

---

### PROJECT 2: Backend Services (dokploy-backend-staging-complete.yml)
**Status**: 2/9 services working, 2 crashing, 5 missing

#### Currently Deployed (Fix Required)
```yaml
services:
  db-init:         # ✅ RUNS ONCE (creates databases)
  brain-api:       # ✅ HEALTHY (Port 8001)
  saleor-api:      # ✅ HEALTHY (Port 8000)
  wagtail-cms:     # ⚠️ CRASHING (Fix: change settings.staging → settings.production)
  django-crm:      # ⚠️ CRASHING (Fix: change settings.staging → settings.production)
```

#### Missing Services (Need to Add)
```yaml
  business-directory-backend: # ❌ Port 8004
  coreldove-backend:          # ❌ Port 8005
  temporal-integration:       # ❌ Port 8009
  ai-agents:                  # ❌ Port 8010
  amazon-sourcing:            # ❌ Port 8085
```

**Action**: Fix settings, add 5 missing services

---

### PROJECT 3: Frontend Services (dokploy-frontend-staging-complete.yml)
**Status**: Not deployed at all

```yaml
services:
  bizoholic-frontend:     # ❌ Port 3000 (Traefik: stg.bizoholic.com)
  client-portal:          # ❌ Port 3001 (Traefik: stg.portal.bizoholic.com)
  coreldove-frontend:     # ❌ Port 3002 (Traefik: stg.coreldove.com)
  business-directory:     # ❌ Port 3004 (Traefik: stg.directory.bizoholic.com)
  admin-dashboard:        # ❌ Port 3009 (Traefik: stg.admin.bizoholic.com)
```

**Action**: Create complete frontend config with all 5 services

---

## Image Source Strategy

### Option 1: Build from GitHub (Current Approach)
✅ **Pros**: Automated, CI/CD friendly, version controlled
❌ **Cons**: Build context issues (as we've experienced), slow builds

### Option 2: Push Local Images to Registry (Recommended for Missing Services)
✅ **Pros**: Uses working local images, faster deployment, guaranteed to work
❌ **Cons**: Need to push to Docker Hub or GitHub Container Registry first

### Recommended Hybrid Approach:
1. **Services with GitHub Dockerfiles working**: Use GitHub build context
   - Brain API ✅
   - Saleor ✅
   - Wagtail (after settings fix) ✅
   - Django CRM (after settings fix) ✅

2. **Services WITHOUT GitHub Dockerfiles**: Push local images to registry
   - Business Directory Backend
   - CorelDove Backend
   - Business Directory Frontend
   - Client Portal
   - Admin Dashboard
   - AI Agents
   - Amazon Sourcing
   - Temporal Integration

---

## Immediate Action Plan

### Step 1: Fix Existing Crashing Services (5 minutes)
- Update `dokploy-backend-staging-v2.yml`
- Change `DJANGO_SETTINGS_MODULE` from `.staging` to `.production`
- Redeploy to fix Wagtail and Django CRM

### Step 2: Add Temporal Services to Infrastructure (10 minutes)
- Update `dokploy-infrastructure-staging.yml`
- Add temporal-server (Port 7234→7233)
- Add temporal-ui (Port 8083→8080)
- Deploy infrastructure update

### Step 3: Push Missing Local Images to Registry (30 minutes)
```bash
# Tag and push to GitHub Container Registry
docker tag bizosaas-business-directory-backend:latest ghcr.io/bizoholic-digital/bizosaas-business-directory-backend:staging
docker tag coreldove-backend-coreldove-backend:latest ghcr.io/bizoholic-digital/coreldove-backend:staging
docker tag bizosaas-platform-temporal-integration:latest ghcr.io/bizoholic-digital/temporal-integration:staging
docker tag bizosaas-platform-bizosaas-brain-enhanced:latest ghcr.io/bizoholic-digital/ai-agents:staging
docker tag bizosaas/amazon-sourcing:latest ghcr.io/bizoholic-digital/amazon-sourcing:staging

# Frontend images
docker tag bizoholic-frontend:dev ghcr.io/bizoholic-digital/bizoholic-frontend:staging
docker tag bizosaas-client-portal:latest ghcr.io/bizoholic-digital/client-portal:staging
docker tag bizosaas-coreldove-frontend:latest ghcr.io/bizoholic-digital/coreldove-frontend:staging
docker tag bizosaas-business-directory:latest ghcr.io/bizoholic-digital/business-directory-frontend:staging
docker tag bizosaas-bizosaas-admin:latest ghcr.io/bizoholic-digital/admin-dashboard:staging

# Push all
docker push ghcr.io/bizoholic-digital/...
```

### Step 4: Create Complete Backend Config (15 minutes)
- Add 5 missing backend services to `dokploy-backend-staging-complete.yml`
- Use registry images for services without GitHub Dockerfiles
- Deploy complete backend

### Step 5: Create Complete Frontend Config (15 minutes)
- Create `dokploy-frontend-staging-complete.yml` with all 5 frontend services
- Configure Traefik labels for subdomains
- Deploy frontend

---

## Expected Final State (All 19 Containers Deployed)

### Infrastructure (5 containers)
✅ PostgreSQL, Redis, Vault, Temporal Server, Temporal UI

### Backend (9 containers)
✅ Brain API, Saleor, Wagtail, Django CRM, Business Directory Backend, CorelDove Backend, Temporal Integration, AI Agents, Amazon Sourcing

### Frontend (5 containers)
✅ Bizoholic, Client Portal, CorelDove, Business Directory, Admin Dashboard

**Total: 19 services across 3 Dokploy projects**

---

## Port Mapping Reference (Staging)

| Service | Local Port | Staging Port | Project |
|---------|-----------|--------------|---------|
| PostgreSQL | 5432 | 5433 | Infrastructure |
| Redis | 6379 | 6380 | Infrastructure |
| Vault | 8200 | 8201 | Infrastructure |
| Temporal Server | 7233 | 7234 | Infrastructure |
| Temporal UI | 8082 | 8083 | Infrastructure |
| Saleor API | 8000 | 8000 | Backend |
| Brain API | 8001 | 8001 | Backend |
| Wagtail CMS | 8002 | 8002 | Backend |
| Django CRM | 8003 | 8003 | Backend |
| Business Directory Backend | 8004 | 8004 | Backend |
| CorelDove Backend | 8005 | 8005 | Backend |
| Temporal Integration | 8009 | 8009 | Backend |
| AI Agents | 8010 | 8010 | Backend |
| Amazon Sourcing | 8085 | 8085 | Backend |
| Bizoholic Frontend | 3000 | 3000 | Frontend |
| Client Portal | 3001 | 3001 | Frontend |
| CorelDove Frontend | 3002 | 3002 | Frontend |
| Business Directory Frontend | 3004 | 3004 | Frontend |
| Admin Dashboard | 3009 | 3009 | Frontend |
