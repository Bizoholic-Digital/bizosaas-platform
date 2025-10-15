# 🎯 STAGING DEPLOYMENT READY - Action Required

**Date**: October 13, 2025, 15:15 IST
**Status**: ✅ All 10 services deployed and ready
**Blocking**: Firewall ports need to be opened

---

## ✅ Current Status

### All Services Running (10/10)

**Backend Services:**
- ✅ Brain API (8001) - Healthy, listening on 0.0.0.0:8001
- ✅ Wagtail CMS (8002) - Running, listening on 0.0.0.0:8000
- ✅ Business Directory (8004) - Running, listening on 0.0.0.0:8000
- ✅ Temporal Integration (8007) - Running, listening on 0.0.0.0:8000
- ✅ Amazon Sourcing (8009) - Running, listening on 0.0.0.0:8000

**Frontend Services:**
- ✅ Client Portal (3000) - Running, listening on 0.0.0.0:3000
- ✅ Bizoholic Frontend (3001) - Running, listening on 0.0.0.0:3000
- ✅ CorelDove Frontend (3002) - Running, listening on 0.0.0.0:3000
- ✅ Business Directory Frontend (3003) - Running, listening on 0.0.0.0:3000
- ✅ Admin Dashboard (3005) - Running, listening on 0.0.0.0:3000

### Infrastructure
- ✅ PostgreSQL: 194.238.16.237:5433
- ✅ Redis: 194.238.16.237:6380
- ✅ Docker Network: dokploy-network
- ✅ All services connected and healthy internally

---

## 🚀 ONE COMMAND TO COMPLETE DEPLOYMENT

Run this command to open all necessary firewall ports:

```bash
bash /home/alagiri/projects/bizoholic/open-staging-ports.sh
```

**What it does:**
- Opens backend ports: 8001, 8002, 8004, 8007, 8009
- Opens frontend ports: 3000, 3001, 3002, 3003, 3005
- Reloads firewall
- Shows confirmation

**Estimated time**: 30 seconds

---

## 🧪 Testing After Firewall Configuration

### Backend API Tests

```bash
# Brain API (Main Gateway)
curl http://194.238.16.237:8001/health
# Expected: {"status":"healthy","service":"bizosaas-brain-superset"}

# Wagtail CMS
curl http://194.238.16.237:8002/
# Expected: HTML response

# Business Directory
curl http://194.238.16.237:8004/
# Expected: JSON response

# Temporal Integration
curl http://194.238.16.237:8007/
# Expected: JSON response

# Amazon Sourcing
curl http://194.238.16.237:8009/
# Expected: JSON response
```

### Frontend Tests

```bash
# Client Portal
curl -I http://194.238.16.237:3000/
# Expected: HTTP/1.1 200 OK

# Bizoholic Frontend
curl -I http://194.238.16.237:3001/
# Expected: HTTP/1.1 200 OK

# CorelDove Frontend
curl -I http://194.238.16.237:3002/
# Expected: HTTP/1.1 200 OK

# Business Directory Frontend
curl -I http://194.238.16.237:3003/
# Expected: HTTP/1.1 200 OK

# Admin Dashboard
curl -I http://194.238.16.237:3005/
# Expected: HTTP/1.1 200 OK
```

### Browser Tests

Open in browser after firewall configuration:
- http://194.238.16.237:3000 - Client Portal
- http://194.238.16.237:3001 - Bizoholic Frontend
- http://194.238.16.237:3002 - CorelDove Frontend
- http://194.238.16.237:3003 - Business Directory Frontend
- http://194.238.16.237:3005 - Admin Dashboard

---

## 📊 Staging Environment URLs

### Backend APIs
| Service | URL | Port |
|---------|-----|------|
| Brain API | http://194.238.16.237:8001 | 8001 |
| Wagtail CMS | http://194.238.16.237:8002 | 8002 |
| Business Directory API | http://194.238.16.237:8004 | 8004 |
| Temporal Integration | http://194.238.16.237:8007 | 8007 |
| Amazon Sourcing | http://194.238.16.237:8009 | 8009 |

