# Phase 3: Frontend Deployment Quick Reference
## Command Cheat Sheet & Essential Information

**Version**: 1.0.0
**Last Updated**: October 10, 2025

---

## Essential URLs

| Service | URL | Port |
|---------|-----|------|
| Dokploy Dashboard | http://194.238.16.237:3000 | 3000 |
| Bizoholic Frontend | https://stg.bizoholic.com | 3000 |
| Client Portal | https://stg.bizoholic.com/login/ | 3001 |
| Admin Dashboard | https://stg.bizoholic.com/admin/ | 3009 |
| CorelDove E-commerce | https://stg.coreldove.com | 3002 |
| ThrillRing Gaming | https://stg.thrillring.com | 3005 |
| Business Directory | http://194.238.16.237:3004 | 3004 |

---

## Quick Deployment Commands

### Verify Prerequisites
```bash
# Check infrastructure (Phase 1)
./verify-infrastructure-deployment.sh

# Check backend services (Phase 2)
./verify-backend-deployment.sh

# Check DNS resolution
nslookup stg.bizoholic.com
nslookup stg.coreldove.com
nslookup stg.thrillring.com
```

### Deployment Verification
```bash
# Run full verification
./verify-frontend-deployment.sh

# Run comprehensive tests
./test-frontend-applications.sh
```

### Container Management
```bash
# List all frontend containers
docker ps | grep -E "frontend|portal|admin|directory|gaming"

# Check specific container
docker ps | grep bizoholic-frontend-3000

# View container logs
docker logs bizoholic-frontend-3000
docker logs coreldove-frontend-3002
docker logs thrillring-gaming-3005

# Follow logs in real-time
docker logs -f bizoholic-frontend-3000

# Check container health
docker inspect bizoholic-frontend-3000 --format='{{.State.Health.Status}}'

# Restart container
docker restart bizoholic-frontend-3000

# Stop container
docker stop bizoholic-frontend-3000

# Start container
docker start bizoholic-frontend-3000
```

### Resource Monitoring
```bash
# Check all container resources
docker stats --no-stream

# Monitor specific container
docker stats bizoholic-frontend-3000

# Check disk usage
df -h

# Check memory usage
free -m

# Check CPU usage
top
```

### Network Debugging
```bash
# Check network exists
docker network ls | grep bizosaas-network

# Inspect network
docker network inspect bizosaas-network

# Test connectivity from container
docker exec bizoholic-frontend-3000 ping bizosaas-brain-staging
docker exec bizoholic-frontend-3000 curl http://bizosaas-brain-staging:8001/health
```

---

## Container Names & Ports

| Container Name | Port | Service |
|----------------|------|---------|
| bizoholic-frontend-3000 | 3000 | Bizoholic Marketing |
| coreldove-frontend-3002 | 3002 | CorelDove E-commerce |
| thrillring-gaming-3005 | 3005 | ThrillRing Gaming |
| bizosaas-client-portal-3001 | 3001 | Client Portal |
| bizosaas-admin-3009 | 3009 | Admin Dashboard |
| business-directory-3004 | 3004 | Business Directory |

---

## Health Check Endpoints

```bash
# Bizoholic Frontend
curl http://194.238.16.237:3000/health
curl https://stg.bizoholic.com/api/health

# CorelDove Frontend
curl http://194.238.16.237:3002/health
curl https://stg.coreldove.com/api/health

# ThrillRing Gaming
curl http://194.238.16.237:3005/health
curl https://stg.thrillring.com/api/health

# Client Portal
curl http://194.238.16.237:3001/health
curl https://stg.bizoholic.com/login/api/health

# Admin Dashboard
curl http://194.238.16.237:3009/health
curl https://stg.bizoholic.com/admin/api/health

# Business Directory
curl http://194.238.16.237:3004/health
```

---

## DNS Configuration Reference

### Required DNS Records

| Record Type | Name | Value | TTL |
|-------------|------|-------|-----|
| A | stg.bizoholic.com | 194.238.16.237 | 300 |
| A | stg.coreldove.com | 194.238.16.237 | 300 |
| A | stg.thrillring.com | 194.238.16.237 | 300 |

### Verify DNS
```bash
# Check DNS resolution
nslookup stg.bizoholic.com
# Expected: Address: 194.238.16.237

dig stg.bizoholic.com +short
# Expected: 194.238.16.237

# Check DNS propagation
host stg.bizoholic.com
```

---

## SSL Certificate Management

### Check Certificate Status
```bash
# View certificate details
openssl s_client -connect stg.bizoholic.com:443 -servername stg.bizoholic.com < /dev/null | openssl x509 -noout -dates

# Check certificate expiry
echo | openssl s_client -connect stg.bizoholic.com:443 -servername stg.bizoholic.com 2>/dev/null | openssl x509 -noout -enddate

# Test SSL configuration
curl -I https://stg.bizoholic.com
```

### Force Certificate Renewal
```bash
# Restart Traefik to trigger renewal
docker restart traefik

# Or restart specific frontend container
docker restart bizoholic-frontend-3000
```

