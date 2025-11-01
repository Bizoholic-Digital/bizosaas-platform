# 502 Bad Gateway - Diagnostic Checklist

## Current Configuration (You Provided)

**Traefik Config**: ✅ Port 3001 configured correctly
```yaml
services:
  frontend-client-portal-service-3:
    loadBalancer:
      servers:
        - url: http://frontend-client-portal:3001  # ✅ CORRECT
```

**Port Config**: ✅ Configured correctly
```
Published Port: 3002
Target Port: 3001
```

## Possible Root Causes for 502 Bad Gateway

Since the Traefik port (3001) is now correct, the 502 error indicates one of these issues:

### 1. ❌ Container Not Running or Crashed
**Symptom**: Container exists but is not in "running" state

**Check in Dokploy UI**:
- Go to your service page
- Look for container status (should show green "Running")
- If status is "Exited" or "Crashed", check logs

### 2. ❌ Container Can't Start - Missing Environment Variables
**Symptom**: Container starts then immediately crashes

**Required Environment Variables**:
```bash
# CRITICAL - Must be set:
PORT=3001
NODE_ENV=production

# Authentication (will crash without these):
JWT_SECRET=<generate with: openssl rand -base64 32>
NEXTAUTH_SECRET=<generate with: openssl rand -base64 32>
NEXTAUTH_URL=https://stg.bizoholic.com/portal

# Optional but recommended:
BASE_PATH=/portal
NEXT_PUBLIC_BASE_PATH=/portal
NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/portal
```

**Action**: Check Dokploy Environment Tab and ensure all required vars are set

### 3. ❌ Container Network Issue - Wrong Docker Network
**Symptom**: Traefik can't reach container via Docker network

**Possible causes**:
- Container is on different Docker network than Traefik
- Container name doesn't match Traefik service URL

**Check**:
- Container name should be: `frontend-client-portal`
- Container should be on same Docker network as Traefik (usually `dokploy-network`)

### 4. ❌ Missing Path Stripping Middleware
**Symptom**: Container receives `/portal/` prefix which Next.js doesn't recognize

**Your Current Config**:
```yaml
middlewares: []  # ❌ Empty!
```

**Should Be**:
```yaml
middlewares:
  - portal-stripprefix  # Need this!
```

**Action**: Add this middleware definition and attach it to the router

### 5. ❌ Health Check Failing
**Symptom**: Container is running but fails health checks

**Check**: Look for health check configuration and ensure it's correct

### 6. ❌ Application Error on Startup
**Symptom**: Next.js starts but crashes immediately

**Common causes**:
- Missing dependencies
- Database connection failure (if configured)
- API endpoint unreachable
- Invalid configuration

**Action**: Check container logs for error messages

---

## Step-by-Step Diagnosis

### Step 1: Check Container Status in Dokploy UI

Go to: https://dk4.bizoholic.com/dashboard/project/VM7SbnKYZKl6nxKYey4Xn/environment/w9JtT6e9Glus_8cjWIEWc/services/application/8EqZXZKYTLiPqTkLF2l4J

**Look for**:
- Container Status: Should show "Running" (green)
- If "Exited" or "Crashed": Read logs for error
- If "Restarting": Container is crash-looping

### Step 2: Check Container Logs

In Dokploy UI, click "Logs" tab

**What to Look For**:

✅ **Successful Start** (you should see):
```
▲ Next.js 15.5.3
- Local:        http://localhost:3001
- Environment:  production

✓ Ready in 2.3s
```

❌ **Error Patterns**:

**Missing Environment Variable**:
```
Error: NEXTAUTH_SECRET must be provided
Error: JWT_SECRET is required
```
**Fix**: Add missing environment variables

**Port Already in Use**:
```
Error: listen EADDRINUSE: address already in use :::3001
```
**Fix**: Change PORT environment variable or restart container

**File Not Found**:
```
Error: Cannot find module '/app/server.js'
```
**Fix**: Redeploy with correct Docker image

**Database Connection Failed**:
```
Error: Connection refused to database
```
**Fix**: Check DATABASE_URL or remove if not needed

### Step 3: Check Environment Variables

In Dokploy UI, go to "Environment" tab

**Verify these are set**:
- [ ] `PORT=3001`
- [ ] `NODE_ENV=production`
- [ ] `JWT_SECRET=<random-string-32-chars>`
- [ ] `NEXTAUTH_SECRET=<random-string-32-chars>`
- [ ] `NEXTAUTH_URL=https://stg.bizoholic.com/portal`

