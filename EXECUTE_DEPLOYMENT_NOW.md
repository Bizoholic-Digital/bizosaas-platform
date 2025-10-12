# 🚀 Execute VPS Staging Deployment - Step-by-Step Instructions

**Start Time**: Record when you begin
**Estimated Total Time**: 1-1.5 hours
**Target**: Deploy 12 remaining services (from 9/21 to 21/21)

---

## 📋 Pre-Deployment Checklist

- [ ] Dokploy accessible at https://dk.bizoholic.com
- [ ] Can login to Dokploy
- [ ] Have the 3 deployment config files ready
- [ ] VPS SSH access working: `ssh root@194.238.16.237`

---

## 🎯 PHASE 1: Deploy Infrastructure with Superset (8-12 minutes)

### Step 1.1: Open Infrastructure Project in Dokploy

1. Open browser: `https://dk.bizoholic.com`
2. Login to Dokploy
3. Navigate to: **Projects** (left sidebar)
4. Find project: **Infrastructure** or **backend-services-azbmbl**
5. Click to open the project

### Step 1.2: Update Compose Configuration

1. In project view, click: **Settings** tab
2. Find section: **Compose File** or **Docker Compose**
3. You'll see current compose configuration
4. Click: **Edit** or directly in text area

### Step 1.3: Replace with New Configuration

**ACTION**: Copy the entire content from this file:
```
/home/alagiri/projects/bizoholic/dokploy-infrastructure-staging-with-superset-build.yml
```

**TO**: Dokploy compose editor (replace ALL existing content)

### Step 1.4: Deploy Infrastructure

1. After pasting, scroll down
2. Click: **Deploy** button (usually green)
3. Dokploy will show deployment progress
4. **Wait 8-12 minutes** for deployment to complete

### Step 1.5: Monitor Deployment Progress

**Watch for these messages in Dokploy logs**:
```
✓ Pulling postgres... done
✓ Pulling redis... done
✓ Pulling vault... done
✓ Pulling temporal-server... done
✓ Pulling temporal-ui... done
Building superset... (this takes 5-7 minutes)
✓ Building superset... done
Creating containers...
✓ Started bizosaas-postgres-staging
✓ Started bizosaas-redis-staging
✓ Started bizosaas-vault-staging
✓ Started bizosaas-temporal-server-staging
✓ Started bizosaas-temporal-ui-staging
✓ Started bizosaas-superset-staging
```

### Step 1.6: Verify Infrastructure Deployment

**Run this command locally**:
```bash
./check-complete-staging.sh
```

**Expected output**:
```
Infrastructure:  6/6   ✅
Backend:         4/9   ⚠️
Frontend:        0/6   ⚠️
Total:           10/21  (47%)
```

**Test Superset access**:
1. Open browser: `http://194.238.16.237:8088`
2. Should see Superset login page
3. Login: `admin` / `Bizoholic2024Admin`
4. Should access Superset dashboard

**✅ PHASE 1 COMPLETE when**:
- [ ] 6/6 infrastructure containers running
- [ ] Superset UI loads and login works
- [ ] No containers in restart loop

**⏱️ Checkpoint 1**: Record time taken for Phase 1: _____ minutes

---

## 🎯 PHASE 2: Deploy Complete Backend (20-30 minutes)

### Step 2.1: Create or Open Backend Project

**Option A - If Backend Project Exists**:
1. In Dokploy, navigate to: **Projects**
2. Find project: **Backend Services** or similar
3. Click to open

**Option B - If No Backend Project**:
1. Click: **Create New Project**
2. Name: `Backend Services Staging`
3. Click: **Create**

### Step 2.2: Add/Update Backend Configuration

1. In project view, go to: **Settings** tab
2. Find: **Compose File** section
3. Click: **Edit**

### Step 2.3: Paste Backend Configuration

**ACTION**: Copy the entire content from this file:
```
/home/alagiri/projects/bizoholic/dokploy-backend-staging-complete-build.yml
```

**TO**: Dokploy compose editor (replace ALL existing content)

### Step 2.4: Deploy Backend Services

1. Click: **Deploy** button
2. Dokploy will start building all 9 services from GitHub
3. **Wait 20-30 minutes** for builds to complete

