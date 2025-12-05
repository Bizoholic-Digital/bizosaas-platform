# Automated Backend Deployment Loop

## Objective
Deploy all 10 backend services to Dokploy staging environment using an incremental, test-driven approach.

## Deployment Strategy

### Phase-Based Rollout
Deploy services in 4 phases, testing each phase before proceeding. This minimizes risk and makes debugging easier.

## Phase Breakdown

### Phase 1: Pre-built Image (1 service)
**File**: `dokploy-backend-staging-phase1.yml`
**Services**: Saleor API (port 8000)
**Risk Level**: LOW - Uses pre-built official image
**Expected Duration**: 2-3 minutes

**Deployment Steps**:
1. In Dokploy, navigate to backend project
2. Replace compose file with Phase 1 configuration
3. Click "Deploy"
4. Wait for container to start
5. Test: `curl http://194.238.16.237:8000/health/`

**Success Criteria**:
- Container running
- Health endpoint returns 200
- No restart loops

---

### Phase 2: Core Services (4 services total)
**File**: `dokploy-backend-staging-phase2.yml`
**New Services**:
- Brain API (port 8001)
- Auth Service (port 8006)
- Wagtail CMS (port 8002)

**Risk Level**: MEDIUM - First build-from-source services
**Expected Duration**: 5-10 minutes (build time)

**Deployment Steps**:
1. Verify Phase 1 is healthy
2. Replace compose file with Phase 2 configuration
3. Click "Deploy"
4. Monitor build logs for errors
5. Test health endpoints:
   ```bash
   curl http://194.238.16.237:8000/health/
   curl http://194.238.16.237:8001/health
   curl http://194.238.16.237:8006/health
   curl http://194.238.16.237:8002/admin/login/
   ```

**Success Criteria**:
- All 4 containers running
- All health checks passing
- Build completed without errors

**Common Issues**:
- **Build timeout**: Increase Dokploy build timeout
- **Missing dependencies**: Check Dockerfile requirements
- **Database connection**: Verify PostgreSQL is accessible

---

### Phase 3: CRM & Business Services (7 services total)
**File**: `dokploy-backend-staging-phase3.yml`
**New Services**:
- Django CRM (port 8003)
- Business Directory (port 8004)
- Temporal Integration (port 8007)

**Risk Level**: MEDIUM - CRM services with Django
**Expected Duration**: 5-8 minutes (build time)

**Deployment Steps**:
1. Verify Phase 2 is healthy (4 services)
2. Replace compose file with Phase 3 configuration
3. Click "Deploy"
4. Monitor build logs
5. Test new health endpoints:
   ```bash
   curl http://194.238.16.237:8003/admin/login/
   curl http://194.238.16.237:8004/health
   curl http://194.238.16.237:8007/health
   ```

**Success Criteria**:
- All 7 containers running
- All health checks passing
- Previous 4 services still healthy

**Common Issues**:
- **Django migrations**: May need to run migrations manually
- **Redis database index conflicts**: Each service uses different Redis DB
- **Temporal server dependency**: Ensure Temporal server container exists

---

### Phase 4: Complete Deployment (10 services total)
**File**: `dokploy-backend-staging-phase4.yml`
**New Services**:
- AI Agents (port 8008)
- Amazon Sourcing (port 8009)
- CorelDove Backend (port 8005)

**Risk Level**: MEDIUM-HIGH - AI services with external API dependencies
**Expected Duration**: 5-8 minutes (build time)

**Deployment Steps**:
1. Verify Phase 3 is healthy (7 services)
2. Replace compose file with Phase 4 configuration
3. Click "Deploy"
4. Monitor build logs
5. Run complete health check:
   ```bash
   ./test-backend-health.sh 194.238.16.237
   ```

**Success Criteria**:
- All 10 containers running
- All health checks passing
- No restart loops
- Services responsive on all ports

**Common Issues**:
- **OpenAI API key missing**: Services will start but may fail on API calls
- **Saleor API dependency**: CorelDove needs Saleor GraphQL endpoint
- **Brain API dependency**: AI Agents need Brain API accessible

---

## Automated Health Check

Use the provided script to test all services:

```bash
# Make executable
chmod +x test-backend-health.sh

# Run health check
./test-backend-health.sh 194.238.16.237

# Expected output:
# All services healthy: 10/10 ✓
```

---

## Troubleshooting Guide

### Container Won't Start
```bash
# Check container status
docker ps -a | grep bizosaas

# Check logs
docker logs bizosaas-[service-name]-staging

# Common fixes:
# 1. Database connection issue → verify PostgreSQL credentials
# 2. Port conflict → check if port already in use
# 3. Missing environment variable → add to compose file
```

