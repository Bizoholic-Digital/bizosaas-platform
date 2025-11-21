# Client Portal - Dokploy Deployment Guide

**Date**: November 11, 2025
**Status**: Ready for Deployment
**Portal URL**: TBD (will be configured in Dokploy)

---

## Pre-Deployment Checklist

### ✅ Local Testing Complete

- [x] Dependencies installed successfully
- [x] Dev server running on http://localhost:3000
- [x] Portal loads without errors
- [x] All pages accessible (Dashboard, CRM, E-commerce, etc.)
- [x] Amazon sourcing module added
- [x] Navigation working correctly
- [x] Dark/light theme toggle functional

### ✅ Code Ready

- [x] All TypeScript files created
- [x] React hooks violations fixed
- [x] Build configuration validated
- [x] Environment variables documented

---

## Deployment Steps

### Step 1: Access Dokploy UI

1. Navigate to Dokploy dashboard (your server)
2. Log in with your credentials
3. Select the BizOSaaS project (or create new if needed)

### Step 2: Create New Application

1. Click **"New Application"** or **"Add Service"**
2. Select **"Docker"** as deployment type
3. Choose **"GitHub Repository"** as source

### Step 3: Configure Repository

**Repository Settings:**
```
Repository URL: https://github.com/YOUR_GITHUB_USERNAME/bizosaas-platform
Branch: main (or your deployment branch)
Build Context: /bizosaas-platform/frontend/apps/client-portal
Dockerfile: Dockerfile
```

### Step 4: Environment Variables

Add these environment variables in Dokploy UI:

#### Production Environment Variables

```bash
# Application Configuration
PORT=3000
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1

# API Configuration (Brain Gateway - when deployed)
NEXT_PUBLIC_API_BASE_URL=https://brain-gateway.bizoholic.com
NEXT_PUBLIC_BRAIN_API_URL=https://brain-gateway.bizoholic.com

# Feature Flags
NEXT_PUBLIC_ENABLE_SOURCING=true

# Amazon Sourcing Service
NEXT_PUBLIC_AMAZON_SOURCING_API_URL=http://backend-amazon-sourcing:8080

# Application Metadata
NEXT_PUBLIC_APP_NAME=BizOSaaS Client Portal
NEXT_PUBLIC_APP_VERSION=1.0.0
```

**Note**: Replace `brain-gateway.bizoholic.com` with your actual Brain Gateway URL when deployed.

### Step 5: Configure Build Settings

**Build Configuration:**
```
Build Command: npm run build
Start Command: npm run start
Port: 3000
```

**Docker Configuration** (if using custom Dockerfile):
- Ensure Dockerfile exists in the repository
- Dockerfile should use Node.js 18+ base image
- Multi-stage build recommended for smaller image size

### Step 6: Network Configuration

**Internal Network:**
- Ensure the service is on the same Docker network as:
  - `backend-amazon-sourcing` (Amazon sourcing service)
  - Brain Gateway (when deployed)
  - Database services

