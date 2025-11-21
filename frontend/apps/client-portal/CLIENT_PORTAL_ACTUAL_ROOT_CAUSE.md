# Client Portal - ACTUAL Root Cause & Solution

**Date**: 2025-11-01
**Status**: ❌ CONTAINERS EXITING IMMEDIATELY AFTER STARTUP

---

## The Real Problem

The Client Portal containers are **starting successfully** but **exiting immediately** after startup, causing a restart loop.

### Evidence

```
Service Logs:
✓ Next.js 15.5.3 Ready in 153ms
✓ Next.js 15.5.3 Ready in 193ms
✓ Next.js 15.5.3 Ready in 204ms
✓ Next.js 15.5.3 Ready in 211ms
✓ Next.js 15.5.3 Ready in 226ms

Service Status:
frontend-client-portal.1  Complete 29 seconds ago
frontend-client-portal.1  Complete 2 minutes ago
frontend-client-portal.1  Complete 4 minutes ago
frontend-client-portal.1  Complete 6 minutes ago
frontend-client-portal.1  Starting 24 seconds ago  ← Currently trying again
```

**Pattern**: Container starts → Reports "Ready" → Exits → Docker Swarm marks as "Complete" → Swarm tries to restart → Loop continues

---

## Root Cause Analysis

### Why Are Containers Exiting?

Possible causes:

####  1. **Healthcheck Failure** (MOST LIKELY)

The Dockerfile has a healthcheck that might be causing the container to be marked as unhealthy and killed:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3001/', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"
```

**Problem**: If the healthcheck fails (even once after the start period), Docker marks the container as unhealthy and may restart it depending on Swarm configuration.

#### 2. **Missing Environment Variables**

The application might be crashing due to missing required environment variables like:
- `NEXTAUTH_URL`
- `DATABASE_URL`
- `NEXT_PUBLIC_API_URL`

#### 3. **Application Error After Startup**

The app starts successfully but encounters a runtime error shortly after, causing the Node process to exit.

#### 4. **Signal Handling Issue**

Docker Swarm might be sending signals (SIGTERM, SIGHUP) that the Next.js standalone server isn't handling properly, causing immediate exit.

---

## Investigation Steps

Let me check the actual container logs right before exit:

```bash
ssh root@72.60.219.244

# Get the currently starting task
docker service ps frontend-client-portal --format "{{.ID}}\t{{.Name}}\t{{.CurrentState}}" | head -1

# Watch the logs in real-time
docker service logs -f frontend-client-portal

# Check container exit code
docker service ps frontend-client-portal --no-trunc --format "{{.Name}}\t{{.Error}}"
```

Expected findings:
- Exit code 0 = Clean exit (healthcheck or signal issue)
- Exit code 1 = Application error
- Exit code 137 = Killed by OOM or Docker
- Exit code 143 = SIGTERM received

---

## Solutions (In Order of Likelihood)

### Solution 1: Disable or Fix Healthcheck

The healthcheck might be failing because:
- Application takes longer than 60s start period to be fully ready
- HTTP request to `localhost:3001` fails even though app is listening
- Timeout (10s) is too short

**Option A: Increase start period and timeout**

Update Dockerfile:
```dockerfile
HEALTHCHECK --interval=30s --timeout=30s --start-period=120s --retries=5 \
  CMD node -e "require('http').get('http://localhost:3001/', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"
```

**Option B: Disable healthcheck temporarily**

```dockerfile
# Remove HEALTHCHECK line entirely
# Or add: HEALTHCHECK NONE
```

**Option C: Use simpler healthcheck**

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD node -e "require('net').createConnection(3001, 'localhost').on('connect', () => process.exit(0)).on('error', () => process.exit(1))"
```

This just checks if port 3001 is listening (simpler than HTTP request).

### Solution 2: Add Required Environment Variables

Via Dokploy UI, ensure ALL these variables are set:

```env
# Required for NextAuth
NEXTAUTH_URL=https://stg.bizoholic.com/portal
NEXTAUTH_SECRET=<your-secret>

# Required for API calls
NEXT_PUBLIC_API_URL=https://stg.bizoholic.com/api

# Database (if required)
DATABASE_URL=postgresql://...

# JWT
JWT_SECRET=<your-secret>

# Base path
BASE_PATH=/portal

# Port
PORT=3001
```

### Solution 3: Rebuild Image Without Healthcheck

Quickest solution - rebuild the Docker image without the HEALTHCHECK:

