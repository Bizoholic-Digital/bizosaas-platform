# Infrastructure Project Deployment to Dokploy - Step by Step

## Deployment Information
- **VPS IP**: 194.238.16.237
- **Dokploy URL**: http://194.238.16.237:3000
- **Project Name**: bizosaas-infrastructure-staging
- **Container Count**: 6 infrastructure containers
- **GitHub Repository**: https://github.com/Bizoholic-Digital/bizosaas-platform.git

---

## STEP 1: Access Dokploy Dashboard

1. Open your web browser
2. Navigate to: **http://194.238.16.237:3000**
3. Login with your Dokploy admin credentials

---

## STEP 2: Create Infrastructure Project

1. Click **"Projects"** in the left sidebar
2. Click **"+ New Project"** button (top right)
3. Fill in project details:
   - **Project Name**: `bizosaas-infrastructure-staging`
   - **Description**: `Core infrastructure services for staging environment`
4. Click **"Create Project"**

---

## STEP 3: Create Docker Compose Application

1. Click on the newly created **"bizosaas-infrastructure-staging"** project
2. Click **"+ New Application"** button
3. Select **"Docker Compose"** as application type
4. Fill in application details:
   - **Application Name**: `infrastructure-services`
   - **Description**: `6 core infrastructure containers`

---

## STEP 4: Configure Docker Compose

### Option A: Upload Configuration File
1. Click **"Upload Compose File"** or **"Import"**
2. Select the file: `/home/alagiri/projects/bizoholic/dokploy-infrastructure-staging.yml`
3. Dokploy will automatically parse the configuration

### Option B: Paste Configuration
1. Click on **"Compose"** or **"Configuration"** tab
2. Copy the entire content from `dokploy-infrastructure-staging.yml`
3. Paste into the compose editor
4. Click **"Save"**

---

## STEP 5: Review Configuration

Verify the following services are configured:

### Service 1: PostgreSQL Database
- **Container**: bizosaas-postgres-staging
- **Port**: 5432
- **Image**: pgvector/pgvector:pg16
- **Environment**:
  - POSTGRES_DB: bizosaas_staging
  - POSTGRES_USER: admin
  - POSTGRES_PASSWORD: BizOSaaS2025!StagingDB

### Service 2: Redis Cache
- **Container**: bizosaas-redis-staging
- **Port**: 6379
- **Image**: redis:7-alpine

### Service 3: HashiCorp Vault
- **Container**: bizosaas-vault-staging
- **Port**: 8200
- **Image**: hashicorp/vault:1.15

### Service 4: Temporal Server
- **Container**: bizosaas-temporal-server-staging
- **Port**: 7233
- **Image**: temporalio/auto-setup:1.22.0

### Service 5: Temporal UI
- **Container**: bizosaas-temporal-ui-staging
- **Port**: 8082
- **Image**: temporalio/ui:2.21.0

### Service 6: Temporal Integration
- **Container**: bizosaas-temporal-integration-staging
- **Port**: 8009
- **Build**: From GitHub repository

---

## STEP 6: Configure Environment Variables (Optional)

The docker-compose file already includes all necessary environment variables. However, if you need to override any:

1. Click on **"Environment Variables"** tab
2. Add any custom variables (none required for basic deployment)
3. Click **"Save"**

---

## STEP 7: Deploy Infrastructure

1. Click **"Deploy"** button (usually at top right or bottom of page)
2. Confirm deployment
3. Monitor deployment progress in real-time logs

**Expected deployment time**: 5-10 minutes

---

## STEP 8: Monitor Deployment Progress

1. Click on **"Logs"** tab to see live deployment logs
2. Watch for these success indicators:
   - ✓ PostgreSQL: "database system is ready to accept connections"
   - ✓ Redis: "Ready to accept connections"
   - ✓ Vault: "Development mode" and "Vault server started!"
   - ✓ Temporal Server: "Started temporal server"
   - ✓ Temporal UI: "Server listening on"
   - ✓ Temporal Integration: Service builds and starts successfully

---

## STEP 9: Verify Container Health

