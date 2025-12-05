# BizOSaaS Infrastructure Project - Deployment Summary

## Quick Reference

| Item | Value |
|------|-------|
| **VPS IP** | 194.238.16.237 |
| **Dokploy URL** | http://194.238.16.237:3000 |
| **Project Name** | bizosaas-infrastructure-staging |
| **Total Containers** | 6 |
| **Deployment Phase** | Phase 1 - Infrastructure Foundation |
| **GitHub Repository** | https://github.com/Bizoholic-Digital/bizosaas-platform.git |

---

## Container Overview

### 1. PostgreSQL Database (bizosaas-postgres-staging)
- **Image**: pgvector/pgvector:pg16
- **Port**: 5432
- **Purpose**: Multi-tenant database with AI vector support
- **Databases**: bizosaas_staging, saleor_staging, temporal_staging, vault_staging
- **Credentials**:
  - User: admin
  - Password: BizOSaaS2025!StagingDB
  - Database: bizosaas_staging
- **Health Check**: `pg_isready -U admin -d bizosaas_staging`
- **Connection String**: `postgresql://admin:BizOSaaS2025!StagingDB@194.238.16.237:5432/bizosaas_staging`

### 2. Redis Cache (bizosaas-redis-staging)
- **Image**: redis:7-alpine
- **Port**: 6379
- **Purpose**: High-performance caching and session storage
- **Features**: Persistence enabled (appendonly)
- **Health Check**: `redis-cli ping`
- **Connection String**: `redis://194.238.16.237:6379/0`

### 3. HashiCorp Vault (bizosaas-vault-staging)
- **Image**: hashicorp/vault:1.15
- **Port**: 8200
- **Purpose**: Secrets management and credential storage
- **Mode**: Development (auto-unsealed)
- **Root Token**: staging-root-token-bizosaas-2025
- **Health Check**: `vault status`
- **Access URLs**:
  - API: http://194.238.16.237:8200
  - UI: http://194.238.16.237:8200/ui

### 4. Temporal Server (bizosaas-temporal-server-staging)
- **Image**: temporalio/auto-setup:1.22.0
- **Port**: 7233
- **Purpose**: Workflow orchestration engine
- **Database**: temporal_staging (PostgreSQL)
- **Health Check**: `tctl workflow list`
- **Connection**: bizosaas-temporal-server-staging:7233

### 5. Temporal UI (bizosaas-temporal-ui-staging)
- **Image**: temporalio/ui:2.21.0
- **Port**: 8082
- **Purpose**: Workflow management and monitoring interface
- **Server Address**: bizosaas-temporal-server-staging:7233
- **Access URL**: http://194.238.16.237:8082
- **CORS Origins**: http://localhost:3000, https://stg.bizoholic.com

### 6. Temporal Integration (bizosaas-temporal-integration-staging)
- **Build**: Custom service from GitHub
- **Port**: 8009
- **Purpose**: Custom workflow integration service
- **Dependencies**: Temporal Server, PostgreSQL, Redis
- **Health Endpoint**: http://194.238.16.237:8009/health
- **Environment**: staging

---

## Network Configuration

### Network Name
`bizosaas-staging-network`

### Network Type
Bridge (internal communication)

### Connected Services
All 6 infrastructure containers are connected to this network for internal communication.

### Internal DNS
Services can communicate using container names:
- `bizosaas-postgres-staging:5432`
- `bizosaas-redis-staging:6379`
- `bizosaas-vault-staging:8200`
- `bizosaas-temporal-server-staging:7233`
- `bizosaas-temporal-ui-staging:8082`
- `bizosaas-temporal-integration-staging:8009`

---

## Volume Configuration

### Data Volumes

1. **postgres_staging_data**
   - Mount: `/var/lib/postgresql/data`
   - Purpose: PostgreSQL data persistence

2. **redis_staging_data**
   - Mount: `/data`
   - Purpose: Redis data persistence

3. **vault_staging_data**
   - Mount: `/vault/data`
   - Purpose: Vault secrets storage

