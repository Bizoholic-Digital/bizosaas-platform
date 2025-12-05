# Phase 2: Backend Services Deployment to Dokploy

## Overview
This guide covers the deployment of 8 backend service containers to Dokploy staging environment.

**Deployment Date**: October 10, 2025
**VPS IP**: 194.238.16.237
**Dokploy URL**: http://194.238.16.237:3000
**Project Name**: bizosaas-backend-staging
**Configuration File**: dokploy-backend-staging.yml

---

## Prerequisites

### 1. Infrastructure Project Must Be Running
Before starting Phase 2, verify that Phase 1 infrastructure is operational:

```bash
# SSH to VPS
ssh root@194.238.16.237

# Check infrastructure containers
docker ps --filter "name=staging" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Expected infrastructure containers:
# - bizosaas-postgres-staging (healthy, port 5432)
# - bizosaas-redis-staging (healthy, port 6379)
# - bizosaas-vault-staging (healthy, port 8200)
# - bizosaas-temporal-server-staging (healthy, port 7233)
# - bizosaas-temporal-ui-staging (healthy, port 8082)
# - bizosaas-temporal-integration-staging (healthy, port 8009)
```

### 2. Required Environment Variables
Gather these API keys before deployment:

**AI Service Keys:**
- `OPENROUTER_API_KEY` - OpenRouter API for multi-model AI routing
- `OPENAI_API_KEY` - OpenAI GPT models
- `ANTHROPIC_API_KEY` - Claude models

**Payment Gateway Keys:**
- `STRIPE_SECRET_KEY` - Stripe payment processing
- `PAYPAL_CLIENT_ID` - PayPal payments client ID
- `PAYPAL_CLIENT_SECRET` - PayPal payments secret

**Integration Keys:**
- `AMAZON_ACCESS_KEY` - Amazon product sourcing access key
- `AMAZON_SECRET_KEY` - Amazon product sourcing secret key

### 3. Verify Network Exists
```bash
# Check if staging network exists
docker network ls | grep bizosaas-staging-network

# If not exists, create it:
docker network create bizosaas-staging-network
```

---

## Deployment Steps

### Step 1: Access Dokploy Dashboard

1. Open browser and navigate to: `http://194.238.16.237:3000`
2. Login with your Dokploy admin credentials
3. Verify you see the existing `bizosaas-infrastructure-staging` project

### Step 2: Create Backend Services Project

1. **Click "Projects"** in left sidebar
2. **Click "New Project"** button (top right)
3. **Enter project details:**
   - **Name**: `bizosaas-backend-staging`
   - **Description**: `Backend services and APIs for staging environment`
   - **Admin Name**: (leave default)
4. **Click "Create Project"**

### Step 3: Configure Docker Compose Application

1. **Click on `bizosaas-backend-staging`** project to enter it
2. **Click "New Application"** button
3. **Select "Docker Compose"** as application type
4. **Enter application details:**
   - **Name**: `backend-services`
   - **Description**: `8 backend API services`

### Step 4: Upload Docker Compose Configuration

1. **In the application configuration screen:**
   - Locate the "Compose File" section
   - **Option A - Upload File:**
     - Click "Upload File" button
     - Select `/home/alagiri/projects/bizoholic/dokploy-backend-staging.yml`

   - **Option B - Copy/Paste:**
     - Copy content from `dokploy-backend-staging.yml`
     - Paste into the text editor

2. **Verify the configuration** shows these services:
   - brain-api (bizosaas-brain-staging)
   - wagtail-cms (bizosaas-wagtail-staging)
   - django-crm (bizosaas-django-crm-staging)
   - business-directory-api (bizosaas-directory-api-staging)
   - coreldove-backend (coreldove-backend-staging)
   - ai-agents (bizosaas-ai-agents-staging)
   - amazon-sourcing (amazon-sourcing-staging)
   - saleor-api (bizosaas-saleor-staging)

### Step 5: Configure Environment Variables

1. **Click "Environment Variables"** tab
2. **Add the following variables** (one by one):

```bash
# AI Service Keys
OPENROUTER_API_KEY=<your-openrouter-key>
OPENAI_API_KEY=<your-openai-key>
ANTHROPIC_API_KEY=<your-anthropic-key>

# Payment Gateway Keys
STRIPE_SECRET_KEY=<your-stripe-secret-key>
PAYPAL_CLIENT_ID=<your-paypal-client-id>
PAYPAL_CLIENT_SECRET=<your-paypal-client-secret>

# Integration Keys
AMAZON_ACCESS_KEY=<your-amazon-access-key>
AMAZON_SECRET_KEY=<your-amazon-secret-key>
```

