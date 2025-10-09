# BizOSaaS Platform - Staging Deployment Plan
## Dokploy VPS Staging Environment Setup

**Date:** October 9, 2025
**Target VPS:** 194.238.16.237
**Dokploy Admin:** bizoholic.digital@gmail.com
**Repository:** https://github.com/Bizoholic-Digital/bizosaas-platform.git
**Current Commit:** b78dc03

---

## Executive Summary

This document provides a comprehensive plan to deploy the BizOSaaS platform to the staging VPS environment using Dokploy. The deployment is based on the **100% Completion Roadmap** and current GitHub repository state.

### Current Platform Status

**From 100% Completion Roadmap:**
- **Overall Completion:** 85-90%
- **Frontend Apps:** 2/5 healthy (need to fix 3 unhealthy apps)
- **Backend Services:** Mostly complete
- **Wizards:** 2/7 have full UI
- **Infrastructure:** 22/25 containers healthy locally

**From GitHub Analysis:**
- **Latest Commit:** Fix platform logo and improve client portal configuration
- **Repository:** Clean, well-organized monorepo structure
- **Available Services:** All Dockerfiles present for deployment

---

## Part 1: Current Architecture Analysis

### 1.1 GitHub Repository Structure

```
bizosaas-platform/
├── ai/                          # AI services
│   └── services/
│       └── bizosaas-brain/      # FastAPI AI Central Hub (Port 8001)
├── backend/                     # Backend services
│   └── services/
│       ├── admin/sqladmin/      # SQLAdmin Dashboard (Port 8005)
│       ├── ai-agents/           # CrewAI Agents (Port 8000)
│       ├── amazon-sourcing/     # Amazon Product Sourcing (Port 8085)
│       ├── auth/                # Authentication Service (Port 8007)
│       ├── cms/                 # Wagtail CMS (Port 4000)
│       ├── crm/                 # Django CRM & Business Directory
│       ├── ecommerce/saleor/    # Saleor E-commerce (Port 8003)
│       └── temporal/            # Temporal Workflows (Port 8202)
├── frontend/                    # Frontend applications
│   └── apps/
│       ├── bizoholic-frontend/  # Marketing Website (Port 3008)
│       ├── bizosaas-admin/      # Admin Dashboard (Port 3009)
│       ├── business-directory/  # Business Directory (Port 3010)
│       ├── client-portal/       # Client Portal (Port 3001) ⚠️ ISSUE
│       ├── coreldove-frontend/  # E-commerce Store (Port 3007)
│       └── unified-auth/        # Auth UI (Port 3011)
├── infrastructure/              # Infrastructure configs
│   ├── vault/                   # HashiCorp Vault (Port 8200)
│   └── temporal/                # Temporal Server (Port 7233)
├── database/                    # Database schemas & migrations
├── analytics/                   # Analytics services
└── docs/                        # Documentation
```

### 1.2 Local Container Inventory

**Currently Running (Healthy):**
- `bizosaas-temporal` - Workflow orchestration
- `bizosaas-temporal-ui-8082` - Temporal UI
- `bizosaas-saleor-api-8003` - E-commerce API
- `bizosaas-elasticsearch-9200` - Search engine
- `bizoholic-traefik` - Reverse proxy
- `registry` - Local Docker registry

**Stopped/Unhealthy (Need Fixing):**
- `bizosaas-client-portal-3000` ⚠️ - Restarting (shows analytics instead of portal)
- `bizosaas-admin-3009` ⚠️ - Port 3009 needs health check fix
- `bizoholic-frontend-container` ⚠️ - Port 3000 needs auth integration
- `bizosaas-brain-core-8001` - Stopped FastAPI brain
- `bizosaas-vault` - Stopped secrets management
- `bizosaas-n8n` - Stopped workflow automation
- `bizosaas-superset-working` - Restarting analytics

### 1.3 Existing Dokploy Configuration

**From `/bizosaas/infrastructure/deployment/deployment/dokploy/bizosaas-platform/docker-compose.yml`:**

Services already configured for Dokploy:
1. **vault** - HashiCorp Vault (Port 8200)
2. **bizosaas-brain** - Central API Hub (Port 8001)
3. **event-bus** - Event Management (Port 8009)
4. **django-crm** - CRM Service (Port 8003)
5. **wagtail-cms** - CMS Service (Port 4000)
6. **ai-agents** - AI Agents (Port 8000)
7. **unified-dashboard** - Admin UI (Port 5004)
8. **telegram-integration** - Telegram Bots (Port 4006)
9. **image-integration** - Image Services (Port 4007)
10. **temporal-workflows** - Workflows (Port 8202)

---

## Part 2: Deployment Strategy

### 2.1 Deployment Phases

#### Phase 1: Infrastructure Layer (Week 1 - Days 1-2)
**Priority:** HIGH
**Estimated Time:** 2 days

**Services to Deploy:**
1. **PostgreSQL with pgvector** (External - Shared Infrastructure)
   - Database: bizosaas_main, bizosaas_auth, bizosaas_analytics
   - Extensions: pgvector, uuid-ossp, pg_trgm
   - Multi-tenant schema with RLS

2. **Redis** (External - Shared Infrastructure)
   - Caching and session storage
   - Message queue for events

3. **Vault** (Port 8200)
   - Secrets management
   - API key storage
   - Certificate management

4. **Elasticsearch** (Port 9200)
   - Search functionality
   - Log aggregation

5. **Temporal Server** (Port 7233)
   - Workflow orchestration
   - Background job processing

**Deployment Steps:**
```bash
# Step 1: SSH into VPS
ssh root@194.238.16.237

# Step 2: Clone repository
git clone https://github.com/Bizoholic-Digital/bizosaas-platform.git
cd bizosaas-platform

# Step 3: Create infrastructure docker-compose
# Use existing file from /bizosaas/infrastructure/deployment/deployment/dokploy/

# Step 4: Deploy via Dokploy
# Create new project in Dokploy: "bizosaas-infrastructure"
# Upload docker-compose for infrastructure services
```

