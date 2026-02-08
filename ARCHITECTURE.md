# BizOSaaS Platform Architecture - Frontend & Service Containerization

## Current Architecture Overview

### Frontend Deployment Strategy

#### Development Environment (Current)
- **Bizoholic Frontend**: Running **OUTSIDE** container as Next.js dev server
  - Port: 3001
  - Process: Node.js process (PID-based)
  - Reason: Hot-reload, faster development iteration
  - Location: `brands/bizoholic/frontend`

#### Production Environment (Future)
- **Bizoholic Frontend**: Will run **INSIDE** container
  - Dockerfile: `brands/bizoholic/frontend/Dockerfile.production`
  - Build: Optimized Next.js production build
  - Benefits: Consistency, scalability, easier deployment

### Service Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Browser                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│         Bizoholic Frontend (Next.js)                         │
│         Port 3001 - DEV: Outside Container                   │
│                    PROD: Inside Container                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│         Brain API Gateway (FastAPI)                          │
│         Port 8000 - Centralized Routing                      │
│         Container: bizosaas-brain-unified                    │
└─────┬───────┬──────┬──────┬─────────────────────────────────┘
      │       │      │      │
      ▼       ▼      ▼      ▼
   ┌────┐ ┌────┐ ┌────┐ ┌─────────┐
   │Auth│ │CRM │ │Wag-│ │ Saleor  │
   │8007│ │8005│ │tail│ │  8001   │
   └────┘ └────┘ │8002│ └─────────┘
                  └────┘
```

### Embedded Admin Panels

All admin interfaces are **embedded** in the Client Portal, NOT accessed directly:

1. **Wagtail CMS Admin**
   - Direct URL: http://localhost:8002/admin/ (for debugging only)
   - **Portal URL**: http://localhost:3001/portal/dashboard/content
   - Embedded via iframe with X-Frame-Options: SAMEORIGIN

2. **Django CRM Admin**
   - Direct URL: http://localhost:8005/admin/ (for debugging only)
   - **Portal URL**: http://localhost:3001/portal/dashboard/crm
   - Embedded in portal dashboard

3. **Saleor Dashboard**
   - Direct URL: http://localhost:9000 (for debugging only)
   - **Portal URL**: http://localhost:3001/portal/dashboard/ecommerce
   - Embedded in portal dashboard

## Service Startup Issues - Fixed

### Issue 1: Wagtail CMS Not Started
**Problem**: Original script didn't include Wagtail CMS
**Fix**: Added `cms` to docker-compose service list
```bash
docker-compose up -d brain-gateway auth crm cms
```

### Issue 2: Auth Service Timing
**Problem**: Auth service needs more time to initialize
**Fix**: 
- Increased wait time from 30s to 35s
- Added retry logic with 3 attempts per service
- Better health check validation

### Issue 3: Service Recreation Logic
**Problem**: Script always stopped and recreated services, even if running
**Fix**: Added intelligent check:
```bash
RUNNING_SERVICES=$(docker ps --filter "name=bizosaas-*" --format "{{.Names}}" | wc -l)
if [ "$RUNNING_SERVICES" -gt 0 ]; then
    # Just restart if already running
    docker-compose restart brain-gateway auth crm cms
else
    # Full stop/remove/start if not running
    docker-compose up -d brain-gateway auth crm cms
fi
```

### Issue 4: Frontend Health Check
**Problem**: Frontend check was too quick, didn't account for Next.js startup time
**Fix**:
- Added 10-second wait before checks
- Retry logic with 3 attempts
- 2-second delay between retries

## Containerization Roadmap

### Phase 1: Development (Current)
- ✅ All backend services containerized
- ✅ Infrastructure containerized (Postgres, Redis, Vault)
- ⚠️ Frontend runs outside container for hot-reload

### Phase 2: Staging
- 🔄 Frontend containerized with production build
- 🔄 Multi-stage Docker builds for optimization
- 🔄 Docker Compose profiles for different environments

### Phase 3: Production
- 📋 Kubernetes deployment manifests
- 📋 Helm charts for easy deployment
- 📋 CI/CD pipeline with automated builds
- 📋 Container registry integration

## Why Frontend is Outside Container (Dev)

### Advantages
1. **Hot Module Replacement (HMR)**: Instant code updates without rebuild
2. **Faster Iteration**: No docker build step for every change
3. **Better Debugging**: Direct access to Node.js debugger
4. **File Watching**: Native file system watchers work better
5. **IDE Integration**: Better TypeScript/ESLint integration

### Disadvantages
1. **Environment Differences**: Dev vs prod parity
2. **Dependency Management**: Node modules on host
3. **Port Conflicts**: Manual port management

### When to Containerize Frontend

**Move to container when:**
- Deploying to staging/production
- Testing production builds
- Verifying Dockerfile works
- Running E2E tests in CI/CD
- Demonstrating to stakeholders

**Command to run containerized frontend:**
```bash
# Build production image
docker build -t bizoholic-frontend:latest -f brands/bizoholic/frontend/Dockerfile.production brands/bizoholic/frontend

# Run container
docker run -p 3001:3000 \
  -e NEXT_PUBLIC_API_BASE_URL=http://localhost:8000 \
  -e NEXT_PUBLIC_WAGTAIL_URL=http://localhost:8002/admin \
  bizoholic-frontend:latest
```

## Service Health Check Endpoints

| Service | Port | Health Endpoint | Expected Response |
|---------|------|----------------|-------------------|
| Frontend | 3001 | / | HTML page |
| Brain API | 8000 | /health | `{"status":"healthy"}` |
| Auth | 8007 | /health | `{"status":"healthy"}` |
| CRM | 8005 | /health | HTML or JSON |
| Wagtail | 8002 | /health/ | `{"status":"healthy"}` |

## Troubleshooting

### Auth Service Not Responding
```bash
# Check logs
docker logs bizosaas-auth-unified --tail 50

# Restart with fresh database connection
docker-compose -f shared/services/docker-compose.services.yml restart auth

# If still failing, check database
docker exec bizosaas-postgres-unified psql -U postgres -c "\l"
```

### Frontend Not Responding
```bash
# Check if process is running
ps aux | grep "next.*3001"

# Check logs
tail -f /tmp/bizoholic-frontend.log

# Kill and restart
pkill -f "next.*3001"
cd brands/bizoholic/frontend && PORT=3001 npm run dev
```

### Wagtail Not Accessible
```bash
# Check container status
docker ps | grep wagtail

# Check logs
docker logs bizosaas-wagtail-unified --tail 50

# Verify migrations
docker exec bizosaas-wagtail-unified python manage.py showmigrations

# Restart
docker-compose -f shared/services/docker-compose.services.yml restart cms
```

## Best Practices

1. **Always use the startup script** instead of manual docker-compose commands
2. **Check service status** before assuming failures (script now has retries)
3. **Use embedded admin panels** through portal, not direct URLs
4. **Keep frontend outside container** during active development
5. **Containerize frontend** before deploying to staging/production
6. **Monitor logs** in `/tmp/bizoholic-frontend.log` for frontend issues
7. **Wait for services** - some services (Auth, Wagtail) need 30+ seconds to fully initialize

## Next Steps

1. ✅ Fixed startup script to include Wagtail
2. ✅ Added intelligent service restart logic
3. ✅ Improved health checks with retries
4. 🔄 Create production Dockerfile for frontend
5. 🔄 Add Docker Compose profiles (dev/staging/prod)
6. 🔄 Implement proper logging aggregation
7. 🔄 Add monitoring with Prometheus/Grafana
