# CI/CD Deployment Guide - BizOSaaS Platform

**Pipeline**: Local WSL2 → GitHub + GHCR → Dokploy Staging → Dokploy Production

---

## 🎯 Complete Workflow

### 1. **Local Development (WSL2)**

```bash
# Work on your feature/fix
cd ~/projects/bizoholic/bizosaas-platform

# Example: Fix frontend issue
cd frontend/apps/bizoholic-frontend
npm run build  # Test locally
```

### 2. **Commit and Push to GitHub**

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "fix: resolve Bizoholic Frontend HTTP 500 error

- Complete Next.js standalone build
- Fixed missing server.js
- Routes through Brain Gateway (Port 8001)

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to trigger CI/CD
git push origin main  # or staging
```

### 3. **GitHub Actions Builds and Pushes to GHCR**

**Automatic Process** (no manual intervention):
- GitHub Actions detects push
- Identifies changed services (frontend/backend/infrastructure)
- Builds Docker images
- Pushes to `ghcr.io/bizoholic-digital/bizosaas-{service}:staging`
- Caches layers for faster subsequent builds

**Monitor Build Progress**:
```
https://github.com/Bizoholic-Digital/bizosaas-platform/actions
```

### 4. **Deploy to Dokploy Staging (VPS)**

```bash
# SSH to VPS
ssh root@194.238.16.237

# Navigate to project
cd /root/bizosaas-platform

# Pull latest code (includes updated compose files)
git pull origin main

# Pull latest images from GHCR
docker-compose -f dokploy-staging-complete.yml pull

# Deploy updated services
docker-compose -f dokploy-staging-complete.yml up -d

# Check status
docker-compose -f dokploy-staging-complete.yml ps
```

### 5. **Test on Staging**

```bash
# Test Brain Gateway (central hub)
curl http://194.238.16.237:8001/health

# Test frontend services
curl http://194.238.16.237:3000  # Bizoholic
curl http://194.238.16.237:3005  # ThrillRing
curl http://194.238.16.237:3002  # CorelDove

# Test backend services through Brain Gateway
curl http://194.238.16.237:8001/api/brain/wagtail/health
curl http://194.238.16.237:8001/api/brain/django-crm/health

# Check all 23 services
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### 6. **If Issues Found**

```bash
# Fix locally (on WSL2)
cd ~/projects/bizoholic/bizosaas-platform
# Make your fixes
git add .
git commit -m "fix: address staging issue XYZ"
git push origin main

# GitHub Actions rebuilds automatically
# Wait for build completion
# Pull and redeploy on staging (repeat step 4)
```

### 7. **Promote to Production**

```bash
# On VPS, tag staging images as production
docker tag ghcr.io/bizoholic-digital/bizosaas-brain-gateway:staging \
           ghcr.io/bizoholic-digital/bizosaas-brain-gateway:production

# Or trigger production deployment from main branch
git checkout main
git tag v1.0.0
git push origin v1.0.0

# Deploy production environment
docker-compose -f dokploy-production-complete.yml up -d
```

---

## 📋 Service Inventory (23 Total)

### Infrastructure (6)
- ✅ PostgreSQL (pgvector) - Port 5433
- ✅ Redis - Port 6380
- ✅ Vault - Port 8201
- ✅ Temporal Server - Port 7234
- ✅ Temporal UI - Port 8083
- ✅ Superset - Port 8088

### Backend (10)
- ✅ Brain Gateway (CRITICAL) - Port 8001 - **ALL REQUESTS ROUTE HERE**
- ✅ AI Agents (93 agents) - Port 8008
- ✅ Auth Service - Port 8007
- ✅ Wagtail CMS - Port 8002
- ✅ Saleor E-commerce - Port 8000
- ✅ Django CRM - Port 8003
- ✅ CorelDove Backend - Port 8005
- ✅ Amazon Sourcing - Port 8009
- ✅ Business Directory Backend - Port 8004
- ✅ QuantTrade Backend - Port 8012

### Frontend (7)
- ✅ Bizoholic Frontend - Port 3000
- ✅ ThrillRing Gaming - Port 3005
- ✅ CorelDove Frontend - Port 3002
- ✅ Client Portal - Port 3001
- ✅ Admin Dashboard - Port 3009
- ✅ Business Directory Frontend - Port 3003
- ✅ QuantTrade Frontend - Port 3012

---

## 🔧 Troubleshooting

### Build Fails on GitHub Actions

```bash
# Check workflow logs
# https://github.com/Bizoholic-Digital/bizosaas-platform/actions

# Common fixes:
# 1. Ensure Dockerfile exists in service path
# 2. Check dependencies in package.json or requirements.txt
# 3. Verify build context in workflow file
```

### Image Pull Fails on VPS

```bash
# Login to GHCR on VPS
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Or use GitHub PAT
echo $GITHUB_PAT | docker login ghcr.io -u USERNAME --password-stdin

# Pull specific image manually
docker pull ghcr.io/bizoholic-digital/bizosaas-brain-gateway:staging
```

### Service Not Starting

```bash
# Check logs
docker logs bizosaas-brain-staging --tail 100

# Check dependencies (must start infrastructure first)
docker-compose -f dokploy-staging-complete.yml ps

# Restart specific service
docker-compose -f dokploy-staging-complete.yml restart brain-gateway
```

---

## 🎯 Key Principles

1. **Brain Gateway First**: All services route through Port 8001
2. **Infrastructure → Backend → Frontend**: Deploy in this order
3. **Test Staging First**: Never deploy untested code to production
4. **GitHub as Source of Truth**: All deployments pull from GHCR
5. **Automated Builds**: GitHub Actions handles all image building

---

## 📊 Deployment Checklist

### Before Each Deployment
- [ ] All tests pass locally
- [ ] Code committed and pushed to GitHub
- [ ] GitHub Actions build completed successfully
- [ ] GHCR images updated with staging tag

### Staging Deployment
- [ ] Pull latest images from GHCR
- [ ] Deploy services in order (infra → backend → frontend)
- [ ] Verify all 23 services running
- [ ] Test Brain Gateway routing
- [ ] Test critical user flows
- [ ] Check logs for errors

### Production Promotion
- [ ] Staging fully validated
- [ ] Tag images as production
- [ ] Create GitHub release
- [ ] Deploy to production environment
- [ ] Monitor metrics and logs
- [ ] Rollback plan ready

---

**Status**: ✅ CI/CD Pipeline Configured
**Last Updated**: October 15, 2025
**Architecture**: Containerized Microservices + DDD + Brain Gateway
