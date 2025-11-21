# Dokploy Environment Variable Updates
## Brain Gateway Integration - Exact Values to Use
**Date:** November 17, 2025

---

## 🔑 Core Principle

**For Production Dokploy Deployments:**
- Use **PUBLIC URL** for `NEXT_PUBLIC_*` variables (client-side): `https://api.bizoholic.com`
- Use **INTERNAL URL** for server-side variables: `http://backend-brain-gateway:8001`

---

## 📋 Updated Environment Variables

### 1. business-directory

**REPLACE ALL with:**

```bash
# ========================================
# Brain Gateway Configuration
# ========================================
NEXT_PUBLIC_API_URL=https://api.bizoholic.com
NEXT_PUBLIC_API_BASE_URL=https://api.bizoholic.com
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/auth
NEXT_PUBLIC_DIRECTORY_API_URL=https://api.bizoholic.com/directory

# ========================================
# Platform Configuration
# ========================================
NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/directory
NEXT_PUBLIC_PLATFORM_NAME=business-directory
NEXT_PUBLIC_TENANT_SLUG=business-directory

# ========================================
# Domain Configuration
# ========================================
NEXT_PUBLIC_STAGING_URL=https://stg.bizoholic.com/directory
NEXT_PUBLIC_PRODUCTION_URL=https://www.bizoholic.net/directory

# ========================================
# Google Maps (if available)
# ========================================
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=

# ========================================
# Feature Flags
# ========================================
NEXT_PUBLIC_ENABLE_REVIEWS=true
NEXT_PUBLIC_ENABLE_LISTINGS=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true

# ========================================
# Production Settings
# ========================================
NODE_ENV=production
PORT=3004
HOSTNAME=0.0.0.0
NEXT_TELEMETRY_DISABLED=1
```

**Changes Made:**
- ❌ Removed: `NEXT_PUBLIC_API_BASE_URL=http://bizosaas-saleor-api-8003:8000` (wrong service)
- ✅ Added: All Brain Gateway URLs pointing to `https://api.bizoholic.com`
- ✅ Added: Feature flags and proper platform configuration

---

### 2. client-portal

**REPLACE ALL with:**

```bash
# ========================================
# Brain Gateway Configuration
# ========================================
NEXT_PUBLIC_API_URL=https://api.bizoholic.com/api
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com/api
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/api/auth
BRAIN_API_BASE_URL=https://api.bizoholic.com/api

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
BASE_PATH=/portal

# ========================================
# Feature Flags
# ========================================
NEXT_PUBLIC_ENABLE_SOURCING=true
NEXT_PUBLIC_ENABLE_CRM=true
NEXT_PUBLIC_ENABLE_MARKETING=true
NEXT_PUBLIC_ENABLE_AUTOMATION=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
NEXT_PUBLIC_ENABLE_HITL=true
NEXT_PUBLIC_USE_MOCK_API=false

# ========================================
# Production Settings
# ========================================
NODE_ENV=production
PORT=3003
NEXT_TELEMETRY_DISABLED=1
```

**Changes Made:**
- ✅ Kept: All existing auth secrets (JWT_SECRET, NEXTAUTH_SECRET)
- ✅ Kept: All Brain Gateway URLs (already correct!)
- ✅ Changed: PORT from 3001 to 3003 (correct port for client portal)
- ✅ Added: Additional feature flags

---

### 3. coreldove-frontend

**REPLACE ALL with:**

