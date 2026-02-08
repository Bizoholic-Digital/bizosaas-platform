# Frontend Deployment Analysis
## Existing Dokploy vs New Brain Gateway Configuration
**Date:** November 17, 2025

---

## 📊 Deployment Comparison

### Existing Dokploy Deployments

| # | Dokploy Service Name | Created | Status |
|---|---------------------|---------|---------|
| 1 | bizoholic-frontend | 21 days ago | ✅ Deployed |
| 2 | coreldove-frontend | 21 days ago | ✅ Deployed |
| 3 | client-portal | 21 days ago | ✅ Deployed |
| 4 | business-directory | 21 days ago | ✅ Deployed |
| 5 | admin-dashboard | 21 days ago | ✅ Deployed |
| 6 | thrillring-gaming | 21 days ago | ✅ Deployed |
| 7 | saleor-dashboard | 14 days ago | ✅ Deployed |

### Our New Configuration

| # | Config Name | Port | .env.production | Brain Gateway |
|---|-------------|------|----------------|---------------|
| 1 | bizoholic-frontend | 3001 | ✅ Created | ✅ Configured |
| 2 | coreldove-storefront | 3002 | ✅ Created | ✅ Configured |
| 3 | client-portal | 3003 | ✅ Created | ✅ Configured |
| 4 | business-directory | 3004 | ✅ Created | ✅ Configured |
| 5 | bizosaas-admin | 3005 | ✅ Created | ✅ Configured |
| 6 | thrillring-gaming | 3006 | ✅ Created | ✅ Configured |
| 7 | analytics-dashboard | 3007 | ✅ Created | ✅ Configured |

---

## 🔍 Gap Analysis

### ✅ Matching Services (6/7)
These services exist in both Dokploy and our configuration:

1. **bizoholic-frontend** ✅
   - Dokploy: bizoholic-frontend
   - Config: bizoholic-frontend
   - Action: **UPDATE**

2. **coreldove-frontend** ⚠️ (name mismatch)
   - Dokploy: coreldove-frontend
   - Config: coreldove-storefront
   - Action: **UPDATE** (same service, different name in config)

3. **client-portal** ✅
   - Dokploy: client-portal
   - Config: client-portal
   - Action: **UPDATE**

4. **business-directory** ✅
   - Dokploy: business-directory
   - Config: business-directory
   - Action: **UPDATE**

5. **admin-dashboard** ⚠️ (name mismatch)
   - Dokploy: admin-dashboard
   - Config: bizosaas-admin
   - Action: **UPDATE** (same service, different name in config)

6. **thrillring-gaming** ✅
   - Dokploy: thrillring-gaming
   - Config: thrillring-gaming
   - Action: **UPDATE**

### ❌ Mismatched Services (1/7)

7. **Analytics vs Saleor Dashboard**
   - Dokploy: **saleor-dashboard** (Saleor admin interface)
   - Config: **analytics-dashboard** (Superset analytics)
   - Issue: These are DIFFERENT applications
   - Action: **DEPLOY NEW** analytics-dashboard

---

## 🎯 Recommended Approach

### **RECOMMENDATION: UPDATE existing deployments, DO NOT REPLACE**

**Rationale:**
1. ✅ Services are already running and configured in Dokploy
2. ✅ We only need to update environment variables to use Brain Gateway
3. ✅ No structural changes to the applications themselves
4. ✅ Minimal downtime with rolling updates
5. ✅ Preserves existing Dokploy configurations (domains, resources, etc.)

---

## 📋 Update Plan

### Step 1: Update Environment Variables in Dokploy

For each existing deployment, update the environment variables to match the new `.env.production` files:

#### 1. bizoholic-frontend
```bash
NEXT_PUBLIC_API_URL=https://api.bizoholic.com
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/auth
NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com
NEXT_PUBLIC_PLATFORM_NAME=bizoholic
NEXT_PUBLIC_TENANT_SLUG=bizoholic
PORT=3001
NODE_ENV=production
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
NEXT_PUBLIC_ENABLE_HITL=true
NEXT_PUBLIC_ENABLE_ANALYTICS=true
```

