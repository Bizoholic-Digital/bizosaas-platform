# 🚀 Dokploy Configuration for Bizoholic Frontend

**Service:** Bizoholic Frontend Microservice
**Image:** `ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:working-2025-10-30`
**Architecture:** Microservices + DDD with shared packages

---

## 📋 Dokploy UI Configuration

### 1. Basic Settings

```yaml
Application Name: bizoholic-frontend
Application Type: Docker Image
Docker Image: ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:working-2025-10-30
Registry Type: GitHub Container Registry (GHCR)
```

**Registry Authentication:**
```
Username: alagirirajesh (or bizoholic-digital)
Password/Token: YOUR_GITHUB_TOKEN_HERE
```

---

### 2. Environment Variables

Copy these into Dokploy Environment Variables section:

```env
# Core Configuration
NODE_ENV=production
PORT=3001
HOSTNAME=0.0.0.0
NEXT_TELEMETRY_DISABLED=1

# Brain Gateway Configuration
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://brain-gateway.automationhub-n8n-91feb0-194-238-16-237.traefik.me
BRAIN_GATEWAY_API_KEY=your_brain_gateway_api_key_here

# Wagtail CMS Configuration
WAGTAIL_API_BASE_URL=http://wagtail-cms:8000/api/v2
NEXT_PUBLIC_WAGTAIL_URL=https://cms.automationhub-n8n-91feb0-194-238-16-237.traefik.me

# Auth Service Configuration
AUTH_SERVICE_URL=http://auth-service:5000
NEXT_PUBLIC_AUTH_URL=https://auth.automationhub-n8n-91feb0-194-238-16-237.traefik.me

# Application Settings
NEXT_PUBLIC_API_URL=https://api.automationhub-n8n-91feb0-194-238-16-237.traefik.me
NEXT_PUBLIC_SITE_URL=https://bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me
```

---

### 3. Port Configuration

```yaml
Container Port: 3001
Host Port: Auto (let Dokploy assign) or 3001
Protocol: TCP
Expose Port: Yes
```

**Port Mapping:**
```
Container: 3001 → Host: [Auto or 3001]
```

---

### 4. Network Configuration

```yaml
Network: bizosaas-network
```

**If network doesn't exist, create it first:**
- Go to Networks section in Dokploy
- Create new network: `bizosaas-network`
- Type: Bridge
- Driver: default

**Connected Services (should be on same network):**
- wagtail-cms
- auth-service
- brain-gateway
- postgres (if local)
- redis (if local)

---

### 5. Domain Configuration

```yaml
Domain Type: Traefik
Domain: bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me
```

**Alternative domains (if available):**
```
Primary: bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me
Aliases:
  - www.bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me
```

**SSL/TLS:**
- Enable: Yes
- Certificate: Let's Encrypt (auto)
- Force HTTPS: Yes

---

### 6. Health Check Configuration

```yaml
Health Check Enabled: Yes
Health Check Path: /
Health Check Port: 3001
Health Check Interval: 30s
Health Check Timeout: 10s
Health Check Retries: 3
Health Check Start Period: 40s
```

**Health Check Command (if needed):**
```bash
curl -f http://localhost:3001/ || exit 1
```

---

### 7. Resource Limits

```yaml
Memory:
  Reservation: 256Mi
  Limit: 512Mi

CPU:
  Reservation: 0.2
  Limit: 0.5
```

**For production (recommended):**
```yaml
Replicas: 2 (for high availability)
```

---

### 8. Restart Policy

```yaml
Restart Policy: unless-stopped
Restart Max Attempts: 3
```

---

### 9. Logging Configuration

```yaml
Log Driver: json-file
Log Options:
  max-size: 10m
  max-file: 3
```

---

### 10. Volume Mounts (Optional)

**If you need persistent storage:**
```yaml
# None required for this stateless frontend
# All assets are in Docker image
```

---

## 🔐 Secrets Configuration

### If using Dokploy Secrets:

Create these secrets in Dokploy Secrets section:

```yaml
BRAIN_GATEWAY_API_KEY: <your_actual_api_key>
AUTH_SECRET: <generate_random_secret>
WAGTAIL_API_KEY: <if_needed>
```

