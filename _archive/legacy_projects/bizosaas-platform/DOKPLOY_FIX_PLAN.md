# BizOSaaS Platform - Dokploy Fix & Deploy Plan

**Current Status**: 6/22 services running (27%)
**Goal**: Get all 23 services running (100%)

## Root Causes Identified

### 1. **Saleor Platform**: Missing Environment Variable
**Error**: `ALLOWED_CLIENT_HOSTS environment variable must be set when DEBUG=False`
**Fix**: Add missing environment variable in Dokploy

### 2. **Wagtail CMS**: Logging Configuration Issue
**Error**: `ValueError: Unable to configure handler 'file'`
**Fix**: Add volume mount or adjust logging configuration

### 3. **Infrastructure**: Saleor PostgreSQL & Redis not starting
**Likely Cause**: Port conflicts or missing network configuration
**Fix**: Verify configuration and restart

### 4. **Frontend Services**: Configured but not deployed
**Issue**: Applications exist in Dokploy but not running
**Fix**: Trigger deployment for each service

## Step-by-Step Fix Plan

### Phase 1: Fix Infrastructure Services (5 minutes)

#### 1.1 Fix Saleor PostgreSQL
```bash
# Via SSH
ssh root@72.60.219.244
docker service rm infrastructureservices-saleorpostgres-las0jw
docker service rm infrastructureservices-saleorredis-qrl0jc
```

**In Dokploy UI**:
1. Navigate to Infrastructure → Staging
2. Find Saleor PostgreSQL service
3. Check environment variables
4. Verify ports: PostgreSQL (5433), Redis (6381 - not 6379 to avoid conflict)
5. Click **"Deploy"** to restart

### Phase 2: Fix Backend Services (20 minutes)

#### 2.1 Fix Saleor Platform
**Via Dokploy UI**:
1. Go to Backend → Staging → Saleor Platform
2. Click **"Environment"** tab
3. Add missing variable:
   ```
   ALLOWED_CLIENT_HOSTS=72.60.219.244,localhost,stg.coreldove.com
   ```
4. Click **"Save"** → **"Deploy"**

#### 2.2 Fix Wagtail CMS
**Via Dokploy UI**:
1. Go to Backend → Staging → Wagtail CMS
2. Click **"Environment"** tab
3. Add/verify variables:
   ```
   DJANGO_SETTINGS_MODULE=wagtail_cms.settings.production
   DATABASE_URL=postgresql://admin:BizOSaaS2025!StagingDB@shared-postgres:5432/bizosaas_staging
   REDIS_URL=redis://bizosaas-redis:6379/3
   SECRET_KEY=staging-secret-key-wagtail-bizosaas-2025
   DEBUG=False
   ```
4. Click **"Advanced"** tab
5. Add volume mount for logs:
   ```
   /var/log/wagtail:/app/logs
   ```
6. Click **"Save"** → **"Deploy"**

#### 2.3 Fix Django CRM
**Via Dokploy UI**:
1. Go to Backend → Staging → Django CRM
2. Verify environment variables:
   ```
   DJANGO_SETTINGS_MODULE=crm_project.settings.production
   DATABASE_URL=postgresql://admin:BizOSaaS2025!StagingDB@shared-postgres:5432/bizosaas_staging
   REDIS_URL=redis://bizosaas-redis:6379/4
   SECRET_KEY=staging-secret-key-djangocrm-bizosaas-2025
   DEBUG=False
   ```
3. Click **"Deploy"**

#### 2.4 Fix Business Directory Backend
**Via Dokploy UI**:
1. Go to Backend → Staging → Business Directory
2. Verify environment variables:
   ```
   DATABASE_URL=postgresql://admin:BizOSaaS2025!StagingDB@shared-postgres:5432/bizosaas_staging
   REDIS_URL=redis://bizosaas-redis:6379/5
   ```
3. Click **"Deploy"**

#### 2.5 Fix CorelDove Backend
**Via Dokploy UI**:
1. Go to Backend → Staging → CorelDove Backend
2. Verify environment variables:
   ```
   DATABASE_URL=postgresql://admin:BizOSaaS2025!StagingDB@shared-postgres:5432/bizosaas_staging
   REDIS_URL=redis://bizosaas-redis:6379/6
   SALEOR_API_URL=http://saleor-platform:8000/graphql/
   ```
3. Click **"Deploy"**