#### 2. coreldove-frontend (update to use Brain Gateway)
```bash
NEXT_PUBLIC_API_BASE_URL=https://api.bizoholic.com
NEXT_PUBLIC_SALEOR_API_URL=https://api.bizoholic.com/graphql
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/auth
NEXT_PUBLIC_STOREFRONT_URL=https://stg.coreldove.com
NEXT_PUBLIC_PLATFORM_NAME=coreldove
NEXT_PUBLIC_TENANT_SLUG=coreldove
PORT=3002
NODE_ENV=production
SALEOR_CHANNEL=default-channel
NEXT_PUBLIC_ENABLE_ACCOUNT=true
NEXT_PUBLIC_ENABLE_CHECKOUT=true
```

#### 3. client-portal
```bash
NEXT_PUBLIC_API_URL=https://api.bizoholic.com
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/auth
NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/portal
NEXT_PUBLIC_PLATFORM_NAME=client-portal
NEXT_PUBLIC_TENANT_SLUG=client-portal
PORT=3003
NODE_ENV=production
NEXT_PUBLIC_ENABLE_CRM=true
NEXT_PUBLIC_ENABLE_MARKETING=true
NEXT_PUBLIC_ENABLE_AUTOMATION=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
```

#### 4. business-directory
```bash
NEXT_PUBLIC_API_URL=https://api.bizoholic.com
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/auth
NEXT_PUBLIC_DIRECTORY_API_URL=https://api.bizoholic.com/directory
NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/directory
NEXT_PUBLIC_PLATFORM_NAME=business-directory
NEXT_PUBLIC_TENANT_SLUG=business-directory
PORT=3004
NODE_ENV=production
NEXT_PUBLIC_ENABLE_REVIEWS=true
NEXT_PUBLIC_ENABLE_LISTINGS=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
```

#### 5. admin-dashboard
```bash
NEXT_PUBLIC_API_URL=https://api.bizoholic.com
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/auth
NEXT_PUBLIC_ADMIN_API_URL=https://api.bizoholic.com/admin
NEXT_PUBLIC_APP_URL=https://admin.bizoholic.com
NEXT_PUBLIC_PLATFORM_NAME=bizosaas-admin
NEXT_PUBLIC_REQUIRED_ROLE=SUPER_ADMIN
PORT=3005
NODE_ENV=production
NEXT_PUBLIC_ENABLE_MONITORING=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
```

#### 6. thrillring-gaming
```bash
NEXT_PUBLIC_API_URL=https://api.bizoholic.com
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/auth
NEXT_PUBLIC_GAMING_API_URL=https://api.bizoholic.com/gaming
NEXT_PUBLIC_WEBSOCKET_URL=wss://api.bizoholic.com/gaming/ws
NEXT_PUBLIC_APP_URL=https://stg.thrillring.com
NEXT_PUBLIC_PLATFORM_NAME=thrillring
NEXT_PUBLIC_TENANT_SLUG=thrillring
PORT=3006
NODE_ENV=production
NEXT_PUBLIC_ENABLE_TOURNAMENTS=true
NEXT_PUBLIC_ENABLE_LEADERBOARD=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
```

### Step 2: Verify GitHub Integration

Ensure each Dokploy application is configured with:
- **Repository:** `Bizoholic-Digital/bizosaas-platform`
- **Branch:** `main`
- **Auto Deploy:** Enabled (optional)

### Step 3: Trigger Redeployments

After updating environment variables, trigger redeploy for each service in this order:

1. ✅ **client-portal** (already triggered successfully)
2. bizoholic-frontend
3. coreldove-frontend
4. business-directory
5. admin-dashboard
6. thrillring-gaming
7. (Deploy new) analytics-dashboard

### Step 4: Deploy Analytics Dashboard (New)