---

## Troubleshooting Quick Fixes

### Container Won't Start
```bash
# Check logs for errors
docker logs bizoholic-frontend-3000 --tail 50

# Check if port is already in use
netstat -tulpn | grep 3000

# Restart container
docker restart bizoholic-frontend-3000

# Rebuild and restart (via Dokploy)
# Go to Dokploy → Projects → bizosaas-frontend-staging → Redeploy
```

### Domain Not Accessible
```bash
# Check DNS
nslookup stg.bizoholic.com

# Check container is running
docker ps | grep bizoholic-frontend

# Check Traefik is running
docker ps | grep traefik

# Test internal port
curl http://194.238.16.237:3000

# Check Traefik logs
docker logs traefik | grep bizoholic
```

### SSL Certificate Issues
```bash
# Wait 2 minutes after first HTTPS request
sleep 120

# Clear browser cache and retry
# Ctrl+Shift+Delete in most browsers

# Check ACME challenge
docker logs traefik | grep -i acme

# Verify port 80/443 accessible
telnet 194.238.16.237 80
telnet 194.238.16.237 443
```

### High Memory Usage
```bash
# Check current usage
docker stats --no-stream bizoholic-frontend-3000

# Restart container to clear cache
docker restart bizoholic-frontend-3000

# Check for memory leaks in logs
docker logs bizoholic-frontend-3000 | grep -i "memory\|heap"
```

### Slow Response Times
```bash
# Test response time
curl -o /dev/null -s -w "Time: %{time_total}s\n" https://stg.bizoholic.com

# Check backend API response time
curl -o /dev/null -s -w "Time: %{time_total}s\n" http://194.238.16.237:8001/health

# Check container resource usage
docker stats bizoholic-frontend-3000
```

### Backend Connection Failed
```bash
# Test from inside container
docker exec bizoholic-frontend-3000 curl http://bizosaas-brain-staging:8001/health

# Check network connectivity
docker exec bizoholic-frontend-3000 ping bizosaas-brain-staging

# Verify environment variable
docker exec bizoholic-frontend-3000 env | grep API_BASE_URL
```

---

## Environment Variables Reference

### Common to All Frontends
```bash
NODE_ENV=staging
ENVIRONMENT=staging
DEBUG_MODE=true
ENABLE_ANALYTICS=false
```

### Bizoholic Frontend
```bash
NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-staging:8001
NEXT_PUBLIC_SITE_URL=https://stg.bizoholic.com
```

### CorelDove Frontend
```bash
NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-staging:8001
NEXT_PUBLIC_SITE_URL=https://stg.coreldove.com
NEXT_PUBLIC_SALEOR_API_URL=http://bizosaas-brain-staging:8001/api/brain/saleor
```

### ThrillRing Gaming
```bash
NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-staging:8001
NEXT_PUBLIC_SITE_URL=https://stg.thrillring.com
```

### Client Portal
```bash
NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-staging:8001
NEXT_PUBLIC_SITE_URL=https://stg.bizoholic.com/login
NEXT_PUBLIC_PORTAL_MODE=true
```

### Admin Dashboard
```bash
NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-staging:8001
NEXT_PUBLIC_SITE_URL=https://stg.bizoholic.com/admin
NEXT_PUBLIC_ADMIN_MODE=true
```

---

## Path-Based Routing Configuration

### Traefik Priority Rules

| Path | Priority | Container | Strip Prefix |
|------|----------|-----------|--------------|
| /login/ | 10 (high) | client-portal | Yes (/login) |
| /admin/ | 10 (high) | admin-dashboard | Yes (/admin) |
| / (catch-all) | 1 (low) | bizoholic-frontend | No |

### Test Path Routing
```bash
# Should go to client portal
curl -I https://stg.bizoholic.com/login/

# Should go to admin dashboard
curl -I https://stg.bizoholic.com/admin/

# Should go to marketing site
curl -I https://stg.bizoholic.com/

# Verify routing in Traefik logs
docker logs traefik | grep -E "login|admin"
```

---

## Performance Benchmarks

### Expected Response Times
| Metric | Target | Acceptable | Critical |
|--------|--------|------------|----------|
| First Request (cold) | < 2s | < 3s | > 5s |
| Subsequent (warm) | < 500ms | < 1s | > 2s |
| API Calls | < 200ms | < 500ms | > 1s |
| Health Check | < 100ms | < 200ms | > 500ms |

### Expected Resource Usage
| Resource | Per Container | Total (6 containers) |
|----------|---------------|----------------------|
| Memory | 100-300 MB | < 2 GB |
| CPU | 1-5% (idle) | < 20% (idle) |
| Disk | 200-400 MB | < 3 GB |

---

## Common API Endpoints

### Bizoholic Frontend
```bash
GET  https://stg.bizoholic.com/api/health
POST https://stg.bizoholic.com/api/contact
GET  https://stg.bizoholic.com/api/services
```

