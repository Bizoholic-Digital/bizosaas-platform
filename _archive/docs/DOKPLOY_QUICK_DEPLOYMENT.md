# 🚀 Quick Dokploy Deployment Guide

## 📍 **ACCESS YOUR DOKPLOY**
URL: `dk.bizoholic.com`

---

## 🏗️ **PHASE 1: Infrastructure Project (6 containers)**

### Create Project
1. **Projects** → **Create Project**
2. **Name**: `bizosaas-infrastructure-staging`
3. **Description**: `Infrastructure services for staging (6 containers)`

### Add Application
1. **Applications** → **Create Application**
2. **Type**: Docker Compose
3. **Name**: `infrastructure-services`
4. **Source**: Repository
5. **Repository**: `https://github.com/Bizoholic-Digital/bizosaas-platform.git`
6. **Branch**: `main`
7. **Docker Compose Path**: `dokploy-infrastructure-staging.yml`

### Deploy
- Click **"Deploy"**
- Wait 15-20 minutes
- Verify 6 containers running

---

## 🔧 **PHASE 2: Backend Services Project (8 containers)**

### Create Project
1. **Projects** → **Create Project**
2. **Name**: `bizosaas-backend-staging`
3. **Description**: `Backend services for staging (8 containers)`

### Add Application
1. **Applications** → **Create Application**
2. **Type**: Docker Compose
3. **Name**: `backend-services`
4. **Source**: Repository
5. **Repository**: `https://github.com/Bizoholic-Digital/bizosaas-platform.git`
6. **Branch**: `main`
7. **Docker Compose Path**: `dokploy-backend-staging-corrected.yml`

### Environment Variables (CRITICAL!)
Add these before deploying:
```
OPENROUTER_API_KEY=your_staging_key
OPENAI_API_KEY=your_staging_key
ANTHROPIC_API_KEY=your_staging_key
STRIPE_SECRET_KEY=sk_test_your_key
PAYPAL_CLIENT_ID=sandbox_client_id
PAYPAL_CLIENT_SECRET=sandbox_secret
AMAZON_ACCESS_KEY=staging_access_key
AMAZON_SECRET_KEY=staging_secret_key
DJANGO_SECRET_KEY=staging-secret-bizosaas
DJANGO_CRM_SECRET_KEY=staging-crm-secret
SALEOR_SECRET_KEY=staging-saleor-secret
```

### Deploy
- Click **"Deploy"**
- Wait 20-25 minutes
- Verify 8 containers running

---

## 🎨 **PHASE 3: Frontend Applications Project (6 containers)**

### Create Project
1. **Projects** → **Create Project**
2. **Name**: `bizosaas-frontend-staging`
3. **Description**: `Frontend applications for staging (6 containers)`

### Add Application
1. **Applications** → **Create Application**
2. **Type**: Docker Compose
3. **Name**: `frontend-applications`
4. **Source**: Repository
5. **Repository**: `https://github.com/Bizoholic-Digital/bizosaas-platform.git`
6. **Branch**: `main`
7. **Docker Compose Path**: `dokploy-frontend-staging.yml`

### Environment Variables
Add these:
```
GTM_ID_PRODUCTION=GTM-STAGING123
HOTJAR_ID_PRODUCTION=staging_hotjar
GTM_ID_CORELDOVE_PRODUCTION=GTM-CORELDOVE123
GTM_ID_THRILLRING_PRODUCTION=GTM-THRILLRING123
BASIC_AUTH_USERS=admin:encrypted_password
ADMIN_BASIC_AUTH_USERS=superadmin:encrypted_password
```

### Deploy
- Click **"Deploy"**
- Wait 15-20 minutes
- Verify 6 containers running

---

## 🌐 **DNS UPDATES REQUIRED**

Update these DNS A records:
```
stg.bizoholic.com     A    194.238.16.237
stg.thrillring.com    A    194.238.16.237
```

---

## ✅ **VERIFICATION**

Once all deployed, test:
```bash
# Infrastructure
curl http://194.238.16.237:8200/v1/sys/health
curl http://194.238.16.237:8082

# Backend
curl http://194.238.16.237:8001/health
curl http://194.238.16.237:8005/health

# Frontend (after DNS updates)
curl -I https://stg.bizoholic.com
curl -I https://stg.coreldove.com
curl -I https://stg.thrillring.com
```

---

## 🎯 **SUCCESS CRITERIA**
- ✅ **20 containers total** (6 + 8 + 6)
- ✅ **3 projects created** in Dokploy
- ✅ **All health checks passing**
- ✅ **Staging domains accessible**

---

**Total Time**: 60-75 minutes for complete staging environment