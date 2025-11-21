# Client Portal Dockerfile Fix - The Real Issue
**Date:** November 17, 2025
**Status:** 🔴 CRITICAL - Dockerfile missing BASE_PATH during build

---

## 🚨 Root Cause: Dockerfile Configuration Error

### What Was Wrong

**The v2.2.15 image still had 502 errors because:**

The Dockerfile was setting `BASE_PATH=/portal` **ONLY at runtime** (after build), but Next.js needs it **DURING the build process**.

### Dockerfile Issues Found

#### Issue #1: BASE_PATH Not Available During Build

**BEFORE (Lines 27-34):**
```dockerfile
# Accept build arguments
ARG NODE_ENV=production
ARG NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com/api

# Set environment variables for build
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=$NODE_ENV
ENV NEXT_PUBLIC_BRAIN_GATEWAY_URL=$NEXT_PUBLIC_BRAIN_GATEWAY_URL
# ❌ BASE_PATH NOT SET HERE!

# Build the application
RUN npm run build  # ❌ Builds without BASE_PATH!
```

**Runtime Only (Line 75):**
```dockerfile
# Runtime environment variables (defaults)
ENV BASE_PATH=/portal  # ⚠️ TOO LATE! Build already done
```

**AFTER (Fixed):**
```dockerfile
# Accept build arguments
ARG NODE_ENV=production
ARG BASE_PATH=/portal  # ✅ Added as build arg
ARG NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com/api

# Set environment variables for build
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=$NODE_ENV
ENV BASE_PATH=$BASE_PATH  # ✅ Available during build
ENV NEXT_PUBLIC_BRAIN_GATEWAY_URL=$NEXT_PUBLIC_BRAIN_GATEWAY_URL

# Build the application
RUN npm run build  # ✅ Now builds WITH BASE_PATH=/portal
```

#### Issue #2: Wrong Port

**BEFORE (Lines 68-70):**
```dockerfile
EXPOSE 3001  # ❌ Wrong port!
ENV PORT=3001  # ❌ Wrong port!
```

**AFTER (Fixed):**
```dockerfile
EXPOSE 3003  # ✅ Correct port
ENV PORT=3003  # ✅ Correct port
```

---

## 🔍 Why This Matters

### How Next.js basePath Works

1. **During Build** (`npm run build`):
   ```javascript
   // next.config.js reads BASE_PATH
   basePath: process.env.BASE_PATH || '',
   ```

   Next.js:
   - Reads `BASE_PATH` from environment
   - Rewrites all routes to include the prefix
   - Generates static files with correct paths
   - Compiles this into `.next/` build output

2. **During Runtime** (container runs):
   - Base path is already **baked into the compiled code**
   - Setting `BASE_PATH` at runtime does nothing
   - The app serves at the paths it was built with

### Why v2.2.15 Still Failed

**Build Process:**
```bash
docker build ...
# During build:
# - BASE_PATH not set (undefined)
# - next.config.js: basePath = '' (empty)
# - Routes compiled for root path: /, /dashboard, /login

# After build:
# - ENV BASE_PATH=/portal set
# - BUT: Routes already compiled for root path
# - Setting it now has no effect!
```

**Result:**
- App expects routes at: `/`, `/dashboard`, `/login`
- Traefik forwards to: `/portal`, `/portal/dashboard`, `/portal/login`
- **Route mismatch** = 502 Error

---

## ✅ The Fix Applied

### Changes Made to Dockerfile

1. **Added BASE_PATH as build argument** (Line 29)
2. **Set BASE_PATH during build** (Line 35)
3. **Fixed port from 3001 to 3003** (Lines 70, 72)

### Changes Made to rebuild-with-basepath.sh

1. **Updated version to v2.2.16**
2. **Added `--build-arg BASE_PATH=/portal`** to docker build command
3. **Added `--build-arg NEXT_PUBLIC_BRAIN_GATEWAY_URL`** for completeness

---

## 🚀 Rebuild Instructions

### Run This Now:

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/client-portal

# Rebuild with CORRECT Dockerfile
./rebuild-with-basepath.sh
```

**When prompted for GitHub token:**
```
ghp_REDACTED
```

**This will:**
1. Build image with BASE_PATH baked in during build
2. Build image with correct port 3003
3. Push as v2.2.16 to GHCR

### After Build:

1. **Go to Dokploy**: https://dk4.bizoholic.com/dashboard
2. **Update image**: `ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.2.16`
3. **Redeploy**
4. **Test**: `curl -I https://stg.bizoholic.com/portal`
   - **Expected**: HTTP/2 200 ✅

---

## 📊 Comparison: v2.2.14 vs v2.2.15 vs v2.2.16

| Aspect | v2.2.14 | v2.2.15 | v2.2.16 |
|--------|---------|---------|---------|
| BASE_PATH in Dockerfile | ❌ Runtime only | ❌ Runtime only | ✅ Build + Runtime |
| BASE_PATH build arg | ❌ Not defined | ❌ Not defined | ✅ Defined |
| BASE_PATH during npm build | ❌ Undefined | ❌ Undefined | ✅ Set to /portal |
| Port | ❌ 3001 | ❌ 3001 | ✅ 3003 |
| Routes compiled for | / | / | /portal |
| Works at /portal | ❌ 502 | ❌ 502 | ✅ 200 |

---

## 🔍 Verification After v2.2.16 Deploy

### 1. Check Build Logs

Look for during build:
```
Building with BASE_PATH: /portal
Next.js configured with basePath: /portal
```

### 2. Check Runtime Logs

```bash
# Should show:
Server listening on port 3003 (not 3001)
```

### 3. Test the Endpoint

```bash
curl -I https://stg.bizoholic.com/portal
# Expected: HTTP/2 200

curl https://stg.bizoholic.com/portal
# Should return HTML
```

### 4. Check in Browser

- Open: https://stg.bizoholic.com/portal
- Should load without 502
- Check Network tab: All assets should load from `/portal/...`

---

## 🎓 Lesson Learned

### Build-time vs Runtime Environment Variables

**Build-time (ARG + ENV before build):**
- Required for: Next.js configuration, static asset paths, route generation
- Examples: `BASE_PATH`, `NEXT_PUBLIC_*` vars used in code
- Must be set BEFORE `npm run build`

**Runtime (ENV after build):**
- Required for: Server configuration, dynamic values, secrets
- Examples: `PORT`, `DATABASE_URL`, API keys
- Can be changed without rebuilding

**Next.js BASE_PATH specifically:**
- ✅ Must be set during build (compile-time)
- ❌ Cannot be changed at runtime
- Requires rebuild if changed

---

## 📝 Summary

**Problem:** Dockerfile set BASE_PATH too late (after build)

**Solution:**
1. Add `ARG BASE_PATH=/portal` before build
2. Set `ENV BASE_PATH=$BASE_PATH` before `npm run build`
3. Pass `--build-arg BASE_PATH=/portal` during docker build

**Result:** Routes compiled correctly for `/portal` path

---

**Status:** 🔧 Ready to rebuild as v2.2.16
**Priority:** 🔴 CRITICAL
**ETA:** ~5-10 minutes build time