#### 2.6 Fix AI Agents
**Via Dokploy UI**:
1. Go to Backend → Staging → AI Agents
2. Verify environment variables:
   ```
   DATABASE_URL=postgresql://admin:BizOSaaS2025!StagingDB@shared-postgres:5432/bizosaas_staging
   REDIS_URL=redis://bizosaas-redis:6379/8
   BRAIN_API_URL=http://brain-gateway:8001
   OPENAI_API_KEY=<your-key>
   ```
3. Click **"Deploy"**

### Phase 3: Deploy Missing Backend Services (15 minutes)

#### 3.1 Deploy Auth Service
**Via Dokploy UI**:
1. Go to Backend → Staging
2. Click **"Create Application"**
3. Select **"Application" (not Compose)**
4. Configure:
   - Name: `auth-service`
   - Source: Git Repository
   - Repo: `https://github.com/Bizoholic-Digital/bizosaas-platform.git`
   - Branch: `main`
   - Build Path: `bizosaas-platform/backend/services/auth-service`
   - Dockerfile Path: `Dockerfile`
   - Port: `8007`
5. Add environment variables:
   ```
   DATABASE_URL=postgresql://admin:BizOSaaS2025!StagingDB@shared-postgres:5432/bizosaas_staging
   REDIS_URL=redis://bizosaas-redis:6379/10
   SECRET_KEY=staging-secret-key-auth-bizosaas-2025
   JWT_SECRET=staging-jwt-secret-bizosaas-2025
   ```
6. Click **"Deploy"**

#### 3.2 Deploy QuantTrade Backend
**Via Dokploy UI**:
1. Go to Backend → Staging
2. Click **"Create Application"**
3. Configure similar to Auth Service
4. Build Path: `bizosaas-platform/backend/services/quanttrade-backend`
5. Port: `8012`
6. Click **"Deploy"**

### Phase 4: Deploy Frontend Services (30 minutes)

#### 4.1 Deploy Admin Dashboard
**Via Dokploy UI**:
1. Go to Frontend → Staging → Admin Dashboard (admin-dashboard-07uryq)
2. Verify configuration:
   - Build Path: `bizosaas-platform/frontend/apps/bizosaas-admin`
   - Port: `3009`
3. Verify environment variables:
   ```
   NODE_ENV=production
   NEXT_PUBLIC_API_BASE_URL=http://brain-gateway:8001
   NEXT_PUBLIC_SUPERSET_URL=http://superset:8088
   NEXT_PUBLIC_TEMPORAL_UI_URL=http://temporal-ui:8080
   NEXT_TELEMETRY_DISABLED=1
   BASE_PATH=/admin
   ```
4. Click **"Deploy"**

#### 4.2 Deploy Client Portal
**Via Dokploy UI**:
1. Go to Frontend → Staging → Client Portal (client-portal-cj6nnf)
2. Verify configuration:
   - Build Path: `bizosaas-platform/frontend/apps/client-portal`
   - Port: `3001`
3. Add environment variables:
   ```
   NODE_ENV=production
   NEXT_PUBLIC_API_BASE_URL=http://brain-gateway:8001
   NEXT_TELEMETRY_DISABLED=1
   BASE_PATH=/login
   ```
4. Click **"Deploy"**

#### 4.3 Deploy CorelDove Frontend
**Via Dokploy UI**:
1. Go to Frontend → Staging → CorelDove Frontend (coreldove-frontend-5q0q5r)
2. Verify configuration:
   - Build Path: `bizosaas-platform/frontend/apps/coreldove-frontend`
   - Port: `3002`
3. Add environment variables:
   ```
   NODE_ENV=production
   NEXT_PUBLIC_API_BASE_URL=http://brain-gateway:8001
   NEXT_PUBLIC_SALEOR_API_URL=http://saleor-platform:8000/graphql/
   NEXT_TELEMETRY_DISABLED=1
   ```
4. Click **"Deploy"**

#### 4.4 Deploy ThrillRing Frontend
**Via Dokploy UI**:
1. Go to Frontend → Staging → ThrillRing Frontend (thrillring-frontend-fpe6rp)
2. Verify configuration:
   - Build Path: `bizosaas-platform/frontend/apps/thrillring-gaming`
   - Port: `3005`
3. Add environment variables:
   ```
   NODE_ENV=production
   NEXT_PUBLIC_API_BASE_URL=http://brain-gateway:8001
   NEXT_TELEMETRY_DISABLED=1
   ```
4. Click **"Deploy"**