**External Access:**
- Configure domain/subdomain (e.g., `portal.bizoholic.com`)
- Enable HTTPS via Traefik (automatic with Dokploy)
- Set up SSL certificate (Let's Encrypt)

### Step 7: Deploy

1. Click **"Deploy"** button
2. Monitor build logs for any errors
3. Wait for deployment to complete (usually 3-5 minutes)

---

## Post-Deployment Verification

### Test 1: Portal Access

```bash
# Check if portal loads
curl https://portal.bizoholic.com

# Expected: HTML response with "Client Portal" title
```

### Test 2: Sourcing Page

```bash
# Check sourcing module
curl https://portal.bizoholic.com/sourcing

# Expected: HTML with "Amazon Product Sourcing" heading
```

### Test 3: API Connectivity

```bash
# From inside the container, test API access
docker exec <container-name> curl http://backend-amazon-sourcing:8080/health

# Expected: {"status": "healthy"}
```

### Test 4: Browser Testing

1. Open https://portal.bizoholic.com
2. Verify dashboard loads
3. Click on **"Product Sourcing"** in sidebar
4. Check that all sourcing pages are accessible:
   - `/sourcing` - Dashboard
   - `/sourcing/search` - Product search
   - `/sourcing/import` - Bulk import
   - `/sourcing/history` - Import history

---

## Troubleshooting

### Issue 1: Build Fails

**Error**: `npm install` fails or dependency conflicts

**Fix**:
```bash
# Add to build command in Dokploy
npm install --legacy-peer-deps && npm run build
```

### Issue 2: Portal Shows "Something went wrong"

**Error**: Next.js server-side rendering error

**Check**:
1. Verify environment variables are set correctly
2. Check that `NODE_ENV=production`
3. Review logs in Dokploy UI
4. Ensure API endpoints are accessible

### Issue 3: Can't Connect to Amazon Sourcing Service

**Error**: API calls to sourcing service fail

**Fix**:
1. Verify both services are on same Docker network
2. Check service name: `backend-amazon-sourcing`
3. Confirm sourcing service is running:
   ```bash
   docker service ls | grep amazon-sourcing
   ```

### Issue 4: Slow Initial Load

**Cause**: Large bundle size or slow cold start

**Fix**:
1. Enable Next.js optimization in `next.config.js`
2. Implement code splitting
3. Increase container resources in Dokploy

---

## Environment-Specific Configuration

### Development (Local)

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
NEXT_PUBLIC_AMAZON_SOURCING_API_URL=http://backend-amazon-sourcing:8080
NODE_ENV=development
```

### Staging

```bash
NEXT_PUBLIC_API_BASE_URL=https://staging-brain-gateway.bizoholic.com
NEXT_PUBLIC_AMAZON_SOURCING_API_URL=http://backend-amazon-sourcing:8080
NODE_ENV=production
```

### Production

```bash
NEXT_PUBLIC_API_BASE_URL=https://brain-gateway.bizoholic.com
NEXT_PUBLIC_AMAZON_SOURCING_API_URL=http://backend-amazon-sourcing:8080
NODE_ENV=production
```

---

## Updating the Deployment

### Method 1: Via Dokploy UI (Recommended)

1. Go to Dokploy dashboard
2. Select Client Portal service
3. Click **"Redeploy"** or **"Deploy Latest"**
4. Monitor logs

### Method 2: Via Git Push

1. Push changes to GitHub:
   ```bash
   git add .
   git commit -m "Update client portal"
   git push origin main
   ```

2. Dokploy auto-deploys if webhook is configured
3. Or manually trigger deploy in Dokploy UI

---

## Monitoring and Logs

### View Live Logs

1. Dokploy UI → Client Portal service → **"Logs"** tab
2. Filter by severity: Info, Warning, Error

### Common Log Patterns

**Successful Start**:
```
✓ Ready in 2.5s
- Local: http://localhost:3000
```

**API Call**:
```
GET /api/v1/amazon/search 200 in 543ms
```

**Error**:
```
Error: Failed to connect to backend-amazon-sourcing:8080
```

---

## Scaling Configuration

### Horizontal Scaling

**Dokploy Settings**:
- Replicas: 2-3 (for high availability)
- Load balancer: Automatic via Traefik
- Session stickiness: Not required (stateless)

### Resource Limits

**Recommended**:
```
CPU: 0.5-1.0 cores
Memory: 512MB - 1GB
```

**For High Traffic**:
```
CPU: 2 cores
Memory: 2GB
Replicas: 3+
```

---

## Security Checklist

- [ ] HTTPS enabled (via Traefik/Let's Encrypt)
- [ ] Environment variables secured (not in code)
- [ ] CORS configured correctly
- [ ] Rate limiting enabled on API
- [ ] Authentication implemented
- [ ] No sensitive data in client-side code
- [ ] CSP headers configured
- [ ] XSS protection enabled

---

## Backup and Rollback

### Creating Backup

1. Dokploy UI → Client Portal → **"Settings"**
2. Click **"Create Snapshot"**
3. Name: `client-portal-backup-YYYY-MM-DD`

### Rolling Back

1. Dokploy UI → Client Portal → **"Deployments"**
2. Select previous successful deployment
3. Click **"Rollback to this version"**

---

## Support and Documentation

### Internal Documentation

- [CLIENT_PORTAL_LOCAL_SETUP_GUIDE.md](./CLIENT_PORTAL_LOCAL_SETUP_GUIDE.md) - Local development
- [CLIENT_PORTAL_FIX_SUMMARY.md](./CLIENT_PORTAL_FIX_SUMMARY.md) - Fixed issues
- [AMAZON_SOURCING_FINAL_RECOMMENDATION.md](/home/alagiri/projects/coreldove/AMAZON_SOURCING_FINAL_RECOMMENDATION.md) - Sourcing architecture

### External Resources

- [Next.js Deployment Docs](https://nextjs.org/docs/deployment)
- [Dokploy Documentation](https://docs.dokploy.com)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

## Quick Commands Reference

### Local Testing

```bash
# Install dependencies
npm install --legacy-peer-deps

# Run dev server
npm run dev

# Build for production
npm run build

# Run production build
npm run start

# Type check
npm run type-check

# Lint code
npm run lint
```

### Docker Commands (for debugging)

```bash
# List running containers
docker ps | grep client-portal

# View logs
docker logs <container-id> --tail 100 -f

# Execute commands in container
docker exec -it <container-id> sh

# Check environment variables
docker exec <container-id> env | grep NEXT_PUBLIC
```

---

## Success Criteria

Deployment is successful when:

- ✅ Portal loads at production URL
- ✅ All pages accessible without errors
- ✅ Sourcing module visible in sidebar
- ✅ API calls to Brain Gateway work
- ✅ Amazon sourcing service connected
- ✅ Dark/light theme toggle works
- ✅ No console errors in browser DevTools
- ✅ SSL certificate valid
- ✅ Response time < 2 seconds

---

## Next Steps After Deployment

1. **Test End-to-End Workflow**
   - Create test account
   - Navigate to Product Sourcing
   - Test product search
   - Verify import functionality

2. **Monitor Performance**
   - Check response times
   - Monitor error rates
   - Review resource usage

3. **Enable Additional Features**
   - Configure authentication
   - Set up billing integration
   - Enable usage tracking

4. **Marketing Launch**
   - Announce to beta users
   - Create documentation for customers
   - Set up support channels

---

**Deployment Status**: Ready
**Last Updated**: November 11, 2025
**Prepared By**: Claude AI Assistant
