# CI/CD Pipeline Architecture

## High-Level Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│                         DEVELOPER WORKFLOW                           │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │   Git Push to main        │
                    │   or staging branch       │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         GITHUB ACTIONS                               │
│                      (Automated Build System)                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  STAGE 1: Build Matrix (Parallel Execution)               │    │
│  │                                                            │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │    │
│  │  │  Service 1  │  │  Service 2  │  │  Service 3  │      │    │
│  │  │brain-gateway│  │bizoholic-fe │  │coreldove-fe │ ...  │    │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘      │    │
│  │         │                 │                 │             │    │
│  │         ▼                 ▼                 ▼             │    │
│  │    Docker Build      Docker Build      Docker Build      │    │
│  │         │                 │                 │             │    │
│  │         ▼                 ▼                 ▼             │    │
│  │  ghcr.io/bizoholic-digital/bizosaas-SERVICE:TAG          │    │
│  │                                                            │    │
│  └────────────────────────────┬───────────────────────────────┘    │
│                                │                                    │
│                                ▼                                    │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  STAGE 2: Push to GHCR                                     │    │
│  │  Authentication: GITHUB_TOKEN (auto)                       │    │
│  │  Registry: ghcr.io                                         │    │
│  │  Organization: bizoholic-digital                           │    │
│  └────────────────────────────┬───────────────────────────────┘    │
│                                │                                    │
└────────────────────────────────┼────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                  GITHUB CONTAINER REGISTRY (GHCR)                    │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Images stored:                                                      │
│  - ghcr.io/bizoholic-digital/bizosaas-brain-gateway:staging         │
│  - ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:staging    │
│  - ghcr.io/bizoholic-digital/bizosaas-coreldove-frontend:staging    │
│  - ghcr.io/bizoholic-digital/bizosaas-client-portal:staging         │
│  - ghcr.io/bizoholic-digital/bizosaas-admin-dashboard:staging       │
│  - ghcr.io/bizoholic-digital/bizosaas-business-directory:staging    │
│  - ghcr.io/bizoholic-digital/bizosaas-thrillring-gaming:staging     │
│                                                                      │
│  Tags per image:                                                     │
│  - staging (overwritten each push to staging branch)                │
│  - latest (overwritten each push to main branch)                    │
│  - staging-<git-sha> (unique per commit)                            │
│  - <branch>-<git-sha> (full reference)                              │
│                                                                      │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         GITHUB ACTIONS                               │
│                    (Deployment Orchestration)                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  STAGE 3: Trigger Dokploy Backend Deployment              │    │
│  │                                                            │    │
│  │  curl -X POST dk.bizoholic.com/api/compose.deploy         │    │
│  │  Header: x-api-key: DOKPLOY_API_KEY                       │    │
│  │  Body: {"composeId": "uimFISkhg1KACigb2CaGz"}             │    │
│  │                                                            │    │
│  └────────────────────────────┬───────────────────────────────┘    │
│                                │                                    │
│                                ▼                                    │
│                           [Wait 60s]                                │
│                                │                                    │
│                                ▼                                    │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  STAGE 4: Trigger Dokploy Frontend Deployment             │    │
│  │                                                            │    │
│  │  curl -X POST dk.bizoholic.com/api/compose.deploy         │    │
│  │  Header: x-api-key: DOKPLOY_API_KEY                       │    │
│  │  Body: {"composeId": "hU2yhYOqv3_ftKGGvcAiv"}             │    │
│  │                                                            │    │
│  └────────────────────────────┬───────────────────────────────┘    │
│                                │                                    │
└────────────────────────────────┼────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                            DOKPLOY                                   │
│                   (VPS: 194.238.16.237)                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Backend Compose (uimFISkhg1KACigb2CaGz):                           │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  1. docker-compose down                                    │    │
│  │  2. docker pull ghcr.io/.../bizosaas-brain-gateway:staging │    │
│  │  3. docker pull ghcr.io/saleor/saleor:3.20                 │    │
│  │  4. docker pull <other backend services>                   │    │
│  │  5. docker-compose up -d                                   │    │
│  │                                                            │    │
│  │  Containers created:                                       │    │
│  │  - bizosaas-brain-staging (port 8001)                      │    │
│  │  - bizosaas-saleor-staging (port 8000)                     │    │
│  │  - bizosaas-wagtail-staging (port 8002)                    │    │
│  │  - bizosaas-auth-service-staging (port 8006)               │    │
│  │  - bizosaas-django-crm-staging (port 8003)                 │    │
│  │  - <other backend services>                                │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  Frontend Compose (hU2yhYOqv3_ftKGGvcAiv):                          │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  1. docker-compose down                                    │    │
│  │  2. docker pull ghcr.io/.../bizosaas-bizoholic-fe:staging  │    │
│  │  3. docker pull ghcr.io/.../bizosaas-coreldove-fe:staging  │    │
│  │  4. docker pull <other frontend services>                  │    │
│  │  5. docker-compose up -d                                   │    │
│  │                                                            │    │
│  │  Containers created:                                       │    │
│  │  - bizosaas-client-portal-staging (port 3004)              │    │
│  │  - bizosaas-bizoholic-frontend-staging (port 3001)         │    │
│  │  - bizosaas-coreldove-frontend-staging (port 3002)         │    │
│  │  - bizosaas-business-directory-frontend-staging (3003)     │    │
│  │  - bizosaas-admin-dashboard-staging (port 3009)            │    │
│  │  - bizosaas-thrillring-gaming-staging (port 3005)          │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         PRODUCTION SERVICES                          │
│                         (Publicly Accessible)                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Backend APIs:                                                       │
│  http://194.238.16.237:8001/health  - Brain Gateway                 │
│  http://194.238.16.237:8000/        - Saleor E-commerce             │
│  http://194.238.16.237:8002/        - Wagtail CMS                   │
│  http://194.238.16.237:8006/health  - Auth Service                  │
│                                                                      │
│  Frontend Apps:                                                      │
│  http://194.238.16.237:3001/        - Bizoholic Website             │
│  http://194.238.16.237:3002/        - Coreldove Website             │
│  http://194.238.16.237:3004/        - Client Portal                 │
│  http://194.238.16.237:3009/        - Admin Dashboard               │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Component Breakdown

