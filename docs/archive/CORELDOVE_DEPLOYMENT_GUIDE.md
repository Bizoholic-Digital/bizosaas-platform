# CoreLdove Storefront - Deployment Guide
**Date:** November 3, 2025
**Status:** ✅ Built and Ready for Deployment
**Image:** `ghcr.io/bizoholic-digital/coreldove-storefront:latest`

---

## 🎉 BUILD SUCCESS

### Docker Image Details
```
Repository: ghcr.io/bizoholic-digital/coreldove-storefront
Tags:       latest, v1.0.1
Size:       202MB (optimized standalone build)
Digest:     sha256:3ebbf4b8446dc5c68f5534225d8e9d51940a9b6070b6e116bcdc73a2c0cf4e93
Created:    2025-11-03 09:14:11 IST
Status:     ✅ Pushed to GHCR
```

### Build Highlights
- ✅ **GraphQL Codegen:** Generated successfully using Saleor demo API
- ✅ **Next.js Build:** 40 static pages generated
- ✅ **First Load JS:** 102 kB (optimized)
- ✅ **Linting:** Passed with 5 warnings (no errors)
- ✅ **Multi-stage Build:** deps → builder → runner
- ✅ **Standalone Output:** Minimal production bundle

---

## 📋 DEPLOYMENT TO KVM4

### Server Details
```
Server:     72.60.219.244 (KVM4)
Platform:   Dokploy
Network:    Docker Swarm overlay
Domain:     stg.bizoholic.com
Path:       /store
```

### Deployment Steps

#### 1. Access Dokploy UI
```
URL: https://panel.dokploy.com (or KVM4 Dokploy panel)
Login with admin credentials
```

#### 2. Create New Application

Navigate to: **Applications → Create Application**

**Basic Settings:**
```
Name:           coreldove-storefront
Project:        BizOSaaS Platform
Description:    CoreLdove E-commerce Storefront (Saleor-based)
```

**Docker Configuration:**
```
Image:          ghcr.io/bizoholic-digital/coreldove-storefront:latest
Port:           3002
Replicas:       1 (can scale later)
Network:        bizosaas-network (same as other services)
```

#### 3. Environment Variables

Configure these environment variables in Dokploy:

```env
# API Gateway (Brain Gateway)
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001
NEXT_PUBLIC_SALEOR_API_URL=http://backend-brain-gateway:8001/api/saleor/graphql

# Storefront Configuration
NEXT_PUBLIC_STOREFRONT_URL=https://stg.bizoholic.com/store
NEXT_PUBLIC_STOREFRONT_NAME=CoreLdove
NEXT_PUBLIC_SALEOR_CHANNEL=default-channel

# Feature Flags
NEXT_PUBLIC_ENABLE_ACCOUNT=true
NEXT_PUBLIC_ENABLE_CHECKOUT=true

# Node Environment
NODE_ENV=production
PORT=3002
```

#### 4. Traefik Configuration (Path Routing)

**Add Traefik Labels:**
```yaml
traefik.enable=true
traefik.http.routers.coreldove-storefront.rule=Host(`stg.bizoholic.com`) && PathPrefix(`/store`)
traefik.http.routers.coreldove-storefront.entrypoints=websecure
traefik.http.routers.coreldove-storefront.tls.certresolver=letsencrypt
traefik.http.services.coreldove-storefront.loadbalancer.server.port=3002

# Middleware to strip /store prefix if needed
traefik.http.middlewares.coreldove-stripprefix.stripprefix.prefixes=/store
traefik.http.routers.coreldove-storefront.middlewares=coreldove-stripprefix
```

**Note:** Since `next.config.js` already has `basePath: "/store"`, the stripprefix middleware may NOT be needed. Test first without it.

#### 5. Health Check
```yaml
HEALTHCHECK:
  interval: 30s
  timeout: 10s
  retries: 3
  test: node -e "require('http').get('http://localhost:3002/', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"
```

#### 6. Deploy
1. Click **"Deploy"** in Dokploy UI
2. Monitor deployment logs
3. Wait for container to be healthy
4. Verify service is running

---

## 🔍 VERIFICATION STEPS

### 1. Check Service Status
```bash
ssh root@72.60.219.244

# Check if container is running
docker ps | grep coreldove-storefront

# Check container logs
docker logs coreldove-storefront -f

# Check service in Docker Swarm
docker service ls | grep coreldove
docker service ps coreldove-storefront
```

### 2. Test Internal Connectivity
```bash
# From KVM4 server
docker exec coreldove-storefront curl http://localhost:3002/

# Should return HTML of the homepage
```

### 3. Test Brain Gateway Connection
```bash
# Test if storefront can reach Brain Gateway
docker exec coreldove-storefront curl -I http://backend-brain-gateway:8001/api/saleor/graphql

# Should return: HTTP/1.1 200 OK
```

### 4. Test Public URL
```bash
# From your local machine
curl -I https://stg.bizoholic.com/store

# Should return: HTTP/2 200
```

### 5. Browser Test
```
URL: https://stg.bizoholic.com/store

Expected:
✅ CoreLdove homepage loads
✅ Product listings appear
✅ Images load correctly
✅ Navigation works
✅ No console errors

Check Network Tab:
✅ API calls go to /api/saleor/graphql (proxied through gateway)
✅ All requests use relative URLs
✅ No CORS errors
```

