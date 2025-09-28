# Database & Services Consolidation Plan

## 🔍 **CURRENT STATE ANALYSIS**

### **PostgreSQL Instances (ALL EXPOSED - CRITICAL SECURITY RISK)**
```
bizoholic-postgres            → Port 5432 (EXPOSED to internet) ⚠️
bizoholic-postgres-new        → Port 5433 (EXPOSED to internet) ⚠️  
bizosaas-postgres-staging     → Port 5434 (EXPOSED to internet) ⚠️
```

### **Redis Instances (ALL EXPOSED - CRITICAL SECURITY RISK)**
```
shared-redis-dev              → Port 6379 (EXPOSED to internet) ⚠️
bizosaas-redis-staging        → Port 6380 (EXPOSED to internet) ⚠️
```

### **Existing Services Analysis**
```
✅ CoreLDove Frontend         → Port 3003 (Next.js with GraphQL)
✅ Saleor Backend            → Port 8020 (coreldove-saleor-minimal)
✅ BizoSaaS Frontend         → Port 3005 (Unified Dashboard)
✅ Wagtail CMS               → Port 8006/8007 (needs consolidation)
```

## 🎯 **CONSOLIDATION STRATEGY**

### **Single PostgreSQL Instance (Recommended)**
```yaml
# One secure PostgreSQL with multiple databases
bizosaas-postgres-primary:
  image: pgvector/pgvector:pg16
  container_name: bizosaas-postgres-unified
  # NO EXTERNAL PORT EXPOSURE
  databases:
    - bizosaas          # Main platform database
    - wagtail_cms       # Wagtail content management
    - saleor_core       # CoreLDove e-commerce
    - directory_db      # Business directory
```

### **Single Redis Instance (Recommended)**
```yaml  
# One secure Redis with multiple databases
bizosaas-redis-primary:
  image: redis:7-alpine
  container_name: bizosaas-redis-unified
  # NO EXTERNAL PORT EXPOSURE  
  databases:
    - db0: Cache (default)
    - db1: Sessions
    - db2: Celery/Background tasks
```

### **Service Port Reorganization**
```yaml
# FRONTEND TIER (Public Access)
CoreLDove Frontend:     3003 → Keep existing (already configured)
Bizoholic Frontend:     3000 → New Next.js (created)
BizoSaaS Dashboard:     3005 → Keep existing (already configured)

# BACKEND TIER (Internal API)
Saleor GraphQL API:     8020 → Move to 4003 (headless mode)
Wagtail Headless API:   8006/8007 → Move to 4000 (headless mode)
FastAPI Brain:          New → 4005 (API orchestration)

# ADMIN TIER (Localhost Only)
Saleor Admin Dashboard: New → 5003 (management interface)
Wagtail Admin:          New → 5000 (CMS management)
```

## 📋 **CONSOLIDATION IMPLEMENTATION PLAN**

### **Phase 1: Data Backup & Analysis**
```bash
# 1. Backup all databases
docker exec bizoholic-postgres pg_dumpall -U admin > bizoholic_backup.sql
docker exec bizosaas-postgres-staging pg_dumpall -U admin > bizosaas_backup.sql

# 2. Analyze database usage
docker exec bizoholic-postgres psql -U admin -c "\l"
docker exec bizosaas-postgres-staging psql -U admin -c "\l"

# 3. Check Redis data
docker exec shared-redis-dev redis-cli INFO keyspace
docker exec bizosaas-redis-staging redis-cli INFO keyspace
```

### **Phase 2: Create Unified Database**
```bash
# 1. Stop old instances (after backup)
docker stop bizoholic-postgres bizoholic-postgres-new bizosaas-postgres-staging
docker stop shared-redis-dev bizosaas-redis-staging

# 2. Create unified PostgreSQL
docker run -d \
  --name bizosaas-postgres-unified \
  --network data-tier \
  -e POSTGRES_DB=bizosaas \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
  -v postgres_unified_data:/var/lib/postgresql/data \
  pgvector/pgvector:pg16

# 3. Create additional databases
docker exec bizosaas-postgres-unified psql -U admin -c "CREATE DATABASE wagtail_cms;"
docker exec bizosaas-postgres-unified psql -U admin -c "CREATE DATABASE saleor_core;"
docker exec bizosaas-postgres-unified psql -U admin -c "CREATE DATABASE directory_db;"

# 4. Restore data
docker exec -i bizosaas-postgres-unified psql -U admin -d bizosaas < bizosaas_backup.sql
```

### **Phase 3: Reconfigure Services**
```bash
# 1. Update Wagtail CMS configuration
# DATABASE_URL=postgresql://admin:${POSTGRES_PASSWORD}@bizosaas-postgres-unified:5432/wagtail_cms

# 2. Update Saleor configuration  
# DATABASE_URL=postgresql://admin:${POSTGRES_PASSWORD}@bizosaas-postgres-unified:5432/saleor_core

# 3. Update BizoSaaS configuration
# DATABASE_URL=postgresql://admin:${POSTGRES_PASSWORD}@bizosaas-postgres-unified:5432/bizosaas
```

### **Phase 4: Remove Old Instances**
```bash
# 1. Verify all services work with new database
# 2. Remove old containers
docker rm bizoholic-postgres bizoholic-postgres-new bizosaas-postgres-staging
docker rm shared-redis-dev bizosaas-redis-staging

# 3. Clean up volumes (after confirming data migration)
docker volume rm bizoholic_postgres_data bizosaas_postgres_staging_data
```

## 🔧 **SALEOR INTEGRATION CONFIGURATION**

### **Current State**
- ✅ **CoreLDove Frontend**: Next.js on port 3003 with GraphQL integration
- ✅ **Saleor Backend**: Running on port 8020 (ghcr.io/saleor/saleor:3.20)