```bash
# ========================================
# Brain Gateway Configuration
# ========================================
NEXT_PUBLIC_API_BASE_URL=https://api.bizoholic.com
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/auth

# ========================================
# Saleor API (through Brain Gateway)
# ========================================
NEXT_PUBLIC_SALEOR_API_URL=https://api.bizoholic.com/graphql

# ========================================
# Amazon Sourcing (through Brain Gateway)
# ========================================
NEXT_PUBLIC_AMAZON_SOURCING_URL=https://api.bizoholic.com/api/amazon

# ========================================
# Platform Configuration
# ========================================
NEXT_PUBLIC_STOREFRONT_URL=https://stg.coreldove.com
NEXT_PUBLIC_STOREFRONT_NAME=CoreLdove
NEXT_PUBLIC_PLATFORM_NAME=coreldove
NEXT_PUBLIC_TENANT_SLUG=coreldove

# ========================================
# Saleor Configuration
# ========================================
NEXT_PUBLIC_SALEOR_CHANNEL=default-channel

# ========================================
# Feature Flags
# ========================================
NEXT_PUBLIC_ENABLE_ACCOUNT=true
NEXT_PUBLIC_ENABLE_CHECKOUT=true
NEXT_PUBLIC_AI_ENABLED=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true

# ========================================
# Production Settings
# ========================================
NODE_ENV=production
PORT=3002
NEXT_TELEMETRY_DISABLED=1
```

**Changes Made:**
- ❌ Removed: `brain-gateway.coreldove.com` (wrong domain)
- ❌ Removed: `api.coreldove.com` (wrong domain)
- ✅ Added: All URLs now point to `https://api.bizoholic.com`
- ✅ Added: Proper platform configuration

---

### 4. bizoholic-frontend

**REPLACE ALL with:**

```bash
# ========================================
# Brain Gateway Configuration (Public URLs)
# ========================================
NEXT_PUBLIC_API_URL=https://api.bizoholic.com
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com
NEXT_PUBLIC_API_GATEWAY_URL=https://api.bizoholic.com
NEXT_PUBLIC_API_BASE_URL=https://api.bizoholic.com/api
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/auth

# ========================================
# Service URLs (through Brain Gateway)
# ========================================
NEXT_PUBLIC_CMS_URL=https://api.bizoholic.com/cms
NEXT_PUBLIC_WIZARDS_URL=https://api.bizoholic.com/wizards
NEXT_PUBLIC_AGENTS_URL=https://api.bizoholic.com/agents
NEXT_PUBLIC_SOCIAL_API_URL=https://api.bizoholic.com/social-media
NEXT_PUBLIC_COMM_API_URL=https://api.bizoholic.com/communications
NEXT_PUBLIC_CRM_URL=https://api.bizoholic.com/crm
NEXT_PUBLIC_COMMERCE_URL=https://api.bizoholic.com/commerce

# ========================================
# Internal Server-Side URLs (Docker network)
# ========================================
WAGTAIL_API_BASE_URL=http://backend-wagtail-cms:8000/api/v2

# ========================================
# Platform Configuration
# ========================================
NEXT_PUBLIC_SITE_URL=https://stg.bizoholic.com
NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com
NEXT_PUBLIC_PLATFORM_NAME=bizoholic
NEXT_PUBLIC_TENANT_SLUG=bizoholic

# ========================================
# Feature Flags
# ========================================
NEXT_PUBLIC_ENABLE_BLOG=true
NEXT_PUBLIC_ENABLE_SERVICES=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
NEXT_PUBLIC_ENABLE_HITL=true

# ========================================
# Production Settings
# ========================================
NODE_ENV=production
PORT=3001
HOSTNAME=0.0.0.0
NEXT_TELEMETRY_DISABLED=1
```

**Changes Made:**
- ✅ Changed: All `NEXT_PUBLIC_*` URLs from internal `http://backend-brain-gateway:8001` to public `https://api.bizoholic.com`
- ✅ Kept: Internal `WAGTAIL_API_BASE_URL` for server-side calls
- ✅ Added: Feature flags and platform configuration

**Why this change?**
- `NEXT_PUBLIC_*` variables are exposed to the browser → must use public URL
- Internal Docker URLs won't work from user's browser
- Server-side URLs (like Wagtail) can still use internal Docker network

---

### 5. admin-dashboard (BizOSaaS Admin)

**ADD ALL (currently empty):**