**Optional (for path-based routing)**:
- [ ] `BASE_PATH=/portal`
- [ ] `NEXT_PUBLIC_BASE_PATH=/portal`

### Step 4: Add Missing Middleware

Your Traefik config is missing the path stripping middleware.

**Current (WRONG)**:
```yaml
frontend-client-portal-router-websecure-3:
  middlewares: []  # ❌ Empty!
```

**Should Be (CORRECT)**:
```yaml
http:
  middlewares:
    portal-stripprefix:
      stripPrefix:
        prefixes:
          - /portal

  routers:
    frontend-client-portal-router-websecure-3:
      rule: Host(`stg.bizoholic.com`) && PathPrefix(`/portal`)
      service: frontend-client-portal-service-3
      middlewares:
        - portal-stripprefix  # ✅ Add this!
      entryPoints:
        - websecure
      tls:
        certResolver: letsencrypt
```

**Why This Matters**:
- User requests: `https://stg.bizoholic.com/portal/`
- Without middleware: Container receives `/portal/`
- Next.js doesn't have `/portal/` route → 404 or crashes
- With middleware: Container receives `/` → Works! ✅

### Step 5: Verify Docker Network

The container must be on the same Docker network as Traefik.

**Check in Dokploy**:
- Look for network configuration
- Should be: `dokploy-network` or similar
- Traefik should be on same network

### Step 6: Test Container Directly

If you have SSH access to the server, test container directly:

```bash
# Find container ID
docker ps | grep portal

# Test container internally
docker exec <container-id> curl -I http://localhost:3001

# Expected output: HTTP/1.1 200 OK
```

---

## Most Likely Issues (In Order)

Based on typical deployment issues:

### 1. Missing Path Stripping Middleware (90% likelihood)
**Fix**: Add `portal-stripprefix` middleware to Traefik config

### 2. Missing Environment Variables (80% likelihood)
**Fix**: Add `JWT_SECRET`, `NEXTAUTH_SECRET`, `NEXTAUTH_URL`

### 3. Container Crash Loop (70% likelihood)
**Fix**: Check logs, fix environment variables or configuration

### 4. Wrong Container Name (50% likelihood)
**Fix**: Ensure container name is `frontend-client-portal` exactly

---

## Quick Fix Checklist

Do these in order:

1. **Check Container Status** in Dokploy UI
   - [ ] Is it running? (Green status)
   - [ ] If not, check logs for errors

2. **Add Required Environment Variables**
   - [ ] `PORT=3001`
   - [ ] `JWT_SECRET=<generate>`
   - [ ] `NEXTAUTH_SECRET=<generate>`
   - [ ] `NEXTAUTH_URL=https://stg.bizoholic.com/portal`

3. **Add Path Stripping Middleware**
   - [ ] Define `portal-stripprefix` middleware
   - [ ] Attach to both HTTP and HTTPS routers

4. **Restart Container**
   - [ ] Click "Redeploy" or "Restart" in Dokploy UI

5. **Check Logs Again**
   - [ ] Should see "Ready in X.Xs"

6. **Test Access**
   - [ ] `curl -I https://stg.bizoholic.com/portal/`
   - [ ] Should return HTTP 200 OK

---

## What to Report Back

Please check these and report back:

1. **Container Status**: Running / Exited / Crashed / Restarting?
2. **Container Logs**: Any errors? (copy/paste last 20 lines)
3. **Environment Variables**: Are JWT_SECRET and NEXTAUTH_SECRET set?
4. **Traefik Middleware**: Is `portal-stripprefix` middleware defined and attached?

---

## Generate Required Secrets

If environment variables are missing, generate them:

```bash
# Generate JWT_SECRET
openssl rand -base64 32

# Generate NEXTAUTH_SECRET
openssl rand -base64 32
```

Then add these to Dokploy Environment tab.

---

## Summary

**Configuration**: ✅ Traefik port is correct (3001)
**Issue**: ❌ 502 Bad Gateway indicates container problem

**Most Likely Causes**:
1. Missing path stripping middleware
2. Missing required environment variables (JWT_SECRET, NEXTAUTH_SECRET)
3. Container not running or crash-looping

**Next Action**: Check container logs in Dokploy UI to see exact error
