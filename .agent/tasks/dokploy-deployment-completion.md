# Dokploy Deployment Completion Plan

## Current Status Summary (2026-01-29 14:42 UTC)

### ✅ Successfully Deployed Services

1. **Vault (Infrastructure)** - Status: `done` ✅
   - Container: `vault`
   - Status: Running (health: starting)
   - Compose Path: `docker-compose.vault.yml`
   - Source: GitHub (Bizoholic-Digital/bizosaas-platform:staging)

2. **Core Stack (Backend Services)** - Status: `done` ✅
   - Compose Path: `docker-compose.core.yml`
   - Running Containers:
     - `bizosaas-brain-staging` (Brain Gateway) - Healthy
     - `brain-mcp-brave-search` - Healthy
     - `brain-mcp-filesystem` - Healthy
     - `brain-mcp-github` - Healthy
     - `brain-mcp-google-drive` - Healthy
     - `brain-mcp-slack` - Healthy
     - `brain-mcp-fluentcrm` - Healthy

3. **Portals Apps (Frontend)** - Status: `done` ✅
   - Compose Path: `docker-compose.client-portal.yml`
   - Running Containers:
     - `compose-generate-open-source-transmitter-kks6gu-client-portal-1` - Healthy
     - `bizosaas-platform-client-portal-1` - Healthy (6 hours uptime)

### 🔧 Configuration Details

**Dokploy Projects:**
- `platform-core` (ID: p4fmYaVZ_iDFDH4XSDnOU)
  - vault (Compose ID: osD7Up5T4VcZzok5yLyXo)
  - core-stack (Compose ID: QiOdwXQi4ZQCM3Qg_KNcl)
  
- `portals` (ID: WfVYVHpPQh_h5s4GpyDdW)
  - portals-apps (Compose ID: zz6VpI3h8BFXPUTZZb01G)

**GitHub Integration:**
- Repository: `Bizoholic-Digital/bizosaas-platform`
- Branch: `staging`
- GitHub App ID: `QZnupLM5a8IgYpTloLpdZ`
- Auto-deploy: Enabled for all services

---

## 🎯 Remaining Tasks

### Phase 1: Verify and Document Current State

#### Task 1.1: Health Check All Services
- [ ] Verify Vault is fully healthy and accessible
- [ ] Check all Brain MCP services are responding
- [ ] Test Brain Gateway API endpoints
- [ ] Verify Client Portal is accessible and functional
- [ ] Document any services showing warnings or errors

#### Task 1.2: Network and Routing Verification
- [ ] Verify Traefik routing for all services
- [ ] Check domain configurations:
  - [ ] `vault.bizoholic.net` → Vault
  - [ ] `api.bizoholic.net` → Brain Gateway
  - [ ] `app.bizoholic.net` → Client Portal
- [ ] Test SSL certificates are valid
- [ ] Verify inter-service communication (brain-network)

#### Task 1.3: Environment Variables Audit
- [ ] Verify all required env vars are set in Dokploy:
  - [ ] `VAULT_DEV_ROOT_TOKEN_ID`
  - [ ] `GITHUB_TOKEN`
  - [ ] `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`
  - [ ] `SLACK_BOT_TOKEN`
  - [ ] `BRAVE_API_KEY`
  - [ ] `FLUENTCRM_URL` / `FLUENTCRM_API_KEY`
  - [ ] `DATABASE_URL` (Neon PostgreSQL)
  - [ ] `REDIS_URL` (Redis Cloud)
  - [ ] `TEMPORAL_ADDRESS` / `TEMPORAL_NAMESPACE`

---

### Phase 2: Missing Services Deployment

#### Task 2.1: Admin Dashboard
**Status:** Not yet deployed
**Priority:** HIGH

**Steps:**
1. Review `docker-compose.admin-portal.yml`
2. Create/update Dokploy compose entry
3. Configure environment variables:
   - `NEXTAUTH_SECRET`
   - `VAULT_URL` / `VAULT_TOKEN`
   - `AUTHENTIK_CLIENT_ID` / `AUTHENTIK_CLIENT_SECRET`
   - `NEXT_PUBLIC_STRIPE_PUBLIC_KEY`
4. Set compose path to `docker-compose.admin-portal.yml`
5. Deploy and verify

**Expected Outcome:**
- Admin Dashboard accessible at `admin.bizoholic.net`
- SSO integration with Authentik working
- Vault integration functional

#### Task 2.2: Business Directory
**Status:** Running but not in Dokploy GitHub workflow
**Priority:** MEDIUM