Then reference in environment variables:
```env
BRAIN_GATEWAY_API_KEY=${SECRET:BRAIN_GATEWAY_API_KEY}
```

---

## 📝 Complete Dokploy Configuration JSON

**Copy this entire configuration:**

```json
{
  "name": "bizoholic-frontend",
  "type": "docker",
  "image": "ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:working-2025-10-30",
  "registry": {
    "type": "ghcr",
    "username": "alagirirajesh",
    "password": "YOUR_GITHUB_TOKEN_HERE"
  },
  "environment": {
    "NODE_ENV": "production",
    "PORT": "3001",
    "HOSTNAME": "0.0.0.0",
    "NEXT_TELEMETRY_DISABLED": "1",
    "NEXT_PUBLIC_BRAIN_GATEWAY_URL": "https://brain-gateway.automationhub-n8n-91feb0-194-238-16-237.traefik.me",
    "WAGTAIL_API_BASE_URL": "http://wagtail-cms:8000/api/v2",
    "AUTH_SERVICE_URL": "http://auth-service:5000",
    "NEXT_PUBLIC_SITE_URL": "https://bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me"
  },
  "ports": [
    {
      "containerPort": 3001,
      "hostPort": 3001,
      "protocol": "tcp"
    }
  ],
  "network": "bizosaas-network",
  "domains": [
    {
      "domain": "bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me",
      "ssl": true,
      "forceHttps": true
    }
  ],
  "healthCheck": {
    "enabled": true,
    "path": "/",
    "port": 3001,
    "interval": "30s",
    "timeout": "10s",
    "retries": 3,
    "startPeriod": "40s"
  },
  "resources": {
    "memory": {
      "reservation": "256Mi",
      "limit": "512Mi"
    },
    "cpu": {
      "reservation": "0.2",
      "limit": "0.5"
    }
  },
  "replicas": 2,
  "restartPolicy": "unless-stopped"
}
```

---

## 🚀 Deployment Steps in Dokploy UI

### Step 1: Create Application

1. Click **"+ New Application"**
2. Select **"Docker Image"**
3. Enter name: `bizoholic-frontend`

### Step 2: Configure Image

1. **Docker Image:** `ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:working-2025-10-30`
2. **Registry Type:** GitHub Container Registry
3. **Username:** `alagirirajesh`
4. **Password/Token:** `YOUR_GITHUB_TOKEN_HERE`

### Step 3: Add Environment Variables

Click **"Environment Variables"** and add all variables from section 2 above.

**Quick copy format:**
```
NODE_ENV=production
PORT=3001
HOSTNAME=0.0.0.0
NEXT_TELEMETRY_DISABLED=1
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://brain-gateway.automationhub-n8n-91feb0-194-238-16-237.traefik.me
WAGTAIL_API_BASE_URL=http://wagtail-cms:8000/api/v2
AUTH_SERVICE_URL=http://auth-service:5000
NEXT_PUBLIC_SITE_URL=https://bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me
```

### Step 4: Configure Port

1. **Container Port:** `3001`
2. **Protocol:** TCP
3. Click **"Add Port"**

### Step 5: Configure Network

1. Select **"Network"** tab
2. Choose or create: `bizosaas-network`
3. Save

### Step 6: Configure Domain

1. Click **"Domains"** tab
2. **Domain:** `bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me`
3. **Enable SSL:** Yes
4. **Force HTTPS:** Yes
5. Click **"Add Domain"**

### Step 7: Configure Health Check

1. Click **"Health Check"** tab
2. **Enable:** Yes
3. **Path:** `/`
4. **Port:** `3001`
5. **Interval:** `30s`
6. **Timeout:** `10s`
7. **Retries:** `3`
8. Save

### Step 8: Configure Resources

1. Click **"Resources"** tab
2. **Memory Limit:** `512Mi`
3. **Memory Reservation:** `256Mi`
4. **CPU Limit:** `0.5`
5. **CPU Reservation:** `0.2`
6. **Replicas:** `2` (for HA)
7. Save

### Step 9: Review Configuration

