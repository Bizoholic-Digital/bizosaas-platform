# Backend Deployment Fix - Network Configuration Issue

**Date**: 2025-10-13
**Issue**: Backend services cannot connect to PostgreSQL/Redis
**Root Cause**: Network mismatch between infrastructure and backend services
**Status**: FIXED - Ready for redeployment

---

## Problem Diagnosis

### Infrastructure Services (Working)
The infrastructure is deployed and running on VPS at 194.238.16.237:
- PostgreSQL: External port 5433, Internal port 5432
- Redis: External port 6380, Internal port 6379
- Vault: External port 8201, Internal port 8200
- Temporal Server: External port 7234, Internal port 7233
- Temporal UI: External port 8083, Internal port 8080
- Superset: External port 8088, Internal port 8088

**Network**: dokploy-network
**Container Names**:
- bizosaas-postgres-staging
- bizosaas-redis-staging
- bizosaas-vault-staging
- bizosaas-temporal-server-staging
- bizosaas-temporal-ui-staging
- bizosaas-superset-staging

### Backend Services (Failing)
Backend services were trying to connect to infrastructure but failing.

**Root Cause Identified**:
The original `dokploy-backend-staging.yml` file used **"bizosaas-staging-network"** while infrastructure uses **"dokploy-network"**.

This meant:
1. Backend containers were in a different network
2. Could not resolve DNS names like "bizosaas-postgres-staging"
3. Connection attempts failed with "host not found" or timeout errors

---

## Solution Applied

### File Updated
**File**: `/home/alagiri/projects/bizoholic/dokploy-backend-staging-corrected.yml`

### Changes Made
1. Changed network from `bizosaas-staging-network` to `dokploy-network`
2. Kept all container names and connection strings the same
3. Backend services will now be in the same network as infrastructure

### Network Configuration
```yaml
networks:
  dokploy-network:
    external: true
```

All 10 backend services now use:
```yaml
services:
  service-name:
    networks:
      - dokploy-network  # Changed from bizosaas-staging-network
```

---

## Backend Services in Corrected Configuration

### 1. Saleor E-commerce API (Port 8000)
- Image: ghcr.io/saleor/saleor:3.20
- Database: saleor_staging
- Redis DB: 1

### 2. Brain API - AI Gateway (Port 8001)
- Build from: bizosaas-platform/ai/services/bizosaas-brain
- Database: bizosaas_staging
- Redis DB: 0

### 3. Wagtail CMS (Port 8002)
- Build from: bizosaas-platform/backend/services/cms
- Database: bizosaas_staging
- Redis DB: 3

### 4. Django CRM (Port 8003)
- Build from: bizosaas-platform/backend/services/crm/django-crm
- Database: bizosaas_staging
- Redis DB: 4

### 5. Business Directory Backend (Port 8004)
- Build from: bizosaas-platform/backend/services/crm/business-directory
- Database: bizosaas_staging
- Redis DB: 5

### 6. CorelDove Backend (Port 8005)
- Build from: bizosaas/ecommerce/services/coreldove-backend
- Database: bizosaas_staging
- Redis DB: 6

### 7. Authentication Service (Port 8006)
- Build from: bizosaas-platform/backend/services/auth
- Database: bizosaas_staging
- Redis DB: 10

### 8. Temporal Integration (Port 8007)
- Build from: bizosaas-platform/backend/services/temporal
- Database: bizosaas_staging
- Redis DB: 7

### 9. AI Agents (Port 8008)
- Build from: bizosaas-platform/backend/services/ai-agents
- Database: bizosaas_staging
- Redis DB: 8

### 10. Amazon Sourcing (Port 8009)
- Build from: bizosaas-platform/backend/services/amazon-sourcing
- Database: bizosaas_staging
- Redis DB: 9

---

## Deployment Instructions

### Step 1: Access Dokploy
```bash
# Open in browser
http://194.238.16.237:3000
```

### Step 2: Navigate to Backend Project
1. Click on "Projects" in left sidebar
2. Find "bizosaas-backend-staging" project
3. Click on the Docker Compose application

### Step 3: Update Configuration
1. Click on "Edit" or "Configuration" tab
2. Delete existing compose file content
3. Copy entire content from `/home/alagiri/projects/bizoholic/dokploy-backend-staging-corrected.yml`
4. Paste into Dokploy editor
5. Save configuration

### Step 4: Deploy
1. Click "Deploy" button
2. Monitor build logs for errors
3. Wait for all 10 services to build (20-30 minutes)
4. Check deployment status

### Step 5: Verify Connectivity
Once deployment completes, verify services can connect:

