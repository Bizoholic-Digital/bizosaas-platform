# Phase 2: Backend Services Deployment Checklist

**Project**: bizosaas-backend-staging
**Date**: ________________
**Deployed By**: ________________
**VPS IP**: 194.238.16.237
**Dokploy URL**: http://194.238.16.237:3000

---

## PRE-DEPLOYMENT VERIFICATION (15 minutes)

### Infrastructure Check (Phase 1)
- [ ] Phase 1 infrastructure project exists
- [ ] PostgreSQL container running (port 5432)
- [ ] Redis container running (port 6379)
- [ ] Vault container running (port 8200)
- [ ] Temporal server running (port 7233)
- [ ] Temporal UI accessible (port 8082)
- [ ] Temporal integration running (port 8009)

**Verification Command**:
```bash
ssh root@194.238.16.237 'docker ps --filter "name=staging" | wc -l'
# Expected: 7 or more lines (6 containers + header)
```

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

### Network Configuration
- [ ] Network `bizosaas-staging-network` exists
- [ ] Network is external and shared

**Verification Command**:
```bash
ssh root@194.238.16.237 'docker network ls | grep bizosaas-staging-network'
```

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

### API Keys Collection
- [ ] OPENROUTER_API_KEY obtained
- [ ] OPENAI_API_KEY obtained
- [ ] ANTHROPIC_API_KEY obtained
- [ ] STRIPE_SECRET_KEY obtained (test mode)
- [ ] PAYPAL_CLIENT_ID obtained (sandbox)
- [ ] PAYPAL_CLIENT_SECRET obtained (sandbox)
- [ ] AMAZON_ACCESS_KEY obtained
- [ ] AMAZON_SECRET_KEY obtained

**Reference**: See `phase2-env-template.txt` for key acquisition guide

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

### Documentation Review
- [ ] Read PHASE2_BACKEND_DEPLOYMENT.md
- [ ] Review PHASE2_QUICK_REFERENCE.md
- [ ] Understand service architecture
- [ ] Know troubleshooting steps

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

### Resource Availability
- [ ] VPS has sufficient CPU (8+ cores)
- [ ] VPS has sufficient RAM (16+ GB)
- [ ] VPS has sufficient disk (50+ GB free)
- [ ] Network connectivity stable

**Verification Command**:
```bash
ssh root@194.238.16.237 'free -h && df -h | grep "/$" && nproc'
```

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

## DEPLOYMENT EXECUTION (15 minutes)

### Access Dokploy Dashboard
- [ ] Opened http://194.238.16.237:3000 in browser
- [ ] Successfully logged in with admin credentials
- [ ] Can see existing projects

**Time Started**: ___:___
**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

### Create Backend Project
- [ ] Clicked "Projects" in sidebar
- [ ] Clicked "New Project" button
- [ ] Entered name: `bizosaas-backend-staging`
- [ ] Entered description: "Backend services and APIs for staging environment"
- [ ] Clicked "Create Project"
- [ ] Project appears in projects list

**Time Completed**: ___:___
**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

### Create Docker Compose Application
- [ ] Entered `bizosaas-backend-staging` project
- [ ] Clicked "New Application" button
- [ ] Selected "Docker Compose" type
- [ ] Entered name: `backend-services`
- [ ] Entered description: "8 backend API services"

**Time Completed**: ___:___
**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

### Upload Configuration
- [ ] Located configuration upload section
- [ ] Uploaded `dokploy-backend-staging.yml` OR
- [ ] Copied and pasted file contents
- [ ] Verified 8 services visible in config
- [ ] Checked services: brain-api, wagtail-cms, django-crm, business-directory-api, coreldove-backend, ai-agents, amazon-sourcing, saleor-api

**Time Completed**: ___:___
**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

### Configure Environment Variables
- [ ] Clicked "Environment Variables" tab
- [ ] Added OPENROUTER_API_KEY
- [ ] Added OPENAI_API_KEY
- [ ] Added ANTHROPIC_API_KEY
- [ ] Added STRIPE_SECRET_KEY
- [ ] Added PAYPAL_CLIENT_ID
- [ ] Added PAYPAL_CLIENT_SECRET
- [ ] Added AMAZON_ACCESS_KEY
- [ ] Added AMAZON_SECRET_KEY
- [ ] Verified no typos in variable names
- [ ] Verified no extra spaces in values