### Step 2.5: Monitor Backend Build Progress

**What's happening**:
- Dokploy builds services in parallel
- Each service takes 5-7 minutes to build from GitHub
- Total ~20-30 minutes due to parallelization

**Watch for in logs**:
```
Building brain-api...
Building wagtail-cms...
Building django-crm...
Building business-directory-backend...
Building coreldove-backend...
Building temporal-integration...
Building ai-agents...
Building amazon-sourcing...
Pulling saleor-api... (uses pre-built image)

✓ All builds completed
Creating containers...
✓ Started all 9 backend services
```

### Step 2.6: Verify Backend Deployment

**Run health check**:
```bash
./check-complete-staging.sh
```

**Expected output**:
```
Infrastructure:  6/6   ✅
Backend:         9/9   ✅
Frontend:        0/6   ⚠️
Total:           15/21  (71%)
```

**Test backend APIs**:
```bash
# From local machine
curl http://194.238.16.237:8001/health  # Brain API
curl http://194.238.16.237:8000/health/  # Saleor
curl http://194.238.16.237:8004/health  # Business Directory (NEW)
curl http://194.238.16.237:8005/health  # CorelDove Backend (NEW)
curl http://194.238.16.237:8008/health  # AI Agents (NEW)
```

**✅ PHASE 2 COMPLETE when**:
- [ ] 9/9 backend containers running
- [ ] All backend APIs respond to health checks
- [ ] No containers in restart loop for 2 minutes

**⏱️ Checkpoint 2**: Record time taken for Phase 2: _____ minutes

---

## 🎯 PHASE 3: Deploy Complete Frontend (30-45 minutes)

### Step 3.1: Create Frontend Project

1. In Dokploy, navigate to: **Projects**
2. Click: **Create New Project**
3. Name: `Frontend Applications Staging`
4. Click: **Create**

### Step 3.2: Add Frontend Configuration

1. Open the new Frontend project
2. Go to: **Settings** tab
3. Find: **Compose File** section

### Step 3.3: Paste Frontend Configuration

**ACTION**: Copy the entire content from this file:
```
/home/alagiri/projects/bizoholic/dokploy-frontend-staging-complete-build.yml
```

**TO**: Dokploy compose editor

### Step 3.4: Deploy Frontend Services

1. Click: **Deploy** button
2. Dokploy will build all 6 Next.js applications from GitHub
3. **Wait 30-45 minutes** for builds to complete

### Step 3.5: Monitor Frontend Build Progress

**What's happening**:
- 6 Next.js apps building in parallel
- Each app takes 8-10 minutes to build
- Largest build time due to npm dependencies
- Total ~30-45 minutes

**Watch for in logs**:
```
Building bizoholic-frontend...
Building client-portal...
Building coreldove-frontend...
Building business-directory-frontend...
Building thrillring-gaming...
Building admin-dashboard...

npm install... (longest step)
next build... (second longest)

✓ All builds completed
Creating containers...
✓ Started all 6 frontend services
```

### Step 3.6: Verify Frontend Deployment

**Run final health check**:
```bash
./check-complete-staging.sh
```

**Expected output**:
```
Infrastructure:  6/6   ✅
Backend:         9/9   ✅
Frontend:        6/6   ✅
Total:           21/21  (100%)

🎉 SUCCESS! All 21 containers deployed and running!
```

**Test frontend apps in browser**:
1. Bizoholic: `http://194.238.16.237:3000`
2. Client Portal: `http://194.238.16.237:3001`
3. CorelDove: `http://194.238.16.237:3002`
4. Business Directory: `http://194.238.16.237:3003`
5. Admin Dashboard: `http://194.238.16.237:3009`

**✅ PHASE 3 COMPLETE when**:
- [ ] 6/6 frontend containers running
- [ ] All frontend apps load in browser
- [ ] Can navigate pages without errors
- [ ] Frontend connects to backend APIs

**⏱️ Checkpoint 3**: Record time taken for Phase 3: _____ minutes

---

## 🎉 DEPLOYMENT COMPLETE!

### Final Verification Checklist

