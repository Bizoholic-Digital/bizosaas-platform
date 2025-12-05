# ✅ CORRECTED Dokploy Configuration - Bizoholic Frontend

**Domain:** `stg.bizoholic.com` (NOT automationhub)
**Image:** `ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:working-2025-10-30`
**Status:** Ready to deploy

---

## 🔧 Configuration Issues Found & Fixed

### ❌ WRONG Configuration:
```
Domain: bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me
Environment: References to automationhub URLs
Port Target: 3000 (incorrect)
```

### ✅ CORRECT Configuration:
```
Domain: stg.bizoholic.com
Environment: Proper backend URLs
Port Target: 3001 (matches container)
```

---

## 📋 CORRECT Dokploy Configuration

### 1. Basic Settings
```yaml
Name: bizoholic-frontend
Type: Docker Image
Image: ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:working-2025-10-30
Registry: GHCR
Username: alagirirajesh
Token: <from credentials.md>
```

### 2. Environment Variables (CORRECTED)

**Remove all automationhub references. Use these:**

```env
NODE_ENV=production
PORT=3001
HOSTNAME=0.0.0.0
NEXT_TELEMETRY_DISABLED=1

# Brain Gateway - Use your actual brain gateway URL
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://backend-brain-gateway:8001
NEXT_PUBLIC_API_GATEWAY_URL=http://backend-brain-gateway:8001
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001/api
NEXT_PUBLIC_AUTH_URL=http://backend-brain-gateway:8001/auth

# Wagtail CMS
NEXT_PUBLIC_CMS_URL=http://backend-brain-gateway:8001/cms
WAGTAIL_API_BASE_URL=http://backend-wagtail-cms:8000/api/v2

# Other Services
NEXT_PUBLIC_WIZARDS_URL=http://backend-brain-gateway:8001/wizards
NEXT_PUBLIC_AGENTS_URL=http://backend-brain-gateway:8001/agents
NEXT_PUBLIC_SOCIAL_API_URL=http://backend-brain-gateway:8001/social-media
NEXT_PUBLIC_COMM_API_URL=http://backend-brain-gateway:8001/communications
NEXT_PUBLIC_CRM_URL=http://backend-brain-gateway:8001/crm
NEXT_PUBLIC_COMMERCE_URL=http://backend-brain-gateway:8001/commerce

# Site URL - Your staging domain
NEXT_PUBLIC_SITE_URL=https://stg.bizoholic.com
```

### 3. Port Configuration (CORRECTED)

```yaml
Published Port: 3001
Published Port Mode: INGRESS
Target Port: 3001  ⚠️ CHANGE FROM 3000 to 3001
Protocol: TCP
```

**IMPORTANT:** The container listens on port 3001, not 3000!

### 4. Network
```yaml
Network: bizosaas-network
```

### 5. Domain (CORRECTED)

```yaml
Domain: stg.bizoholic.com
SSL: Yes
Force HTTPS: Yes
Certificate: Let's Encrypt (auto)
```

**DNS Requirement:**
Make sure `stg.bizoholic.com` points to `194.238.16.237`

### 6. Health Check
```yaml
Enabled: Yes
Path: /
Port: 3001  ⚠️ Use 3001, not 3000
Interval: 30s
Timeout: 10s
Retries: 3
Start Period: 40s
```

### 7. Resources
```yaml
Memory:
  Reservation: 256Mi
  Limit: 512Mi
CPU:
  Reservation: 0.2
  Limit: 0.5
Replicas: 1  (start with 1, scale to 2 after verified)
Restart Policy: unless-stopped
```

---

## 🔍 Configuration Review

### What Changed:

| Setting | Old (Wrong) | New (Correct) |
|---------|-------------|---------------|
| **Domain** | automationhub-n8n-... | stg.bizoholic.com |
| **Target Port** | 3000 | 3001 |
| **NEXT_PUBLIC_SITE_URL** | automationhub URL | https://stg.bizoholic.com |
| **Gateway URLs** | Mixed | All backend-brain-gateway:8001 |
| **Replicas** | 2 | 1 (start) |

### Why These Changes:

1. **Domain:** You have `stg.bizoholic.com` configured, no need for automationhub
2. **Port:** The container exposes port 3001, not 3000
3. **URLs:** Should point to your existing backend services
4. **Replicas:** Start with 1 to verify, then scale to 2

---

## ✅ Pre-Deployment Checklist

Before deploying, verify:

### DNS Configuration
```bash
# Check DNS points to Dokploy server
dig stg.bizoholic.com

# Should return: 194.238.16.237
```

### Backend Services Running
```bash
# Check brain-gateway is accessible
curl http://backend-brain-gateway:8001/health

# Or check in Dokploy UI that backend services are running
```

### Port 3001 Available
```bash
# Make sure port 3001 is not already in use
netstat -tuln | grep 3001
# Should be empty or show only dokploy listeners
```

### Network Exists
```bash
# Verify bizosaas-network exists in Dokploy
# Go to Networks tab in Dokploy UI
```

---

## 🚀 Deployment Steps

### Step 1: Update Configuration in Dokploy

1. Go to **bizoholic-frontend** application in Dokploy
2. Click **"Edit"** or **"Settings"**

### Step 2: Update Image
```
Image: ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:working-2025-10-30
```
✅ Already updated by you

### Step 3: Update Environment Variables

**Delete all old automationhub environment variables**

