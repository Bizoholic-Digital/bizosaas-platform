# Traefik Routing Configuration - January 7, 2026

## ✅ Changes Applied

Added complete Traefik routing labels to all three services to enable proper domain routing and SSL certificates.

## 📋 What Was Added

### Common Labels for All Services

Each service now has the following Traefik configuration:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.docker.network=dokploy-network"
  
  # HTTP Router (redirect to HTTPS)
  - "traefik.http.routers.SERVICE-http.rule=Host(`DOMAIN`)"
  - "traefik.http.routers.SERVICE-http.entrypoints=web"
  - "traefik.http.routers.SERVICE-http.middlewares=redirect-to-https"
  
  # HTTPS Router
  - "traefik.http.routers.SERVICE.rule=Host(`DOMAIN`)"
  - "traefik.http.routers.SERVICE.entrypoints=websecure"
  - "traefik.http.routers.SERVICE.tls=true"
  - "traefik.http.routers.SERVICE.tls.certresolver=letsencrypt"
  
  # Service
  - "traefik.http.services.SERVICE.loadbalancer.server.port=PORT"
  
  # Middleware for HTTPS redirect
  - "traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https"
  - "traefik.http.middlewares.redirect-to-https.redirectscheme.permanent=true"
```

### Service-Specific Configurations

#### 1. Brain Gateway (API)
- **Domain**: `api.bizoholic.net`
- **Port**: `8000`
- **Router Name**: `brain-gateway`
- **File**: `docker-compose.core.yml`

#### 2. Admin Portal
- **Domain**: `admin.bizoholic.net`
- **Port**: `3000`
- **Router Name**: `admin-dashboard`
- **File**: `docker-compose.admin-portal.yml`

#### 3. Client Portal
- **Domain**: `app.bizoholic.net`
- **Port**: `3000`
- **Router Name**: `client-portal`
- **File**: `docker-compose.client-portal.yml`

## 🔧 How Traefik Routing Works

### 1. **HTTP Entry (Port 80)**
```
User → http://admin.bizoholic.net
  ↓
Traefik (web entrypoint)
  ↓
Matches: traefik.http.routers.admin-dashboard-http.rule=Host(`admin.bizoholic.net`)
  ↓
Applies middleware: redirect-to-https
  ↓
Redirects to: https://admin.bizoholic.net
```

### 2. **HTTPS Entry (Port 443)**
```
User → https://admin.bizoholic.net
  ↓
Traefik (websecure entrypoint)
  ↓
Matches: traefik.http.routers.admin-dashboard.rule=Host(`admin.bizoholic.net`)
  ↓
TLS enabled with Let's Encrypt certificate
  ↓
Routes to: admin-dashboard container on port 3000
  ↓
Service responds
```

## 🎯 Benefits of This Configuration

### ✅ Automatic SSL Certificates
- Let's Encrypt certificates are automatically requested and renewed
- No manual certificate management needed
- Works for custom domains configured in Dokploy UI

### ✅ HTTP to HTTPS Redirect
- All HTTP traffic is automatically redirected to HTTPS
- Permanent redirect (301) for SEO benefits
- Secure by default

### ✅ Dokploy UI Integration
- Custom domains can be configured in Dokploy UI
- Traefik.me default domains will work automatically
- No manual Traefik configuration needed

### ✅ Multi-Service Support
- Multiple services can run on the same server
- No port conflicts (all use internal ports)
- Domain-based routing handles traffic distribution

## 🚀 Deployment Steps

### Step 1: Redeploy Brain Gateway
1. Go to Dokploy UI → BizOSaaS Brain Gateway
2. Click "Redeploy"
3. Wait for deployment to complete
4. Verify: `https://api.bizoholic.net/health`

### Step 2: Redeploy Admin Portal
1. Go to Dokploy UI → BizOSaaS Frontend (Admin Portal)
2. Click "Redeploy"
3. Wait for deployment to complete
4. Verify: `https://admin.bizoholic.net`

