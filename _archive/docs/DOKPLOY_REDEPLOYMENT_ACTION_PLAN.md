# Dokploy Redeployment Action Plan
**Date**: 2025-10-13
**Status**: Build Failures - Requires Manual Intervention

## Current Status Summary

### Infrastructure Layer ✅ HEALTHY
- **Project**: bizosaas_infrastructure_staging (8aGGQnNJMycKORdg5nFip)
- **Compose ID**: 3xkedHPvMZJa1BDtwGIJO
- **Status**: `done` (all services running)
- **Services**: 9 containers including PostgreSQL, Redis, Vault, Temporal, Superset

### Backend Services ❌ FAILED
- **Project**: bizosaas_backend_staging (hEv_lJzlNChWpMj_GusEf)
- **Compose ID**: uimFISkhg1KACigb2CaGz
- **App Name**: backend-services-azbmbl
- **Status**: `error`
- **Current Config**: `./dokploy-backend-staging.yml`
- **Error**: Build failure in `temporal-integration` service (pip install failed)

### Frontend Services ❌ FAILED
- **Project**: bizosaas_frontend_staging (lypG2IONOtjn_oBXYHc92)
- **Compose ID**: hU2yhYOqv3_ftKGGvcAiv
- **App Name**: frontend-services-a89ci2
- **Status**: `error`
- **Current Config**: `./dokploy-frontend-staging.yml`
- **Error**: Build failure in `business-directory-frontend` service (npm build failed)
- **Domains**: 6 staging domains configured

## Problem Analysis

### Root Cause
The current compose files (`dokploy-backend-staging.yml` and `dokploy-frontend-staging.yml`) attempt to build ALL services from GitHub, but several services have:
1. Missing or incomplete `requirements.txt` / `package.json` files
2. Incorrect build contexts
3. Services that don't exist yet in repository
4. Build configuration errors

### Failing Services
**Backend**:
- `temporal-integration` - Missing requirements.txt or dependency resolution failure
- Possibly others (build stopped at first failure)

**Frontend**:
- `business-directory-frontend` - npm build script failure
- Possibly others (build stopped at first failure)

## Available Alternative Configurations

### Option A: Working Services Only (RECOMMENDED)
**File**: `dokploy-backend-staging-working.yml`
- **Services**: 3 verified working services
  - Wagtail CMS (8002)
  - Django CRM (8003)
  - Saleor API (8000) - pre-built image
- **Pros**: Known to build successfully
- **Cons**: Missing 7 backend services

**File**: `dokploy-frontend-staging-simplified.yml` (need to verify contents)
- Unknown service count, needs inspection

### Option B: Pre-built Images
**File**: `dokploy-backend-staging-prebuilt.yml`
- **Requires**: Images with tags like `backend-services-azbmbl-*:latest`
- **Problem**: These images don't exist in local registry or Docker Hub
- **Would need**: Manual build and push of all images first

### Option C: Fix Current Files
**Files**: Current `dokploy-backend-staging.yml` and `dokploy-frontend-staging.yml`
- **Requires**: Fix Dockerfiles, requirements files, and build contexts in GitHub repo
- **Time**: Several hours to debug and test each service
- **Risk**: High - may discover more broken services

## Recommended Solution: Incremental Deployment

### Phase 1: Deploy Working Backend Services (IMMEDIATE)
1. **Manually update compose path in Dokploy UI**:
   - Navigate to Backend project → Compose deployment
   - Change path from `./dokploy-backend-staging.yml` to `./dokploy-backend-staging-working.yml`
   - Save and redeploy

2. **Expected Result**: 3 backend services running
   - Saleor API at port 8000
   - Wagtail CMS at port 8002
   - Django CRM at port 8003

### Phase 2: Deploy Simplified Frontend (NEXT)
1. **Check simplified frontend contents**:
   ```bash
   curl -s "https://raw.githubusercontent.com/Bizoholic-Digital/bizosaas-platform/main/dokploy-frontend-staging-simplified.yml"
   ```

2. **Update compose path in Dokploy UI**:
   - Navigate to Frontend project → Compose deployment
   - Change path to `./dokploy-frontend-staging-simplified.yml`
   - Save and redeploy

### Phase 3: Add Additional Services (GRADUAL)
For each missing service:
1. Verify service code exists in GitHub repo
2. Check Dockerfile and requirements.txt exist and are correct
3. Test build locally
4. Add to working compose file
5. Push update and redeploy
6. Verify service health
7. Move to next service

## Manual Steps Required (Cannot be done via API)

### Step 1: Update Backend Compose Path
**Location**: https://dk.bizoholic.com
**Navigation**: Projects → bizosaas_backend_staging → Staging Environment → backend_staging compose

**Action**:
1. Click "Edit" or settings icon
2. Find "Compose Path" field (currently: `./dokploy-backend-staging.yml`)
3. Change to: `./dokploy-backend-staging-working.yml`
4. Save changes
5. Click "Redeploy" or "Deploy" button

**Expected**: Build should succeed with 3 services

### Step 2: Update Frontend Compose Path
**Location**: https://dk.bizoholic.com
**Navigation**: Projects → bizosaas_frontend_staging → Staging Environment → frontend_services compose

**Action**:
1. Click "Edit" or settings icon
2. Find "Compose Path" field (currently: `./dokploy-frontend-staging.yml`)
3. Change to: `./dokploy-frontend-staging-simplified.yml`
4. Save changes
5. Click "Redeploy" or "Deploy" button

**Expected**: Build should succeed (need to verify simplified file first)

### Step 3: Verify Deployments
After both updates:

