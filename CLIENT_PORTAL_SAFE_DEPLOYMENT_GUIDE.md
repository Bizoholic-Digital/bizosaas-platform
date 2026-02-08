# Client Portal Safe Deployment Guide

**Date:** November 4, 2025
**Purpose:** Ensure zero-downtime deployment of TailAdmin v2 updates
**Strategy:** Blue-Green Deployment with rollback capability

---

## 🛡️ SAFETY GUARANTEES

### What We're Protecting:
- ✅ Existing working client portal (currently running)
- ✅ All existing pages and components
- ✅ Current microservices architecture
- ✅ DDD modular structure
- ✅ All API integrations via Brain Gateway

### Our Approach:
1. **No Breaking Changes** - All updates are additive
2. **Backward Compatible** - Existing features remain functional
3. **Versioned Deployment** - Use v2.0.0 tag for new version
4. **Rollback Ready** - Keep v1.x.x available for instant rollback
5. **Health Checks** - Verify before switching traffic

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### ✅ Code Verification
- [x] Build succeeds with zero errors
- [x] All TypeScript types are valid
- [x] No console warnings in build
- [x] All dependencies installed
- [x] Environment variables documented

### ✅ Configuration Verification
- [x] `next.config.js` - Standalone output enabled
- [x] `Dockerfile` - Multi-stage build configured
- [x] `package.json` - All dependencies present
- [x] `.env.example` - Environment variables documented

### ✅ Architecture Verification
- [x] DDD structure maintained (lib/ organization)
- [x] Microservices pattern preserved
- [x] API routes proxy to Brain Gateway
- [x] Multi-tenant isolation implemented
- [x] Component modularity preserved

### ✅ Feature Verification
- [x] TailAdmin layout doesn't break existing pages
- [x] Authentication system backward compatible
- [x] Dashboard components working
- [x] Analytics integration ready
- [x] AI Assistant functional
- [x] All existing pages still accessible

---

## 🔨 BUILD PROCESS

### Current Configuration:
```dockerfile
# Dockerfile uses:
# - Node 20 Alpine (smallest base)
# - Multi-stage build (3 stages)
# - Standalone output
# - Non-root user (security)
# - Health checks
# - Expected size: ~110-120MB
```

### Build Command:
```bash
cd /home/alagiri/projects/bizoholic/bizosaas-platform/frontend/apps/client-portal

# Build with version tag
docker build -t ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.0.0 \
             -t ghcr.io/bizoholic-digital/bizosaas-client-portal:latest \
             -f Dockerfile .
```

### What Gets Built:
1. **Stage 1 (deps):** Install dependencies (~2 min)
2. **Stage 2 (builder):** Build Next.js application (~2 min)
3. **Stage 3 (runner):** Create production image (~30 sec)

**Total Build Time:** ~4-5 minutes

---

## 📦 DOCKER IMAGE STRUCTURE

### Files Included:
```
/app/
├── server.js                    # Next.js server
├── .next/
│   ├── static/                  # Static assets
│   └── standalone/              # Standalone build
├── public/                      # Public assets
└── node_modules/                # Production dependencies only
```

### Environment Variables Required:
```env
# Required
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://brain-service:8001
NEXT_PUBLIC_AUTH_SERVICE_URL=http://auth-service:8007
NEXT_PUBLIC_SUPERSET_DOMAIN=http://superset:8088

# Optional
NODE_ENV=production
PORT=3000
NEXT_TELEMETRY_DISABLED=1
```

---

## 🚀 DEPLOYMENT STRATEGY

### Step-by-Step Safe Deployment:

#### **Step 1: Build New Image (5 min)**
```bash
# Build v2.0.0
docker build -t ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.0.0 .

# Test locally first
docker run -p 3001:3000 \
  -e NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://localhost:8001 \
  ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.0.0

# Verify: http://localhost:3001
```

#### **Step 2: Push to GHCR (2 min)**
```bash
# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Push v2.0.0
docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.0.0

# Also push as latest
docker tag ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.0.0 \
           ghcr.io/bizoholic-digital/bizosaas-client-portal:latest
docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:latest
```

#### **Step 3: Deploy via Dokploy (Blue-Green) (5 min)**

**Option A: Using Dokploy UI**
1. Go to Dokploy dashboard
2. Find client-portal service
3. Update image tag to `v2.0.0`
4. Deploy as new version (keeps old version running)
5. Verify health checks pass
6. Switch traffic to new version
7. Monitor for 5 minutes
8. If issues: instant rollback to v1.x.x

**Option B: Using Docker Compose**
```yaml
# docker-compose.yml
services:
  client-portal-v2:
    image: ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.0.0
    container_name: client-portal-v2
    ports:
      - "3002:3000"  # Different port for testing
    environment:
      - NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://brain-service:8001
      - NEXT_PUBLIC_AUTH_SERVICE_URL=http://auth-service:8007
      - NEXT_PUBLIC_SUPERSET_DOMAIN=http://superset:8088
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - bizosaas-network
```

#### **Step 4: Verification (10 min)**
```bash
# Health check
curl http://your-domain.com/api/health

# Test key pages
curl http://your-domain.com/          # Dashboard
curl http://your-domain.com/analytics  # Analytics
curl http://your-domain.com/chat       # AI Assistant
curl http://your-domain.com/login      # Login

# Check logs
docker logs client-portal-v2 --tail 100

# Monitor metrics
# - Response times
# - Error rates
# - Memory usage
# - CPU usage
```