#### Phase 2: Backend Services (Week 1 - Days 3-4)
**Priority:** HIGH
**Estimated Time:** 2 days

**Services to Deploy:**
1. **BizOSaaS Brain API** (Port 8001) - Central AI Hub
2. **Event Bus** (Port 8009) - Event management
3. **Auth Service** (Port 8007) - Authentication
4. **Django CRM** (Port 8003) - Customer management
5. **Wagtail CMS** (Port 4000) - Content management
6. **Saleor E-commerce** (Port 8003) - E-commerce backend
7. **AI Agents** (Port 8000) - CrewAI agents
8. **SQLAdmin** (Port 8005) - Database administration

**Critical Configuration:**
- All services connect via Central Brain API (Port 8001)
- Multi-tenant isolation enabled
- Vault integration for secrets
- Event bus for real-time updates

#### Phase 3: Frontend Applications (Week 1 - Day 5)
**Priority:** HIGH
**Estimated Time:** 1 day

**Services to Deploy:**
1. **Client Portal** (Port 3001) ⚠️ CRITICAL - Fix routing issue
2. **BizOSaaS Admin** (Port 3009) - Fix health check
3. **Bizoholic Frontend** (Port 3008) - Add auth integration
4. **CorelDove Frontend** (Port 3007) - E-commerce store
5. **Business Directory** (Port 3010) - Directory service

**Critical Fixes Required:**
1. **Client Portal** - Ensure shows dashboard, not analytics
2. **Admin Dashboard** - Fix health check to use 0.0.0.0
3. **Bizoholic** - Integrate authentication properly

#### Phase 4: Supporting Services (Week 2 - Days 1-2)
**Priority:** MEDIUM
**Estimated Time:** 2 days

**Services to Deploy:**
1. **Temporal Workflows** (Port 8202)
2. **Telegram Integration** (Port 4006)
3. **Image Integration** (Port 4007)
4. **Amazon Sourcing** (Port 8085)
5. **Superset Analytics** (Optional)
6. **n8n Workflows** (Port 5678) - Optional

#### Phase 5: Testing & Validation (Week 2 - Days 3-5)
**Priority:** HIGH
**Estimated Time:** 3 days

**Testing Checklist:**
- [ ] All containers healthy (25/25)
- [ ] All frontend apps load correctly
- [ ] Client portal shows correct dashboard
- [ ] Authentication works across apps
- [ ] API routes work through Central Hub
- [ ] Multi-tenant isolation verified
- [ ] Database connections stable
- [ ] Vault secrets accessible
- [ ] SSL certificates configured
- [ ] Domain mappings correct

---

## Part 3: Service-by-Service Deployment Guide

### 3.1 Infrastructure Services

#### Service: PostgreSQL with pgvector

**Docker Image:** `pgvector/pgvector:pg16`

**Environment Variables:**
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_DB=bizosaas_main
POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.UTF-8
```

**Volumes:**
```yaml
volumes:
  - postgres-data:/var/lib/postgresql/data
  - ./database/init:/docker-entrypoint-initdb.d
```

**Initialization Scripts:**
```sql
-- /database/init/01_create_databases.sql
CREATE DATABASE bizosaas_main;
CREATE DATABASE bizosaas_auth;
CREATE DATABASE bizosaas_analytics;