**IMPORTANT NOTES:**
- Do NOT include the angle brackets `< >` in actual values
- Keep these keys secure and never commit to version control
- Use production-grade keys for staging (test mode keys where available)

### Step 6: Configure Build Settings

1. **Build Settings** (if not auto-configured):
   - **Repository**: https://github.com/Bizoholic-Digital/bizosaas-platform.git
   - **Branch**: main (or staging branch if exists)
   - **Build Context**: ./ (root)

2. **Docker Registry** (optional):
   - Leave as default (Dokploy will build locally)
   - Or configure private registry if available

### Step 7: Deploy the Application

1. **Review configuration** one final time
2. **Click "Deploy"** button (top right)
3. **Monitor deployment progress:**
   - Watch the logs in real-time
   - Deployment will take 10-15 minutes
   - Multiple services will build in sequence

### Step 8: Monitor Deployment Progress

Watch for these deployment stages:

1. **Network Creation**: `bizosaas-staging-network` (should already exist)
2. **Image Building**: Each service builds from GitHub repository
3. **Container Startup**: Services start with dependency order
4. **Health Checks**: Each service runs health check probes

**Expected Build Order:**
1. PostgreSQL and Redis (already running from Phase 1)
2. Vault and Temporal (already running from Phase 1)
3. Brain API (main coordinator)
4. Wagtail CMS
5. Django CRM
6. Business Directory API
7. CorelDove Backend
8. AI Agents Service
9. Amazon Sourcing API
10. Saleor E-commerce

---

## Post-Deployment Verification

### Step 9: Verify Container Status

1. **In Dokploy Dashboard:**
   - Navigate to `bizosaas-backend-staging` project
   - Click on `backend-services` application
   - Check "Containers" tab
   - Verify all 8 containers show "Running" status

2. **SSH to VPS and verify:**

```bash
# List all backend containers
docker ps --filter "name=staging" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(brain|wagtail|django-crm|directory|coreldove|ai-agents|amazon|saleor)"

# Expected output (8 containers):
# bizosaas-brain-staging         Up XX minutes (healthy)   0.0.0.0:8001->8001/tcp
# bizosaas-wagtail-staging       Up XX minutes (healthy)   0.0.0.0:8002->8002/tcp
# bizosaas-django-crm-staging    Up XX minutes (healthy)   0.0.0.0:8003->8003/tcp
# bizosaas-directory-api-staging Up XX minutes (healthy)   0.0.0.0:8004->8004/tcp
# coreldove-backend-staging      Up XX minutes (healthy)   0.0.0.0:8005->8005/tcp
# bizosaas-ai-agents-staging     Up XX minutes (healthy)   0.0.0.0:8010->8010/tcp
# amazon-sourcing-staging        Up XX minutes (healthy)   0.0.0.0:8085->8085/tcp
# bizosaas-saleor-staging        Up XX minutes (healthy)   0.0.0.0:8000->8000/tcp
```

### Step 10: Health Check Testing

Test each service's health endpoint:

```bash
# 1. Brain API (Most Critical - Main Hub)
curl -f http://194.238.16.237:8001/health
# Expected: {"status": "healthy", "services": [...]}

# 2. Wagtail CMS
curl -f http://194.238.16.237:8002/health/
# Expected: {"status": "ok"}

# 3. Django CRM
curl -f http://194.238.16.237:8003/health/
# Expected: {"status": "healthy"}

# 4. Business Directory API
curl -f http://194.238.16.237:8004/health
# Expected: {"status": "ok"}

# 5. CorelDove Backend
curl -f http://194.238.16.237:8005/health
# Expected: {"status": "healthy", "database": "connected"}

# 6. AI Agents Service
curl -f http://194.238.16.237:8010/health
# Expected: {"status": "healthy", "ai_models": "ready"}

# 7. Amazon Sourcing API
curl -f http://194.238.16.237:8085/health
# Expected: {"status": "ok", "amazon_api": "connected"}

# 8. Saleor E-commerce
curl -f http://194.238.16.237:8000/health/
# Expected: {"status": "ok"}
```

### Step 11: Service Connectivity Verification

Verify services can communicate with infrastructure:

```bash
# Check Brain API can connect to all dependencies
curl http://194.238.16.237:8001/health | jq .

# Expected JSON output showing:
# - postgres: connected
# - redis: connected
# - vault: accessible
# - temporal: connected
```

### Step 12: Check Service Logs

1. **In Dokploy Dashboard:**
   - Click on each service
   - View "Logs" tab
   - Verify no critical errors

2. **Via SSH:**

