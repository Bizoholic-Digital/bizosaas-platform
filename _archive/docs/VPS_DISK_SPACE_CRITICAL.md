# VPS Disk Space Critical - Immediate Action Required

**Status**: CRITICAL - Deployment stopped due to disk space
**VPS Usage**: 93.5% of 95.82GB
**Error**: `write: no space left on device`

---

## Immediate Actions Required

### 1. Clean Docker Images and Containers (Highest Priority)
```bash
# On VPS - Remove unused Docker data
ssh root@194.238.16.237 "docker system prune -af --volumes"
```
**Expected Recovery**: 10-20GB

### 2. Clean Docker Build Cache
```bash
# Remove all build cache
ssh root@194.238.16.237 "docker builder prune -af"
```
**Expected Recovery**: 5-10GB

### 3. Clean Temporary Deployment Files
```bash
# Remove uploaded image archives
ssh root@194.238.16.237 "rm -rf /opt/bizosaas-staging/images/*.tar.gz"
```
**Expected Recovery**: 5-10GB

### 4. Clean Old Logs
```bash
# Truncate Docker logs
ssh root@194.238.16.237 "find /var/lib/docker/containers/ -name '*.log' -exec truncate -s 0 {} \;"
```
**Expected Recovery**: 1-3GB

---

## Current Situation

### What Happened
1. Images saved locally: 13 services (backend 8 + frontend 5) ✅
2. Images transferred to VPS: All 13 services ✅
3. Backend images loaded: 8/8 ✅
4. Frontend images loading: 1/5 (failed on admin-dashboard) ❌
5. Error: VPS ran out of disk space at 93.5% usage

### Current VPS State
- **Disk**: 93.5% of 95.82GB used
- **Backend Images**: All 8 loaded successfully
- **Frontend Images**: Only admin-dashboard partially loaded (failed)
- **Remaining**: 4 frontend images not loaded yet

---

## Recovery Plan

### Step 1: Free Up Space (5 minutes)
```bash
# Execute cleanup commands
ssh root@194.238.16.237 << 'EOF'
  echo "🧹 Cleaning Docker system..."
  docker system prune -af --volumes

  echo "🧹 Cleaning build cache..."
  docker builder prune -af

  echo "🧹 Removing deployment archives..."
  rm -rf /opt/bizosaas-staging/images/*.tar.gz

  echo "✅ Cleanup complete"
  df -h | grep -E 'Filesystem|/$'
EOF
```

### Step 2: Verify Available Space
```bash
ssh root@194.238.16.237 "df -h | grep -E 'Filesystem|/$'"
```
**Target**: <70% usage

### Step 3: Resume Image Loading
```bash
# Load remaining 4 frontend images
ssh root@194.238.16.237 << 'EOF'
  cd /opt/bizosaas-staging/images/frontend/

  gunzip -c bizoholic-frontend.tar.gz | docker load
  gunzip -c coreldove-frontend.tar.gz | docker load
  gunzip -c business-directory-frontend.tar.gz | docker load
  gunzip -c admin-dashboard.tar.gz | docker load  # Retry this one

  echo "✅ All frontend images loaded"
EOF
```

### Step 4: Verify All Images Available
```bash
ssh root@194.238.16.237 "docker images | grep -E 'bizosaas|bizoholic'"
```

### Step 5: Deploy via Dokploy
Once images are verified, deploy using local image compose files.

---

## Alternative: Optimized Transfer Strategy

Instead of transferring all images at once, use a **sequential load-and-delete** approach:

```bash
# Modified deployment script
ssh root@194.238.16.237 << 'EOF'
  cd /opt/bizosaas-staging/images/backend/

  for img in *.tar.gz; do
    echo "Loading $img..."
    gunzip -c "$img" | docker load
    echo "Deleting $img to free space..."
    rm -f "$img"
  done

  cd ../frontend/
  for img in *.tar.gz; do
    echo "Loading $img..."
    gunzip -c "$img" | docker load
    echo "Deleting $img to free space..."
    rm -f "$img"
  done
EOF
```

This loads one image at a time and immediately deletes the archive to free space.

---

## Current Deployment Status

### ✅ Successfully Loaded (8 backend services)
1. Brain API (bizosaas-brain-gateway:latest)
2. Wagtail CMS (bizosaas-wagtail-cms:latest)
3. Django CRM (bizoholic-django-crm:latest)
4. Business Directory Backend (bizosaas-business-directory-backend:latest)
5. CorelDove Backend (bizoholic-coreldove-backend:latest)
6. Auth Service (bizoholic-auth-service:latest)
7. AI Agents (bizoholic-ai-agents:latest)
8. Amazon Sourcing (bizosaas/amazon-sourcing:latest)

### ❌ Failed to Load (5 frontend services)
1. Client Portal (bizosaas-client-portal:latest) - NOT LOADED
2. Bizoholic Frontend (bizosaas-bizoholic-frontend:latest) - PARTIAL
3. CorelDove Frontend (bizosaas-coreldove-frontend:latest) - NOT LOADED
4. Business Directory Frontend (bizosaas-business-directory:latest) - NOT LOADED
5. Admin Dashboard (bizosaas-bizosaas-admin:latest) - FAILED

---

## Next Steps After Cleanup

1. ✅ Execute VPS cleanup (Step 1)
2. ✅ Verify disk space recovered
3. ✅ Resume frontend image loading
4. 📝 Update Dokploy compose files with local images
5. 🚀 Trigger backend deployment
6. 🚀 Trigger frontend deployment
7. ✅ Verify all 12 services running

---

## Prevention for Future Deployments

### Option 1: Use GHCR (Recommended Long-term)
- Push images to GitHub Container Registry
- Dokploy pulls directly from GHCR
- No local disk space used for image archives
- Automatic cleanup by Dokploy

### Option 2: Deploy Incrementally
- Deploy services in batches (3-4 at a time)
- Clean up between batches
- Prevents disk space exhaustion

### Option 3: Increase VPS Disk Space
- Current: 95.82GB
- Recommended: 200GB minimum for 22 services
- One-time infrastructure upgrade

---

**Immediate Action**: Execute Step 1 cleanup commands to free up 20-30GB space, then resume deployment.
