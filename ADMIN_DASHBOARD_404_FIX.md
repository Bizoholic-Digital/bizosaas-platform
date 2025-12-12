# 🔍 Admin Dashboard 404 Troubleshooting Guide

## Current Status
- ✅ Container is running (`bizosaas-admin-dashboard`)
- ✅ App is listening on port 3004
- ✅ Environment variables are set
- ❌ Traefik is returning 404 (routing issue)

---

## 🔧 Immediate Fix Steps

### Option 1: Check Dokploy Domain Configuration

1. **Go to Dokploy UI** > Your Application > **Domains** tab
2. **Verify these settings**:
   - **Host**: `admin.bizoholic.net`
   - **Path**: `/`
   - **Container Port**: `3004` ⚠️ **CRITICAL**
   - **HTTPS**: Enabled
   - **Certificate**: Let's Encrypt

3. **After verifying, click "Save" and then "Redeploy"**

---

### Option 2: Manual Traefik Labels (If Dokploy UI Doesn't Work)

If the Dokploy UI domain configuration isn't working, we need to add Traefik labels back to the docker-compose file.

**Update `docker-compose.admin-dashboard.yml`** to add these labels:

```yaml
services:
  admin-dashboard:
    # ... existing config ...
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.admin-dashboard.rule=Host(`admin.bizoholic.net`)"
      - "traefik.http.routers.admin-dashboard.entrypoints=websecure"
      - "traefik.http.routers.admin-dashboard.tls=true"
      - "traefik.http.routers.admin-dashboard.tls.certresolver=letsencrypt"
      - "traefik.http.services.admin-dashboard.loadbalancer.server.port=3004"
      - "traefik.docker.network=dokploy-network"
```

---

### Option 3: Check Container Network

Run this command on your VPS to verify the container is on the right network:

```bash
docker inspect bizosaas-admin-dashboard | grep -A 10 Networks
```

**Expected output**: Should show both `bizosaas-network` AND `dokploy-network`.

If `dokploy-network` is missing, the container can't be reached by Traefik.

---

## 🐛 Debug Commands (Run on VPS)

```bash
# 1. Check if container is running
docker ps | grep admin-dashboard

# 2. Check container logs
docker logs bizosaas-admin-dashboard --tail 50

# 3. Check if app responds internally
docker exec bizosaas-admin-dashboard wget -qO- http://localhost:3004

# 4. Check Traefik routes
docker logs traefik 2>&1 | grep admin

# 5. List all Traefik routers
curl http://localhost:8080/api/http/routers | jq
```

---

## 🎯 Most Likely Issue

**Dokploy's domain configuration isn't creating Traefik labels automatically.**

This happens when:
1. The domain was added BEFORE the container was deployed
2. Dokploy's Traefik integration isn't working properly
3. The service name doesn't match

**Solution**: Add manual Traefik labels to `docker-compose.admin-dashboard.yml` (Option 2 above).

---

## ✅ Next Steps

1. Try **Option 1** first (verify Dokploy domain config)
2. If that doesn't work, use **Option 2** (manual labels)
3. Share the output of the debug commands if still not working
