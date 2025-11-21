# Saleor Dashboard Deployment Guide - KVM4 via Dokploy

**Service:** CoreLdove E-Commerce Admin Dashboard
**Priority:** HIGH (Essential for CoreLdove e-commerce management)
**Effort:** LOW (Official image - no custom build required)
**Status:** Ready for deployment

## Overview

The Saleor Dashboard is the official admin interface for managing the CoreLdove e-commerce platform. We'll use the official Saleor Dashboard Docker image with Dokploy for easy deployment and management.

## Official Image Details

- **Image:** `ghcr.io/saleor/saleor-dashboard:latest`
- **Version:** 3.20 (compatible with Saleor Core 3.20)
- **Official Docs:** https://docs.saleor.io/docs/3.x/dashboard/quickstart
- **Container Port:** 80 (Nginx serving static React app)
- **Host Port:** 9000

## Dokploy Configuration

### Service Configuration

```yaml
Service Name: saleor-dashboard
Service Type: Docker Image
Image: ghcr.io/saleor/saleor-dashboard:latest
```

### Port Mapping

```yaml
Container Port: 80
Host Port: 9000
Protocol: TCP
```

### Environment Variables

**Required Configuration:**

```yaml
API_URL: http://172.31.0.1:8000/graphql/
```

**Notes:**
- `API_URL` must point to the Saleor Core GraphQL endpoint
- Use the internal Docker network IP for KVM4
- Default value is `http://localhost:8000/graphql/` if not specified
- The dashboard is a static React app that connects to the API from the browser

### URL Routing (Traefik)

**Primary URL:**
```
https://stg.coreldove.com/dashboard
```

**Traefik Labels:**
```yaml
traefik.enable: "true"
traefik.http.routers.saleor-dashboard.rule: "Host(`stg.coreldove.com`) && PathPrefix(`/dashboard`)"
traefik.http.routers.saleor-dashboard.entrypoints: "websecure"
traefik.http.routers.saleor-dashboard.tls: "true"
traefik.http.routers.saleor-dashboard.tls.certresolver: "letsencrypt"
traefik.http.services.saleor-dashboard.loadbalancer.server.port: "80"

# Strip /dashboard prefix for the container
traefik.http.middlewares.saleor-dashboard-stripprefix.stripprefix.prefixes: "/dashboard"
traefik.http.routers.saleor-dashboard.middlewares: "saleor-dashboard-stripprefix"
```

### Resource Limits

```yaml
CPU Limit: 0.5 cores
Memory Limit: 512MB
Memory Reservation: 256MB
```

**Rationale:** Static React app served by Nginx - very lightweight

### Health Check

```yaml
Test: ["CMD", "curl", "-f", "http://localhost:80/"]
Interval: 30s
Timeout: 10s
Retries: 3
Start Period: 40s
```

## Deployment Steps via Dokploy UI

### 1. Access Dokploy

```bash
URL: https://automationhub-n8n-91feb0-194-238-16-237.traefik.me
VPS: KVM4 (72.60.219.244)
```

### 2. Create New Service

1. Navigate to **Services** → **Add Service**
2. Select **Docker Image** service type
3. Enter service details:
   - **Service Name:** `saleor-dashboard`
   - **Image:** `ghcr.io/saleor/saleor-dashboard:latest`
   - **Project:** CoreLdove (or appropriate project)

### 3. Configure Ports

1. Go to **Network** tab
2. Add port mapping:
   - **Container Port:** 80
   - **Host Port:** 9000
   - **Protocol:** TCP

### 4. Set Environment Variables

1. Go to **Environment** tab
2. Add environment variable:
   - **Key:** `API_URL`
   - **Value:** `http://172.31.0.1:8000/graphql/`

**Important:** Replace `172.31.0.1` with the actual internal IP of the Saleor Core service on KVM4.

### 5. Configure Resource Limits

1. Go to **Resources** tab
2. Set limits:
   - **CPU Limit:** 0.5
   - **Memory Limit:** 512 (MB)
   - **Memory Reservation:** 256 (MB)

### 6. Configure Traefik Routing

1. Go to **Routing** tab
2. Enable Traefik
3. Add labels:

```yaml
traefik.enable=true
traefik.http.routers.saleor-dashboard.rule=Host(`stg.coreldove.com`) && PathPrefix(`/dashboard`)
traefik.http.routers.saleor-dashboard.entrypoints=websecure
traefik.http.routers.saleor-dashboard.tls=true
traefik.http.routers.saleor-dashboard.tls.certresolver=letsencrypt
traefik.http.services.saleor-dashboard.loadbalancer.server.port=80
traefik.http.middlewares.saleor-dashboard-stripprefix.stripprefix.prefixes=/dashboard
traefik.http.routers.saleor-dashboard.middlewares=saleor-dashboard-stripprefix
```

### 7. Deploy

1. Click **Deploy** button
2. Wait for the container to pull and start
3. Monitor logs for any startup errors

## Post-Deployment Verification

### 1. Check Service Status

```bash
# Via Dokploy UI
Services → saleor-dashboard → Status should be "Running"

# Via SSH (if needed)
sshpass -p '&k3civYG5Q6YPb' ssh -o StrictHostKeyChecking=no root@72.60.219.244 \
  "docker ps | grep saleor-dashboard"
```

### 2. Verify HTTP Response

