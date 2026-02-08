# Phase 2: Backend Services - Quick Reference Card

## Overview
**Project Name**: bizosaas-backend-staging
**Container Count**: 8 backend services
**Deployment Time**: 10-15 minutes
**Configuration**: dokploy-backend-staging.yml

---

## Pre-Deployment Checklist

- [ ] Phase 1 infrastructure is running (6 containers)
- [ ] Network `bizosaas-staging-network` exists
- [ ] API keys collected for all services
- [ ] Dokploy dashboard accessible at http://194.238.16.237:3000

---

## Required Environment Variables

```bash
# AI Services (3 keys)
OPENROUTER_API_KEY=<your-key>
OPENAI_API_KEY=<your-key>
ANTHROPIC_API_KEY=<your-key>

# Payment Gateways (3 keys)
STRIPE_SECRET_KEY=<your-key>
PAYPAL_CLIENT_ID=<your-key>
PAYPAL_CLIENT_SECRET=<your-key>

# Integrations (2 keys)
AMAZON_ACCESS_KEY=<your-key>
AMAZON_SECRET_KEY=<your-key>
```

---

## 8 Backend Services

| Service | Container Name | Port | Purpose |
|---------|---------------|------|---------|
| Brain API | bizosaas-brain-staging | 8001 | Main API hub |
| Wagtail CMS | bizosaas-wagtail-staging | 8002 | Content management |
| Django CRM | bizosaas-django-crm-staging | 8003 | Customer management |
| Directory API | bizosaas-directory-api-staging | 8004 | Business directory |
| CorelDove API | coreldove-backend-staging | 8005 | E-commerce API |
| AI Agents | bizosaas-ai-agents-staging | 8010 | AI coordination |
| Amazon Sourcing | amazon-sourcing-staging | 8085 | Product sourcing |
| Saleor Engine | bizosaas-saleor-staging | 8000 | Advanced e-commerce |

---

## Quick Deployment Steps

### 1. Access Dokploy
```
URL: http://194.238.16.237:3000
Login with admin credentials
```

### 2. Create Project
```
Name: bizosaas-backend-staging
Description: Backend services and APIs for staging environment
```

### 3. Create Application
```
Type: Docker Compose
Name: backend-services
Upload: dokploy-backend-staging.yml
```

### 4. Add Environment Variables
Copy all 8 environment variables from above section

### 5. Deploy
Click "Deploy" button and monitor progress

### 6. Verify
Run verification script:
```bash
./verify-backend-deployment.sh
```

---

## Health Check URLs

```bash
# Primary - Brain API
curl http://194.238.16.237:8001/health

# CMS Services
curl http://194.238.16.237:8002/health/
curl http://194.238.16.237:8003/health/

# Business Services
curl http://194.238.16.237:8004/health
curl http://194.238.16.237:8005/health

# AI & Integration
curl http://194.238.16.237:8010/health
curl http://194.238.16.237:8085/health

# E-commerce
curl http://194.238.16.237:8000/health/
```

---

## Common Issues & Quick Fixes

### Container Won't Start
```bash
# Check logs
ssh root@194.238.16.237 'docker logs <container-name> --tail 100'

# Restart container
ssh root@194.238.16.237 'docker restart <container-name>'
```

### Database Connection Failed
```bash
# Verify infrastructure running
ssh root@194.238.16.237 'docker ps | grep postgres'

# Test connectivity
ssh root@194.238.16.237 'docker exec bizosaas-brain-staging nc -zv bizosaas-postgres-staging 5432'
```

### Missing Environment Variables
```bash
# Check variables in container
ssh root@194.238.16.237 'docker exec <container-name> env | grep API_KEY'

# Update in Dokploy and redeploy
```

### Network Issues
```bash
# Check network exists
ssh root@194.238.16.237 'docker network ls | grep staging'

# Inspect network
ssh root@194.238.16.237 'docker network inspect bizosaas-staging-network'
```

---

## Verification Commands

### Check All Containers
```bash
ssh root@194.238.16.237 'docker ps --filter "name=staging" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
```

### Test All Health Endpoints
```bash
for port in 8001 8002 8003 8004 8005 8010 8085 8000; do
    echo "Port $port:"
    curl -s http://194.238.16.237:$port/health | head -1
done
```

### Monitor Resource Usage
```bash
ssh root@194.238.16.237 'docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | grep staging'
```

---

## Success Criteria

All of these must be true:

- [ ] All 8 containers show "Running" status
- [ ] All health checks return HTTP 200
- [ ] Brain API responds at port 8001
- [ ] No critical errors in logs
- [ ] Services can connect to PostgreSQL
- [ ] Services can connect to Redis
- [ ] CPU usage < 20% per container
- [ ] Memory usage < 512MB per container

---

## Next Steps

After successful deployment:

1. **Verify All Services**: Run `./verify-backend-deployment.sh`
2. **Check Logs**: Review logs for any warnings
3. **Test APIs**: Test key endpoints manually
4. **Proceed to Phase 3**: Frontend applications deployment

---

## Key Files

- **Deployment Guide**: `PHASE2_BACKEND_DEPLOYMENT.md`
- **Configuration**: `dokploy-backend-staging.yml`
- **Verification Script**: `verify-backend-deployment.sh`
- **Master Guide**: `DOKPLOY_DEPLOYMENT_GUIDE.md`

---

## Support Resources

### Documentation
- Phase 1 Guide: `PHASE1_INFRASTRUCTURE_DEPLOYMENT.md`
- Phase 3 Guide: `PHASE3_FRONTEND_DEPLOYMENT.md` (coming next)
- Dokploy Docs: https://docs.dokploy.com

### Monitoring
- Dokploy Dashboard: http://194.238.16.237:3000
- Temporal UI: http://194.238.16.237:8082
- Vault UI: http://194.238.16.237:8200

---

## Emergency Commands

### Stop All Backend Services
```bash
ssh root@194.238.16.237 'docker stop $(docker ps -q --filter "name=brain") $(docker ps -q --filter "name=wagtail") $(docker ps -q --filter "name=django-crm") $(docker ps -q --filter "name=directory") $(docker ps -q --filter "name=coreldove-backend") $(docker ps -q --filter "name=ai-agents") $(docker ps -q --filter "name=amazon-sourcing") $(docker ps -q --filter "name=saleor")'
```

### Restart All Backend Services
```bash
ssh root@194.238.16.237 'docker restart $(docker ps -q --filter "name=staging" | grep -E "brain|wagtail|django|directory|coreldove|ai-agents|amazon|saleor")'
```

### View All Logs
```bash
ssh root@194.238.16.237 'for container in bizosaas-brain-staging bizosaas-wagtail-staging bizosaas-django-crm-staging bizosaas-directory-api-staging coreldove-backend-staging bizosaas-ai-agents-staging amazon-sourcing-staging bizosaas-saleor-staging; do echo "=== $container ==="; docker logs $container --tail 20; done'
```

---

**Version**: 1.0
**Last Updated**: October 10, 2025
**Deployment Phase**: 2 of 3

**Quick Start**: Follow steps 1-6, then run verification script!