Create a new Dokploy application for analytics-dashboard:
```bash
NEXT_PUBLIC_API_URL=https://api.bizoholic.com
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/auth
NEXT_PUBLIC_ANALYTICS_API_URL=https://api.bizoholic.com/analytics
NEXT_PUBLIC_SUPERSET_URL=https://api.bizoholic.com/superset
NEXT_PUBLIC_APP_URL=https://analytics.bizoholic.com
NEXT_PUBLIC_PLATFORM_NAME=analytics
NEXT_PUBLIC_TENANT_SLUG=bizosaas
PORT=3007
NODE_ENV=production
NEXT_PUBLIC_ENABLE_CUSTOM_DASHBOARDS=true
NEXT_PUBLIC_ENABLE_EXPORTS=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
```

---

## 🔧 Implementation Steps

### Option A: Update via Dokploy UI (Recommended)

1. **Access Dokploy Dashboard:**
   ```
   https://dk4.bizoholic.com/dashboard
   ```

2. **For each application:**
   - Navigate to the application settings
   - Go to "Environment Variables" section
   - Update/add the variables from above
   - Click "Save"
   - Click "Redeploy" to apply changes

3. **Monitor deployments:**
   - Watch deployment logs for each service
   - Verify services restart successfully
   - Check health endpoints

### Option B: Update via Dokploy API (Automated)

Create a script to update environment variables via API:
```bash
#!/bin/bash
# update-dokploy-env-vars.sh

DOKPLOY_URL="https://dk4.bizoholic.com"
DOKPLOY_API_KEY="dk4ixNgzxiGcZWrjlvocbOJqTLjlZsJUEgmTJjXYvLVSwiUBUPARxklyNFyVQRDHBa"

# Get application IDs from Dokploy UI first
# Then update environment variables for each app
```

---

## ⚠️ Critical Considerations

### 1. Saleor Dashboard vs Analytics Dashboard

**Question:** What is the purpose of "saleor-dashboard" in your Dokploy?

- If it's the **Saleor Admin Dashboard** (for managing e-commerce), keep it
- If it was meant to be **Analytics Dashboard** (Superset), replace it

**Recommendation:**
- Keep saleor-dashboard (it's the Saleor admin interface)
- Deploy analytics-dashboard as a NEW application
- You'll have 8 frontend services total

### 2. Zero-Downtime Deployment

Since these are production services:
- Update environment variables during low-traffic hours
- Deploy one service at a time
- Monitor health after each deployment
- Roll back if issues occur

### 3. DNS/Domain Verification

Ensure domains are correctly configured:
- ✅ https://stg.bizoholic.com → bizoholic-frontend
- ✅ https://stg.coreldove.com → coreldove-frontend
- ✅ https://stg.bizoholic.com/portal → client-portal
- ✅ https://stg.bizoholic.com/directory → business-directory
- ✅ https://admin.bizoholic.com → admin-dashboard
- ✅ https://stg.thrillring.com → thrillring-gaming
- ❓ https://analytics.bizoholic.com → analytics-dashboard (NEW)

---

## ✅ Validation Checklist

After updating each service, verify:

- [ ] Service restarts successfully
- [ ] Application loads at its URL
- [ ] API calls go to `https://api.bizoholic.com`
- [ ] No CORS errors in browser console
- [ ] Authentication works (login/logout)
- [ ] No errors in application logs
- [ ] Brain Gateway receives requests (check logs)

---

## 🎯 Final Recommendation

### **UPDATE EXISTING DEPLOYMENTS**

**Do NOT replace or recreate the applications.** Instead:

1. ✅ **Update environment variables** for all 6 existing deployments
2. ✅ **Redeploy each service** to pick up new Brain Gateway configuration
3. ✅ **Deploy analytics-dashboard** as a new 8th application
4. ✅ **Keep saleor-dashboard** (it serves a different purpose)

**Why Update vs Replace?**
- Preserves existing Dokploy configuration (domains, resources, health checks)
- Maintains deployment history
- Less risk of misconfiguration
- Faster deployment
- No DNS changes needed

**Estimated Time:**
- Environment variable updates: 15-20 minutes (manual) or 5 minutes (automated)
- Redeployments: 5-10 minutes per service × 6 = 30-60 minutes
- Total: ~45-80 minutes for all services

---

**Status:** ✅ Analysis Complete | Ready for Implementation
**Next Action:** Update environment variables in Dokploy for existing deployments