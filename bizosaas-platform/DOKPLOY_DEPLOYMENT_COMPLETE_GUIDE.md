# BizOSaaS Platform - Complete Dokploy Deployment Guide

**Date**: October 15, 2025
**Dokploy Dashboard**: https://dk.bizoholic.com
**Admin**: bizoholic.digital@gmail.com / 25IKC#1XiKABRo
**API Key**: bizoholicKRGZxqgQXBDBzumvvnMhiEZLmnetMTAWwTnFztwuGofadbHagGbJiiMZTqczBDKY

---

## 🎯 Deployment Strategy

### Why Use Dokploy Dashboard Instead of CLI?

1. **Visual Management**: See all 23 services in one place
2. **Easy Monitoring**: Real-time logs, health checks, resource usage
3. **Deployment History**: Track all deployments and rollbacks
4. **Domain Management**: Configure SSL and domains through UI
5. **Project Organization**: Separate environments (staging/production)

### Architecture Overview

```
Dokploy Dashboard (dk.bizoholic.com)
├── Project: BizOSaaS Platform - Staging
│   ├── Infrastructure Compose (6 services)
│   ├── Backend Compose (10 services)
│   └── Frontend Compose (7 services)
└── Existing Projects (Preserved)
    ├── bizoholic-website (WordPress)
    ├── shared_infrastructure
    └── automation-hub (n8n)
```

---

## 📋 Step-by-Step Deployment

### Phase 1: Access Dokploy Dashboard

1. **Open Dashboard**: https://dk.bizoholic.com
2. **Login**:
   - Email: bizoholic.digital@gmail.com
   - Password: 25IKC#1XiKABRo

### Phase 2: Create BizOSaaS Platform Project

1. Click **"Create Project"**
2. Enter details:
   - **Name**: `bizosaas-platform-staging`
   - **Description**: `BizOSaaS multi-tenant SaaS platform - staging environment (23 services: Infrastructure + Backend + Frontend)`
3. Click **"Create"**

### Phase 3: Deploy Infrastructure Layer (6 Services)

#### Create Docker Compose Service

1. Inside `bizosaas-platform-staging` project
2. Click **"Add Service"** → **"Docker Compose"**
3. Configuration:
   - **Name**: `infrastructure`
   - **Description**: `Core infrastructure: PostgreSQL, Redis, Vault, Temporal, Superset`

#### Configure Source

1. **Source Type**: GitHub
2. **Repository**: `https://github.com/Bizoholic-Digital/bizosaas-platform.git`
3. **Branch**: `main`
4. **Compose File Path**: `dokploy-infrastructure-staging-with-superset-build.yml`

#### Deploy

1. Click **"Deploy"**
2. Monitor deployment logs in real-time
3. Wait for all 6 services to show **"Running"**

**Services Deployed**:
- bizosaas-postgres-staging (Port 5433)
- bizosaas-redis-staging (Port 6380)
- bizosaas-vault-staging (Port 8201)
- bizosaas-temporal-server-staging (Port 7234)
- bizosaas-temporal-ui-staging (Port 8083)
- bizosaas-superset-staging (Port 8088)

### Phase 4: Deploy Backend Layer (10 Services)

#### Create Backend Compose Service

1. Click **"Add Service"** → **"Docker Compose"**
2. Configuration:
   - **Name**: `backend`
   - **Description**: `Backend services: Brain Gateway, AI Agents, Auth, CMS, E-commerce, etc.`

#### Configure Source

1. **Source Type**: GitHub
2. **Repository**: `https://github.com/Bizoholic-Digital/bizosaas-platform.git`
3. **Branch**: `main`
4. **Compose File Path**: `dokploy-backend-staging-local.yml`

#### Deploy

1. Click **"Deploy"**
2. Monitor deployment logs
3. Verify all 10 services running

**Services Deployed**:
- bizosaas-brain-staging (Port 8001) - **CRITICAL**
- bizosaas-ai-agents-staging (Port 8008)
- bizosaas-auth-staging (Port 8007)
- bizosaas-wagtail-staging (Port 8002)
- bizosaas-saleor-staging (Port 8000)
- bizosaas-django-crm-staging (Port 8003)
- bizosaas-coreldove-backend-staging (Port 8005)
- bizosaas-amazon-sourcing-staging (Port 8009)
- bizosaas-business-directory-staging (Port 8004)
- bizosaas-quanttrade-backend-staging (Port 8012)

