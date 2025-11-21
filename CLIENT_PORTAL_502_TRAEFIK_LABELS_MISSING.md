# Client Portal 502 Error - Missing Traefik Labels

**Date:** November 18, 2025
**Status:** 🔴 **ROOT CAUSE IDENTIFIED**

---

## 🔍 Diagnosis Complete

### Container Status: ✅ HEALTHY
- **Image:** `v2.2.16` deployed successfully
- **App Status:** Running correctly
- **Port:** 3003 listening on 0.0.0.0
- **Logs:** "Ready in 197ms" - no errors
- **BASE_PATH:** Correctly built with `/portal`

### Traefik Routing: ❌ NOT CONFIGURED
- **Docker Swarm Service:** `frontend-client-portal`
- **Service Labels:** `{}` (EMPTY!)
- **Problem:** Traefik has NO routing configuration

---

## 🚨 Root Cause

The Docker Swarm service `frontend-client-portal` has **ZERO Traefik labels** configured.

**Current State:**
```bash
$ docker service inspect frontend-client-portal --format "{{json .Spec.Labels}}"
{}  # ← EMPTY! No Traefik configuration!
```

**What's Happening:**
1. ✅ Container runs correctly on port 3003
2. ✅ Port 3003 is published (`*:3003->3003/tcp`)
3. ❌ Traefik has NO labels telling it how to route to this service
4. ❌ When request comes to `stg.bizoholic.com/portal`, Traefik doesn't know where to send it
5. ❌ Traefik returns 502 Bad Gateway

---

## ✅ Solution: Configure Traefik Labels in Dokploy

### Required Labels

The service needs these Traefik labels:

```yaml
# Enable Traefik
traefik.enable: "true"

# Router configuration
traefik.http.routers.client-portal.rule: "Host(`stg.bizoholic.com`) && PathPrefix(`/portal`)"
traefik.http.routers.client-portal.entrypoints: "websecure"
traefik.http.routers.client-portal.tls: "true"
traefik.http.routers.client-portal.tls.certresolver: "letsencrypt"
traefik.http.routers.client-portal.service: "client-portal"

# Service configuration
traefik.http.services.client-portal.loadbalancer.server.port: "3003"

# Optional: Strip prefix if needed (probably NOT needed since BASE_PATH=/portal)
# traefik.http.middlewares.client-portal-strip.stripprefix.prefixes: "/portal"
# traefik.http.routers.client-portal.middlewares: "client-portal-strip"

# Docker Swarm specific
traefik.docker.network: "dokploy-network"  # or whatever network Traefik is on
```

---

## 🔧 How to Fix in Dokploy

### Step 1: Access Dokploy Dashboard
```
URL: https://dk4.bizoholic.com/dashboard
```

### Step 2: Navigate to Client Portal Service
1. Find **client-portal** service
2. Click to open service configuration

### Step 3: Add Traefik Labels

In Dokploy, look for the **"Labels"** or **"Traefik"** configuration section.

Add these labels:

#### Basic Configuration:
```
traefik.enable=true
traefik.http.routers.client-portal.rule=Host(`stg.bizoholic.com`) && PathPrefix(`/portal`)
traefik.http.routers.client-portal.entrypoints=websecure
traefik.http.routers.client-portal.tls=true
traefik.http.services.client-portal.loadbalancer.server.port=3003
traefik.docker.network=dokploy-network
```

#### If Dokploy has a "Domain" field:
- **Domain:** `stg.bizoholic.com`
- **Path:** `/portal`
- **Port:** `3003`
- **HTTPS:** Enabled
- **Certificate Resolver:** `letsencrypt` (or default)

### Step 4: Redeploy
1. Click **"Save"** or **"Update"**
2. Click **"Redeploy"**
3. Wait for service to restart (~30 seconds)

### Step 5: Verify
```bash
curl -I https://stg.bizoholic.com/portal
# Expected: HTTP/2 200 ✅
```

---

## 📊 Verification Commands

### Before Fix:
```bash
# Check labels (should be empty)
docker service inspect frontend-client-portal --format "{{json .Spec.Labels}}"
# Output: {}

# Test endpoint (will fail)
curl -I https://stg.bizoholic.com/portal
# Output: HTTP/2 502
```

### After Fix:
```bash
# Check labels (should have Traefik config)
docker service inspect frontend-client-portal --format "{{json .Spec.Labels}}"
# Output: {"traefik.enable":"true", "traefik.http.routers..."}

# Test endpoint (should work)
curl -I https://stg.bizoholic.com/portal
# Output: HTTP/2 200
```

---

## 🎯 Why This Happened

### Dokploy Configuration Issue

When deploying to Docker Swarm through Dokploy, Traefik labels are NOT automatically added from the Docker image.

**Common Scenarios:**

1. **Docker Image Deployment:**
   - User deploys pre-built image
   - Dokploy creates Docker Swarm service
   - ❌ Traefik labels NOT added automatically
   - **Fix:** Manually configure in Dokploy UI

2. **GitHub Deployment (Dockerfile):**
   - Dokploy builds from Dockerfile
   - Dokploy creates Docker Swarm service
   - ❌ Dockerfile labels NOT transferred to service
   - **Fix:** Configure labels in Dokploy's deployment settings

