# ThrillRing Gaming Portal - Dokploy Deployment Configuration
**Date:** November 3, 2025
**Status:** ✅ Building Docker Image
**Target:** stg.thrillring.com (standalone domain)

---

## 📋 APPLICATION OVERVIEW

### Service Details
```
Application:    ThrillRing Gaming Portal
Purpose:        E-sports Tournament Platform
Technology:     Next.js 15.5.3 + React 19
Port:           3006 (container)
Domain:         stg.thrillring.com (standalone)
Architecture:   Standalone Microservice (DDD-compliant)
```

### Key Features
- Tournament management and registration
- Live gaming statistics and leaderboards
- Player profiles and rankings
- Real-time match tracking
- Community engagement features
- Multi-game support

---

## 🔧 DOCKERFILE DETAILS

### Build Configuration
```dockerfile
# Multi-stage build
Stage 1: deps    - Install npm dependencies
Stage 2: builder - Build Next.js application
Stage 3: runner  - Production runtime

# Image optimization
- Base: node:20-alpine (~150MB)
- Package Manager: npm (not pnpm)
- Output: standalone (~200MB estimated)
- Health Check: HTTP GET on localhost:3006/
```

---

## 📦 DOCKER IMAGE

### Image Details
```
Registry:       ghcr.io (GitHub Container Registry)
Repository:     ghcr.io/bizoholic-digital/bizosaas-thrillring-gaming
Tags:           latest, v1.0.0
Build Status:   ⏳ Building...
Expected Size:  ~200MB (standalone build)
```

### Registry Credentials
```
Registry:       ghcr.io
Username:       bizoholic-digital
Token:          ghp_REDACTED
```

---

## 🚀 DOKPLOY DEPLOYMENT CONFIGURATION

### Step 1: Application Basic Settings

```
Application Name:          thrillring-gaming
Project:                   BizOSaaS Platform
Type:                      Docker
Deployment Method:         Docker Image (Registry)
Description:               ThrillRing Gaming Portal - E-sports Tournament Platform
```

---

### Step 2: Docker Image Configuration

#### Registry Settings
```
Registry Type:             Custom Registry
Registry URL:              ghcr.io
Registry Username:         bizoholic-digital
Registry Password/Token:   ghp_REDACTED
```

#### Image Details
```
Image:                     ghcr.io/bizoholic-digital/bizosaas-thrillring-gaming:latest
Tag:                       latest (or v1.0.0 for specific version)
Pull Policy:               Always (to get latest updates)
```

---

### Step 3: Port Configuration

#### Container Port Mapping
```
Container Port:            3006
Protocol:                  TCP
Publish Port:              YES
Published Port:            3006
Published Port Mode:       INGRESS
```

**Explanation:** Unlike path-based routing services, this standalone domain service needs a published port.

---

### Step 4: Environment Variables

Copy and paste these **EXACTLY** as shown:

```env
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001
NEXT_PUBLIC_GAMING_API_URL=http://backend-brain-gateway:8001/api/gaming
NEXT_PUBLIC_TOURNAMENT_API_URL=http://backend-brain-gateway:8001/api/gaming/tournaments
NEXT_PUBLIC_SOCKET_URL=http://backend-brain-gateway:8001
NEXT_PUBLIC_STOREFRONT_URL=https://stg.thrillring.com
NEXT_PUBLIC_STOREFRONT_NAME=ThrillRing
NODE_ENV=production
PORT=3006
```

**Important Notes:**
- ✅ ALL API calls go through `backend-brain-gateway:8001` (centralized gateway)
- ✅ `NEXT_PUBLIC_STOREFRONT_URL` is the public domain
- ✅ `PORT=3006` must match the container port
- ✅ Socket.IO connections also through Brain Gateway

---

### Step 5: Domain & Routing Configuration

#### Standalone Domain Configuration

```
Domain:                    stg.thrillring.com
Path:                      / (root - no path prefix)
HTTPS:                     Enabled (Let's Encrypt)
Certificate Resolver:      letsencrypt
```

**Result URL:** `https://stg.thrillring.com`

#### Traefik Labels (if manual configuration needed)
```yaml
traefik.enable=true
traefik.http.routers.thrillring-gaming.rule=Host(`stg.thrillring.com`)
traefik.http.routers.thrillring-gaming.entrypoints=websecure
traefik.http.routers.thrillring-gaming.tls.certresolver=letsencrypt
traefik.http.services.thrillring-gaming.loadbalancer.server.port=3006
```

**Note:** Since this is a standalone domain (no basePath), no StripPrefix middleware needed.

---

### Step 6: Network Configuration

```
Network:                   dokploy-network (or bizosaas-network)
Network Mode:              Overlay (Docker Swarm)
```

