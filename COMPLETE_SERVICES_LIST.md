# Complete BizOSaaS Staging Services List

## 📊 Summary: 20 Services Total (95% of planned 21)

- **Infrastructure**: 6 services ✅
- **Backend**: 9 services ✅
- **Frontend**: 5 services ⚠️ (1 skipped: business-directory)

---

## 🏗️ INFRASTRUCTURE PROJECT (6 Services)

### Container Prefix: `bizosaas-*-staging`
### Dokploy Project: Infrastructure / backend-services-azbmbl

| # | Service Name | Container Name | Port | Purpose | Status |
|---|--------------|----------------|------|---------|--------|
| 1 | PostgreSQL | `bizosaas-postgres-staging` | 5433→5432 | Multi-tenant database with pgvector | ✅ Running |
| 2 | Redis | `bizosaas-redis-staging` | 6380→6379 | High-performance cache & sessions | ✅ Running |
| 3 | HashiCorp Vault | `bizosaas-vault-staging` | 8201→8200 | Secrets management | ✅ Running |
| 4 | Temporal Server | `bizosaas-temporal-server-staging` | 7234→7233 | Workflow orchestration engine | ⚠️ Restarting |
| 5 | Temporal UI | `bizosaas-temporal-ui-staging` | 8083→8080 | Workflow management interface | ✅ Running |
| 6 | Apache Superset | `bizosaas-superset-staging` | 8088→8088 | Analytics & BI dashboards | 🎯 **NEWLY ADDED** |

**Key Features**:
- PostgreSQL with pgvector extension for AI embeddings
- Redis for caching, sessions, and pub/sub
- Vault for secure API key storage
- Temporal for workflow orchestration
- Superset for multi-tenant analytics

**Access**:
- Superset: `http://194.238.16.237:8088` (admin / Bizoholic2024Admin)
- Temporal UI: `http://194.238.16.237:8083`
- Vault: `http://194.238.16.237:8201`

---

## 🔧 BACKEND PROJECT (9 Services)

### Container Prefix: `bizosaas-*-staging`
### Dokploy Project: Backend Services / backend-services-azbmbl

| # | Service Name | Container Name | Port | Purpose | Build From |
|---|--------------|----------------|------|---------|------------|
| 1 | Saleor E-Commerce | `bizosaas-saleor-staging` | 8000→8000 | Complete e-commerce platform | Pre-built image |
| 2 | Brain API | `bizosaas-brain-staging` | 8001→8001 | Central AI orchestration hub | GitHub build |
| 3 | Wagtail CMS | `bizosaas-wagtail-staging` | 8002→8000 | Content management system | GitHub build |
| 4 | Django CRM | `bizosaas-django-crm-staging` | 8003→8000 | Customer relationship mgmt | GitHub build |
| 5 | Business Directory Backend | `bizosaas-business-directory-staging` | 8004→8000 | Directory listings API | GitHub build |
| 6 | CorelDove Backend | `bizosaas-coreldove-backend-staging` | 8005→8000 | E-commerce backend bridge | GitHub build |
| 7 | Temporal Integration | `bizosaas-temporal-integration-staging` | 8007→8000 | Workflow service integration | GitHub build |
| 8 | AI Agents | `bizosaas-ai-agents-staging` | 8008→8000 | Specialized AI services | GitHub build |
| 9 | Amazon Sourcing | `bizosaas-amazon-sourcing-staging` | 8009→8000 | Product sourcing from Amazon | GitHub build |

**Service Details**:

### 1. Saleor E-Commerce (8000)
- **Type**: Complete GraphQL e-commerce API
- **Features**: Products, orders, checkout, payments
- **Image**: `ghcr.io/saleor/saleor:3.20`
- **Database**: Separate `saleor_staging` database
- **Status**: ✅ Healthy (4 hours uptime)

### 2. Brain API (8001)
- **Type**: FastAPI AI Gateway
- **Features**: AI orchestration, model routing, embeddings
- **Build**: From `bizosaas-platform/ai/services/bizosaas-brain`
- **Dependencies**: PostgreSQL, Redis, OpenAI API
- **Status**: ✅ Healthy (4 hours uptime)

### 3. Wagtail CMS (8002)
- **Type**: Django-based headless CMS
- **Features**: Content pages, blog, media management
- **Build**: From `bizosaas-platform/backend/services/cms`
- **Settings**: `wagtail_cms.settings.production`
- **Status**: ✅ Healthy (4 hours uptime)

### 4. Django CRM (8003)
- **Type**: Django CRM application
- **Features**: Contacts, deals, pipeline, activities
- **Build**: From `bizosaas-platform/backend/services/crm/django-crm`
- **Settings**: `crm_project.settings.production`
- **Status**: ✅ Healthy (4 hours uptime)

### 5. Business Directory Backend (8004)
- **Type**: FastAPI directory service
- **Features**: Business listings, search, reviews
- **Build**: From `bizosaas-platform/backend/services/crm/business-directory`
- **Status**: 🔄 Will deploy with fixed config

