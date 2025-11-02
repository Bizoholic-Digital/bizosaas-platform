# Business Directory - Dokploy Deployment Guide
## DDD-Compliant Microservice Deployment to stg.bizoholic.com/directory/

**Date:** 2025-11-02
**Status:** ✅ Ready for Deployment
**Architecture:** DDD Microservices with Workspace Packages
**Image:** `ghcr.io/bizoholic-digital/bizosaas-business-directory:latest`

---

## 🎯 DEPLOYMENT STRATEGY

### Recommended Approach: GHCR Pre-built Images

Following the established pattern used by Client Portal and other services, we'll use GitHub Container Registry (GHCR) for consistent deployments.

**Why GHCR:**
- ✅ Consistent with other BizOSaaS services
- ✅ Faster deployments (pre-built images)
- ✅ Better control over build process
- ✅ Easier rollbacks and version management

---

## 📦 STEP 1: BUILD & PUSH TO GHCR

### Build from Repository Root

The Business Directory uses workspace packages from `/packages/*`, so build from the **repository root**:

```bash
# Navigate to repository root
cd /home/alagiri/projects/bizosaas-platform

# Build the image
docker build \
  -f bizosaas/frontend/apps/business-directory/Dockerfile.production \
  -t ghcr.io/bizoholic-digital/bizosaas-business-directory:v1.0.0 \
  -t ghcr.io/bizoholic-digital/bizosaas-business-directory:latest \
  .

# Login to GHCR (if not already logged in)
docker login ghcr.io -u <your-github-username>

# Push to GHCR
docker push ghcr.io/bizoholic-digital/bizosaas-business-directory:v1.0.0
docker push ghcr.io/bizoholic-digital/bizosaas-business-directory:latest
```

**Note:** The `.dockerignore` file reduces build context from 702MB to 617KB for faster builds.

---

## 📋 STEP 2: DOKPLOY UI CONFIGURATION

### Application Type: Docker Image (Not Git Repository)

Since we're using GHCR, configure Dokploy to pull the pre-built image:

**General Settings:**
```
Application Name:        frontend-business-directory
Deployment Type:        Docker Image
Image:                  ghcr.io/bizoholic-digital/bizosaas-business-directory:latest
```

### Environment Variables

```bash
NEXT_PUBLIC_API_BASE_URL=http://bizosaas-saleor-api-8003:8000
NODE_ENV=production
PORT=3004
HOSTNAME=0.0.0.0
NEXT_TELEMETRY_DISABLED=1
NEXT_PUBLIC_STAGING_URL=https://stg.bizoholic.com/directory
NEXT_PUBLIC_PRODUCTION_URL=https://www.bizoholic.net
```

### Network & Routing

```
Docker Network:         dokploy-network
Port:                   3004
Domain:                 stg.bizoholic.com
Path Prefix:            /directory
Strip Prefix:           ✅ YES
HTTPS:                  ✅ YES
```

---

## 🔄 ALTERNATIVE: BUILD FROM GIT (Not Recommended)

If you prefer Dokploy to build from Git (slower, but simpler):

**General Settings:**
```
Application Name:        frontend-business-directory
Deployment Type:        Git Repository
Repository:             https://github.com/Bizoholic-Digital/bizosaas-platform
Branch:                 main
Build Context:          /
Dockerfile Path:        bizosaas/frontend/apps/business-directory/Dockerfile.production
```

**Environment Variables:** (same as above)

**Network & Routing:** (same as above)

---

## ✅ DEPLOYMENT CHECKLIST

Pre-deployment verification:
- ✅ Component refactoring (workspace packages)
- ✅ Dockerfile optimization (.dockerignore)
- ✅ Git commit & push (9892595)
- ✅ Architecture alignment (DDD compliant)
- ⏳ Build and push to GHCR (pending)
- ⏳ Configure Dokploy UI (pending)
- ⏳ Deploy and verify (pending)

---

## 🚀 DEPLOYMENT STEPS

1. **Build & Push** (5 min): Run build commands above
2. **Configure Dokploy** (5 min): Set up application in Dokploy UI
3. **Deploy** (2 min): Click "Deploy" in Dokploy
4. **Verify** (3 min): Test at https://stg.bizoholic.com/directory

**ESTIMATED TIME:** 15 minutes
**SUCCESS RATE:** High (proven GHCR pattern)
