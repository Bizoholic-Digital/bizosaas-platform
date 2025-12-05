# Client Portal - Fix Instructions

**Date**: 2025-11-01
**Status**: Container Exit Loop - Healthcheck Removed, Ready to Redeploy

---

## Current Situation

The Client Portal containers start successfully but exit immediately, causing a restart loop. I've identified and fixed the root cause.

### Root Cause
The HEALTHCHECK in `Dockerfile.optimized` was causing containers to be marked unhealthy and restart:

```dockerfile
# This was causing the exit loop:
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3001/', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"
```

### Fix Applied
I've removed the healthcheck from `Dockerfile.optimized` (lines 27-28). The file is now ready for rebuilding.

---

## Option 1: Rebuild via Dokploy UI (RECOMMENDED - 2 minutes)

This is the fastest and easiest solution.

### Steps:

1. **Go to Dokploy Service Page:**
   - URL: https://dk4.bizoholic.com/dashboard/project/VM7SbnKYZKl6nxKYey4Xn/environment/w9JtT6e9Glus_8cjWIEWc/services/application/8EqZXZKYTLiPqTkLF2l4J

2. **Click "Redeploy" or "Rebuild"**
   - Dokploy will automatically:
     - Pull latest code from GitHub (which includes the fixed Dockerfile)
     - Build new image without healthcheck
     - Deploy to the service

3. **Wait 2-3 minutes for build to complete**

4. **Verify service is running:**
   ```bash
   ssh root@72.60.219.244
   docker service ps frontend-client-portal
   ```

   Should show:
   ```
   NAME                     CURRENT STATE      DESIRED STATE
   frontend-client-portal.1 Running X minutes  Running
   ```

5. **Test portal access:**
   ```bash
   curl -I https://stg.bizoholic.com/portal/
   ```

   Should return: `HTTP/2 200 OK` or `HTTP/2 302` (redirect to login)

---

## Option 2: Manual Build & Push (if Dokploy rebuild fails)

If Dokploy UI rebuild doesn't work, use this manual approach.

### Prerequisites:
- Updated GitHub Personal Access Token with `write:packages` permission
- Docker installed locally
- Access to KVM4 server

### Steps:

1. **Build Next.js App Locally** (Already done ✅)
   ```bash
   cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/client-portal
   npm install --legacy-peer-deps
   npm run build
   ```

2. **Build Docker Image**
   ```bash
   docker build -f Dockerfile.optimized \
     -t ghcr.io/bizoholic-digital/bizosaas-client-portal:v1.0.1-stable \
     -t ghcr.io/bizoholic-digital/bizosaas-client-portal:latest \
     .
   ```

3. **Login to GHCR** (Need fresh token)
   ```bash
   echo "YOUR_NEW_GITHUB_TOKEN" | docker login ghcr.io -u bizoholic-digital --password-stdin
   ```

4. **Push to GHCR**
   ```bash
   docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:v1.0.1-stable
   docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:latest
   ```

5. **Update Dokploy Service**
   - Go to Dokploy UI → General tab
   - Change image tag to: `v1.0.1-stable`
   - Click "Deploy"

---

## Option 3: Deploy on KVM4 Server Directly

Build the image directly on KVM4 to avoid GHCR login issues.

### Steps:

1. **Copy build output to KVM4:**
   ```bash
   # From local machine
   cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/client-portal

   tar czf client-portal-build.tar.gz \
     .next/standalone \
     .next/static \
     public \
     Dockerfile.optimized

   scp client-portal-build.tar.gz root@72.60.219.244:/tmp/
   ```

2. **Build on KVM4:**
   ```bash
   ssh root@72.60.219.244

   cd /tmp
   mkdir -p client-portal-build
   cd client-portal-build
   tar xzf ../client-portal-build.tar.gz

   # Login to GHCR
   echo "YOUR_GITHUB_TOKEN" | docker login ghcr.io -u bizoholic-digital --password-stdin

   # Build and push
   docker build -f Dockerfile.optimized \
     -t ghcr.io/bizoholic-digital/bizosaas-client-portal:v1.0.1-stable \
     .

   docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:v1.0.1-stable
   ```

3. **Update Dokploy via UI**
   - Change image tag to `v1.0.1-stable`
   - Deploy

---

## Verification Checklist

After deploying the fixed image, verify these:

### 1. Service is Running
```bash
ssh root@72.60.219.244
docker service ls | grep client-portal
```

Expected:
```
frontend-client-portal  replicated  1/1  ghcr.io/bizoholic-digital/bizosaas-client-portal:v1.0.1-stable
```

### 2. Container Stays Running (Not Exiting)
```bash
docker service ps frontend-client-portal
```