Review all settings:
- ✅ Image configured
- ✅ Registry authenticated
- ✅ Environment variables set
- ✅ Port mapped
- ✅ Network configured
- ✅ Domain configured
- ✅ Health check enabled
- ✅ Resources set

### Step 10: Deploy

1. Click **"Deploy"** button
2. Monitor deployment logs
3. Wait for "Running" status
4. Check health status

---

## ✅ Post-Deployment Verification

### 1. Check Container Status

```bash
# In Dokploy UI
Go to Application → bizoholic-frontend → Status
Should show: "Running" (green)
```

### 2. Test Health Endpoint

```bash
curl https://bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me/
# Should return: HTML content
```

### 3. Check Logs

```bash
# In Dokploy UI
Go to Application → bizoholic-frontend → Logs
Should see:
  - ▲ Next.js 15.5.3
  - ✓ Ready in Xms
  - No errors
```

### 4. Verify All Routes

```bash
# Homepage
curl https://bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me/

# Login page
curl https://bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me/login

# Should both return HTML
```

### 5. Test Performance

```bash
# Response time
time curl https://bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me/
# Should be < 200ms
```

---

## 🔧 Troubleshooting

### Issue: Container Not Starting

**Check:**
1. Pull logs from Dokploy
2. Verify environment variables
3. Check port 3001 not in use
4. Verify network exists

**Solution:**
```bash
# In Dokploy, check logs for specific error
# Common issues:
# - Missing environment variable
# - Port conflict
# - Network not found
```

### Issue: Cannot Pull Image

**Check:**
1. Registry credentials correct
2. Image exists in GHCR
3. Token has correct permissions

**Solution:**
```bash
# Verify image exists
docker pull ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:working-2025-10-30

# If fails, check token permissions
```

### Issue: Health Check Failing

**Check:**
1. Container actually running
2. Port 3001 accessible
3. Application started successfully

**Solution:**
```bash
# Check container logs
# Look for "Ready in Xms" message
# Increase health check timeout if needed
```

### Issue: Domain Not Resolving

**Check:**
1. Traefik running
2. Domain configured correctly
3. SSL certificate issued

**Solution:**
```bash
# Check Traefik logs
# Verify domain in Traefik dashboard
# Wait for SSL cert (can take 1-2 min)
```

---

## 📊 Expected Metrics

### After Successful Deployment

**Container Status:**
```
Status: Running
Health: Healthy
Uptime: > 0s
Memory: ~150-200 MB
CPU: < 5%
```

**Application Metrics:**
```
Response Time: < 100ms
Error Rate: 0%
Requests/sec: Variable
Active Connections: Variable
```

**Resource Usage:**
```
Memory: 150-200 MB (within 512 MB limit)
CPU: 0.1-0.2 (within 0.5 limit)
Network: Minimal
```

---

## 🎯 Success Criteria

- [x] Container status: Running
- [x] Health check: Passing
- [x] Domain: Accessible
- [x] SSL: Active
- [x] Homepage: Loads
- [x] Login page: Loads
- [x] No errors in logs
- [x] Performance: < 200ms
- [x] Memory: < 512 MB
- [x] CPU: < 0.5

---

## 📝 Notes

### Architecture

This deployment uses:
- ✅ Microservices architecture (independent service)
- ✅ DDD principles (bounded context)
- ✅ Shared packages from GitHub Packages
- ✅ Docker for containerization
- ✅ Traefik for routing
- ✅ Let's Encrypt for SSL

### Package Integration

The service uses these shared packages:
- @bizoholic-digital/auth@1.0.0
- @bizoholic-digital/ui-components@1.0.0
- @bizoholic-digital/api-client@1.0.0
- @bizoholic-digital/hooks@1.0.0
- @bizoholic-digital/utils@1.0.0
- @bizoholic-digital/animated-components@1.0.0

All packages are included in the Docker image (no runtime npm install needed).

---

## ✅ Ready to Deploy!

**You now have everything configured to deploy in Dokploy UI!**

Follow the steps above and you'll have Bizoholic frontend running with the new microservices architecture.

**Good luck! 🚀**

---

*Dokploy Configuration for Bizoholic Frontend Microservice*
*BizOSaaS Platform - Microservices + DDD Architecture*
