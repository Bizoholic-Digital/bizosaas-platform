# Complete BizOSaaS Staging Deployment Instructions

## Current Status: 62% Complete (13/21 containers)

---

## 🚀 IMMEDIATE ACTIONS REQUIRED

### Step 1: Deploy Superset (Infrastructure) - **DO THIS NOW**

**Via Dokploy UI:**
1. Go to: `https://dk.bizoholic.com`
2. Navigate to Projects → **Infrastructure** (or **backend-services-azbmbl** if no separate infra project)
3. Settings → Compose File: `dokploy-infrastructure-staging.yml`
4. Click: **Deploy** button
5. Wait: 3-5 minutes for deployment
6. Verify: Check that Superset container is running

**Expected Result:**
- New container: `bizosaas-superset-staging` on port 8088
- Access: `http://194.238.16.237:8088`
- Login: `admin` / `Bizoholic2024Admin`

---

### Step 2: Fix Registry Authentication

**Option A: Use Existing GitHub Token**
```bash
# If you have a GitHub PAT with packages:write scope
docker login ghcr.io
# Username: your-github-username
# Password: ghp_REDACTED
```

**Option B: Create New Token**
1. Go to: https://github.com/settings/tokens/new
2. Name: `BizOSaaS Registry Push`
3. Expiration: 90 days
4. Scopes: Check **`write:packages`** and **`read:packages`**
5. Click: **Generate token**
6. Copy token (starts with `ghp_`)
7. Run: `docker login ghcr.io`
8. Username: `Bizoholic-Digital` (or your GitHub username)
9. Password: Paste the token

---

### Step 3: Push All Images to Registry

Once authenticated, run:
```bash
cd /home/alagiri/projects/bizoholic
./setup-registry-and-push-all.sh
```

This will push **14 images** (Superset already pushed):
- 8 Backend images
- 6 Frontend images

**Expected Time**: 30-60 minutes (large images)

---

## 📋 Alternative: Deploy Without Registry (Faster)

If registry push is problematic, we can build images directly on VPS:

### Option 1: Build on VPS from GitHub
```bash
ssh root@194.238.16.237
cd /path/to/compose/directory

# Build from GitHub repository
docker-compose -f dokploy-backend-staging-complete-all9.yml build
docker-compose -f dokploy-backend-staging-complete-all9.yml up -d
```

### Option 2: Save and Transfer Images
```bash
# On local machine
docker save bizosaas-business-directory-backend:latest | gzip > business-directory-backend.tar.gz
scp business-directory-backend.tar.gz root@194.238.16.237:/tmp/

# On VPS
ssh root@194.238.16.237
cd /tmp
gunzip -c business-directory-backend.tar.gz | docker load
```

---

## 🎯 Deployment Order

### Phase 1: Infrastructure (6 services) - **IN PROGRESS**
- [x] PostgreSQL - Running
- [x] Redis - Running
- [x] Vault - Running
- [ ] Temporal Server - Needs config fix
- [x] Temporal UI - Running
- [ ] **Superset - DEPLOY NOW** ⬅️ **YOU ARE HERE**

### Phase 2: Backend (9 services) - **44% Complete**
- [x] Saleor API - Running
- [x] Brain API - Running
- [x] Wagtail CMS - Running (fixed)
- [x] Django CRM - Running (fixed)
- [ ] Business Directory Backend - Needs image
- [ ] CorelDove Backend - Needs image
- [ ] Temporal Integration - Needs image
- [ ] AI Agents - Needs image
- [ ] Amazon Sourcing - Needs image

### Phase 3: Frontend (6 services) - **0% Complete**
- [ ] Bizoholic Frontend - Needs image
- [ ] Client Portal - Needs image
- [ ] CorelDove Frontend - Needs image
- [ ] Business Directory Frontend - Needs image
- [ ] ThrillRing Gaming - Needs image/code
- [ ] Admin Dashboard - Needs image

---

## 📊 Service Dependencies

```
Infrastructure (Foundation)
├── PostgreSQL ✅
├── Redis ✅
├── Vault ✅
├── Temporal Server ⚠️
├── Temporal UI ✅
└── Superset ⏳ DEPLOYING

Backend Services (Depend on Infrastructure)
├── Saleor API ✅
├── Brain API ✅
├── Wagtail CMS ✅
├── Django CRM ✅
├── Business Directory Backend ❌
├── CorelDove Backend ❌
├── Temporal Integration ❌
├── AI Agents ❌
└── Amazon Sourcing ❌

Frontend Services (Depend on Backend)
├── Bizoholic Frontend ❌
├── Client Portal ❌
├── CorelDove Frontend ❌
├── Business Directory Frontend ❌
├── ThrillRing Gaming ❌
└── Admin Dashboard ❌
```

---

## 🔧 Troubleshooting

### If Superset Deployment Fails
```bash
# Check logs
ssh root@194.238.16.237
docker logs bizosaas-superset-staging -f

# Common issues:
# 1. Database not ready - wait 2 minutes and restart
docker restart bizosaas-superset-staging

# 2. Permission errors - check volume permissions
docker exec bizosaas-superset-staging ls -la /app/superset_home
```

### If Registry Push Fails
```bash
# Check authentication
docker logout ghcr.io
docker login ghcr.io

# Retry push
./setup-registry-and-push-all.sh
```

### If Backend Services Don't Start
```bash
# Check database connections
ssh root@194.238.16.237
docker exec bizosaas-postgres-staging psql -U admin -l

# Check backend logs
docker logs bizosaas-brain-staging
docker logs bizosaas-saleor-staging
```

---

## ✅ Success Criteria

### Infrastructure Complete
- [ ] All 6 containers running
- [ ] All healthy (except Temporal Server)
- [ ] Superset accessible at :8088
- [ ] Can login to Superset

### Backend Complete
- [ ] All 9 containers running
- [ ] All healthy
- [ ] Brain API responding at :8001
- [ ] Saleor API responding at :8000
- [ ] Django CRM responding at :8003
- [ ] Wagtail responding at :8002
- [ ] All other services responding

### Frontend Complete
- [ ] All 6 containers running
- [ ] All accessible via their ports
- [ ] Traefik routing working
- [ ] SSL certificates generated
- [ ] All domains resolving

---

## 📞 What to Share

After each deployment step, please share:

1. **Dokploy deployment output** (copy full text)
2. **Container status**:
   ```bash
   ssh root@194.238.16.237
   docker ps --filter 'name=bizosaas' --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
   ```
3. **Any error messages** from logs

---

## 🎯 Priority Actions (RIGHT NOW)

1. **Deploy Superset** (Step 1 above) - 5 minutes
2. **Share deployment output** - 1 minute
3. **Authenticate with registry** (Step 2 above) - 2 minutes
4. **Push all images** (Step 3 above) - 30-60 minutes (can run in background)

**Total Active Time**: 8 minutes
**Total Background Time**: 30-60 minutes

---

*Last Updated: 2025-10-12 12:50 UTC*