```bash
# ========================================
# Brain Gateway Configuration
# ========================================
NEXT_PUBLIC_API_URL=https://api.bizoholic.com
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/auth
NEXT_PUBLIC_ADMIN_API_URL=https://api.bizoholic.com/admin

# ========================================
# Authentication (Use SAME as client-portal)
# ========================================
JWT_SECRET=n62SLTZfZjKABOw04EjBWvjp6635XifgQP1+XRkfbac=
NEXTAUTH_SECRET=BQ8cXrPJhPp4MD/OT9GYNTE3DHpZjiIJM4kbPGXkcpY=
NEXTAUTH_URL=https://admin.bizoholic.com

# ========================================
# Platform Configuration
# ========================================
NEXT_PUBLIC_APP_URL=https://admin.bizoholic.com
NEXT_PUBLIC_PLATFORM_NAME=bizosaas-admin
NEXT_PUBLIC_TENANT_SLUG=bizosaas
NEXT_PUBLIC_REQUIRED_ROLE=SUPER_ADMIN

# ========================================
# Feature Flags
# ========================================
NEXT_PUBLIC_ENABLE_MONITORING=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
NEXT_PUBLIC_ENABLE_HITL=true
NEXT_PUBLIC_ENABLE_USER_MANAGEMENT=true
NEXT_PUBLIC_ENABLE_TENANT_MANAGEMENT=true

# ========================================
# Production Settings
# ========================================
NODE_ENV=production
PORT=3005
HOSTNAME=0.0.0.0
NEXT_TELEMETRY_DISABLED=1
```

**Notes:**
- ✅ Uses SAME JWT_SECRET and NEXTAUTH_SECRET as client-portal (shared auth)
- ✅ NEXTAUTH_URL is different (admin.bizoholic.com vs portal)
- ✅ Includes role-based access control (SUPER_ADMIN required)
- ✅ Ready for implementation once client-portal auth is stable

---

### 6. thrillring-gaming

**ADD ALL (currently empty):**

```bash
# ========================================
# Brain Gateway Configuration
# ========================================
NEXT_PUBLIC_API_URL=https://api.bizoholic.com
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/auth
NEXT_PUBLIC_GAMING_API_URL=https://api.bizoholic.com/gaming

# ========================================
# WebSocket Configuration
# ========================================
NEXT_PUBLIC_WEBSOCKET_URL=wss://api.bizoholic.com/gaming/ws

# ========================================
# Authentication (Use SAME as client-portal)
# ========================================
JWT_SECRET=n62SLTZfZjKABOw04EjBWvjp6635XifgQP1+XRkfbac=
NEXTAUTH_SECRET=BQ8cXrPJhPp4MD/OT9GYNTE3DHpZjiIJM4kbPGXkcpY=
NEXTAUTH_URL=https://stg.thrillring.com

# ========================================
# Platform Configuration
# ========================================
NEXT_PUBLIC_APP_URL=https://stg.thrillring.com
NEXT_PUBLIC_PLATFORM_NAME=thrillring
NEXT_PUBLIC_TENANT_SLUG=thrillring

# ========================================
# Feature Flags
# ========================================
NEXT_PUBLIC_ENABLE_TOURNAMENTS=true
NEXT_PUBLIC_ENABLE_LEADERBOARD=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
NEXT_PUBLIC_ENABLE_HITL=true
NEXT_PUBLIC_ENABLE_REALTIME=true

# ========================================
# Production Settings
# ========================================
NODE_ENV=production
PORT=3006
HOSTNAME=0.0.0.0
NEXT_TELEMETRY_DISABLED=1
```

**Notes:**
- ✅ Uses SAME JWT_SECRET and NEXTAUTH_SECRET as client-portal
- ✅ Includes WebSocket URL for real-time gaming features
- ✅ Gaming-specific feature flags

---

### 7. saleor-dashboard

**KEEP AS IS (DO NOT CHANGE):**

```bash
# Saleor Dashboard - Keep existing configuration
# This is the Saleor Admin Interface, NOT part of our frontend stack
# It connects directly to Saleor API for e-commerce management

# Current: http://10.0.1.47:8000/graphql/
# This is correct for Saleor admin dashboard
```