- [ ] All 21 containers running: `./check-complete-staging.sh`
- [ ] Infrastructure healthy (6/6)
- [ ] Backend healthy (9/9)
- [ ] Frontend healthy (6/6)
- [ ] Superset accessible and login works
- [ ] Backend APIs responding to /health
- [ ] Frontend apps load in browser
- [ ] No services in crash loop

### Success Metrics

**Container Status**:
```bash
ssh root@194.238.16.237
docker ps --format 'table {{.Names}}\t{{.Status}}' | grep bizosaas | wc -l
# Should show: 21
```

**Health Check Summary**:
```bash
./check-complete-staging.sh
# Should show: 21/21 (100%)
```

---

## 📊 Record Your Deployment

**Total Deployment Time**: _____ minutes

**Phase Breakdown**:
- Phase 1 (Infrastructure): _____ minutes
- Phase 2 (Backend): _____ minutes
- Phase 3 (Frontend): _____ minutes

**Issues Encountered**: (if any)
- [ ] None - smooth deployment ✅
- [ ] Build timeout: _____
- [ ] Container crashes: _____
- [ ] Other: _____

---

## 🚨 Troubleshooting During Deployment

### If Build Times Out
**Symptom**: Dokploy shows "Build timeout" or "Build failed"
**Solution**:
1. In Dokploy project settings, increase timeout to 3600 seconds (1 hour)
2. Re-deploy the same configuration
3. Dokploy will resume from where it failed

### If Container Crashes After Build
**Symptom**: Container shows "Restarting" or "Exited"
**Solution**:
1. Check logs in Dokploy UI or SSH:
   ```bash
   ssh root@194.238.16.237
   docker logs <container-name> --tail 100
   ```
2. Common fixes:
   - Database not ready: Wait 30 seconds, restart container
   - Environment variable missing: Check compose config
   - Port conflict: Verify no other service using same port

### If Service Won't Start
**Symptom**: Container stuck in "Created" status
**Solution**:
1. Check dependencies are running:
   ```bash
   docker ps | grep postgres
   docker ps | grep redis
   ```
2. Manually start container:
   ```bash
   docker start <container-name>
   ```
3. Check logs for specific error

### If Frontend Build Fails (ENOSPC)
**Symptom**: "ENOSPC: no space left on device"
**Solution**:
1. We already freed 33GB, but if this happens:
   ```bash
   ssh root@194.238.16.237
   docker system prune -f
   ```
2. Re-deploy frontend configuration

---

## 📞 Post-Deployment Actions

### Immediate (Next 15 minutes)
1. **Configure Superset**:
   - Login to http://194.238.16.237:8088
   - Add PostgreSQL data source
   - Create first dashboard

2. **Test Critical Flows**:
   - User registration (if applicable)
   - Form submission (Bizoholic)
   - Product browsing (CorelDove)

3. **Check Logs**:
   ```bash
   ssh root@194.238.16.237
   docker logs bizosaas-superset-staging --tail 50
   docker logs bizosaas-brain-staging --tail 50
   ```

### This Week
1. Set up domain DNS for staging subdomains
2. Configure Traefik SSL certificates
3. Run end-to-end testing
4. Document any deployment-specific issues

---

## 🔗 Quick Reference

**Dokploy UI**: https://dk.bizoholic.com
**VPS SSH**: `ssh root@194.238.16.237`
**Health Check**: `./check-complete-staging.sh`

**Config Files**:
1. `dokploy-infrastructure-staging-with-superset-build.yml`
2. `dokploy-backend-staging-complete-build.yml`
3. `dokploy-frontend-staging-complete-build.yml`

**Service URLs**:
- Superset: http://194.238.16.237:8088
- Brain API: http://194.238.16.237:8001
- Bizoholic: http://194.238.16.237:3000
- Admin: http://194.238.16.237:3009

---

## ✅ Ready to Start!

**Current Status**: 9/21 containers (42%)
**Target Status**: 21/21 containers (100%)
**Estimated Time**: 1-1.5 hours

**First Action**: Go to https://dk.bizoholic.com and start Phase 1 (Infrastructure)

---

*Deployment Guide Version: 1.0*
*Last Updated: 2025-10-12 14:15 UTC*
*Prepared for: VPS Staging Deployment*

Good luck! 🚀