### Build Failures
```bash
# Check Dokploy build logs
# Common issues:
# 1. GitHub access → verify repository is public or credentials correct
# 2. Dockerfile not found → check build context path
# 3. Dependency install fails → check requirements.txt or package.json
# 4. Build timeout → increase Dokploy timeout setting
```

### Health Check Failures
```bash
# Test manually
curl -v http://194.238.16.237:8001/health

# Check if service is listening
docker exec bizosaas-brain-staging netstat -tulpn | grep 8001

# Check database connectivity
docker exec bizosaas-brain-staging psql postgres://admin:password@194.238.16.237:5433/bizosaas_staging -c "SELECT 1"
```

### Database Connection Issues
```bash
# Test from VPS
psql -h 194.238.16.237 -p 5433 -U admin -d bizosaas_staging

# Test from container
docker exec bizosaas-brain-staging curl -v telnet://194.238.16.237:5433

# Common fixes:
# 1. Firewall blocking → open port 5433
# 2. PostgreSQL not listening on external IP → check postgresql.conf
# 3. Wrong credentials → verify DATABASE_URL
```

---

## Rollback Procedure

If a phase fails:

1. **Identify failing service**:
   ```bash
   docker ps -a | grep bizosaas
   docker logs [failing-container]
   ```

2. **Rollback to previous phase**:
   - In Dokploy, replace compose with previous working phase
   - Click "Deploy"
   - Verify previous services still working

3. **Debug offline**:
   - Fix Dockerfile or configuration
   - Test build locally if possible
   - Push fix to GitHub
   - Retry deployment

---

## Deployment Checklist

### Pre-Deployment
- [ ] VPS PostgreSQL running on 194.238.16.237:5433
- [ ] VPS Redis running on 194.238.16.237:6380
- [ ] Dokploy accessible at dk.bizoholic.com
- [ ] GitHub repository accessible
- [ ] Environment variables configured in Dokploy

### Phase 1
- [ ] Deploy Phase 1 compose
- [ ] Wait for container to start
- [ ] Test Saleor health endpoint
- [ ] Verify no errors in logs

### Phase 2
- [ ] Deploy Phase 2 compose
- [ ] Monitor build logs
- [ ] Test all 4 health endpoints
- [ ] Verify all containers running

### Phase 3
- [ ] Deploy Phase 3 compose
- [ ] Monitor build logs
- [ ] Test all 7 health endpoints
- [ ] Verify no restart loops

### Phase 4
- [ ] Deploy Phase 4 compose
- [ ] Monitor build logs
- [ ] Run automated health check script
- [ ] Verify all 10 services healthy

### Post-Deployment
- [ ] Document any issues encountered
- [ ] Update environment variables if needed
- [ ] Test basic API calls to each service
- [ ] Monitor logs for 10 minutes
- [ ] Create snapshot/backup of working state

---

## Success Metrics

### Phase 1 Success
- 1/10 services running (10% complete)
- Saleor API accessible
- Foundation for other services established

### Phase 2 Success
- 4/10 services running (40% complete)
- Core infrastructure services operational
- Build pipeline validated

### Phase 3 Success
- 7/10 services running (70% complete)
- CRM and business services operational
- Most dependencies resolved

### Phase 4 Success
- 10/10 services running (100% complete)
- All health checks passing
- Platform fully operational on staging

---

## Next Steps After Complete Deployment

1. **Integration Testing**: Test service-to-service communication
2. **Load Testing**: Verify services can handle expected load
3. **Monitoring Setup**: Configure logging and alerting
4. **Documentation**: Document API endpoints and usage
5. **Production Planning**: Prepare for production deployment

---

## Files Created

| File | Purpose |
|------|---------|
| `dokploy-backend-staging-phase1.yml` | Phase 1: Saleor only |
| `dokploy-backend-staging-phase2.yml` | Phase 2: + Core services |
| `dokploy-backend-staging-phase3.yml` | Phase 3: + CRM services |
| `dokploy-backend-staging-phase4.yml` | Phase 4: Complete (10 services) |
| `test-backend-health.sh` | Automated health check script |
| `BACKEND_DEPLOYMENT_DIAGNOSIS.md` | Root cause analysis |
| `AUTOMATED_DEPLOYMENT_LOOP.md` | This file - deployment guide |

---

## Support

If you encounter issues not covered in this guide:

1. Check Dokploy logs in the UI
2. Check container logs: `docker logs [container-name]`
3. Verify infrastructure: PostgreSQL, Redis, network
4. Review GitHub Actions logs if using CI/CD
5. Test build contexts locally before deploying

---

**Last Updated**: 2025-10-13
**Status**: Ready for deployment
**Next Action**: Start with Phase 1 deployment
