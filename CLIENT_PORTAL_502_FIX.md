# Client Portal 502 Error - Root Cause and Fix

**Date:** November 17, 2025
**Status:** 🔴 CRITICAL - Missing Environment Variables

---

## 🔍 Root Cause Analysis

### Comparison: Local (Working) vs Production (502 Error)

| Variable | Local .env.local | Production .env.production | Status |
|----------|------------------|---------------------------|---------|
| **BASE_PATH** | ❌ Not set | ❌ Not set | 🔴 **MISSING** |
| **JWT_SECRET** | ✅ Set (placeholder) | ❌ Not set | 🔴 **MISSING** |
| **NEXTAUTH_SECRET** | ✅ Set (placeholder) | ❌ Not set | 🔴 **MISSING** |
| **NEXTAUTH_URL** | ✅ http://localhost:3001 | ❌ Not set | 🔴 **MISSING** |
| **BRAIN_API_BASE_URL** | ✅ http://localhost:8001/api | ❌ Not set | 🔴 **MISSING** |
| PORT | ✅ 3003 (package.json) | ✅ 3003 | ✅ Correct |
| NEXT_PUBLIC_API_URL | ✅ localhost:8001/api | ✅ api.bizoholic.com | ✅ Correct |

---

## 🚨 Critical Issue: Missing BASE_PATH

### Why BASE_PATH=/portal is Required

