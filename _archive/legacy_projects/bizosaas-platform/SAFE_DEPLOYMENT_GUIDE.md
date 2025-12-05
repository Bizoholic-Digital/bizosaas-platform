# Safe Deployment Guide - BizOSaaS Platform

**Date**: October 15, 2025
**Strategy**: Deploy BizOSaaS Platform WITHOUT touching existing WordPress/n8n services
**VPS**: 194.238.16.237

---

## ⚠️ SAFETY FIRST

### What Will Be Preserved (NOT Touched)

✅ **WordPress Services**
- All WordPress containers
- WordPress databases
- WordPress volumes
- WordPress networks

✅ **n8n Automation Services**
- n8n containers
- n8n databases
- n8n workflows
- n8n volumes

✅ **Shared Infrastructure** (if used by WordPress/n8n)
- Existing PostgreSQL instances
- Existing Redis/Dragonfly instances
- pgAdmin containers
- Any shared networks

### What Will Be Deployed (New)

🆕 **BizOSaaS Platform** (23 services)
- Infrastructure: 6 services (PostgreSQL, Redis, Vault, Temporal x2, Superset)
- Backend: 10 services (Brain Gateway, AI Agents, Auth, CMS, CRM, etc.)
- Frontend: 7 services (Bizoholic, ThrillRing, CorelDove, Portals, etc.)

**All new services prefixed with**: `bizosaas-*`

---

## 📋 Step-by-Step Deployment

### Step 1: Check Current VPS State (READ-ONLY)

```bash
cd ~/projects/bizoholic/bizosaas-platform

# Install sshpass if needed
sudo apt-get install sshpass

# Run inventory check (no changes made)
./check-vps-services.sh
```

**What This Shows:**
- All currently running containers
- Docker images on VPS
- Docker volumes
- Disk usage
- **NO CHANGES MADE** - Read-only check

**Review the output** and confirm:
- [ ] WordPress services are running
- [ ] n8n services are running
- [ ] Note their container names
- [ ] Check available disk space

---

### Step 2: Deploy BizOSaaS Platform (Safe Mode)

```bash
# Run safe deployment
./deploy-safe-no-cleanup.sh
```

**What This Does:**
1. ✅ Checks VPS connectivity
2. ✅ Shows existing services that will be preserved
3. ✅ Asks for confirmation before proceeding
4. ✅ Pulls latest code from GitHub
5. ✅ Deploys Infrastructure (6 services)
6. ✅ Deploys Backend (10 services)
7. ✅ Deploys Frontend (7 services)
8. ✅ Verifies deployments
9. ✅ Tests Brain Gateway
10. ⚠️ **DOES NOT remove any existing services**

**Deployment Time:** ~5-10 minutes

---

### Step 3: Verify Deployment

```bash
# SSH to VPS
ssh root@194.238.16.237
# Password: &k3civYG5Q6YPb

# Check all services
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

# Count BizOSaaS services
docker ps | grep bizosaas | wc -l
# Expected: 23

# Test Brain Gateway
curl http://localhost:8001/health

# Test Bizoholic Frontend
curl http://localhost:3001

# Check logs if needed
docker logs bizosaas-brain-staging --tail 50
```

---

### Step 4: Test BizOSaaS Services

#### Test Infrastructure
```bash
# PostgreSQL
docker exec bizosaas-postgres-staging psql -U admin -d bizosaas_staging -c "SELECT version();"

# Redis
docker exec bizosaas-redis-staging redis-cli ping

# Temporal UI (browser)
http://194.238.16.237:8083

# Superset (browser)
http://194.238.16.237:8088
```

#### Test Backend Services
```bash
# Brain Gateway (CRITICAL - all routes through here)
curl http://194.238.16.237:8001/health

# Wagtail CMS
curl http://194.238.16.237:8002

# Saleor E-commerce
curl http://194.238.16.237:8000/health/

# Auth Service
curl http://194.238.16.237:8007/health
```

#### Test Frontend Services
```bash
# Bizoholic
curl -I http://194.238.16.237:3001

# ThrillRing Gaming
curl -I http://194.238.16.237:3005

# CorelDove
curl -I http://194.238.16.237:3002

# Client Portal
curl -I http://194.238.16.237:3000

# Admin Dashboard
curl -I http://194.238.16.237:3009
```

---

## 🎯 Success Criteria

### ✅ Deployment Successful If:

