# BizOSaaS Platform - Dokploy UI Deployment Guide

## Overview
This guide walks you through deploying all 23 services to KVM4 (72.60.219.244) using the Dokploy web interface at https://dk4.bizoholic.com.

## Service Distribution

### KVM4 (72.60.219.244) - 23 Services:
- **Infrastructure**: 6 services
- **Backend APIs**: 10 services
- **Frontend Apps**: 7 services

### KVM2 (194.238.16.237) - 1 Service:
- **CorelDove WordPress** (staying on KVM2)

## Routing Configuration

**Unified Domain Strategy:**
- `stg.bizoholic.com` → Bizoholic Frontend (main landing page)
- `stg.bizoholic.com/login/` → Client Portal (tenant login)
- `stg.bizoholic.com/admin/` → Admin Dashboard (platform admin)
- `stg.bizoholic.com/directory/` → Business Directory
- `stg.coreldove.com` → CorelDove Storefront (e-commerce)
- `stg.thrillring.com` → ThrillRing Gaming (games)

All backend requests route through **Brain Gateway (Port 8001)**.

## Step-by-Step Deployment via Dokploy UI

### Step 1: Access Dokploy
1. Open browser: https://dk4.bizoholic.com
2. Login with your credentials
3. Navigate to **Projects** section

### Step 2: Create Project
1. Click **"Create New Project"** button
2. Fill in project details:
   - **Name**: `bizosaas-platform-staging`
   - **Description**: `BizOSaaS Complete Platform - 23 Services`
3. Click **"Create"**

### Step 3: Add Docker Compose Application
1. Inside the `bizosaas-platform-staging` project, click **"Create Application"**
2. Select **"Docker Compose"** as application type
3. Configure deployment:
   - **Name**: `staging-complete`
   - **Source Type**: `Git Repository`
   - **Repository URL**: `https://github.com/Bizoholic-Digital/bizosaas-platform.git`
   - **Branch**: `main`
   - **Compose File Path**: `bizosaas-platform/dokploy-staging-complete.yml`

### Step 4: Configure Environment Variables
Click **"Environment Variables"** tab and add:

```bash
# Required API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Amazon Integration
AMAZON_ACCESS_KEY=...
AMAZON_SECRET_KEY=...

# Payment Gateways (optional)
STRIPE_SECRET_KEY=sk_...
PAYPAL_CLIENT_ID=...

# Email Services (optional)
SMTP_HOST=smtp.resend.com
SMTP_USER=...
SMTP_PASSWORD=...

# External APIs (optional)
GOOGLE_ADS_API_KEY=...
META_ADS_API_KEY=...
```

**Note**: Only `OPENAI_API_KEY` is strictly required for initial deployment.

### Step 5: Configure Domains
After deployment completes, configure domains for each frontend:

1. Navigate to **"Domains"** tab in Dokploy
2. Add domains for each service:

