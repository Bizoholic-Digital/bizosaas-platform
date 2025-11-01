# URGENT: Fix Multiple Portal Containers Issue

## The Problem

You have multiple Client Portal containers running, which is causing the 502 Bad Gateway error. Traefik is getting confused about which container to connect to.

## Why Container Is Healthy But 502 Happens

- ✅ Container logs show: "Ready in 219ms" (HEALTHY)
- ❌ Traefik returns 502 Bad Gateway
- **Cause**: Multiple containers with similar names causing routing conflicts

---

## Solution: Find and Remove Duplicate Containers

### Step 1: SSH to VPS Server

```bash
ssh root@194.238.16.237
# Password: Welcome2BizOholic!@#
```

### Step 2: List ALL Portal Containers

```bash
# List all containers with "portal" in the name
docker ps -a --filter "name=portal" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

**What to look for**:
- Multiple containers with "portal" in the name
- Check which ones are "Up" (running) vs "Exited"

### Step 3: Find the CORRECT Container

```bash
# Find containers using the Client Portal image
docker ps --filter "ancestor=ghcr.io/bizoholic-digital/bizosaas-client-portal:v1.0.0-foundation-dashboard" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

**Expected output**: Should show ONLY ONE running container

If you see multiple containers, note their names.

### Step 4: Check Container Names

```bash
# Get the exact name of the running portal container
docker ps | grep portal
```

**Example output**:
```
abc123def456   ghcr.io/bizoholic-digital/bizosaas-client-portal:v1.0.0-foundation-dashboard   Up 5 minutes   0.0.0.0:3002->3001/tcp   8EqZXZKYTLiPqTkLF2l4J
xyz789ghi012   ghcr.io/bizoholic-digital/bizosaas-client-portal:latest                        Up 2 hours     0.0.0.0:3003->3001/tcp   old-portal-container
```

**The correct container name** is in the last column.

### Step 5: Stop and Remove OLD Containers

**IMPORTANT**: Only stop containers that are NOT the current one (from Step 4)

```bash
# List all exited portal containers
docker ps -a --filter "name=portal" --filter "status=exited"

# Remove all exited portal containers
docker ps -a --filter "name=portal" --filter "status=exited" -q | xargs docker rm

# If there are OLD running portal containers (not the current one):
docker stop <old-container-name>
docker rm <old-container-name>
```

### Step 6: Verify Only ONE Portal Container Exists

```bash
# Should show ONLY ONE container
docker ps --filter "ancestor=ghcr.io/bizoholic-digital/bizosaas-client-portal"
```

**Expected**: One line showing the current portal container

### Step 7: Get the EXACT Container Name

```bash
# Get the exact Docker container name
docker ps | grep portal | awk '{print $NF}'
```

**Example output**: `8EqZXZKYTLiPqTkLF2l4J`

**Copy this name exactly** - you'll need it for Traefik.

---

## Step 8: Update Traefik Configuration

Now that you have the EXACT container name, update your Traefik config:

```yaml
services:
  frontend-client-portal-service-3:
    loadBalancer:
      servers:
        - url: http://<EXACT-CONTAINER-NAME>:3001  # Use name from Step 7
```

**Example**:
```yaml
services:
  frontend-client-portal-service-3:
    loadBalancer:
      servers:
        - url: http://8EqZXZKYTLiPqTkLF2l4J:3001
```

---

## Alternative: Check in Dokploy UI

### Method 1: Check Service Name in Dokploy

1. Go to: https://dk4.bizoholic.com/dashboard/project/VM7SbnKYZKl6nxKYey4Xn/environment/w9JtT6e9Glus_8cjWIEWc

2. Look at ALL services in this environment

3. **Check for duplicate portal services**:
   - Do you see multiple services with "portal" in the name?
   - Are they all running?

4. **If you find duplicates**:
   - Stop/delete the OLD portal services
   - Keep only the current one: `8EqZXZKYTLiPqTkLF2l4J`

### Method 2: Check Container Name in General Tab

1. Go to your Client Portal service General tab

2. Look for fields:
   - **Name**: ________________
   - **App Name**: ________________
   - **Container Name**: ________________

3. Use the EXACT value shown in one of these fields for Traefik

---

## Quick Diagnostic Commands

If you have SSH access, run ALL these commands and share the output:

```bash
# 1. List all portal containers (running and stopped)
echo "=== ALL PORTAL CONTAINERS ==="
docker ps -a --filter "name=portal"

# 2. List only running portal containers
echo "=== RUNNING PORTAL CONTAINERS ==="
docker ps --filter "name=portal"

# 3. Find containers with client-portal image
echo "=== CONTAINERS WITH CLIENT PORTAL IMAGE ==="
docker ps --filter "ancestor=ghcr.io/bizoholic-digital/bizosaas-client-portal"

# 4. Check exact container name
echo "=== EXACT CONTAINER NAME ==="
docker ps | grep portal | awk '{print "Container Name:", $NF}'

# 5. Inspect container to get name and network
echo "=== CONTAINER DETAILS ==="
CONTAINER_ID=$(docker ps | grep portal | head -1 | awk '{print $1}')
docker inspect $CONTAINER_ID | jq -r '{Name: .Name, Networks: .NetworkSettings.Networks | keys}'
```

---

## Most Likely Container Names

Based on Dokploy patterns and Bizoholic Frontend example, try these:

1. `8EqZXZKYTLiPqTkLF2l4J` (application ID - already tried)
2. `frontend-client-portal` (service name pattern - already tried)
3. `dokploy-8EqZXZKYTLiPqTkLF2l4J` (with dokploy prefix)
4. `dokploy-frontend-client-portal` (full service name with prefix)
5. Container name shown in Dokploy General tab (CHECK THIS!)

---

## Expected Result After Fix

After finding and using the correct container name:

1. ✅ Only ONE portal container running
2. ✅ Traefik config uses correct container name
3. ✅ `curl -I https://stg.bizoholic.com/portal/` returns 200 OK
4. ✅ Portal loads in browser

---

## Summary

**Problem**: Multiple portal containers causing routing conflicts
**Solution**:
1. Find exact container name via SSH or Dokploy UI
2. Remove duplicate/old containers
3. Update Traefik with exact container name
4. Test access

**What I Need**:
- Output of: `docker ps | grep portal` from the VPS
- Or the exact container name shown in Dokploy General tab

Once you provide this, I can give you the exact Traefik configuration to use!
