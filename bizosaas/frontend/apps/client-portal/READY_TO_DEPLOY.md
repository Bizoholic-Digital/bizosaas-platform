# Client Portal - Ready for Deployment

**Status**: ✅ **READY TO DEPLOY**
**Date**: 2025-11-12
**Images Pushed**: staging-v2.1.6

---

## Quick Deployment

### Image to Deploy
```
ghcr.io/bizoholic-digital/bizosaas-client-portal:staging-v2.1.6
```

### Steps
1. Log in to Dokploy at KVM4
2. Navigate to: Services → Client Portal
3. Update image to: `ghcr.io/bizoholic-digital/bizosaas-client-portal:staging-v2.1.6`
4. Click **Redeploy**
5. Wait 2-3 minutes for deployment
6. Test at: https://stg.bizoholic.com/portal/login

---

## What Was Fixed

### Problem
Login failed with 401 errors after deploying v2.1.2-production:
- Console error: `/api/auth/me:1 Failed to load resource: 401`
- Client making **relative** API calls (`/api`) instead of **absolute** (`https://api.bizoholic.com/api`)

### Root Cause
Next.js requires `NEXT_PUBLIC_*` environment variables to be available **during build** to embed them in JavaScript bundles. Simply having `.env.production` file wasn't sufficient.

### Solution
1. **Updated Dockerfile** ([Dockerfile:19-35](./Dockerfile#L19-L35))
   - Added ARG declarations to accept build arguments
   - Convert ARGs to ENV variables for build stage

2. **Proper Image Naming**
   - Following naming convention: `staging-v2.1.4` and `staging-latest`
   - Created [IMAGE_NAMING_CONVENTION.md](./IMAGE_NAMING_CONVENTION.md)

3. **Production URLs Embedded**
   - Built with production API URLs as build arguments
   - API URLs now embedded in JavaScript bundles at build time

---

## Environment Variables (Already Set in Dokploy)

The following environment variables are already configured in Dokploy and **do not need to be changed**:

```env
NODE_ENV=production
PORT=3000
NEXT_TELEMETRY_DISABLED=1

# Authentication
JWT_SECRET=n62SLTZfZjKABOw04EjBWvjp6635XifgQP1+XRkfbac=
NEXTAUTH_SECRET=BQ8cXrPJhPp4MD/OT9GYNTE3DHpZjiIJM4kbPGXkcpY=
NEXTAUTH_URL=https://stg.bizoholic.com/portal

# API URLs (CRITICAL - Already correct)
NEXT_PUBLIC_API_URL=https://api.bizoholic.com/api
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com/api
BRAIN_API_BASE_URL=https://api.bizoholic.com/api
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/api/auth

# App Configuration
NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/portal
BASE_PATH=/portal
NEXT_PUBLIC_ENABLE_SOURCING=true
NEXT_PUBLIC_USE_MOCK_API=false
```

---

## Testing Checklist

After deployment, verify:

### 1. Clear Browser Cache
- Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
- Or use Incognito/Private window

### 2. Test Unauthenticated Flow
```
Visit: https://stg.bizoholic.com/portal/
Expected: Immediate redirect to /portal/login (no flash)
Should NOT see: Dashboard appearing briefly
```

### 3. Test Login
```
At login page:
Email: demo@bizosaas.com
Password: demo123

Expected:
- Redirect to /portal/dashboard
- Dashboard displays user information
- No console errors
```

### 4. Check Browser Console
```
Open DevTools (F12)
Check Console tab
Expected: NO errors like "/api/auth/me:1 Failed to load resource: 401"
```

### 5. Check Network Tab
```
Open DevTools (F12)
Go to Network tab
Filter by: "auth"
Expected: API calls show "https://api.bizoholic.com/api/auth/me" (absolute URL, not /api/auth/me)
```

---

## What's Different from v2.1.2-production

### v2.1.2-production (BROKEN)
```javascript
// In browser JavaScript bundle:
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api'
// Results in: API_BASE_URL = '/api' (relative path) ❌
// Browser makes call to: https://stg.bizoholic.com/api/auth/me → 404
```

### staging-v2.1.4 (FIXED)
```javascript
// In browser JavaScript bundle:
const API_BASE_URL = "https://api.bizoholic.com/api" || '/api'
// Results in: API_BASE_URL = 'https://api.bizoholic.com/api' (absolute URL) ✅
// Browser makes call to: https://api.bizoholic.com/api/auth/me → 200
```

---

## Image Details

**Repository**: `ghcr.io/bizoholic-digital/bizosaas-client-portal`
**Tags**:
- `staging-v2.1.6` (specific version)

**Digest**: `sha256:e9ec4278c27e47db82918d5e66ac13080643566e3e6c5a1e07e7a080fb4a7f7f`

**Built**: 2025-11-12 09:50 UTC
**Size**: 205 MB
**Image ID**: 99ca027e9f71

---

## Files Modified

All authentication fixes are included in this image:

1. [src/middleware.ts](./src/middleware.ts:7-39) - Server-side route protection
2. [src/app/page.tsx](./src/app/page.tsx:4-15) - Server-side auth check
3. [src/lib/auth-client.ts](./src/lib/auth-client.ts:13-15) - API URL configuration
4. [Dockerfile](./Dockerfile:19-35) - ARG/ENV for build-time variables

---

## Rollback Plan (If Needed)

If issues occur, rollback to previous version:

```bash
# Via Dokploy UI: Change image to
ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.0.32

# Or via CLI
docker service update --image ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.0.32 frontend-client-portal
```

---

## Support Information

**Demo Credentials**:
- Email: `demo@bizosaas.com`
- Password: `demo123`

**API Endpoints**:
- Login: `https://api.bizoholic.com/api/auth/login`
- Auth Check: `https://api.bizoholic.com/api/auth/me`
- Portal: `https://stg.bizoholic.com/portal/`

**Documentation**:
- [DEPLOYMENT_FINAL.md](./DEPLOYMENT_FINAL.md) - Detailed deployment guide
- [CLIENT_PORTAL_AUTH_FIX_COMPLETE.md](./CLIENT_PORTAL_AUTH_FIX_COMPLETE.md) - Complete fix documentation
- [IMAGE_NAMING_CONVENTION.md](./IMAGE_NAMING_CONVENTION.md) - Naming standards

---

## Next Steps After Successful Deployment

### Immediate
- [ ] Verify authentication works with demo credentials
- [ ] Confirm no console errors
- [ ] Test protected routes

### Short Term (This Week)
- [ ] Move JWT_SECRET and NEXTAUTH_SECRET to HashiCorp Vault
- [ ] Implement user registration flow
- [ ] Add forgot password functionality

### Medium Term (Next Sprint)
- [ ] Promote to production (use `prod-v2.1.4` tag)
- [ ] Implement tenant switching UI
- [ ] Add multi-factor authentication

---

**Deployment Ready**: ✅ YES
**Image**: `ghcr.io/bizoholic-digital/bizosaas-client-portal:staging-v2.1.6`
**Action Required**: Deploy via Dokploy UI and test

---

## Deployment Command Summary

```bash
# Image to deploy in Dokploy UI:
ghcr.io/bizoholic-digital/bizosaas-client-portal:staging-v2.1.6
```
