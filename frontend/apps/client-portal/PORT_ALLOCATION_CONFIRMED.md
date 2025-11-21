# Port Allocation - CONFIRMED ✅

## Current Port Usage

Based on analysis of Dockerfiles and running services:

| Service | Container Internal Port | Published Port | Traefik URL | Status |
|---------|------------------------|----------------|-------------|--------|
| **Dokploy** | N/A | 3000 | N/A | Running ✅ |
| **Bizoholic Frontend** | 3001 | ? | `http://bizoholic-frontend:3001` | Running ✅ |
| **Client Portal** | 3001 | 3002 | `http://frontend-client-portal:3001` | Running ✅ |

## Key Findings

### 1. Bizoholic Frontend Dockerfile
```dockerfile
ENV PORT 3001
EXPOSE 3001
```
**Container listens on**: Port 3001 internally

### 2. Client Portal Dockerfile
```dockerfile
ENV PORT=3001
EXPOSE 3001
```
**Container listens on**: Port 3001 internally

### 3. Both Services Use Port 3001 Internally - THIS IS FINE! ✅

**Why this works**:
- Each Docker container has its **own isolated network namespace**
- Multiple containers can use the same internal port (3001) without conflicts
- Traefik connects to containers via **Docker's internal network** using service names
- Published ports are only for host-level access and must be unique

## Port Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│  Host Machine (dk4.bizoholic.com)                            │
│                                                               │
│  Port 3000: Dokploy UI                                       │
│  Port 3002: Client Portal (Published - for host access only) │
│  Port ????: Bizoholic Frontend (Published - unknown)         │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ Docker Bridge Network
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Traefik    │      │  Bizoholic   │      │    Client    │
│              │      │   Frontend   │      │    Portal    │
│              │      │              │      │              │
│ Port: 80/443 │      │ Internal:    │      │ Internal:    │
│              │──────▶   3001       │      │   3001       │
│              │      │              │      │              │
│              │──────┼──────────────┼─────▶│              │
└──────────────┘      └──────────────┘      └──────────────┘
       │                     │                     │
       │ Via Docker Network  │                     │
       │ Service Names:      │                     │
       │                     │                     │
       │ bizoholic-frontend:3001                   │
       │                                           │
       │ frontend-client-portal:3001 ◄─────────────┘
```

## The Answer to Your Question

### ❓ Question:
> "if we are using port 3000 for dokploy and port 3001 for bizoholic frontend and now we need to be using client portal please check and confirm i still have to be updating the port from 3002 to 3001?"

### ✅ Answer: YES, YOU MUST UPDATE FROM 3002 TO 3001

**Why?**

1. **Your Traefik Config Currently Says**:
   ```yaml
   url: http://frontend-client-portal:3002  # ❌ WRONG
   ```

2. **Client Portal Container Actually Listens On**:
   ```
   Port 3001 (from Dockerfile: ENV PORT=3001, EXPOSE 3001)
   ```

3. **What Port 3002 Means**:
   - Port 3002 is the **Published Port** you set in Dokploy
   - This is ONLY for accessing the container from the host machine
   - Example: `curl http://localhost:3002` from the host
   - Traefik does NOT use this port!

4. **What Traefik Needs**:
   - Traefik connects via Docker's internal network
   - Must use the **container's internal port**: 3001
   - Service name: `frontend-client-portal`
   - Correct URL: `http://frontend-client-portal:3001`

## Visual Explanation

### ❌ Your Current (WRONG) Setup:
```
Traefik tries to connect:
  http://frontend-client-portal:3002
         │
         └──▶ Port 3002 doesn't exist in Docker network!
              (Published ports only exist at host level)

Result: 502 Bad Gateway ❌
```

### ✅ Correct Setup:
```
Traefik connects:
  http://frontend-client-portal:3001
         │
         └──▶ Port 3001 is the container's internal port
              Container is listening on 3001 ✅

Result: 200 OK ✅
```

## Port Conflict Analysis

### Can Both Services Use Port 3001? YES! ✅

**Bizoholic Frontend**:
- Container Internal: 3001 ✅
- Traefik URL: `http://bizoholic-frontend:3001` ✅

**Client Portal**:
- Container Internal: 3001 ✅ (Same port, different container)
- Traefik URL: `http://frontend-client-portal:3001` ✅

**No Conflict Because**:
1. Each container is isolated
2. Service names are different (`bizoholic-frontend` vs `frontend-client-portal`)
3. Traefik routes based on domain/path, not port
4. Published ports (3002) only matter for host-level access

## What You Need To Do

### In Dokploy Traefik Configuration:

**Change this**:
```yaml
services:
  frontend-client-portal-service-3:
    loadBalancer:
      servers:
        - url: http://frontend-client-portal:3002  # ❌ WRONG
```

**To this**:
```yaml
services:
  frontend-client-portal-service-3:
    loadBalancer:
      servers:
        - url: http://frontend-client-portal:3001  # ✅ CORRECT
```

### Port Configuration Summary

**Keep in Dokploy**:
- Published Port: 3002 (or any unused port - doesn't matter for Traefik)
- Target Port: 3001 ✅ (this is what matters!)

**Use in Traefik**:
- Service URL: `http://frontend-client-portal:3001` ✅ (Target Port)

## Testing After Fix

```bash
# This should return 200 OK after fix
curl -I https://stg.bizoholic.com/portal/

# Check container is listening on 3001
docker exec frontend-client-portal netstat -tuln | grep 3001

# Expected output:
# tcp        0      0 :::3001                 :::*                    LISTEN
```

## Final Confirmation

### Your Configuration Should Be:

**Dokploy Port Settings**:
```
Published Port: 3002 (for host-level access if needed)
Target Port: 3001 (container internal port)
```

**Traefik Service URL**:
```yaml
url: http://frontend-client-portal:3001  # ✅ Must be 3001 (Target Port)
```

**Environment Variable**:
```bash
PORT=3001  # Must match Target Port
```

---

## Summary

✅ **YES, update Traefik from port 3002 to 3001**
✅ Both services can use internal port 3001 (no conflict)
✅ Published port 3002 is fine (only for host access)
✅ Traefik MUST use the Target Port (3001), not Published Port (3002)

The confusion comes from:
- **Published Port** (3002) = Host-level access only
- **Target Port** (3001) = Container internal + Traefik access ✅

**Bottom Line**: Change the Traefik service URL from `:3002` to `:3001` to fix the 502 Bad Gateway error.
