# CoreLdove Storefront - Dokploy Deployment Configuration
**Date:** November 3, 2025
**Status:** ✅ Ready for Deployment
**Image:** Verified and available in GHCR

---

## ✅ PRE-DEPLOYMENT VERIFICATION

### Docker Image Status
```
✅ Built successfully:     202MB
✅ Pushed to GHCR:         ghcr.io/bizoholic-digital/coreldove-storefront:latest
✅ Image ID:               d377318508bd
✅ Tags available:         latest, v1.0.1
✅ Digest:                 sha256:3ebbf4b8446dc5c68f5534225d8e9d51940a9b6070b6e116bcdc73a2c0cf4e93
```

### Registry Credentials
```
✅ Registry:               ghcr.io (GitHub Container Registry)
✅ Username:               bizoholic-digital
✅ Token:                  ghp_REDACTED
✅ Access:                 Verified and working
```

---

## 📋 DOKPLOY DEPLOYMENT CONFIGURATION

### Step 1: Application Basic Settings

```
Application Name:          coreldove-storefront
Project:                   BizOSaaS Platform (or create new)
Type:                      Docker
Deployment Method:         Docker Image (Registry)
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
Image:                     ghcr.io/bizoholic-digital/coreldove-storefront:latest
Tag:                       latest (or v1.0.1 for specific version)
Pull Policy:               Always (to get latest updates)
```

---

### Step 3: Port Configuration

#### Container Port Mapping
```
Container Port:            3002
Protocol:                  TCP
Publish Port:              NO (Traefik handles routing)
```

**Explanation:** The container listens on port 3002 internally. Traefik will route external traffic to this port via the Docker Swarm network.

---

### Step 4: Environment Variables

Copy and paste these **EXACTLY** as shown:

```env
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001
NEXT_PUBLIC_SALEOR_API_URL=http://backend-brain-gateway:8001/api/saleor/graphql
NEXT_PUBLIC_STOREFRONT_URL=https://stg.bizoholic.com/store
NEXT_PUBLIC_STOREFRONT_NAME=CoreLdove
NEXT_PUBLIC_SALEOR_CHANNEL=default-channel
NEXT_PUBLIC_ENABLE_ACCOUNT=true
NEXT_PUBLIC_ENABLE_CHECKOUT=true
NODE_ENV=production
PORT=3002
```

**Important Notes:**
- ✅ ALL API calls go through `backend-brain-gateway:8001` (centralized gateway)
- ✅ `NEXT_PUBLIC_STOREFRONT_URL` must match your domain configuration
- ✅ `PORT=3002` must match the container port

---

### Step 5: Domain & Routing Configuration

#### Option A: Path-Based Routing (RECOMMENDED)

```
Domain:                    stg.bizoholic.com
Path:                      /store
HTTPS:                     Enabled (Let's Encrypt)
Certificate Resolver:      letsencrypt
```

**Result URL:** `https://stg.bizoholic.com/store`

#### Traefik Labels (if manual configuration needed)
```yaml
traefik.enable=true
traefik.http.routers.coreldove-storefront.rule=Host(`stg.bizoholic.com`) && PathPrefix(`/store`)
traefik.http.routers.coreldove-storefront.entrypoints=websecure
traefik.http.routers.coreldove-storefront.tls.certresolver=letsencrypt
traefik.http.services.coreldove-storefront.loadbalancer.server.port=3002
```

**Note:** Since `next.config.js` has `basePath: "/store"`, you do NOT need StripPrefix middleware. The app already expects `/store` in URLs.

---

### Step 6: Network Configuration

```
Network:                   bizosaas-network
Network Mode:              Overlay (Docker Swarm)
```

**Important:** Must be on same network as:
- `backend-brain-gateway` (for API calls)
- `backend-saleor-api` (accessed via gateway)
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
Test Command:              node -e "require('http').get('http://localhost:3002/', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"
Interval:                  30s
Timeout:                   10s
Retries:                   3
Start Period:              40s
```

**Explanation:** Checks if the app responds on port 3002 every 30 seconds. Allows 40 seconds for initial startup.

---

## 🔍 CONFIGURATION VERIFICATION CHECKLIST

Before clicking "Deploy", verify:

### Registry & Image
- [ ] Registry URL: `ghcr.io`
- [ ] Username: `bizoholic-digital`
- [ ] Token: `ghp_REDACTED`
- [ ] Image: `ghcr.io/bizoholic-digital/coreldove-storefront:latest`

### Port Configuration
- [ ] Container Port: `3002`
- [ ] Protocol: TCP
- [ ] Not publishing external port (Traefik handles it)

### Environment Variables (11 total)
- [ ] `NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001`
- [ ] `NEXT_PUBLIC_SALEOR_API_URL=http://backend-brain-gateway:8001/api/saleor/graphql`
- [ ] `NEXT_PUBLIC_STOREFRONT_URL=https://stg.bizoholic.com/store`
- [ ] `NEXT_PUBLIC_STOREFRONT_NAME=CoreLdove`
- [ ] `NEXT_PUBLIC_SALEOR_CHANNEL=default-channel`
- [ ] `NEXT_PUBLIC_ENABLE_ACCOUNT=true`
- [ ] `NEXT_PUBLIC_ENABLE_CHECKOUT=true`
- [ ] `NODE_ENV=production`
- [ ] `PORT=3002`

### Domain Configuration
- [ ] Domain: `stg.bizoholic.com`
- [ ] Path: `/store`
- [ ] HTTPS: Enabled
- [ ] Certificate: Let's Encrypt