3. **Docker Compose Deployment:**
   - User provides docker-compose.yml with labels
   - ✅ Labels transferred to service
   - **But:** We used Docker Image deployment, not Compose

---

## 🔍 Complete Diagnostic Log

### 1. Container Health Check
```bash
$ docker ps | grep client-portal
aad08d13921b   ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.2.16
Status: Up 3 minutes
Port: 3003/tcp
✅ HEALTHY
```

### 2. Container Logs
```bash
$ docker logs aad08d13921b
▲ Next.js 15.5.3
   - Local:        http://localhost:3003
   - Network:      http://0.0.0.0:3003
 ✓ Starting...
 ✓ Ready in 197ms
✅ NO ERRORS
```

### 3. Port Listening
```bash
$ docker exec aad08d13921b netstat -tuln
Proto Local Address           State
tcp   0.0.0.0:3003            LISTEN
✅ PORT 3003 LISTENING
```

### 4. Environment Variables
```bash
$ docker exec aad08d13921b env | grep -E "(PORT|BASE_PATH|HOSTNAME)"
HOSTNAME=0.0.0.0
BASE_PATH=/portal
PORT=3003
✅ CORRECT CONFIGURATION
```

### 5. Docker Swarm Service
```bash
$ docker service ls | grep client-portal
frontend-client-portal   1/1   *:3003->3003/tcp
✅ SERVICE RUNNING, PORT PUBLISHED
```

### 6. Service Labels
```bash
$ docker service inspect frontend-client-portal --format "{{json .Spec.Labels}}"
{}
❌ NO TRAEFIK LABELS!
```

### 7. External Access Test
```bash
$ curl -I https://stg.bizoholic.com/portal
HTTP/2 502
❌ TRAEFIK CAN'T ROUTE (no labels)
```

---

## 📋 Summary

| Component | Status | Details |
|-----------|--------|---------|
| Docker Image | ✅ Correct | v2.2.16 with BASE_PATH=/portal |
| Container | ✅ Running | No errors, listening on port 3003 |
| Application | ✅ Healthy | Next.js 15.5.3 ready |
| Port Mapping | ✅ Published | *:3003->3003/tcp |
| Environment | ✅ Correct | BASE_PATH=/portal, PORT=3003 |
| **Traefik Labels** | ❌ **MISSING** | Service has {} labels |
| External Access | ❌ 502 Error | Traefik can't route |

**Conclusion:** The application is PERFECT. The Docker configuration is MISSING Traefik labels.

---

## 🚀 Next Steps

### Immediate Action Required:

1. **Configure Traefik labels in Dokploy UI**
   - Add routing rules
   - Set port to 3003
   - Enable HTTPS
   - Set domain and path

2. **Redeploy the service**
   - Click redeploy in Dokploy
   - Wait for service restart

3. **Verify fix**
   ```bash
   curl -I https://stg.bizoholic.com/portal
   # Expected: HTTP/2 200
   ```

### Alternative: Use Docker Compose

If Dokploy supports it, create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  client-portal:
    image: ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.2.16
    environment:
      - PORT=3003
      - BASE_PATH=/portal
      - NODE_ENV=production
      - NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com/api
      - JWT_SECRET=n62SLTZfZjKABOw04EjBWvjp6635XifgQP1+XRkfbac=
      - NEXTAUTH_SECRET=BQ8cXrPJhPp4MD/OT9GYNTE3DHpZjiIJM4kbPGXkcpY=
      - NEXTAUTH_URL=https://stg.bizoholic.com/portal
    networks:
      - dokploy-network
    deploy:
      mode: replicated
      replicas: 1
      labels:
        - "traefik.enable=true"
        - "traefik.http.routers.client-portal.rule=Host(`stg.bizoholic.com`) && PathPrefix(`/portal`)"
        - "traefik.http.routers.client-portal.entrypoints=websecure"
        - "traefik.http.routers.client-portal.tls=true"
        - "traefik.http.routers.client-portal.tls.certresolver=letsencrypt"
        - "traefik.http.services.client-portal.loadbalancer.server.port=3003"
        - "traefik.docker.network=dokploy-network"

networks:
  dokploy-network:
    external: true
```

Then deploy this compose file through Dokploy.

---

## 📞 Support

**If labels are still not working after adding in Dokploy:**

1. **Check Dokploy's Traefik integration:**
   - Is Traefik enabled for this project?
   - Is the network correct (`dokploy-network`)?
   - Are other services working with Traefik?

2. **Check Traefik logs:**
   ```bash
   docker service logs dokploy-traefik
   # Look for routing configuration
   ```

3. **Verify network:**
   ```bash
   docker service inspect frontend-client-portal | grep -A 5 Networks
   # Should include dokploy-network
   ```

---

**Status:** 🔴 **WAITING FOR TRAEFIK LABELS CONFIGURATION IN DOKPLOY**
**Priority:** 🔴 **CRITICAL**
**Action Required:** Configure Traefik labels in Dokploy UI for client-portal service