**Time Completed**: ___:___
**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

### Deploy Application
- [ ] Clicked "Deploy" button
- [ ] Deployment process started
- [ ] Watched build logs for progress
- [ ] No build errors appeared
- [ ] All services started successfully
- [ ] Deployment completed

**Time Started**: ___:___
**Time Completed**: ___:___
**Total Deploy Time**: _____ minutes
**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

## POST-DEPLOYMENT VERIFICATION (10 minutes)

### Container Status Check
- [ ] All 8 containers show "Running" status in Dokploy
- [ ] Brain API container (bizosaas-brain-staging) running
- [ ] Wagtail CMS container (bizosaas-wagtail-staging) running
- [ ] Django CRM container (bizosaas-django-crm-staging) running
- [ ] Directory API container (bizosaas-directory-api-staging) running
- [ ] CorelDove Backend container (coreldove-backend-staging) running
- [ ] AI Agents container (bizosaas-ai-agents-staging) running
- [ ] Amazon Sourcing container (amazon-sourcing-staging) running
- [ ] Saleor container (bizosaas-saleor-staging) running

**Verification Command**:
```bash
ssh root@194.238.16.237 'docker ps --filter "name=staging" --format "{{.Names}}" | grep -E "(brain|wagtail|django|directory|coreldove|ai-agents|amazon|saleor)"'
```

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

### Health Endpoint Tests

#### Brain API (Port 8001) - CRITICAL
- [ ] Health endpoint responds
- [ ] Returns HTTP 200
- [ ] Status shows "healthy"

**Test Command**:
```bash
curl -f http://194.238.16.237:8001/health
```

**Status**: ☐ Pass | ☐ Fail | **Response**: _______________________

---

#### Wagtail CMS (Port 8002)
- [ ] Health endpoint responds
- [ ] Returns HTTP 200

**Test Command**:
```bash
curl -f http://194.238.16.237:8002/health/
```

**Status**: ☐ Pass | ☐ Fail | **Response**: _______________________

---

#### Django CRM (Port 8003)
- [ ] Health endpoint responds
- [ ] Returns HTTP 200

**Test Command**:
```bash
curl -f http://194.238.16.237:8003/health/
```

**Status**: ☐ Pass | ☐ Fail | **Response**: _______________________

---

#### Business Directory API (Port 8004)
- [ ] Health endpoint responds
- [ ] Returns HTTP 200

**Test Command**:
```bash
curl -f http://194.238.16.237:8004/health
```

**Status**: ☐ Pass | ☐ Fail | **Response**: _______________________

---

#### CorelDove Backend (Port 8005)
- [ ] Health endpoint responds
- [ ] Returns HTTP 200
- [ ] Database connection confirmed

**Test Command**:
```bash
curl -f http://194.238.16.237:8005/health
```

**Status**: ☐ Pass | ☐ Fail | **Response**: _______________________

---

#### AI Agents Service (Port 8010)
- [ ] Health endpoint responds
- [ ] Returns HTTP 200
- [ ] AI models status shows "ready"

**Test Command**:
```bash
curl -f http://194.238.16.237:8010/health
```

**Status**: ☐ Pass | ☐ Fail | **Response**: _______________________

---

#### Amazon Sourcing API (Port 8085)
- [ ] Health endpoint responds
- [ ] Returns HTTP 200
- [ ] Amazon API connection confirmed

**Test Command**:
```bash
curl -f http://194.238.16.237:8085/health
```

**Status**: ☐ Pass | ☐ Fail | **Response**: _______________________

---

#### Saleor E-commerce (Port 8000)
- [ ] Health endpoint responds
- [ ] Returns HTTP 200

**Test Command**:
```bash
curl -f http://194.238.16.237:8000/health/
```

**Status**: ☐ Pass | ☐ Fail | **Response**: _______________________

---

### Infrastructure Connectivity Tests

#### PostgreSQL Connection
- [ ] Backend can connect to PostgreSQL
- [ ] Database queries successful

**Test Command**:
```bash
ssh root@194.238.16.237 'docker exec bizosaas-brain-staging nc -zv bizosaas-postgres-staging 5432'
```

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

