# Quick Deployment Commands

## 🚀 Fast Track Deployment

Copy and run these commands in order:

### 1. Verify Code is Ready
```bash
cd /home/alagiri/projects/bizosaas-platform
git pull origin staging
git log --oneline -1
# Should show: "feat: migrate to official Docker images..."
```

### 2. Check Current Status
```bash
ssh root@72.60.98.213 "docker ps --format 'table {{.Names}}\t{{.Status}}' | head -20"
```

### 3. Deploy Authentik (New Service)
```bash
# Copy compose file to server
scp docker-compose.authentik.yml root@72.60.98.213:/root/authentik-compose.yml

# Deploy
ssh root@72.60.98.213 "cd /root && docker-compose -f authentik-compose.yml up -d"

# Verify
ssh root@72.60.98.213 "docker ps | grep authentik"
```

### 4. Create Authentik Admin
```bash
ssh root@72.60.98.213 "docker exec -it authentik-server ak create_recovery_key 10 akadmin"
# Copy the recovery URL and open in browser
```

### 5. Verify All Services
```bash
# Check for unhealthy/restarting containers
ssh root@72.60.98.213 "docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -E 'Restart|unhealthy'"

# Should return empty or minimal results
```

### 6. Test Endpoints
```bash
# Test APIs
curl https://api.bizoholic.net/health
curl https://api.bizoholic.net/api/connectors/
curl https://sso.bizoholic.net/.well-known/openid-configuration

# All should return 200
```

### 7. Check Seeding Logs
```bash
ssh root@72.60.98.213 "docker logs brain-gateway 2>&1 | grep -E '🌱|✅'"
# Should show: "✅ Seeding Complete! Registered 4 connectors"
```

---

## ✅ Success Criteria

After running these commands, you should have:

- ✅ Authentik running (4 containers)
- ✅ brain-auth running (no restarts)
- ✅ Lago running (no restarts)
- ✅ All APIs responding
- ✅ Connectors seeded

---

## 🔧 If Something Fails

### Authentik won't start
```bash
ssh root@72.60.98.213 "docker logs authentik-server --tail 50"
# Check for errors, verify environment variables
```

### brain-auth still restarting
```bash
# Redeploy Core Services in Dokploy
# OR manually:
ssh root@72.60.98.213 "docker restart brain-auth && docker logs -f brain-auth"
```

### Lago still crashing
```bash
# Redeploy Lago in Dokploy
# Check migration logs:
ssh root@72.60.98.213 "docker logs lago-migrate 2>&1 | tail -30"
```

---

## 📋 Deployment Checklist

- [ ] Code pulled from GitHub
- [ ] Authentik deployed
- [ ] Authentik admin created
- [ ] Core Services redeployed (if needed)
- [ ] Lago redeployed (if needed)
- [ ] All services healthy
- [ ] APIs responding
- [ ] Connectors seeded
- [ ] Client Portal login works