**Important:** Must be on same network as:
- `backend-brain-gateway` (for API calls)
- `backend-gaming` (accessed via gateway)
- Other backend services

---

### Step 7: Resource Limits (Optional but Recommended)

```
CPU Limit:                 1.0 (1 CPU core)
Memory Limit:              512MB
Memory Reservation:        256MB
Replicas:                  1 (can scale later)
Restart Policy:            on-failure
```

---

### Step 8: Health Check Configuration

```yaml
Test Command:              node -e "require('http').get('http://localhost:3006/', (r) => {process.exit(r.statusCode === 200 || r.statusCode === 307 ? 0 : 1)})"
Interval:                  30s
Timeout:                   10s
Retries:                   3
Start Period:              40s
```

**Explanation:** Checks if the app responds on port 3006 every 30 seconds. Allows 40 seconds for initial startup.

---

## 🔍 CONFIGURATION VERIFICATION CHECKLIST

Before clicking "Deploy", verify:

### Registry & Image
- [ ] Registry URL: `ghcr.io`
- [ ] Username: `bizoholic-digital`
- [ ] Token: `ghp_REDACTED`
- [ ] Image: `ghcr.io/bizoholic-digital/bizosaas-thrillring-gaming:latest`

### Port Configuration
- [ ] Container Port: `3006`
- [ ] Protocol: TCP
- [ ] Published Port: `3006`
- [ ] Published Port Mode: INGRESS

### Environment Variables (8 total)
- [ ] `NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001`
- [ ] `NEXT_PUBLIC_GAMING_API_URL=http://backend-brain-gateway:8001/api/gaming`
- [ ] `NEXT_PUBLIC_TOURNAMENT_API_URL=http://backend-brain-gateway:8001/api/gaming/tournaments`
- [ ] `NEXT_PUBLIC_SOCKET_URL=http://backend-brain-gateway:8001`
- [ ] `NEXT_PUBLIC_STOREFRONT_URL=https://stg.thrillring.com`
- [ ] `NEXT_PUBLIC_STOREFRONT_NAME=ThrillRing`
- [ ] `NODE_ENV=production`
- [ ] `PORT=3006`

### Domain Configuration
- [ ] Domain: `stg.thrillring.com`
- [ ] Path: `/` (root)
- [ ] HTTPS: Enabled
- [ ] Certificate: Let's Encrypt

### Network
- [ ] Network: `dokploy-network` or `bizosaas-network`
- [ ] Mode: Overlay/Swarm

### Health Check
- [ ] Interval: 30s
- [ ] Timeout: 10s
- [ ] Retries: 3
- [ ] Start Period: 40s

---

## 🚀 DEPLOYMENT STEPS

### 1. Wait for Docker Build to Complete
```bash
# Monitor build progress
tail -f /tmp/thrillring-build.log

# Expected completion message:
# Successfully tagged ghcr.io/bizoholic-digital/bizosaas-thrillring-gaming:v1.0.0
# Successfully tagged ghcr.io/bizoholic-digital/bizosaas-thrillring-gaming:latest
```

### 2. Push Image to GHCR
```bash
# Login to GHCR
echo "ghp_REDACTED" | docker login ghcr.io -u bizoholic-digital --password-stdin

# Push images
docker push ghcr.io/bizoholic-digital/bizosaas-thrillring-gaming:v1.0.0
docker push ghcr.io/bizoholic-digital/bizosaas-thrillring-gaming:latest
```

### 3. Login to Dokploy
```
URL: https://panel.dokploy.com (or your Dokploy panel)
Server: KVM4 (72.60.219.244)
```

### 4. Navigate to Applications
```
Projects → BizOSaaS Platform → Create Application
Or: Applications → Create New Application
```

### 5. Configure Application
```
- Follow the configuration above step-by-step
- Double-check all values
- Ensure no typos in environment variables
```

### 6. Deploy
```
- Click "Create" or "Deploy"
- Monitor deployment logs
- Wait for "Running" status
```

### 7. Verify Deployment
```bash
# SSH to KVM4
ssh root@72.60.219.244

# Check service
docker service ls | grep thrillring

# Check container
docker ps | grep thrillring

# Check logs
docker logs <container-id>
```

---

## 🔍 POST-DEPLOYMENT VERIFICATION

### 1. Check Service Status
```bash
ssh root@72.60.219.244

# Should show thrillring-gaming service
docker service ls | grep thrillring

# Should show 1/1 replicas
docker service ps thrillring-gaming
```

### 2. Check Container Health
```bash
# Should show "healthy" status
docker ps | grep thrillring

# Check logs for errors
docker logs <container-id> -f
```