**Current State:**
- Container `business-directory` is running (2 days uptime)
- Needs to be migrated to GitHub-based deployment

**Steps:**
1. Review `docker-compose.directory.yml`
2. Create Dokploy compose entry in `portals` project
3. Configure GitHub source
4. Deploy and verify continuity

#### Task 2.3: Authentik SSO
**Status:** Running but needs verification
**Priority:** HIGH

**Current State:**
- Containers running:
  - `authentik-sso-hxogz6-authentik-server-1` (healthy)
  - `authentik-sso-hxogz6-authentik-worker-1` (unhealthy)

**Steps:**
1. Investigate worker unhealthy status
2. Review `docker-compose.authentik.yml`
3. Verify Dokploy compose configuration
4. Fix worker health issues
5. Test SSO flow for both portals

---

### Phase 3: GitHub CI/CD Workflow Restoration

#### Task 3.1: Resolve Git Push Protection Issues
**Blocker:** GitHub Secret Scanning blocking push

**Identified Secrets in Commits:**
- GitHub Personal Access Token in `DOKPLOY_INTEGRATION_STATUS.md`
- Anthropic API Key in `project_all_start.json` and `project_info.json`

**Resolution Steps:**
1. ✅ Remove sensitive files from git tracking (COMPLETED)
2. ✅ Add files to `.gitignore` (COMPLETED)
3. [ ] Push changes to GitHub
4. [ ] Verify auto-deploy triggers for all services
5. [ ] Test full CI/CD workflow:
   - Make local change
   - Commit and push
   - Verify Dokploy auto-deploys

#### Task 3.2: GHCR Authentication Fix
**Status:** BLOCKED - Invalid PAT

**Issue:**
- Current PAT (`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`) returns "denied" for GHCR
- Dokploy cannot pull images from `ghcr.io/bizoholic-digital/*`

**Required Action:**
- User needs to generate new GitHub PAT with:
  - `read:packages` scope
  - `repo` scope
  - `workflow` scope (optional, for GitHub Actions)

**Steps After New PAT:**
1. Update Dokploy registry settings (ID: `20SzyK6MhITruzOvD26c_`)
2. Test image pull manually
3. Re-deploy services to verify GHCR access

---

### Phase 4: Monitoring and Optimization

#### Task 4.1: Resource Monitoring
- [ ] Review container resource usage
- [ ] Identify any containers exceeding limits
- [ ] Optimize resource allocations if needed
- [ ] Set up alerts for resource thresholds

#### Task 4.2: Logging Configuration
- [ ] Verify all services are logging properly
- [ ] Configure log rotation
- [ ] Set up centralized logging (if needed)

#### Task 4.3: Backup Strategy
- [ ] Verify Vault data persistence
- [ ] Document backup procedures
- [ ] Test restore procedures

---

## 📋 Pre-Development Checklist

Before starting new development work, ensure:

- [ ] All services are deployed and healthy
- [ ] GitHub CI/CD workflow is fully functional
- [ ] GHCR authentication is working
- [ ] All environment variables are documented
- [ ] Domain routing is verified
- [ ] SSL certificates are valid
- [ ] Inter-service communication is tested
- [ ] Backup procedures are in place

---

## 🚨 Known Issues

1. **Authentik Worker Unhealthy**
   - Impact: SSO may be degraded
   - Priority: HIGH
   - Action: Investigate logs and fix

2. **GHCR Authentication Failure**
   - Impact: Cannot pull new images
   - Priority: CRITICAL
   - Action: User must provide new PAT

3. **Git Push Protection**
   - Impact: Cannot push to staging branch
   - Priority: HIGH
   - Action: Remove secrets from commit history

---

## 📝 Notes

- All services are now using GitHub as source (no more RAW mode)
- Auto-deploy is enabled for automatic updates on push
- Vault is using `docker-compose.vault.yml` (not `dokploy-infrastructure-staging.yml`)
- Core stack uses `docker-compose.core.yml`
- Portals use `docker-compose.client-portal.yml`
- The consolidated `dokploy-*-staging.yml` files exist but are not currently used

---

## Next Immediate Actions

1. **User Action Required:** Provide new GitHub PAT with `read:packages` scope
2. **Push to GitHub:** Once secrets are removed, push staging branch
3. **Deploy Admin Dashboard:** High priority for platform completeness
4. **Fix Authentik Worker:** Critical for SSO functionality
5. **Verify All Domains:** Ensure routing and SSL are working

---

**Last Updated:** 2026-01-29 14:42 UTC
**Status:** 3/3 Core Services Deployed ✅ | Admin Dashboard Pending | GHCR Auth Blocked
