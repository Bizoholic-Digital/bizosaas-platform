# Client Portal 502 Error - Advanced Diagnosis
**Date:** November 17, 2025
**Status:** 🔴 CRITICAL - Image built without BASE_PATH

---

## 🚨 Root Cause: Pre-built Docker Image Issue

### Current Situation
- **Docker Image**: `ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.2.14`
- **Application Status**: ✅ Running on port 3003
- **Next.js Status**: ✅ Ready in 212ms
- **HTTP Response**: ❌ 502 Bad Gateway

### The Real Problem

**You're using a pre-built Docker image that was created BEFORE we added the missing environment variables.**

From your deployment log:
```
ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.2.14
Status: Image is up to date for ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.2.14
```

This image was built WITHOUT:
- ❌ `BASE_PATH=/portal`
- ❌ Other critical environment variables

### Why Adding Environment Variables in Dokploy Doesn't Fix It

**Next.js BASE_PATH is a BUILD-TIME configuration:**

From [next.config.js:24](bizosaas/frontend/apps/client-portal/next.config.js#L24):
```javascript
basePath: process.env.BASE_PATH || '',
```

1. **During Build**: Next.js reads `BASE_PATH` and bakes it into the static files
2. **During Runtime**: The basePath is already set in compiled code
3. **Adding env var later**: Won't change the already-built application

**Result:**
- Image built with `BASE_PATH=''` (empty)
- App serves routes at `/` (root)
- Traefik forwards to `/portal`
- App doesn't recognize `/portal` → 502 Error

---

## 🔍 Verification of Issue

### Application Logs Show Success
```
✓ Next.js 15.5.3
✓ Local:   http://localhost:3003
✓ Network: http://0.0.0.0:3003
✓ Ready in 212ms
```

✅ App is running correctly on port 3003

### But basePath is Wrong

The image was built with:
```javascript
basePath: ''  // Empty because BASE_PATH env var wasn't set during build
```

So the app expects routes at:
- `/` (homepage)
- `/dashboard` (dashboard)
- `/login` (login)

But Traefik is forwarding:
- `/portal/` (homepage)
- `/portal/dashboard` (dashboard)
- `/portal/login` (login)

**Route mismatch** = 502 Bad Gateway

---

## ✅ Solutions (3 Options)

### Option 1: Rebuild Docker Image with BASE_PATH (RECOMMENDED)

**Trigger a new build with correct environment variables:**

#### A. Via GitHub Actions (if configured)
1. Ensure `.env.production` has `BASE_PATH=/portal` ✅ (already done)
2. Push the updated code to GitHub (already attempted, blocked by secrets)
3. GitHub Actions builds new image with v2.2.15
4. Dokploy pulls new image

#### B. Manual Build and Push
```bash
# From your local machine or VPS
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/client-portal

# Build with environment variables
docker build \
  --build-arg BASE_PATH=/portal \
  --build-arg NODE_ENV=production \
  -t ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.2.15 \
  -f Dockerfile .

# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Push new image
docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.2.15
```

#### C. Update Dokploy to use new image
```
ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.2.15
```

---

### Option 2: Use Dokploy GitHub Integration (BEST LONG-TERM)

**Switch from pre-built images to Dokploy building from source:**

#### Setup Steps:

1. **In Dokploy Dashboard** → client-portal:
   - Change deployment method from "Docker Image" to "GitHub"
   - Repository: `Bizoholic-Digital/bizosaas-platform`
   - Branch: `main`
   - Build Path: `bizosaas/frontend/apps/client-portal`
   - Dockerfile: `bizosaas/frontend/apps/client-portal/Dockerfile`

2. **Set Environment Variables** (same as before):
   ```bash
   BASE_PATH=/portal
   NEXT_PUBLIC_API_URL=https://api.bizoholic.com/api
   NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com/api
   BRAIN_API_BASE_URL=https://api.bizoholic.com/api
   JWT_SECRET=n62SLTZfZjKABOw04EjBWvjp6635XifgQP1+XRkfbac=
   NEXTAUTH_SECRET=BQ8cXrPJhPp4MD/OT9GYNTE3DHpZjiIJM4kbPGXkcpY=
   NEXTAUTH_URL=https://stg.bizoholic.com/portal
   NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/portal
   NEXT_PUBLIC_PLATFORM_NAME=client-portal
   NEXT_PUBLIC_TENANT_SLUG=bizosaas
   NODE_ENV=production
   PORT=3003
   # ... (all other vars)
   ```

3. **Trigger Build**:
   - Dokploy will build from source WITH environment variables
   - BASE_PATH will be set during build
   - Image will be built correctly

**Advantages:**
- ✅ Always builds with latest code
- ✅ Environment variables applied during build
- ✅ No manual image building needed
- ✅ Auto-deploy on git push (optional)

---

### Option 3: Test Without BASE_PATH (Quick Diagnosis)

**Temporarily deploy at root path to verify everything else works:**

#### Modify Traefik Routing:
Instead of routing to `/portal`, temporarily route to `/`:
- Change PathPrefix from `/portal` to `/`
- Test if app loads at root

**This won't fix the production issue but confirms:**
- Port mapping is correct
- Container is healthy
- Only BASE_PATH is the issue

---

## 🎯 Recommended Action Plan

### Immediate Fix (Choose One):

**Option A: If you have GitHub Actions CI/CD configured**
1. Fix the secret detection issues in GitHub
2. Push the updated .env.production
3. Wait for GitHub Actions to build v2.2.15
4. Update Dokploy to use new image
5. Redeploy

**Option B: Switch to Dokploy GitHub Integration (BEST)**
1. Change client-portal deployment from "Docker Image" to "GitHub"
2. Configure repository and build path
3. Set all environment variables in Dokploy
4. Trigger build - Dokploy builds from source
5. Environment variables will be baked into build

**Option C: Manual rebuild**
1. Build image locally with BASE_PATH
2. Push to GHCR as v2.2.15
3. Update Dokploy to use new image
4. Redeploy

---

## 📋 Verification After Fix

Once new image is deployed, verify:

```bash
# 1. Check if app recognizes /portal path
curl -I https://stg.bizoholic.com/portal
# Expected: 200 OK (not 502)

# 2. Check deployment logs
# Should show: "Using basePath: /portal"

# 3. Test in browser
# https://stg.bizoholic.com/portal should load

# 4. Check API calls
# Network tab should show calls to https://api.bizoholic.com
```

---

## 🔍 Additional Diagnostics

### Check Traefik Routing

**In Dokploy, verify Traefik labels:**
```yaml
traefik.http.routers.client-portal.rule=Host(`stg.bizoholic.com`) && PathPrefix(`/portal`)
traefik.http.routers.client-portal.service=client-portal
traefik.http.services.client-portal.loadbalancer.server.port=3003
```

### Check if Service is Reachable

**From VPS (if you have SSH access):**
```bash
# Check if container is listening
docker ps | grep client-portal

# Get container ID
CONTAINER_ID=$(docker ps | grep client-portal | awk '{print $1}')

# Test direct container access
docker exec $CONTAINER_ID curl -I http://localhost:3003
# Should return Next.js response

# Check environment variables in container
docker exec $CONTAINER_ID env | grep BASE_PATH
# Should show: BASE_PATH=/portal (after rebuild)
```

### Current vs Required State

| Aspect | Current State | Required State |
|--------|--------------|----------------|
| Docker Image | v2.2.14 (old build) | v2.2.15 (new build) |
| BASE_PATH in build | ❌ Not set (empty) | ✅ /portal |
| Environment vars | ✅ Set in Dokploy | ✅ Set in Dokploy |
| Port | ✅ 3003 | ✅ 3003 |
| App Running | ✅ Yes | ✅ Yes |
| basePath in code | ❌ '' (empty) | ✅ '/portal' |
| Route handling | ❌ Expects / | ✅ Expects /portal |

---

## 💡 Why This Happened

1. **Initial Setup**: Image v2.2.14 was built without proper .env.production
2. **Our Fix**: We created correct .env.production locally
3. **Deployment**: You updated Dokploy environment variables
4. **Problem**: Dokploy is using OLD pre-built image from GHCR
5. **Result**: Environment variables in Dokploy don't affect pre-built image

**The Fix**: Build a new image (v2.2.15) WITH the correct environment variables

---

## 🚀 Next Steps

**Choose the best option for your workflow:**

1. **For Quick Fix**: Use Option 2 (Dokploy GitHub Integration)
   - Most reliable long-term solution
   - No manual image building
   - Environment variables always fresh

2. **For Existing CI/CD**: Use Option 1 (Rebuild via GitHub Actions)
   - If you already have automation
   - Just need to allow secrets in GitHub

3. **For Manual Control**: Use Option 3 (Manual rebuild)
   - Build and push manually
   - Full control over image

---

**Status:** 🔧 Diagnosis Complete | Awaiting Image Rebuild
**Priority:** 🔴 HIGH
**ETA:** ~15-20 minutes (depending on build method)