### Step 3: Redeploy Client Portal
1. Go to Dokploy UI → BizOSaaS Frontend (Client Portal)
2. Click "Redeploy"
3. Wait for deployment to complete
4. Verify: `https://app.bizoholic.net`

## 🔍 Verification

After redeployment, check each service:

```bash
# Check HTTP redirect (should return 301)
curl -I http://api.bizoholic.net
curl -I http://admin.bizoholic.net
curl -I http://app.bizoholic.net

# Check HTTPS (should return 200)
curl -I https://api.bizoholic.net/health
curl -I https://admin.bizoholic.net
curl -I https://app.bizoholic.net

# Check SSL certificate
openssl s_client -connect api.bizoholic.net:443 -servername api.bizoholic.net < /dev/null 2>/dev/null | grep "subject="
```

## 📊 Traefik Dashboard

To view routing in Traefik dashboard:
1. Access Traefik UI (if enabled in Dokploy)
2. Check "HTTP Routers" section
3. You should see:
   - `brain-gateway-http` → redirects to HTTPS
   - `brain-gateway` → routes to brain-gateway service
   - `admin-dashboard-http` → redirects to HTTPS
   - `admin-dashboard` → routes to admin-dashboard service
   - `client-portal-http` → redirects to HTTPS
   - `client-portal` → routes to client-portal service

## 🐛 Troubleshooting

### Issue: Domain not accessible
**Check:**
1. DNS records point to server IP
2. Service is running: `docker ps | grep SERVICE_NAME`
3. Container is on dokploy-network: `docker inspect CONTAINER | grep dokploy-network`
4. Traefik labels are applied: `docker inspect CONTAINER | grep traefik`

### Issue: SSL certificate not generated
**Check:**
1. Domain DNS is properly configured
2. Port 80 and 443 are accessible from internet
3. Let's Encrypt rate limits not exceeded
4. Check Traefik logs: `docker logs dokploy-traefik`

### Issue: 404 or 502 errors
**Check:**
1. Service is healthy: `docker ps` (check STATUS column)
2. Service port matches Traefik label: `loadbalancer.server.port`
3. Service is on correct network: `dokploy-network`
4. Check service logs: `docker logs CONTAINER_NAME`

## 📝 Configuration in Dokploy UI

### Adding Custom Domain
1. Go to service in Dokploy UI
2. Navigate to "Domains" section
3. Add custom domain (e.g., `admin.bizoholic.net`)
4. Dokploy will automatically:
   - Update Traefik configuration
   - Request SSL certificate
   - Enable routing

### Traefik.me Default Domain
- Dokploy automatically provides a `*.traefik.me` domain
- Format: `SERVICE-PROJECT.traefik.me`
- Works immediately without DNS configuration
- Useful for testing before custom domain setup

## 🎓 Best Practices

### ✅ DO:
- Use HTTPS for all production traffic
- Let Traefik handle SSL certificates
- Use domain-based routing (not port-based)
- Keep services on dokploy-network
- Use `expose` instead of `ports` in docker-compose

### ❌ DON'T:
- Bind services to host ports (causes conflicts)
- Manually manage SSL certificates
- Bypass Traefik for external access
- Use IP-based routing in production
- Mix external and internal network modes

## 📦 Git Commit

**Commit**: `51bda36`
**Branch**: `staging`
**Message**: "fix: Add complete Traefik routing labels for all services"

## 🔄 Next Steps

1. ✅ Changes committed and pushed to GitHub
2. ⏳ Redeploy all three services via Dokploy UI
3. ⏳ Verify domain accessibility
4. ⏳ Test SSL certificates
5. ⏳ Configure custom domains in Dokploy UI (if not already done)
6. ⏳ Test login flows on both portals

---

**Note**: After redeployment, it may take 1-2 minutes for Let's Encrypt to issue SSL certificates for new domains. During this time, you might see certificate warnings - this is normal and will resolve automatically.