#### Redis Connection
- [ ] Backend can connect to Redis
- [ ] Cache operations successful

**Test Command**:
```bash
ssh root@194.238.16.237 'docker exec bizosaas-brain-staging nc -zv bizosaas-redis-staging 6379'
```

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

#### Vault Connection
- [ ] Backend can connect to Vault
- [ ] Secrets accessible

**Test Command**:
```bash
ssh root@194.238.16.237 'docker exec bizosaas-brain-staging nc -zv bizosaas-vault-staging 8200'
```

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

#### Temporal Connection
- [ ] Backend can connect to Temporal
- [ ] Workflow engine accessible

**Test Command**:
```bash
ssh root@194.238.16.237 'docker exec bizosaas-brain-staging nc -zv bizosaas-temporal-server-staging 7233'
```

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

### Automated Verification Script

- [ ] Made script executable
- [ ] Ran verification script
- [ ] All checks passed
- [ ] No critical errors reported

**Execute Script**:
```bash
chmod +x /home/alagiri/projects/bizoholic/verify-backend-deployment.sh
./verify-backend-deployment.sh
```

**Script Output**:
- Total Backend Services: ___
- Containers Running: ___
- Health Checks Passed: ___
- Failed Services: ___

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

### Log Review

#### Brain API Logs (CRITICAL)
- [ ] No critical errors in logs
- [ ] Server started successfully
- [ ] Connected to all dependencies

**Check Command**:
```bash
ssh root@194.238.16.237 'docker logs bizosaas-brain-staging --tail 100 | grep -i error'
```

**Status**: ☐ Pass | ☐ Fail | **Issues Found**: _______________________

---

#### Other Services Logs
- [ ] Wagtail CMS: No critical errors
- [ ] Django CRM: No critical errors
- [ ] Directory API: No critical errors
- [ ] CorelDove Backend: No critical errors
- [ ] AI Agents: No critical errors
- [ ] Amazon Sourcing: No critical errors
- [ ] Saleor: No critical errors

**Check Command**:
```bash
ssh root@194.238.16.237 'for c in bizosaas-wagtail-staging bizosaas-django-crm-staging bizosaas-directory-api-staging coreldove-backend-staging bizosaas-ai-agents-staging amazon-sourcing-staging bizosaas-saleor-staging; do echo "=== $c ==="; docker logs $c --tail 20 | grep -i "error\|critical"; done'
```

**Status**: ☐ Pass | ☐ Fail | **Issues Found**: _______________________

---

### Resource Usage Check

- [ ] CPU usage < 50% per container
- [ ] Memory usage < 512MB per container
- [ ] No resource exhaustion warnings

**Check Command**:
```bash
ssh root@194.238.16.237 'docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | grep staging'
```

**Observed Usage**:
- Average CPU: ____%
- Average Memory: ____ MB
- Highest Consumer: _______________________

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

## INTEGRATION TESTING (5 minutes)

### Brain API Routing Test
- [ ] Brain API can route requests
- [ ] All backend services accessible through Brain API
- [ ] API gateway functioning properly

**Test Commands**:
```bash
# Test Brain API status
curl http://194.238.16.237:8001/health | jq .

# Expected: Shows connectivity to all services
```

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

### AI Services Test
- [ ] AI Agents service operational
- [ ] OpenRouter integration working
- [ ] Multi-model routing functional

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

### E-commerce Services Test
- [ ] CorelDove API operational
- [ ] Saleor engine running
- [ ] Payment gateways responding (test mode)

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

### CMS & CRM Test
- [ ] Wagtail CMS accessible
- [ ] Django CRM operational
- [ ] Directory API functional

**Status**: ☐ Pass | ☐ Fail | **Notes**: _______________________

---

## FINAL VALIDATION

### Overall Deployment Status

**Container Count**:
- Expected: 8 backend containers
- Running: ___ containers
- Healthy: ___ containers
- Failed: ___ containers

**Health Checks**:
- Expected: 8 passing
- Passing: ___ checks
- Failing: ___ checks