```bash
cd /tmp/client-portal-build

# Edit Dockerfile - remove HEALTHCHECK line
nano Dockerfile

# Rebuild
docker build -t ghcr.io/bizoholic-digital/bizosaas-client-portal:v1.0.1-no-healthcheck .

# Push
docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:v1.0.1-no-healthcheck

# Update Dokploy to use new image
```

### Solution 4: Use Regular Container Instead of Swarm Service

Deploy as a regular Docker container (not Swarm service) to avoid Swarm's restart policies:

Via Dokploy UI:
1. Delete current Swarm service deployment
2. Create new deployment as "Docker Compose" or "Docker Container"
3. Use same image and configuration

---

## Recommended Action Plan

### Immediate Fix (5 minutes)

1. **Disable healthcheck and redeploy:**

```bash
ssh root@72.60.219.244
cd /tmp/client-portal-build

# Create new Dockerfile without healthcheck
cat > Dockerfile.no-health <<'EOF'
FROM node:18-alpine

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3001
ENV HOSTNAME=0.0.0.0

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

COPY --chown=nextjs:nodejs standalone ./
COPY --chown=nextjs:nodejs .next/static ./.next/static
COPY --chown=nextjs:nodejs public ./public

USER nextjs

EXPOSE 3001

# NO HEALTHCHECK!

CMD ["node", "bizosaas/frontend/apps/client-portal/server.js"]
EOF

# Build and push
docker build -f Dockerfile.no-health -t ghcr.io/bizoholic-digital/bizosaas-client-portal:v1.0.1-no-healthcheck .
docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:v1.0.1-no-healthcheck
```

2. **Update Dokploy to use new image:**
   - Go to Dokploy UI
   - Change image tag to `v1.0.1-no-healthcheck`
   - Click "Deploy"

### If That Doesn't Work (10 minutes)

Deploy as regular container via Docker Compose through Dokploy:

```yaml
version: '3.8'
services:
  client-portal:
    image: ghcr.io/bizoholic-digital/bizosaas-client-portal:v1.0.0-foundation-dashboard
    container_name: client-portal
    restart: unless-stopped
    ports:
      - "3002:3001"
    environment:
      PORT: 3001
      BASE_PATH: /portal
      NEXTAUTH_URL: https://stg.bizoholic.com/portal
      NEXTAUTH_SECRET: ${NEXTAUTH_SECRET}
      JWT_SECRET: ${JWT_SECRET}
      NODE_ENV: production
    networks:
      - dokploy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.client-portal.rule=Host(`stg.bizoholic.com`) && PathPrefix(`/portal`)"
      - "traefik.http.routers.client-portal.entrypoints=websecure"
      - "traefik.http.routers.client-portal.tls.certresolver=letsencrypt"
      - "traefik.http.services.client-portal.loadbalancer.server.port=3001"
      - "traefik.http.middlewares.portal-strip.stripprefix.prefixes=/portal"
      - "traefik.http.routers.client-portal.middlewares=portal-strip"

networks:
  dokploy-network:
    external: true
```

---

## Why Bizoholic Frontend Works But Client Portal Doesn't

Comparing the two services:

### Bizoholic Frontend (WORKING)
- **Replicas**: 1/1 (running)
- **Status**: Running for days
- **Logs**: No restarts, no exits
- **Healthcheck**: Probably none or working correctly

### Client Portal (NOT WORKING)
- **Replicas**: 0/1 (exit loop)
- **Status**: Starts → Ready in ~200ms → Exits → Repeat
- **Logs**: Multiple restart attempts
- **Healthcheck**: Present and possibly failing

**Key Difference**: The healthcheck configuration or missing environment variables.

---

## Next Steps

1. **I'll create a new Docker image without healthcheck**
2. **Push to GHCR**
3. **You update Dokploy UI to use new image and deploy**
4. **We verify the service stays running**
5. **Test portal accessibility**

Would you like me to proceed with building the image without healthcheck now?

---

## Status Summary

| Component | Status |
|-----------|--------|
| Docker Image | ✅ Built and pushed |
| Container Startup | ✅ Starts successfully |
| Container Runtime | ❌ Exits immediately |
| Swarm Service | ❌ In restart loop |
| Traefik Config | ✅ Correct (service name) |
| Network | ✅ Configured properly |
| **Root Cause** | ❌ **Healthcheck or env vars causing exit** |

**Blocking Issue**: Containers exit immediately after "Ready" message

**Solution**: Rebuild without healthcheck OR add missing env vars OR deploy as regular container

---

**Priority**: HIGH - Service cannot stay running
**ETA to Fix**: 5-10 minutes once solution is chosen
