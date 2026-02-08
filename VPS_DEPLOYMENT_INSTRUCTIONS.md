# VPS Deployment Fix Instructions

## Current Issues on VPS (194.238.16.237)
1. ❌ Temporal-server (f41566ffd086) - Restarting
2. ❌ Container 343f493bcbd0 - Restarting (likely auth service)
3. ❌ NO frontend services deployed (0/6)

## Expected Final State: 22 Services Total

### Infrastructure (7):
1. PostgreSQL (5432)
2. Redis (6379)
3. Vault (8200)
4. Temporal Server (7233)
5. Temporal UI (8082)
6. Temporal Integration (8007)
7. Apache Superset (8088)

### Backend (9):
1. Brain API (8001)
2. Wagtail CMS (8002)
3. Django CRM (8003)
4. Business Directory Backend (8004)
5. CorelDove Backend (8005)
6. Auth Service (8006)
7. AI Agents (8008)
8. Amazon Sourcing (8009)
9. Saleor API (8000)

### Frontend (6):
1. Bizoholic Frontend (3000)
2. Client Portal (3001)
3. CorelDove Frontend (3002)
4. Business Directory Frontend (3003)
5. ThrillRing Gaming (3004)
6. Admin Dashboard (3005)

---

## Step-by-Step Fix

### Step 1: SSH to VPS
```bash
ssh root@194.238.16.237
```

### Step 2: Check Current Status
```bash
# Count running containers
docker ps | wc -l

# See all containers
docker ps -a --format "table {{.Names}}\t{{.Status}}" | head -30
```

### Step 3: Fix Restarting Containers

#### A. Check Temporal Server Logs
```bash
docker logs f41566ffd086 --tail 50
```

**Common Issues:**
- Database connection failure → Check if Postgres is running
- Port conflict → Check if port 7233 is available

**Fix:**
```bash
# Restart temporal server
docker restart f41566ffd086

# If still fails, check postgres connection
docker exec f41566ffd086 nc -zv bizosaas-postgres-staging 5432
```

#### B. Check Auth Service Logs
```bash
# Identify the service
docker inspect 343f493bcbd0 | grep "Name"

# Check logs
docker logs 343f493bcbd0 --tail 50
```

**Common Issues:**
- Missing psycopg2/asyncpg module
- Database connection failure

**Fix:**
```bash
# Restart auth service
docker restart 343f493bcbd0

# If module error, rebuild from GitHub
cd /root/dokploy-projects/bizosaas  # or wherever your project is
docker-compose -f dokploy-backend-staging.yml up -d --build auth-service
```

### Step 4: Deploy ALL Frontend Services

Navigate to your Dokploy project directory:
```bash
cd /root/dokploy-projects/bizosaas
# OR
cd /opt/dokploy/bizosaas
# OR
cd /var/lib/dokploy/bizosaas
```

Pull latest code:
```bash
git pull origin main
```

Deploy frontend services:
```bash
docker-compose -f dokploy-frontend-staging.yml up -d
```

**This will deploy:**
- bizoholic-frontend (3000)
- client-portal (3001)
- coreldove-frontend (3002)
- business-directory-frontend (3003)
- thrillring-gaming (3004)
- admin-dashboard (3005)

### Step 5: Verify All Services

```bash
# Count total containers
docker ps | wc -l
# Should show 22

# List all services
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | sort

# Check for unhealthy containers
docker ps --filter "health=unhealthy"

# Check for restarting containers
docker ps -a | grep "Restarting"
```

### Step 6: Test Frontend Services

```bash
# Test each frontend port
for port in 3000 3001 3002 3003 3004 3005; do
  echo "Testing port $port..."
  curl -I http://194.238.16.237:$port
done
```

---

## Quick Commands Reference

```bash
# View all containers
docker ps -a

# Restart a specific service
docker restart <container-id-or-name>

# View logs
docker logs <container-name> --tail 50 -f

# Deploy backend
docker-compose -f dokploy-backend-staging.yml up -d

# Deploy frontend
docker-compose -f dokploy-frontend-staging.yml up -d

# Rebuild specific service
docker-compose -f dokploy-backend-staging.yml up -d --build <service-name>

# Stop all containers
docker-compose -f dokploy-backend-staging.yml down
docker-compose -f dokploy-frontend-staging.yml down

# Check service health
docker inspect <container-name> | grep -A 10 "Health"
```

---

## Troubleshooting

### Frontend Not Starting

**Issue:** Frontend containers exit immediately

**Check:**
```bash
docker logs <frontend-container> --tail 100
```

**Common causes:**
1. Build errors → Rebuild with `--build` flag
2. Missing environment variables → Check compose file
3. Port conflicts → Check if ports are available

**Fix:**
```bash
docker-compose -f dokploy-frontend-staging.yml up -d --build --force-recreate
```

### Database Connection Errors

**Symptoms:** Backend services restarting, logs show connection refused

**Check:**
```bash
# Verify postgres is running
docker ps | grep postgres

# Test connection from another container
docker exec <backend-container> nc -zv bizosaas-postgres-staging 5432
```

**Fix:**
```bash
# Restart postgres
docker restart bizosaas-postgres-staging

# Wait 10 seconds
sleep 10

# Restart dependent services
docker-compose -f dokploy-backend-staging.yml restart
```

### Port Conflicts

**Symptoms:** Containers exit with "port already in use"

**Check:**
```bash
# List listening ports
netstat -tulpn | grep LISTEN

# Or
ss -tulpn | grep LISTEN
```

**Fix:**
```bash
# Stop conflicting service or change port in docker-compose
# Then redeploy
```

---

## Final Verification Checklist

- [ ] PostgreSQL running (5432)
- [ ] Redis running (6379)
- [ ] Vault running (8200)
- [ ] Temporal Server running (7233)
- [ ] Temporal UI running (8082)
- [ ] Temporal Integration running (8007)
- [ ] Superset running (8088)
- [ ] Brain API running (8001)
- [ ] Wagtail CMS running (8002)
- [ ] Django CRM running (8003)
- [ ] Business Directory Backend running (8004)
- [ ] CorelDove Backend running (8005)
- [ ] Auth Service running (8006)
- [ ] AI Agents running (8008)
- [ ] Amazon Sourcing running (8009)
- [ ] Saleor API running (8000)
- [ ] Bizoholic Frontend running (3000)
- [ ] Client Portal running (3001)
- [ ] CorelDove Frontend running (3002)
- [ ] Business Directory Frontend running (3003)
- [ ] ThrillRing Gaming running (3004)
- [ ] Admin Dashboard running (3005)

**Total:** 22 services ✅