#### Bizoholic Frontend:
- **Domain**: `stg.bizoholic.com`
- **Port**: `3000`
- **Enable SSL**: ✓ (Let's Encrypt)

#### ThrillRing Gaming:
- **Domain**: `stg.thrillring.com`
- **Port**: `3005`
- **Enable SSL**: ✓ (Let's Encrypt)

#### CorelDove Frontend:
- **Domain**: `stg.coreldove.com`
- **Port**: `3002`
- **Enable SSL**: ✓ (Let's Encrypt)

#### Subdirectory Routes (handled by Traefik labels):
- `stg.bizoholic.com/login/` → Port 3001
- `stg.bizoholic.com/admin/` → Port 3009
- `stg.bizoholic.com/directory/` → Port 3003

### Step 6: Deploy
1. Click the **"Deploy"** button
2. Monitor deployment logs in the **"Logs"** tab
3. Wait for all services to start (~5-10 minutes)

### Step 7: Verify Deployment
Check container status in Dokploy **"Containers"** tab or via SSH:

```bash
ssh root@72.60.219.244
docker ps --format 'table {{.Names}}\t{{.Status}}' | wc -l
# Should show ~30 containers (23 services + infrastructure)
```

## Expected Build Time
- **Initial deployment**: 60-75 minutes (builds from source)
- **Subsequent deployments**: 5-10 minutes (uses pre-built images from GHCR)

## Service Health Checks

### Infrastructure Services:
```bash
# PostgreSQL
nc -z 72.60.219.244 5433

# Redis
nc -z 72.60.219.244 6380

# Vault
nc -z 72.60.219.244 8201

# Temporal UI
curl http://72.60.219.244:8083
```

### Backend APIs:
```bash
# Brain Gateway
curl http://72.60.219.244:8001/health

# Saleor
curl http://72.60.219.244:8000/health/

# Wagtail CMS
curl http://72.60.219.244:8002/admin/

# Django CRM
curl http://72.60.219.244:8003/admin/
```

### Frontend Applications:
```bash
# Bizoholic
curl -I https://stg.bizoholic.com

# CorelDove
curl -I https://stg.coreldove.com

# ThrillRing
curl -I https://stg.thrillring.com

# Client Portal
curl -I https://stg.bizoholic.com/login/

# Admin Dashboard
curl -I https://stg.bizoholic.com/admin/

# Business Directory
curl -I https://stg.bizoholic.com/directory/
```

## Troubleshooting

### Services Not Starting
1. Check logs in Dokploy **"Logs"** tab
2. Verify environment variables are set correctly
3. Ensure all images are available in GHCR
4. Check Docker network connectivity

### Frontend 404 Errors
1. Verify Traefik routing labels are applied
2. Check domain DNS records point to KVM4 (72.60.219.244)
3. Ensure SSL certificates are generated
4. Verify subdirectory routing priority in Traefik

### Database Connection Errors
1. Ensure PostgreSQL container is running
2. Check database credentials in environment variables
3. Verify Docker network `dokploy-network` exists
4. Test connection: `docker exec bizosaas-postgres-staging pg_isready`

### Backend API Errors
1. Check if Brain Gateway is running and healthy
2. Verify all backend services can connect to PostgreSQL and Redis
3. Ensure Vault is accessible for secrets management
4. Check API logs for specific error messages

## Monitoring & Maintenance

### View Logs:
**Via Dokploy UI**:
1. Navigate to **"Applications"**
2. Click on service name
3. Go to **"Logs"** tab

**Via SSH**:
```bash
ssh root@72.60.219.244

# All services
cd /opt/bizosaas-platform
docker-compose -f dokploy-staging-complete.yml logs -f

# Specific service
docker logs -f bizosaas-brain-staging
docker logs -f bizosaas-bizoholic-frontend-staging
```

### Restart Services:
**Via Dokploy UI**:
1. Navigate to service
2. Click **"Restart"** button

**Via SSH**:
```bash
ssh root@72.60.219.244
cd /opt/bizosaas-platform

# Restart all
docker-compose -f dokploy-staging-complete.yml restart

# Restart specific service
docker restart bizosaas-brain-staging
```

### Update Deployment:
1. Push changes to GitHub `main` branch
2. Wait for GitHub Actions to build images (~15-20 min)
3. In Dokploy, click **"Redeploy"** button
4. Monitor logs for successful update

## DNS Configuration

Ensure these DNS records point to KVM4:

| Domain | Type | Value | Proxy |
|--------|------|-------|-------|
| stg.bizoholic.com | A | 72.60.219.244 | DNS Only |
| stg.coreldove.com | A | 72.60.219.244 | DNS Only |
| stg.thrillring.com | A | 72.60.219.244 | DNS Only |

**Important**: Use "DNS Only" mode in Cloudflare, NOT "Proxied".

## Post-Deployment Checklist

- [ ] All 23 containers running
- [ ] Infrastructure services healthy (PostgreSQL, Redis, Vault, Temporal)
- [ ] Backend APIs responding on ports 8000-8009
- [ ] Frontend apps accessible via HTTPS
- [ ] Traefik routing subdirectories correctly
- [ ] SSL certificates generated for all domains
- [ ] Brain Gateway accepting requests
- [ ] Database connections working
- [ ] No errors in service logs

## Support

**Issues**: https://github.com/Bizoholic-Digital/bizosaas-platform/issues
**Dokploy Dashboard**: https://dk4.bizoholic.com
**Server**: ssh root@72.60.219.244

---

**Last Updated**: October 25, 2025
**Target Server**: KVM4 (72.60.219.244)
**Total Services**: 23
**Excluded**: CorelDove WordPress (KVM2)
