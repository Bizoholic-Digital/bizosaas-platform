# Client Portal - Final Deployment Instructions

**Date**: 2025-11-12
**Issue**: Login API calling relative `/api/auth/me` instead of `https://api.bizoholic.com/api/auth/me`
**Root Cause**: NEXT_PUBLIC_* environment variables not embedded at build time
**Solution**: Updated Dockerfile to accept build args and rebuild with production URLs

---

## What Was Fixed (v2.1.4-final)

### Dockerfile Update
Added ARG and ENV declarations to properly embed production API URLs at build time:

```dockerfile
# Accept build arguments
ARG NODE_ENV=production
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_BRAIN_GATEWAY_URL
ARG NEXT_PUBLIC_AUTH_API_URL
ARG NEXT_PUBLIC_APP_URL
ARG BASE_PATH

# Set environment variables for build
ENV NODE_ENV=$NODE_ENV
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_BRAIN_GATEWAY_URL=$NEXT_PUBLIC_BRAIN_GATEWAY_URL
ENV NEXT_PUBLIC_AUTH_API_URL=$NEXT_PUBLIC_AUTH_API_URL
ENV NEXT_PUBLIC_APP_URL=$NEXT_PUBLIC_APP_URL
ENV BASE_PATH=$BASE_PATH
```

### Build Command
Built with production URLs explicitly passed as build arguments:

```bash
docker build \
  --no-cache \
  --build-arg NODE_ENV=production \
  --build-arg NEXT_PUBLIC_API_URL=https://api.bizoholic.com/api \
  --build-arg NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com/api \
  --build-arg NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/api/auth \
  --build-arg NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/portal \
  --build-arg BASE_PATH=/portal \
  -t ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.1.4-final \
  -t ghcr.io/bizoholic-digital/bizosaas-client-portal:latest \
  .
```

---

## Deployment Steps

### Step 1: Wait for Build Completion
The build is currently running in the background. Check build status:

```bash
# Will complete in ~3-5 minutes
# Look for: "Successfully built..." and "Successfully tagged..."
```

### Step 2: Push to GHCR (After build completes)
```bash
docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.1.4-final
docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:latest
```

### Step 3: Update Dokploy
1. Log in to Dokploy UI on KVM4
2. Navigate to **Services** → **Client Portal**
3. Update image to: `ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.1.4-final`
4. Verify environment variables are set (they should already be correct):
   ```env
   NODE_ENV=production
   PORT=3000
   NEXT_PUBLIC_API_URL=https://api.bizoholic.com/api
   NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com/api
   BRAIN_API_BASE_URL=https://api.bizoholic.com/api
   NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/api/auth
   NEXTAUTH_URL=https://stg.bizoholic.com/portal
   BASE_PATH=/portal
   ```
5. Click **Redeploy**
6. Wait for deployment to complete (~2 minutes)

### Step 4: Test Authentication Flow

**Clear Browser Cache First!**
- Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
- Or use Incognito/Private window

**Test 1: Unauthenticated Access**
```
Visit: https://stg.bizoholic.com/portal/
Expected: Immediate redirect to /portal/login (no flash)
```

**Test 2: Login**
```
At login page:
Email: demo@bizosaas.com
Password: demo123

Expected:
- Redirect to /portal/dashboard
- No console errors
- API calls go to https://api.bizoholic.com/api/auth/login (not /api/auth/login)
```

**Test 3: Check Browser Console**
```
Open DevTools (F12)
Go to Console tab
Expected: NO errors like "/api/auth/me:1 Failed to load resource"
```

**Test 4: Check Network Tab**
```
Open DevTools (F12)
Go to Network tab
Filter by: "auth"
Expected: API calls show "https://api.bizoholic.com/api/auth/me" (absolute URL)
```

---

## Key Differences from Previous Versions

### v2.1.2-production (BROKEN)
- Built with .env.production file
- NEXT_PUBLIC_* variables NOT embedded (Next.js didn't read them)
- Client made relative API calls: `/api/auth/me`
- Result: 401 errors, login failed

### v2.1.4-final (FIXED)
- Built with `--build-arg` flags
- Dockerfile accepts and uses ARG → ENV conversion
- NEXT_PUBLIC_* variables embedded in JavaScript bundles at build time
- Client makes absolute API calls: `https://api.bizoholic.com/api/auth/me`
- Result: Authentication works ✅

---

## Why This Fix Works

### Next.js Build-Time Variable Embedding

Next.js replaces `process.env.NEXT_PUBLIC_*` with actual values during build:

**Before Build** (source code):
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api'
```

**After Build** (JavaScript bundle):
```javascript
const API_BASE_URL = "https://api.bizoholic.com/api" || '/api'
```

This only works if the environment variables are available **during `npm run build`**:
- ❌ `.env.production` file alone doesn't work (Next.js doesn't always read it)
- ✅ Dockerfile ENV from ARG ensures variables are set in build environment

---

## Verification Checklist

After deployment, verify:

- [ ] Login page loads at https://stg.bizoholic.com/portal/login
- [ ] Enter demo credentials (demo@bizosaas.com / demo123)
- [ ] Login succeeds and redirects to /portal/dashboard
- [ ] Browser console shows NO `/api/auth/me` errors
- [ ] Browser console shows NO `401` errors
- [ ] Network tab shows API calls to `https://api.bizoholic.com/api/*`
- [ ] Dashboard displays user information
- [ ] No flash behavior when visiting /portal/

---

## Troubleshooting

### If login still fails with 401 errors:

**Check 1: Verify correct image deployed**
```bash
# SSH to KVM4
ssh root@72.60.219.244

# Check image
docker service inspect frontend-client-portal --format '{{.Spec.TaskTemplate.ContainerSpec.Image}}'

# Should show: ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.1.4-final
```

**Check 2: Verify API URLs embedded**
```bash
# In browser DevTools Console, run:
fetch('/portal/_next/static/chunks/app/login/page-*.js').then(r=>r.text()).then(t=>console.log(t.includes('api.bizoholic.com')))

# Should return: true
```

**Check 3: Clear browser cache**
```
- Close all browser tabs
- Clear cache completely
- Restart browser
- Try in incognito/private window
```

### If still not working:

1. Check Brain Gateway is running and accessible
2. Test Brain Gateway directly:
   ```bash
   curl -X POST https://api.bizoholic.com/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"demo@bizosaas.com","password":"demo123"}'

   # Should return: {"success": true, "token": "...", "user": {...}}
   ```

3. Check Traefik routing:
   ```bash
   curl -I https://api.bizoholic.com/api/auth/login
   # Should return: 405 Method Not Allowed (GET not allowed, but route exists)
   ```

---

## Summary

**Problem**: Client making relative API calls `/api/auth/me` → 401 errors

**Solution**:
1. Updated Dockerfile to accept build arguments
2. Rebuilt with `--build-arg NEXT_PUBLIC_API_URL=https://api.bizoholic.com/api`
3. Production URLs now embedded in JavaScript bundles

**Result**: Client makes absolute API calls → Authentication works ✅

---

**Next Image to Deploy**: `ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.1.4-final`

**ETA**: Build completing in ~3-5 minutes, then push to GHCR and redeploy
