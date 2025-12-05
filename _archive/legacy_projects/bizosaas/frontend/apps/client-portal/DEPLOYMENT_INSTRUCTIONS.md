# Client Portal Deployment Instructions

## Quick Reference

**Service to Update**: Client Portal (frontend)
**Current Image**: `ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.0.32`
**New Image**: `ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.1.0-fixed-auth`
**Platform**: Dokploy on KVM4 (72.60.219.244)
**Access URL**: https://stg.bizoholic.com/portal/

---

## Environment Variables to Set in Dokploy

```env
NODE_ENV=production
PORT=3001
NEXT_TELEMETRY_DISABLED=1

# Authentication
JWT_SECRET=n62SLTZfZjKABOw04EjBWvjp6635XifgQP1+XRkfbac=
NEXTAUTH_SECRET=BQ8cXrPJhPp4MD/OT9GYNTE3DHpZjiIJM4kbPGXkcpY=
NEXTAUTH_URL=https://stg.bizoholic.com/portal

# API URLs (CRITICAL - Fixed paths)
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

### Key Changes from Your Current Settings:
1. **PORT**: Changed from `3000` to `3001` (matches Dockerfile)
2. **Added**: `BRAIN_API_BASE_URL=https://api.bizoholic.com/api`
3. **Kept**: All your existing URLs and secrets

---

## Deployment Steps

### Step 1: Update Dokploy Environment Variables
1. Log in to Dokploy: https://KVM4-DOKPLOY-URL
2. Navigate to Services → Client Portal
3. Go to Environment Variables section
4. Update `PORT` from `3000` to `3001`
5. Verify all API URLs end with `/api`
6. Save changes

### Step 2: Update Docker Image
1. In the same Client Portal service
2. Find the "Image" or "Docker Image" field
3. Change from: `ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.0.32`
4. Change to: `ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.1.0-fixed-auth`
5. Save changes

### Step 3: Redeploy
1. Click "Redeploy" or "Deploy" button
2. Wait for deployment to complete (~2-3 minutes)
3. Check deployment logs for any errors

### Step 4: Verify Deployment
1. Visit: https://stg.bizoholic.com/portal/
2. **Expected**: Immediately redirected to `/portal/login` (no flash)
3. **Should NOT see**: Dashboard appearing briefly before redirect

### Step 5: Test Login
1. At login page, enter credentials:
   - Email: `demo@bizosaas.com`
   - Password: `demo123`
2. Click "Sign In"
3. **Expected**: Redirect to `/portal/dashboard`
4. **Should see**: Dashboard with user data
5. **Check console**: No errors

---

## Testing Checklist

### ✅ Authentication Flow
- [ ] Visit `/portal/` → redirects to `/portal/login` immediately
- [ ] No flash of dashboard content
- [ ] Login page loads correctly
- [ ] Form accepts credentials
- [ ] Login succeeds with demo credentials
- [ ] Redirects to `/portal/dashboard` after login
- [ ] Dashboard displays user information
- [ ] No console errors

### ✅ Protected Routes
- [ ] Visit `/portal/dashboard` without login → redirects to login
- [ ] Visit `/portal/settings` without login → redirects to login with `?from=/settings`
- [ ] After login, can access all protected routes
- [ ] Logout redirects to login page

### ✅ API Integration
- [ ] Login calls `https://api.bizoholic.com/api/auth/login`
- [ ] Auth check calls `https://api.bizoholic.com/api/auth/me`
- [ ] Cookies are set correctly (`access_token`)
- [ ] API responses are in correct format

---

## Troubleshooting

### Issue: Still seeing flash behavior

**Check**:
1. Browser cache cleared?
2. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
3. Incognito/Private window test
4. Check if new image was actually pulled
5. Verify environment variables are correct

**Debug**:
```bash
# SSH to KVM4
ssh root@72.60.219.244

# Check running container
docker ps | grep client-portal

# Check image tag
docker inspect <container-id> | grep Image

# Should show: ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.1.0-fixed-auth
```

### Issue: Login fails

**Check**:
1. Network tab shows POST to `https://api.bizoholic.com/api/auth/login`
2. Response status is 200
3. Response has `{"success": true, "user": {...}}`
4. Cookies are being set

**Debug**:
```bash
# Test Brain Gateway directly
curl -X POST https://api.bizoholic.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@bizosaas.com", "password": "demo123"}'

# Should return:
# {"success": true, "token": "...", "user": {...}}
```

### Issue: Redirect loops

**Check**:
1. `BASE_PATH=/portal` is set
2. `NEXTAUTH_URL=https://stg.bizoholic.com/portal`
3. No trailing slashes in URLs
4. Middleware is not conflicting

### Issue: 404 on dashboard

**Check**:
1. `BASE_PATH=/portal` is set correctly
2. Next.js standalone output built correctly
3. Traefik routing configured for `/portal` prefix

---

## Rollback Plan

If issues occur, rollback to previous version:

```bash
# In Dokploy UI
# Change image back to:
ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.0.32

# Redeploy

# Or via CLI
docker service update --image ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.0.32 frontend-client-portal
```

---

## What Was Fixed

### Before (v2.0.32):
- ❌ Middleware was a stub (no auth check)
- ❌ Root page redirected to dashboard unconditionally
- ❌ Client-side-only auth validation
- ❌ Flash behavior (dashboard → login)

### After (v2.1.0-fixed-auth):
- ✅ Middleware checks cookies and redirects
- ✅ Root page checks auth server-side
- ✅ Server-side + client-side auth validation
- ✅ Clean redirect (no flash)

### Files Modified:
1. `src/middleware.ts` - Server-side route protection
2. `src/app/page.tsx` - Server-side auth check
3. `src/lib/auth-client.ts` - Brain Gateway response handling
4. `.env.production` - Production environment config

---

## Support

**Documentation**: [CLIENT_PORTAL_AUTH_FIX_COMPLETE.md](./CLIENT_PORTAL_AUTH_FIX_COMPLETE.md)
**Brain Gateway Auth**: https://api.bizoholic.com/api/auth/login
**Demo Credentials**: demo@bizosaas.com / demo123

---

**Deployment Date**: 2025-11-12
**Version**: v2.1.0-fixed-auth
**Status**: Ready for Deployment
