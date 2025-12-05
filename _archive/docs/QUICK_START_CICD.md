# Quick Start: Deploy CI/CD in 5 Minutes

## Step 1: Add GitHub Secret (2 minutes)

1. Open: https://github.com/Bizoholic-Digital/bizosaas-platform/settings/secrets/actions
2. Click: **"New repository secret"**
3. Enter:
   - **Name**: `DOKPLOY_API_KEY`
   - **Secret**: `bizoholicKRGZxqgQXBDBzumvvnMhiEZLmnetMTAWwTnFztwuGofadbHagGbJiiMZTqczBDKY`
4. Click: **"Add secret"**

## Step 2: Verify Workflow Permissions (1 minute)

1. Open: https://github.com/Bizoholic-Digital/bizosaas-platform/settings/actions
2. Scroll to **"Workflow permissions"**
3. Select: **"Read and write permissions"**
4. Click: **"Save"**

## Step 3: Trigger First Build (1 minute)

### Option A: Empty Commit (Recommended)

```bash
cd /home/alagiri/projects/bizoholic
git commit --allow-empty -m "chore: Trigger initial CI/CD deployment"
git push origin main
```

### Option B: Add Workflow Dispatch

Add this line to `.github/workflows/deploy-staging.yml` after line 9:

```yaml
on:
  push:
    branches: [staging, main]
    paths:
      - 'bizosaas/**'
      - 'dokploy-*-ghcr.yml'
      - '.github/workflows/**'
  workflow_dispatch:  # ADD THIS
```

Then:
1. Go to: https://github.com/Bizoholic-Digital/bizosaas-platform/actions
2. Click: "Deploy to Staging" workflow
3. Click: "Run workflow" button
4. Select: "main" branch
5. Click: "Run workflow"

## Step 4: Monitor Build (1 minute)

1. Open: https://github.com/Bizoholic-Digital/bizosaas-platform/actions
2. Watch live logs
3. Expected duration: **15-20 minutes**

## Step 5: Verify Deployment

```bash
# Test backend
curl http://194.238.16.237:8001/health

# Test frontend
curl http://194.238.16.237:3001/

# Check all services
ssh root@194.238.16.237 'docker ps --filter name=bizosaas'
```

---

## What Happens Behind the Scenes

1. GitHub Actions builds 7 Docker images (parallel)
2. Pushes images to GHCR (ghcr.io/bizoholic-digital/bizosaas-*)
3. Triggers Dokploy backend deployment
4. Waits 60 seconds
5. Triggers Dokploy frontend deployment
6. Done!

---

## Services Being Deployed

| Service | Port | URL |
|---------|------|-----|
| Brain Gateway | 8001 | http://194.238.16.237:8001/health |
| Saleor API | 8000 | http://194.238.16.237:8000/ |
| Wagtail CMS | 8002 | http://194.238.16.237:8002/ |
| Client Portal | 3004 | http://194.238.16.237:3004/ |
| Bizoholic Frontend | 3001 | http://194.238.16.237:3001/ |
| Coreldove Frontend | 3002 | http://194.238.16.237:3002/ |
| Admin Dashboard | 3009 | http://194.238.16.237:3009/ |

---

## Troubleshooting

### Build Failed?

**Error**: "Secret DOKPLOY_API_KEY not found"
- **Fix**: Re-add secret (Step 1)

**Error**: "Permission denied to push to ghcr.io"
- **Fix**: Update workflow permissions (Step 2)

**Error**: "Dockerfile not found"
- **Fix**: Check if Dockerfile exists in service directory

### Deployment Failed?

**Error**: "Connection refused to dk.bizoholic.com"
- **Fix**: Verify Dokploy is running: `curl https://dk.bizoholic.com`

**Error**: "Image pull failed"
- **Fix**: Make GHCR packages public: https://github.com/orgs/Bizoholic-Digital/packages

---

## Emergency Rollback

If deployment breaks production:

```bash
# SSH into VPS
ssh root@194.238.16.237

# Stop broken service
docker stop bizosaas-brain-staging

# Restart with old image
docker start bizosaas-brain-staging

# OR use Dokploy UI to redeploy previous version
# https://dk.bizoholic.com -> Deployments -> Redeploy
```

---

## Full Documentation

See: `/home/alagiri/projects/bizoholic/GITHUB_ACTIONS_SETUP_GUIDE.md`

---

**Ready? Let's deploy!**

```bash
cd /home/alagiri/projects/bizoholic
git commit --allow-empty -m "chore: Trigger CI/CD deployment"
git push origin main
```

Then watch: https://github.com/Bizoholic-Digital/bizosaas-platform/actions