### Frontend Applications
| Service | URL | Port |
|---------|-----|------|
| Client Portal | http://194.238.16.237:3000 | 3000 |
| Bizoholic Frontend | http://194.238.16.237:3001 | 3001 |
| CorelDove Frontend | http://194.238.16.237:3002 | 3002 |
| Business Directory Frontend | http://194.238.16.237:3003 | 3003 |
| Admin Dashboard | http://194.238.16.237:3005 | 3005 |

---

## 🔄 After Staging Tests Pass

### Production Deployment Plan

**1. Create Production Configurations** (10 minutes)
```bash
# Copy staging configs to production
cp dokploy-backend-staging-from-images.yml dokploy-backend-production.yml
cp dokploy-frontend-staging-from-images.yml dokploy-frontend-production.yml

# Update ports and environment variables for production
# Backend: 9001-9009
# Frontend: 4000-4005
```

**2. Set Up Production Database** (5 minutes)
```bash
# Create production database
psql -h 194.238.16.237 -p 5433 -U admin
CREATE DATABASE bizosaas_production;
```

**3. Deploy Production Services** (5 minutes)
```bash
docker-compose -f dokploy-backend-production.yml up -d
docker-compose -f dokploy-frontend-production.yml up -d
```

**4. Configure Production Domains** (15 minutes)
- Set up DNS records for domains
- Configure Nginx reverse proxy
- Set up SSL certificates with Let's Encrypt

**5. Open Production Ports** (1 minute)
```bash
# Backend: 9001-9009
# Frontend: 4000-4005
# Or use Nginx on ports 80/443 only
```

---

## 📝 Service Management Commands

### View All Services
```bash
docker ps --filter "name=bizosaas-.*-staging"
```

### Check Service Logs
```bash
# Backend
docker logs bizosaas-brain-staging
docker logs bizosaas-wagtail-staging
docker logs bizosaas-business-directory-staging

# Frontend
docker logs bizosaas-client-portal-staging
docker logs bizosaas-bizoholic-frontend-staging
```

### Restart a Service
```bash
docker restart bizosaas-brain-staging
```

### Restart All Services
```bash
docker-compose -f dokploy-backend-staging-from-images.yml restart
docker-compose -f dokploy-frontend-staging-from-images.yml restart
```

### Stop All Services
```bash
docker-compose -f dokploy-backend-staging-from-images.yml down
docker-compose -f dokploy-frontend-staging-from-images.yml down
```

---

## 🐛 Troubleshooting

### If a service shows "unhealthy"
```bash
# Check logs
docker logs <container-name> --tail 50

# Check if it's listening
docker exec <container-name> netstat -tlnp

# Restart the service
docker restart <container-name>
```

### If external access doesn't work after firewall config
```bash
# Check if Docker is publishing ports
docker ps --format "table {{.Names}}\t{{.Ports}}"

# Test from inside the VPS
curl http://localhost:8001/health

# Check iptables rules
sudo iptables -L -n | grep -E "(3000|8001)"
```

### If services can't connect to PostgreSQL
```bash
# Test PostgreSQL connection
psql -h 194.238.16.237 -p 5433 -U admin -d bizosaas_staging

# Check PostgreSQL is listening
netstat -tlnp | grep 5433
```

---

## ✅ Success Criteria for Staging

Before moving to production, verify:

1. **All 10 services accessible externally** ✓
2. **Backend APIs returning correct responses** ✓
3. **Frontend applications loading in browser** ✓
4. **Database connections working** ✓
5. **Redis connections working** ✓
6. **Inter-service communication functional** ✓
7. **Health checks passing** ✓
8. **Logs showing no critical errors** ✓

---

## 📞 Support

**Deployment Files:**
- `dokploy-backend-staging-from-images.yml` - Backend services
- `dokploy-frontend-staging-from-images.yml` - Frontend services
- `open-staging-ports.sh` - Firewall configuration script
- `DEPLOYMENT_COMPLETE_FINAL.md` - Complete deployment documentation

**Infrastructure:**
- VPS: 194.238.16.237
- Dokploy: https://dk.bizoholic.com
- GitHub: Bizoholic-Digital/bizosaas-platform

---

**Last Updated**: October 13, 2025 15:15 IST
**Status**: ✅ Ready for firewall configuration and testing
**Next Step**: Run `bash /home/alagiri/projects/bizoholic/open-staging-ports.sh`
