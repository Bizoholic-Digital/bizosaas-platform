# Dokploy Deployment Fixes - January 7, 2026

## Issues Identified

### 1. Brain Gateway - Missing Network
**Error**: `network brain-network not found`
**Cause**: The `brain-network` was marked as `external: true` but didn't exist on the server

### 2. Admin Portal - Port Conflict
**Error**: `Bind for 0.0.0.0:3000 failed: port is already allocated`
**Cause**: Multiple services trying to bind to host port 3000

### 3. Client Portal - Port Conflict
**Error**: `Bind for 0.0.0.0:3000 failed: port is already allocated`
**Cause**: Same as Admin Portal

## Solutions Implemented

### ✅ Fix 1: Brain Network Creation
**File**: `docker-compose.core.yml`

Changed from:
```yaml
networks:
  brain-network:
    external: true
```

To:
```yaml
networks:
  brain-network:
    driver: bridge
    name: brain-network
```

**Result**: The network will now be created automatically when the stack is deployed.

### ✅ Fix 2: Remove Port Bindings
**Files**: 
- `docker-compose.core.yml` (brain-gateway)
- `docker-compose.admin-portal.yml` (admin-dashboard)
- `docker-compose.client-portal.yml` (client-portal)

Changed from:
```yaml
ports:
  - "3000:3000"  # or "8000:8000"
```

To:
```yaml
expose:
  - "3000"  # or "8000"
```

**Result**: 
- No port conflicts on the host
- Traefik handles all routing via the existing labels
- Services are only accessible through their configured domains

## Deployment Order via Dokploy UI

### Step 1: Deploy Brain Gateway (Core Services)
1. Go to Dokploy UI → Projects → BizOSaaS Brain Gateway
2. Click "Redeploy" or "Deploy"
3. Wait for successful deployment
4. Verify: `https://api.bizoholic.net/health` should return 200 OK

### Step 2: Deploy Admin Portal
1. Go to Dokploy UI → Projects → BizOSaaS Frontend (Admin Portal)
2. Click "Redeploy" or "Deploy"
3. Wait for successful deployment
4. Verify: `https://admin.bizoholic.net` should load

### Step 3: Deploy Client Portal
1. Go to Dokploy UI → Projects → BizOSaaS Frontend (Client Portal)
2. Click "Redeploy" or "Deploy"
3. Wait for successful deployment
4. Verify: `https://app.bizoholic.net` should load

### Step 4: Deploy Vault (if not already running)
1. Go to Dokploy UI → Projects → Vault
2. Click "Deploy"
3. Verify: `https://vault.bizoholic.net` should load

## Technical Details

### Why Remove Port Bindings?

1. **Prevents Conflicts**: Multiple services can use the same internal port (3000) without conflicts
2. **Security**: Services aren't directly exposed on host ports
3. **Traefik Routing**: Traefik uses the `expose` directive and service labels to route traffic
4. **Best Practice**: In a reverse proxy setup, only the proxy should bind to host ports

### How Traefik Routes Traffic

Each service has labels like:
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.SERVICE.rule=Host(`domain.com`)"
  - "traefik.http.services.SERVICE.loadbalancer.server.port=3000"
```

Traefik:
1. Listens on ports 80/443 (already bound by Dokploy's Traefik)
2. Reads the service labels
3. Routes requests to the internal container port
4. No host port binding needed!

## Verification Commands

After deployment, verify each service:

```bash
# Brain Gateway
curl -I https://api.bizoholic.net/health

# Admin Portal
curl -I https://admin.bizoholic.net

# Client Portal
curl -I https://app.bizoholic.net

# Vault
curl -I https://vault.bizoholic.net
```

## Git Commit

**Commit**: `c89dd18`
**Branch**: `staging`
**Message**: "fix: Remove port conflicts and create brain-network internally"

## Next Steps

1. ✅ Changes committed and pushed to GitHub
2. ⏳ Redeploy services via Dokploy UI in the order specified above
3. ⏳ Verify all services are accessible via their domains
4. ⏳ Test login flows on both portals

## Notes

- All changes maintain existing Traefik labels
- No environment variables were modified
- Services will communicate internally via Docker networks
- External access is only through Traefik (ports 80/443)