#### 4.5 Deploy Business Directory Frontend
**Via Dokploy UI**:
1. Go to Frontend → Staging
2. Click **"Create Application"**
3. Configure:
   - Name: `business-directory-frontend`
   - Build Path: `bizosaas-platform/frontend/apps/business-directory-frontend`
   - Port: `3003`
4. Add environment variables:
   ```
   NODE_ENV=production
   NEXT_PUBLIC_API_BASE_URL=http://brain-gateway:8001
   NEXT_TELEMETRY_DISABLED=1
   BASE_PATH=/directory
   ```
5. Click **"Deploy"**

#### 4.6 Deploy QuantTrade Frontend
**Via Dokploy UI**:
1. Go to Frontend → Staging
2. Click **"Create Application"**
3. Configure similar to Business Directory
4. Build Path: `bizosaas-platform/frontend/apps/quanttrade-frontend`
5. Port: `3012`
6. Click **"Deploy"**

### Phase 5: Configure Routing (10 minutes)

After all services are deployed, configure Traefik routing:

#### 5.1 Main Domains
**Via Dokploy UI - Domains Tab**:

For **Bizoholic Frontend**:
- Domain: `stg.bizoholic.com`
- Port: `3000`
- SSL: ✓ Let's Encrypt

For **CorelDove Frontend**:
- Domain: `stg.coreldove.com`
- Port: `3002`
- SSL: ✓ Let's Encrypt

For **ThrillRing Frontend**:
- Domain: `stg.thrillring.com`
- Port: `3005`
- SSL: ✓ Let's Encrypt

#### 5.2 Subdirectory Routes
**Via Traefik Configuration** (if not auto-configured by labels):

These should route as subdirectories of `stg.bizoholic.com`:
- `/login/` → Client Portal (Port 3001)
- `/admin/` → Admin Dashboard (Port 3009)
- `/directory/` → Business Directory (Port 3003)

## Verification Checklist

### Infrastructure (6 services)
- [ ] Shared PostgreSQL (running)
- [ ] BizOSaaS Redis (running)
- [ ] PostgreSQL Backup (running)
- [ ] Saleor PostgreSQL (fix & restart)
- [ ] Saleor Redis (fix & restart)
- [ ] Temporal UI (running)

### Backend (10 services)
- [ ] Brain Gateway (running)
- [ ] Amazon Sourcing (running)
- [ ] Wagtail CMS (fix & restart)
- [ ] Django CRM (fix & restart)
- [ ] Business Directory (fix & restart)
- [ ] CorelDove Backend (fix & restart)
- [ ] AI Agents (fix & restart)
- [ ] Saleor Platform (fix & restart)
- [ ] Auth Service (deploy new)
- [ ] QuantTrade Backend (deploy new)

### Frontend (7 services)
- [ ] Bizoholic Frontend (running)
- [ ] Admin Dashboard (deploy)
- [ ] Client Portal (deploy)
- [ ] CorelDove Frontend (deploy)
- [ ] ThrillRing Frontend (deploy)
- [ ] Business Directory Frontend (deploy new)
- [ ] QuantTrade Frontend (deploy new)

## Estimated Timeline

| Phase | Time | Services |
|-------|------|----------|
| Phase 1: Infrastructure | 5 min | 2 services |
| Phase 2: Fix Backends | 20 min | 6 services |
| Phase 3: Deploy Backends | 15 min | 2 services |
| Phase 4: Deploy Frontends | 30 min | 6 services |
| Phase 5: Configure Routing | 10 min | All services |
| **Total** | **80 min** | **23 services** |

## Quick Commands for Verification

### Check all services status:
```bash
ssh root@72.60.219.244 "docker service ls --format 'table {{.Name}}\t{{.Replicas}}\t{{.Image}}'"
```

### Check specific service logs:
```bash
ssh root@72.60.219.244 "docker service logs <service-name> --tail 50"
```

### Health check endpoints:
```bash
# Infrastructure
curl http://72.60.219.244:8083  # Temporal UI

# Backend
curl http://72.60.219.244:8001/health  # Brain Gateway
curl http://72.60.219.244:8000/health/  # Saleor
curl http://72.60.219.244:8002/admin/  # Wagtail
curl http://72.60.219.244:8003/admin/  # Django CRM

# Frontend
curl -I https://stg.bizoholic.com
curl -I https://stg.coreldove.com
curl -I https://stg.thrillring.com
```

---

**Note**: This plan assumes you want to keep the existing Dokploy structure (3 projects: infrastructure, backend, frontend). Alternatively, you could deploy everything fresh using `dokploy-staging-complete.yml` which would be faster but would require removing existing services first.