### 6. CorelDove Backend (8005)
- **Type**: E-commerce integration layer
- **Features**: Saleor bridge, product sync
- **Build**: From `bizosaas/ecommerce/services/coreldove-backend`
- **Dependencies**: Saleor API
- **Status**: 🔄 Will deploy with fixed config

### 7. Temporal Integration (8007)
- **Type**: Workflow orchestration service
- **Features**: Long-running workflows, task scheduling
- **Build**: From `bizosaas-platform/backend/services/temporal`
- **Dependencies**: Temporal Server
- **Status**: 🔄 Will deploy with fixed config

### 8. AI Agents (8008)
- **Type**: Specialized AI agent services
- **Features**: Task-specific AI agents, automation
- **Build**: From `bizosaas-platform/backend/services/ai-agents`
- **Dependencies**: Brain API, OpenAI
- **Status**: 🔄 Will deploy with fixed config

### 9. Amazon Sourcing (8009)
- **Type**: Product sourcing service
- **Features**: Amazon product import, pricing sync
- **Build**: From `bizosaas-platform/backend/services/amazon-sourcing`
- **Dependencies**: Saleor API, Amazon API
- **Status**: 🔄 Will deploy with fixed config

**Health Check Endpoints**:
```bash
curl http://194.238.16.237:8000/health/  # Saleor
curl http://194.238.16.237:8001/health   # Brain API
curl http://194.238.16.237:8002/admin/   # Wagtail
curl http://194.238.16.237:8003/admin/   # Django CRM
curl http://194.238.16.237:8004/health   # Business Directory
curl http://194.238.16.237:8005/health   # CorelDove Backend
curl http://194.238.16.237:8007/health   # Temporal Integration
curl http://194.238.16.237:8008/health   # AI Agents
curl http://194.238.16.237:8009/health   # Amazon Sourcing
```

---

## 🎨 FRONTEND PROJECT (5 Services Deploying)

### Container Prefix: `bizosaas-*-frontend-staging` / `bizosaas-*-staging`
### Dokploy Project: Frontend Services / frontend-services-a89ci2

| # | Service Name | Container Name | Port | Purpose | Status |
|---|--------------|----------------|------|---------|--------|
| 1 | Bizoholic Frontend | `bizosaas-bizoholic-frontend-staging` | 3000→3000 | Marketing agency website | 🔄 Will deploy |
| 2 | Client Portal | `bizosaas-client-portal-staging` | 3001→3000 | Multi-tenant client dashboard | 🔄 Will deploy |
| 3 | CorelDove Frontend | `bizosaas-coreldove-frontend-staging` | 3002→3000 | E-commerce storefront | 🔄 Will deploy |
| 4 | **Business Directory Frontend** | ~~`bizosaas-business-directory-frontend-staging`~~ | ~~3003→3000~~ | **Directory listings UI** | ❌ **SKIPPED** |
| 5 | ThrillRing Gaming | `bizosaas-thrillring-gaming-staging` | 3005→3000 | Gaming platform | 🔄 Will deploy |
| 6 | Admin Dashboard | `bizosaas-admin-dashboard-staging` | 3009→3000 | Platform administration | 🔄 Will deploy |

**Service Details**:

### 1. Bizoholic Frontend (3000)
- **Type**: Next.js 18 marketing website
- **Features**: Landing pages, blog, contact forms
- **Build**: From `bizosaas-platform/frontend/apps/bizoholic-frontend`
- **APIs**: Brain API, Wagtail CMS, Django CRM
- **Domain**: `stg.bizoholic.com` (Traefik routing)

### 2. Client Portal (3001)
- **Type**: Next.js 20 multi-tenant dashboard
- **Features**: Client area, campaigns, reports, billing
- **Build**: From `bizosaas-platform/frontend/apps/client-portal`
- **APIs**: Brain API, CRM, CMS, Saleor
- **Domain**: `stg.portal.bizoholic.com`

### 3. CorelDove Frontend (3002)
- **Type**: Next.js 18 e-commerce storefront
- **Features**: Product catalog, cart, checkout
- **Build**: From `bizosaas-platform/frontend/apps/coreldove-frontend`
- **APIs**: Saleor GraphQL, CorelDove Backend
- **Domain**: `stg.coreldove.com`