4. **temporal_staging_data**
   - Mount: `/etc/temporal/config/dynamicconfig`
   - Purpose: Temporal configuration

### Backup Strategy
All volumes use local driver and should be backed up regularly.

---

## Service Dependencies

```
PostgreSQL (foundation)
  ├── Temporal Server (depends on PostgreSQL)
  │   ├── Temporal UI (depends on Temporal Server)
  │   └── Temporal Integration (depends on Temporal Server, PostgreSQL, Redis)
  └── Redis (independent)
      └── Temporal Integration (depends on Redis)

Vault (independent)
```

**Startup Order**:
1. PostgreSQL, Redis, Vault (parallel)
2. Temporal Server (waits for PostgreSQL)
3. Temporal UI, Temporal Integration (wait for Temporal Server)

---

## Security Configuration

### Default Credentials (Staging Only)

**PostgreSQL**:
- Username: `admin`
- Password: `BizOSaaS2025!StagingDB`

**Vault**:
- Root Token: `staging-root-token-bizosaas-2025`

**Redis**:
- No authentication (staging environment)

**IMPORTANT**: Change all credentials for production deployment!

### Port Exposure

All ports are exposed for staging testing:
- 5432 (PostgreSQL)
- 6379 (Redis)
- 7233 (Temporal Server)
- 8009 (Temporal Integration)
- 8082 (Temporal UI)
- 8200 (Vault)

**Production Note**: Use internal networking and expose only necessary ports.

---

## Deployment Files

### Configuration Files
1. **dokploy-infrastructure-staging.yml** - Main Docker Compose configuration
2. **init-scripts/01-create-databases.sql** - PostgreSQL initialization script

### Documentation Files
1. **INFRASTRUCTURE_DEPLOYMENT_STEPS.md** - Detailed step-by-step deployment guide
2. **INFRASTRUCTURE_DEPLOYMENT_CHECKLIST.md** - Deployment verification checklist
3. **DOKPLOY_DEPLOYMENT_GUIDE.md** - Complete multi-phase deployment guide

### Verification Scripts
1. **verify-infrastructure-deployment.sh** - Automated health check script

---

## Access Information

### Web Interfaces

| Service | URL | Purpose |
|---------|-----|---------|
| Temporal UI | http://194.238.16.237:8082 | Workflow monitoring |
| Vault UI | http://194.238.16.237:8200/ui | Secrets management |

### API Endpoints

| Service | Endpoint | Purpose |
|---------|----------|---------|
| Temporal Integration | http://194.238.16.237:8009/health | Health check |
| Vault API | http://194.238.16.237:8200/v1/sys/health | Vault status |

### Direct Connections

| Service | Connection String |
|---------|-------------------|
| PostgreSQL | `postgresql://admin:BizOSaaS2025!StagingDB@194.238.16.237:5432/bizosaas_staging` |
| Redis | `redis://194.238.16.237:6379/0` |
| Temporal | `bizosaas-temporal-server-staging:7233` (internal) |

---

## Health Check Commands

### From Local Machine

```bash
# PostgreSQL
PGPASSWORD="BizOSaaS2025!StagingDB" psql -h 194.238.16.237 -p 5432 -U admin -d bizosaas_staging -c "SELECT 1;"

# Redis
redis-cli -h 194.238.16.237 -p 6379 ping

# Vault
curl http://194.238.16.237:8200/v1/sys/health

# Temporal UI
curl -I http://194.238.16.237:8082

# Temporal Integration
curl http://194.238.16.237:8009/health
```

### Run Automated Verification

```bash
cd /home/alagiri/projects/bizoholic
./verify-infrastructure-deployment.sh
```

---

## Resource Requirements

### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 4GB
- **Disk**: 20GB
- **Network**: 10 Mbps

### Recommended Requirements
- **CPU**: 4 cores
- **RAM**: 8GB
- **Disk**: 50GB SSD
- **Network**: 100 Mbps

### Expected Resource Usage
- PostgreSQL: 512MB - 1GB RAM
- Redis: 128MB - 256MB RAM
- Vault: 128MB - 256MB RAM
- Temporal Server: 512MB - 1GB RAM
- Temporal UI: 256MB - 512MB RAM
- Temporal Integration: 256MB - 512MB RAM