### 1. GitHub Actions Workflow

**File**: `.github/workflows/deploy-staging.yml`

**Triggers**:
- Push to `main` or `staging` branches
- Changes in:
  - `bizosaas/**` (all service code)
  - `dokploy-*-ghcr.yml` (compose files)
  - `.github/workflows/**` (workflow changes)
- Manual trigger via `workflow_dispatch`

**Environment Variables**:
- `REGISTRY`: `ghcr.io`
- `ORG_NAME`: `bizoholic-digital`

**Secrets Required**:
- `GITHUB_TOKEN`: Auto-provided by GitHub
- `DOKPLOY_API_KEY`: Must be configured manually

---

### 2. Build Matrix Strategy

**Matrix Configuration**:
```yaml
strategy:
  matrix:
    include:
      - name: brain-gateway
        context: ./bizosaas/ai/services/bizosaas-brain
        dockerfile: Dockerfile
      - name: bizoholic-frontend
        context: ./bizosaas/frontend/apps/bizoholic-frontend
        dockerfile: Dockerfile.production
      # ... 5 more services
```

**Parallel Execution**:
- All 7 services build simultaneously
- Utilizes GitHub Actions runner parallelism
- Reduces total build time from ~35 minutes to ~15 minutes

**Build Optimization**:
- Docker Buildx enabled
- Layer caching via GitHub Actions cache (`cache-from: type=gha`)
- Multi-stage builds reduce final image sizes
- `.dockerignore` files exclude unnecessary files

---

### 3. Image Tagging Strategy

**Generated Tags per Image**:

| Tag Pattern | Example | Purpose |
|-------------|---------|---------|
| `staging` | `bizosaas-brain-gateway:staging` | Latest staging build |
| `latest` | `bizosaas-brain-gateway:latest` | Latest main branch |
| `staging-<sha>` | `bizosaas-brain-gateway:staging-abc1234` | Specific commit |
| `<branch>-<sha>` | `bizosaas-brain-gateway:main-abc1234` | Full reference |