### **Required Changes**
```yaml
# 1. Move Saleor to proper backend tier
saleor-headless:
  image: ghcr.io/saleor/saleor:3.20
  container_name: coreldove-saleor-headless
  ports:
    - "127.0.0.1:4003:8000"  # Move from 8020 to 4003
  environment:
    DATABASE_URL: postgresql://admin:${POSTGRES_PASSWORD}@bizosaas-postgres-unified:5432/saleor_core
    REDIS_URL: redis://:${REDIS_PASSWORD}@bizosaas-redis-unified:6379/0

# 2. Add Saleor Admin Dashboard  
saleor-admin:
  image: ghcr.io/saleor/saleor-dashboard:latest
  container_name: coreldove-saleor-admin
  ports:
    - "127.0.0.1:5003:80"  # Admin interface (localhost only)
  environment:
    API_URI: http://saleor-headless:8000/graphql/
```

### **CoreLDove Frontend Configuration**
```javascript
// coreldove-frontend/next.config.js
const nextConfig = {
  env: {
    SALEOR_API_URL: process.env.SALEOR_API_URL || 'http://localhost:4003/graphql/',
    SALEOR_ADMIN_URL: process.env.SALEOR_ADMIN_URL || 'http://localhost:5003/',
  },
  
  async rewrites() {
    return [
      {
        source: '/api/graphql/:path*',
        destination: 'http://saleor-headless:8000/graphql/:path*',
      },
    ]
  }
}
```

## 🛠️ **UPDATED DOCKER COMPOSE**

```yaml
version: '3.8'

networks:
  data-tier:
    internal: true
  backend-tier:
    internal: true  
  frontend-tier: {}
  admin-tier:
    internal: true

services:
  # UNIFIED DATA TIER
  postgres-unified:
    image: pgvector/pgvector:pg16
    container_name: bizosaas-postgres-unified
    networks: [data-tier]
    environment:
      POSTGRES_DB: bizosaas
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_unified:/var/lib/postgresql/data
    restart: unless-stopped

  redis-unified:
    image: redis:7-alpine
    container_name: bizosaas-redis-unified
    networks: [data-tier]
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_unified:/data
    restart: unless-stopped

  # BACKEND TIER
  saleor-headless:
    image: ghcr.io/saleor/saleor:3.20
    container_name: coreldove-saleor-headless
    networks: [backend-tier, data-tier]
    ports: ["127.0.0.1:4003:8000"]
    environment:
      DATABASE_URL: postgresql://admin:${POSTGRES_PASSWORD}@postgres-unified:5432/saleor_core
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis-unified:6379/0
    depends_on: [postgres-unified, redis-unified]

  wagtail-headless:
    build: ./services/wagtail-cms
    container_name: bizosaas-wagtail-headless  
    networks: [backend-tier, data-tier]
    ports: ["127.0.0.1:4000:8000"]
    environment:
      DATABASE_URL: postgresql://admin:${POSTGRES_PASSWORD}@postgres-unified:5432/wagtail_cms
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis-unified:6379/1
    depends_on: [postgres-unified, redis-unified]

  # FRONTEND TIER
  coreldove-frontend:
    build: ./services/coreldove-frontend
    container_name: coreldove-frontend
    networks: [frontend-tier, backend-tier]
    ports: ["3003:3000"]
    environment:
      SALEOR_API_URL: http://saleor-headless:8000/graphql/
    depends_on: [saleor-headless]

  bizoholic-frontend:
    build: ./services/bizoholic-frontend
    container_name: bizoholic-frontend
    networks: [frontend-tier, backend-tier]
    ports: ["3000:3000"]
    environment:
      WAGTAIL_API_URL: http://wagtail-headless:8000/api/
    depends_on: [wagtail-headless]

  # ADMIN TIER
  saleor-admin:
    image: ghcr.io/saleor/saleor-dashboard:latest
    container_name: coreldove-saleor-admin
    networks: [admin-tier]
    ports: ["127.0.0.1:5003:80"]
    environment:
      API_URI: http://saleor-headless:8000/graphql/
    depends_on: [saleor-headless]

volumes:
  postgres_unified:
  redis_unified:
```

## ✅ **CONSOLIDATION BENEFITS**

### **Security Improvements**
- ❌ **5 exposed PostgreSQL ports** → ✅ **0 exposed (internal network only)**
- ❌ **2 exposed Redis ports** → ✅ **0 exposed (internal network only)**
- ✅ **Network segmentation** with Docker networks
- ✅ **Admin interfaces** localhost-only access

### **Resource Optimization**  
- 🔻 **Memory usage**: 3 PostgreSQL → 1 PostgreSQL (~2GB savings)
- 🔻 **Storage usage**: Consolidated data volumes
- 🔻 **Maintenance overhead**: Single database to monitor/backup
- 🔻 **Network complexity**: Simplified service discovery

### **Architecture Benefits**
- ✅ **Clean separation**: Frontend/Backend/Admin/Data tiers
- ✅ **Proper port organization**: 3000s (Frontend), 4000s (Backend), 5000s (Admin)
- ✅ **Headless architecture**: APIs separate from admin interfaces
- ✅ **Scalability**: Services can be scaled independently

## 🚨 **IMMEDIATE ACTION REQUIRED**

1. **🔥 CRITICAL**: Stop exposed database services immediately
2. **💾 BACKUP**: Export all data before consolidation  
3. **🔧 MIGRATE**: Implement unified database architecture
4. **🔒 SECURE**: Apply network isolation and firewall rules
5. **✅ TEST**: Verify all services work with consolidated setup

This consolidation will address the critical security vulnerabilities while creating a more maintainable and scalable architecture.