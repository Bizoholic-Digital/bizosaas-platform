# VPS Deployment Execution Guide - BizOSaaS Platform
*Ready for immediate deployment to staging VPS: 194.238.16.237*

## 🎯 Mission: Deploy All 22 Services to VPS

### Current VPS Status
- **IP**: 194.238.16.237
- **Dokploy URL**: https://dk.bizoholic.com
- **Issues**: 2 containers restarting, 0 frontend services deployed
- **Target**: 22 services total (6 infrastructure + 10 backend + 6 frontend)

## 🚀 Immediate Actions Required

### Step 1: Fix Restarting Containers (2 minutes)
```bash
# SSH to VPS (you have access, I don't)
ssh root@194.238.16.237

# Fix the 2 restarting containers
docker restart f41566ffd086  # temporal-server
docker restart 343f493bcbd0  # auth-service or similar

# Verify they're now stable
docker ps | grep -E "f41566ffd086|343f493bcbd0"
```

### Step 2: Deploy Frontend Stack (5 minutes)
The frontend services are completely missing from VPS. Deploy them:

```bash
# On VPS, clone the repository if not present
cd /opt/
git clone https://github.com/Bizoholic-Digital/bizosaas-platform.git
cd bizosaas-platform

# Or pull latest changes if already cloned
git pull origin main

# Deploy all 6 frontend services
docker-compose -f dokploy-frontend-staging.yml up -d --build
```

**Expected Result**: 6 new containers running on ports 3000-3005

### Step 3: Add Superset (22nd Service) (3 minutes)
```bash
# Create Superset configuration
cat > superset-staging.yml << 'EOF'
version: '3.8'
services:
  superset:
    image: apache/superset:latest
    container_name: bizosaas-superset-staging
    ports:
      - "8088:8088"
    environment:
      - SUPERSET_CONFIG_PATH=/app/superset/superset_config.py
      - SUPERSET_SECRET_KEY=your-secret-key-here
    volumes:
      - superset_home:/app/superset_home
      - ./superset_config.py:/app/superset/superset_config.py
    networks:
      - dokploy-network
    restart: unless-stopped
    command: ["sh", "-c", "superset db upgrade && superset fab create-admin --username admin --firstname Admin --lastname User --email admin@bizosaas.com --password admin123 && superset init && superset run -h 0.0.0.0 -p 8088"]

volumes:
  superset_home:

networks:
  dokploy-network:
    external: true
EOF

# Deploy Superset
docker-compose -f superset-staging.yml up -d
```

## 📊 Verification Commands

### Check All 22 Services Running
```bash
# Should show 22 services + header = 23 lines
docker ps | wc -l

# Detailed view of all services
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | sort
```

### Expected Service List (22 Total)
```
Infrastructure (6):
✓ bizosaas-postgres-unified       (5432)
✓ bizosaas-redis-unified         (6379)
✓ bizosaas-temporal-server       (7233)
✓ bizosaas-temporal-ui-server    (8082)
✓ bizosaas-vault                 (8200)
⚠ bizosaas-superset-staging      (8088) - NEW

Backend (10):
⚠ bizosaas-brain-staging         (8001) - REDEPLOY
⚠ bizosaas-wagtail-staging       (8002) - REDEPLOY
⚠ bizosaas-django-crm-staging    (8003) - REDEPLOY
⚠ bizosaas-business-directory-staging (8004) - REDEPLOY
⚠ bizosaas-amazon-sourcing-staging (8005) - REDEPLOY
⚠ bizosaas-temporal-integration-staging (8006) - REDEPLOY
⚠ bizosaas-ai-agents-staging     (8007) - REDEPLOY
⚠ bizosaas-auth-service-staging  (8008) - REDEPLOY
⚠ bizosaas-coreldove-backend-staging (8009) - REDEPLOY
⚠ bizosaas-saleor-staging        (8010) - REDEPLOY

Frontend (6):
⚠ bizosaas-client-portal-staging (3000) - NEW
⚠ bizosaas-bizoholic-frontend-staging (3001) - NEW
⚠ bizosaas-coreldove-frontend-staging (3002) - NEW
⚠ bizosaas-business-directory-frontend-staging (3003) - NEW
⚠ bizosaas-thrillring-gaming-staging (3004) - NEW
⚠ bizosaas-admin-dashboard-staging (3005) - NEW
```

## 🔧 Backend Services Deployment

If backend services aren't running, redeploy them:
```bash
# Deploy backend services with latest fixes
docker-compose -f dokploy-backend-staging.yml down
docker-compose -f dokploy-backend-staging.yml up -d --build
```

## 🌐 Access URLs After Deployment

### Management Interfaces
- **Dokploy Dashboard**: https://dk.bizoholic.com
- **Temporal UI**: http://194.238.16.237:8082
- **Vault UI**: http://194.238.16.237:8200
- **Superset Analytics**: http://194.238.16.237:8088

### Application URLs
- **Client Portal**: http://194.238.16.237:3000
- **Bizoholic Frontend**: http://194.238.16.237:3001
- **CorelDove Frontend**: http://194.238.16.237:3002
- **Business Directory**: http://194.238.16.237:3003
- **ThrillRing Gaming**: http://194.238.16.237:3004
- **Admin Dashboard**: http://194.238.16.237:3005

### API Endpoints
- **Brain API**: http://194.238.16.237:8001
- **Wagtail CMS**: http://194.238.16.237:8002
- **Django CRM**: http://194.238.16.237:8003
- **Auth Service**: http://194.238.16.237:8008

## ⚡ Quick Deploy Script

If you want to execute everything at once:
```bash
#!/bin/bash
echo "🚀 Deploying all 22 BizOSaaS services..."

# Fix restarting containers
echo "1. Fixing restarting containers..."
docker restart f41566ffd086 343f493bcbd0

# Deploy frontend stack
echo "2. Deploying frontend services..."
docker-compose -f dokploy-frontend-staging.yml up -d --build

# Deploy backend stack (if needed)
echo "3. Ensuring backend services are running..."
docker-compose -f dokploy-backend-staging.yml up -d

# Add Superset
echo "4. Adding Superset analytics..."
docker-compose -f superset-staging.yml up -d

# Final verification
echo "5. Verification:"
docker ps --format "table {{.Names}}\t{{.Status}}" | wc -l
echo "✅ Deployment complete! Check https://dk.bizoholic.com"
```

## 🔍 Troubleshooting

### If Services Fail to Start
1. **Check logs**: `docker logs [container-name] --tail 50`
2. **Check disk space**: `df -h`
3. **Check memory**: `free -h`
4. **Restart Docker**: `systemctl restart docker`

### If Builds Fail
1. **Clear Docker cache**: `docker system prune -a`
2. **Pull latest changes**: `git pull origin main`
3. **Rebuild with no cache**: `docker-compose up -d --build --no-cache`

## ✅ Success Criteria
- [ ] 22 containers running (`docker ps | wc -l` = 23)
- [ ] No containers in "Restarting" status
- [ ] All frontend URLs accessible (3000-3005)
- [ ] All backend APIs responding (8001-8010)
- [ ] Dokploy showing all services as "healthy"

---
**Status**: Ready for immediate VPS deployment. All code fixes are in GitHub main branch.