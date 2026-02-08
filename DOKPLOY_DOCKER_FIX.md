# Dokploy Docker Error Fix
**Date:** November 17, 2025
**Error:** `spawn docker ENOENT`

---

## 🔍 Error Analysis

### Error Message
```
Error ❌
spawn docker ENOENT
```

**Meaning:** Dokploy cannot find or execute the `docker` command.

**ENOENT** = "Error NO ENTry" = File/command not found

### Secondary Issue
```
tail: inotify cannot be used, reverting to polling: Too many open files
```

This indicates the system has too many open file handles (inotify watches).

---

## 🔧 Fixes Required

### Fix 1: Verify Docker Installation on VPS

**Connect to VPS and check Docker:**

```bash
# SSH to VPS
ssh root@72.60.219.244

# Check if Docker is installed
docker --version

# Check Docker service status
systemctl status docker

# If Docker is not running, start it
systemctl start docker
systemctl enable docker
```

### Fix 2: Check Dokploy User Permissions

**Dokploy needs Docker access:**

```bash
# SSH to VPS
ssh root@72.60.219.244

# Check which user runs Dokploy
ps aux | grep dokploy

# Add Dokploy user to docker group (if needed)
# Replace 'dokploy' with actual user if different
usermod -aG docker dokploy

# Restart Dokploy after permission change
systemctl restart dokploy
# OR
docker restart <dokploy-container-id>
```

### Fix 3: Fix Docker Socket Permissions

**Ensure Docker socket is accessible:**

```bash
# SSH to VPS
ssh root@72.60.219.244

# Check Docker socket permissions
ls -la /var/run/docker.sock

# Should show: srw-rw---- 1 root docker

# Fix permissions if needed
chmod 666 /var/run/docker.sock

# Or better, add user to docker group (Fix 2)
```

### Fix 4: Fix "Too Many Open Files" Issue

**Increase inotify limits:**

```bash
# SSH to VPS
ssh root@72.60.219.244

# Check current limits
cat /proc/sys/fs/inotify/max_user_watches
cat /proc/sys/fs/inotify/max_user_instances

# Increase limits (temporary)
echo 524288 | sudo tee /proc/sys/fs/inotify/max_user_watches
echo 512 | sudo tee /proc/sys/fs/inotify/max_user_instances

# Make permanent (add to /etc/sysctl.conf)
echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf
echo "fs.inotify.max_user_instances=512" | sudo tee -a /etc/sysctl.conf

# Apply changes
sudo sysctl -p
```

---

## 🎯 Recommended Action Plan

### Immediate Steps:

1. **SSH to VPS:**
   ```bash
   ssh root@72.60.219.244
   ```

2. **Run Diagnostic Commands:**
   ```bash
   # Check Docker
   docker --version
   systemctl status docker

   # Check Docker socket
   ls -la /var/run/docker.sock

   # Check Dokploy process
   ps aux | grep dokploy

   # Check if Dokploy can access Docker
   docker ps
   ```

3. **Apply Fixes Based on Results:**

   **If Docker is not running:**
   ```bash
   systemctl start docker
   systemctl enable docker
   ```

   **If permission denied:**
   ```bash
   # Find Dokploy user
   DOKPLOY_USER=$(ps aux | grep dokploy | grep -v grep | awk '{print $1}' | head -1)

   # Add to docker group
   usermod -aG docker $DOKPLOY_USER

   # Restart Dokploy
   systemctl restart dokploy
   ```

   **If inotify issues:**
   ```bash
   echo 524288 | sudo tee /proc/sys/fs/inotify/max_user_watches
   echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf
   sudo sysctl -p
   ```

4. **Retry Deployment in Dokploy**

---

## 🔄 Alternative: Use Pre-built Docker Images

**While we fix Dokploy's Docker access, use the manual build approach:**

### Local Build and Push (Your Machine)

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/client-portal

# Ensure .env.production has BASE_PATH=/portal (already done)

# Build with environment from .env.production
docker build \
  --build-arg NODE_ENV=production \
  --build-arg BASE_PATH=/portal \
  -t ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.2.15 \
  -f Dockerfile .

