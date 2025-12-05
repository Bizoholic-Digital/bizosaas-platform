# BizOSaaS Platform - Complete Deployment Automation

**Status**: Ready for execution
**Target**: 22/22 services deployed with domains configured
**Method**: Hybrid automation (scripts + Dokploy UI)

---

## Current Status Summary

**Services Running**: 9/22 (41%)
- Infrastructure: 5/6 (PostgreSQL, Redis, Vault, Temporal UI, Superset)
- Backend: 3/10 (Brain API, Wagtail, Django CRM)
- Frontend: 1/6 (Bizoholic)

**Services Needed**: 13/22 (59%)
- Infrastructure: 1 (Temporal Server)
- Backend: 7 (Saleor, Business Directory, CorelDove, Auth, Temporal Int, AI Agents, Amazon)
- Frontend: 5 (Client Portal, CorelDove, Directory, ThrillRing, Admin)

---

## Automated Deployment Approach

Since direct API automation requires additional configuration, we use a **hybrid approach**:

1. **Automated Scripts**: Pre-deployment checks, monitoring, verification
2. **Manual Deployment**: Dokploy UI for container deployment (one-time setup)
3. **Automated Verification**: Continuous health checking and reporting

---

## Available Automation Scripts

### 1. Pre-Deployment Check
```bash
./check-services.sh
```
**Purpose**: Quick status check of all 22 services
**Duration**: 30 seconds
**Output**: List of running/not-running services

### 2. Full Verification
```bash
./verify-staging-deployment.sh
```
**Purpose**: Comprehensive health check with pass/fail report
**Duration**: 2-3 minutes
**Output**: Detailed status report with percentage

### 3. Deployment Executor (Interactive)
```bash
./final-deployment-executor.sh
```
**Purpose**: Interactive deployment orchestration
**Features**:
- Shows deployment instructions
- Monitors deployment progress
- Generates deployment reports
- Continuous health checking

### 4. API Deployment (Advanced)
```bash
./dokploy-api-deploy.sh
```
**Purpose**: Attempts API-based deployment
**Requires**: Configured Docker context or API credentials

---

## Recommended Deployment Process

### Phase 1: Pre-Deployment (5 minutes)

```bash
cd /home/alagiri/projects/bizoholic/bizosaas-platform

# Check current status
./check-services.sh

# Run full verification
./verify-staging-deployment.sh
```

**Expected Output**:
- 9/22 services running
- Infrastructure mostly ready
- Backend partially deployed
- Frontend needs deployment

### Phase 2: Deploy Backend Services (40 minutes)

**Option A: Via Dokploy UI (Recommended)**

1. Open: https://dk.bizoholic.com
2. Create Project: `backend-services`
3. Add Docker Compose Application:
   - Source: Git Repository
   - Repo: `https://github.com/Bizoholic-Digital/bizosaas-platform.git`
   - Branch: `main`
   - Compose: `bizosaas-platform/dokploy-backend-staging.yml`
4. Add Environment Variables:
   ```bash
   OPENAI_API_KEY=<your-key>
   ANTHROPIC_API_KEY=<your-key>
   AMAZON_ACCESS_KEY=<your-key>
   AMAZON_SECRET_KEY=<your-key>
   ```
5. Click "Deploy"
6. Monitor build logs

**Option B: Automated Monitoring**

While deployment runs in Dokploy UI, monitor progress automatically:

```bash
# Start monitoring in another terminal
./final-deployment-executor.sh

# Select option 2: Monitor deployment progress
```

This will:
- Check service status every 60 seconds
- Report progress as services come online
- Alert when all backend services are healthy
- Generate deployment report

### Phase 3: Deploy Frontend Services (30 minutes)

1. In Dokploy, create Project: `frontend-services`
2. Add Docker Compose Application:
   - Repo: Same as backend
   - Branch: `main`
   - Compose: `bizosaas-platform/dokploy-frontend-staging.yml`
3. Click "Deploy"
4. Continue monitoring with script

**Expected Progress**:
```
Check #1: 9/22 services (41%)
Check #5: 12/22 services (55%)  ← Backend builds starting
Check #10: 16/22 services (73%) ← Backend complete
Check #15: 19/22 services (86%) ← Frontend builds starting
Check #20: 22/22 services (100%) ← ALL COMPLETE
```

### Phase 4: Domain Configuration (15 minutes)

After all containers are running, configure domains in Dokploy:

```bash
# Verify services are ready for domain configuration
curl http://194.238.16.237:3000/api/health  # Should return {"ok":true}
curl http://194.238.16.237:3002/api/health  # Should return {"ok":true}
curl http://194.238.16.237:3005/api/health  # Should return {"ok":true}
```

