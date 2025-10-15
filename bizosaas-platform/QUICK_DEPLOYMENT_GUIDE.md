# Quick Deployment Guide - BizOSaaS Platform

**Status**: 9/22 containers running, 13 need deployment
**Time Required**: 60-90 minutes
**Access**: https://dk.bizoholic.com

---

## Current Situation

✅ **Infrastructure**: 5/6 running (PostgreSQL, Redis, Vault, Temporal UI, Superset)
⚠️ **Backend**: 3/10 running (Brain API, Wagtail, Django CRM) - **7 need deployment**
⚠️ **Frontend**: 1/6 running (Bizoholic) - **5 need deployment**

---

## Deploy Now (2 Simple Steps)

### Step 1: Deploy Backend Services (40 minutes)

1. Go to: https://dk.bizoholic.com
2. Click: **Projects** → **Create New Project**
3. Name: `backend-services`
4. Description: `BizOSaaS Backend Services`
5. Click: **Create**

6. Inside project, click: **Create Application**
7. Select: **Docker Compose**
8. Name: `backend-staging`
9. Source Type: **Git Repository**
10. Repository: `https://github.com/Bizoholic-Digital/bizosaas-platform.git`
11. Branch: `main`
12. Compose File Path: `bizosaas-platform/dokploy-backend-staging.yml`

13. Click: **Environment Variables** tab
14. Add variables:
```bash
OPENAI_API_KEY=<your-openai-key>
ANTHROPIC_API_KEY=<your-anthropic-key>
AMAZON_ACCESS_KEY=<your-amazon-key>
AMAZON_SECRET_KEY=<your-amazon-secret>
```

15. Click: **Deploy** button
16. Monitor logs (builds 7 containers: Saleor, CorelDove Backend, Business Directory, Auth, Temporal Integration, AI Agents, Amazon Sourcing)

### Step 2: Deploy Frontend Services (30 minutes)

1. In Dokploy, click: **Projects** → **Create New Project**
2. Name: `frontend-services`
3. Description: `BizOSaaS Frontend Applications`
4. Click: **Create**

5. Inside project, click: **Create Application**
6. Select: **Docker Compose**
7. Name: `frontend-staging`
8. Source Type: **Git Repository**
9. Repository: `https://github.com/Bizoholic-Digital/bizosaas-platform.git`
10. Branch: `main`
11. Compose File Path: `bizosaas-platform/dokploy-frontend-staging.yml`

12. Click: **Deploy** button
13. Monitor logs (builds 5 containers: Client Portal, CorelDove Frontend, Business Directory Frontend, ThrillRing, Admin Dashboard)

---

## After Deployment: Configure Domains (15 minutes)

### Domain 1: Bizoholic Staging
- Container: `bizosaas-bizoholic-frontend-staging`
- Domain: `stg.bizoholic.com`
- Port: `3000`
- SSL: ✅ Enable (Let's Encrypt)

### Domain 2: CorelDove Staging
- Container: `bizosaas-coreldove-frontend-staging`
- Domain: `stg.coreldove.com`
- Port: `3002`
- SSL: ✅ Enable (Let's Encrypt)

### Domain 3: ThrillRing Staging
- Container: `bizosaas-thrillring-gaming-staging`
- Domain: `stg.thrillring.com`
- Port: `3005`
- SSL: ✅ Enable (Let's Encrypt)

### Path 1: Client Portal
- Container: `bizosaas-client-portal-staging`
- Host: `stg.bizoholic.com`
- Path: `/login`
- Port: `3001`
- Strip Path: ✅ Yes

### Path 2: Admin Dashboard
- Container: `bizosaas-admin-dashboard-staging`
- Host: `stg.bizoholic.com`
- Path: `/admin`
- Port: `3009`
- Strip Path: ✅ Yes

---

## Verify Deployment

Run from terminal:
```bash
cd /home/alagiri/projects/bizoholic/bizosaas-platform
./verify-staging-deployment.sh
```

Or check manually:
```bash
# Check backend services
curl http://194.238.16.237:8000/health/    # Saleor
curl http://194.238.16.237:8005/health     # CorelDove Backend
curl http://194.238.16.237:8006/health     # Auth Service

# Check frontend services
curl http://194.238.16.237:3001/api/health # Client Portal
curl http://194.238.16.237:3002/api/health # CorelDove Frontend
curl http://194.238.16.237:3009/api/health # Admin Dashboard

# Check staging domains
curl -I https://stg.bizoholic.com
curl -I https://stg.coreldove.com
curl -I https://stg.thrillring.com
```

---

## Expected Results

**After Backend Deployment**:
- ✅ 10/10 backend services running
- ✅ Saleor, Auth, CorelDove Backend, AI Agents operational

**After Frontend Deployment**:
- ✅ 6/6 frontend applications running
- ✅ All staging domains accessible

**Total Platform**:
- ✅ 22/22 containers running (100%)
- ✅ Complete BizOSaaS platform operational

---

## Deployment Timeline

| Step | Duration | Cumulative |
|------|----------|------------|
| Backend Deployment | 40 min | 40 min |
| Frontend Deployment | 30 min | 70 min |
| Domain Configuration | 15 min | 85 min |
| SSL Certificate Generation | 5 min | 90 min |
| **Total** | **90 min** | |

---

## Troubleshooting

### Build Fails
- Check logs in Dokploy UI
- Verify GitHub repository is accessible
- Ensure environment variables are set

### Container Won't Start
- Check container logs: `docker logs <container-name>`
- Verify dependencies (PostgreSQL, Redis) are running
- Check resource limits (RAM, CPU)

### Domain Not Working
- Verify DNS points to 194.238.16.237
- Wait 5-10 minutes for SSL generation
- Check Traefik routing in Dokploy

---

## Files Reference

All deployment files location:
```
/home/alagiri/projects/bizoholic/bizosaas-platform/
```

- `dokploy-backend-staging.yml` - Backend configuration
- `dokploy-frontend-staging.yml` - Frontend configuration
- `verify-staging-deployment.sh` - Verification script
- `DEPLOYMENT_EXECUTION_REPORT.md` - Detailed guide
- `CURRENT_DEPLOYMENT_STATUS.md` - Current status

---

## Support

**Dokploy**: https://dk.bizoholic.com
**VPS IP**: 194.238.16.237
**GitHub**: https://github.com/Bizoholic-Digital/bizosaas-platform.git

---

*Quick Guide - October 13, 2025*
*Deploy 13 remaining containers in ~90 minutes*
*🚀 Ready to deploy via Dokploy UI*
