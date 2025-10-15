# Quick Start: Infrastructure Deployment to Dokploy

## 5-Minute Deployment Guide

---

## Step 1: Access Dokploy (1 minute)

1. Open browser: **http://194.238.16.237:3000**
2. Login with admin credentials

---

## Step 2: Create Project (1 minute)

1. Click **"Projects"** → **"+ New Project"**
2. Project Name: `bizosaas-infrastructure-staging`
3. Description: `Core infrastructure services for staging environment`
4. Click **"Create Project"**

---

## Step 3: Create Application (1 minute)

1. Click on **"bizosaas-infrastructure-staging"** project
2. Click **"+ New Application"** → Select **"Docker Compose"**
3. Application Name: `infrastructure-services`
4. Click **"Create"**

---

## Step 4: Upload Configuration (1 minute)

1. Click **"Upload Compose File"** or **"Configuration"** tab
2. Upload: `/home/alagiri/projects/bizoholic/dokploy-infrastructure-staging.yml`
3. OR paste the file contents directly
4. Click **"Save"**

---

## Step 5: Deploy (1 minute + 5-10 min wait)

1. Click **"Deploy"** button
2. Monitor logs for deployment progress
3. Wait 5-10 minutes for all containers to start

---

## Step 6: Verify (1 minute)

### Quick Check in Browser:
- Temporal UI: http://194.238.16.237:8082 ✓
- Vault UI: http://194.238.16.237:8200/ui ✓

### Run Verification Script:
```bash
cd /home/alagiri/projects/bizoholic
./verify-infrastructure-deployment.sh
```

### Expected Result:
- 6 containers running
- All health checks green
- Services accessible

---

## What Gets Deployed

| # | Container | Port | Purpose |
|---|-----------|------|---------|
| 1 | PostgreSQL | 5432 | Multi-tenant database |
| 2 | Redis | 6379 | Cache & sessions |
| 3 | Vault | 8200 | Secrets management |
| 4 | Temporal Server | 7233 | Workflow engine |
| 5 | Temporal UI | 8082 | Workflow interface |
| 6 | Temporal Integration | 8009 | Custom workflows |

---

## Connection Details

### PostgreSQL
```
Host: 194.238.16.237
Port: 5432
User: admin
Password: BizOSaaS2025!StagingDB
Database: bizosaas_staging
```

### Redis
```
Host: 194.238.16.237
Port: 6379
```

### Vault
```
URL: http://194.238.16.237:8200
Root Token: staging-root-token-bizosaas-2025
```

---

## Quick Troubleshooting

### Container won't start?
```bash
# Check logs in Dokploy UI
Click container → View Logs

# Or via SSH
docker logs <container-name>
```

### Service not accessible?
```bash
# Check if port is open
telnet 194.238.16.237 <port>

# Or use curl
curl http://194.238.16.237:<port>
```

### Need to restart?
```bash
# In Dokploy UI
Click container → Restart

# Or via SSH
docker restart <container-name>
```

---

## Next Steps

After infrastructure deployment succeeds:

1. ✓ Infrastructure running (Phase 1) - **YOU ARE HERE**
2. → Deploy Backend Services (Phase 2) - 8 containers
3. → Deploy Frontend Applications (Phase 3) - 6 containers

---

## Need Help?

- **Detailed Guide**: INFRASTRUCTURE_DEPLOYMENT_STEPS.md
- **Checklist**: INFRASTRUCTURE_DEPLOYMENT_CHECKLIST.md
- **Complete Summary**: INFRASTRUCTURE_DEPLOYMENT_SUMMARY.md
- **Full Deployment**: DOKPLOY_DEPLOYMENT_GUIDE.md

---

## One-Command Verification

```bash
./verify-infrastructure-deployment.sh
```

This script checks:
- All 6 container ports
- HTTP endpoint health
- Redis connectivity
- PostgreSQL connectivity
- Service status

---

**Infrastructure Foundation Complete - Ready for Backend Services!**

*Deployment Time: 5-15 minutes*
*Total Containers: 6*
*Zero Downtime: Yes*