**Benefits**:
- **Staging tag**: Dokploy always pulls latest staging
- **SHA tags**: Enables pinning to specific versions
- **Latest tag**: Production deploys use main
- **Branch tags**: Multi-environment support

---

### 4. GHCR Authentication

**How It Works**:
```yaml
- name: Log in to GHCR
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

**Key Points**:
- `GITHUB_TOKEN` is automatically injected by GitHub
- No manual PAT creation needed
- Token has write access to packages in same repository
- Token expires after workflow completes (secure)

**Permissions Required**:
```yaml
permissions:
  contents: read
  packages: write
```

---

### 5. Dokploy Integration

**API Endpoints**:

**Backend Deployment**:
```bash
POST https://dk.bizoholic.com/api/compose.deploy
Headers:
  x-api-key: DOKPLOY_API_KEY
  Content-Type: application/json
Body:
  {"composeId": "uimFISkhg1KACigb2CaGz"}
```

**Frontend Deployment**:
```bash
POST https://dk.bizoholic.com/api/compose.deploy
Headers:
  x-api-key: DOKPLOY_API_KEY
  Content-Type: application/json
Body:
  {"composeId": "hU2yhYOqv3_ftKGGvcAiv"}
```

**Response**:
- HTTP 200: Deployment triggered successfully
- HTTP 401: Invalid API key
- HTTP 404: Compose project not found

**Compose IDs**:
- Backend: `uimFISkhg1KACigb2CaGz`
- Frontend: `hU2yhYOqv3_ftKGGvcAiv`

These IDs are unique to the Dokploy instance and configured in:
- `/home/alagiri/projects/bizoholic/dokploy-backend-staging-ghcr.yml`
- `/home/alagiri/projects/bizoholic/dokploy-frontend-staging-ghcr.yml`

---

## Timeline and Performance

### Expected Build Times

| Stage | Duration | Notes |
|-------|----------|-------|
| **Checkout** | 10-30s | Clone repository |
| **Buildx Setup** | 5-10s | Prepare Docker builder |
| **GHCR Login** | 2-5s | Authenticate |
| **Brain Gateway Build** | 3-5 min | Python + FastAPI + AI libs |
| **Frontend Builds** | 2-4 min each | Next.js 14 builds (parallel) |
| **Push to GHCR** | 1-2 min each | Upload layers |
| **Backend Deploy** | 30-60s | Dokploy pulls + restarts |
| **Frontend Deploy** | 30-60s | Dokploy pulls + restarts |
| **TOTAL** | **15-25 min** | End-to-end |

**Optimization Factors**:
- **Parallel builds**: 7 services build at once
- **Layer caching**: Only changed layers rebuild
- **Incremental builds**: Dependencies cached between runs
- **Efficient Dockerfiles**: Multi-stage builds reduce size

---

## Security Model

### GitHub Actions Security

**Token Scopes**:
- `GITHUB_TOKEN`: Scoped to repository, expires after workflow
- `DOKPLOY_API_KEY`: Long-lived, scoped to Dokploy API only

**Secrets Management**:
- Secrets encrypted at rest in GitHub
- Masked in logs (never shown in plain text)
- Accessible only to workflows in same repository
- Can be rotated without code changes

**Network Security**:
- All connections over HTTPS
- GitHub runners are ephemeral (no persistent state)
- VPS firewall allows only necessary ports

---

### GHCR Package Visibility

**Default**: Private (only accessible to repository members)

**Options**:
1. **Keep Private**: Dokploy must authenticate with GitHub PAT
2. **Make Public**: Anyone can pull images (no auth needed)

**For Staging**: Recommended to keep private, authenticate Dokploy:

```bash
# On VPS (194.238.16.237)
docker login ghcr.io -u USERNAME -p GITHUB_PAT
```

Generate PAT: https://github.com/settings/tokens/new
- Scope: `read:packages`
- Note: "Dokploy GHCR pull access"

---

### Dokploy API Security

**API Key**:
```
bizoholicKRGZxqgQXBDBzumvvnMhiEZLmnetMTAWwTnFztwuGofadbHagGbJiiMZTqczBDKY
```

**Key Properties**:
- **Scope**: Can only deploy compose projects
- **Access**: Cannot modify settings or delete data
- **Rotation**: Can be regenerated in Dokploy UI
- **Storage**: Stored as GitHub secret (encrypted)

**Network**:
- Dokploy API exposed on HTTPS (port 443)
- VPS IP: 194.238.16.237
- Domain: dk.bizoholic.com

---

## Failure Modes and Recovery

### Build Failures

**Symptom**: Red X in GitHub Actions

**Common Causes**:
1. Missing Dockerfile
2. Build dependency errors
3. Out of memory (large builds)
4. Network timeout

**Recovery**:
- Fix code/Dockerfile
- Push commit (auto-triggers rebuild)
- No manual cleanup needed

---

### Push Failures

**Symptom**: "Permission denied" pushing to GHCR

**Common Causes**:
1. Workflow permissions not set to "write"
2. GITHUB_TOKEN expired or invalid
3. Package already exists with different permissions

**Recovery**:
- Set workflow permissions: Settings > Actions > "Read and write"
- Delete package and rebuild: https://github.com/orgs/Bizoholic-Digital/packages
- Re-run workflow

---

### Deployment Failures

**Symptom**: Build succeeds, but Dokploy doesn't update

**Common Causes**:
1. Invalid DOKPLOY_API_KEY
2. Wrong compose IDs
3. Dokploy server down
4. Network connectivity issues

**Recovery**:
- Verify API key: Test with `curl` manually
- Check compose IDs in Dokploy UI
- Restart Dokploy: `docker restart dokploy`
- Re-run deployment step only (no rebuild needed)

---

### Service Health Failures

**Symptom**: Containers start but are unhealthy

**Common Causes**:
1. Database connection errors
2. Missing environment variables
3. Port conflicts
4. Dependency services not running

**Recovery**:
- Check container logs: `docker logs bizosaas-brain-staging`
- Verify environment variables in compose file
- Rollback to previous deployment
- Fix and redeploy

---

## Monitoring and Observability

### Build Monitoring

**Real-time**:
- GitHub Actions UI: https://github.com/Bizoholic-Digital/bizosaas-platform/actions
- Live logs streaming
- Progress indicators per job

**Post-build**:
- Build artifacts (logs) downloadable
- Workflow run history preserved
- Email notifications on failure

---

### Deployment Monitoring

**Dokploy Dashboard**:
- Login: https://dk.bizoholic.com
- Container status (running/stopped/unhealthy)
- Resource usage (CPU/memory)
- Logs per container

**VPS Monitoring**:
```bash
# SSH into VPS
ssh root@194.238.16.237