-- /database/init/02_enable_extensions.sql
\c bizosaas_main;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgvector";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- /database/init/03_multi_tenant_schema.sql
-- Create tenants table with RLS
CREATE TABLE IF NOT EXISTS tenants (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  subdomain VARCHAR(100) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enable Row Level Security
ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
```

**Deployment Command:**
```yaml
# Add to Dokploy project: bizosaas-infrastructure
# Service name: postgres
# Image: pgvector/pgvector:pg16
# Port: 5432
# Traefik: Disabled (internal only)
```

#### Service: Redis

**Docker Image:** `redis:7-alpine`

**Configuration:**
```yaml
redis:
  image: redis:7-alpine
  container_name: bizosaas-redis
  ports:
    - "6379:6379"
  command: redis-server --requirepass ${REDIS_PASSWORD}
  volumes:
    - redis-data:/data
  networks:
    - dokploy-network
  restart: unless-stopped
```

**Deployment Command:**
```bash
# Add to Dokploy: bizosaas-infrastructure
# Service: redis
# Image: redis:7-alpine
# Port: 6379 (internal)
```

#### Service: Vault

**Docker Image:** `hashicorp/vault:1.15.0`

**Configuration:**
```yaml
vault:
  image: hashicorp/vault:1.15.0
  container_name: bizosaas-vault
  ports:
    - "8200:8200"
  environment:
    - VAULT_DEV_ROOT_TOKEN_ID=${VAULT_ROOT_TOKEN}
    - VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200
    - VAULT_ADDR=http://0.0.0.0:8200
  cap_add:
    - IPC_LOCK
  volumes:
    - vault-data:/vault/data
    - vault-logs:/vault/logs
  networks:
    - dokploy-network
  restart: unless-stopped
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.vault.rule=Host(`vault.bizoholic.digital`)"
    - "traefik.http.services.vault.loadbalancer.server.port=8200"
```

**Initial Setup:**
```bash
# After deployment, initialize Vault
docker exec -it bizosaas-vault vault operator init

# Store unseal keys securely
# Unseal Vault
docker exec -it bizosaas-vault vault operator unseal <key1>
docker exec -it bizosaas-vault vault operator unseal <key2>
docker exec -it bizosaas-vault vault operator unseal <key3>
```

### 3.2 Backend Services

#### Service: BizOSaaS Brain API (Central Hub)

**Location:** `/bizosaas-platform/ai/services/bizosaas-brain/`

**Dockerfile:** Present at `Dockerfile`

**Build Command:**
```bash
cd /home/alagiri/projects/bizoholic/bizosaas-platform/ai/services/bizosaas-brain
docker build -t bizosaas/brain:latest .
```

**Environment Variables:**
```env
# Vault Configuration
VAULT_ADDR=http://vault:8200
VAULT_TOKEN=${VAULT_ROOT_TOKEN}
VAULT_NAMESPACE=bizosaas

# Database
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=bizosaas_main
POSTGRES_USER=postgres
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=${REDIS_PASSWORD}
REDIS_DB=0

# Event Bus
EVENT_BUS_URL=http://event-bus:8009
EVENT_BUS_ENABLED=true
TENANT_ISOLATION_ENABLED=true

# Security
JWT_SECRET_KEY=${JWT_SECRET_KEY}
ENCRYPTION_KEY=${ENCRYPTION_KEY}
SERVICE_SECRET=${SERVICE_SECRET}

# AI API Keys
OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
OPENAI_API_KEY=${OPENAI_API_KEY}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

# Settings
NODE_ENV=production
DEBUG=false
LOG_LEVEL=info
BRAIN_API_VERSION=2.0.0
```

**Docker Compose:**
```yaml
bizosaas-brain:
  image: bizosaas/brain:latest
  container_name: bizosaas-brain
  ports:
    - "8001:8001"
  environment:
    # ... (all env vars above)
  networks:
    - dokploy-network
  depends_on:
    - postgres
    - redis
    - vault
  restart: unless-stopped
  healthcheck:
    test: ["CMD", "curl", "-f", "http://0.0.0.0:8001/health"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 40s
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.brain.rule=Host(`api.bizoholic.digital`)"
    - "traefik.http.services.brain.loadbalancer.server.port=8001"
    - "traefik.http.routers.brain.tls=true"
    - "traefik.http.routers.brain.tls.certresolver=letsencrypt"
```

**Deployment Steps:**
```bash
# 1. Build image locally
cd bizosaas-platform/ai/services/bizosaas-brain
docker build -t bizosaas/brain:staging .

# 2. Tag for registry
docker tag bizosaas/brain:staging registry.bizoholic.digital/bizosaas/brain:staging

# 3. Push to Dokploy registry
docker push registry.bizoholic.digital/bizosaas/brain:staging

# 4. Deploy via Dokploy
# Create service in Dokploy: bizosaas-brain
# Image: registry.bizoholic.digital/bizosaas/brain:staging
# Port: 8001
# Domain: api.bizoholic.digital
```

#### Service: Auth Service

**Location:** `/bizosaas-platform/backend/services/auth/`

**Build Command:**
```bash
cd bizosaas-platform/backend/services/auth
docker build -t bizosaas/auth:staging .
```

**Environment Variables:**
```env
# Database
DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/bizosaas_auth

# JWT
JWT_SECRET=${JWT_SECRET_KEY}
JWT_ALGORITHM=HS256
JWT_EXPIRATION=86400

# Vault
VAULT_ADDR=http://vault:8200
VAULT_TOKEN=${VAULT_ROOT_TOKEN}

# Brain API
BRAIN_API_URL=http://bizosaas-brain:8001
BRAIN_API_TOKEN=${SERVICE_SECRET}

# CORS
ALLOWED_ORIGINS=https://portal.bizoholic.digital,https://admin.bizoholic.digital,https://bizoholic.digital

# Security
BCRYPT_ROUNDS=12
PASSWORD_MIN_LENGTH=8
ENABLE_MFA=true
```

**Docker Compose:**
```yaml
auth-service:
  image: bizosaas/auth:staging
  container_name: bizosaas-auth
  ports:
    - "8007:8007"
  environment:
    # ... (all env vars above)
  networks:
    - dokploy-network
  depends_on:
    - postgres
    - vault
    - bizosaas-brain
  restart: unless-stopped
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.auth.rule=Host(`auth.bizoholic.digital`)"
    - "traefik.http.services.auth.loadbalancer.server.port=8007"
```

### 3.3 Frontend Services

#### Service: Client Portal (Port 3001) ⚠️ CRITICAL FIX

**Location:** `/bizosaas-platform/frontend/apps/client-portal/`

**Issue:** Currently showing analytics dashboard instead of main portal

**Root Cause Analysis:**
- Next.js routing showing wrong page
- Analytics route taking precedence
- Metadata/title override issue
- Cache not clearing properly

**Fix Required:**
```typescript
// /app/page.tsx - Ensure this is the main portal page
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Client Portal - Dashboard',
  description: 'Your comprehensive business management portal',
};

export default function PortalPage() {
  return (
    <main>
      {/* Full client portal dashboard with sidebar */}
      <ClientPortalDashboard />
    </main>
  );
}
```

**Dockerfile Fix:**
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci

# Copy application
COPY . .

# Build Next.js
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app

# Copy built files
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3001

ENV PORT=3001
ENV HOSTNAME=0.0.0.0
ENV NODE_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://0.0.0.0:3001/ || exit 1

CMD ["node", "server.js"]
```

**Environment Variables:**
```env
# API Configuration
NEXT_PUBLIC_API_BASE_URL=https://api.bizoholic.digital
NEXT_PUBLIC_AUTH_API_URL=https://auth.bizoholic.digital

# App Configuration
NEXT_PUBLIC_APP_NAME=Client Portal
NEXT_PUBLIC_APP_ENV=production
NEXT_PUBLIC_TENANT_MODE=client

# Feature Flags
NEXT_PUBLIC_ENABLE_AUTH=true
NEXT_PUBLIC_ENABLE_CAMPAIGN_APPROVAL=true
NEXT_PUBLIC_ENABLE_REPORT_VIEWER=true
NEXT_PUBLIC_ENABLE_COMMUNICATION_HUB=true
```

**Build & Deploy:**
```bash
# 1. Fix the routing issue locally first
cd bizosaas-platform/frontend/apps/client-portal

# 2. Clear Next.js cache
rm -rf .next

# 3. Test locally
npm run dev

# 4. Build Docker image
docker build -t bizosaas/client-portal:staging .

# 5. Push to registry
docker tag bizosaas/client-portal:staging registry.bizoholic.digital/bizosaas/client-portal:staging
docker push registry.bizoholic.digital/bizosaas/client-portal:staging

# 6. Deploy via Dokploy
# Service: client-portal
# Image: registry.bizoholic.digital/bizosaas/client-portal:staging
# Port: 3001
# Domain: portal.bizoholic.digital
```

#### Service: BizOSaaS Admin (Port 3009) ⚠️ HEALTH CHECK FIX

**Location:** `/bizosaas-platform/frontend/apps/bizosaas-admin/`

**Issue:** Health check failing - app listens on container IP, not localhost

**Dockerfile Fix:**
```dockerfile
# Change health check from localhost to 0.0.0.0
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://0.0.0.0:3009/api/health || exit 1

# Ensure app binds to 0.0.0.0
ENV HOSTNAME=0.0.0.0
ENV PORT=3009
```

**Build & Deploy:**
```bash
cd bizosaas-platform/frontend/apps/bizosaas-admin
docker build -t bizosaas/admin:staging .
docker push registry.bizoholic.digital/bizosaas/admin:staging
```

#### Service: Bizoholic Frontend (Port 3008) ⚠️ AUTH INTEGRATION

**Location:** `/bizosaas-platform/frontend/apps/bizoholic-frontend/`

**Issue:** Authentication integration incomplete

**Required Additions:**
1. Auth provider integration
2. Protected routes middleware
3. JWT token management
4. Login/logout pages

**Environment Variables:**
```env
NEXT_PUBLIC_AUTH_API_URL=https://auth.bizoholic.digital
NEXT_PUBLIC_BRAIN_API_URL=https://api.bizoholic.digital
NEXT_PUBLIC_ENABLE_AUTH=true
```

**Build & Deploy:**
```bash
cd bizosaas-platform/frontend/apps/bizoholic-frontend
docker build -t bizosaas/bizoholic:staging .
docker push registry.bizoholic.digital/bizosaas/bizoholic:staging
```

---

## Part 4: Deployment Execution Plan

### 4.1 Pre-Deployment Checklist

**Infrastructure Preparation:**
- [ ] VPS accessible via SSH (root@194.238.16.237)
- [ ] Dokploy admin access (bizoholic.digital@gmail.com)
- [ ] GitHub repository access
- [ ] Domain DNS configured (*.bizoholic.digital → 194.238.16.237)
- [ ] SSL certificates via Let's Encrypt
- [ ] Docker registry configured

**Credential Preparation:**
- [ ] All API keys from ~/projects/credentials.md
- [ ] Database passwords generated
- [ ] JWT secrets generated
- [ ] Vault root token generated
- [ ] Service secrets generated

**Local Preparation:**
- [ ] All Dockerfiles reviewed
- [ ] Environment templates created
- [ ] Build scripts prepared
- [ ] Test data prepared
- [ ] Backup plan established

### 4.2 Deployment Timeline

**Week 1: Core Infrastructure & Backend**

**Monday (Day 1):**
- [ ] 09:00-10:00: SSH setup, repository clone
- [ ] 10:00-12:00: Deploy PostgreSQL, Redis, Vault
- [ ] 12:00-13:00: Initialize databases, create schemas
- [ ] 13:00-14:00: Lunch break
- [ ] 14:00-16:00: Deploy Elasticsearch, Temporal
- [ ] 16:00-17:00: Verify infrastructure health

**Tuesday (Day 2):**
- [ ] 09:00-10:00: Build BizOSaaS Brain API image
- [ ] 10:00-12:00: Deploy Brain API, test endpoints
- [ ] 12:00-13:00: Deploy Event Bus
- [ ] 13:00-14:00: Lunch break
- [ ] 14:00-16:00: Deploy Auth Service
- [ ] 16:00-17:00: Test authentication flow

**Wednesday (Day 3):**
- [ ] 09:00-11:00: Deploy Django CRM
- [ ] 11:00-13:00: Deploy Wagtail CMS
- [ ] 13:00-14:00: Lunch break
- [ ] 14:00-16:00: Deploy Saleor E-commerce
- [ ] 16:00-17:00: Verify backend services

**Thursday (Day 4):**
- [ ] 09:00-11:00: Deploy AI Agents
- [ ] 11:00-13:00: Deploy SQLAdmin Dashboard
- [ ] 13:00-14:00: Lunch break
- [ ] 14:00-16:00: Test backend integration
- [ ] 16:00-17:00: Document issues

**Friday (Day 5):**
- [ ] 09:00-10:00: Fix Client Portal routing
- [ ] 10:00-11:00: Deploy Client Portal (Port 3001)
- [ ] 11:00-12:00: Fix Admin health check
- [ ] 12:00-13:00: Deploy BizOSaaS Admin (Port 3009)
- [ ] 13:00-14:00: Lunch break
- [ ] 14:00-15:00: Deploy Bizoholic Frontend (Port 3008)
- [ ] 15:00-16:00: Deploy CorelDove Frontend (Port 3007)
- [ ] 16:00-17:00: Test all frontend apps

**Week 2: Testing & Optimization**

**Monday (Day 1):**
- [ ] 09:00-12:00: Deploy supporting services (Temporal, Telegram, Images)
- [ ] 12:00-13:00: Lunch break
- [ ] 13:00-17:00: Integration testing

**Tuesday (Day 2):**
- [ ] 09:00-17:00: End-to-end testing, bug fixes

**Wednesday (Day 3):**
- [ ] 09:00-17:00: Performance optimization, load testing

**Thursday (Day 4):**
- [ ] 09:00-17:00: Security audit, SSL configuration

**Friday (Day 5):**
- [ ] 09:00-12:00: Documentation finalization
- [ ] 12:00-13:00: Stakeholder demo
- [ ] 13:00-17:00: Final adjustments, go-live

### 4.3 Docker Compose for Dokploy

**Create:** `/bizosaas-platform/docker-compose.staging.yml`

```yaml
version: '3.8'

# BizOSaaS Platform - Staging Environment
# Dokploy VPS: 194.238.16.237
# Updated: October 9, 2025

services:
  # Infrastructure Layer
  postgres:
    image: pgvector/pgvector:pg16
    container_name: bizosaas-postgres-staging
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: bizosaas_main
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d
    networks:
      - dokploy-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: bizosaas-redis-staging
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/data
    networks:
      - dokploy-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  vault:
    image: hashicorp/vault:1.15.0
    container_name: bizosaas-vault-staging
    ports:
      - "8200:8200"
    environment:
      VAULT_DEV_ROOT_TOKEN_ID: ${VAULT_ROOT_TOKEN}
      VAULT_DEV_LISTEN_ADDRESS: 0.0.0.0:8200
      VAULT_ADDR: http://0.0.0.0:8200
    cap_add:
      - IPC_LOCK
    volumes:
      - vault-data:/vault/data
      - vault-logs:/vault/logs
    networks:
      - dokploy-network
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.vault.rule=Host(`vault.bizoholic.digital`)"
      - "traefik.http.services.vault.loadbalancer.server.port=8200"
      - "traefik.http.routers.vault.tls=true"
      - "traefik.http.routers.vault.tls.certresolver=letsencrypt"

  # Core Backend Services
  bizosaas-brain:
    image: registry.bizoholic.digital/bizosaas/brain:staging
    container_name: bizosaas-brain-staging
    ports:
      - "8001:8001"
    environment:
      # (All environment variables from Part 3.2)
      VAULT_ADDR: http://vault:8200
      VAULT_TOKEN: ${VAULT_ROOT_TOKEN}
      POSTGRES_HOST: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      REDIS_HOST: redis
      REDIS_PASSWORD: ${REDIS_PASSWORD}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      NODE_ENV: production
    networks:
      - dokploy-network
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      vault:
        condition: service_started
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.brain.rule=Host(`api.bizoholic.digital`)"
      - "traefik.http.services.brain.loadbalancer.server.port=8001"
      - "traefik.http.routers.brain.tls=true"
      - "traefik.http.routers.brain.tls.certresolver=letsencrypt"

  auth-service:
    image: registry.bizoholic.digital/bizosaas/auth:staging
    container_name: bizosaas-auth-staging
    ports:
      - "8007:8007"
    environment:
      DATABASE_URL: postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/bizosaas_auth
      JWT_SECRET: ${JWT_SECRET_KEY}
      VAULT_ADDR: http://vault:8200
      VAULT_TOKEN: ${VAULT_ROOT_TOKEN}
      BRAIN_API_URL: http://bizosaas-brain:8001
      ALLOWED_ORIGINS: https://portal.bizoholic.digital,https://admin.bizoholic.digital
    networks:
      - dokploy-network
    depends_on:
      postgres:
        condition: service_healthy
      vault:
        condition: service_started
      bizosaas-brain:
        condition: service_started
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.auth.rule=Host(`auth.bizoholic.digital`)"
      - "traefik.http.services.auth.loadbalancer.server.port=8007"
      - "traefik.http.routers.auth.tls=true"
      - "traefik.http.routers.auth.tls.certresolver=letsencrypt"

  # Frontend Services
  client-portal:
    image: registry.bizoholic.digital/bizosaas/client-portal:staging
    container_name: bizosaas-client-portal-staging
    ports:
      - "3001:3001"
    environment:
      NEXT_PUBLIC_API_BASE_URL: https://api.bizoholic.digital
      NEXT_PUBLIC_AUTH_API_URL: https://auth.bizoholic.digital
      NEXT_PUBLIC_APP_NAME: Client Portal
      NEXT_PUBLIC_TENANT_MODE: client
      NODE_ENV: production
      PORT: 3001
      HOSTNAME: 0.0.0.0
    networks:
      - dokploy-network
    depends_on:
      - bizosaas-brain
      - auth-service
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.portal.rule=Host(`portal.bizoholic.digital`)"
      - "traefik.http.services.portal.loadbalancer.server.port=3001"
      - "traefik.http.routers.portal.tls=true"
      - "traefik.http.routers.portal.tls.certresolver=letsencrypt"

  bizosaas-admin:
    image: registry.bizoholic.digital/bizosaas/admin:staging
    container_name: bizosaas-admin-staging
    ports:
      - "3009:3009"
    environment:
      NEXT_PUBLIC_API_BASE_URL: https://api.bizoholic.digital
      NEXT_PUBLIC_AUTH_API_URL: https://auth.bizoholic.digital
      NODE_ENV: production
      PORT: 3009
      HOSTNAME: 0.0.0.0
    networks:
      - dokploy-network
    depends_on:
      - bizosaas-brain
      - auth-service
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.admin.rule=Host(`admin.bizoholic.digital`)"
      - "traefik.http.services.admin.loadbalancer.server.port=3009"
      - "traefik.http.routers.admin.tls=true"
      - "traefik.http.routers.admin.tls.certresolver=letsencrypt"

  bizoholic-frontend:
    image: registry.bizoholic.digital/bizosaas/bizoholic:staging
    container_name: bizoholic-frontend-staging
    ports:
      - "3008:3008"
    environment:
      NEXT_PUBLIC_API_BASE_URL: https://api.bizoholic.digital
      NEXT_PUBLIC_AUTH_API_URL: https://auth.bizoholic.digital
      NODE_ENV: production
      PORT: 3008
      HOSTNAME: 0.0.0.0
    networks:
      - dokploy-network
    depends_on:
      - bizosaas-brain
      - auth-service
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.bizoholic.rule=Host(`bizoholic.digital`) || Host(`www.bizoholic.digital`)"
      - "traefik.http.services.bizoholic.loadbalancer.server.port=3008"
      - "traefik.http.routers.bizoholic.tls=true"
      - "traefik.http.routers.bizoholic.tls.certresolver=letsencrypt"

volumes:
  postgres-data:
    driver: local
  redis-data:
    driver: local
  vault-data:
    driver: local
  vault-logs:
    driver: local

networks:
  dokploy-network:
    external: true
```

---

## Part 5: Environment Variables Template

**Create:** `/bizosaas-platform/.env.staging`

```env
# BizOSaaS Platform - Staging Environment
# VPS: 194.238.16.237
# Updated: October 9, 2025

# ==================== DATABASE ====================
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<GENERATE_STRONG_PASSWORD>
POSTGRES_DB=bizosaas_main
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# ==================== REDIS ====================
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=<GENERATE_STRONG_PASSWORD>

# ==================== VAULT ====================
VAULT_ADDR=http://vault:8200
VAULT_ROOT_TOKEN=<GENERATE_VAULT_TOKEN>
VAULT_NAMESPACE=bizosaas

# ==================== SECURITY ====================
JWT_SECRET_KEY=<GENERATE_JWT_SECRET>
ENCRYPTION_KEY=<GENERATE_ENCRYPTION_KEY>
SERVICE_SECRET=<GENERATE_SERVICE_SECRET>
DJANGO_SECRET_KEY=<GENERATE_DJANGO_SECRET>
WAGTAIL_SECRET_KEY=<GENERATE_WAGTAIL_SECRET>

# ==================== AI API KEYS ====================
# From ~/projects/credentials.md
OPENAI_API_KEY=<FROM_CREDENTIALS_FILE>
ANTHROPIC_API_KEY=<FROM_CREDENTIALS_FILE>
OPENROUTER_API_KEY=<FROM_CREDENTIALS_FILE>

# ==================== TELEGRAM BOTS ====================
# From ~/projects/credentials.md
TELEGRAM_JONNYAI_BOT_TOKEN=<FROM_CREDENTIALS_FILE>
TELEGRAM_BIZOHOLIC_BOT_TOKEN=<FROM_CREDENTIALS_FILE>
TELEGRAM_DEALS4ALL_BOT_TOKEN=<FROM_CREDENTIALS_FILE>
TELEGRAM_BOTTRADER_BOT_TOKEN=<FROM_CREDENTIALS_FILE>
TELEGRAM_GOGOFATHER_BOT_TOKEN=<FROM_CREDENTIALS_FILE>

# ==================== IMAGE APIS ====================
PEXELS_API_KEY=<FROM_CREDENTIALS_FILE>
UNSPLASH_ACCESS_KEY=<FROM_CREDENTIALS_FILE>
PIXABAY_API_KEY=<FROM_CREDENTIALS_FILE>

# ==================== AMAZON SP-API ====================
AMAZON_ACCESS_KEY=<FROM_CREDENTIALS_FILE>
AMAZON_SECRET_KEY=<FROM_CREDENTIALS_FILE>
AMAZON_PARTNER_TAG=<FROM_CREDENTIALS_FILE>

# ==================== STRIPE ====================
STRIPE_PUBLIC_KEY=<FROM_CREDENTIALS_FILE>
STRIPE_SECRET_KEY=<FROM_CREDENTIALS_FILE>
STRIPE_WEBHOOK_SECRET=<FROM_CREDENTIALS_FILE>

# ==================== APPLICATION URLS ====================
NEXT_PUBLIC_API_BASE_URL=https://api.bizoholic.digital
NEXT_PUBLIC_AUTH_API_URL=https://auth.bizoholic.digital
BRAIN_API_URL=http://bizosaas-brain:8001

# ==================== CORS ====================
ALLOWED_ORIGINS=https://portal.bizoholic.digital,https://admin.bizoholic.digital,https://bizoholic.digital

# ==================== PRODUCTION SETTINGS ====================
NODE_ENV=production
DEBUG=false
LOG_LEVEL=info
```

---

## Part 6: Deployment Scripts

### 6.1 Build All Images Script

**Create:** `/scripts/build-staging-images.sh`

```bash
#!/bin/bash

# BizOSaaS Platform - Build All Staging Images
# Date: October 9, 2025

set -e  # Exit on error

REGISTRY="registry.bizoholic.digital"
TAG="staging"

echo "🚀 Building BizOSaaS Platform Staging Images..."

# Navigate to project root
cd /home/alagiri/projects/bizoholic/bizosaas-platform

# Backend Services
echo "📦 Building Backend Services..."

echo "  Building Brain API..."
cd ai/services/bizosaas-brain
docker build -t $REGISTRY/bizosaas/brain:$TAG .

echo "  Building Auth Service..."
cd ../../backend/services/auth
docker build -t $REGISTRY/bizosaas/auth:$TAG .

echo "  Building Django CRM..."
cd ../crm/django-crm
docker build -t $REGISTRY/bizosaas/django-crm:$TAG .

echo "  Building Wagtail CMS..."
cd ../cms
docker build -t $REGISTRY/bizosaas/wagtail-cms:$TAG .

echo "  Building AI Agents..."
cd ../ai-agents
docker build -t $REGISTRY/bizosaas/ai-agents:$TAG .

echo "  Building SQLAdmin..."
cd ../admin/sqladmin
docker build -t $REGISTRY/bizosaas/sqladmin:$TAG .

# Frontend Services
echo "📦 Building Frontend Services..."

echo "  Building Client Portal..."
cd ../../../../frontend/apps/client-portal
docker build -t $REGISTRY/bizosaas/client-portal:$TAG .

echo "  Building BizOSaaS Admin..."
cd ../bizosaas-admin
docker build -t $REGISTRY/bizosaas/admin:$TAG .

echo "  Building Bizoholic Frontend..."
cd ../bizoholic-frontend
docker build -t $REGISTRY/bizosaas/bizoholic:$TAG .

echo "  Building CorelDove Frontend..."
cd ../coreldove-frontend
docker build -t $REGISTRY/bizosaas/coreldove:$TAG .

echo "✅ All images built successfully!"

# Push to registry
echo "📤 Pushing images to registry..."

docker push $REGISTRY/bizosaas/brain:$TAG
docker push $REGISTRY/bizosaas/auth:$TAG
docker push $REGISTRY/bizosaas/django-crm:$TAG
docker push $REGISTRY/bizosaas/wagtail-cms:$TAG
docker push $REGISTRY/bizosaas/ai-agents:$TAG
docker push $REGISTRY/bizosaas/sqladmin:$TAG
docker push $REGISTRY/bizosaas/client-portal:$TAG
docker push $REGISTRY/bizosaas/admin:$TAG
docker push $REGISTRY/bizosaas/bizoholic:$TAG
docker push $REGISTRY/bizosaas/coreldove:$TAG

echo "✅ All images pushed to registry!"
echo "🎉 Build complete! Ready for deployment."
```

### 6.2 Deploy to Dokploy Script

**Create:** `/scripts/deploy-staging.sh`

```bash
#!/bin/bash

# BizOSaaS Platform - Deploy to Dokploy Staging
# VPS: 194.238.16.237
# Date: October 9, 2025

set -e

VPS_HOST="194.238.16.237"
VPS_USER="root"
DEPLOY_DIR="/opt/bizosaas-platform"

echo "🚀 Deploying BizOSaaS Platform to Staging..."

# 1. Copy files to VPS
echo "📤 Uploading deployment files..."
scp docker-compose.staging.yml $VPS_USER@$VPS_HOST:$DEPLOY_DIR/
scp .env.staging $VPS_USER@$VPS_HOST:$DEPLOY_DIR/.env
scp -r database/init $VPS_USER@$VPS_HOST:$DEPLOY_DIR/database/

# 2. Deploy via SSH
echo "🔧 Deploying services on VPS..."
ssh $VPS_USER@$VPS_HOST << 'ENDSSH'
cd /opt/bizosaas-platform

# Pull latest images
docker-compose -f docker-compose.staging.yml pull

# Stop existing containers
docker-compose -f docker-compose.staging.yml down

# Start new containers
docker-compose -f docker-compose.staging.yml up -d

# Check health
sleep 30
docker-compose -f docker-compose.staging.yml ps

echo "✅ Deployment complete!"
ENDSSH

echo "🎉 BizOSaaS Platform deployed to staging!"
echo "🌐 Access URLs:"
echo "  - API: https://api.bizoholic.digital"
echo "  - Portal: https://portal.bizoholic.digital"
echo "  - Admin: https://admin.bizoholic.digital"
echo "  - Website: https://bizoholic.digital"
```

---

## Part 7: Post-Deployment Validation

### 7.1 Health Check Script

**Create:** `/scripts/check-staging-health.sh`

```bash
#!/bin/bash

# BizOSaaS Platform - Staging Health Check
# Date: October 9, 2025

STAGING_API="https://api.bizoholic.digital"
STAGING_PORTAL="https://portal.bizoholic.digital"
STAGING_ADMIN="https://admin.bizoholic.digital"
STAGING_WEB="https://bizoholic.digital"

echo "🏥 Checking BizOSaaS Platform Health..."

# Check API
echo -n "API (Brain): "
if curl -f -s $STAGING_API/health > /dev/null; then
  echo "✅ Healthy"
else
  echo "❌ Unhealthy"
fi

# Check Portal
echo -n "Client Portal: "
if curl -f -s $STAGING_PORTAL > /dev/null; then
  echo "✅ Healthy"
else
  echo "❌ Unhealthy"
fi

# Check Admin
echo -n "Admin Dashboard: "
if curl -f -s $STAGING_ADMIN > /dev/null; then
  echo "✅ Healthy"
else
  echo "❌ Unhealthy"
fi

# Check Website
echo -n "Bizoholic Website: "
if curl -f -s $STAGING_WEB > /dev/null; then
  echo "✅ Healthy"
else
  echo "❌ Unhealthy"
fi

echo ""
echo "📊 Full Status Report:"
ssh root@194.238.16.237 "cd /opt/bizosaas-platform && docker-compose -f docker-compose.staging.yml ps"
```

### 7.2 Validation Checklist

**Infrastructure:**
- [ ] PostgreSQL healthy and accepting connections
- [ ] Redis responding to ping
- [ ] Vault unsealed and accessible
- [ ] Elasticsearch cluster green status
- [ ] Temporal server running

**Backend Services:**
- [ ] Brain API responding at https://api.bizoholic.digital/health
- [ ] Auth service login/logout working
- [ ] Django CRM API endpoints responding
- [ ] Wagtail CMS admin accessible
- [ ] Saleor API returning products
- [ ] AI Agents responding to requests
- [ ] SQLAdmin dashboard accessible

**Frontend Applications:**
- [ ] Client Portal loading dashboard (not analytics!) ⚠️
- [ ] BizOSaaS Admin healthy (not health check error) ⚠️
- [ ] Bizoholic website loading with content
- [ ] CorelDove store showing products
- [ ] All pages have SSL certificates
- [ ] Authentication working across apps

**Integration Tests:**
- [ ] Contact form submission works (Bizoholic → CRM)
- [ ] User login/logout across portals
- [ ] Product creation in Saleor visible in store
- [ ] Content changes in Wagtail reflect on site
- [ ] Lead creation in CRM triggers notifications
- [ ] Multi-tenant isolation verified
- [ ] API routes through Central Hub work

---

## Part 8: Rollback Plan

### 8.1 Rollback Script

**Create:** `/scripts/rollback-staging.sh`

```bash
#!/bin/bash

# BizOSaaS Platform - Rollback Staging Deployment
# Date: October 9, 2025

VPS_HOST="194.238.16.237"
VPS_USER="root"

echo "⚠️  Rolling back staging deployment..."

ssh $VPS_USER@$VPS_HOST << 'ENDSSH'
cd /opt/bizosaas-platform

# Stop current deployment
docker-compose -f docker-compose.staging.yml down

# Restore previous version (if backed up)
if [ -f docker-compose.staging.yml.backup ]; then
  mv docker-compose.staging.yml.backup docker-compose.staging.yml
  docker-compose -f docker-compose.staging.yml up -d
  echo "✅ Rolled back to previous version"
else
  echo "❌ No backup found - manual intervention required"
fi
ENDSSH
```

### 8.2 Backup Procedure

Before each deployment:
```bash
# Backup current configuration
ssh root@194.238.16.237 << 'ENDSSH'
cd /opt/bizosaas-platform
cp docker-compose.staging.yml docker-compose.staging.yml.backup
cp .env .env.backup

# Backup database
docker exec bizosaas-postgres-staging pg_dump -U postgres bizosaas_main > backup_$(date +%Y%m%d_%H%M%S).sql
ENDSSH
```

---

## Part 9: Success Metrics

### 9.1 Completion Criteria

**Infrastructure (100% Required):**
- [x] PostgreSQL with pgvector deployed and healthy
- [x] Redis deployed and responding
- [x] Vault deployed, initialized, and unsealed
- [x] Elasticsearch cluster green
- [x] Temporal server running workflows

**Backend Services (100% Required):**
- [ ] Brain API (Central Hub) healthy - Port 8001
- [ ] Auth Service healthy - Port 8007
- [ ] Django CRM healthy - Port 8003
- [ ] Wagtail CMS healthy - Port 4000
- [ ] Saleor E-commerce healthy - Port 8003
- [ ] AI Agents healthy - Port 8000
- [ ] SQLAdmin healthy - Port 8005

**Frontend Applications (100% Required):**
- [ ] Client Portal healthy - Port 3001 (shows dashboard, NOT analytics)
- [ ] BizOSaaS Admin healthy - Port 3009 (health check passing)
- [ ] Bizoholic Frontend healthy - Port 3008 (auth working)
- [ ] CorelDove Frontend healthy - Port 3007
- [ ] All apps have SSL certificates

**Integration (100% Required):**
- [ ] All API routes go through Central Hub (Port 8001)
- [ ] Authentication works across all apps
- [ ] Multi-tenant isolation verified
- [ ] Contact forms create CRM leads
- [ ] E-commerce orders persist correctly

**Performance (90% Required):**
- [ ] API response time < 500ms (p95)
- [ ] Frontend load time < 3s
- [ ] Database queries < 100ms (p95)
- [ ] All containers use < 80% memory

**Security (100% Required):**
- [ ] All services behind SSL
- [ ] Secrets stored in Vault
- [ ] Row-level security enabled
- [ ] CORS properly configured
- [ ] JWT tokens validated

### 9.2 Final Verification

**Run this command after deployment:**
```bash
# SSH into VPS
ssh root@194.238.16.237

# Check all containers
cd /opt/bizosaas-platform
docker-compose -f docker-compose.staging.yml ps

# Expected output: All services "Up" and "healthy"
```

**Test these URLs:**
1. https://api.bizoholic.digital/health → 200 OK
2. https://auth.bizoholic.digital/health → 200 OK
3. https://portal.bizoholic.digital → Client Portal Dashboard
4. https://admin.bizoholic.digital → Admin Dashboard
5. https://bizoholic.digital → Marketing Website

---

## Part 10: Next Steps After Staging

### 10.1 Immediate Follow-Up (Week 3)

**Monday:**
- [ ] Stakeholder demo of staging environment
- [ ] Collect feedback on user experience
- [ ] Document any issues found

**Tuesday-Wednesday:**
- [ ] Fix bugs identified in staging
- [ ] Optimize performance bottlenecks
- [ ] Complete wizard UIs (based on roadmap)

**Thursday-Friday:**
- [ ] Security audit
- [ ] Load testing
- [ ] Prepare for production

### 10.2 Production Deployment (Week 4)

**Prerequisites:**
- [ ] All staging tests passing
- [ ] Performance meets requirements
- [ ] Security audit complete
- [ ] Documentation complete
- [ ] Backup/restore tested

**Production Deployment:**
- Follow same process as staging
- Use production environment variables
- Enable monitoring and alerting
- Set up automated backups
- Configure auto-scaling

---

## Conclusion

This deployment plan provides a comprehensive, step-by-step guide to deploying the BizOSaaS platform to the Dokploy staging environment. The plan is based on:

1. **100% Completion Roadmap** - Addresses all 3 unhealthy frontend apps
2. **Current GitHub Repository** - Uses actual code and Dockerfiles
3. **Local Container Analysis** - Understands what's working and what's not
4. **Dokploy Best Practices** - Uses proper Docker Compose structure

**Critical Success Factors:**
- Fix Client Portal routing before deployment
- Fix Admin dashboard health check
- Integrate authentication properly
- Test thoroughly before moving to production

**Timeline:** 2 weeks to complete staging deployment and testing

**Next Action:** Begin with Phase 1 (Infrastructure Layer) on Monday, Week 1

---

**Document Version:** 1.0
**Last Updated:** October 9, 2025
**Author:** BizOSaaS Platform Team
**Review Date:** After each deployment phase

**Ready to deploy! 🚀**
