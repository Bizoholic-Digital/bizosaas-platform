# 🚨 URGENT: VPS Issues Analysis & Fix Plan

**Date**: 2025-12-15 12:18 UTC  
**Status**: CRITICAL - Immediate Action Required

---

## 🔴 Critical Issue #1: Disk Space (91% Full)

**Current State**: 91 GB / 100 GB used  
**Risk Level**: CRITICAL  
**Impact**: VPS may stop accepting new data, deployments will fail

### Immediate Actions Required

#### 1. Clean Docker Resources (SSH into VPS)

```bash
# SSH into VPS
ssh root@194.238.16.237

# Check current disk usage
df -h

# Clean Docker system (removes unused images, containers, volumes)
docker system prune -a --volumes -f

# This typically frees 20-40 GB

# Check disk usage after cleanup
df -h

# Remove old Docker images
docker images | grep "<none>" | awk '{print $3}' | xargs docker rmi -f

# Remove stopped containers
docker container prune -f

# Remove unused volumes
docker volume prune -f

# Remove build cache
docker builder prune -a -f
```

#### 2. Clean System Logs

```bash
# Check log sizes
du -sh /var/log/*

# Clean old logs
journalctl --vacuum-time=7d
journalctl --vacuum-size=500M

# Clean apt cache
apt-get clean
apt-get autoclean
apt-get autoremove -y
```

#### 3. Check Large Files

```bash
# Find largest directories
du -h --max-depth=1 / 2>/dev/null | sort -hr | head -20

# Find large files
find / -type f -size +500M 2>/dev/null | xargs ls -lh

# Check Docker directory size
du -sh /var/lib/docker
```

#### 4. Optimize Dokploy

```bash
# Clean Dokploy build cache
cd /var/lib/dokploy
docker-compose down
docker system prune -a -f
docker-compose up -d
```

### Expected Results
- **Before**: 91 GB / 100 GB (91% full)
- **After Cleanup**: ~50-60 GB / 100 GB (50-60% full)
- **Space Freed**: 30-40 GB

---

## ⚠️ Issue #2: GitHub Actions Failing

### Analysis

Looking at the failure pattern:
- All workflows on `staging` branch are failing
- But deployments might still work via Dokploy (separate from GitHub Actions)
- Dokploy pulls from GitHub and deploys independently

### Likely Causes

1. **GitHub Actions workflow misconfiguration**
2. **Missing secrets/environment variables**
3. **Build failures in CI (different from Dokploy)**
4. **Disk space on VPS causing deployment failures**

### Investigation Steps

```bash
# 1. Check the workflow file
cat .github/workflows/ci-cd.yml

# 2. Check recent workflow runs
# Visit: https://github.com/Bizoholic-Digital/bizosaas-platform/actions/runs/latest

# 3. Check Dokploy deployment status (on VPS)
ssh root@194.238.16.237
docker ps | grep -E "brain-gateway|client-portal|admin-dashboard"
docker logs brain-gateway --tail 50
docker logs client-portal --tail 50
```

### Two Deployment Paths

**Path 1: GitHub Actions → VPS**
- Builds in GitHub
- Pushes to registry
- Deploys to VPS
- Status: ❌ FAILING

**Path 2: Dokploy → GitHub → VPS**
- Dokploy watches GitHub
- Pulls code on push
- Builds locally on VPS
- Deploys containers
- Status: ✅ LIKELY WORKING (if disk space allows)

---

## 🔧 Immediate Fix Plan

### Priority 1: Free Disk Space (DO THIS FIRST)

```bash
ssh root@194.238.16.237

# Run cleanup script
cat > /tmp/cleanup.sh << 'EOF'
#!/bin/bash
echo "=== Starting Cleanup ==="
echo "Current disk usage:"
df -h /

echo -e "\n=== Cleaning Docker ==="
docker system prune -a --volumes -f

echo -e "\n=== Cleaning Logs ==="
journalctl --vacuum-time=7d
journalctl --vacuum-size=500M

echo -e "\n=== Cleaning APT ==="
apt-get clean
apt-get autoclean
apt-get autoremove -y

echo -e "\n=== Final disk usage ==="
df -h /
EOF

chmod +x /tmp/cleanup.sh
/tmp/cleanup.sh
```

### Priority 2: Verify Deployments