```bash
# Check Brain API logs (most important)
docker logs bizosaas-brain-staging --tail 100

# Check for successful startup messages:
# - "Server started on port 8001"
# - "Connected to PostgreSQL"
# - "Connected to Redis"
# - "Temporal client initialized"

# Check other services
docker logs bizosaas-wagtail-staging --tail 50
docker logs bizosaas-django-crm-staging --tail 50
docker logs bizosaas-ai-agents-staging --tail 50
```

---

## Service Architecture

### Backend Services Overview

#### 1. AI Central Hub (Brain API) - Port 8001
**Purpose**: Main API coordinator and router
**Key Features**:
- Central request routing
- API gateway functionality
- Orchestrates all backend services
- Health monitoring dashboard

**Critical Dependencies**:
- PostgreSQL (tenant data, routing rules)
- Redis (request caching, rate limiting)
- Vault (API key management)
- Temporal (workflow orchestration)

#### 2. Wagtail CMS - Port 8002
**Purpose**: Headless content management system
**Key Features**:
- Content creation and management
- Rich text editor
- Media library
- API for frontend consumption

#### 3. Django CRM - Port 8003
**Purpose**: Customer relationship management
**Key Features**:
- Client management
- Lead tracking
- Contact management
- Sales pipeline

#### 4. Business Directory API - Port 8004
**Purpose**: Business directory management
**Key Features**:
- Business listing CRUD
- Search functionality
- Category management
- Review system

#### 5. CorelDove Backend - Port 8005
**Purpose**: Custom e-commerce API
**Key Features**:
- Product catalog
- Order management
- Payment processing (Stripe, PayPal)
- Inventory tracking

#### 6. AI Agents Service - Port 8010
**Purpose**: Multi-model AI coordination
**Key Features**:
- OpenRouter integration
- Multi-model AI routing
- Agent orchestration
- Temporal workflow integration

#### 7. Amazon Sourcing API - Port 8085
**Purpose**: Product sourcing integration
**Key Features**:
- Amazon product search
- Price comparison
- Product data enrichment
- Inventory sync

#### 8. Saleor E-commerce - Port 8000
**Purpose**: Advanced e-commerce platform
**Key Features**:
- Full-featured e-commerce
- GraphQL API
- Multi-channel support
- Advanced inventory management

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                           │
│         (Phase 3 - Will connect to these APIs)              │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               AI CENTRAL HUB (BRAIN API)                    │
│                    Port 8001                                │
│         Main API Gateway & Request Router                   │
└─────────────────────────────────────────────────────────────┘
                            ▼
        ┌──────────────────┴──────────────────┐
        │                                     │
┌───────▼────────┐                 ┌──────────▼─────────┐
│  CMS SERVICES  │                 │  COMMERCE SERVICES │
├────────────────┤                 ├────────────────────┤
│ Wagtail (8002) │                 │ CorelDove (8005)   │
│ Django CRM     │                 │ Saleor (8000)      │
│ (8003)         │                 │ Amazon (8085)      │
│ Directory      │                 │                    │
│ (8004)         │                 │                    │
└────────────────┘                 └────────────────────┘
                            │
                  ┌─────────▼─────────┐
                  │   AI SERVICES     │
                  ├───────────────────┤
                  │ AI Agents (8010)  │
                  │ OpenRouter        │
                  │ Multi-Model AI    │
                  └───────────────────┘
                            │
┌───────────────────────────▼───────────────────────────┐
│           INFRASTRUCTURE LAYER (Phase 1)              │
├───────────────────────────────────────────────────────┤
│ PostgreSQL | Redis | Vault | Temporal                │
└───────────────────────────────────────────────────────┘
```

---

## Troubleshooting

### Issue 1: Container Fails to Start

**Symptoms**: Container shows "Exited" or "Restarting" status

**Solutions**:

1. **Check logs for specific error:**
```bash
docker logs <container-name> --tail 200
```

2. **Common causes:**
   - **Database connection failed**: Verify infrastructure project is running
   - **Environment variable missing**: Check all required env vars are set
   - **Port conflict**: Ensure no other service uses the same port
   - **Build failure**: Check GitHub repository access

3. **Restart specific container:**
```bash
docker restart <container-name>
```

### Issue 2: Health Check Failing

**Symptoms**: Container running but health check returns error

**Solutions**:

1. **Check service-specific health endpoint:**
```bash
# Get container IP
docker inspect <container-name> | grep IPAddress

