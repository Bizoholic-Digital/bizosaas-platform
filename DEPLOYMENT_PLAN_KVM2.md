# BizOSaaS Platform - KVM2 Deployment Plan
**Created:** 2026-01-20  
**Server:** KVM2 (194.238.16.237)  
**Status:** In Progress

---

## Current Status Analysis

### ✅ **Working Services**
1. **Vault Server** (`app-hack-multi-byte-application-um7u9p`)
   - Status: Running as Docker Swarm service
   - Domain: `vault.bizoholic.net` (Cloudflare 522 - needs Traefik routing)
   - Issue: Not exposed via Traefik yet

2. **Core Stack - Build Phase**
   - Status: Images built successfully ✅
   - Brain Gateway: **Restarting** (missing DATABASE_URL env var)
   - All MCP Servers: Running ✅
   - Issue: Missing environment variables

3. **Lago Stack**
   - Status: DB and Redis running
   - API/Worker/Front: Not started yet
   - Issue: Waiting for Vault connection

### ❌ **Failing Services**
1. **Client Portal** - Build errors
2. **Admin Portal** - Build errors  
3. **Business Directory** - Build errors

---

## Root Cause Analysis

### Issue #1: GitHub vs Git Configuration
**Current:** Using `customGitUrl` (generic git)  
**Recommended:** Use `sourceType: "github"` with GitHub App integration

**Why GitHub is Better:**
- ✅ Automatic webhook integration for CI/CD
- ✅ Better authentication (GitHub App vs PAT)
- ✅ Commit status updates
- ✅ Native Dokploy UI support

**Action Required:**
- Install Dokploy GitHub App on `Bizoholic-Digital` organization
- Reconfigure all stacks to use `sourceType: "github"`

### Issue #2: Missing Environment Variables
**Brain Gateway Error:**
```
sqlalchemy.exc.ArgumentError: Could not parse SQLAlchemy URL from string ''
```

**Missing Variables:**
- `DATABASE_URL` - Not passed to container
- `VECTOR_DB_URL` - Not set
- `REDIS_URL` - Not passed correctly

**Root Cause:** Environment variables set in Dokploy UI but not being injected into containers.

### Issue #3: Traefik Domain Configuration
**Current State:**
- Vault: No Traefik labels (522 error from Cloudflare)
- Brain Gateway: Has labels but not routing (522 error)

**Issue:** Traefik is running but not detecting services because:
1. Services are in `brain-network` but Traefik needs `dokploy-network`
2. Domain labels exist but service not in correct network

### Issue #4: Portal Build Failures
**Likely Causes:**
1. Missing build context (building from repo root vs portal subdirectory)
2. Missing build args
3. Dockerfile path issues

---

## Comprehensive Fix Plan

### Phase 1: Fix Vault Traefik Routing (5 min)
**Goal:** Make `vault.bizoholic.net` accessible

**Steps:**
1. Update Vault application to add Traefik labels via API
2. Ensure service is on `dokploy-network`
3. Verify SSL certificate generation

**Script:**
```python
# Update vault-server with Traefik labels
update_application({
    "applicationId": "xFPHD7N1DMPeqqzjYAqlC",
    "labelsSwarm": {
        "traefik.enable": "true",
        "traefik.http.routers.vault.rule": "Host(`vault.bizoholic.net`)",
        "traefik.http.routers.vault.entrypoints": "websecure",
        "traefik.http.routers.vault.tls": "true",
        "traefik.http.routers.vault.tls.certresolver": "letsencrypt",
        "traefik.http.services.vault.loadbalancer.server.port": "8200"
    }
})
```

### Phase 2: Fix Core Stack Environment Variables (10 min)
**Goal:** Get Brain Gateway running

**Actions:**
1. Update `docker-compose.core.yml` to use external DB URLs as defaults
2. Set global environment variables in Dokploy project
3. Redeploy core-stack

**Required Env Vars:**
```bash
DATABASE_URL=postgresql://neondb_owner:npg_puEbTnkSO9F8@ep-gentle-flower-a15rdh2r-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
VECTOR_DB_URL=postgresql://neondb_owner:npg_puEbTnkSO9F8@ep-gentle-flower-a15rdh2r-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
REDIS_URL=redis://default:Gt7QxXA4ybMzYzD9e6KIBULfnv1IU6f9@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690/0
JWT_SECRET=vdMxrD6bZpZk6lClpkSP56+WNapkPAG5lY+BojEA/u7ffehUKcVL7re6xRaPWUCZffoxXF9ZFuU+KcZSWpz6CA==
VAULT_TOKEN=staging-root-token-bizosaas-2025
OPENAI_API_KEY=sk-proj-************************************************************
ANTHROPIC_API_KEY=sk-ant-********************************************************
GOOGLE_API_KEY=AIzaSy*******************************
```

