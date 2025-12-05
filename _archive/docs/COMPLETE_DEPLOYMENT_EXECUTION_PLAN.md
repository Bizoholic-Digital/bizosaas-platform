# Complete BizOSaaS Staging Deployment - Execution Plan

**Status**: Ready to Deploy All 21 Services
**Strategy**: Build directly from GitHub - No registry authentication required
**Deployment Method**: Dokploy UI (https://dk.bizoholic.com)

---

## 🎯 Overview

All 21 containers can now be deployed WITHOUT registry authentication:
- **Infrastructure**: 6 services (including Superset)
- **Backend**: 9 services (all backend APIs)
- **Frontend**: 6 services (all client-facing apps)

**Key Advantage**: Every service builds directly from GitHub repository, eliminating registry push bottleneck.

---

## 📋 Phase 1: Infrastructure Deployment (6 Services)

### Step 1.1: Deploy Complete Infrastructure

**File**: `dokploy-infrastructure-staging-with-superset-build.yml`

**Action in Dokploy**:
1. Navigate to: `https://dk.bizoholic.com`
2. Go to: Projects → **Infrastructure** (or backend-services-azbmbl)
3. Settings → Compose File
4. **Replace entire content** with: `dokploy-infrastructure-staging-with-superset-build.yml`
5. Click: **Deploy** button
6. Wait: 8-12 minutes (Superset image is large ~5GB)

**Expected Result**:
```
✅ bizosaas-postgres-staging     (Port 5433) - Healthy
✅ bizosaas-redis-staging        (Port 6380) - Healthy
✅ bizosaas-vault-staging        (Port 8201) - Healthy
⚠️  bizosaas-temporal-server-staging (Port 7234) - Restarting (known issue)
✅ bizosaas-temporal-ui-staging  (Port 8083) - Healthy
✅ bizosaas-superset-staging     (Port 8088) - Healthy (after 2-3 min)
```

**Superset Access**:
- URL: `http://194.238.16.237:8088`
- Username: `admin`
- Password: `Bizoholic2024Admin`

### Step 1.2: Verify Infrastructure Health

```bash
ssh root@194.238.16.237
docker ps --filter 'name=bizosaas.*staging' --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

**Success Criteria**:
- [ ] All 6 containers running
- [ ] 5/6 healthy (Temporal Server known issue acceptable)
- [ ] Superset UI accessible and can login
- [ ] PostgreSQL accepting connections
- [ ] Redis responding to PING

---

## 📋 Phase 2: Backend Deployment (9 Services)

### Step 2.1: Deploy Complete Backend

**File**: `dokploy-backend-staging-complete-build.yml`

**Action in Dokploy**:
1. Go to: Projects → **Backend Services** (or create new project)
2. Settings → Compose File
3. **Replace entire content** with: `dokploy-backend-staging-complete-build.yml`
4. Click: **Deploy** button
5. Wait: 20-30 minutes (builds 9 services from GitHub)

**Build Order** (Dokploy builds in parallel):
1. Saleor API (from image) - 2 minutes
2. Brain API (build) - 5-7 minutes
3. Wagtail CMS (build) - 5-7 minutes
4. Django CRM (build) - 5-7 minutes
5. Business Directory (build) - 5-7 minutes
6. CorelDove Backend (build) - 5-7 minutes
7. Temporal Integration (build) - 5-7 minutes
8. AI Agents (build) - 5-7 minutes
9. Amazon Sourcing (build) - 5-7 minutes

**Expected Result**:
```
✅ bizosaas-saleor-staging              (Port 8000) - Healthy
✅ bizosaas-brain-staging               (Port 8001) - Healthy
✅ bizosaas-wagtail-staging             (Port 8002) - Healthy
✅ bizosaas-django-crm-staging          (Port 8003) - Healthy
✅ bizosaas-business-directory-staging  (Port 8004) - Healthy
✅ bizosaas-coreldove-backend-staging   (Port 8005) - Healthy
✅ bizosaas-temporal-integration-staging (Port 8007) - Healthy
✅ bizosaas-ai-agents-staging           (Port 8008) - Healthy
✅ bizosaas-amazon-sourcing-staging     (Port 8009) - Healthy
```

### Step 2.2: Verify Backend Services

```bash
# Check all backend containers
ssh root@194.238.16.237
docker ps --filter 'name=bizosaas.*staging' --filter 'name=.*800[0-9]' --format 'table {{.Names}}\t{{.Status}}'

# Test API endpoints
curl http://194.238.16.237:8001/health  # Brain API
curl http://194.238.16.237:8000/health/  # Saleor
curl http://194.238.16.237:8002/admin/login/  # Wagtail
curl http://194.238.16.237:8003/admin/login/  # Django CRM
```

**Success Criteria**:
- [ ] All 9 containers running
- [ ] All 9 healthy
- [ ] All API endpoints responding
- [ ] Database connections working
- [ ] No crash loops

---

## 📋 Phase 3: Frontend Deployment (6 Services)

### Step 3.1: Deploy Complete Frontend

**File**: `dokploy-frontend-staging-complete-build.yml`

**Action in Dokploy**:
1. Go to: Projects → **Frontend Applications** (or create new project)
2. Settings → Compose File
3. **Replace entire content** with: `dokploy-frontend-staging-complete-build.yml`
4. Click: **Deploy** button
5. Wait: 30-45 minutes (builds 6 Next.js apps from GitHub)

**Build Order** (Dokploy builds in parallel):
1. Bizoholic Frontend (build) - 8-10 minutes
2. Client Portal (build) - 8-10 minutes
3. CorelDove Frontend (build) - 8-10 minutes
4. Business Directory Frontend (build) - 8-10 minutes
5. ThrillRing Gaming (build) - 8-10 minutes
6. Admin Dashboard (build) - 8-10 minutes

**Expected Result**:
```
✅ bizosaas-bizoholic-frontend-staging       (Port 3000) - Healthy
✅ bizosaas-client-portal-staging            (Port 3001) - Healthy
✅ bizosaas-coreldove-frontend-staging       (Port 3002) - Healthy
✅ bizosaas-business-directory-frontend-staging (Port 3003) - Healthy
✅ bizosaas-thrillring-gaming-staging        (Port 3005) - Healthy
✅ bizosaas-admin-dashboard-staging          (Port 3009) - Healthy
```

### Step 3.2: Verify Frontend Services

```bash
# Check all frontend containers
ssh root@194.238.16.237
docker ps --filter 'name=bizosaas.*frontend' --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

# Test frontend endpoints
curl http://194.238.16.237:3000/  # Bizoholic
curl http://194.238.16.237:3001/  # Client Portal
curl http://194.238.16.237:3002/  # CorelDove
curl http://194.238.16.237:3003/  # Business Directory
curl http://194.238.16.237:3009/  # Admin Dashboard
```

**Success Criteria**:
- [ ] All 6 containers running
- [ ] All 6 healthy
- [ ] All frontends loading in browser
- [ ] API connections working
- [ ] No build errors

---

## 🔍 Monitoring and Verification

### Complete System Health Check

```bash
#!/bin/bash
# Save as: check-complete-staging.sh

VPS_IP="194.238.16.237"
VPS_PASS="&k3civYG5Q6YPb"

echo "================================"
echo "BizOSaaS Staging Health Check"
echo "================================"
echo ""

# Infrastructure (6 services)
echo "📊 INFRASTRUCTURE (6 services):"
sshpass -p "$VPS_PASS" ssh root@$VPS_IP "docker ps --filter 'name=bizosaas-postgres-staging' --filter 'name=bizosaas-redis-staging' --filter 'name=bizosaas-vault-staging' --filter 'name=bizosaas-temporal' --filter 'name=bizosaas-superset-staging' --format 'table {{.Names}}\t{{.Status}}'"
echo ""

# Backend (9 services)
echo "🔧 BACKEND (9 services):"
sshpass -p "$VPS_PASS" ssh root@$VPS_IP "docker ps --filter 'name=bizosaas.*staging' | grep -E '800[0-9]:' | awk '{print \$NF}'"
echo ""

# Frontend (6 services)
echo "🎨 FRONTEND (6 services):"
sshpass -p "$VPS_PASS" ssh root@$VPS_IP "docker ps --filter 'name=bizosaas.*frontend' --filter 'name=bizosaas.*portal' --filter 'name=bizosaas.*admin' --filter 'name=bizosaas.*thrillring' --format 'table {{.Names}}\t{{.Status}}'"
echo ""

# Summary
echo "📈 SUMMARY:"
TOTAL=$(sshpass -p "$VPS_PASS" ssh root@$VPS_IP "docker ps --filter 'name=bizosaas.*staging' | wc -l")
echo "Total Running: $((TOTAL - 1))/21 containers"
echo ""
echo "================================"
```

Make executable and run:
```bash
chmod +x check-complete-staging.sh
./check-complete-staging.sh
```

### Service URL Reference

**Infrastructure:**
- PostgreSQL: `194.238.16.237:5433`
- Redis: `194.238.16.237:6380`
- Vault: `http://194.238.16.237:8201`
- Temporal UI: `http://194.238.16.237:8083`
- Superset: `http://194.238.16.237:8088`

**Backend APIs:**
- Saleor: `http://194.238.16.237:8000`
- Brain API: `http://194.238.16.237:8001`
- Wagtail: `http://194.238.16.237:8002`
- Django CRM: `http://194.238.16.237:8003`
- Business Directory: `http://194.238.16.237:8004`
- CorelDove Backend: `http://194.238.16.237:8005`
- Temporal Integration: `http://194.238.16.237:8007`
- AI Agents: `http://194.238.16.237:8008`
- Amazon Sourcing: `http://194.238.16.237:8009`

**Frontend Apps:**
- Bizoholic: `http://194.238.16.237:3000`
- Client Portal: `http://194.238.16.237:3001`
- CorelDove: `http://194.238.16.237:3002`
- Business Directory: `http://194.238.16.237:3003`
- ThrillRing Gaming: `http://194.238.16.237:3005`
- Admin Dashboard: `http://194.238.16.237:3009`

---

## ⚠️ Common Issues and Solutions

### Issue 1: Build Timeout
**Symptom**: Dokploy build exceeds timeout
**Solution**:
```bash
# Build can take 30+ minutes for large services
# In Dokploy Settings, increase timeout to 3600 seconds (1 hour)
```

### Issue 2: Service Crashing After Build
**Symptom**: Container builds successfully but crashes on start
**Solution**:
```bash
# Check logs for specific error
ssh root@194.238.16.237
docker logs <container-name> --tail 100

# Common fixes:
# - Database not ready: Wait 30 seconds and restart
# - Environment variable missing: Check .env in Dokploy
# - Port conflict: Check no other service using same port
```

### Issue 3: Frontend API Connection Fails
**Symptom**: Frontend loads but can't connect to backend
**Solution**:
```bash
# Verify backend services are healthy first
# Check environment variables in frontend config
# Ensure NEXT_PUBLIC_API_BASE_URL points to correct backend
```

### Issue 4: Superset Taking Too Long
**Symptom**: Superset container starting for 5+ minutes
**Solution**:
```bash
# Normal - Superset is 5GB image with database migrations
# Wait up to 10 minutes on first deployment
# Check logs: docker logs bizosaas-superset-staging -f
```

---

## 📊 Deployment Timeline

### Realistic Time Estimates

**Phase 1: Infrastructure** (8-12 minutes)
- PostgreSQL, Redis, Vault: 2 minutes (images)
- Temporal Server, UI: 3 minutes (images)
- Superset: 5-7 minutes (GitHub build)

**Phase 2: Backend** (20-30 minutes)
- Saleor: 2 minutes (image)
- 8 services building in parallel: 18-28 minutes

**Phase 3: Frontend** (30-45 minutes)
- 6 Next.js apps building in parallel: 30-45 minutes

**Total Deployment Time**: 58-87 minutes (~1-1.5 hours)

---

## ✅ Final Verification Checklist

### Infrastructure Complete
- [ ] 6/6 containers running
- [ ] PostgreSQL healthy (port 5433)
- [ ] Redis healthy (port 6380)
- [ ] Vault healthy (port 8201)
- [ ] Temporal UI accessible (port 8083)
- [ ] Superset accessible (port 8088)
- [ ] Can login to Superset with admin credentials

### Backend Complete
- [ ] 9/9 containers running
- [ ] All containers healthy (no restarts)
- [ ] Brain API responding (8001)
- [ ] Saleor API responding (8000)
- [ ] Wagtail CMS accessible (8002)
- [ ] Django CRM accessible (8003)
- [ ] All other backend APIs responding

### Frontend Complete
- [ ] 6/6 containers running
- [ ] All containers healthy
- [ ] Bizoholic loads in browser (3000)
- [ ] Client Portal loads (3001)
- [ ] CorelDove loads (3002)
- [ ] Business Directory loads (3003)
- [ ] Admin Dashboard loads (3009)
- [ ] All frontends can connect to backends

### Platform Integration
- [ ] Frontend → Backend API calls working
- [ ] Backend → PostgreSQL connections working
- [ ] Backend → Redis connections working
- [ ] Superset can query PostgreSQL
- [ ] No service crash loops
- [ ] All health checks passing

---

## 🎯 Next Steps After Deployment

### Immediate (Day 1)
1. Configure Superset dashboards with data sources
2. Test critical user flows (registration, checkout, form submission)
3. Verify multi-tenant data isolation
4. Check error rates in service logs

### Short-term (Week 1)
1. Set up domain DNS for staging subdomains
2. Configure Traefik SSL certificates
3. Enable monitoring and alerting
4. Run load testing on critical endpoints
5. Document any deployment-specific issues

### Medium-term (Month 1)
1. Configure automated backups
2. Set up log aggregation (ELK/Loki)
3. Implement CI/CD pipeline for auto-deployments
4. Create runbooks for common issues
5. Plan production migration strategy

---

## 📞 Success Metrics

**Deployment is complete when:**
- ✅ All 21 containers running and healthy
- ✅ All service URLs accessible from browser
- ✅ Critical user flows working end-to-end
- ✅ No service crash loops for 1 hour
- ✅ Database queries completing successfully
- ✅ Frontend-backend integration working

**Platform is production-ready when:**
- ✅ Domain DNS configured and SSL active
- ✅ Monitoring and alerting configured
- ✅ Automated backups running
- ✅ Load testing passed
- ✅ Documentation complete
- ✅ Team trained on staging environment

---

## 🚀 Ready to Deploy!

All configuration files are prepared and committed to repository:
1. `dokploy-infrastructure-staging-with-superset-build.yml` ✅
2. `dokploy-backend-staging-complete-build.yml` ✅
3. `dokploy-frontend-staging-complete-build.yml` ✅

**Start with Phase 1 (Infrastructure) and proceed sequentially through Phase 2 (Backend) and Phase 3 (Frontend).**

**Total estimated time: 1-1.5 hours for complete 21-service deployment.**

---

*Last Updated: 2025-10-12 13:15 UTC*
*Strategy: Build from GitHub (No Registry Required)*
*Deployment Platform: Dokploy at dk.bizoholic.com*