### CorelDove E-commerce
```bash
GET  https://stg.coreldove.com/api/health
GET  https://stg.coreldove.com/api/products
POST https://stg.coreldove.com/api/cart
POST https://stg.coreldove.com/api/checkout
```

### Client Portal
```bash
GET  https://stg.bizoholic.com/login/api/health
POST https://stg.bizoholic.com/login/api/auth/login
GET  https://stg.bizoholic.com/login/api/dashboard
```

### Admin Dashboard
```bash
GET  https://stg.bizoholic.com/admin/api/health
GET  https://stg.bizoholic.com/admin/api/users
GET  https://stg.bizoholic.com/admin/api/analytics
```

---

## Deployment Checklist (Quick)

### Before Deployment
- [ ] Infrastructure running (Phase 1)
- [ ] Backend running (Phase 2)
- [ ] DNS configured
- [ ] Dokploy accessible

### During Deployment
- [ ] Project created in Dokploy
- [ ] Configuration uploaded
- [ ] Deployment initiated
- [ ] Logs monitored

### After Deployment
- [ ] All containers running
- [ ] Health checks passing
- [ ] Domains accessible
- [ ] SSL certificates valid
- [ ] Verification script passed

---

## Emergency Procedures

### If All Containers Down
```bash
# Restart via Dokploy
# Go to Dokploy → Projects → bizosaas-frontend-staging → Restart All

# Or manually restart all
docker restart bizoholic-frontend-3000 coreldove-frontend-3002 thrillring-gaming-3005 bizosaas-client-portal-3001 bizosaas-admin-3009 business-directory-3004
```

### If Domains Not Resolving
```bash
# 1. Check DNS
nslookup stg.bizoholic.com

# 2. If wrong, update DNS records
# Contact domain registrar

# 3. Clear local DNS cache
sudo systemctl restart systemd-resolved  # Linux
```

### If SSL Certificates Failing
```bash
# 1. Verify DNS is correct
nslookup stg.bizoholic.com

# 2. Check port 80 accessibility
curl http://stg.bizoholic.com/.well-known/acme-challenge/test

# 3. Restart Traefik
docker restart traefik

# 4. Wait 2 minutes and test
sleep 120 && curl -I https://stg.bizoholic.com
```

### Rollback Procedure
```bash
# 1. Stop current deployment
# Go to Dokploy → Stop All Containers

# 2. Note current configuration
docker ps -a | grep frontend

# 3. Restore previous version
# Go to Dokploy → Deployments → Select previous version → Deploy

# 4. Verify rollback
./verify-frontend-deployment.sh
```

---

## Helpful Docker Commands

```bash
# View all containers (including stopped)
docker ps -a

# Remove stopped container
docker rm bizoholic-frontend-3000

# View container resource usage
docker stats

# Execute command in container
docker exec -it bizoholic-frontend-3000 /bin/sh

# Copy files from container
docker cp bizoholic-frontend-3000:/app/logs/app.log ./

# View container details
docker inspect bizoholic-frontend-3000

# View container environment variables
docker exec bizoholic-frontend-3000 env

# View container processes
docker top bizoholic-frontend-3000
```

---

## Monitoring Commands

```bash
# Watch container status
watch -n 5 'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.State}}"'

# Monitor logs in real-time
docker logs -f bizoholic-frontend-3000

# Check recent errors
docker logs bizoholic-frontend-3000 2>&1 | grep -i error | tail -20

# Monitor resource usage
watch -n 2 'docker stats --no-stream | grep frontend'

# Check disk usage
du -sh /var/lib/docker/

# Check network traffic
docker exec bizoholic-frontend-3000 netstat -an | grep ESTABLISHED
```

---

## Support Resources

### Documentation
- Full Deployment Guide: `PHASE3_FRONTEND_DEPLOYMENT.md`
- Deployment Checklist: `PHASE3_DEPLOYMENT_CHECKLIST.md`
- Troubleshooting Guide: `frontend-troubleshooting.md`
- API Integration: `frontend-api-integration.md`

### Scripts
- Verification: `./verify-frontend-deployment.sh`
- Testing: `./test-frontend-applications.sh`

### Logs Location
- Container logs: `docker logs <container-name>`
- Dokploy logs: Dokploy dashboard → Logs tab
- System logs: `/var/log/syslog`

---

## Important Notes

1. **Always verify DNS before deployment** - SSL certificates won't generate without correct DNS
2. **Wait for health checks** - Containers may take 30-60 seconds to show healthy
3. **Path routing priority matters** - Higher priority (10) routes are evaluated first
4. **SSL generation takes time** - First HTTPS request may take 30-120 seconds
5. **Monitor resource usage** - Each container should use < 400 MB memory
6. **Backend must be running** - Frontends depend on Brain API and other services
7. **Network is critical** - All containers must be on bizosaas-network

---

**Quick Reference Card - Keep This Handy During Deployment**

**Version**: 1.0.0
**Last Updated**: October 10, 2025