From [next.config.js:24](bizosaas/frontend/apps/client-portal/next.config.js#L24):
```javascript
basePath: process.env.BASE_PATH || '',
```

**Problem:**
- Next.js reads `BASE_PATH` from environment variables
- Without it, the app serves at root path `/` instead of `/portal`
- Traefik forwards requests to `/portal`, but the app doesn't recognize this path
- Result: **502 Bad Gateway** because routing fails

**Local vs Production:**
- **Local:** Works at `http://localhost:3001` (root path, no BASE_PATH needed)
- **Production:** Must work at `https://stg.bizoholic.com/portal` (subpath, requires BASE_PATH=/portal)

---

## 🔐 Critical Issue: Missing Authentication Variables

### Why JWT_SECRET and NEXTAUTH_SECRET are Required

From [middleware.ts:14](bizosaas/frontend/apps/client-portal/src/middleware.ts#L14):
```typescript
const refreshToken = request.cookies.get('refresh_token')
```

The middleware checks for authentication cookies, which are signed using JWT_SECRET and NEXTAUTH_SECRET.

**Problem:**
- Without these secrets, NextAuth cannot:
  - Sign JWT tokens
  - Verify refresh tokens
  - Maintain user sessions
- Result: Authentication fails, all protected routes inaccessible

### Why NEXTAUTH_URL is Required

NextAuth requires `NEXTAUTH_URL` to:
- Generate callback URLs
- Handle OAuth redirects
- Construct absolute URLs for emails

**Problem:**
- Without NEXTAUTH_URL, NextAuth cannot initialize properly
- Authentication endpoints fail
- Login/logout flows break

---

## 🔧 Complete Fix: Add Missing Variables to Dokploy

### Current Dokploy Environment (What You Have)

```bash
# ✅ These are correct and already set
NEXT_PUBLIC_API_URL=https://api.bizoholic.com
NEXT_PUBLIC_API_BASE_URL=https://api.bizoholic.com
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/auth
NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/portal
NEXT_PUBLIC_PLATFORM_NAME=client-portal
NEXT_PUBLIC_TENANT_SLUG=client-portal
PORT=3003
NODE_ENV=production
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
NEXT_PUBLIC_ENABLE_HITL=true
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_CRM=true
NEXT_PUBLIC_ENABLE_MARKETING=true
NEXT_PUBLIC_ENABLE_AUTOMATION=true
NEXT_PUBLIC_ENABLE_MULTI_TENANT=true
```

### 🚨 ADD THESE MISSING VARIABLES

```bash
# ========================================
# CRITICAL: BASE_PATH for Subpath Routing
# ========================================
BASE_PATH=/portal

# ========================================
# CRITICAL: Authentication Secrets
# ========================================
JWT_SECRET=n62SLTZfZjKABOw04EjBWvjp6635XifgQP1+XRkfbac=
NEXTAUTH_SECRET=BQ8cXrPJhPp4MD/OT9GYNTE3DHpZjiIJM4kbPGXkcpY=
NEXTAUTH_URL=https://stg.bizoholic.com/portal

# ========================================
# Server-Side Brain Gateway URL
# ========================================
BRAIN_API_BASE_URL=https://api.bizoholic.com/api

# ========================================
# Additional Recommended Variables
# ========================================
NEXT_PUBLIC_TENANT_SLUG=bizosaas
NEXT_PUBLIC_ENABLE_SOURCING=true
NEXT_PUBLIC_USE_MOCK_API=false
NEXT_TELEMETRY_DISABLED=1
```

---

## ✅ Complete Environment Variable List for Dokploy

**Copy this entire block into Dokploy → client-portal → Environment Variables:**

```bash
# ========================================
# Brain Gateway Configuration
# ========================================
NEXT_PUBLIC_API_URL=https://api.bizoholic.com/api
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com/api
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/api/auth
BRAIN_API_BASE_URL=https://api.bizoholic.com/api

# ========================================
# CRITICAL: BASE_PATH for /portal routing
# ========================================
BASE_PATH=/portal

# ========================================
# Authentication (Keep existing secrets!)
# ========================================
JWT_SECRET=n62SLTZfZjKABOw04EjBWvjp6635XifgQP1+XRkfbac=
NEXTAUTH_SECRET=BQ8cXrPJhPp4MD/OT9GYNTE3DHpZjiIJM4kbPGXkcpY=
NEXTAUTH_URL=https://stg.bizoholic.com/portal

# ========================================
# Platform Configuration
# ========================================
NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/portal
NEXT_PUBLIC_PLATFORM_NAME=client-portal
NEXT_PUBLIC_TENANT_SLUG=bizosaas

# ========================================
# Feature Flags
# ========================================
NEXT_PUBLIC_ENABLE_SOURCING=true
NEXT_PUBLIC_ENABLE_CRM=true
NEXT_PUBLIC_ENABLE_MARKETING=true
NEXT_PUBLIC_ENABLE_AUTOMATION=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
NEXT_PUBLIC_ENABLE_HITL=true
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_MULTI_TENANT=true
NEXT_PUBLIC_USE_MOCK_API=false

# ========================================
# Production Settings
# ========================================
NODE_ENV=production
PORT=3003
NEXT_TELEMETRY_DISABLED=1
```

---

## 📋 Step-by-Step Fix Instructions

### 1. Access Dokploy Dashboard
```
https://dk4.bizoholic.com/dashboard
```

### 2. Navigate to client-portal Service
- Click on "client-portal" service
- Go to "Environment Variables" tab

### 3. Add Missing Variables

**Option A: Add Only Missing Variables**
Add these 5 critical variables:
```bash
BASE_PATH=/portal
JWT_SECRET=n62SLTZfZjKABOw04EjBWvjp6635XifgQP1+XRkfbac=
NEXTAUTH_SECRET=BQ8cXrPJhPp4MD/OT9GYNTE3DHpZjiIJM4kbPGXkcpY=
NEXTAUTH_URL=https://stg.bizoholic.com/portal
BRAIN_API_BASE_URL=https://api.bizoholic.com/api
```

**Option B: Replace All Variables** (Recommended)
- Clear all existing variables
- Paste the complete environment variable list from above
- Ensures consistency and no missing variables

### 4. Save Changes
- Click "Save" or "Update" button

### 5. Redeploy Service
- Click "Redeploy" or "Rebuild" button
- Wait for deployment to complete (check logs)

### 6. Verify Fix
```bash
# Test the endpoint
curl -I https://stg.bizoholic.com/portal

# Expected result: 200 OK (not 502)
# If still getting 502, check deployment logs
```

---

## 🔍 Verification Checklist

After redeployment, verify:

- [ ] Service status shows "Running" (not "Failed" or "Restarting")
- [ ] Deployment logs show "Server listening on port 3003"
- [ ] Deployment logs show "Using basePath: /portal"
- [ ] No errors about missing environment variables
- [ ] `curl https://stg.bizoholic.com/portal` returns 200 OK (not 502)
- [ ] Browser loads https://stg.bizoholic.com/portal without errors
- [ ] Login page accessible at https://stg.bizoholic.com/portal/login
- [ ] API calls in Network tab go to https://api.bizoholic.com

---

## 🚨 If Still Getting 502 After Fix

### Check Deployment Logs

1. **In Dokploy Dashboard:**
   - Go to client-portal → Logs tab
   - Look for errors during startup

2. **Common Issues to Look For:**
   ```
   ❌ "Error: Invalid basePath"
   ❌ "NEXTAUTH_URL must be configured"
   ❌ "Port 3003 already in use"
   ❌ "Cannot find module..."
   ❌ "Error: JWT_SECRET is required"
   ```

3. **Check Container Status:**
   ```bash
   # If you have SSH access to VPS
   docker ps | grep client-portal
   docker logs <container-id>
   ```

### Possible Additional Issues

1. **Port Conflict:**
   - Ensure no other service is using port 3003
   - Check Dokploy port mappings are correct: 3003 → 3003

2. **Traefik Routing:**
   - Verify Traefik labels include PathPrefix=/portal
   - Check Traefik dashboard for routes

3. **Build Errors:**
   - Check if build completed successfully
   - Look for TypeScript errors or missing dependencies

---

## 📊 Expected Behavior After Fix

### Before Fix (Current State)
```
User Request → Traefik → https://stg.bizoholic.com/portal
                 ↓
          client-portal container (port 3003)
                 ↓
     App serves at "/" (no BASE_PATH)
                 ↓
          Route "/portal" not found
                 ↓
            502 Bad Gateway ❌
```

### After Fix (Expected)
```
User Request → Traefik → https://stg.bizoholic.com/portal
                 ↓
          client-portal container (port 3003)
                 ↓
     App serves at "/portal" (BASE_PATH set)
                 ↓
          Route "/portal" matches
                 ↓
            200 OK ✅
```

---

## 📈 Impact Assessment

### Current Status
- **Affected:** client-portal only
- **Other Services:** Working correctly (4/6 frontends operational)
- **Root Cause:** Incomplete environment variable configuration

### After Fix
- **Expected:** 5/6 frontends working (83% success rate)
- **Remaining Issue:** admin-dashboard (404 - not deployed yet)
- **Next Priority:** Deploy admin-dashboard

---

## 🎯 Priority and Timeline

**Priority:** 🔴 **CRITICAL** (Blocks client portal access)

**Estimated Fix Time:**
- Add environment variables: 2 minutes
- Redeploy service: 3-5 minutes
- Verify and test: 2 minutes
- **Total: ~10 minutes**

**Business Impact:**
- **High:** Client portal is customer-facing
- Users cannot access CRM, marketing, automation features
- All authentication flows broken

---

**Next Steps:**
1. Add the 5 missing environment variables to Dokploy
2. Redeploy client-portal
3. Verify https://stg.bizoholic.com/portal returns 200 OK
4. Test login functionality
5. Proceed to configure admin-dashboard

---

**Created:** November 17, 2025
**Status:** 🔧 Ready for Implementation