```bash
# Check compose status
curl -s -X GET "https://dk.bizoholic.com/api/compose.one?composeId=uimFISkhg1KACigb2CaGz" \
  -H "X-API-Key: agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi" \
  | jq '{status: .composeStatus, path: .composePath}'

curl -s -X GET "https://dk.bizoholic.com/api/compose.one?composeId=hU2yhYOqv3_ftKGGvcAiv" \
  -H "X-API-Key: agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi" \
  | jq '{status: .composeStatus, path: .composePath}'

# Check running containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep staging
```

## Alternative: Delete and Recreate Compose Deployments

If editing isn't possible, delete and recreate:

### Delete Current Deployments
```bash
# Via API (if delete endpoint exists)
curl -X DELETE "https://dk.bizoholic.com/api/compose.remove" \
  -H "X-API-Key: agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi" \
  -H "Content-Type: application/json" \
  -d '{"composeId": "uimFISkhg1KACigb2CaGz"}'

# Or manually in Dokploy UI
```

### Create New Compose Deployments
```bash
# Create new backend compose (pseudo-API call, check actual endpoint)
curl -X POST "https://dk.bizoholic.com/api/compose.create" \
  -H "X-API-Key: agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi" \
  -H "Content-Type: application/json" \
  -d '{
    "projectId": "hEv_lJzlNChWpMj_GusEf",
    "name": "backend_working_services",
    "sourceType": "github",
    "repository": "bizosaas-platform",
    "owner": "Bizoholic-Digital",
    "branch": "main",
    "composePath": "./dokploy-backend-staging-working.yml",
    "autoDeploy": true
  }'
```

## Service Inventory: What's Running vs What's Needed

### Currently Running (Outside Compose)
✅ Infrastructure services (9 containers - healthy)
✅ Some backend services from old deployment:
- bizosaas-brain-unified (port 8001)
- bizosaas-django-crm-8003 (unhealthy)
- coreldove-backend-8005
- bizosaas-business-directory-backend-8004
- bizosaas-temporal-unified (port 8009)

### Stopped (From Old Deployment)
❌ Frontend services (all stopped 2 days ago):
- coreldove-frontend-3002
- bizoholic-frontend-3000
- bizosaas-client-portal-3001
- thrillring-gaming-3005

❌ Some backend services:
- bizosaas-wagtail-cms
- bizosaas-ai-agents-8010
- amazon-sourcing-8085
- bizosaas-saleor-unified

### Target Architecture (22 containers)
**Infrastructure**: 9 containers ✅
**Backend**: 10 containers ❌ (only 3 can build currently)
**Frontend**: 6 containers ❌ (unknown how many can build)

## Next Actions

### IMMEDIATE (You can do)
1. ✅ Document current status (DONE - this file)
2. ⏳ Check frontend simplified file contents
3. ⏳ Provide manual steps to user

### USER MUST DO (Manual Dokploy UI)
1. ⏳ Update backend compose path to working version
2. ⏳ Update frontend compose path to simplified version
3. ⏳ Trigger redeployment of both
4. ⏳ Verify services are healthy

### FUTURE (After working deployment)
1. ⏳ Fix build issues for remaining 7 backend services
2. ⏳ Fix build issues for remaining frontend services
3. ⏳ Add services incrementally
4. ⏳ Configure domain routing for all services
5. ⏳ Set up monitoring and alerts
6. ⏳ Document service dependencies and startup order

## Reference Information

### API Endpoints Used
- **Get Projects**: `GET /api/project.all`
- **Get Compose**: `GET /api/compose.one?composeId=<id>`
- **Deploy Compose**: `POST /api/compose.deploy` with `{"composeId": "<id>"}`
- **Redeploy Compose**: `POST /api/compose.redeploy` with `{"composeId": "<id>"}`
- **Start Compose**: `POST /api/compose.start` with `{"composeId": "<id>"}`
- **Stop Compose**: `POST /api/compose.stop` with `{"composeId": "<id>"}`

### API Authentication
- **Header**: `X-API-Key` (not Bearer token)
- **Key**: `agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi`

### GitHub Repository
- **Org**: Bizoholic-Digital
- **Repo**: bizosaas-platform
- **Branch**: main
- **Compose Files Location**: Root directory

### Dokploy Instance
- **URL**: https://dk.bizoholic.com
- **Organization**: Y-SEgS66udYaAsN3hM4_J

## Monitoring Commands

```bash
# Check all compose deployments status
for id in "3xkedHPvMZJa1BDtwGIJO" "uimFISkhg1KACigb2CaGz" "hU2yhYOqv3_ftKGGvcAiv"; do
  echo "=== Compose ID: $id ==="
  curl -s -X GET "https://dk.bizoholic.com/api/compose.one?composeId=$id" \
    -H "X-API-Key: agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi" \
    | jq '{name: .name, status: .composeStatus, path: .composePath}'
  echo ""
done

# Check all running containers
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}" | grep -E "(bizosaas|staging)"

# Check container health
docker ps --filter "health=unhealthy" --format "table {{.Names}}\t{{.Status}}"
```

## Success Criteria

### Phase 1 Complete When:
- [ ] Backend compose status shows `done` or `running`
- [ ] At least 3 backend containers are running and healthy:
  - [ ] bizosaas-saleor-staging (port 8000)
  - [ ] bizosaas-wagtail-staging (port 8002)
  - [ ] bizosaas-django-crm-staging (port 8003)

### Phase 2 Complete When:
- [ ] Frontend compose status shows `done` or `running`
- [ ] Frontend containers are running (count depends on simplified file)
- [ ] Domains resolve correctly to services

### Full Deployment Complete When:
- [ ] All 22 containers running (9 infra + 10 backend + 6 frontend)
- [ ] All services passing health checks
- [ ] All domains resolving correctly
- [ ] No error status in any compose deployment

---

**Last Updated**: 2025-10-13
**Next Review**: After manual compose path updates are complete
