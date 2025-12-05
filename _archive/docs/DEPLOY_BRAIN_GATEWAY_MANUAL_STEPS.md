# Manual Deployment Steps for Brain Gateway v2.1.0-HITL to VPS

Since automated SSH deployment requires credentials, here are the manual steps to deploy the Brain Gateway with HITL to VPS staging.

## Prerequisites
- SSH access to VPS: `root@194.238.16.237`
- Docker installed on VPS
- Network: `dokploy-network` exists on VPS

---

## Option 1: Transfer Docker Image (Recommended)

### Step 1: Save Image Locally
```bash
# Already completed - image exists locally
docker images | grep brain-gateway
# Output: bizosaas/brain-gateway  v2.1.0-hitl  a98a1d7e07b0  176MB
```

### Step 2: Save to Tar File
```bash
cd /tmp
docker save bizosaas/brain-gateway:v2.1.0-hitl | gzip > brain-gateway-v2.1.0-hitl.tar.gz
ls -lh brain-gateway-v2.1.0-hitl.tar.gz
```

### Step 3: Transfer to VPS
```bash
# Using SCP
scp /tmp/brain-gateway-v2.1.0-hitl.tar.gz root@194.238.16.237:/tmp/

# Or using rsync for resume capability
rsync -avz --progress /tmp/brain-gateway-v2.1.0-hitl.tar.gz root@194.238.16.237:/tmp/
```

### Step 4: SSH to VPS and Load Image
```bash
ssh root@194.238.16.237

# Load the image
docker load < /tmp/brain-gateway-v2.1.0-hitl.tar.gz

# Verify image loaded
docker images | grep brain-gateway

# Clean up
rm /tmp/brain-gateway-v2.1.0-hitl.tar.gz
```

### Step 5: Stop Old Container (if exists)
```bash
# Check if container exists
docker ps -a --filter name=bizosaas-brain-staging

# Stop and remove
docker stop bizosaas-brain-staging 2>/dev/null || true
docker rm bizosaas-brain-staging 2>/dev/null || true
```

### Step 6: Start New Container
```bash
docker run -d \
  --name bizosaas-brain-staging \
  --network dokploy-network \
  -p 8001:8001 \
  -e REDIS_URL=redis://194.238.16.237:6380/0 \
  -e DATABASE_URL=postgresql://admin:BizOSaaS2025\!StagingDB@194.238.16.237:5433/bizosaas_staging \
  -e ENVIRONMENT=staging \
  -e LOG_LEVEL=INFO \
  --restart unless-stopped \
  bizosaas/brain-gateway:v2.1.0-hitl
```

### Step 7: Verify Deployment
```bash
# Check container status
docker ps --filter name=bizosaas-brain-staging

# View logs
docker logs bizosaas-brain-staging --tail 30

# Test health endpoint
curl -s http://localhost:8001/health | jq .

# Test HITL workflows
curl -s http://localhost:8001/api/brain/hitl/workflows | jq '.total'
```

---

## Option 2: Use Docker Compose (Alternative)

### Step 1: Update Deployment File on VPS
```bash
# SSH to VPS
ssh root@194.238.16.237

# Navigate to deployment directory
cd /opt/bizosaas  # or wherever your docker-compose files are

# Create or update the deployment file
nano dokploy-backend-staging.yml
```

### Step 2: Update Brain API Service Section
Replace the brain-api service definition with:
```yaml
  brain-api:
    image: bizosaas/brain-gateway:v2.1.0-hitl
    container_name: bizosaas-brain-staging
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://admin:BizOSaaS2025!StagingDB@194.238.16.237:5433/bizosaas_staging
      - REDIS_URL=redis://194.238.16.237:6380/0
      - OPENAI_API_KEY=${OPENAI_API_KEY:-}
      - ENVIRONMENT=staging
      - LOG_LEVEL=INFO
    networks:
      - dokploy-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Step 3: Load Image (from Option 1)
```bash
# Load the transferred image
docker load < /tmp/brain-gateway-v2.1.0-hitl.tar.gz
```

### Step 4: Deploy with Docker Compose
```bash
# Deploy just the brain-api service
docker-compose -f dokploy-backend-staging.yml up -d brain-api

# Or restart all services
docker-compose -f dokploy-backend-staging.yml up -d
```

---

## Option 3: Push to Container Registry (Future)

If you have access to GitHub Container Registry:

### Local Machine:
```bash
# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin

# Tag for registry
docker tag bizosaas/brain-gateway:v2.1.0-hitl ghcr.io/YOUR_GITHUB_USERNAME/bizosaas-brain-gateway:v2.1.0-hitl

# Push to registry
docker push ghcr.io/YOUR_GITHUB_USERNAME/bizosaas-brain-gateway:v2.1.0-hitl
```

### VPS:
```bash
# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin

# Pull image
docker pull ghcr.io/YOUR_GITHUB_USERNAME/bizosaas-brain-gateway:v2.1.0-hitl

# Tag locally
docker tag ghcr.io/YOUR_GITHUB_USERNAME/bizosaas-brain-gateway:v2.1.0-hitl bizosaas/brain-gateway:v2.1.0-hitl

