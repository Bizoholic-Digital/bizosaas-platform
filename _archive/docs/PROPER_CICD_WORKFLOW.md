# Proper CI/CD Workflow: Local → GitHub → Dokploy → VPS

**Goal**: Sync local changes to staging automatically via GitHub

---

## Current Status

✅ **Local WSL2**: All 12 services working with pre-built images
✅ **VPS**: All 12 images loaded and ready
✅ **GitHub**: Code repository up to date with all fixes
⏳ **Dokploy**: Needs to be configured to build from GitHub

---

## The Workflow You Want

```
Developer (WSL2)
    ↓ git push
GitHub Repository
    ↓ Dokploy webhook/pull
Dokploy Build
    ↓ deploy
VPS Staging Containers
```

### Benefits:
- ✅ Make changes locally
- ✅ Push to GitHub
- ✅ Dokploy automatically rebuilds
- ✅ Changes live on staging
- ✅ Proper version control
- ✅ Rollback capability

---

## What Needs to Change

### Current Setup (Local Images):
- Dokploy uses pre-loaded images: `bizosaas-brain-gateway:latest`
- **Problem**: Code changes don't trigger rebuilds

### New Setup (GitHub Builds):
- Dokploy builds from GitHub: `build: context: https://github.com/...`
- **Benefit**: Every git push triggers new build and deploy

---

## Implementation Plan

### Step 1: Create GitHub Build Compose Files

**Backend**: `dokploy-backend-staging-github.yml`
```yaml
services:
  brain-api:
    build:
      context: https://github.com/Bizoholic-Digital/bizosaas-platform.git#main:bizosaas-platform/ai/services/bizosaas-brain
      dockerfile: Dockerfile
    container_name: bizosaas-brain-staging
    # ... rest of config
```

**Frontend**: `dokploy-frontend-staging-github.yml`
```yaml
services:
  client-portal:
    build:
      context: https://github.com/Bizoholic-Digital/bizosaas-platform.git#main:bizosaas-platform/frontend/apps/client-portal
      dockerfile: Dockerfile
    container_name: bizosaas-client-portal-staging
    # ... rest of config
```

### Step 2: Apply All Previous Fixes

These fixes MUST be in the GitHub build files:

#### Backend Fixes:
1. ✅ `python-dotenv>=1.1.1` (not 1.0.0)
2. ✅ `openai>=1.68.2` (not ≥1.13.3)
3. ✅ Database URL: `194.238.16.237:5433` (not container DNS)
4. ✅ Redis URL: `194.238.16.237:6380` (not container DNS)
5. ✅ Remove duplicate temporal-integration service

#### Frontend Fixes:
1. ✅ `npm ci --legacy-peer-deps` (not --only=production)
2. ✅ Correct API URLs to backend services

### Step 3: Update Dokploy Projects

Replace current compose files in Dokploy dashboard with GitHub build versions.

### Step 4: Configure GitHub Webhook (Optional but Recommended)

Enable automatic deployments on git push:
1. Dokploy → Project Settings → Enable GitHub Integration
2. GitHub → Repository → Settings → Webhooks
3. Add webhook URL from Dokploy

---

## Hybrid Approach (Recommended for Now)

Since we have working images loaded, use a **gradual migration**:

### Phase 1: Immediate (Use Current Local Images)
- Deploy with `dokploy-backend-staging-local.yml`
- Deploy with `dokploy-frontend-staging-local.yml`
- **Result**: Services running ASAP

### Phase 2: Switch to GitHub Builds (After Phase 1 Success)
- Replace with `dokploy-backend-staging-github.yml`
- Replace with `dokploy-frontend-staging-github.yml`
- Test one service at a time
- **Result**: Proper CI/CD pipeline

---

## The Files We Need

### Option A: Pure GitHub Builds (Your Question)
- `dokploy-backend-staging-github.yml` - Build from GitHub repo
- `dokploy-frontend-staging-github.yml` - Build from GitHub repo

### Option B: Hybrid (Safer Transition)
- Use local images NOW (already loaded)
- Switch to GitHub builds LATER (after verifying deployment works)

---

## Answer to Your Question

> "now going forward as we have the same files locally (wsl2) container and vps we should be able to use local -> github -> dokploy (staging environment) right?"

**YES, absolutely!** Here's what will happen:

1. **You make changes** in WSL2 (edit code, fix bugs, add features)
2. **Commit and push** to GitHub:
   ```bash
   git add .
   git commit -m "feat: Add new feature"
   git push origin main
   ```
3. **Dokploy detects change** (via webhook or manual trigger)
4. **Dokploy builds** from GitHub source using Dockerfile
5. **Dokploy deploys** to VPS staging environment
6. **Changes are live** at `stg.bizoholic.com`, `194.238.16.237:PORT`

### Requirements for This to Work:
1. ✅ All code fixes must be in GitHub (we already pushed them)
2. ✅ Dokploy must use `build:` not `image:` in compose files
3. ✅ All dependency fixes must be in requirements.txt/package.json (done)
4. ⏳ Update Dokploy compose files to use GitHub source

---

## Immediate Next Steps

### Option 1: Get Services Running First (Recommended)
```bash
# 1. Deploy using loaded images (fast)
# Update Dokploy with dokploy-backend-staging-local.yml
# Update Dokploy with dokploy-frontend-staging-local.yml

# 2. Verify everything works
curl http://194.238.16.237:8001/health  # Brain API
curl http://194.238.16.237:3000         # Client Portal

# 3. THEN switch to GitHub builds
# Update Dokploy with dokploy-backend-staging-github.yml
# Update Dokploy with dokploy-frontend-staging-github.yml
```

### Option 2: Jump Straight to GitHub Builds
```bash
# Create GitHub build compose files with all fixes
# Deploy directly from GitHub
# Longer initial deployment (20-30 min build time)
# But proper CI/CD from day 1
```

---

## What I Recommend

**Do Option 1**: Get services running with local images first, then migrate to GitHub builds.

**Why?**
- ✅ Services running in 5 minutes (images already loaded)
- ✅ Verify deployment works
- ✅ Then switch to GitHub builds knowing everything is configured correctly
- ✅ Less risk of issues

**Shall I proceed with:**
1. Creating the proper GitHub build compose files with all fixes?
2. Deploying current local images first, then migrating to GitHub builds?

Both approaches end up with the workflow you want: **Local → GitHub → Dokploy → VPS**