**Total**: ~2-4GB RAM for infrastructure layer

---

## Monitoring & Maintenance

### Log Access
```bash
# View all infrastructure logs
docker-compose -f dokploy-infrastructure-staging.yml logs -f

# View specific service logs
docker logs bizosaas-postgres-staging -f
docker logs bizosaas-redis-staging -f
docker logs bizosaas-vault-staging -f
docker logs bizosaas-temporal-server-staging -f
docker logs bizosaas-temporal-ui-staging -f
docker logs bizosaas-temporal-integration-staging -f
```

### Container Management
```bash
# Restart specific container
docker restart bizosaas-postgres-staging

# Stop all infrastructure
docker-compose -f dokploy-infrastructure-staging.yml down

# Start all infrastructure
docker-compose -f dokploy-infrastructure-staging.yml up -d

# Check container status
docker-compose -f dokploy-infrastructure-staging.yml ps
```

### Backup Commands
```bash
# Backup PostgreSQL
docker exec bizosaas-postgres-staging pg_dump -U admin bizosaas_staging > backup_$(date +%Y%m%d).sql

# Backup Redis
docker exec bizosaas-redis-staging redis-cli SAVE
docker cp bizosaas-redis-staging:/data/dump.rdb ./redis_backup_$(date +%Y%m%d).rdb

# Backup Vault
docker exec bizosaas-vault-staging vault operator raft snapshot save /tmp/vault_backup.snap
docker cp bizosaas-vault-staging:/tmp/vault_backup.snap ./vault_backup_$(date +%Y%m%d).snap
```

---

## Troubleshooting

### Common Issues

#### PostgreSQL Connection Refused
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check PostgreSQL logs
docker logs bizosaas-postgres-staging

# Restart PostgreSQL
docker restart bizosaas-postgres-staging
```

#### Redis Connection Failed
```bash
# Test Redis locally
docker exec bizosaas-redis-staging redis-cli ping

# Check Redis logs
docker logs bizosaas-redis-staging
```

#### Temporal Server Not Starting
```bash
# Ensure PostgreSQL is running first
docker ps | grep postgres

# Check Temporal logs
docker logs bizosaas-temporal-server-staging

# Verify database exists
PGPASSWORD="BizOSaaS2025!StagingDB" psql -h 194.238.16.237 -p 5432 -U admin -d temporal_staging -c "\l"
```

#### Vault Sealed/Unhealthy
```bash
# Check Vault status
curl http://194.238.16.237:8200/v1/sys/health

# In development mode, Vault should auto-unseal
# If not, restart the container
docker restart bizosaas-vault-staging
```

---

## Next Phase: Backend Services Deployment

After successful infrastructure deployment, proceed with:

1. **Backend Services Project** (Phase 2)
   - 8 backend containers
   - APIs and microservices
   - Dependencies on infrastructure

2. **Frontend Applications Project** (Phase 3)
   - 6 frontend containers
   - Web applications with domains
   - Dependencies on backend services

**Total Platform**: 20 containers across 3 projects

---

## Support & Documentation

### Reference Documents
- **Detailed Deployment**: INFRASTRUCTURE_DEPLOYMENT_STEPS.md
- **Deployment Checklist**: INFRASTRUCTURE_DEPLOYMENT_CHECKLIST.md
- **Complete Guide**: DOKPLOY_DEPLOYMENT_GUIDE.md

### GitHub Repository
https://github.com/Bizoholic-Digital/bizosaas-platform.git

### Configuration File
`/home/alagiri/projects/bizoholic/dokploy-infrastructure-staging.yml`

---

## Deployment Status

- [ ] Infrastructure deployment started
- [ ] All 6 containers deployed
- [ ] Health checks passing
- [ ] Services accessible
- [ ] Verification completed
- [ ] Ready for Phase 2

---

**Infrastructure Foundation - Ready for Multi-Tenant SaaS Platform**

*Last Updated: October 10, 2025*