```bash
# Direct container access
curl -I http://72.60.219.244:9000/

# Via Traefik (domain routing)
curl -I https://stg.coreldove.com/dashboard/
```

Expected: HTTP 200 OK

### 3. Test Dashboard Access

1. Open browser: `https://stg.coreldove.com/dashboard/`
2. Should see Saleor Dashboard login page
3. Verify static assets load (CSS, JS, images)
4. Check browser console for API connection errors

### 4. Test API Connection

1. Try to login with Saleor credentials
2. Dashboard should connect to `http://172.31.0.1:8000/graphql/`
3. Verify in browser Network tab that GraphQL requests succeed
4. Check browser console for CORS errors (if any)

### 5. Verify Logs

```bash
# Via Dokploy UI
Services → saleor-dashboard → Logs

# Look for:
# - Nginx startup messages
# - No error logs
# - Access logs when navigating
```

## Troubleshooting

### Issue 1: Dashboard Loads but Can't Connect to API

**Symptoms:** Dashboard UI loads, but login fails with "Network error" or "Cannot connect to API"

**Causes:**
1. Wrong `API_URL` environment variable
2. Saleor Core service not running
3. CORS not configured on Saleor Core

**Solutions:**

```bash
# Check Saleor Core is running
docker ps | grep saleor

# Verify API_URL is correct
docker inspect saleor-dashboard | grep API_URL

# Test API endpoint directly
curl http://172.31.0.1:8000/graphql/ -d '{"query":"{ shop { name } }"}'

# Check Saleor Core CORS settings
# API_URL must be in ALLOWED_CLIENT_HOSTS in Saleor Core
```

### Issue 2: 502 Bad Gateway

**Symptoms:** https://stg.coreldove.com/dashboard/ returns 502

**Causes:**
1. Container not running
2. Wrong port mapping
3. Traefik misconfiguration

**Solutions:**

```bash
# Check container status
docker ps | grep saleor-dashboard

# Check Traefik routes
docker logs traefik 2>&1 | grep saleor-dashboard

# Verify port is listening
netstat -tulpn | grep 9000

# Test direct container access
curl http://localhost:9000/
```

### Issue 3: Static Assets 404

**Symptoms:** Dashboard page loads but CSS/JS files return 404

**Causes:**
1. Strip prefix middleware misconfigured
2. Wrong base path in dashboard config

**Solutions:**

```bash
# Verify stripprefix middleware is applied
docker logs traefik 2>&1 | grep stripprefix

# Check Nginx access logs
docker logs saleor-dashboard 2>&1 | tail -50

# Test asset paths
curl -I https://stg.coreldove.com/dashboard/static/css/main.css
```

### Issue 4: CORS Errors

**Symptoms:** Browser console shows CORS policy errors

**Causes:**
1. Saleor Core CORS not configured for dashboard domain
2. Wrong API_URL scheme (http vs https)

**Solutions:**

```bash
# Update Saleor Core environment variables:
ALLOWED_CLIENT_HOSTS=stg.coreldove.com,localhost

# Restart Saleor Core service after adding domain
docker restart saleor-core

# Verify CORS headers
curl -I -H "Origin: https://stg.coreldove.com" \
  http://172.31.0.1:8000/graphql/
```

## Architecture Integration

### Service Dependency Map

```
User Browser
    ↓ HTTPS
Traefik (Reverse Proxy)
    ↓ HTTP (strip /dashboard)
Saleor Dashboard Container (Port 9000)
    ↓ GraphQL API calls (from user browser)
Saleor Core API (Port 8000)
    ↓
PostgreSQL Database
```

**Important:** The dashboard is a **client-side React application**. API calls are made directly from the user's browser to the Saleor Core API, not from the dashboard container.

### Security Considerations

1. **HTTPS Only:** All external access via HTTPS (Traefik handles SSL)
2. **CORS Configuration:** Saleor Core must whitelist dashboard domain
3. **Authentication:** Dashboard uses Saleor Core's JWT authentication
4. **API Access:** GraphQL API must be accessible to end users (not container-to-container only)

### Performance Optimization

1. **CDN Caching:** Static assets can be cached by Traefik/browser
2. **Nginx Configuration:** Official image already optimized with gzip, caching headers
3. **Resource Limits:** 512MB is more than enough for Nginx serving static files

## Success Criteria

✅ **Deployment Successful When:**

1. Container status shows "Running" in Dokploy
2. https://stg.coreldove.com/dashboard/ returns HTTP 200
3. Dashboard login page loads with all styles/scripts
4. Can successfully login with Saleor admin credentials
5. Dashboard can query and display store data
6. No CORS errors in browser console
7. Resource usage stays under limits (< 512MB RAM, < 0.5 CPU)

## Next Steps After Deployment

1. ✅ Verify dashboard deployment and API connection
2. 📝 Update [COMPLETE_FRONTEND_MIGRATION_ROADMAP.md](./COMPLETE_FRONTEND_MIGRATION_ROADMAP.md)
3. ✅ Mark Saleor Dashboard as completed (6/9 services)
4. 🚀 Proceed with next frontend: Analytics Dashboard or Setup Wizard

---

**Deployment Method:** Dokploy UI (Official Saleor Dashboard Image)
**Date:** November 3, 2025
**Deployment Team:** BizOSaaS Platform Team
**Status:** Ready for deployment - configuration documented
