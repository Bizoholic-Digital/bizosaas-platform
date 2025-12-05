# Quick Deploy Reference Card

## 🚀 4-Phase Deployment Strategy

### Phase 1: Foundation (3 min)
```yaml
File: dokploy-backend-staging-phase1.yml
Services: 1 (Saleor only)
Test: curl http://194.238.16.237:8000/health/
```

### Phase 2: Core Services (10 min)
```yaml
File: dokploy-backend-staging-phase2.yml
Services: 4 (Saleor + Brain + Auth + Wagtail)
Test: ./test-backend-health.sh 194.238.16.237
```

### Phase 3: Business Services (8 min)
```yaml
File: dokploy-backend-staging-phase3.yml
Services: 7 (Previous + Django CRM + Business Directory + Temporal)
Test: ./test-backend-health.sh 194.238.16.237
```

### Phase 4: Complete (8 min)
```yaml
File: dokploy-backend-staging-phase4.yml
Services: 10 (All backend services)
Test: ./test-backend-health.sh 194.238.16.237
```

## 📋 Deployment Checklist

- [ ] PostgreSQL running at 194.238.16.237:5433
- [ ] Redis running at 194.238.16.237:6380
- [ ] Dokploy accessible at dk.bizoholic.com
- [ ] Deploy Phase 1
- [ ] Test Phase 1 health
- [ ] Deploy Phase 2
- [ ] Test Phase 2 health
- [ ] Deploy Phase 3
- [ ] Test Phase 3 health
- [ ] Deploy Phase 4
- [ ] Test all services with health script

## 🔍 Quick Health Check Commands

```bash
# Single service
curl http://194.238.16.237:8000/health/

# All services (automated)
./test-backend-health.sh 194.238.16.237

# Manual check all ports
for port in 8000 8001 8002 8003 8004 8005 8006 8007 8008 8009; do
  echo "Port $port:"
  curl -s -o /dev/null -w "%{http_code}\n" http://194.238.16.237:$port/health
done
```

## 🐛 Quick Troubleshooting

```bash
# Check container status
docker ps -a | grep bizosaas

# View logs
docker logs bizosaas-[service]-staging

# Test database
psql -h 194.238.16.237 -p 5433 -U admin -d bizosaas_staging

# Test Redis
redis-cli -h 194.238.16.237 -p 6380 ping
```

## 📊 Service Port Reference

| Port | Service | Phase |
|------|---------|-------|
| 8000 | Saleor API | 1 |
| 8001 | Brain API | 2 |
| 8002 | Wagtail CMS | 2 |
| 8003 | Django CRM | 3 |
| 8004 | Business Directory | 3 |
| 8005 | CorelDove Backend | 4 |
| 8006 | Auth Service | 2 |
| 8007 | Temporal | 3 |
| 8008 | AI Agents | 4 |
| 8009 | Amazon Sourcing | 4 |

## ⏱️ Expected Timeline

- Phase 1: 3 min
- Phase 2: 10 min (cumulative: 13 min)
- Phase 3: 8 min (cumulative: 21 min)
- Phase 4: 8 min (cumulative: 29 min)
- **Total: ~30 minutes**

## 🎯 Success Criteria

✅ All 10 containers running
✅ Health check script shows 10/10
✅ No restart loops
✅ All ports accessible

## 📁 File Locations

All files in: `/home/alagiri/projects/bizoholic/`

- `dokploy-backend-staging-phase1.yml`
- `dokploy-backend-staging-phase2.yml`
- `dokploy-backend-staging-phase3.yml`
- `dokploy-backend-staging-phase4.yml`
- `test-backend-health.sh`

## 🔄 Rollback Command

If phase fails, redeploy previous phase compose file in Dokploy.

## 📖 Full Documentation

See `AUTOMATED_DEPLOYMENT_LOOP.md` for complete guide.
