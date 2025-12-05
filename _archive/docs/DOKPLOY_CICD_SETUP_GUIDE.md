# 🚀 BizOSaaS Platform - Dokploy CI/CD Setup Guide

**Date**: October 13, 2025
**Workflow**: Local (WSL2) → GitHub → Dokploy (Staging) → Dokploy (Production)

---

## 📋 Table of Contents

1. [Workflow Overview](#workflow-overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: GitHub Setup](#phase-1-github-setup)
4. [Phase 2: Dokploy Staging Configuration](#phase-2-dokploy-staging-configuration)
5. [Phase 3: Dokploy Production Configuration](#phase-3-dokploy-production-configuration)
6. [Phase 4: Testing the CI/CD Flow](#phase-4-testing-the-cicd-flow)
7. [Daily Development Workflow](#daily-development-workflow)
8. [Troubleshooting](#troubleshooting)

---

## Workflow Overview

```
┌──────────────────┐
│   Local WSL2     │ ← Develop & test locally
│   (Docker)       │
└────────┬─────────┘
         │ git push
         ▼
┌──────────────────┐
│     GitHub       │ ← Source of truth
│  main branch     │
└────┬────────┬────┘
     │        │
     │webhook │webhook
     ▼        ▼
┌─────────┐  ┌──────────┐
│ Dokploy │  │ Dokploy  │
│ Staging │  │Production│
│ (auto)  │  │ (manual) │
└─────────┘  └──────────┘
```

**Key Benefits:**
- ✅ Single source of truth (GitHub)
- ✅ Automated staging deployments
- ✅ Manual production control
- ✅ Full version control & audit trail
- ✅ Easy rollbacks
- ✅ Team collaboration ready

---

## Prerequisites

### Already Configured ✅
- [x] GitHub Repository: `Bizoholic-Digital/bizosaas-platform`
- [x] Dokploy Dashboard: `https://dk.bizoholic.com`
- [x] VPS Server: `194.238.16.237`
- [x] Docker Images: 10 services built locally
- [x] Deployment Configs: Backend + Frontend compose files

### Required Access
- GitHub repository access with push permissions
- Dokploy dashboard login credentials
- VPS SSH access (if needed for debugging)

---

## Phase 1: GitHub Setup

### 1.1 Verify Repository Structure

Your repository should have this structure:

```
bizosaas-platform/
├── ai/
│   └── services/
│       └── bizosaas-brain/
│           ├── Dockerfile
│           └── simple_api.py
├── backend/
│   └── services/
│       ├── cms/              # Wagtail
│       ├── crm/
│       │   ├── business-directory/
│       │   └── django-crm/
│       ├── auth/
│       ├── temporal/
│       ├── ai-agents/
│       └── amazon-sourcing/
├── frontend/
│   └── apps/
│       ├── client-portal/
│       ├── bizoholic-frontend/
│       ├── coreldove-frontend/
│       ├── business-directory/
│       └── bizosaas-admin/
├── dokploy-backend-staging-from-images.yml
├── dokploy-frontend-staging-from-images.yml
├── dokploy-backend-production.yml
└── dokploy-frontend-production.yml
```

### 1.2 Push Current Configuration

```bash
cd /home/alagiri/projects/bizoholic

# Add deployment configurations
git add dokploy-*.yml
git add DOKPLOY_CICD_SETUP_GUIDE.md

# Commit
git commit -m "feat: Add Dokploy CI/CD deployment configurations

- Staging configs for 10 services (5 backend + 5 frontend)
- Production configs ready for manual deployment
- Comprehensive CI/CD setup guide
- GitHub → Dokploy workflow implementation"

# Push to GitHub
git push origin main
```

---

## Phase 2: Dokploy Staging Configuration

### 2.1 Create Staging Project

1. **Login to Dokploy**
   - URL: https://dk.bizoholic.com
   - Navigate to Projects

2. **Create New Project**
   - Name: `BizOSaaS Staging`
   - Description: `Automated staging environment for BizOSaaS platform`

### 2.2 Configure Backend Services (5 Services)

For each backend service, create an application:

#### Service 1: Brain API Gateway (Port 8001)

**Application Settings:**
- Name: `brain-api-staging`
- Type: `Docker Compose`
- Git Provider: `GitHub`
- Repository: `Bizoholic-Digital/bizosaas-platform`
- Branch: `main`
- Dockerfile Path: `ai/services/bizosaas-brain/Dockerfile`
- Build Context: `ai/services/bizosaas-brain`

**Environment Variables:**
```env
DATABASE_URL=postgresql://admin:BizOSaaS2025!StagingDB@194.238.16.237:5433/bizosaas_staging
REDIS_URL=redis://194.238.16.237:6380/0
ENVIRONMENT=staging
LOG_LEVEL=INFO
```

**Port Mapping:**
- Container Port: `8001`
- Host Port: `8001`

**Auto Deploy:** ✅ Enabled (deploy on git push)

**Health Check:**
- Endpoint: `/health`
- Interval: 30s

---

#### Service 2: Wagtail CMS (Port 8002)

**Application Settings:**
- Name: `wagtail-cms-staging`
- Repository: `Bizoholic-Digital/bizosaas-platform`
- Branch: `main`
- Dockerfile Path: `backend/services/cms/Dockerfile`
- Build Context: `backend/services/cms`

**Environment Variables:**
```env
DJANGO_SETTINGS_MODULE=wagtail_cms.settings.production
DATABASE_URL=postgresql://admin:BizOSaaS2025!StagingDB@194.238.16.237:5433/bizosaas_staging
REDIS_URL=redis://194.238.16.237:6380/3
SECRET_KEY=staging-secret-key-wagtail-bizosaas-2025
ALLOWED_HOSTS=194.238.16.237,stg-cms.bizoholic.com,0.0.0.0
DEBUG=False
```

**Port Mapping:**
- Container Port: `8000`
- Host Port: `8002`

**Auto Deploy:** ✅ Enabled

---

#### Service 3: Business Directory Backend (Port 8004)

**Application Settings:**
- Name: `business-directory-backend-staging`
- Dockerfile Path: `backend/services/crm/business-directory/Dockerfile`
- Build Context: `backend/services/crm/business-directory`

**Environment Variables:**
```env
DATABASE_URL=postgresql://admin:BizOSaaS2025!StagingDB@194.238.16.237:5433/bizosaas_staging
REDIS_URL=redis://194.238.16.237:6380/5
SECRET_KEY=staging-secret-key-bizdir-bizosaas-2025
ENVIRONMENT=staging
```

**Port Mapping:**
- Container Port: `8000`
- Host Port: `8004`

---

#### Service 4: Temporal Integration (Port 8007)

**Application Settings:**
- Name: `temporal-integration-staging`
- Dockerfile Path: `backend/services/temporal/Dockerfile`
- Build Context: `backend/services/temporal`

**Environment Variables:**
```env
DATABASE_URL=postgresql://admin:BizOSaaS2025!StagingDB@194.238.16.237:5433/bizosaas_staging
REDIS_URL=redis://194.238.16.237:6380/7
TEMPORAL_HOST=bizosaas-temporal-server-staging
TEMPORAL_PORT=7233
ENVIRONMENT=staging
```

**Port Mapping:**
- Container Port: `8000`
- Host Port: `8007`

---

#### Service 5: Amazon Sourcing (Port 8009)

**Application Settings:**
- Name: `amazon-sourcing-staging`
- Dockerfile Path: `backend/services/amazon-sourcing/Dockerfile`
- Build Context: `backend/services/amazon-sourcing`

**Environment Variables:**
```env
DATABASE_URL=postgresql://admin:BizOSaaS2025!StagingDB@194.238.16.237:5433/bizosaas_staging
REDIS_URL=redis://194.238.16.237:6380/9
ENVIRONMENT=staging
```

**Port Mapping:**
- Container Port: `8000`
- Host Port: `8009`

---

### 2.3 Configure Frontend Services (5 Services)

#### Service 6: Client Portal (Port 3000)

**Application Settings:**
- Name: `client-portal-staging`
- Dockerfile Path: `frontend/apps/client-portal/Dockerfile`
- Build Context: `frontend/apps/client-portal`

**Environment Variables:**
```env
NODE_ENV=production
NEXT_PUBLIC_API_BASE_URL=http://194.238.16.237:8001
NEXT_PUBLIC_CRM_API_URL=http://194.238.16.237:8000
NEXT_PUBLIC_CMS_API_URL=http://194.238.16.237:8002
NEXT_TELEMETRY_DISABLED=1
```

**Port Mapping:**
- Container Port: `3000`
- Host Port: `3000`

---

#### Service 7: Bizoholic Frontend (Port 3001)

**Application Settings:**
- Name: `bizoholic-frontend-staging`
- Dockerfile Path: `frontend/apps/bizoholic-frontend/Dockerfile`
- Build Context: `frontend/apps/bizoholic-frontend`

**Environment Variables:**
```env
NODE_ENV=production
NEXT_PUBLIC_API_BASE_URL=http://194.238.16.237:8001
NEXT_PUBLIC_CMS_API_URL=http://194.238.16.237:8002
NEXT_TELEMETRY_DISABLED=1
```

**Port Mapping:**
- Container Port: `3000`
- Host Port: `3001`

---

#### Service 8: CorelDove Frontend (Port 3002)

**Application Settings:**
- Name: `coreldove-frontend-staging`
- Dockerfile Path: `frontend/apps/coreldove-frontend/Dockerfile`
- Build Context: `frontend/apps/coreldove-frontend`

**Environment Variables:**
```env
NODE_ENV=production
NEXT_PUBLIC_API_BASE_URL=http://194.238.16.237:8001
NEXT_TELEMETRY_DISABLED=1
```

**Port Mapping:**
- Container Port: `3000`
- Host Port: `3002`

---

#### Service 9: Business Directory Frontend (Port 3003)

**Application Settings:**
- Name: `business-directory-frontend-staging`
- Dockerfile Path: `frontend/apps/business-directory/Dockerfile`
- Build Context: `frontend/apps/business-directory`

**Environment Variables:**
```env
NODE_ENV=production
NEXT_PUBLIC_API_BASE_URL=http://194.238.16.237:8001
NEXT_PUBLIC_DIRECTORY_API_URL=http://194.238.16.237:8004
NEXT_TELEMETRY_DISABLED=1
```

**Port Mapping:**
- Container Port: `3000`
- Host Port: `3003`

---

#### Service 10: Admin Dashboard (Port 3005)

**Application Settings:**
- Name: `admin-dashboard-staging`
- Dockerfile Path: `frontend/apps/bizosaas-admin/Dockerfile`
- Build Context: `frontend/apps/bizosaas-admin`

**Environment Variables:**
```env
NODE_ENV=production
NEXT_PUBLIC_API_BASE_URL=http://194.238.16.237:8001
NEXT_TELEMETRY_DISABLED=1
```

**Port Mapping:**
- Container Port: `3000`
- Host Port: `3005`

---

### 2.4 Configure GitHub Webhooks

Dokploy should automatically configure webhooks when you connect GitHub. Verify:

1. Go to GitHub Repository Settings → Webhooks
2. Look for webhook pointing to `https://dk.bizoholic.com/api/webhook/...`
3. Ensure it's active and has "push" events enabled

---

## Phase 3: Dokploy Production Configuration

### 3.1 Create Production Project

1. **Create New Project**
   - Name: `BizOSaaS Production`
   - Description: `Production environment - manual deployments only`

### 3.2 Configure Production Services

**Same configuration as staging BUT:**

1. **Different Ports:**
   - Backend: 9001-9009 (instead of 8001-8009)
   - Frontend: 4000-4005 (instead of 3000-3005)

2. **Different Environment:**
   - `ENVIRONMENT=production`
   - Production database credentials
   - Production API keys

3. **Auto Deploy:** ❌ **DISABLED** (manual deployments only)

4. **Domains:**
   - Configure proper domain names:
     - `api.bizoholic.com` → Brain API
     - `cms.bizoholic.com` → Wagtail
     - `bizoholic.com` → Client Portal
     - etc.

5. **SSL Certificates:**
   - Enable Let's Encrypt SSL for all domains
   - Dokploy handles auto-renewal

---

## Phase 4: Testing the CI/CD Flow

### 4.1 Test Staging Auto-Deployment

```bash
# Make a small test change
echo "# Test deployment" >> README.md

# Commit and push
git add README.md
git commit -m "test: Verify CI/CD staging deployment"
git push origin main

# Monitor Dokploy dashboard
# You should see staging services rebuilding automatically
```

### 4.2 Verify Staging Deployment

```bash
# Test Backend Services
curl http://194.238.16.237:8001/health  # Brain API
curl http://194.238.16.237:8002/        # Wagtail CMS
curl http://194.238.16.237:8004/        # Business Directory
curl http://194.238.16.237:8007/        # Temporal
curl http://194.238.16.237:8009/        # Amazon Sourcing

# Test Frontend Services (in browser)
http://194.238.16.237:3000  # Client Portal
http://194.238.16.237:3001  # Bizoholic Frontend
http://194.238.16.237:3002  # CorelDove Frontend
http://194.238.16.237:3003  # Business Directory Frontend
http://194.238.16.237:3005  # Admin Dashboard
```

### 4.3 Test Production Manual Deployment

1. Login to Dokploy dashboard
2. Navigate to Production project
3. Select a service
4. Click "Deploy" button
5. Monitor build logs
6. Test production endpoints

---

## Daily Development Workflow

### Developer Workflow

```bash
# 1. Start local development
cd /home/alagiri/projects/bizoholic
docker-compose -f dokploy-backend-staging-from-images.yml up -d
docker-compose -f dokploy-frontend-staging-from-images.yml up -d

# 2. Develop and test locally
# Make your code changes
# Test: curl http://localhost:8001/health

# 3. Commit changes
git add .
git commit -m "feat: Add new feature"

# 4. Push to GitHub (triggers staging deployment)
git push origin main

# 5. Monitor Dokploy staging
# Open: https://dk.bizoholic.com
# Watch build logs and deployment status

# 6. Test on staging
curl http://194.238.16.237:8001/health

# 7. If staging tests pass, deploy to production manually
# Dokploy Dashboard → Production Project → Deploy button
```

### Hotfix Workflow

```bash
# 1. Create hotfix branch
git checkout -b hotfix/critical-bug

# 2. Fix the bug
# Make necessary changes

# 3. Test locally
docker-compose up -d
# Test the fix

# 4. Merge to main
git checkout main
git merge hotfix/critical-bug
git push origin main

# 5. Staging auto-deploys (verify fix)
curl http://194.238.16.237:8001/health

# 6. Deploy to production immediately
# Dokploy Dashboard → Production → Deploy
```

---

## Troubleshooting

### Issue 1: Staging Not Auto-Deploying

**Symptoms:** Push to GitHub but Dokploy staging doesn't rebuild

**Solutions:**
1. Check GitHub webhook status: Repository Settings → Webhooks
2. Verify webhook deliveries show successful responses
3. Check Dokploy logs for webhook received
4. Manually trigger deployment to verify build works

### Issue 2: Build Failures

**Symptoms:** Dokploy shows build failed

**Solutions:**
1. Check build logs in Dokploy dashboard
2. Verify Dockerfile paths are correct
3. Ensure all dependencies are in repository
4. Test build locally: `docker build -f path/to/Dockerfile .`

### Issue 3: Service Won't Start

**Symptoms:** Build succeeds but container crashes

**Solutions:**
1. Check container logs in Dokploy
2. Verify environment variables are set correctly
3. Check database/Redis connectivity
4. Verify port mappings don't conflict

### Issue 4: Cannot Access Services

**Symptoms:** Services running but not accessible

**Solutions:**
1. Check VPS firewall: `sudo ufw status`
2. Open required ports: `sudo ufw allow 8001/tcp` (etc.)
3. Verify services listening on 0.0.0.0 not 127.0.0.1
4. Check Docker port mappings: `docker ps`

---

## Success Metrics

### Staging Environment
- ✅ 10/10 services deployed from GitHub
- ✅ Auto-deploy triggers on git push
- ✅ All services accessible externally
- ✅ Health checks passing
- ✅ Database connections working

### Production Environment
- ✅ Manual deployment control
- ✅ SSL certificates configured
- ✅ Custom domains working
- ✅ Monitoring and alerts active
- ✅ Backup strategy in place

---

## Next Steps

1. **Complete Dokploy Configuration** (Phase 2 & 3)
2. **Test CI/CD Flow** (Phase 4)
3. **Configure Custom Domains** for production
4. **Set Up Monitoring** (Dokploy built-in + external)
5. **Create Backup Strategy** for databases
6. **Document Runbooks** for common operations

---

## Support & Resources

- **Dokploy Dashboard:** https://dk.bizoholic.com
- **GitHub Repository:** https://github.com/Bizoholic-Digital/bizosaas-platform
- **VPS Server:** 194.238.16.237
- **Documentation:** This file + deployment configs

---

**Last Updated:** October 13, 2025
**Status:** Ready for implementation
**Next Action:** Configure Dokploy staging project (Phase 2)