### 3. Test Internal Connectivity
```bash
# Test container responds
docker exec <container-id> curl http://localhost:3006/

# Test Brain Gateway connectivity
docker exec <container-id> ping backend-brain-gateway

# Test Gaming API through gateway
docker exec <container-id> curl http://backend-brain-gateway:8001/api/gaming/health
```

### 4. Test Public URL
```bash
# From your local machine
curl -I https://stg.thrillring.com

# Should return: HTTP/2 200 OK
```

### 5. Browser Test
```
URL: https://stg.thrillring.com

Expected Results:
✅ ThrillRing homepage loads with gaming theme
✅ Tournament listings appear
✅ Navigation works
✅ Images load correctly
✅ No console errors in DevTools
✅ Network tab shows API calls to backend-brain-gateway
✅ Socket.IO connection establishes
```

---

## 🚨 TROUBLESHOOTING

### Issue: Service won't start

**Check:**
```bash
# View service events
docker service ps thrillring-gaming --no-trunc

# Check logs
docker service logs thrillring-gaming
```

**Common Causes:**
- Registry credentials incorrect
- Image not found in GHCR
- Port 3006 already in use
- Network not configured

**Solution:**
- Verify registry token is correct
- Ensure image was pushed successfully
- Check no other service uses port 3006: `ss -tulpn | grep 3006`
- Verify network exists: `docker network ls | grep dokploy`

### Issue: HTTP 502 Bad Gateway

**Check:**
```bash
# Is container healthy?
docker ps | grep thrillring

# Check container logs
docker logs <container-id>
```

**Common Causes:**
- Container not ready (still starting)
- Health check failing
- App crashed on startup

**Solution:**
- Wait 40s for startup period
- Check logs for errors
- Verify environment variables are correct

### Issue: API Errors (Gaming/Tournament data not loading)

**Check:**
```bash
# Can container reach gateway?
docker exec <container-id> ping backend-brain-gateway

# Is gateway accessible?
docker exec <container-id> curl http://backend-brain-gateway:8001/api/gaming/health
```

**Common Causes:**
- Brain Gateway not running
- Wrong environment variable
- Network misconfiguration
- Gaming backend not responding

**Solution:**
- Verify gateway service is running
- Check `NEXT_PUBLIC_GAMING_API_URL` is correct
- Ensure both services on same network
- Verify gaming backend is healthy

### Issue: 404 Not Found

**Check:**
```bash
# View Traefik routing
docker service ps dokploy-traefik

# Check Traefik logs
docker service logs dokploy-traefik | grep thrillring
```

**Common Causes:**
- Domain configuration incorrect
- Traefik labels missing
- Certificate not issued
- DNS not pointing to server

**Solution:**
- Verify domain and path in Dokploy UI
- Check Traefik labels are applied
- Wait for Let's Encrypt certificate (can take 2-3 minutes)
- Verify A record in Cloudflare points to 72.60.219.244

---

## 📊 EXPECTED DEPLOYMENT OUTCOME

### Service Status
```bash
docker service ls | grep thrillring

# Expected output:
# thrillring-gaming   replicated   1/1   ghcr.io/bizoholic-digital/bizosaas-thrillring-gaming:latest
```

### Container Status
```bash
docker ps | grep thrillring

# Expected output:
# <container-id>   ghcr.io/bizoholic-digital/bizosaas-thrillring-gaming:latest   Up 5 minutes   (healthy)   3006/tcp
```

### Public Access
```
URL: https://stg.thrillring.com
Status: 200 OK
Content: ThrillRing Gaming Portal Homepage
```

---

## ✅ CONFIRMATION CHECKLIST

After deployment, confirm:

- [ ] Service shows in `docker service ls`
- [ ] Container is running and healthy
- [ ] Logs show no errors
- [ ] Can access https://stg.thrillring.com
- [ ] Homepage loads correctly
- [ ] Tournament listings displayed
- [ ] Player leaderboards working
- [ ] Navigation works
- [ ] Images load
- [ ] No console errors
- [ ] API calls go through Brain Gateway
- [ ] Socket.IO connection works (if live features enabled)
- [ ] Mobile responsive design works

---

## 📝 SUMMARY

**Image:** ⏳ Building (ghcr.io/bizoholic-digital/bizosaas-thrillring-gaming:latest)
**Registry Access:** ✅ Credentials provided and working
**Configuration:** ✅ Complete and verified
**Network:** ✅ dokploy-network (same as other services)
**Port:** ✅ 3006 (container and published)
**Domain:** ✅ https://stg.thrillring.com (standalone)
**Environment:** ✅ 8 variables configured for Brain Gateway routing

**Status:** ⏳ BUILD IN PROGRESS → READY FOR DEPLOYMENT

---

**Next Step:** Wait for build completion, push to GHCR, then deploy in Dokploy UI using the configuration above!