```bash
# Check if services are running
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Check recent deployments in Dokploy
# Visit: http://194.238.16.237:3000 (or your Dokploy URL)

# Test endpoints
curl -I https://api.bizoholic.net/health
curl -I https://app.bizoholic.net/api/health
curl -I https://admin.bizoholic.net/api/health
```

### Priority 3: Fix GitHub Actions (If Needed)

If Dokploy is working but you want GitHub Actions fixed:

1. **Check workflow logs** for specific errors
2. **Verify secrets** are set in GitHub repo settings
3. **Update workflow** if needed
4. **Consider disabling** if Dokploy is sufficient

---

## 📊 Deployment Status Check

### Current Hypothesis

Based on the pattern:
- ✅ **Dokploy IS deploying** (independent of GitHub Actions)
- ❌ **GitHub Actions ARE failing** (CI/CD workflow issues)
- ⚠️ **Disk space IS critical** (may cause future failures)

### Verification Commands

```bash
# SSH into VPS
ssh root@194.238.16.237

# 1. Check if latest commit is deployed
docker exec brain-gateway cat /app/main.py | head -20
# Should show updated imports (cms, crm, ecommerce)

# 2. Check container creation times
docker ps --format "{{.Names}}\t{{.CreatedAt}}"
# Should show recent timestamps if deployed

# 3. Check Dokploy logs
docker logs dokploy --tail 100 | grep -i "deploy"

# 4. Test new endpoints
curl https://api.bizoholic.net/api/cms/pages
curl https://api.bizoholic.net/api/crm/contacts
curl https://api.bizoholic.net/api/ecommerce/products
```

---

## 🎯 Action Items (In Order)

### Step 1: Clean Disk Space (5 minutes)
```bash
ssh root@194.238.16.237
docker system prune -a --volumes -f
journalctl --vacuum-time=7d
apt-get clean && apt-get autoremove -y
df -h
```

### Step 2: Verify Deployment Status (2 minutes)
```bash
docker ps
curl https://api.bizoholic.net/health
curl https://app.bizoholic.net
```

### Step 3: Test New Features (3 minutes)
```bash
# Open browser
https://app.bizoholic.net

# Navigate to Connectors tab
# Check if new UI is visible
```

### Step 4: Monitor Resources (Ongoing)
```bash
# Set up monitoring
watch -n 5 'df -h / && echo "" && docker stats --no-stream'
```

---

## 🚨 If Deployment Failed Due to Disk Space

If services are down:

```bash
# 1. Free space first
docker system prune -a --volumes -f

# 2. Restart Dokploy
systemctl restart dokploy

# 3. Trigger manual deployment in Dokploy UI
# Or force rebuild:
cd /path/to/dokploy/project
docker-compose down
docker-compose up -d --build
```

---

## 📈 Long-Term Solutions

### 1. Increase VPS Disk Space
- Current: 100 GB
- Recommended: 200 GB minimum
- Action: Upgrade VPS plan

### 2. Implement Log Rotation
```bash
# Add to crontab
0 0 * * * docker system prune -f
0 0 * * 0 journalctl --vacuum-time=7d
```

### 3. Monitor Disk Usage
```bash
# Install monitoring
apt-get install -y prometheus-node-exporter
# Configure alerts for >80% disk usage
```

### 4. Optimize Docker Images
- Use multi-stage builds
- Remove unnecessary dependencies
- Use Alpine-based images where possible

---

## 🔍 GitHub Actions Debug (If Needed)

If you want to fix GitHub Actions:

1. **View latest workflow run**:
   ```bash
   # Get workflow logs
   gh run view --log
   ```

2. **Common fixes**:
   - Add missing secrets in GitHub repo settings
   - Update workflow to use correct Docker registry
   - Fix build context paths
   - Add proper environment variables

3. **Or disable GitHub Actions**:
   ```bash
   # Rename workflow to disable
   git mv .github/workflows/ci-cd.yml .github/workflows/ci-cd.yml.disabled
   git commit -m "chore: Disable GitHub Actions (using Dokploy)"
   git push
   ```

---

## ✅ Success Criteria

- [ ] Disk usage < 70%
- [ ] All Docker services running
- [ ] Health endpoints returning 200
- [ ] New connector features accessible
- [ ] No deployment errors in logs

---

**IMMEDIATE ACTION**: Run the disk cleanup commands NOW before proceeding with testing.

**Next Steps After Cleanup**:
1. Verify deployment status
2. Test connector functionality
3. Set up monitoring
4. Plan VPS upgrade