**Infrastructure Connectivity**:
- PostgreSQL: ☐ Connected | ☐ Failed
- Redis: ☐ Connected | ☐ Failed
- Vault: ☐ Connected | ☐ Failed
- Temporal: ☐ Connected | ☐ Failed

---

### Success Criteria Met

- [ ] All 8 containers running
- [ ] All 8 health checks passing
- [ ] All infrastructure connections working
- [ ] No critical errors in logs
- [ ] Resource usage acceptable
- [ ] Integration tests passing

**Overall Status**: ☐ **SUCCESS** | ☐ **PARTIAL** | ☐ **FAILED**

---

## ISSUES ENCOUNTERED

### Issue #1
**Description**: _________________________________________________
**Severity**: ☐ Critical | ☐ High | ☐ Medium | ☐ Low
**Resolution**: _________________________________________________
**Time to Resolve**: _____ minutes

### Issue #2
**Description**: _________________________________________________
**Severity**: ☐ Critical | ☐ High | ☐ Medium | ☐ Low
**Resolution**: _________________________________________________
**Time to Resolve**: _____ minutes

### Issue #3
**Description**: _________________________________________________
**Severity**: ☐ Critical | ☐ High | ☐ Medium | ☐ Low
**Resolution**: _________________________________________________
**Time to Resolve**: _____ minutes

---

## POST-DEPLOYMENT ACTIONS

### Documentation Updates
- [ ] Updated deployment notes
- [ ] Documented any issues and resolutions
- [ ] Recorded actual deployment time
- [ ] Noted any configuration changes

### Team Communication
- [ ] Notified team of successful deployment
- [ ] Shared any important observations
- [ ] Updated project status board
- [ ] Scheduled Phase 3 deployment

### Monitoring Setup
- [ ] Added containers to monitoring dashboard
- [ ] Configured alert thresholds
- [ ] Set up log aggregation
- [ ] Scheduled health check cron job

---

## NEXT STEPS

### Immediate (Today)
- [ ] Monitor containers for 1-2 hours
- [ ] Review logs for any warnings
- [ ] Test critical API endpoints
- [ ] Document deployment completion

### Short-term (This Week)
- [ ] Prepare for Phase 3 deployment
- [ ] Review frontend application configurations
- [ ] Plan domain configuration
- [ ] Schedule Phase 3 deployment time

### Phase 3 Preparation
- [ ] Review PHASE3_FRONTEND_DEPLOYMENT.md
- [ ] Prepare domain DNS records
- [ ] Plan SSL certificate setup
- [ ] Schedule deployment window

---

## DEPLOYMENT METRICS

**Total Deployment Time**: _____ minutes
- Preparation: _____ minutes
- Execution: _____ minutes
- Verification: _____ minutes
- Issue Resolution: _____ minutes

**Deployment Efficiency**:
- Expected time: 30 minutes
- Actual time: _____ minutes
- Efficiency: _____%

**Issues Encountered**: _____ total
- Critical: _____
- High: _____
- Medium: _____
- Low: _____

---

## SIGN-OFF

### Deployment Team
**Deployed By**: _____________________________ **Date**: __________
**Verified By**: _____________________________ **Date**: __________
**Approved By**: _____________________________ **Date**: __________

### Notes
________________________________________________________________
________________________________________________________________
________________________________________________________________
________________________________________________________________

---

## APPENDIX: QUICK COMMANDS

### View All Backend Containers
```bash
ssh root@194.238.16.237 'docker ps --filter "name=staging" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(brain|wagtail|django|directory|coreldove|ai-agents|amazon|saleor)"'
```

### Test All Health Endpoints
```bash
for port in 8001 8002 8003 8004 8005 8010 8085 8000; do
    echo "Testing port $port:"
    curl -f http://194.238.16.237:$port/health 2>/dev/null && echo " ✓" || echo " ✗"
done
```

### Check Resource Usage
```bash
ssh root@194.238.16.237 'docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | grep staging'
```

### View Recent Logs
```bash
ssh root@194.238.16.237 'docker logs bizosaas-brain-staging --tail 50'
```

### Restart Service
```bash
ssh root@194.238.16.237 'docker restart <container-name>'
```

---

**Checklist Version**: 1.0
**Last Updated**: October 10, 2025
**Phase**: 2 of 3

**Print this checklist and check items as you complete them!**
