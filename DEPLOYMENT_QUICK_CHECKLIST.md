# ✅ Quick Deployment Checklist

## 📋 PRE-DEPLOYMENT
- [ ] Access Dokploy: http://194.238.16.237:3000
- [ ] DNS configured: stg.bizoholic.com, stg.coreldove.com, stg.thrillring.com → 194.238.16.237
- [ ] API keys ready (8 keys)
- [ ] Files ready: dokploy-infrastructure-staging.yml, dokploy-backend-staging.yml, dokploy-frontend-staging.yml

---

## 🏗️ PHASE 1: INFRASTRUCTURE (15-20 min)
- [ ] Create project: `bizosaas-infrastructure-staging`
- [ ] Add application: `infrastructure-services` (Docker Compose)
- [ ] Upload/link: `dokploy-infrastructure-staging.yml`
- [ ] Deploy
- [ ] Wait 5-10 minutes
- [ ] Verify 6 containers running:
  - [ ] bizosaas-postgres-staging
  - [ ] bizosaas-redis-staging
  - [ ] bizosaas-vault-staging
  - [ ] bizosaas-temporal-server-staging
  - [ ] bizosaas-temporal-ui-staging
  - [ ] bizosaas-temporal-integration-staging
- [ ] Test: `curl http://194.238.16.237:8200/v1/sys/health`
- [ ] Test: `curl http://194.238.16.237:8082`

---

## 🔧 PHASE 2: BACKEND (20-30 min)
- [ ] Create project: `bizosaas-backend-staging`
- [ ] Add application: `backend-services` (Docker Compose)
- [ ] Upload/link: `dokploy-backend-staging.yml`
- [ ] Add 8 environment variables:
  - [ ] OPENROUTER_API_KEY
  - [ ] OPENAI_API_KEY
  - [ ] ANTHROPIC_API_KEY
  - [ ] STRIPE_SECRET_KEY
  - [ ] PAYPAL_CLIENT_ID
  - [ ] PAYPAL_CLIENT_SECRET
  - [ ] AMAZON_ACCESS_KEY
  - [ ] AMAZON_SECRET_KEY
- [ ] Deploy
- [ ] Wait 10-15 minutes
- [ ] Verify 8 containers running:
  - [ ] bizosaas-brain-staging (8001)
  - [ ] bizosaas-wagtail-staging (8002)
  - [ ] bizosaas-django-crm-staging (8003)
  - [ ] bizosaas-directory-api-staging (8004)
  - [ ] coreldove-backend-staging (8005)
  - [ ] bizosaas-ai-agents-staging (8010)
  - [ ] amazon-sourcing-staging (8085)
  - [ ] bizosaas-saleor-staging (8000)
- [ ] Test Brain API: `curl http://194.238.16.237:8001/health`
- [ ] Run: `./verify-backend-deployment.sh`

---

## 📱 PHASE 3: FRONTEND (30-40 min)
- [ ] Verify DNS propagated: `dig stg.bizoholic.com`
- [ ] Create project: `bizosaas-frontend-staging`
- [ ] Add application: `frontend-applications` (Docker Compose)
- [ ] Upload/link: `dokploy-frontend-staging.yml`
- [ ] Deploy
- [ ] Wait 10-15 minutes
- [ ] Verify 6 containers running:
  - [ ] bizoholic-frontend-staging (3000)
  - [ ] client-portal-staging (3001)
  - [ ] coreldove-frontend-staging (3002)
  - [ ] business-directory-staging (3004)
  - [ ] thrillring-gaming-staging (3005)
  - [ ] admin-dashboard-staging (3009)

### Configure Domains:
- [ ] bizoholic-frontend → stg.bizoholic.com:3000 (SSL: Yes)
- [ ] coreldove-frontend → stg.coreldove.com:3002 (SSL: Yes)
- [ ] thrillring-gaming → stg.thrillring.com:3005 (SSL: Yes)
- [ ] client-portal → stg.bizoholic.com/login:3001 (SSL: Yes, Strip Path: Yes)
- [ ] admin-dashboard → stg.bizoholic.com/admin:3009 (SSL: Yes, Strip Path: Yes)

### Test Domains:
- [ ] https://stg.bizoholic.com (loads, SSL valid)
- [ ] https://stg.coreldove.com (loads, SSL valid)
- [ ] https://stg.thrillring.com (loads, SSL valid)
- [ ] https://stg.bizoholic.com/login/ (loads)
- [ ] https://stg.bizoholic.com/admin/ (loads)

---

## ✅ FINAL VERIFICATION
- [ ] Run: `./verify-all-20-containers.sh`
- [ ] Expected: 20/20 containers running
- [ ] Success rate: 100%

### WordPress Safety Check:
- [ ] https://bizoholic.com (still works)
- [ ] https://coreldove.com (still works)
- [ ] https://thrillring.com (still works)

---

## 🎉 DEPLOYMENT COMPLETE
**Total Time**: _____ minutes
**Containers Running**: _____ / 20
**Issues Encountered**: _____________
**Status**: [ ] Success  [ ] Partial  [ ] Failed

---

**Notes**:
_____________________________________________
_____________________________________________
_____________________________________________