1. **All 23 BizOSaaS services running**
   ```bash
   docker ps | grep bizosaas | wc -l
   # Should output: 23
   ```

2. **Brain Gateway responding**
   ```bash
   curl http://194.238.16.237:8001/health
   # Should return HTTP 200 or JSON response
   ```

3. **WordPress still running** (preserved)
   ```bash
   docker ps | grep wordpress
   # Should show WordPress containers
   ```

4. **n8n still running** (preserved)
   ```bash
   docker ps | grep n8n
   # Should show n8n containers
   ```

5. **No port conflicts**
   - BizOSaaS uses: 5433, 6380, 8000-8012, 3000-3009, 8083, 8088, 8201, 7234
   - Verify these don't conflict with WordPress/n8n

---

## 🔄 If Issues Found

### Issue: Port Conflicts

**Symptom**: Container fails to start, port already in use

**Solution**:
```bash
# Check what's using the port
netstat -tlnp | grep :8001

# Stop BizOSaaS service
docker stop bizosaas-brain-staging

# Edit compose file to use different port
# Then redeploy
```

### Issue: Service Not Starting

**Symptom**: Container shows "Restarting" or "Unhealthy"

**Solution**:
```bash
# Check logs
docker logs bizosaas-[service-name] --tail 100

# Common fixes:
# 1. Database not ready - wait 30 seconds
# 2. Environment variable missing - check compose file
# 3. Network issue - verify dokploy-network exists
```

### Issue: Brain Gateway Not Responding

**Symptom**: curl returns connection refused

**Solution**:
```bash
# Check if running
docker ps | grep brain

# Check logs
docker logs bizosaas-brain-staging --tail 50

# Restart
docker restart bizosaas-brain-staging

# Wait 30 seconds and test again
curl http://194.238.16.237:8001/health
```

---

## 🧹 Cleanup (AFTER Testing Complete)

### When WordPress/n8n No Longer Needed

**Only run this AFTER:**
- [ ] BizOSaaS platform fully tested
- [ ] WordPress data migrated (if needed)
- [ ] n8n workflows migrated (if needed)
- [ ] Confirmation from team

```bash
# Will create this script after testing complete
./cleanup-old-services.sh

# This will:
# - Stop WordPress containers
# - Stop n8n containers
# - Remove old images
# - Clean up unused volumes
# - Free disk space
```

**DO NOT run cleanup until instructed!**

---

## 📊 Resource Usage

### Before Deployment
- Run `df -h` to check disk space
- Ensure at least 20GB free

### After Deployment
- BizOSaaS uses ~10-15GB (images + volumes)
- Monitor: `docker system df`

### If Disk Space Low
1. Test BizOSaaS thoroughly first
2. Confirm WordPress/n8n can be removed
3. Run cleanup script
4. Expected to free: 5-10GB

---

## 🎯 Next Steps After Successful Deployment

1. **Document Current State**
   ```bash
   docker ps > ~/bizosaas-deployment-$(date +%Y%m%d).txt
   ```

2. **Test Multi-Tenant Isolation**
   - Create test tenants
   - Verify data separation
   - Test Brain Gateway routing

3. **Performance Testing**
   - Load test Brain Gateway
   - Monitor service response times
   - Check database query performance

4. **Domain Configuration** (future)
   - Setup SSL certificates
   - Configure domain routing
   - Setup Traefik/Nginx

5. **Backup Strategy**
   - Backup PostgreSQL data
   - Backup volumes
   - Document restore procedure

---

## 📞 Quick Reference

### SSH Access
```bash
ssh root@194.238.16.237
Password: &k3civYG5Q6YPb
```

### Important Directories
- Code: `/root/bizosaas-platform`
- Compose files: `/root/bizosaas-platform/dokploy-*.yml`

### Key Services
- Brain Gateway: Port 8001 (CRITICAL)
- Bizoholic: Port 3001
- Admin: Port 3009
- Superset: Port 8088

### Troubleshooting
```bash
# View all services
docker ps -a

# Check specific service
docker logs bizosaas-[service] --tail 100

# Restart service
docker restart bizosaas-[service]

# Check resource usage
docker stats --no-stream
```

---

**Status**: ✅ Ready for Safe Deployment
**Risk Level**: LOW (preserves existing services)
**Estimated Time**: 5-10 minutes
**Rollback**: Easy (stop BizOSaaS containers, existing services unaffected)
