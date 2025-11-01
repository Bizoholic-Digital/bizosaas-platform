# Client Portal Deployment Fix - Bad Gateway 502

## Issue Identified ✅

**Status**: Container deployed successfully ✅ | Getting 502 Bad Gateway ❌

**Root Cause**: Traefik is trying to connect to port 3002, but the container is listening on port 3001.

## Port Configuration Confusion

### Current (WRONG) Configuration:
```yaml
# Dokploy Ports:
Published Port: 3002    # Host-level port
Target Port: 3001       # Container internal port

# Traefik Service:
url: http://frontend-client-portal:3002  # ❌ WRONG! Using published port
```

### The Problem:

Traefik communicates with containers via **Docker's internal network**, not the host. The "Published Port" (3002) is only for accessing the container from the host machine directly (e.g., `http://localhost:3002`).

For **Traefik → Container** communication, use the **Target Port (3001)**.

## Correct Configuration

### ✅ Fixed Traefik Configuration:

```yaml
http:
  routers:
    frontend-client-portal-router-3:
      rule: Host(`stg.bizoholic.com`) && PathPrefix(`/portal`)
      service: frontend-client-portal-service-3
      middlewares:
        - redirect-to-https
        - portal-stripprefix  # ⚠️ IMPORTANT: Add this!
      entryPoints:
        - web

    frontend-client-portal-router-websecure-3:
      rule: Host(`stg.bizoholic.com`) && PathPrefix(`/portal`)
      service: frontend-client-portal-service-3
      middlewares:
        - portal-stripprefix  # ⚠️ IMPORTANT: Add this!
      entryPoints:
        - websecure
      tls:
        certResolver: letsencrypt

  services:
    frontend-client-portal-service-3:
      loadBalancer:
        servers:
          - url: http://frontend-client-portal:3001  # ✅ FIXED: Use Target Port
        passHostHeader: true

  middlewares:
    portal-stripprefix:  # ⚠️ IMPORTANT: Add this middleware!
      stripPrefix:
        prefixes:
          - /portal
```

## Required Changes in Dokploy

### Step 1: Fix Traefik Service URL

In the Dokploy UI, update the Traefik configuration:

**Change:**
```yaml
url: http://frontend-client-portal:3002
```

**To:**
```yaml
url: http://frontend-client-portal:3001
```

### Step 2: Add Path Stripping Middleware

The `/portal` prefix needs to be stripped before forwarding to Next.js.

**Add this middleware section:**
```yaml
http:
  middlewares:
    portal-stripprefix:
      stripPrefix:
        prefixes:
          - /portal
```

**Then add it to both routers:**
```yaml
middlewares:
  - portal-stripprefix
```

### Step 3: Verify Environment Variables

Make sure these are set in the Environment Tab:

```bash
# Required for path-based routing
BASE_PATH=/portal
NEXT_PUBLIC_BASE_PATH=/portal
NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/portal

# Port configuration
PORT=3001
NODE_ENV=production

# Authentication (generate with: openssl rand -base64 32)
JWT_SECRET=your-jwt-secret-here
NEXTAUTH_SECRET=your-nextauth-secret-here
NEXTAUTH_URL=https://stg.bizoholic.com/portal

# Database (if needed)
DATABASE_URL=postgresql://user:password@host:5432/database

# Brain Gateway API
NEXT_PUBLIC_API_BASE_URL=https://api.bizoholic.com
BRAIN_GATEWAY_API_URL=https://api.bizoholic.com
BRAIN_GATEWAY_API_KEY=your-api-key-here
```

## Port Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  External Request                                            │
│  https://stg.bizoholic.com/portal/                          │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  Traefik (Reverse Proxy)                                    │
│  - Matches: Host(`stg.bizoholic.com`) && PathPrefix(`/portal`) │
│  - Middleware: Strip `/portal` prefix                       │
│  - Forwards to: http://frontend-client-portal:3001         │
└────────────────┬────────────────────────────────────────────┘
                 │ Docker Internal Network
                 │ (Uses Target Port: 3001)
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  Docker Container: frontend-client-portal                    │
│                                                              │
│  Internal: 3001 ← Traefik connects here                     │
│  Published: 3002 ← Only for host-level access (not used)   │
│                                                              │
│  Next.js Server running on port 3001                        │
│  ENV: BASE_PATH=/portal                                     │
└─────────────────────────────────────────────────────────────┘
```

## Why This Matters

### Published Port (3002):
- **Purpose**: Direct host-level access
- **Usage**: `curl http://localhost:3002` from the host machine
- **Not used by**: Traefik (it uses Docker network)

### Target Port (3001):
- **Purpose**: Container's internal listening port
- **Usage**: Traefik connects via Docker network
- **Service name**: `http://frontend-client-portal:3001`

### Docker Networking:
- Containers communicate via Docker's internal network using **service names**
- Example: `frontend-client-portal` resolves to container's IP
- Traefik accesses: `http://frontend-client-portal:3001` (Target Port)
- NOT: `http://frontend-client-portal:3002` (Published Port doesn't exist in Docker network)

## Alternative: Use Only Port 3001 for Both

To avoid confusion, you can set **both** published and target ports to 3001:

```yaml
Published Port: 3001
Target Port: 3001
```

Then Traefik config:
```yaml
url: http://frontend-client-portal:3001
```

This makes it clearer and avoids the published/target port confusion.

## Testing After Fix

### 1. Update Traefik Configuration
Update the service URL from 3002 to 3001 in Dokploy

### 2. Add Middleware
Add the `portal-stripprefix` middleware

### 3. Restart Container (if needed)
Dokploy should auto-restart after config changes

### 4. Test Access
```bash
# Should return 200 OK
curl -I https://stg.bizoholic.com/portal/

# Should see HTML content
curl https://stg.bizoholic.com/portal/
```

### 5. Check Container Logs
```bash
docker logs frontend-client-portal
```

Should see:
```
▲ Next.js 15.5.3
- Local:        http://localhost:3001
- Environment:  production

✓ Ready in 2.3s
```

## Quick Fix Checklist

- [ ] Change Traefik service URL from `:3002` to `:3001`
- [ ] Add `portal-stripprefix` middleware definition
- [ ] Add middleware to both HTTP and HTTPS routers
- [ ] Verify `BASE_PATH=/portal` environment variable is set
- [ ] Verify `PORT=3001` environment variable is set
- [ ] Restart container if needed
- [ ] Test access at `https://stg.bizoholic.com/portal/`
- [ ] Check container logs for startup confirmation

## Expected Result

After fixing the Traefik configuration:

✅ `https://stg.bizoholic.com/portal/` → Returns 200 OK
✅ Next.js app loads correctly
✅ Assets load with `/portal/` prefix
✅ API calls work
✅ Routing works correctly

---

**Next Steps**: After fixing this, continue with Week 1 implementation from `CLIENT_PORTAL_COMPLETE_IMPLEMENTATION_PLAN.md`