### Phase 3: Fix Portal Docker Compose Files (15 min)
**Goal:** Ensure portals build correctly from GitHub

**Issues to Fix:**
1. **Build Context:** All portals use `context: .` (repo root) but Dockerfiles expect portal subdirectory
2. **Dockerfile Paths:** Need to verify paths are correct
3. **Build Args:** Ensure all NEXT_PUBLIC_* vars are passed

**Fix for `docker-compose.client-portal.yml`:**
```yaml
services:
  client-portal:
    build:
      context: .  # Repo root
      dockerfile: ./portals/client-portal/Dockerfile.prod  # ✅ Correct
      args:
        # Pass all required build args
        NEXT_PUBLIC_API_BASE_URL: ${NEXT_PUBLIC_API_BASE_URL:-https://api.bizoholic.net}
        NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: ${NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY}
        CLERK_SECRET_KEY: ${CLERK_SECRET_KEY}
```

**Verification Needed:**
- Check if `Dockerfile.prod` exists in each portal
- Verify Dockerfile COPY commands match build context

### Phase 4: Migrate to GitHub Source Type (20 min)
**Goal:** Enable proper CI/CD with GitHub webhooks

**Prerequisites:**
1. Install Dokploy GitHub App on `Bizoholic-Digital` org
2. Grant access to `bizosaas-platform` repository

**Migration Steps:**
1. Get GitHub App installation ID
2. Update all compose stacks:
```python
update_compose({
    "composeId": "QiOdwXQi4ZQCM3Qg_KNcl",
    "sourceType": "github",
    "repository": "bizosaas-platform",
    "owner": "Bizoholic-Digital",
    "branch": "staging",
    "composePath": "./docker-compose.core.yml",
    "githubId": "<installation_id>"
})
```

### Phase 5: Configure All Domains (10 min)
**Goal:** Ensure all services are accessible via their domains

**Domains to Configure:**
1. `vault.bizoholic.net` → Vault Server (port 8200)
2. `api.bizoholic.net` → Brain Gateway (port 8000)
3. `app.bizoholic.net` → Client Portal (port 3000)
4. `admin.bizoholic.net` → Admin Portal (port 3000)
5. `directory.bizoholic.net` → Business Directory (port 3005)
6. `billing-api.bizoholic.net` → Lago API (port 3000)
7. `billing.bizoholic.net` → Lago Front (port 80)

**Method:** Domains are configured in docker-compose files via Traefik labels (already done ✅)

### Phase 6: Deploy Lago Stack (5 min)
**Goal:** Get billing engine running

**Actions:**
1. Ensure Vault is accessible from Lago containers
2. Verify `lago-init-all-from-vault.sh` script is in repo
3. Deploy lago-stack

---

## Execution Order

### Immediate Actions (Next 30 min)
1. ✅ **Fix Vault Traefik routing** (make it accessible)
2. ✅ **Update core-stack environment variables** (fix Brain Gateway)
3. ✅ **Verify portal Dockerfiles exist** (check repo)
4. ✅ **Fix portal docker-compose files** (correct build context issues)

### Post-Deployment Actions (Next 60 min)
5. ⏳ **Migrate to GitHub source type** (enable CI/CD)
6. ⏳ **Deploy all portal stacks** (client, admin, directory)
7. ⏳ **Deploy Lago stack** (billing engine)
8. ⏳ **Verify all domains resolve** (test HTTPS)

### Final Verification
- [ ] All services show "Running" in Dokploy
- [ ] All domains return 200 OK (not 522)
- [ ] Brain Gateway `/health` endpoint responds
- [ ] Client Portal login page loads
- [ ] Admin Portal login page loads
- [ ] Vault UI accessible

---

## Recommended: GitHub vs Git

**Use GitHub Source Type Because:**
1. **Automatic Webhooks:** Push to `staging` → Auto-deploy
2. **Better Security:** GitHub App tokens vs Personal Access Tokens
3. **Commit Statuses:** See deployment status in GitHub UI
4. **Easier Management:** No need to manage SSH keys or PATs

**Migration is Simple:**
- Install GitHub App (1-click in Dokploy UI)
- Update source type via API (script provided)
- All existing configurations preserved

---

## Next Steps

**Immediate (You):**
1. Confirm you want to proceed with GitHub source type
2. Verify portal Dockerfiles exist in repo

**Immediate (Me):**
1. Fix Vault Traefik routing
2. Update core-stack env vars
3. Fix portal compose files
4. Deploy all stacks

**Post-Deployment:**
- Monitor logs for any errors
- Test all endpoints
- Configure Loki/Grafana for monitoring
- Plan WordPress migration to shared hosting
