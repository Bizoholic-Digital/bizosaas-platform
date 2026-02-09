# Admin Dashboard 404 - VPS Commands

## 🚨 Current Status
- ✅ Deployment successful
- ✅ Build completed (using cache)
- ✅ Container started
- ❌ Still returning 404

## 🔍 Quick Diagnosis

**SSH to your VPS and run these commands:**

### Option 1: Run Diagnostic Script (Recommended)
```bash
cd /etc/dokploy/compose/bizosaasadmindashboard-bizosaasadmindashboard-clo6cl/code
bash scripts/diagnose-admin-dashboard.sh
```

This will show you:
- Container status and health
- Container logs
- Network configuration
- Traefik routing
- Whether the app is actually listening on port 3004

### Option 2: Manual Quick Checks

```bash
# 1. Check if container is running
docker ps | grep bizosaas-admin-dashboard

# 2. Check container logs
docker logs bizosaas-admin-dashboard --tail 50

# 3. Test health endpoint from inside container
docker exec bizosaas-admin-dashboard wget -qO- http://localhost:3004/api/health

# 4. Check if container is on dokploy-network
docker inspect bizosaas-admin-dashboard | grep -A 10 Networks

# 5. Check Traefik logs
docker logs traefik 2>&1 | grep admin
```

## 🔧 Potential Issues & Solutions

### Issue 1: Container Not Listening on Port 3004
**Symptom**: Health check from inside container fails

**Solution**:
```bash
# Check what's running inside container
docker exec bizosaas-admin-dashboard ps aux

# If node process isn't running, check logs
docker logs bizosaas-admin-dashboard
```

### Issue 2: Container Not on dokploy-network
**Symptom**: Traefik can't reach the container

**Solution**:
```bash
# Add container to dokploy-network
docker network connect dokploy-network bizosaas-admin-dashboard

# Restart Traefik to pick up changes
docker restart traefik
```

### Issue 3: Traefik Not Seeing the Labels
**Symptom**: No admin-dashboard router in Traefik

**Solution**:
```bash
# Recreate container with labels
cd /etc/dokploy/compose/bizosaasadmindashboard-bizosaasadmindashboard-clo6cl/code
docker compose -f docker-compose.admin-dashboard.yml up -d --force-recreate

# Restart Traefik
docker restart traefik
```

### Issue 4: Auth Middleware Blocking Everything
**Symptom**: Container is healthy but all requests return 404/redirect

**Check**:
```bash
# Test root path
curl -I https://admin.bizoholic.net

# Test health endpoint (should work without auth)
curl https://admin.bizoholic.net/api/health

# If health works but root doesn't, it's an auth issue
```

## 🚀 Quick Fix Script

If diagnosis shows issues, run the fix script:

```bash
cd /etc/dokploy/compose/bizosaasadmindashboard-bizosaasadmindashboard-clo6cl/code
bash scripts/fix-admin-dashboard-404.sh
```

This will:
1. Stop and remove the container
2. Ensure networks exist
3. Pull latest code
4. Rebuild and start container
5. Wait for health check
6. Verify everything is working

## 📊 Expected Outputs

### Healthy Container
```bash
$ docker ps | grep bizosaas-admin-dashboard
bizosaas-admin-dashboard   Up 2 minutes (healthy)
```

### Working Health Endpoint
```bash
$ curl https://admin.bizoholic.net/api/health
{"status":"healthy","service":"bizosaas-admin","timestamp":"2025-12-12T..."}
```

### Correct Networks
```bash
$ docker inspect bizosaas-admin-dashboard | grep -A 10 Networks
"Networks": {
    "bizosaas-network": {...},
    "dokploy-network": {...}
}
```

### Traefik Routing
```bash
$ docker logs traefik 2>&1 | grep admin-dashboard
time="..." level=debug msg="Creating middleware" middlewareName=admin-dashboard-...
time="..." level=debug msg="Creating router" routerName=admin-dashboard
```

## 🎯 Most Likely Issues (Based on Logs)

Since the build used all cached layers, the most likely issues are:

1. **Container started but app crashed** - Check container logs
2. **Traefik not seeing the container** - Check networks
3. **Health check failing** - App not listening on port 3004
4. **Auth middleware issue** - Blocking all requests including root

## 📝 What to Share

After running the diagnostic script, please share:

1. The full output of `diagnose-admin-dashboard.sh`
2. Or at minimum:
   - Container status (`docker ps | grep admin`)
   - Container logs (`docker logs bizosaas-admin-dashboard --tail 30`)
   - Health check result (`docker exec bizosaas-admin-dashboard wget -qO- http://localhost:3004/api/health`)
   - Networks (`docker inspect bizosaas-admin-dashboard | grep -A 10 Networks`)

This will help identify the exact issue!

## 🔄 Alternative: Force Complete Rebuild

If nothing works, force a complete rebuild without cache:

```bash
cd /etc/dokploy/compose/bizosaasadmindashboard-bizosaasadmindashboard-clo6cl/code

# Stop and remove everything
docker compose -f docker-compose.admin-dashboard.yml down
docker rmi ghcr.io/bizoholic-digital/bizosaas-platform/admin-dashboard:latest

# Rebuild from scratch
docker compose -f docker-compose.admin-dashboard.yml build --no-cache
docker compose -f docker-compose.admin-dashboard.yml up -d

# Check logs
docker logs bizosaas-admin-dashboard -f
```

---

**Next Steps**: Run the diagnostic script and share the output!