---

## 🧠 VERIFY BRAIN GATEWAY ROUTING

The CoreLdove Storefront MUST route all Saleor API calls through the Brain Gateway.

### Check Gateway Has Saleor Route

```bash
ssh root@72.60.219.244

# Find Brain Gateway container
docker ps | grep brain-gateway

# Test Saleor proxy route
docker exec backend-brain-gateway.1.* curl -X POST \
  http://localhost:8001/api/saleor/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ shop { name description } }"}'

# Should return JSON with shop details
```

### If Route Doesn't Exist

The Brain Gateway needs this route added:

```python
# brain-gateway/app/routes/saleor.py

from fastapi import APIRouter, Request, Response
from httpx import AsyncClient

router = APIRouter(prefix="/api/saleor", tags=["saleor"])

@router.post("/graphql")
@router.get("/graphql")
async def saleor_graphql_proxy(request: Request):
    """Proxy GraphQL requests to Saleor backend"""
    body = await request.json() if request.method == "POST" else None

    async with AsyncClient(timeout=30.0) as client:
        response = await client.request(
            method=request.method,
            url="http://backend-saleor-api:8000/graphql/",
            json=body,
            params=dict(request.query_params) if request.method == "GET" else None,
            headers={"Content-Type": "application/json"}
        )

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
```

---

## 🚨 TROUBLESHOOTING

### Issue 1: Container Won't Start
```bash
# Check logs
docker logs coreldove-storefront

# Common causes:
# - Missing environment variables
# - Port 3002 already in use
# - Network connectivity issues
```

### Issue 2: GraphQL Errors
```bash
# Check Brain Gateway is accessible
docker exec coreldove-storefront ping backend-brain-gateway

# Check Saleor backend is running
docker service ps backend-saleor-api

# Verify environment variable
docker exec coreldove-storefront env | grep SALEOR_API_URL
```

### Issue 3: 404 on /store
```
Problem: Traefik routing not configured correctly

Solution:
1. Verify Traefik labels in Dokploy
2. Check next.config.js has basePath: "/store"
3. Restart Traefik if needed
```

### Issue 4: Images Not Loading
```
Problem: Image domains not whitelisted

Solution:
In next.config.js, ensure:
images: {
  remotePatterns: [{
    hostname: "*"  // Or specific CDN domain
  }]
}
```

---

## 📊 MONITORING

### Logs
```bash
# Real-time logs
docker logs coreldove-storefront -f --tail 100

# Search for errors
docker logs coreldove-storefront 2>&1 | grep -i error
```

### Metrics
```bash
# Container stats
docker stats coreldove-storefront

# Memory usage
docker inspect coreldove-storefront | grep Memory

# Health status
docker inspect coreldove-storefront | grep Health -A 10
```

---

## 🔄 UPDATING THE DEPLOYMENT

### Rebuild and Redeploy

```bash
# 1. Make changes to code
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/coreldove-storefront

# 2. Rebuild image
docker build -f Dockerfile.production \
  -t ghcr.io/bizoholic-digital/coreldove-storefront:v1.0.2 \
  -t ghcr.io/bizoholic-digital/coreldove-storefront:latest \
  .

# 3. Push to GHCR
docker push ghcr.io/bizoholic-digital/coreldove-storefront:v1.0.2
docker push ghcr.io/bizoholic-digital/coreldove-storefront:latest

# 4. Redeploy in Dokploy UI
# Click "Redeploy" button in application settings
```

---

## ✅ POST-DEPLOYMENT CHECKLIST

- [ ] Container is running and healthy
- [ ] Accessible at https://stg.bizoholic.com/store
- [ ] Homepage loads correctly
- [ ] Product listings work
- [ ] GraphQL queries go through Brain Gateway
- [ ] Images load from CDN/backend
- [ ] No console errors
- [ ] Cart functionality works
- [ ] Checkout flow accessible
- [ ] Mobile responsive
- [ ] Performance is good (< 3s load time)

---

## 📝 DEPLOYMENT SUMMARY

### What Was Deployed
```
Application:    CoreLdove Storefront
Base:           Saleor Next.js Official Storefront
Framework:      Next.js 15.2.4 with App Router
Package Mgr:    pnpm 9.6.0
Image Size:     202MB (standalone build)
Architecture:   Standalone Microservice (DDD-compliant)
Routing:        ALL API calls through Brain Gateway
```

### Key Features
- ✅ E-commerce storefront with full Saleor features
- ✅ Multi-channel support (default-channel)
- ✅ GraphQL-driven data fetching
- ✅ Server-side rendering (SSR) and Static Generation (SSG)
- ✅ Integrated payment gateways (Stripe, Adyen)
- ✅ Centralized API routing through Brain Gateway
- ✅ Optimized for performance (102 kB first load)

### Next Steps
1. Deploy to KVM4 via Dokploy (follow steps above)
2. Verify Brain Gateway has Saleor proxy route
3. Test all functionality
4. Configure Saleor backend with products/categories
5. Set up payment gateway credentials
6. Test checkout flow end-to-end

---

**Status:** ✅ Ready for Deployment
**Documentation:** Complete
**Build Artifacts:** Available in GHCR
**Deployment Method:** Dokploy UI (recommended) or Docker Swarm CLI