**Domain Mappings**:
1. `stg.bizoholic.com` → Container: `bizosaas-bizoholic-frontend-staging` (Port 3000)
2. `stg.coreldove.com` → Container: `bizosaas-coreldove-frontend-staging` (Port 3002)
3. `stg.thrillring.com` → Container: `bizosaas-thrillring-gaming-staging` (Port 3005)
4. `stg.portal.bizoholic.com` → Container: `bizosaas-client-portal-staging` (Port 3001)
5. `stg.directory.bizoholic.com` → Container: `bizosaas-business-directory-frontend-staging` (Port 3003)
6. `stg.admin.bizoholic.com` → Container: `bizosaas-admin-dashboard-staging` (Port 3009)

**SSL Configuration**:
- Enable Let's Encrypt for all 6 domains
- Wait 5-10 minutes for certificate generation
- Verify HTTPS access

### Phase 5: Final Verification (10 minutes)

```bash
# Run comprehensive verification
./verify-staging-deployment.sh

# Check domain access
curl -I https://stg.bizoholic.com
curl -I https://stg.coreldove.com
curl -I https://stg.thrillring.com

# Generate final report
./final-deployment-executor.sh  # Option 3: Generate report
```

**Expected Results**:
- All 22 services healthy
- All 6 domains accessible with SSL
- Verification score: 100%

---

## Monitoring During Deployment

### Real-Time Monitoring Script

Run this in a separate terminal while deployment is in progress:

```bash
watch -n 30 './check-services.sh'
```

This will refresh every 30 seconds showing live service status.

### Continuous Monitoring with Alerts

```bash
./final-deployment-executor.sh

# Select option 2 for continuous monitoring
```

This script:
1. Checks status every 60 seconds
2. Reports progress when new services come online
3. Stops automatically when 22/22 services are running
4. Generates final deployment report

---

## Troubleshooting

### Build Failures

If Dokploy build fails:

1. Check build logs in Dokploy UI
2. Common issues:
   - Missing Dockerfile in path
   - Git repository not accessible
   - Missing environment variables
3. Fix and re-deploy

### Service Not Starting

If container builds but won't start:

```bash
# Check specific service
curl http://194.238.16.237:PORT/health

# Check logs in Dokploy UI
# Look for database connection errors
# Verify dependencies are running
```

### Domain Not Accessible

If domain configuration fails:

1. Verify DNS points to 194.238.16.237
2. Check Traefik routing in Dokploy
3. Wait 5-10 minutes for SSL generation
4. Check firewall rules on VPS

---

## Deployment Timeline

| Phase | Duration | Cumulative | Status |
|-------|----------|------------|--------|
| Pre-deployment checks | 5 min | 5 min | ✅ Ready |
| Backend deployment | 40 min | 45 min | 🔄 Pending |
| Frontend deployment | 30 min | 75 min | 🔄 Pending |
| Domain configuration | 15 min | 90 min | 🔄 Pending |
| SSL generation | 10 min | 100 min | 🔄 Pending |
| Final verification | 10 min | 110 min | 🔄 Pending |

**Total Estimated Time**: 110 minutes (~2 hours)

---

## Success Criteria

Deployment is complete when:

1. ✅ All 22 containers running
2. ✅ All health endpoints return 200
3. ✅ All 6 domains accessible
4. ✅ SSL certificates active
5. ✅ Verification score: 100%

---

## Post-Deployment Tasks

After 22/22 services are running:

1. **Test Core Functionality**:
   - User registration via Auth Service
   - Product browsing in CorelDove
   - CRM data entry
   - AI agent queries

2. **Configure Monitoring**:
   - Setup uptime checks
   - Configure alert emails
   - Enable error tracking

3. **Documentation**:
   - Update API documentation
   - Create user guides
   - Document domain access

4. **Security**:
   - Review firewall rules
   - Check SSL configurations
   - Verify API rate limiting

---

## Quick Reference Commands

```bash
# Check all services
./check-services.sh

# Full verification
./verify-staging-deployment.sh

# Interactive executor
./final-deployment-executor.sh

# Watch deployment progress
watch -n 30 './check-services.sh'

# Check specific service
curl http://194.238.16.237:PORT/health

# Test domain
curl -I https://stg.bizoholic.com
```

---

## Support Information

**VPS IP**: 194.238.16.237
**Dokploy**: https://dk.bizoholic.com
**Repository**: https://github.com/Bizoholic-Digital/bizosaas-platform.git
**Branch**: main

**Deployment Files**:
- `/home/alagiri/projects/bizoholic/bizosaas-platform/dokploy-backend-staging.yml`
- `/home/alagiri/projects/bizoholic/bizosaas-platform/dokploy-frontend-staging.yml`

**Automation Scripts**:
- `check-services.sh` - Quick status
- `verify-staging-deployment.sh` - Full verification
- `final-deployment-executor.sh` - Interactive orchestrator
- `dokploy-api-deploy.sh` - API deployment (advanced)

---

## Next Steps

To begin automated deployment:

```bash
cd /home/alagiri/projects/bizoholic/bizosaas-platform

# Start interactive deployment
./final-deployment-executor.sh
```

Select option 1 for instructions, option 2 for monitoring.

---

*Automated Deployment Guide - October 13, 2025*
*Deploy 13 remaining services in 2 hours with hybrid automation*