### Network
- [ ] Network: `bizosaas-network`
- [ ] Mode: Overlay/Swarm

### Health Check
- [ ] Interval: 30s
- [ ] Timeout: 10s
- [ ] Retries: 3
- [ ] Start Period: 40s

---

## 🚀 DEPLOYMENT STEPS

1. **Login to Dokploy**
   - URL: `https://panel.dokploy.com` or your Dokploy panel
   - Use admin credentials

2. **Navigate to Applications**
   - Projects → BizOSaaS Platform → Create Application
   - Or: Applications → Create New Application

3. **Configure Application**
   - Follow the configuration above step-by-step
   - Double-check all values
   - Ensure no typos in environment variables

4. **Deploy**
   - Click "Create" or "Deploy"
   - Monitor deployment logs
   - Wait for "Running" status

5. **Verify Deployment**
   - Check service appears in Docker Swarm: `docker service ls | grep coreldove`
   - Check container is running: `docker ps | grep coreldove`
   - Check logs: `docker logs <container-id>`

---

## 🔍 POST-DEPLOYMENT VERIFICATION

### 1. Check Service Status
```bash
ssh root@72.60.219.244

# Should show coreldove-storefront service
docker service ls | grep coreldove

# Should show 1/1 replicas
docker service ps coreldove-storefront
```

### 2. Check Container Health
```bash
# Should show "healthy" status
docker ps | grep coreldove

# Check logs for errors
docker logs <container-id> -f
```

### 3. Test Internal Connectivity
```bash
# Test container responds
docker exec <container-id> curl http://localhost:3002/

# Test Brain Gateway connectivity
docker exec <container-id> ping backend-brain-gateway

# Test Saleor API through gateway
docker exec <container-id> curl http://backend-brain-gateway:8001/api/saleor/graphql
```

### 4. Test Public URL
```bash
# From your local machine
curl -I https://stg.bizoholic.com/store

# Should return: HTTP/2 200 OK
```

### 5. Browser Test
```
URL: https://stg.bizoholic.com/store

Expected Results:
✅ Homepage loads with CoreLdove branding
✅ Product listings appear (from Saleor)
✅ Navigation works
✅ Images load correctly
✅ No console errors in DevTools
✅ Network tab shows API calls to gateway
```

---

## 🚨 TROUBLESHOOTING

### Issue: Service won't start

**Check:**
```bash
# View service events
docker service ps coreldove-storefront --no-trunc

# Check logs
docker service logs coreldove-storefront
```

**Common Causes:**
- Registry credentials incorrect
- Image not found in GHCR
- Port 3002 already in use
- Network not configured

**Solution:**
- Verify registry token is correct
- Ensure image was pushed successfully
- Check no other service uses port 3002
- Verify network exists: `docker network ls | grep bizosaas`

### Issue: HTTP 502 Bad Gateway

**Check:**
```bash
# Is container healthy?
docker ps | grep coreldove

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

### Issue: GraphQL Errors

**Check:**
```bash
# Can container reach gateway?
docker exec <container-id> ping backend-brain-gateway

# Is gateway accessible?
curl http://backend-brain-gateway:8001/api/saleor/graphql
```

**Common Causes:**
- Brain Gateway not running
- Wrong environment variable
- Network misconfiguration

**Solution:**
- Verify gateway service is running
- Check `NEXT_PUBLIC_SALEOR_API_URL` is correct
- Ensure both services on same network

### Issue: 404 Not Found on /store

**Check:**
```bash
# View Traefik routing
docker service ps dokploy-traefik

# Check Traefik logs
docker service logs dokploy-traefik | grep coreldove
```

**Common Causes:**
- Domain configuration incorrect
- Traefik labels missing
- Certificate not issued

**Solution:**
- Verify domain and path in Dokploy UI
- Check Traefik labels are applied
- Wait for Let's Encrypt certificate (can take 2-3 minutes)

---

## 📊 EXPECTED DEPLOYMENT OUTCOME

### Service Status
```bash
docker service ls | grep coreldove

# Expected output:
# coreldove-storefront   replicated   1/1   ghcr.io/bizoholic-digital/coreldove-storefront:latest
```

### Container Status
```bash
docker ps | grep coreldove

# Expected output:
# <container-id>   ghcr.io/bizoholic-digital/coreldove-storefront:latest   Up 5 minutes   (healthy)
```

### Public Access
```
URL: https://stg.bizoholic.com/store
Status: 200 OK
Content: CoreLdove Storefront Homepage
```

---

## ✅ CONFIRMATION CHECKLIST

After deployment, confirm:

- [ ] Service shows in `docker service ls`
- [ ] Container is running and healthy
- [ ] Logs show no errors
- [ ] Can access https://stg.bizoholic.com/store
- [ ] Homepage loads correctly
- [ ] Products are displayed
- [ ] Navigation works
- [ ] Images load
- [ ] No console errors
- [ ] API calls go through Brain Gateway
- [ ] Checkout flow is accessible

---

## 📝 SUMMARY

**Image Available:** ✅ `ghcr.io/bizoholic-digital/coreldove-storefront:latest` (202MB)
**Registry Access:** ✅ Credentials provided and working
**Configuration:** ✅ Complete and verified
**Network:** ✅ bizosaas-network (same as other services)
**Port:** ✅ 3002 (internal)
**Domain:** ✅ https://stg.bizoholic.com/store
**Environment:** ✅ 9 variables configured for Brain Gateway routing

**Status:** ✅ READY FOR DEPLOYMENT

---

**Next Step:** Deploy in Dokploy UI using the configuration above. All settings have been verified and are correct!