# Test health endpoint directly
curl http://<container-ip>:<internal-port>/health
```

2. **Common causes:**
   - **Database migrations pending**: Run migrations manually
   - **Redis connection timeout**: Check Redis connectivity
   - **API key invalid**: Verify environment variables

### Issue 3: Service Cannot Connect to Infrastructure

**Symptoms**: "Connection refused" or "Host not found" errors

**Solutions**:

1. **Verify network membership:**
```bash
docker network inspect bizosaas-staging-network
# Ensure both infrastructure and backend containers are listed
```

2. **Test connectivity:**
```bash
# From inside backend container
docker exec bizosaas-brain-staging ping bizosaas-postgres-staging
docker exec bizosaas-brain-staging nc -zv bizosaas-postgres-staging 5432
```

3. **Verify DNS resolution:**
```bash
docker exec bizosaas-brain-staging nslookup bizosaas-postgres-staging
```

### Issue 4: Build Failures

**Symptoms**: Deployment fails during image building

**Solutions**:

1. **Check GitHub repository access:**
```bash
git ls-remote https://github.com/Bizoholic-Digital/bizosaas-platform.git
```

2. **Verify Dockerfile paths:**
   - Ensure each Dockerfile exists in specified path
   - Check for typos in context paths

3. **Review build logs in Dokploy:**
   - Navigate to application → Build Logs
   - Look for specific error messages

### Issue 5: Environment Variables Not Applied

**Symptoms**: Service complains about missing configuration

**Solutions**:

1. **Verify in Dokploy:**
   - Check Environment Variables tab
   - Ensure no typos in variable names

2. **Test variable availability:**
```bash
docker exec bizosaas-brain-staging env | grep API_KEY
```

3. **Redeploy with new variables:**
   - Update variables in Dokploy
   - Click "Redeploy" button

---

## Performance Monitoring

### Key Metrics to Monitor

1. **Container Resource Usage:**
```bash
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

2. **Service Response Times:**
```bash
# Test API response time
time curl http://194.238.16.237:8001/health
```

3. **Database Connection Pool:**
```bash
# Check PostgreSQL connections
docker exec bizosaas-postgres-staging psql -U admin -d bizosaas_staging -c "SELECT count(*) FROM pg_stat_activity;"
```

### Expected Performance Baselines

- **Brain API Response**: < 100ms
- **CMS Services Response**: < 200ms
- **Commerce Services Response**: < 300ms
- **AI Agents Response**: < 1000ms (depends on AI model)
- **Memory Usage per Container**: 200-500MB
- **CPU Usage per Container**: 5-15%

---

## Security Checklist

- [ ] All API keys stored in Dokploy environment variables (not in code)
- [ ] Database credentials use strong passwords
- [ ] Services only expose necessary ports
- [ ] No DEBUG mode in production-like staging
- [ ] SSL/TLS for all external communication
- [ ] Network isolation between projects
- [ ] Container user is non-root where possible
- [ ] Regular security updates applied

---

## Next Steps

### Phase 3: Frontend Applications Deployment

Once all backend services are verified healthy:

1. **Proceed to Phase 3**: Frontend applications deployment
2. **Configuration File**: `dokploy-frontend-staging.yml`
3. **Deployment Guide**: `PHASE3_FRONTEND_DEPLOYMENT.md`
4. **Domain Configuration**: Setup staging subdomains

### Integration Testing

Before Phase 3, test backend API endpoints:

```bash
# Test Brain API routing
curl -X POST http://194.238.16.237:8001/api/test-routing

# Test CMS content API
curl http://194.238.16.237:8002/api/v2/pages/

# Test CRM API
curl http://194.238.16.237:8003/api/clients/

# Test Commerce API
curl http://194.238.16.237:8005/api/products/
```

---

## Success Criteria

Phase 2 deployment is successful when:

- [ ] All 8 backend containers are running
- [ ] All health checks return "healthy" status
- [ ] Brain API can route to all services
- [ ] Services can connect to infrastructure (PostgreSQL, Redis, Vault, Temporal)
- [ ] No critical errors in container logs
- [ ] API endpoints respond within acceptable time limits
- [ ] Environment variables are properly configured
- [ ] Resource usage is within expected ranges

**Once all criteria are met, you are ready for Phase 3: Frontend Applications Deployment!**

---

## Support & Resources

### Dokploy Documentation
- Official Docs: https://docs.dokploy.com
- Docker Compose Guide: https://docs.dokploy.com/docker-compose

### Project Resources
- GitHub Repository: https://github.com/Bizoholic-Digital/bizosaas-platform
- Infrastructure Guide: `PHASE1_INFRASTRUCTURE_DEPLOYMENT.md`
- Master Deployment Guide: `DOKPLOY_DEPLOYMENT_GUIDE.md`

### Emergency Contacts
- DevOps Team: (contact info)
- VPS Provider Support: (provider support)
- Dokploy Community: Discord/Forum

---

**Deployment Guide Version**: 1.0
**Last Updated**: October 10, 2025
**Next Review**: October 17, 2025

**Generated with Claude Code - BizOSaaS Platform Deployment Automation**