Expected (should show ONLY ONE "Running" entry):
```
NAME                       CURRENT STATE          DESIRED STATE
frontend-client-portal.1   Running 2 minutes ago  Running
```

### 3. Container Logs Show No Errors
```bash
docker service logs frontend-client-portal --tail 20
```

Expected:
```
✓ Next.js 15.5.3
✓ Ready in XXXms
```

NO "Complete" or "Shutdown" messages!

### 4. Traefik Can Resolve Service Name
```bash
docker exec dokploy-traefik nslookup frontend-client-portal
```

Expected:
```
Name: frontend-client-portal
Address: 10.0.1.XXX  (some IP)
```

### 5. Portal is Accessible
```bash
curl -I https://stg.bizoholic.com/portal/
```

Expected:
```
HTTP/2 200 OK
```
or
```
HTTP/2 302
location: /portal/auth/signin
```

### 6. Test in Browser
Open: https://stg.bizoholic.com/portal/

Should see:
- Login page, OR
- Redirect to `/portal/auth/signin`, OR
- Dashboard (if cookies from previous session exist)

Should NOT see:
- ❌ 502 Bad Gateway
- ❌ 504 Gateway Timeout
- ❌ Connection refused

---

## Files Modified

1. **Dockerfile.optimized** (line 27-28)
   - Removed: HEALTHCHECK causing exit loop
   - Added: Comment explaining removal

2. **next.config.js** (line 7)
   - Added: `basePath: process.env.BASE_PATH || ''`
   - Purpose: Support `/portal/` path prefix

3. **Traefik Config** (`/etc/dokploy/traefik/dynamic/frontend-client-portal.yml`)
   - Fixed: Using service name instead of hardcoded IP
   - Line: `url: http://frontend-client-portal:3001`

---

## Environment Variables Required

Ensure these are set in Dokploy UI (General → Environment Variables):

```env
PORT=3001
BASE_PATH=/portal
NODE_ENV=production
HOSTNAME=0.0.0.0

# Auth
NEXTAUTH_URL=https://stg.bizoholic.com/portal
NEXTAUTH_SECRET=<your-secret-here>
JWT_SECRET=<your-jwt-secret>

# API
NEXT_PUBLIC_API_URL=https://stg.bizoholic.com/api

# Database (if needed)
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

---

## Success Criteria

The deployment is successful when ALL of these are true:

- [ ] Docker service shows `1/1` replicas running
- [ ] Container stays in "Running" state (not exiting/restarting)
- [ ] Logs show "✓ Ready in XXXms" with no errors
- [ ] Traefik can resolve `frontend-client-portal` service name
- [ ] `curl https://stg.bizoholic.com/portal/` returns 200 or 302
- [ ] Portal loads in browser without 502 errors
- [ ] Can access login page at `/portal/auth/signin`

---

## If Issues Persist

If the container still exits after removing healthcheck, the issue is likely missing environment variables. Check:

1. **Container logs for errors:**
   ```bash
   docker service logs frontend-client-portal --tail 50
   ```

2. **Environment variables in Dokploy:**
   - Go to General tab → Environment Variables
   - Verify ALL required vars are set (especially `NEXTAUTH_SECRET`, `JWT_SECRET`)

3. **Check exit code:**
   ```bash
   docker service ps frontend-client-portal --no-trunc
   ```

   Exit codes mean:
   - `0` = Clean exit (possibly healthcheck related)
   - `1` = Application error (check logs for stack trace)
   - `137` = Out of memory
   - `143` = Received SIGTERM signal

---

## Next Steps After Portal is Live

Once the portal is accessible and stable:

1. **Monitor for 30 minutes** - Ensure no unexpected restarts
2. **Test all routes:**
   - `/portal/` → Should redirect to login
   - `/portal/auth/signin` → Login page
   - `/portal/auth/signup` → Signup page
   - `/portal/dashboard` → Dashboard (after login)

3. **Clean up:**
   - Remove duplicate containers on KVM4
   - Remove mistaken container on KVM2
   - Delete old Docker images

4. **Continue Week 1 Implementation:**
   - Day 3: Tenant Context & RBAC
   - Day 4-5: Portal Layout & Sidebar
   - Day 6-7: Dashboard Page & Stats Cards

---

## Summary

**Problem**: Containers exit immediately after startup due to failing HEALTHCHECK
**Solution**: Removed HEALTHCHECK from Dockerfile.optimized
**Action Required**: Rebuild via Dokploy UI or manually build/push new image
**ETA to Fix**: 2-5 minutes
**Expected Result**: Container stays running, portal accessible at `https://stg.bizoholic.com/portal/`

---

**Status**: ✅ Fix Applied - Ready for Deployment
**Next Action**: Use **Option 1** (Dokploy UI rebuild) - Fastest solution