```bash
# Test from VPS
ssh root@194.238.16.237

# Check if backend can reach postgres
docker exec bizosaas-brain-staging nc -zv bizosaas-postgres-staging 5432

# Check if backend can reach redis
docker exec bizosaas-brain-staging nc -zv bizosaas-redis-staging 6379

# Check container network
docker inspect bizosaas-brain-staging | grep NetworkMode
# Should show: dokploy-network

# List all containers in dokploy-network
docker network inspect dokploy-network | grep Name
```

### Step 6: Health Check
Test service endpoints:
```bash
# From local machine or VPS
curl http://194.238.16.237:8000/health/  # Saleor
curl http://194.238.16.237:8001/health   # Brain API
curl http://194.238.16.237:8002/admin/login/  # Wagtail
curl http://194.238.16.237:8003/admin/login/  # Django CRM
curl http://194.238.16.237:8004/health   # Business Directory
curl http://194.238.16.237:8005/health   # CorelDove
curl http://194.238.16.237:8006/health   # Auth Service
curl http://194.238.16.237:8007/health   # Temporal Integration
curl http://194.238.16.237:8008/health   # AI Agents
curl http://194.238.16.237:8009/health   # Amazon Sourcing
```

---

## Expected Results

### Before Fix
- Backend services start but crash/restart constantly
- Logs show database connection errors
- Health checks fail
- Status: "Restarting" or "Unhealthy"

### After Fix
- Backend services start successfully
- Database connections established
- Health checks pass
- Status: "Running" and "Healthy"
- Logs show successful database migrations

---

## Troubleshooting

### If Services Still Can't Connect

#### Option A: Verify Network
```bash
# Check if dokploy-network exists
docker network ls | grep dokploy

# Inspect network to see all containers
docker network inspect dokploy-network

# Expected to see:
# - bizosaas-postgres-staging
# - bizosaas-redis-staging
# - bizosaas-brain-staging
# - etc.
```

#### Option B: Check Container Names
```bash
# List all running containers
docker ps --format "table {{.Names}}\t{{.Networks}}"

# Verify infrastructure containers are named correctly
docker ps | grep postgres  # Should show: bizosaas-postgres-staging
docker ps | grep redis     # Should show: bizosaas-redis-staging
```

#### Option C: Manual Connection Test
```bash
# Try connecting to postgres from VPS
PGPASSWORD="BizOSaaS2025!StagingDB" psql -h 127.0.0.1 -p 5433 -U admin -d bizosaas_staging

# Try redis
redis-cli -h 127.0.0.1 -p 6380 PING
```

#### Option D: Check Logs
```bash
# Check backend service logs for specific errors
docker logs bizosaas-brain-staging --tail 50
docker logs bizosaas-wagtail-staging --tail 50
docker logs bizosaas-django-crm-staging --tail 50
```

---

## Alternative: If Infrastructure Has Different Container Names

If `docker ps` shows infrastructure containers with different names, update the configuration:

### Find Actual Container Names
```bash
docker ps | grep postgres
docker ps | grep redis
```

### Update Connection Strings
In `dokploy-backend-staging-corrected.yml`, replace:
- `bizosaas-postgres-staging` with actual PostgreSQL container name
- `bizosaas-redis-staging` with actual Redis container name

Example:
```yaml
environment:
  - DATABASE_URL=postgresql://admin:BizOSaaS2025!StagingDB@<ACTUAL_POSTGRES_NAME>:5432/bizosaas_staging
  - REDIS_URL=redis://<ACTUAL_REDIS_NAME>:6379/0
```

---

## Commit and Push

After verifying the fix works, commit the changes:

```bash
cd /home/alagiri/projects/bizoholic

# Add corrected file
git add dokploy-backend-staging-corrected.yml
git add BACKEND_DEPLOYMENT_FIX.md

# Commit
git commit -m "fix: Backend network configuration - change to dokploy-network

- Changed all backend services from bizosaas-staging-network to dokploy-network
- Matches infrastructure network configuration
- Enables proper DNS resolution between containers
- All 10 backend services updated
- Documented troubleshooting steps"

# Push to GitHub
git push origin main
```

---

## Summary

**Problem**: Network mismatch preventing backend-to-infrastructure communication
**Solution**: Updated all backend services to use dokploy-network
**File**: `/home/alagiri/projects/bizoholic/dokploy-backend-staging-corrected.yml`
**Status**: Ready for deployment
**Expected Time**: 20-30 minutes for full deployment
**Success Criteria**: All 10 services show "Running" and "Healthy" status

---

## Next Steps After Successful Deployment

1. Verify all 10 backend services are healthy
2. Test critical endpoints (Brain API, Saleor, Auth)
3. Run database migrations if needed
4. Configure domain names for staging
5. Proceed with frontend deployment (Phase 3)
6. Set up monitoring and logging
7. Document any issues encountered

---

**Generated**: 2025-10-13
**Author**: Claude Code (DevOps Automation)
**VPS**: 194.238.16.237
**Dokploy**: http://194.238.16.237:3000