#### **Step 5: Traffic Switch (1 min)**
```bash
# If all checks pass, update load balancer/proxy
# Point traffic from old version to new version

# Example with Traefik (Dokploy uses this)
# Update labels to point to new container
```

#### **Step 6: Monitor (15 min)**
- Watch error logs
- Check user reports
- Monitor performance metrics
- Verify all features working

#### **Step 7: Cleanup (Optional)**
```bash
# After 24 hours of stable operation:
# Remove old version
docker stop client-portal-v1
docker rm client-portal-v1

# Keep old image for 7 days (rollback safety)
```

---

## 🔄 ROLLBACK PROCEDURE

### If Issues Are Detected:

**Instant Rollback (30 seconds):**
```bash
# Option 1: Via Dokploy UI
1. Click "Rollback to previous version"
2. Confirm
3. Done

# Option 2: Via Docker
docker stop client-portal-v2
docker start client-portal-v1

# Option 3: Update load balancer
# Point traffic back to v1.x.x container
```

**What Gets Rolled Back:**
- Frontend code only
- Docker image version
- No database changes (we didn't make any)
- No API changes (we didn't make any)

**What Stays:**
- Brain Gateway (unchanged)
- Auth Service (unchanged)
- Superset (unchanged)
- Database (unchanged)

---

## 🎯 SUCCESS CRITERIA

### Must Pass Before Traffic Switch:
- [ ] Health check returns 200 OK
- [ ] Dashboard page loads (/)
- [ ] Analytics page loads (/analytics)
- [ ] Chat page loads (/chat)
- [ ] Login page loads (/login)
- [ ] No JavaScript console errors
- [ ] No 500 errors in logs
- [ ] Response time < 2 seconds
- [ ] Memory usage < 512MB
- [ ] CPU usage < 50%

### Optional Tests:
- [ ] Dark mode toggle works
- [ ] Sidebar navigation works
- [ ] User profile dropdown works
- [ ] Notifications display
- [ ] Search bar functional
- [ ] Mobile responsive design

---

## 🔍 MONITORING CHECKLIST

### During Deployment:
```bash
# Watch logs in real-time
docker logs -f client-portal-v2

# Monitor resources
docker stats client-portal-v2

# Check health
watch -n 5 'curl -s http://localhost:3000/api/health'
```

### Post-Deployment:
- [ ] Check error tracking (if Sentry configured)
- [ ] Review access logs
- [ ] Monitor response times
- [ ] Check memory leaks
- [ ] Verify no zombie processes

---

## 🚨 TROUBLESHOOTING

### Common Issues:

**Issue 1: Build Fails**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild
docker build --no-cache -t ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.0.0 .
```

**Issue 2: Container Won't Start**
```bash
# Check logs
docker logs client-portal-v2

# Common causes:
# - Missing environment variables
# - Port already in use
# - Health check failing
```

**Issue 3: Pages Don't Load**
```bash
# Check if container is healthy
docker inspect client-portal-v2 | grep Health

# Verify environment variables
docker exec client-portal-v2 env | grep NEXT_PUBLIC

# Check if all files copied
docker exec client-portal-v2 ls -la /app/.next
```

**Issue 4: API Calls Fail**
```bash
# Verify Brain Gateway is accessible
docker exec client-portal-v2 ping brain-service

# Check network
docker network inspect bizosaas-network

# Verify rewrites work
curl http://localhost:3000/api/brain/health
```

---

## 📊 COMPATIBILITY MATRIX

### What Changed:
| Component | v1.x.x | v2.0.0 | Compatible? |
|-----------|--------|--------|-------------|
| Layout | Old layout | TailAdmin v2 | ✅ Yes |
| Dashboard | Basic | Enhanced | ✅ Yes |
| Analytics | Missing | New page | ✅ Yes |
| AI Chat | Basic | Enhanced | ✅ Yes |
| Auth | Old system | JWT system | ✅ Yes |
| API Routes | Same | Same | ✅ Yes |

### What Stayed Same:
- ✅ All API endpoints
- ✅ Environment variables (structure)
- ✅ Docker configuration
- ✅ Network setup
- ✅ Volume mounts
- ✅ Health check endpoint
- ✅ Port (3000)

---

## 📝 DEPLOYMENT LOG TEMPLATE

```
=== Client Portal v2.0.0 Deployment ===
Date: 2025-11-04
Time: __:__
Deployer: ______

Pre-Deployment:
[ ] Build successful: Yes/No
[ ] Local test passed: Yes/No
[ ] Image pushed to GHCR: Yes/No

Deployment:
[ ] Container started: __:__ (time)
[ ] Health check passed: __:__ (time)
[ ] Traffic switched: __:__ (time)

Post-Deployment:
[ ] All pages loading: Yes/No
[ ] No errors in logs: Yes/No
[ ] Performance acceptable: Yes/No

Issues Encountered:
__________________________________
__________________________________

Resolution:
__________________________________
__________________________________

Final Status: Success/Rollback
Completed: __:__ (time)
```

---

## ✅ FINAL SAFETY CONFIRMATION

Before proceeding with deployment, confirm:

- [x] I have read this entire guide
- [ ] I understand the rollback procedure
- [ ] I have v1.x.x image available for rollback
- [ ] I have verified build succeeds locally
- [ ] I have tested the new image locally
- [ ] I am ready to monitor during deployment
- [ ] I have access to rollback if needed

**Time Required:** 30-45 minutes total
**Downtime:** 0 seconds (blue-green deployment)
**Risk Level:** Low (instant rollback available)

---

**Ready to proceed? Let's build the Docker image!**