# Login to GHCR (use your GitHub PAT)
echo $GITHUB_TOKEN | docker login ghcr.io -u <your-github-username> --password-stdin

# Push to registry
docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.2.15
```

### Update Dokploy to Use New Image

1. In Dokploy, switch back to "Docker Image" mode
2. Set image: `ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.2.15`
3. Redeploy

---

## 📋 Verification Checklist

After applying fixes:

### On VPS:
- [ ] `docker --version` returns version
- [ ] `systemctl status docker` shows active (running)
- [ ] `/var/run/docker.sock` is accessible
- [ ] `docker ps` works without errors
- [ ] Inotify limits increased

### In Dokploy:
- [ ] GitHub deployment works without "spawn docker ENOENT"
- [ ] Build completes successfully
- [ ] Service starts and shows healthy

### Client Portal:
- [ ] `curl -I https://stg.bizoholic.com/portal` returns 200 OK
- [ ] Browser loads https://stg.bizoholic.com/portal
- [ ] No 502 errors

---

## 🔍 Additional Diagnostics

### Check Dokploy Configuration

**If Dokploy runs in Docker itself:**

```bash
# SSH to VPS
ssh root@72.60.219.244

# Find Dokploy container
docker ps | grep dokploy

# Check if Docker socket is mounted
docker inspect <dokploy-container-id> | grep -A 10 Mounts

# Should show:
# /var/run/docker.sock:/var/run/docker.sock
```

**If Docker socket not mounted:**

Dokploy container needs Docker socket access. Check Dokploy installation documentation for proper setup.

### Check Docker Buildx

```bash
# SSH to VPS
ssh root@72.60.219.244

# Check if Docker Buildx is available
docker buildx version

# If not installed
docker buildx install
```

---

## 💡 Common Causes and Solutions

| Symptom | Cause | Solution |
|---------|-------|----------|
| spawn docker ENOENT | Docker not in PATH | Add Docker to PATH or use absolute path |
| Permission denied | User not in docker group | `usermod -aG docker <user>` |
| Cannot connect to Docker daemon | Docker service not running | `systemctl start docker` |
| Too many open files | Low inotify limits | Increase fs.inotify.max_user_watches |
| Docker socket not found | Socket permissions wrong | `chmod 666 /var/run/docker.sock` |

---

## 🚀 Quick Fix Script

**Run this on VPS to fix all common issues:**

```bash
#!/bin/bash
# fix-dokploy-docker.sh

echo "Fixing Docker access for Dokploy..."

# Start Docker if not running
systemctl start docker
systemctl enable docker

# Find Dokploy user
DOKPLOY_USER=$(ps aux | grep dokploy | grep -v grep | awk '{print $1}' | head -1)
echo "Dokploy user: $DOKPLOY_USER"

# Add to docker group
if [ ! -z "$DOKPLOY_USER" ]; then
    usermod -aG docker $DOKPLOY_USER
    echo "Added $DOKPLOY_USER to docker group"
fi

# Fix inotify limits
echo 524288 > /proc/sys/fs/inotify/max_user_watches
echo "fs.inotify.max_user_watches=524288" >> /etc/sysctl.conf
sysctl -p

# Restart Dokploy
if systemctl list-units | grep -q dokploy; then
    systemctl restart dokploy
    echo "Restarted Dokploy service"
else
    DOKPLOY_CONTAINER=$(docker ps | grep dokploy | awk '{print $1}')
    if [ ! -z "$DOKPLOY_CONTAINER" ]; then
        docker restart $DOKPLOY_CONTAINER
        echo "Restarted Dokploy container"
    fi
fi

echo "Done! Try deploying again in 30 seconds."
```

Save and run:
```bash
chmod +x fix-dokploy-docker.sh
./fix-dokploy-docker.sh
```

---

**Status:** 🔧 Awaiting VPS Docker Fix
**Priority:** 🔴 HIGH
**Next:** Fix Docker access, then retry GitHub deployment