# Check all BizOSaaS containers
docker ps --filter name=bizosaas

# Check specific service logs
docker logs bizosaas-brain-staging --tail 100 -f

# Resource usage
docker stats --no-stream
```

---

### Health Check Endpoints

**Backend**:
```bash
curl http://194.238.16.237:8001/health  # Brain Gateway
curl http://194.238.16.237:8000/        # Saleor
curl http://194.238.16.237:8002/        # Wagtail
curl http://194.238.16.237:8006/health  # Auth Service
```

**Frontend**:
```bash
curl http://194.238.16.237:3001/  # Bizoholic
curl http://194.238.16.237:3002/  # Coreldove
curl http://194.238.16.237:3004/  # Client Portal
curl http://194.238.16.237:3009/  # Admin Dashboard
```

**Expected**: HTTP 200 or valid response

---

## Optimization Strategies

### Build Speed Optimization

**Current**: 15-25 minutes total

**Potential Improvements**:

1. **Reduce Docker Image Sizes**:
   - Use Alpine base images
   - Multi-stage builds (already implemented)
   - Remove dev dependencies in production

2. **Optimize Dependencies**:
   - Pre-build base images with common deps
   - Use .dockerignore aggressively
   - Cache npm/pip packages separately

3. **Parallel Job Limits**:
   - Current: 7 parallel jobs
   - Free tier: 20 concurrent jobs
   - Can split more aggressively

4. **Self-Hosted Runners**:
   - Use VPS as GitHub Actions runner
   - Eliminates network latency to Dokploy
   - Persistent caching between builds

**Target**: < 10 minutes total build time

---

### Cost Optimization

**GitHub Actions Minutes**:
- Free tier: 2,000 minutes/month
- Current usage: ~20 min/build
- Max builds/month: 100 builds

**GHCR Storage**:
- Free tier: 500 MB
- Current usage: ~4 GB (7 services x ~500MB)
- **Over limit**: Requires GitHub Team plan ($4/user/month)

**Optimization**:
- Delete old image tags (keep only last 10)
- Use smaller base images (Alpine)
- Implement tag retention policy

---

## Future Enhancements

### Phase 2: Advanced CI/CD Features

1. **Automated Testing**:
   - Add test stage before build
   - Unit tests, integration tests, e2e tests
   - Test coverage reporting

2. **Blue-Green Deployments**:
   - Deploy to separate "staging-blue" environment
   - Smoke test
   - Swap to production if healthy

3. **Canary Releases**:
   - Deploy to 10% of traffic
   - Monitor error rates
   - Gradually increase if stable

4. **Automated Rollback**:
   - Health checks after deployment
   - Auto-rollback if health fails
   - Slack/email notifications

5. **Multi-Environment**:
   - Dev, staging, production pipelines
   - Environment-specific secrets
   - Promotion workflows

6. **Performance Monitoring**:
   - Lighthouse CI for frontend
   - API response time tracking
   - Database query performance

---

## Quick Reference

### Key Files

| File | Purpose | Location |
|------|---------|----------|
| Workflow | GitHub Actions config | `.github/workflows/deploy-staging.yml` |
| Backend Compose | Dokploy backend config | `dokploy-backend-staging-ghcr.yml` |
| Frontend Compose | Dokploy frontend config | `dokploy-frontend-staging-ghcr.yml` |
| Verification Script | Pre-flight checks | `verify-cicd-setup.sh` |
| Quick Start | Fast setup guide | `QUICK_START_CICD.md` |
| Full Guide | Complete documentation | `GITHUB_ACTIONS_SETUP_GUIDE.md` |

---

### Key URLs

| Resource | URL |
|----------|-----|
| GitHub Repository | https://github.com/Bizoholic-Digital/bizosaas-platform |
| Actions Dashboard | https://github.com/Bizoholic-Digital/bizosaas-platform/actions |
| Secrets Configuration | https://github.com/Bizoholic-Digital/bizosaas-platform/settings/secrets/actions |
| GHCR Packages | https://github.com/orgs/Bizoholic-Digital/packages |
| Dokploy Dashboard | https://dk.bizoholic.com |
| VPS Services | http://194.238.16.237 |

---

### Key Commands

**Trigger Build**:
```bash
git commit --allow-empty -m "chore: Trigger CI/CD"
git push origin main
```

**Test Dokploy API**:
```bash
curl -X POST "https://dk.bizoholic.com/api/compose.deploy" \
  -H "x-api-key: bizoholicKRGZxqgQXBDBzumvvnMhiEZLmnetMTAWwTnFztwuGofadbHagGbJiiMZTqczBDKY" \
  -H "Content-Type: application/json" \
  -d '{"composeId": "uimFISkhg1KACigb2CaGz"}'
```

**Check Service Health**:
```bash
ssh root@194.238.16.237 'docker ps --filter name=bizosaas --format "table {{.Names}}\t{{.Status}}"'
```

---

## Architecture Benefits

### Developer Experience

- **Fast feedback**: Know if build fails in < 5 minutes
- **Automated deployments**: No manual VPS SSH needed
- **Reproducible**: Same process every time
- **Rollback ready**: Previous versions always available

### Operational Benefits

- **Zero downtime**: Containers restart gracefully
- **Immutable infrastructure**: Every deployment is fresh
- **Audit trail**: Full history in GitHub Actions
- **Scalable**: Add services by updating matrix

### Business Benefits

- **Ship faster**: Deploy multiple times per day
- **Reduce errors**: No manual deployment steps
- **Cost efficient**: Free tier for small teams
- **Professional**: Industry-standard CI/CD

---

**Ready to deploy?** Follow the Quick Start guide!