### Phase 5: Deploy Frontend Layer (7 Services)

#### Create Frontend Compose Service

1. Click **"Add Service"** → **"Docker Compose"**
2. Configuration:
   - **Name**: `frontend`
   - **Description**: `Frontend applications: Bizoholic, ThrillRing, CorelDove, Portals, Admin`

#### Configure Source

1. **Source Type**: GitHub
2. **Repository**: `https://github.com/Bizoholic-Digital/bizosaas-platform.git`
3. **Branch**: `main`
4. **Compose File Path**: `dokploy-frontend-staging-local.yml`

#### Deploy

1. Click **"Deploy"**
2. Monitor deployment logs
3. Verify all 7 services running

**Services Deployed**:
- bizosaas-bizoholic-frontend-staging (Port 3001)
- bizosaas-thrillring-gaming-staging (Port 3005)
- bizosaas-coreldove-frontend-staging (Port 3002)
- bizosaas-client-portal-staging (Port 3000)
- bizosaas-admin-dashboard-staging (Port 3009)
- bizosaas-business-directory-frontend-staging (Port 3003)
- bizosaas-quanttrade-frontend-staging (Port 3012)

---

## ✅ Verification Checklist

### Through Dokploy Dashboard

1. **Project View**:
   - [ ] See `bizosaas-platform-staging` project
   - [ ] 3 compose services listed (infrastructure, backend, frontend)
   - [ ] All services showing "Running" status

2. **Infrastructure Services**:
   - [ ] PostgreSQL: Healthy
   - [ ] Redis: Healthy
   - [ ] Vault: Healthy
   - [ ] Temporal Server: Running
   - [ ] Temporal UI: Accessible at Port 8083
   - [ ] Superset: Accessible at Port 8088

3. **Backend Services**:
   - [ ] Brain Gateway: Healthy (Port 8001)
   - [ ] All 10 backend services: Running

4. **Frontend Services**:
   - [ ] All 7 frontend services: Running
   - [ ] No HTTP 500 errors

### Manual Testing

```bash
# Test Brain Gateway (CRITICAL)
curl http://194.238.16.237:8001/health

# Test Bizoholic Frontend
curl -I http://194.238.16.237:3001

# Test ThrillRing Gaming
curl -I http://194.238.16.237:3005

# Test Temporal UI
curl -I http://194.238.16.237:8083

# Test Superset
curl -I http://194.238.16.237:8088
```

---

## 🎛️ Dashboard Management

### Monitoring Services

1. Click on any service to view:
   - **Logs**: Real-time container logs
   - **Metrics**: CPU, Memory, Network usage
   - **Environment**: View/edit environment variables
   - **Deployments**: Deployment history

### Managing Deployments

**Redeploy Service**:
1. Select service
2. Click **"Redeploy"**
3. Optionally pull latest code from GitHub

**View Logs**:
1. Select service
2. Click **"Logs"** tab
3. Filter by service name
4. Search for errors

**Stop/Start Services**:
1. Select service
2. Click **"Stop"** or **"Start"**
3. Confirm action

### Environment Variables

1. Select service
2. Click **"Environment"** tab
3. Add/edit variables
4. Click **"Save"**
5. Redeploy to apply changes

---

## 🔄 CI/CD Integration

### GitHub Integration (Recommended)

1. **In Dokploy Dashboard**:
   - Navigate to service settings
   - Enable **"Auto Deploy on Push"**
   - Copy webhook URL

2. **In GitHub Repository**:
   - Go to Settings → Webhooks
   - Add webhook URL from Dokploy
   - Select events: Push to main/staging branch

3. **Workflow**:
   ```
   Local Changes → Git Push → GitHub → Dokploy Webhook → Auto Deploy
   ```

---

## 🌐 Domain Configuration (Future)

### Setting Up Domains