**Add these (copy entire block):**
```
NODE_ENV=production
PORT=3001
HOSTNAME=0.0.0.0
NEXT_TELEMETRY_DISABLED=1
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://backend-brain-gateway:8001
NEXT_PUBLIC_API_GATEWAY_URL=http://backend-brain-gateway:8001
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001/api
NEXT_PUBLIC_AUTH_URL=http://backend-brain-gateway:8001/auth
NEXT_PUBLIC_CMS_URL=http://backend-brain-gateway:8001/cms
WAGTAIL_API_BASE_URL=http://backend-wagtail-cms:8000/api/v2
NEXT_PUBLIC_WIZARDS_URL=http://backend-brain-gateway:8001/wizards
NEXT_PUBLIC_AGENTS_URL=http://backend-brain-gateway:8001/agents
NEXT_PUBLIC_SOCIAL_API_URL=http://backend-brain-gateway:8001/social-media
NEXT_PUBLIC_COMM_API_URL=http://backend-brain-gateway:8001/communications
NEXT_PUBLIC_CRM_URL=http://backend-brain-gateway:8001/crm
NEXT_PUBLIC_COMMERCE_URL=http://backend-brain-gateway:8001/commerce
NEXT_PUBLIC_SITE_URL=https://stg.bizoholic.com
```

### Step 4: Fix Port Configuration

**Current (Wrong):**
```
Target Port: 3000
```

**Change to:**
```
Target Port: 3001
```

### Step 5: Update Domain

**Current (Wrong):**
```
Domain: bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me
```

**Change to:**
```
Domain: stg.bizoholic.com
```

### Step 6: Update Health Check Port

```
Health Check Port: 3001 (not 3000)
```

### Step 7: Save Configuration

Click **"Save"** or **"Update"**

### Step 8: Deploy

Click **"Deploy"** or **"Redeploy"**

---

## 📊 Expected Deployment Process

### What Will Happen:

```
1. Dokploy pulls image from GHCR
   → ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:working-2025-10-30

2. Creates container with:
   → Port 3001 exposed
   → Environment variables set
   → Connected to bizosaas-network

3. Traefik configures routing:
   → stg.bizoholic.com → container:3001
   → Requests SSL cert from Let's Encrypt
   → Enables HTTPS

4. Health check starts:
   → Checks http://container:3001/
   → Waits for "Ready" status

5. Container becomes "Running"
   → Service accessible at https://stg.bizoholic.com
```

### Timeline:
```
0:00 - Pull image (30s-1min)
0:30 - Start container (10s)
0:40 - Configure Traefik (10s)
0:50 - Request SSL cert (30s-2min)
2:00 - Health checks pass (30s)
2:30 - Status: RUNNING ✅
```

---

## ✅ Post-Deployment Verification

### 1. Check Container Status
```bash
# In Dokploy UI
Application → bizoholic-frontend → Status
Should show: "Running" (green)
```

### 2. Check Logs
```bash
# In Dokploy UI → Logs
Look for:
  ▲ Next.js 15.5.3
  ✓ Ready in Xms
  - Local: http://0.0.0.0:3001
```

### 3. Test Domain
```bash
# Test from your machine
curl https://stg.bizoholic.com/

# Should return HTML content (not error)
```

### 4. Test in Browser
```
Open: https://stg.bizoholic.com/
Should see: Bizoholic homepage

Open: https://stg.bizoholic.com/login
Should see: Login page
```

### 5. Check SSL Certificate
```bash
# Verify SSL is working
curl -I https://stg.bizoholic.com/

# Should return:
# HTTP/2 200
# (no SSL errors)
```

---

## 🔧 Troubleshooting

### Issue: Container Won't Start

**Check:**
```bash
# In Dokploy logs, look for:
# - Port 3001 already in use
# - Environment variable errors
# - Image pull errors
```

**Solution:**
```bash
# Stop any conflicting containers
# Verify all environment variables are set
# Check registry credentials
```

### Issue: Domain Not Accessible

**Check:**
```bash
# Verify DNS
dig stg.bizoholic.com
# Should return: 194.238.16.237

# Check Traefik
# Go to Traefik dashboard in Dokploy
# Verify stg.bizoholic.com route exists
```

**Solution:**
```bash
# Wait 1-2 minutes for SSL cert
# Check Traefik logs
# Verify domain in Dokploy settings
```

### Issue: 502 Bad Gateway

**Check:**
```bash
# Container might be running but not ready
# Check health check status
# Verify port 3001 is open in container
```

**Solution:**
```bash
# Wait for health checks to pass
# Check container logs for startup errors
# Increase health check timeout if needed
```

---

## 📝 Configuration Summary

### Final Configuration:

```yaml
Application:
  Name: bizoholic-frontend
  Image: ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:working-2025-10-30
  Status: Ready to deploy

Network:
  Domain: stg.bizoholic.com
  Port: 3001 (internal and external)
  SSL: Yes (Let's Encrypt)
  Network: bizosaas-network

Environment:
  Backend: backend-brain-gateway:8001
  CMS: backend-wagtail-cms:8000
  Domain: stg.bizoholic.com

Resources:
  Memory: 256Mi-512Mi
  CPU: 0.2-0.5
  Replicas: 1 (scale to 2 later)
```

---

## ✅ READY TO DEPLOY

**Current Status:**
- ✅ Image updated to working-2025-10-30
- ✅ Correct domain: stg.bizoholic.com
- ⚠️ Need to fix: Target Port (3000 → 3001)
- ⚠️ Need to update: Environment variables (remove automationhub)

**Action Required:**
1. Fix Target Port to 3001
2. Update environment variables (copy from above)
3. Update domain to stg.bizoholic.com
4. Click Deploy

**After these fixes, you can deploy!** 🚀

---

*Corrected Dokploy Configuration for Bizoholic Frontend*
*Using proper domain and backend services*
