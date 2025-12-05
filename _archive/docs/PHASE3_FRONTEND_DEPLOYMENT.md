# Phase 3: Frontend Applications Deployment Guide
## BizOSaaS Platform - Staging Environment

**Status**: READY FOR DEPLOYMENT
**Phase**: 3 of 3 (Final Deployment Phase)
**Target Environment**: Staging with staging subdomains
**Deployment Method**: Dokploy with Traefik proxy
**Total Containers**: 6 frontend applications

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Domain Configuration](#domain-configuration)
4. [Deployment Steps](#deployment-steps)
5. [SSL Certificate Setup](#ssl-certificate-setup)
6. [Verification Procedures](#verification-procedures)
7. [Troubleshooting](#troubleshooting)
8. [Post-Deployment](#post-deployment)

---

## Overview

### What This Phase Deploys

Phase 3 deploys all 6 frontend applications with staging domain configuration:

| Application | Container | Port | Domain/Path | Purpose |
|------------|-----------|------|-------------|---------|
| Bizoholic Frontend | bizoholic-frontend-3000 | 3000 | stg.bizoholic.com | Marketing website |
| Client Portal | bizosaas-client-portal-3001 | 3001 | stg.bizoholic.com/login/ | Client dashboard |
| Admin Dashboard | bizosaas-admin-3009 | 3009 | stg.bizoholic.com/admin/ | Admin interface |
| CorelDove Frontend | coreldove-frontend-3002 | 3002 | stg.coreldove.com | E-commerce site |
| ThrillRing Gaming | thrillring-gaming-3005 | 3005 | stg.thrillring.com | Gaming platform |
| Business Directory | business-directory-3004 | 3004 | Internal testing | Directory service |

### Architecture Overview

```
Internet
    │
    └─> Traefik Reverse Proxy (Dokploy built-in)
            │
            ├─> stg.bizoholic.com → bizoholic-frontend-3000:3000
            ├─> stg.bizoholic.com/login/ → client-portal-3001:3001
            ├─> stg.bizoholic.com/admin/ → admin-dashboard-3009:3009
            ├─> stg.coreldove.com → coreldove-frontend-3002:3002
            └─> stg.thrillring.com → thrillring-gaming-3005:3005
                    │
                    └─> Backend Services (Phase 2)
                            │
                            └─> Infrastructure (Phase 1)
```

### Key Features

- **Staging Subdomains**: Real staging domains for testing
- **Path-based Routing**: /login/ and /admin/ paths on stg.bizoholic.com
- **SSL Certificates**: Automatic Let's Encrypt SSL for all domains
- **Reverse Proxy**: Traefik handles all routing and SSL
- **Next.js SSR**: Server-side rendering for optimal performance
- **API Integration**: All frontends connected to Brain API
- **Debug Mode**: Enabled for detailed staging logs

---

## Prerequisites

### Required Infrastructure (Phase 1)

All Phase 1 infrastructure services must be running:

```bash
# Verify infrastructure containers
docker ps | grep -E "postgres|redis|vault|temporal"

# Expected containers:
# bizosaas-postgres-staging        (port 5432)
# bizosaas-redis-staging           (port 6379)
# bizosaas-vault-staging           (port 8200)
# bizosaas-temporal-server-staging (port 7233)
# bizosaas-temporal-ui-staging     (port 8082)
# bizosaas-temporal-integration-staging (port 8009)
```

**Status Check**: Run infrastructure verification
```bash
cd /home/alagiri/projects/bizoholic
./verify-infrastructure-deployment.sh
```

### Required Backend Services (Phase 2)

All Phase 2 backend services must be running and healthy:

```bash
# Verify backend containers
docker ps | grep -E "brain|wagtail|crm|directory|coreldove|ai-agents|amazon|saleor"

# Expected containers:
# bizosaas-brain-staging           (port 8001) ✓
# bizosaas-wagtail-staging         (port 8002) ✓
# bizosaas-django-crm-staging      (port 8003) ✓
# bizosaas-directory-api-staging   (port 8004) ✓
# coreldove-backend-staging        (port 8005) ✓
# bizosaas-ai-agents-staging       (port 8010) ✓
# amazon-sourcing-staging          (port 8085) ✓
# bizosaas-saleor-staging          (port 8000) ✓
```

**Status Check**: Run backend verification
```bash
cd /home/alagiri/projects/bizoholic
./verify-backend-deployment.sh
```

### Domain DNS Configuration

**CRITICAL**: Configure DNS before deployment for SSL certificates to work.

#### Primary Staging Domains

| Domain | Type | Value | TTL |
|--------|------|-------|-----|
| stg.bizoholic.com | A | 194.238.16.237 | 300 |
| stg.coreldove.com | A | 194.238.16.237 | 300 |
| stg.thrillring.com | A | 194.238.16.237 | 300 |

**DNS Provider**: Configure in your domain registrar's DNS settings

**Propagation Time**: 5-30 minutes (usually)

**Verification**:
```bash
# Test DNS resolution
nslookup stg.bizoholic.com
nslookup stg.coreldove.com
nslookup stg.thrillring.com

# Should return: 194.238.16.237
```

### VPS Access

- **VPS IP**: 194.238.16.237
- **SSH Access**: Configured and tested
- **Dokploy URL**: http://194.238.16.237:3000
- **Dokploy Login**: Admin credentials ready

### System Requirements

**Minimum Resources**:
- CPU: 2 cores (in addition to Phases 1+2)
- RAM: 4 GB (in addition to Phases 1+2)
- Disk: 20 GB free space
- Network: 100 Mbps

**Total System Resources** (All Phases):
- CPU: 8 cores recommended
- RAM: 16 GB recommended
- Disk: 100 GB recommended

**Current Usage Check**:
```bash
# SSH into VPS
ssh user@194.238.16.237

# Check resources
docker stats --no-stream
df -h
free -m
```

### GitHub Repository Access

- **Repository**: https://github.com/Bizoholic-Digital/bizosaas-platform.git
- **Access**: Public or deploy key configured
- **Dockerfiles**: All frontend Dockerfiles present in repository

**Verification**:
```bash
# Test repository access
curl -I https://github.com/Bizoholic-Digital/bizosaas-platform.git
# Should return: HTTP 200 or redirect
```

---

## Domain Configuration

### Domain Priority and Routing

Traefik uses priority values to determine routing order. Higher priority routes are evaluated first.

**Route Configuration**:

1. **Client Portal** (`/login/` path)
   - Priority: 10 (highest)
   - Rule: `Host(stg.bizoholic.com) && PathPrefix(/login)`
   - Middleware: Strip `/login` prefix
   - Target: Port 3001

2. **Admin Dashboard** (`/admin/` path)
   - Priority: 10 (highest)
   - Rule: `Host(stg.bizoholic.com) && PathPrefix(/admin)`
   - Middleware: Strip `/admin` prefix
   - Target: Port 3009

3. **Bizoholic Marketing** (main site)
   - Priority: 1 (lowest for catch-all)
   - Rule: `Host(stg.bizoholic.com) && !PathPrefix(/login) && !PathPrefix(/admin)`
   - Target: Port 3000

4. **CorelDove E-commerce**
   - Priority: Default
   - Rule: `Host(stg.coreldove.com)`
   - Target: Port 3002

5. **ThrillRing Gaming**
   - Priority: Default
   - Rule: `Host(stg.thrillring.com)`
   - Target: Port 3005

### Path-Based Routing Details

**How it works**:

1. User visits `https://stg.bizoholic.com/login/dashboard`
2. Traefik matches highest priority route (portal)
3. Middleware strips `/login` from path
4. Request forwarded to container as `/dashboard`
5. Container responds with correct content

**Important**: Applications must be configured to handle their base path correctly.

### SSL Certificate Configuration

**Let's Encrypt Integration**:
- Automatic certificate generation
- Auto-renewal every 60 days
- Wildcard certificates NOT used (individual certs per domain)
- Certificate resolver: `letsencrypt`

**Traefik Labels for SSL**:
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.app-name.tls=true"
  - "traefik.http.routers.app-name.tls.certresolver=letsencrypt"
```

**Certificate Storage**: Handled automatically by Dokploy/Traefik

**Verification**: Check browser shows green lock icon

---

## Deployment Steps

### Step 1: Access Dokploy Dashboard

1. Open browser and navigate to: http://194.238.16.237:3000
2. Log in with admin credentials
3. Navigate to "Projects" section

**Expected**: Dokploy dashboard loads successfully

### Step 2: Create Frontend Project

1. Click **"Create Project"** button
2. Fill in project details:
   - **Project Name**: `bizosaas-frontend-staging`
   - **Description**: `BizOSaaS Frontend Applications - Staging Environment`
   - **Environment**: `Staging`

3. Click **"Create"**

**Expected**: New project created and visible in projects list

### Step 3: Create Docker Compose Application

1. Inside the `bizosaas-frontend-staging` project, click **"Add Application"**
2. Select **"Docker Compose"** application type
3. Fill in application details:
   - **Application Name**: `frontend-applications`
   - **Description**: `6 frontend containers with staging domains`

4. Click **"Create"**

**Expected**: New application created

### Step 4: Upload Configuration File

**Option A: Direct Upload (Recommended)**

1. Click **"Upload docker-compose.yml"** button
2. Browse to: `/home/alagiri/projects/bizoholic/dokploy-frontend-staging.yml`
3. Select and upload the file
4. Verify configuration appears in editor

**Option B: Copy-Paste**

1. Open local file:
```bash
cat /home/alagiri/projects/bizoholic/dokploy-frontend-staging.yml
```

2. Copy entire contents
3. In Dokploy, click **"Edit Configuration"**
4. Paste configuration into editor
5. Click **"Save Configuration"**

**Expected**: Configuration loaded with 6 services visible

### Step 5: Verify Configuration

Review the loaded configuration and verify:

**Services Present**:
- ✓ bizoholic-frontend
- ✓ coreldove-frontend
- ✓ thrillring-gaming
- ✓ client-portal
- ✓ admin-dashboard
- ✓ business-directory

**Network Configuration**:
- ✓ Network: `bizosaas-network` (external)
- ✓ All services connected to same network

**Traefik Labels**:
- ✓ All domain services have Traefik labels
- ✓ TLS enabled on all public services
- ✓ Certificate resolver configured
- ✓ Path-based routes have correct priorities

**Environment Variables**:
- ✓ NODE_ENV=staging on all services
- ✓ NEXT_PUBLIC_API_BASE_URL points to Brain API
- ✓ NEXT_PUBLIC_SITE_URL matches domain
- ✓ DEBUG_MODE=true for staging
- ✓ ENABLE_ANALYTICS=false for staging

### Step 6: Configure Build Settings (Optional)

If using Git-based deployment instead of GitHub URL in build context:

1. Navigate to **"Build Settings"**
2. Configure:
   - **Repository**: `https://github.com/Bizoholic-Digital/bizosaas-platform.git`
   - **Branch**: `main`
   - **Build Context**: Root directory

3. Save settings

**Note**: Current configuration uses GitHub URL in `build.context`, which works without this step.

### Step 7: Deploy Application

1. Review all configuration one final time
2. Click **"Deploy"** button (large green button)
3. Confirm deployment when prompted

**Expected**: Deployment process starts

### Step 8: Monitor Deployment Progress

**Watch the Deployment Logs**:

1. Click **"Logs"** tab
2. Monitor build progress for each service
3. Watch for successful container starts

**Expected Timeline**:
- Image building: 10-15 minutes (Next.js builds)
- Container startup: 2-3 minutes
- Total time: 12-18 minutes

**Progress Indicators**:
```
✓ Pulling base images...
✓ Building bizoholic-frontend...
✓ Building coreldove-frontend...
✓ Building thrillring-gaming...
✓ Building client-portal...
✓ Building admin-dashboard...
✓ Building business-directory...
✓ Starting containers...
✓ Configuring Traefik routes...
✓ Requesting SSL certificates...
✓ Deployment complete!
```

**Common Log Messages** (Normal):
- "Installing dependencies..." (npm install)
- "Building application..." (Next.js build)
- "Optimizing production build..."
- "Container started successfully"
- "Health check passed"

**Warning Messages to Ignore** (Non-Critical):
- Development dependency warnings
- Optional peer dependency notices
- TypeScript build warnings

**Error Messages to Watch For** (Critical):
- "Build failed"
- "Container exited with code 1"
- "Network not found"
- "Cannot connect to database"

### Step 9: Verify Container Status

After deployment completes:

1. Navigate to **"Containers"** tab
2. Verify all 6 containers show **"Running"** status
3. Check health status shows **"Healthy"** (may take 30-60 seconds)

**Expected Container Status**:
```
bizoholic-frontend-3000        Running  Healthy
coreldove-frontend-3002        Running  Healthy
thrillring-gaming-3005         Running  Healthy
bizosaas-client-portal-3001    Running  Healthy
bizosaas-admin-3009            Running  Healthy
business-directory-3004        Running  Healthy
```

**If any container shows "Unhealthy" or "Exited"**: See [Troubleshooting](#troubleshooting) section

### Step 10: Verify Traefik Routes

1. Navigate to Traefik dashboard (if enabled)
2. Or check Dokploy **"Domains"** section
3. Verify all routes are configured:

**Expected Routes**:
- stg.bizoholic.com → bizoholic-frontend
- stg.bizoholic.com/login → client-portal
- stg.bizoholic.com/admin → admin-dashboard
- stg.coreldove.com → coreldove-frontend
- stg.thrillring.com → thrillring-gaming

**SSL Certificates**:
- ✓ Certificate issued for stg.bizoholic.com
- ✓ Certificate issued for stg.coreldove.com
- ✓ Certificate issued for stg.thrillring.com

**Certificate Generation Time**: 30-120 seconds after first request

---

## SSL Certificate Setup

### Automatic SSL with Let's Encrypt

Dokploy's Traefik automatically handles SSL certificates using Let's Encrypt.

**How it Works**:

1. Container starts with Traefik labels
2. Traefik detects `tls=true` and `certresolver=letsencrypt`
3. On first HTTPS request, Traefik:
   - Validates domain points to server
   - Requests certificate from Let's Encrypt
   - Completes ACME challenge
   - Installs certificate
   - Starts serving HTTPS traffic

**Timeline**:
- First HTTPS request: 30-120 seconds delay
- Subsequent requests: Instant (certificate cached)
- Certificate renewal: Automatic every 60 days

### Manual Certificate Verification

**Test SSL Certificate Installation**:

```bash
# Test stg.bizoholic.com
curl -I https://stg.bizoholic.com
# Should show: HTTP/2 200 or HTTP/2 301

# Check certificate details
openssl s_client -connect stg.bizoholic.com:443 -servername stg.bizoholic.com < /dev/null 2>/dev/null | openssl x509 -noout -dates
# Should show valid dates

# Test stg.coreldove.com
curl -I https://stg.coreldove.com

# Test stg.thrillring.com
curl -I https://stg.thrillring.com
```

### Troubleshooting SSL Issues

**Problem**: Certificate not generating

**Possible Causes**:
1. DNS not configured correctly
2. Port 80/443 not accessible
3. Domain validation failing
4. Let's Encrypt rate limit hit

**Solutions**:

1. **Verify DNS Resolution**:
```bash
nslookup stg.bizoholic.com
# Must return: 194.238.16.237
```

2. **Check Port Accessibility**:
```bash
# From external machine
telnet 194.238.16.237 80
telnet 194.238.16.237 443
# Both should connect
```

3. **Verify ACME Challenge**:
```bash
# Check Traefik logs
docker logs traefik 2>&1 | grep -i "acme"
# Look for successful ACME challenges
```

4. **Check Let's Encrypt Rate Limits**:
- 50 certificates per domain per week
- 5 duplicate certificates per week
- If hit: Wait 1 week or use staging certificates

**Fallback**: Use HTTP for testing while debugging SSL

### Certificate Renewal

**Automatic Renewal**:
- Traefik checks certificate expiry daily
- Renews certificates 30 days before expiration
- No manual intervention needed

**Manual Renewal** (if needed):
```bash
# Restart Traefik to force renewal check
docker restart traefik
```

---

## Verification Procedures

### Automated Verification Script

Run the comprehensive verification script:

```bash
cd /home/alagiri/projects/bizoholic
./verify-frontend-deployment.sh
```

**Script Checks**:
1. Container status (all 6 running)
2. Health checks (all healthy)
3. Domain accessibility (HTTP/HTTPS)
4. SSL certificate validity
5. Backend connectivity
6. Response time performance
7. Path-based routing
8. Resource usage

**Expected Output**:
```
=== Frontend Deployment Verification ===

✓ Container Status
  ✓ bizoholic-frontend-3000: Running
  ✓ coreldove-frontend-3002: Running
  ✓ thrillring-gaming-3005: Running
  ✓ client-portal-3001: Running
  ✓ admin-dashboard-3009: Running
  ✓ business-directory-3004: Running

✓ Health Checks
  ✓ Bizoholic Frontend: Healthy
  ✓ CorelDove Frontend: Healthy
  ✓ ThrillRing Gaming: Healthy
  ✓ Client Portal: Healthy
  ✓ Admin Dashboard: Healthy
  ✓ Business Directory: Healthy

✓ Domain Accessibility
  ✓ https://stg.bizoholic.com: 200 OK
  ✓ https://stg.coreldove.com: 200 OK
  ✓ https://stg.thrillring.com: 200 OK

✓ Path-Based Routing
  ✓ https://stg.bizoholic.com/login/: 200 OK
  ✓ https://stg.bizoholic.com/admin/: 200 OK

✓ SSL Certificates
  ✓ stg.bizoholic.com: Valid (expires 2026-01-08)
  ✓ stg.coreldove.com: Valid (expires 2026-01-08)
  ✓ stg.thrillring.com: Valid (expires 2026-01-08)

✓ Backend Connectivity
  ✓ All frontends can reach Brain API

=== ALL CHECKS PASSED ===
Deployment successful!
```

**Success Criteria**: All checks show ✓ (green checkmark)

### Manual Domain Testing

**Test Each Domain in Browser**:

1. **Bizoholic Marketing**: https://stg.bizoholic.com
   - Should show: Marketing homepage
   - Check: SSL certificate valid
   - Test: Navigation works
   - Verify: Footer shows staging environment

2. **Client Portal**: https://stg.bizoholic.com/login/
   - Should show: Login page
   - Check: URL doesn't have double slashes
   - Test: Login form renders
   - Verify: Path routing working

3. **Admin Dashboard**: https://stg.bizoholic.com/admin/
   - Should show: Admin login
   - Check: Correct path routing
   - Test: Admin UI loads
   - Verify: Debug mode enabled

4. **CorelDove E-commerce**: https://stg.coreldove.com
   - Should show: E-commerce homepage
   - Check: Product listings load
   - Test: Shopping cart works
   - Verify: Saleor integration active

5. **ThrillRing Gaming**: https://stg.thrillring.com
   - Should show: Gaming platform
   - Check: Game listings render
   - Test: User features work
   - Verify: Gaming API connected

### Performance Testing

**Test Page Load Times**:

```bash
# Bizoholic Frontend
curl -o /dev/null -s -w "Time: %{time_total}s\n" https://stg.bizoholic.com

# CorelDove Frontend
curl -o /dev/null -s -w "Time: %{time_total}s\n" https://stg.coreldove.com

# ThrillRing Gaming
curl -o /dev/null -s -w "Time: %{time_total}s\n" https://stg.thrillring.com
```

**Expected Response Times**:
- First request (cold start): < 3 seconds
- Subsequent requests: < 1 second
- API calls: < 500ms

**Browser Performance**:
1. Open browser developer tools (F12)
2. Navigate to Network tab
3. Visit each staging domain
4. Check:
   - Total page size < 2 MB
   - Number of requests < 50
   - First contentful paint < 2 seconds
   - Time to interactive < 3 seconds

### API Integration Testing

**Test Frontend-to-Backend Communication**:

```bash
# Test from inside frontend container
docker exec bizoholic-frontend-3000 curl http://bizosaas-brain-staging:8001/health

# Expected: {"status": "healthy", "service": "brain"}
```

**Test from Browser Console**:

1. Visit https://stg.bizoholic.com
2. Open developer console (F12)
3. Run:
```javascript
fetch('/api/health')
  .then(r => r.json())
  .then(d => console.log('API Health:', d));
```

**Expected**: API health response logged

### Resource Usage Monitoring

**Check Container Resource Usage**:

```bash
docker stats --no-stream | grep -E "frontend|portal|admin|directory|coreldove|thrillring"
```

**Expected Resource Usage** (per container):
- CPU: 1-5% (idle), up to 50% (under load)
- Memory: 100-300 MB per container
- Total: ~1.5 GB for all 6 frontends

**Warning Signs**:
- CPU > 80% sustained
- Memory > 500 MB per container
- Memory continuously increasing (leak)

---

## Troubleshooting

### Container Won't Start

**Symptoms**: Container status shows "Exited" or "Restarting"

**Diagnosis**:
```bash
# Check container logs
docker logs bizoholic-frontend-3000 --tail 100

# Check exit code
docker inspect bizoholic-frontend-3000 --format='{{.State.ExitCode}}'
```

**Common Causes and Solutions**:

1. **Build Failed**
   - **Cause**: Dockerfile error or dependency issue
   - **Solution**: Check build logs for npm errors
   - **Fix**: Verify package.json and Dockerfile are correct

2. **Port Already in Use**
   - **Cause**: Port 3000-3009 occupied by another service
   - **Solution**: Check for conflicting containers
   - **Fix**: Stop conflicting container or change port

3. **Network Not Found**
   - **Cause**: bizosaas-network doesn't exist
   - **Solution**: Create network from Phase 1/2
   - **Fix**:
   ```bash
   docker network create bizosaas-network
   ```

4. **Cannot Connect to Backend**
   - **Cause**: Brain API not running or wrong hostname
   - **Solution**: Verify backend services are up
   - **Fix**: Check NEXT_PUBLIC_API_BASE_URL environment variable

### Health Check Failing

**Symptoms**: Container running but health check shows "Unhealthy"

**Diagnosis**:
```bash
# Check health check command
docker inspect bizoholic-frontend-3000 | grep -A 5 Healthcheck

# Test health endpoint manually
docker exec bizoholic-frontend-3000 curl -f http://localhost:3000/health
```

**Solutions**:

1. **Health Endpoint Not Implemented**
   - Add `/health` or `/api/health` route to Next.js application
   - Return JSON: `{"status": "healthy"}`

2. **Application Not Fully Started**
   - Wait 60-90 seconds for Next.js to fully start
   - Health check interval: 30 seconds
   - May need 2-3 checks before showing healthy

3. **Port Mismatch**
   - Health check uses wrong port
   - Verify health check matches container internal port

### Domain Not Accessible

**Symptoms**: Cannot access https://stg.bizoholic.com or gets timeout/502 error

**Diagnosis**:
```bash
# Test DNS resolution
nslookup stg.bizoholic.com

# Test port accessibility
curl -I http://194.238.16.237:3000

# Check Traefik routing
docker logs traefik 2>&1 | grep bizoholic
```

**Solutions**:

1. **DNS Not Configured**
   - **Fix**: Add A record for stg.bizoholic.com pointing to 194.238.16.237
   - **Wait**: 5-30 minutes for DNS propagation

2. **Traefik Not Routing**
   - **Cause**: Missing or incorrect Traefik labels
   - **Fix**: Verify labels in docker-compose.yml
   - **Restart**: `docker restart traefik`

3. **Container Not Responding**
   - **Cause**: Application crashed or stuck
   - **Fix**: Check container logs and restart if needed

4. **Firewall Blocking**
   - **Cause**: VPS firewall blocking port 80/443
   - **Fix**: Configure firewall to allow HTTP/HTTPS traffic

### SSL Certificate Issues

**Symptoms**: Browser shows "Not Secure" or certificate error

**Diagnosis**:
```bash
# Check certificate
openssl s_client -connect stg.bizoholic.com:443 -servername stg.bizoholic.com < /dev/null

# Check Traefik ACME logs
docker logs traefik 2>&1 | grep -i "acme\|certificate"
```

**Solutions**:

1. **Certificate Not Generated Yet**
   - **Wait**: 30-120 seconds after first HTTPS request
   - **Retry**: Visit domain again in browser
   - **Force**: Clear browser cache

2. **ACME Challenge Failed**
   - **Cause**: Domain not resolving correctly
   - **Fix**: Verify DNS with `nslookup`
   - **Cause**: Port 80 not accessible
   - **Fix**: Test `curl http://stg.bizoholic.com/.well-known/acme-challenge/test`

3. **Rate Limit Hit**
   - **Cause**: Too many certificate requests
   - **Fix**: Wait 1 week or use Let's Encrypt staging
   - **Temporary**: Use HTTP for testing

4. **Wrong Domain in Certificate**
   - **Cause**: SNI mismatch
   - **Fix**: Verify `Host` rule matches actual domain

### Path-Based Routing Not Working

**Symptoms**: `/login/` or `/admin/` routes return 404 or go to wrong application

**Diagnosis**:
```bash
# Test routing
curl -I https://stg.bizoholic.com/login/
curl -I https://stg.bizoholic.com/admin/

# Check Traefik routes
docker exec traefik traefik show routers
```

**Solutions**:

1. **Priority Issues**
   - **Cause**: Wrong router priority
   - **Fix**: Ensure path-based routes have priority=10
   - **Verify**: Main site has priority=1

2. **StripPrefix Middleware Not Working**
   - **Cause**: Middleware not applied or misconfigured
   - **Fix**: Verify middleware labels
   - **Test**: Check if `/login` is being stripped

3. **Application Not Handling Base Path**
   - **Cause**: Next.js app expects different base URL
   - **Fix**: Configure `basePath` in next.config.js if needed

### High Memory Usage

**Symptoms**: Container using > 500 MB memory or memory leak

**Diagnosis**:
```bash
# Monitor memory over time
docker stats bizoholic-frontend-3000

# Check memory limits
docker inspect bizoholic-frontend-3000 | grep Memory
```

**Solutions**:

1. **No Memory Limits Set**
   - **Fix**: Add memory limits to docker-compose.yml
   ```yaml
   deploy:
     resources:
       limits:
         memory: 512M
   ```

2. **Memory Leak**
   - **Cause**: Next.js development mode or webpack-dev-server
   - **Fix**: Ensure NODE_ENV=production in build
   - **Verify**: Check package.json build script

3. **Large Bundle Size**
   - **Cause**: Too many dependencies or large assets
   - **Fix**: Analyze bundle with `next build --analyze`
   - **Optimize**: Remove unused dependencies, compress images

### Slow Response Times

**Symptoms**: Page loads taking > 3 seconds

**Diagnosis**:
```bash
# Test response time
curl -o /dev/null -s -w "Time: %{time_total}s\n" https://stg.bizoholic.com

# Check container logs for slow queries
docker logs bizoholic-frontend-3000 | grep -i "slow\|timeout"
```

**Solutions**:

1. **Cold Start Delay**
   - **Expected**: First request after container start takes longer
   - **Normal**: 2-3 seconds for first request
   - **Improve**: Keep container running, don't restart frequently

2. **Backend API Slow**
   - **Cause**: Brain API or other backend service slow
   - **Fix**: Check backend performance
   - **Verify**: Test backend endpoints directly

3. **Large Asset Files**
   - **Cause**: Unoptimized images or large JavaScript bundles
   - **Fix**: Optimize images, enable compression
   - **Implement**: CDN for static assets

4. **No Caching**
   - **Cause**: Browser cache headers not set
   - **Fix**: Configure Next.js cache headers
   - **Implement**: Redis caching for API responses

### Cannot Connect to Backend API

**Symptoms**: Frontend shows API errors or cannot fetch data

**Diagnosis**:
```bash
# Test from inside frontend container
docker exec bizoholic-frontend-3000 curl http://bizosaas-brain-staging:8001/health

# Check network connectivity
docker exec bizoholic-frontend-3000 ping bizosaas-brain-staging

# Verify environment variable
docker exec bizoholic-frontend-3000 env | grep API_BASE_URL
```

**Solutions**:

1. **Wrong API URL**
   - **Cause**: NEXT_PUBLIC_API_BASE_URL points to wrong host
   - **Fix**: Should be `http://bizosaas-brain-staging:8001`
   - **Verify**: Check environment variables in Dokploy

2. **Network Isolation**
   - **Cause**: Frontend and backend on different Docker networks
   - **Fix**: Both must be on `bizosaas-network`
   - **Verify**: `docker network inspect bizosaas-network`

3. **Backend Not Running**
   - **Cause**: Brain API container stopped or crashed
   - **Fix**: Start backend services (Phase 2)
   - **Verify**: `docker ps | grep brain`

4. **CORS Issues**
   - **Cause**: Backend blocking frontend origin
   - **Fix**: Configure CORS in Brain API
   - **Allow**: `https://stg.bizoholic.com`

---

## Post-Deployment

### Comprehensive Testing Checklist

Run the full test suite:

```bash
cd /home/alagiri/projects/bizoholic
./test-frontend-applications.sh
```

**Test Categories** (8 suites):
1. Domain accessibility
2. SSL certificate validation
3. Path-based routing
4. API integration
5. Performance benchmarks
6. Resource usage
7. Error handling
8. User workflows

**Expected Results**: >95% pass rate

### Integration Testing

**Test End-to-End Workflows**:

1. **User Registration Flow**:
   - Visit https://stg.bizoholic.com
   - Click "Sign Up"
   - Fill registration form
   - Submit and verify account creation
   - Check email verification

2. **Client Portal Login**:
   - Visit https://stg.bizoholic.com/login/
   - Enter test credentials
   - Verify dashboard loads
   - Test navigation between sections

3. **Admin Functions**:
   - Visit https://stg.bizoholic.com/admin/
   - Login with admin credentials
   - Test user management
   - Test content management
   - Verify analytics dashboard

4. **E-commerce Flow** (CorelDove):
   - Visit https://stg.coreldove.com
   - Browse products
   - Add item to cart
   - Proceed to checkout
   - Test payment flow (test mode)

5. **Gaming Platform** (ThrillRing):
   - Visit https://stg.thrillring.com
   - Browse games
   - Test game launch
   - Verify user profile

### Monitoring Setup

**Configure Monitoring**:

1. **Container Health Monitoring**:
```bash
# Create health check cron job
crontab -e

# Add line:
*/5 * * * * /home/alagiri/projects/bizoholic/monitor-frontend-health.sh
```

2. **Resource Monitoring**:
```bash
# Install monitoring tools (if not already)
docker run -d \
  --name=cadvisor \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  google/cadvisor:latest
```

3. **Log Aggregation**:
```bash
# Set up log rotation
docker exec bizoholic-frontend-3000 logrotate /etc/logrotate.conf
```

### Performance Optimization

**Enable Performance Features**:

1. **Next.js Production Optimizations**:
   - Verify `NODE_ENV=production` set
   - Enable compression
   - Configure image optimization
   - Set up ISR (Incremental Static Regeneration)

2. **CDN Configuration** (Optional):
   - CloudFlare for static assets
   - Image CDN for Next.js images
   - CSS/JS bundle caching

3. **Database Query Optimization**:
   - Enable query caching
   - Add database indexes
   - Optimize N+1 queries

### Security Hardening

**Production Security Checklist**:

- [ ] All domains use HTTPS
- [ ] SSL certificates valid and auto-renewing
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] API rate limiting enabled
- [ ] CORS properly configured
- [ ] Environment variables secured
- [ ] No debug info exposed in production
- [ ] Regular security updates scheduled

**Configure Security Headers**:
```yaml
# Add to Traefik configuration
labels:
  - "traefik.http.middlewares.security-headers.headers.stsSeconds=31536000"
  - "traefik.http.middlewares.security-headers.headers.contentTypeNosniff=true"
  - "traefik.http.middlewares.security-headers.headers.browserXssFilter=true"
```

### Backup and Disaster Recovery

**Backup Strategy**:

1. **Container Images**:
```bash
# Backup Docker images
docker save bizoholic-frontend:latest | gzip > bizoholic-frontend-backup.tar.gz
```

2. **Configuration Files**:
```bash
# Backup compose files
cp dokploy-frontend-staging.yml /backup/
```

3. **Environment Variables**:
```bash
# Export environment variables
docker inspect bizoholic-frontend-3000 | jq '.[].Config.Env' > frontend-env-backup.json
```

**Rollback Plan**:
1. Stop current containers
2. Restore previous image version
3. Redeploy with previous configuration
4. Verify rollback successful

### Documentation Updates

**Update Documentation**:

1. **Deployment Diary**:
   - Record deployment date/time
   - Note any issues encountered
   - Document solutions applied
   - Record performance benchmarks

2. **Team Knowledge Base**:
   - Add common issues and solutions
   - Document custom configurations
   - Update runbooks

3. **User Documentation**:
   - Update API documentation
   - Create user guides for new features
   - Update changelog

### Handoff to Operations

**Operational Handoff Checklist**:

- [ ] All services running and healthy
- [ ] Monitoring configured and alerts set
- [ ] Backup procedures documented
- [ ] Runbook updated with troubleshooting steps
- [ ] Team trained on deployment process
- [ ] Support escalation path defined
- [ ] Performance baselines documented

**Handoff Meeting Agenda**:
1. Architecture overview
2. Deployment walkthrough
3. Monitoring dashboard review
4. Common issues and solutions
5. Emergency procedures
6. Q&A session

### Next Steps

**Production Migration Planning**:

1. **Performance Review**:
   - Analyze staging performance metrics
   - Identify optimization opportunities
   - Test under load

2. **Production Environment Preparation**:
   - Acquire production domains
   - Configure production DNS
   - Set up production monitoring
   - Configure production secrets

3. **Production Deployment**:
   - Use same deployment process
   - Different domain configuration
   - Production-grade resources
   - Enhanced monitoring

4. **Post-Production**:
   - Monitor for 72 hours
   - Gradual traffic migration
   - Performance tuning
   - User feedback collection

---

## Deployment Timeline

### Typical First Deployment
- **Preparation**: 15-20 minutes (DNS, prerequisites)
- **Dokploy Setup**: 5-10 minutes (project creation)
- **Deployment**: 12-18 minutes (builds + startup)
- **SSL Setup**: 5-10 minutes (certificate generation)
- **Verification**: 10-15 minutes (testing)
- **Total**: 50-70 minutes

### Experienced Team
- **Preparation**: 5 minutes
- **Deployment**: 15 minutes
- **Verification**: 5 minutes
- **Total**: 25-30 minutes

### With Issues
- **Troubleshooting**: +15-45 minutes
- **Retry**: +15 minutes
- **Total**: 80-130 minutes

---

## Success Criteria

**Deployment is successful when**:

- ✓ All 6 containers running with "Running" status
- ✓ All containers show "Healthy" health status
- ✓ All staging domains accessible via HTTPS
- ✓ SSL certificates valid on all domains
- ✓ Path-based routing working correctly
- ✓ Frontends successfully communicate with backend
- ✓ verify-frontend-deployment.sh passes 100%
- ✓ No critical errors in logs
- ✓ Response times within acceptable limits
- ✓ Resource usage within expected ranges

**Quality Gates**:
- ✓ test-frontend-applications.sh success rate >95%
- ✓ All integration tests passing
- ✓ Performance benchmarks met
- ✓ Security headers configured
- ✓ Monitoring active

**Production Readiness**:
- ✓ All success criteria met
- ✓ No blocking issues
- ✓ Performance acceptable under load
- ✓ Team trained on operations
- ✓ Documentation complete
- ✓ Backup/recovery tested

---

## Related Documentation

- **Phase 1**: `/home/alagiri/projects/bizoholic/INFRASTRUCTURE_DEPLOYMENT_STEPS.md`
- **Phase 2**: `/home/alagiri/projects/bizoholic/PHASE2_BACKEND_DEPLOYMENT.md`
- **Verification Script**: `/home/alagiri/projects/bizoholic/verify-frontend-deployment.sh`
- **Test Suite**: `/home/alagiri/projects/bizoholic/test-frontend-applications.sh`
- **Troubleshooting**: `/home/alagiri/projects/bizoholic/frontend-troubleshooting.md`
- **API Reference**: `/home/alagiri/projects/bizoholic/frontend-api-integration.md`
- **Quick Reference**: `/home/alagiri/projects/bizoholic/PHASE3_QUICK_REFERENCE.md`

---

**Frontend Deployment Guide - Ready for Production Staging Deployment**

**Last Updated**: October 10, 2025
**Version**: 1.0.0
**Phase**: 3 of 3 (Final Phase)