1. **In Dokploy Dashboard**:
   - Select service
   - Click **"Domains"** tab
   - Add domain (e.g., `api.bizosaas.com`)
   - Enable SSL (Let's Encrypt automatic)

2. **Traefik Auto-Configuration**:
   - Dokploy automatically configures Traefik
   - SSL certificates auto-generated
   - HTTP → HTTPS redirect enabled

### Recommended Domain Structure

**Staging Environment**:
- `staging.bizosaas.com` → Brain Gateway
- `staging-bizoholic.bizosaas.com` → Bizoholic Frontend
- `staging-thrillring.bizosaas.com` → ThrillRing Gaming
- `staging-admin.bizosaas.com` → Admin Dashboard
- `staging-temporal.bizosaas.com` → Temporal UI
- `staging-superset.bizosaas.com` → Superset

**Production Environment** (after testing):
- `api.bizosaas.com` → Brain Gateway
- `bizoholic.com` → Bizoholic Frontend
- `thrillring.com` → ThrillRing Gaming
- `admin.bizosaas.com` → Admin Dashboard
- `temporal.bizosaas.com` → Temporal UI
- `analytics.bizosaas.com` → Superset

---

## 🚨 Troubleshooting

### Service Not Starting

1. **Check Logs in Dashboard**:
   - Click service → Logs tab
   - Look for error messages
   - Common issues:
     - Database not ready (wait 30s)
     - Environment variable missing
     - Port conflict

2. **Fix and Redeploy**:
   - Update compose file in GitHub
   - Click **"Redeploy"** in Dokploy
   - Monitor logs for success

### Port Conflicts

If ports are already in use:
1. Check existing services in dashboard
2. Either:
   - Stop conflicting service
   - Change port in compose file
3. Redeploy

### Database Connection Issues

1. **Verify PostgreSQL Running**:
   - Check infrastructure compose logs
   - Verify health check passing

2. **Check Connection String**:
   - Brain Gateway should use: `postgresql://admin:BizOSaaS2025!StagingDB@bizosaas-postgres-staging:5432/bizosaas_staging`
   - Backend services connect through Brain Gateway

---

## 🧹 Cleanup Old Services

### After Successful Deployment

1. **In Dokploy Dashboard**:
   - View old BizOSaaS containers
   - Select containers NOT part of new deployment
   - Click **"Delete"**

2. **Preserve These Projects**:
   - bizoholic-website (WordPress)
   - shared_infrastructure
   - automation-hub (n8n)

---

## 📊 Success Metrics

### Deployment Complete When:

1. ✅ All 23 services visible in Dokploy dashboard
2. ✅ All services showing "Running" status
3. ✅ Brain Gateway responding to health checks
4. ✅ Frontend services accessible (no HTTP 500)
5. ✅ No service restart loops
6. ✅ WordPress and n8n services still running

### Performance Indicators:

- Brain Gateway response time < 200ms
- Frontend load time < 2s
- All health checks passing
- No error logs

---

## 🎯 Next Steps After Deployment

### Immediate (Today)

1. **Test All Endpoints**: Verify each service responds
2. **Check Logs**: Review for any errors or warnings
3. **Monitor Performance**: Use dashboard metrics
4. **Document Issues**: Note any failing services

### Short-term (This Week)

1. **Configure Domains**: Set up staging subdomains
2. **Enable SSL**: Let's Encrypt certificates
3. **Fix Unhealthy Services**: Address any failures
4. **Performance Testing**: Load test Brain Gateway

### Medium-term (Next 2 Weeks)

1. **Production Environment**: Create production project
2. **CI/CD Automation**: Enable GitHub webhooks
3. **Monitoring Setup**: Configure alerts
4. **Backup Strategy**: Implement database backups

---

## 📞 Quick Reference

### Dokploy Dashboard
- **URL**: https://dk.bizoholic.com
- **Admin**: bizoholic.digital@gmail.com
- **Password**: 25IKC#1XiKABRo

### VPS Access
- **SSH**: `ssh root@194.238.16.237`
- **Password**: `&k3civYG5Q6YPb`

### GitHub Repository
- **URL**: https://github.com/Bizoholic-Digital/bizosaas-platform
- **Branch**: main
- **Compose Files**:
  - Infrastructure: `dokploy-infrastructure-staging-with-superset-build.yml`
  - Backend: `dokploy-backend-staging-local.yml`
  - Frontend: `dokploy-frontend-staging-local.yml`

### Key Ports
- Brain Gateway: 8001 (CRITICAL)
- Bizoholic: 3001
- ThrillRing: 3005
- PostgreSQL: 5433
- Redis: 6380
- Superset: 8088
- Temporal UI: 8083

---

**Status**: ✅ Ready for Dokploy Dashboard Deployment
**Total Services**: 23 (Infrastructure: 6, Backend: 10, Frontend: 7)
**Deployment Method**: Dokploy Dashboard (UI-based)
**Management**: All services managed through dk.bizoholic.com