# Deploy (use steps from Option 1)
```

---

## Verification Checklist

After deployment, verify these:

### 1. Container Status
```bash
docker ps --filter name=bizosaas-brain-staging --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```
**Expected**: Container running with port 8001 exposed

### 2. Health Check
```bash
curl -s http://localhost:8001/health
```
**Expected**:
```json
{
  "status": "healthy",
  "service": "bizosaas-brain-core",
  "timestamp": "2025-10-14T...",
  "tenant_registry": "active",
  "services_registered": 13
}
```

### 3. HITL Workflows
```bash
curl -s http://localhost:8001/api/brain/hitl/workflows
```
**Expected**: JSON with 8 workflows configured

### 4. Service Registry
```bash
curl -s http://localhost:8001/services
```
**Expected**: 13 backend services listed

### 5. Test Toggle Functionality
```bash
# Enable HITL
curl -X POST "http://localhost:8001/api/brain/hitl/workflows/campaign_optimization/toggle?enabled=true"

# Verify change
curl -s http://localhost:8001/api/brain/hitl/workflows/campaign_optimization | jq '.hitl_enabled'

# Disable HITL
curl -X POST "http://localhost:8001/api/brain/hitl/workflows/campaign_optimization/toggle?enabled=false"
```

### 6. External Access (if configured)
```bash
# From local machine
curl -s http://194.238.16.237:8001/health

# Test HITL endpoints
curl -s http://194.238.16.237:8001/api/brain/hitl/workflows
```

---

## Troubleshooting

### Issue: Container won't start
```bash
# Check logs
docker logs bizosaas-brain-staging

# Common issues:
# 1. Port 8001 already in use
docker ps | grep 8001

# 2. Network doesn't exist
docker network ls | grep dokploy-network
docker network create dokploy-network  # if needed

# 3. Image not found
docker images | grep brain-gateway
```

### Issue: Redis connection failed
```bash
# Check Redis accessibility from container
docker exec bizosaas-brain-staging ping -c 2 194.238.16.237

# Test Redis directly
docker exec bizosaas-brain-staging curl -s http://194.238.16.237:6380/

# Note: HITL system works without Redis (in-memory fallback)
```

### Issue: Database connection failed
```bash
# Check PostgreSQL accessibility
docker exec bizosaas-brain-staging nc -zv 194.238.16.237 5433

# Verify credentials in environment
docker exec bizosaas-brain-staging env | grep DATABASE_URL
```

### Issue: Health check failing
```bash
# Check if service is listening
docker exec bizosaas-brain-staging netstat -tlnp | grep 8001

# Test health endpoint from inside container
docker exec bizosaas-brain-staging curl -f http://localhost:8001/health

# Check application logs
docker logs bizosaas-brain-staging --tail 50 -f
```

---

## Rollback Plan

If deployment fails, rollback to previous version:

```bash
# Stop new container
docker stop bizosaas-brain-staging
docker rm bizosaas-brain-staging

# Restart old container (if it exists)
docker start bizosaas-brain-staging-old

# Or rebuild from GitHub
docker-compose -f dokploy-backend-staging.yml up -d brain-api --build
```

---

## Post-Deployment Tasks

After successful deployment:

1. **Update Documentation**
   - Record deployment timestamp
   - Document any configuration changes
   - Update architecture diagrams

2. **Monitor Initial Performance**
   - Watch logs for errors: `docker logs -f bizosaas-brain-staging`
   - Monitor CPU/memory: `docker stats bizosaas-brain-staging`
   - Check response times: `curl -w "@curl-format.txt" http://localhost:8001/health`

3. **Test HITL Endpoints**
   - List workflows
   - Toggle HITL on/off
   - Update confidence thresholds
   - Test decision approval flow (when AI agents integrated)

4. **Integrate with AI Agents**
   - Update AI agents to use HITL-aware routing
   - Configure confidence scores per agent
   - Test end-to-end workflows

5. **Connect Frontend Applications**
   - Update admin dashboard with HITL controls
   - Add pending decision approval UI
   - Implement real-time notifications

---

## Next Phase: AI Agents Integration

After Brain Gateway is deployed:

1. **Fix AI Agents Service Health**
   - Container: `bizosaas-ai-agents-8010`
   - Update health check
   - Connect to Brain Gateway

2. **Update Agent Routing**
   - Change from direct service calls to Brain Gateway routing
   - Add confidence scoring to agent outputs
   - Use `/api/brain/{service}/with-hitl/{path}` endpoint

3. **Test Workflows**
   - Lead processing with HITL
   - Product sourcing with AI validation
   - Campaign optimization autonomous mode
   - Content generation autonomous mode

4. **Deploy Frontend Applications**
   - Bizoholic Frontend (Port 3000)
   - CorelDove Frontend (Port 3002)
   - Client Portal (Port 3006)
   - BizOSaaS Admin (Port 3009)

---

## Support & Documentation

- **Deployment Guide**: `/home/alagiri/projects/bizoholic/BRAIN_GATEWAY_HITL_V2.1.0_DEPLOYMENT.md`
- **Implementation Summary**: `/home/alagiri/projects/bizoholic/HITL_IMPLEMENTATION_COMPLETE_SUMMARY.md`
- **This File**: `/home/alagiri/projects/bizoholic/DEPLOY_BRAIN_GATEWAY_MANUAL_STEPS.md`

---

**Ready to deploy!** Follow Option 1 (Transfer Docker Image) for the most reliable deployment.