1. Navigate to **"Containers"** or **"Services"** tab
2. Confirm all 6 containers show **"Running"** status:
   - [ ] bizosaas-postgres-staging
   - [ ] bizosaas-redis-staging
   - [ ] bizosaas-vault-staging
   - [ ] bizosaas-temporal-server-staging
   - [ ] bizosaas-temporal-ui-staging
   - [ ] bizosaas-temporal-integration-staging

---

## STEP 10: Test Service Connectivity

### Access from Browser:
- **Temporal UI**: http://194.238.16.237:8082
- **Vault UI**: http://194.238.16.237:8200/ui

### Test via curl (from local terminal):
```bash
# Test Vault health
curl http://194.238.16.237:8200/v1/sys/health

# Test Temporal UI
curl http://194.238.16.237:8082

# Test Temporal Integration
curl http://194.238.16.237:8009/health

# Test Redis (requires redis-cli)
redis-cli -h 194.238.16.237 -p 6379 ping
# Expected: PONG
```

---

## STEP 11: Verify Network Configuration

1. Click on **"Networks"** tab
2. Confirm **"bizosaas-staging-network"** is created
3. All 6 containers should be connected to this network

---

## STEP 12: Check Volumes and Data Persistence

1. Click on **"Volumes"** tab
2. Verify these volumes are created:
   - postgres_staging_data
   - redis_staging_data
   - vault_staging_data
   - temporal_staging_data

---

## TROUBLESHOOTING

### Issue: PostgreSQL container won't start
**Solution**:
- Check logs for port conflicts
- Ensure port 5432 is not already in use
- Verify environment variables are correct

### Issue: Temporal Integration build fails
**Solution**:
- Verify GitHub repository is accessible
- Check if Dockerfile exists at: `ai/services/temporal-integration/Dockerfile`
- Ensure Docker has internet access to clone repository

### Issue: Container shows "Unhealthy" status
**Solution**:
- Click on container → View logs
- Check health check configuration
- Verify dependencies are running (e.g., Temporal needs PostgreSQL)
- Restart container if needed

### Issue: Services can't communicate
**Solution**:
- Verify all containers are on same network
- Use container names for internal communication
- Check firewall rules on VPS

---

## DEPLOYMENT SUCCESS INDICATORS

When deployment is successful, you should see:

✅ **6 containers running** in Dokploy dashboard
✅ **All health checks passing** (green status indicators)
✅ **Temporal UI accessible** at http://194.238.16.237:8082
✅ **Vault UI accessible** at http://194.238.16.237:8200/ui
✅ **Network created** (bizosaas-staging-network)
✅ **Volumes persisted** (4 data volumes)
✅ **No error logs** in container outputs

---

## NEXT STEPS

After infrastructure deployment is complete:

1. **Document Infrastructure Details**: Save connection strings and credentials
2. **Prepare for Backend Deployment**: Infrastructure is now ready for backend services
3. **Monitor Resource Usage**: Check CPU/memory usage in Dokploy
4. **Setup Backups**: Configure volume backup strategy
5. **Deploy Backend Project**: Proceed with Phase 2 deployment

---

## IMPORTANT NOTES

- **Foundation Layer**: This infrastructure must be running before deploying backend services
- **No External Domains**: Infrastructure services are internal-only (no domain configuration needed)
- **Data Persistence**: All data is stored in named volumes and will persist across container restarts
- **Service Dependencies**: Temporal services depend on PostgreSQL, so startup order matters
- **Security**: Change default passwords in production environment

---

## DEPLOYMENT COMMAND REFERENCE

If deploying via SSH instead of Dokploy UI:

```bash
# SSH into VPS
ssh root@194.238.16.237

# Navigate to project directory
cd /opt/dokploy/projects/bizosaas-infrastructure-staging

# Deploy with docker-compose
docker-compose -f dokploy-infrastructure-staging.yml up -d

# Check status
docker-compose -f dokploy-infrastructure-staging.yml ps

# View logs
docker-compose -f dokploy-infrastructure-staging.yml logs -f

# Stop services
docker-compose -f dokploy-infrastructure-staging.yml down
```

---

**Infrastructure Deployment Guide Complete**

Foundation layer ready for backend and frontend deployments!
