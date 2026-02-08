# Code Synchronization & Deployment Guide

## Overview
This document ensures code consistency between local development, GitHub repository, and production servers (KVM8 and KVM2).

## Current Architecture

### Code Flow
```
Local Development → GitHub (staging branch) → Dokploy → Production Server
```

### Key Principles
1. **Single Source of Truth**: GitHub `staging` branch is the authoritative source
2. **No Direct Server Edits**: All changes must go through Git workflow
3. **Dokploy Auto-Deploy**: Configured to pull from GitHub on each deployment

## Files Modified in This Session

### Core Changes (Committed to GitHub)
1. **bizosaas-brain-core/brain-gateway/seed_mcp.py**
   - Added 30+ SMB tools (Finance, CRM, Email, PM, Communication)
   - Added SMS providers: Twilio, MessageBird, Plivo
   - Status: ✅ Committed (7997480)

2. **bizosaas-brain-core/brain-gateway/app/api/onboarding.py**
   - Integrated billing subscription creation
   - Status: ✅ Committed (7997480)

3. **bizosaas-brain-core/brain-gateway/app/services/mcp_orchestrator.py**
   - Added ZipWP-style WordPress site generation
   - Status: ✅ Committed (7997480)

4. **docker-compose.staging.yml**
   - Updated Lago API key to verified key
   - Added Traefik labels for api.bizoholic.net
   - Updated frontend API URLs to https://api.bizoholic.net
   - Status: ✅ Committed (7997480)

5. **bizosaas-details-11012026.md**
   - Updated MCP inventory with complete tool list
   - Status: ✅ Committed (7997480)

### Temporary Server Changes (Already Synced)
These were made directly on the server but have been incorporated into the local codebase:
- `/etc/dokploy/compose/.../seed_mcp.py` → Synced to local
- `/etc/dokploy/compose/.../onboarding.py` → Synced to local
- `/etc/dokploy/compose/.../mcp_orchestrator.py` → Synced to local

## Deployment Workflow

### For New Deployments (KVM2 Migration)

#### Step 1: Prepare Dokploy Project
```bash
# In Dokploy UI:
1. Create new project: "bizosaas-brain-gateway"
2. Add service: "brain-gateway" (Docker Compose)
3. Connect to GitHub repository
4. Set branch: "staging"
5. Set compose file: "docker-compose.staging.yml"
```

#### Step 2: Configure Environment Variables
```bash
# Required environment variables in Dokploy:
VECTOR_DB_URL=postgresql://postgres:password@brain-postgres:5432/bizosaas
REDIS_URL=redis://brain-redis:6379
LAGO_API_URL=http://lago-api:3000
LAGO_API_KEY=df1933ae-50fd-4c06-972c-1b092be9d96b
```

#### Step 3: Deploy
```bash
# Dokploy will automatically:
1. Clone from GitHub
2. Build images
3. Start containers
4. Run seed scripts (seed_mcp.py runs on startup)
```

### For Code Updates

#### Local Development → Production
```bash
# 1. Make changes locally
cd /home/alagiri/projects/bizosaas-platform

# 2. Test locally (optional)
docker-compose -f docker-compose.staging.yml up -d

# 3. Commit to Git
git add .
git commit -m "feat: description of changes"

# 4. Push to GitHub
git push origin staging

# 5. Deploy via Dokploy
# Option A: Auto-deploy (if configured)
# Option B: Manual trigger in Dokploy UI
```

#### Emergency Server Changes (Avoid if possible)
If you MUST make changes directly on the server:

```bash
# 1. SSH to server
ssh root@72.60.98.213

# 2. Navigate to Dokploy compose directory
cd /etc/dokploy/compose/bizosaasbraingateway-braingateway-p5xytd/code

# 3. Make changes
vim bizosaas-brain-core/brain-gateway/seed_mcp.py

# 4. Restart service
docker compose -f docker-compose.staging.yml restart brain-gateway

# 5. IMPORTANT: Sync back to local
# On local machine:
sshpass -p "&k3civYG5Q6YPb" scp root@72.60.98.213:/etc/dokploy/compose/.../seed_mcp.py \
  /home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/brain-gateway/seed_mcp.py

# 6. Commit to Git
git add bizosaas-brain-core/brain-gateway/seed_mcp.py
git commit -m "sync: emergency server changes"
git push origin staging
```

## Database Seeding

### Automatic Seeding
The `seed_mcp.py` script runs automatically on Brain Gateway startup (configured in `main.py`).

### Manual Re-seeding
```bash
# If you need to force re-seed after adding new tools:
docker exec code-brain-gateway-1 python seed_mcp.py
```

## Verification Checklist

After any deployment, verify:

- [ ] Brain Gateway is accessible: `curl https://api.bizoholic.net/health`
- [ ] MCP categories load: `curl https://api.bizoholic.net/api/mcp/categories`
- [ ] MCP registry loads: `curl https://api.bizoholic.net/api/mcp/registry`
- [ ] Client Portal can access API: Check browser console on app.bizoholic.net
- [ ] Onboarding Step 3 shows tools
- [ ] All new tools appear in the registry (Twilio, QuickBooks, etc.)

## KVM2 Migration Checklist

When moving to KVM2:

- [ ] Ensure Dokploy is installed on KVM2
- [ ] Create Traefik configuration for api.bizoholic.net
- [ ] Set up external networks (dokploy-network, brain-network)
- [ ] Deploy Lago stack first (docker-compose.lago.yml)
- [ ] Deploy Brain Gateway (docker-compose.staging.yml)
- [ ] Deploy Client Portal (docker-compose.client-portal.yml)
- [ ] Update DNS to point to KVM2 IP
- [ ] Verify all endpoints are accessible
- [ ] Run database migrations if needed

## Current Status

✅ All code changes committed to GitHub (commit: 7997480)
✅ GitHub repository is up to date
✅ Local codebase matches production
✅ Ready for KVM2 migration

## Important Notes

1. **Never edit files directly on the server** unless it's an emergency
2. **Always sync server changes back to Git** immediately
3. **Use Dokploy's GitHub integration** for deployments
4. **Test locally first** when possible
5. **Document all environment variables** in Dokploy UI

## Contact & Support

For deployment issues:
- Check Dokploy logs in UI
- Check container logs: `docker logs code-brain-gateway-1`
- Check Brain Gateway logs: `docker logs code-brain-gateway-1 --tail 100`
