# Targeted Deployment Plan - Only Missing/Broken Services
*Efficient deployment - only what's needed*

## 🎯 Current VPS Status (from context)

### ✅ Already Running (DO NOT REDEPLOY)
1. PostgreSQL Database - Port 5432 ✅
2. Redis Cache - Port 6379 ✅
3. Temporal UI - Port 8082 ✅
4. HashiCorp Vault - Port 8200 ✅

### ⚠️ Need Fixing (2 containers)
1. **Temporal Server** - Container f41566ffd086 (RESTARTING)
2. **Auth Service** - Container 343f493bcbd0 (RESTARTING)

### ❌ Completely Missing (Need Full Deployment)
**Frontend Services (6):**
1. Client Portal - Port 3000
2. Bizoholic Frontend - Port 3001
3. CorelDove Frontend - Port 3002
4. Business Directory Frontend - Port 3003
5. ThrillRing Gaming - Port 3004
6. Admin Dashboard - Port 3005

**Infrastructure:**
7. Superset Analytics - Port 8088 (22nd service)

## 📊 Deployment Statistics
- **Already Running**: 4 services (skip these)
- **Need Restart**: 2 services (quick fix)
- **Need Deployment**: 7 services (frontend + superset)
- **Total to Deploy**: 9 services (instead of 22)
- **Time Savings**: ~70% faster deployment

## 🚀 Execution Plan

### Phase 1: Fix Restarting Containers (30 seconds)
```bash
# Simple restart command
ssh root@194.238.16.237 "docker restart f41566ffd086 343f493bcbd0"
```

### Phase 2: Deploy Frontend Stack (5 minutes)
```bash
ssh root@194.238.16.237 << 'EOF'
cd /root/bizosaas-platform
git pull origin main
docker-compose -f dokploy-frontend-staging.yml up -d
EOF
```

### Phase 3: Deploy Superset (2 minutes)
```bash
ssh root@194.238.16.237 << 'EOF'
docker run -d \
  --name bizosaas-superset-staging \
  -p 8088:8088 \
  --network dokploy-network \
  --restart unless-stopped \
  -e SUPERSET_SECRET_KEY=bizosaas-superset-2025 \
  apache/superset:latest
EOF
```

## ✅ Success Criteria
After deployment, verify:
- [ ] 2 containers no longer restarting
- [ ] 6 frontend services accessible (ports 3000-3005)
- [ ] Superset accessible (port 8088)
- [ ] Total running containers = 13+ (4 infra + 2 fixed + 6 frontend + 1 superset)

## 📝 Notes
- **No need to redeploy**: PostgreSQL, Redis, Temporal UI, Vault
- **Backend services**: Status unclear, but not mentioned as broken
- **API token issue**: Falling back to SSH commands for reliability
- **GitHub repo**: All fixes already pushed (commits 4ec02f3, 84279e6)

## 🕐 Estimated Timeline
- Phase 1 (restart): 30 seconds
- Phase 2 (frontend): 5 minutes (build + deploy)
- Phase 3 (superset): 2 minutes
- **Total**: ~7-8 minutes (vs 20+ minutes for full redeployment)
