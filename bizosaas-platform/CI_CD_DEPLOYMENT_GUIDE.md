# BizOSaaS Platform - CI/CD Deployment Guide

## Architecture Overview

```
Local Development (WSL2)
    ↓ git push to main
GitHub Repository (Bizoholic-Digital/bizosaas-platform)
    ↓ triggers GitHub Actions
Automated Build & Test
    ↓ docker build for each service
GitHub Container Registry (GHCR)
    ↓ push images with tags
Dokploy (dk4.bizoholic.com)
    ↓ pull and deploy
KVM4 Server (72.60.219.244)
```

## Server Organization

### KVM4 (72.60.219.244) - Primary Production Server
**Dokploy URL**: https://dk4.bizoholic.com
**Purpose**: All BizOSaaS platform services (24 containers)

**Infrastructure Layer (6 services)**:
- PostgreSQL with pgvector (Port 5433)
- Redis Cache (Port 6380)
- Vault Secrets Manager (Port 8201)
- Temporal Server (Port 7234)
- Temporal UI (Port 8083)
- Apache Superset (Port 8088)

**Backend Services (10 services)**:
- Brain Gateway - AI Hub (Port 8001)
- Saleor E-commerce (Port 8000)
- Wagtail CMS (Port 8002)
- Django CRM (Port 8003)
- Business Directory Backend (Port 8004)
- CorelDove Backend (Port 8005)
- Auth Service (Port 8006)
- AI Agents (Port 8008)
- Amazon Sourcing (Port 8009)
- QuantTrade Backend (Port 8010)

**Frontend Applications (6 services)**:
- Bizoholic Frontend (Port 3000) → stg.bizoholic.com
- Client Portal (Port 3001) → stg.portal.bizoholic.com
- CorelDove Frontend (Port 3002) → stg.coreldove.com
- Business Directory (Port 3003) → stg.directory.bizoholic.com
- ThrillRing Gaming (Port 3005) → stg.thrillring.com
- Admin Dashboard (Port 3009) → stg.admin.bizoholic.com

**WordPress (2 services)**:
- QuantTrade WordPress (Port 8010/8011)

### KVM2 (194.238.16.237) - WordPress Only
**Dokploy URL**: https://dk.bizoholic.com
**Purpose**: CoreLDove WordPress website only

**Services**:
- CorelDove WordPress + MySQL (Port 80)

## CI/CD Workflow

### 1. Automated Image Builds (GitHub Actions)

**Trigger**: Push to `main`, `staging`, or `develop` branch

**GitHub Actions Workflow** (`.github/workflows/build-and-push.yml`):
- Builds Docker images for all 16 application services
- Pushes to GHCR with tags:
  - `staging` (for staging branch)
  - `main` (for main branch)
  - `main-<sha>` (commit-specific)
  - `latest` (for main branch only)

**Build Time**:
- Backend services: ~5-10 minutes each
- Frontend services: ~8-12 minutes each
- Total parallel build: ~15-20 minutes

### 2. Container Registry (GHCR)

**Images are stored at**:
```
ghcr.io/bizoholic-digital/bizosaas-<service-name>:staging
```

**Example**:
- `ghcr.io/bizoholic-digital/bizosaas-brain-gateway:staging`
- `ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:staging`
- `ghcr.io/bizoholic-digital/bizosaas-wagtail-cms:staging`

### 3. Deployment to KVM4

**Option A: Automated via Dokploy UI**
1. Login to https://dk4.bizoholic.com
2. Navigate to project: "bizosaas-platform-staging"
3. Click "Deploy" → automatically pulls from GHCR
4. Monitor build logs in Dokploy interface

**Option B: Manual via SSH**
```bash
# SSH into KVM4
ssh root@72.60.219.244

# Navigate to deployment directory
cd /opt/bizosaas-platform

# Pull latest images from GHCR
docker-compose -f dokploy-staging-complete.yml pull

# Deploy with zero downtime
docker-compose -f dokploy-staging-complete.yml up -d

# Monitor deployment
docker-compose -f dokploy-staging-complete.yml ps
```

**Option C: Automated Script**
```bash
# From local machine
cd /home/alagiri/projects/bizoholic/bizosaas-platform

# Deploy to KVM4
./deploy-kvm4-staging.sh
```

## Environment Variables

### Required Secrets (Set in Dokploy or .env)
```bash
# AI Services
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Amazon Integration
AMAZON_ACCESS_KEY=...
AMAZON_SECRET_KEY=...

# Payment Gateways
STRIPE_SECRET_KEY=sk_...
PAYPAL_CLIENT_ID=...

# Email Services
SMTP_HOST=smtp.resend.com
SMTP_USER=...
SMTP_PASSWORD=...

# External APIs
GOOGLE_ADS_API_KEY=...
META_ADS_API_KEY=...
```

## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing locally
- [ ] Environment variables configured in Dokploy
- [ ] Database migrations reviewed
- [ ] Backup created on KVM4

### Deployment
- [ ] Push to GitHub main/staging branch
- [ ] Wait for GitHub Actions build (check Actions tab)
- [ ] Verify images pushed to GHCR
- [ ] Trigger deployment in Dokploy
- [ ] Monitor container startup (watch logs)

### Post-Deployment
- [ ] All 24 services running (check `docker ps`)
- [ ] Health checks passing
- [ ] Frontend URLs accessible:
  - https://stg.bizoholic.com
  - https://stg.coreldove.com
  - https://stg.thrillring.com
  - https://stg.portal.bizoholic.com
  - https://stg.directory.bizoholic.com
  - https://stg.admin.bizoholic.com
- [ ] Backend APIs responding:
  - http://72.60.219.244:8001/health (Brain Gateway)
  - http://72.60.219.244:8000/health/ (Saleor)
  - http://72.60.219.244:8002/admin/ (Wagtail)
- [ ] Database connections working
- [ ] Redis cache operational

## Monitoring & Logs

### Via Dokploy UI
1. Login to https://dk4.bizoholic.com
2. Navigate to "Applications"
3. Click on service name
4. View "Logs" tab for real-time output

### Via SSH
```bash
# SSH into KVM4
ssh root@72.60.219.244

# View all service logs
docker-compose -f /opt/bizosaas-platform/dokploy-staging-complete.yml logs -f

# View specific service logs
docker logs -f bizosaas-brain-staging
docker logs -f bizosaas-bizoholic-frontend-staging
docker logs -f bizosaas-wagtail-staging

# Check service health
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Health Check Endpoints
```bash
# Brain Gateway
curl http://72.60.219.244:8001/health

# Saleor API
curl http://72.60.219.244:8000/health/

# Wagtail CMS
curl http://72.60.219.244:8002/admin/

# Frontend Apps
curl https://stg.bizoholic.com/api/health
curl https://stg.coreldove.com/api/health
```

## Rollback Procedure

### Quick Rollback (Previous Image)
```bash
# SSH into KVM4
ssh root@72.60.219.244

# Rollback to previous image tag
docker-compose -f /opt/bizosaas-platform/dokploy-staging-complete.yml pull --ignore-pull-failures

# Change image tags to previous commit SHA in compose file
nano /opt/bizosaas-platform/dokploy-staging-complete.yml

# Deploy previous version
docker-compose -f /opt/bizosaas-platform/dokploy-staging-complete.yml up -d
```

### Emergency Rollback (Restore Backup)
```bash
# Restore PostgreSQL backup
docker exec -i bizosaas-postgres-staging psql -U admin bizosaas_staging < /backup/postgres-backup-YYYYMMDD.sql

# Restart affected services
docker-compose -f /opt/bizosaas-platform/dokploy-staging-complete.yml restart
```

## Troubleshooting

### Services Not Starting
```bash
# Check logs for error messages
docker logs bizosaas-<service-name>-staging

# Common issues:
# 1. Missing environment variables
# 2. Database connection failures
# 3. Port conflicts
# 4. Volume mount issues
```

### Images Not Pulling from GHCR
```bash
# Login to GHCR manually
echo $GITHUB_TOKEN | docker login ghcr.io -u BizoDokploy --password-stdin

# Pull specific image
docker pull ghcr.io/bizoholic-digital/bizosaas-brain-gateway:staging
```

### Frontend Not Loading
```bash
# Check Traefik routing
docker logs dokploy-traefik

# Verify DNS records point to KVM4
dig stg.bizoholic.com +short  # Should return 72.60.219.244

# Check SSL certificates
curl -vI https://stg.bizoholic.com
```

## Performance Optimization

### Database Tuning
- Enable connection pooling in all services
- Set `max_connections=200` in PostgreSQL
- Use Redis for session storage and caching

### Container Resource Limits
Set in `dokploy-staging-complete.yml`:
```yaml
services:
  brain-gateway:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### Load Balancing
- Traefik automatically load balances across service replicas
- Scale services with: `docker-compose up -d --scale brain-gateway=3`

## Security Considerations

1. **Secrets Management**: All API keys stored in Vault (Port 8201)
2. **SSL/TLS**: Automatic Let's Encrypt via Traefik
3. **Database**: PostgreSQL only accessible within Docker network
4. **Rate Limiting**: Implemented at Traefik level
5. **Container Isolation**: Each service in separate container with minimal privileges

## Support

**Issues**: https://github.com/Bizoholic-Digital/bizosaas-platform/issues
**Documentation**: This repository
**Monitoring Dashboard**: https://dk4.bizoholic.com
**Status Page**: https://stg.admin.bizoholic.com/system-status

---

**Last Updated**: October 25, 2025
**Platform Version**: 1.0.0-staging
**Deployment Target**: KVM4 (72.60.219.244)