**Why keep it?**
- Saleor Dashboard is the ADMIN interface for managing Saleor e-commerce
- It's separate from our frontend applications
- It connects directly to Saleor API, not through Brain Gateway
- It's for internal use (managing products, orders, etc.)

---

## 🔐 Authentication Strategy

### Shared Authentication Across All Frontends

**Key Principle:** All frontends share the SAME authentication backend and secrets

```bash
# These should be IDENTICAL across all frontends:
JWT_SECRET=n62SLTZfZjKABOw04EjBWvjp6635XifgQP1+XRkfbac=
NEXTAUTH_SECRET=BQ8cXrPJhPp4MD/OT9GYNTE3DHpZjiIJM4kbPGXkcpY=

# Only NEXTAUTH_URL changes per frontend:
# client-portal:    https://stg.bizoholic.com/portal
# admin-dashboard:  https://admin.bizoholic.com
# thrillring:       https://stg.thrillring.com
# etc.
```

### Why This Works:

1. ✅ **Single Sign-On (SSO):** Users log in once, authenticated everywhere
2. ✅ **Shared Sessions:** JWT tokens work across all platforms
3. ✅ **Centralized Auth:** All auth requests go to Brain Gateway `/auth` endpoint
4. ✅ **No Redundant Code:** Same auth logic, same backend service
5. ✅ **Easier Maintenance:** Update auth in one place, applies everywhere

### Implementation Status:

- ✅ **client-portal:** Auth working (being debugged/refined)
- ⏳ **admin-dashboard:** Waiting for client-portal auth to stabilize
- ⏳ **thrillring-gaming:** Waiting for client-portal auth to stabilize
- ⏳ **business-directory:** Needs auth implementation
- ⏳ **bizoholic-frontend:** Needs auth implementation
- ⏳ **coreldove-frontend:** Needs auth implementation

**Next Steps for Auth:**
1. Finish fixing client-portal authentication issues
2. Once stable, replicate the auth components to other frontends
3. All frontends will use the same auth flow and secrets

---

## 📊 Summary of Changes

| Frontend | Current Issue | Fix Applied |
|----------|--------------|-------------|
| business-directory | Wrong API URL (pointing to Saleor) | ✅ Now points to Brain Gateway |
| client-portal | PORT wrong (3001), otherwise good | ✅ Fixed PORT to 3003 |
| coreldove-frontend | Wrong domains (brain-gateway.coreldove.com) | ✅ Now uses api.bizoholic.com |
| bizoholic-frontend | Internal Docker URLs in public vars | ✅ Changed to public URLs |
| admin-dashboard | Empty config | ✅ Full config added |
| thrillring-gaming | Empty config | ✅ Full config added |
| saleor-dashboard | N/A | ⚠️ Keep as-is (different purpose) |

---

## 🚀 Deployment Order

**Recommended order to update and redeploy:**

1. ✅ **client-portal** (already has good config, just fix PORT)
2. **bizoholic-frontend** (main website, high priority)
3. **coreldove-frontend** (e-commerce, high priority)
4. **business-directory** (customer-facing)
5. **thrillring-gaming** (gaming platform)
6. **admin-dashboard** (internal, can wait for auth fix)

**After each update:**
1. Update environment variables in Dokploy
2. Click "Redeploy"
3. Monitor deployment logs
4. Test the frontend URL
5. Verify API calls go to `https://api.bizoholic.com`

---

## ✅ Validation Checklist

After updating each frontend, verify:

- [ ] Service restarts successfully
- [ ] Frontend loads at correct URL
- [ ] No CORS errors in browser console
- [ ] API calls show `https://api.bizoholic.com` in Network tab
- [ ] Authentication flow works (if implemented)
- [ ] No 404 errors for API endpoints
- [ ] Brain Gateway logs show incoming requests

---

**Ready to copy-paste into Dokploy!** 🚀

Each section above can be directly copied into the Dokploy environment variable editor for the respective service.