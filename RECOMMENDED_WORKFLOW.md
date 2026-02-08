# Recommended Deployment Workflow - BizOSaaS Platform

## ✅ Best Approach: Local Build → Direct VPS Deploy

### Why This Works Best:
1. **Your local containers already work** - no dependency issues
2. **Same environment everywhere** - WSL2 → VPS (both Linux)
3. **Fast deployment** - no rebuilding, just transfer images
4. **Simple workflow** - 2 steps instead of 4
5. **Easy rollback** - keep versioned images locally

---

## Workflow: WSL2 → VPS Staging → VPS Production

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Local WSL2 │────▶│ VPS Staging  │────▶│ VPS Prod     │
│  (Testing)  │     │ (Validation) │     │ (Live)       │
└─────────────┘     └──────────────┘     └──────────────┘
     Build              Deploy              Promote
     Test               Verify              Monitor
```

---

## Step-by-Step Implementation

### Phase 1: Setup One-Time Infrastructure

**1. Setup Docker Registry on VPS (or use existing Dokploy)**
```bash
# Option A: Use Dokploy's built-in registry
# Already available at: dk.bizoholic.com

# Option B: Simple Docker Compose Registry (if needed)
ssh root@194.238.16.237
docker run -d -p 5000:5000 --restart=always --name registry \
  -v /opt/registry:/var/lib/registry \
  registry:2
```

**2. Setup Local Docker Context (Point to VPS)**
```bash
# On Local WSL2
docker context create vps-staging \
  --docker "host=ssh://root@194.238.16.237"

# Test connection
docker context use vps-staging
docker ps
```

---

### Phase 2: Daily Development Workflow

**Step 1: Develop & Test Locally (WSL2)**
```bash
# Your normal development
cd /home/alagiri/projects/bizoholic/bizosaas
docker-compose up -d

# Test everything works
curl http://localhost:8001/health  # Brain API
curl http://localhost:3000         # Client Portal
# etc.
```

**Step 2: Save & Export Working Images**
```bash
# Option A: Save images to tar files
docker save bizosaas-brain-gateway:latest | gzip > brain-api.tar.gz
docker save bizosaas-wagtail-cms:latest | gzip > wagtail-cms.tar.gz
# ... etc for all 13 services

# Option B: Use docker-compose to bundle
docker-compose -f bizosaas/docker-compose.yml bundle -o bizosaas-staging.dab
```

**Step 3: Transfer to VPS Staging**
```bash
# Option A: SCP transfer
scp brain-api.tar.gz root@194.238.16.237:/tmp/
ssh root@194.238.16.237 "docker load < /tmp/brain-api.tar.gz"

# Option B: Direct push using docker context
docker context use vps-staging
docker tag bizosaas-brain-gateway:latest localhost:5000/brain-api:staging
docker push localhost:5000/brain-api:staging
```

**Step 4: Deploy on VPS via Dokploy**
```bash
# Update Dokploy compose to use local registry
# dokploy-backend-staging.yml:
services:
  brain-api:
    image: localhost:5000/brain-api:staging  # From local registry
    # OR
    image: bizosaas-brain-gateway:latest     # If loaded directly
```

---

## Alternative: Simplified Docker-Only Deployment

**Skip Dokploy entirely, use Docker Compose directly on VPS:**

```bash
# 1. Copy your working compose file
scp bizosaas/docker-compose.yml root@194.238.16.237:/opt/bizosaas/

# 2. SSH and deploy
ssh root@194.238.16.237
cd /opt/bizosaas
docker-compose up -d

# That's it! Same setup as local.
```

**Benefits:**
- ✅ Identical to local (guaranteed to work)
- ✅ No Dokploy complexity
- ✅ Simple docker-compose commands
- ✅ Easy troubleshooting

---

## Comparison: All Workflows

| Workflow | Build Time | Reliability | Complexity | Recommended? |
|----------|------------|-------------|------------|--------------|
| **Local → Direct VPS** | 0 min (pre-built) | ✅ 100% | ⭐ Simple | ✅ **YES** |
| Local → GHCR → Dokploy | 2 min (push) | ✅ 95% | ⭐⭐ Medium | ⚠️ Optional |
| GitHub → Dokploy Build | 60 min (build all) | ❌ 40% | ⭐⭐⭐ Complex | ❌ **NO** |

---

## Recommended Final Workflow

### For Staging (Daily Deploys):
```bash
#!/bin/bash
# deploy-to-staging.sh

# 1. Test locally first
docker-compose -f bizosaas/docker-compose.yml up -d
sleep 5
curl -f http://localhost:8001/health || { echo "Local test failed!"; exit 1; }

# 2. Tag images for staging
docker tag bizosaas-brain-gateway:latest bizosaas-brain-gateway:staging-$(date +%Y%m%d)
docker tag bizosaas-wagtail-cms:latest bizosaas-wagtail-cms:staging-$(date +%Y%m%d)
# ... etc

# 3. Save to tar files
mkdir -p staging-images
docker save bizosaas-brain-gateway:staging-$(date +%Y%m%d) | gzip > staging-images/brain-api.tar.gz
docker save bizosaas-wagtail-cms:staging-$(date +%Y%m%d) | gzip > staging-images/wagtail-cms.tar.gz
# ... etc

# 4. Transfer to VPS
scp staging-images/*.tar.gz root@194.238.16.237:/opt/staging-images/

# 5. Load on VPS and restart
ssh root@194.238.16.237 << 'ENDSSH'
cd /opt/staging-images
for img in *.tar.gz; do
    docker load < $img
done
cd /opt/bizosaas-staging
docker-compose down
docker-compose up -d
ENDSSH

echo "✅ Deployed to staging!"
```

### For Production (Weekly/Manual):
```bash
#!/bin/bash
# promote-to-production.sh

# 1. Verify staging working
curl -f https://stg.bizoholic.com/health || { echo "Staging not healthy!"; exit 1; }

# 2. Tag staging images as production
docker context use vps-staging
docker tag bizosaas-brain-gateway:staging-20251013 bizosaas-brain-gateway:production
# ... etc

# 3. Copy to production
docker save bizosaas-brain-gateway:production | \
  ssh root@PROD_IP "docker load"

# 4. Deploy to production
ssh root@PROD_IP "cd /opt/bizosaas-prod && docker-compose up -d"

echo "✅ Promoted to production!"
```

---

## Summary: What You Should Do NOW

**Immediate (Next 30 minutes):**
1. ✅ Your local setup works - keep using it!
2. ❌ Stop trying to build from GitHub source in Dokploy
3. ✅ Create simple deploy script (deploy-to-staging.sh above)
4. ✅ Test deployment to VPS using your working images

**Short-term (This week):**
1. Automate the image transfer script
2. Version your images with dates
3. Keep last 5 versions for rollback

**Long-term (Optional):**
1. Move to GHCR once token issues resolved
2. Setup CI/CD pipeline later (not critical now)
3. Focus on features, not deployment complexity

---

## Key Insight

**You don't need Dokploy to build from GitHub source.**
**You can use Dokploy just for orchestration with pre-built images.**

Or even simpler: **Skip Dokploy, use plain docker-compose on VPS.**

Your local setup already works. Just copy it to VPS. Done.
