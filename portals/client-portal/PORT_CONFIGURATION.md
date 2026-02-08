# Port Configuration Summary

**Date**: November 11, 2025
**Status**: ✅ Configured

---

## Local Development Port Assignments

### Frontend Services

| Service | Port | URL | Status |
|---------|------|-----|--------|
| **Bizoholic Frontend** | 3000 | http://localhost:3000 | Reserved |
| **Client Portal** | 3001 | http://localhost:3001 | ✅ Running |
| **CoreLDove Storefront** | 3002 | http://localhost:3002 | Reserved |

### Backend Services

| Service | Port | URL | Status |
|---------|------|-----|--------|
| **API Gateway (Brain Gateway)** | 8080 | http://localhost:8080 | ❌ Not Running (code synced from VPS) |
| **Amazon Sourcing** | 8009 | http://localhost:8009 | ❌ Not Running |

**Note**: API Gateway has been synced from VPS to `/home/alagiri/projects/reference-from-vps/api-gateway/` for reference. Not running locally due to resource constraints. Using mock API responses in development.

---

## Client Portal Configuration

### Files Updated

1. **`.env`** - Port set to 3001, API Gateway on 8080
   ```bash
   PORT=3001
   NEXTAUTH_URL=http://localhost:3001
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8080
   NEXT_PUBLIC_BRAIN_API_URL=http://localhost:8080
   NEXT_PUBLIC_AUTH_API_URL=http://localhost:8080
   NEXT_PUBLIC_USE_MOCK_API=true
   ```

2. **`package.json`** - Dev and start scripts updated
   ```json
   {
     "scripts": {
       "dev": "next dev --port 3001",
       "start": "next start --port 3001"
     }
   }
   ```

---

## How to Start Each Service

### Client Portal (Port 3001)

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas-platform/frontend/apps/client-portal
npm run dev

# Access at: http://localhost:3001
```

### Bizoholic Frontend (Port 3000)

```bash
cd /home/alagiri/projects/bizoholic
# Start command here (TBD)

# Access at: http://localhost:3000
```

### CoreLDove Storefront (Port 3002)

```bash
cd /home/alagiri/projects/coreldove/coreldove-storefront-production
# Update port configuration to 3002
# Start command here

# Access at: http://localhost:3002
```

---

## Verification

### Check Running Services

```bash
# List all services and their ports
lsof -i :3000 -i :3001 -i :3002 -i :8001 -i :8080
```

### Test Each Service

```bash
# Client Portal
curl http://localhost:3001

# Bizoholic Frontend
curl http://localhost:3000

# CoreLDove Storefront
curl http://localhost:3002
```

---

## Current Status

### ✅ Client Portal on Port 3001

**Server Output:**
```
✓ Ready in 1974ms
- Local:        http://localhost:3001
- Network:      http://10.255.255.254:3001
```

**Test Result:**
```bash
$ curl http://localhost:3001 | grep h1
<h1 class="text-xl font-semibold text-gray-900 dark:text-white">Dashboard</h1>
```

✅ **CONFIRMED**: Client Portal running successfully on port 3001

---

## Deployment Configuration

### Production Ports (Dokploy)

All services in Dokploy use internal Docker network and Traefik for routing:

| Service | Internal Port | Public URL |
|---------|--------------|------------|
| **Client Portal** | 3001 | https://portal.bizoholic.com |
| **Bizoholic Frontend** | 3000 | https://bizoholic.com |
| **CoreLDove Storefront** | 3002 | https://stg.coreldove.com |
| **Brain Gateway** | 8001 | https://brain-gateway.bizoholic.com |
| **Amazon Sourcing** | 8080 | http://backend-amazon-sourcing:8080 (internal) |

---

## Troubleshooting

### Port Already in Use

```bash
# Find what's using a port
lsof -i :3001

# Kill process
kill -9 <PID>
```

### Change Port

To change the Client Portal port:

1. Update `.env`:
   ```bash
   PORT=<new-port>
   NEXTAUTH_URL=http://localhost:<new-port>
   ```

2. Update `package.json`:
   ```json
   "dev": "next dev --port <new-port>",
   "start": "next start --port <new-port>"
   ```

3. Restart server:
   ```bash
   pkill -f "next dev"
   npm run dev
   ```

---

## Documentation References

- [CLIENT_PORTAL_LOCAL_SETUP_GUIDE.md](./CLIENT_PORTAL_LOCAL_SETUP_GUIDE.md)
- [DOKPLOY_DEPLOYMENT_GUIDE.md](./DOKPLOY_DEPLOYMENT_GUIDE.md)
- [CLIENT_PORTAL_SETUP_COMPLETE.md](./CLIENT_PORTAL_SETUP_COMPLETE.md)

---

**Last Updated**: November 11, 2025
**Status**: ✅ Port 3001 Configured and Running