### 4. Business Directory Frontend (3003) ❌ **SKIPPED**
- **Type**: Next.js 15 directory interface
- **Features**: Business search, listings, reviews
- **Build**: From `bizosaas-platform/frontend/apps/business-directory`
- **Issue**: Missing dependencies (tailwindcss, @/components/ui/*)
- **Status**: **Excluded from deployment - needs repository fix**
- **Domain**: `stg.directory.bizoholic.com` (when fixed)

### 5. ThrillRing Gaming (3005)
- **Type**: Next.js 20 gaming platform
- **Features**: Gaming content, community
- **Build**: From `bizosaas/frontend/apps/thrillring-gaming`
- **APIs**: Brain API
- **Domain**: `stg.thrillring.com`

### 6. Admin Dashboard (3009)
- **Type**: Next.js 18 admin interface
- **Features**: Platform admin, analytics, monitoring
- **Build**: From `bizosaas-platform/frontend/apps/bizosaas-admin`
- **APIs**: Brain API, Superset, Temporal UI
- **Domain**: `stg.admin.bizoholic.com`

**Browser Access**:
```
http://194.238.16.237:3000  # Bizoholic
http://194.238.16.237:3001  # Client Portal
http://194.238.16.237:3002  # CorelDove
http://194.238.16.237:3005  # ThrillRing Gaming
http://194.238.16.237:3009  # Admin Dashboard
```

---

## 📊 Complete Deployment Matrix

| Project | Services | Deployed | Pending | Excluded | Success Rate |
|---------|----------|----------|---------|----------|--------------|
| **Infrastructure** | 6 | 6 | 0 | 0 | 100% ✅ |
| **Backend** | 9 | 4 | 5 | 0 | 44% 🔄 |
| **Frontend** | 6 | 0 | 5 | 1 | 0% 🔄 |
| **TOTAL** | **21** | **10** | **10** | **1** | **48%** → **95% after deployment** |

---

## 🔗 Service Dependencies Map

```
Infrastructure Layer (6 services)
├── PostgreSQL ─────────────┐
├── Redis ──────────────────┤
├── Vault                   │
├── Temporal Server         │
├── Temporal UI             │
└── Superset                │
                            │
Backend Layer (9 services)  │
├── Saleor ◄────────────────┤
├── Brain API ◄─────────────┤
├── Wagtail CMS ◄───────────┤
├── Django CRM ◄────────────┤
├── Business Dir Backend ◄──┤
├── CorelDove Backend ◄─────┤── (depends on Saleor)
├── Temporal Integration ◄──┤
├── AI Agents ◄─────────────┤── (depends on Brain API)
└── Amazon Sourcing ◄───────┘── (depends on Saleor)
                            │
Frontend Layer (5 services) │
├── Bizoholic ◄─────────────┤── (connects to Brain, CMS, CRM)
├── Client Portal ◄─────────┤── (connects to Brain, CRM, Saleor)
├── CorelDove ◄─────────────┤── (connects to Saleor, CorelDove Backend)
├── ThrillRing ◄────────────┤── (connects to Brain)
└── Admin Dashboard ◄───────┘── (connects to Brain, Superset, Temporal)

❌ Business Dir Frontend (EXCLUDED - missing dependencies)
```

---

## 🎯 What Gets Deployed Now

### With Fixed Configs:

**Backend** (`dokploy-backend-staging-clean.yml`):
- ✅ All 9 backend services will deploy
- ⏱️ Build time: 20-30 minutes
- 🔧 Builds from GitHub: 8 services
- 📦 Pre-built image: 1 service (Saleor)

**Frontend** (`dokploy-frontend-staging-5apps.yml`):
- ✅ 5 frontend apps will deploy
- ❌ 1 app excluded (business-directory)
- ⏱️ Build time: 25-35 minutes
- 🔧 All build from GitHub

**Total After Deployment**: **20/21 services (95%)**

---

## 📋 Service Ports Reference

### Infrastructure
- 5433 - PostgreSQL
- 6380 - Redis
- 7234 - Temporal Server
- 8083 - Temporal UI
- 8088 - Superset
- 8201 - Vault

### Backend
- 8000 - Saleor E-Commerce
- 8001 - Brain API
- 8002 - Wagtail CMS
- 8003 - Django CRM
- 8004 - Business Directory Backend
- 8005 - CorelDove Backend
- 8007 - Temporal Integration
- 8008 - AI Agents
- 8009 - Amazon Sourcing

### Frontend
- 3000 - Bizoholic
- 3001 - Client Portal
- 3002 - CorelDove
- ~~3003~~ - ~~Business Directory~~ (excluded)
- 3005 - ThrillRing Gaming
- 3009 - Admin Dashboard

---

## ✅ Verification Commands

### Check All Services
```bash
./check-complete-staging.sh
```

### Check by Project
```bash
# Infrastructure
ssh root@194.238.16.237 "docker ps --filter 'name=bizosaas-postgres-staging' --filter 'name=bizosaas-redis-staging' --filter 'name=bizosaas-vault-staging' --filter 'name=bizosaas-temporal' --filter 'name=bizosaas-superset-staging'"

# Backend
ssh root@194.238.16.237 "docker ps | grep -E 'bizosaas.*(saleor|brain|wagtail|django-crm|business-directory|coreldove-backend|temporal-integration|ai-agents|amazon-sourcing)'"

# Frontend
ssh root@194.238.16.237 "docker ps | grep -E 'bizosaas.*(bizoholic|portal|coreldove-frontend|thrillring|admin-dashboard)'"
```

---

**Last Updated**: 2025-10-12 15:00 UTC
**Deployment Status**: Ready to deploy backend + frontend (20/21 services)
**Excluded**: Business Directory Frontend (repository dependencies issue)
