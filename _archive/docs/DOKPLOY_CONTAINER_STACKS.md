# Dokploy Container Stack Organization for VPS Deployment

## Overview
This document outlines the container organization for deploying the BizOSaaS platform across three live websites using Dokploy on VPS.

## Live Websites
- **Bizoholic.com** - AI Marketing Agency SaaS Platform
- **CorelDove.com** - E-commerce & Product Sourcing Platform
- **ThrillRing.com** - Gaming & E-sports Tournament Platform

---

## **PROJECT 1: BIZOHOLIC.COM**

### Frontend Applications
| Container Name | Port | Image | Purpose |
|----------------|------|-------|---------|
| `bizoholic-frontend-3000-final` | 3000 | `bizoholic-frontend:dev` | Main marketing website & landing pages |
| `client-portal-3001` | 3001 | `node:20-alpine` | Client dashboard, campaigns, analytics |

### Backend Services
| Container Name | Port | Image | Purpose |
|----------------|------|-------|---------|
| `bizosaas-brain-unified` | 8001 | `bizosaas-brain-gateway:latest` | AI Brain Gateway & Smart LLM Router |
| `bizosaas-wagtail-cms-8002` | 8002 | `bizosaas-wagtail-cms:latest` | Headless CMS for content management |
| `bizosaas-django-crm-8003` | 8003 | `django-crm-django-crm` | Customer relationship management |

### Environment Variables (Bizoholic)
```env
NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-unified:8001
NEXT_PUBLIC_CMS_URL=http://bizosaas-wagtail-cms-8002:4000
POSTGRES_DB=bizoholic_db
REDIS_URL=redis://bizosaas-redis-unified:6379
```

---

## **PROJECT 2: CORELDOVE.COM**

### Frontend Applications
| Container Name | Port | Image | Purpose |
|----------------|------|-------|---------|
| `coreldove-frontend-3002` | 3002 | `node:20-alpine` | E-commerce frontend & product catalog |

### Backend Services
| Container Name | Port | Image | Purpose |
|----------------|------|-------|---------|
| `bizosaas-saleor-unified` | 8000 | `ghcr.io/saleor/saleor:3.20` | E-commerce backend & GraphQL API |
| `amazon-sourcing-8085` | 8085 | `bizosaas/amazon-sourcing:latest` | Amazon SP-API integration & product sourcing |
| `bizosaas-business-directory-backend-8004` | 8004 | `bizosaas-business-directory-backend:latest` | Business directory & supplier management |

### Environment Variables (CorelDove)
```env
NEXT_PUBLIC_API_BASE_URL=http://amazon-sourcing-8085:8080
NEXT_PUBLIC_SALEOR_API=http://bizosaas-saleor-unified:8000/graphql/
NEXT_PUBLIC_DIRECTORY_API=http://bizosaas-business-directory-backend-8004:8004
AMAZON_SP_API_CLIENT_ID=${AMAZON_SP_API_CLIENT_ID}
AMAZON_SP_API_CLIENT_SECRET=${AMAZON_SP_API_CLIENT_SECRET}
SALEOR_SECRET_KEY=${SALEOR_SECRET_KEY}
```

---

## **PROJECT 3: THRILLRING.COM**

### Frontend Applications
| Container Name | Port | Image | Purpose |
|----------------|------|-------|---------|
| `thrillring-gaming-3005` | 3005 | `node:20-alpine` | Gaming portal & tournament platform |

### Gaming Services
| Container Name | Port | Image | Purpose |
|----------------|------|-------|---------|
| `bizosaas-admin-3009` | 3009 | `node:20-alpine` | Gaming admin dashboard & tournament management |
| `business-directory-3004` | 3004 | `node:20-alpine` | Gaming community & player directory |

### Environment Variables (ThrillRing)
```env
NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-unified:8001
NEXT_PUBLIC_GAMING_API=http://bizosaas-admin-3009:3009
POSTGRES_DB=thrillring_gaming_db
```

---

## **SHARED INFRASTRUCTURE PROJECT**

### Database & Cache
| Container Name | Port | Image | Purpose |
|----------------|------|-------|---------|
| `bizosaas-postgres-unified` | 5432 | `postgres:15-alpine` | PostgreSQL with pgvector for AI |
| `bizosaas-redis-unified` | 6379 | `redis:7-alpine` | Cache & session storage |

### Workflow & Analytics
| Container Name | Port | Image | Purpose |
|----------------|------|-------|---------|
| `bizosaas-temporal-unified` | 8009 | `bizosaas-platform-temporal-integration:latest` | Workflow orchestration |
| `bizosaas-temporal-ui-server` | 8082 | `temporalio/ui:2.21.0` | Temporal workflow UI |
| `bizosaas-temporal-server` | 7233 | `temporalio/auto-setup:1.22.0` | Temporal server core |
| `bizosaas-superset-8088` | 8088 | `bizosaas-platform-apache-superset:latest` | Analytics & BI dashboard |

### Security & Management
| Container Name | Port | Image | Purpose |
|----------------|------|-------|---------|
| `bizosaas-vault` | 8200 | `hashicorp/vault:1.15` | Secrets management |
| `bizosaas-sqladmin-comprehensive-fixed` | 8005 | `bizosaas-sqladmin-superadmin:latest` | Database administration |

---

## **Dokploy Deployment Strategy**

### Project Structure in Dokploy
```
VPS Dokploy Instance
├── bizoholic-com/          # Project for bizoholic.com
│   ├── frontend-stack/     # Frontend containers (3000, 3001)
│   └── backend-stack/      # Backend services (8001, 8002, 8003)
├── coreldove-com/          # Project for coreldove.com
│   ├── frontend-stack/     # Frontend containers (3002)
│   └── backend-stack/      # Backend services (8000, 8085, 8004)
├── thrillring-com/         # Project for thrillring.com
│   ├── frontend-stack/     # Frontend containers (3005)
│   └── gaming-stack/       # Gaming services (3009, 3004)
└── shared-infrastructure/  # Shared services
    ├── database-stack/     # PostgreSQL, Redis (5432, 6379)
    ├── workflow-stack/     # Temporal services (8009, 8082, 7233)
    ├── analytics-stack/    # Superset (8088)
    └── security-stack/     # Vault, SQL Admin (8200, 8005)
```

### Network Configuration
- **Internal Network**: `bizosaas-platform-network`
- **External Access**: Through Dokploy reverse proxy
- **SSL**: Managed by Dokploy with Let's Encrypt
- **Domains**:
  - bizoholic.com → Port 3000
  - coreldove.com → Port 3002
  - thrillring.com → Port 3005

### Resource Requirements
| Service Type | CPU | Memory | Storage |
|-------------|-----|--------|---------|
| Frontend Apps | 0.5 CPU | 512MB | 2GB |
| Backend APIs | 1 CPU | 1GB | 5GB |
| Database | 2 CPU | 4GB | 50GB |
| AI Services | 2 CPU | 2GB | 10GB |

---

## **Deployment Commands**

### Start All Containers
```bash
# Core Infrastructure
docker start bizosaas-postgres-unified bizosaas-redis-unified

# Bizoholic.com Stack
docker start bizoholic-frontend-3000-final client-portal-3001
docker start bizosaas-brain-unified bizosaas-wagtail-cms-8002 bizosaas-django-crm-8003

# CorelDove.com Stack
docker start coreldove-frontend-3002
docker start bizosaas-saleor-unified amazon-sourcing-8085 bizosaas-business-directory-backend-8004

# ThrillRing.com Stack
docker start thrillring-gaming-3005
docker start bizosaas-admin-3009 business-directory-3004

# Analytics & Management
docker start bizosaas-superset-8088 bizosaas-vault bizosaas-sqladmin-comprehensive-fixed
docker start bizosaas-temporal-unified bizosaas-temporal-ui-server bizosaas-temporal-server
```

### Health Check
```bash
# Test all frontends
curl -f http://localhost:3000 && echo "✅ Bizoholic"
curl -f http://localhost:3002 && echo "✅ CorelDove"
curl -f http://localhost:3005 && echo "✅ ThrillRing"

# Test key backends
curl -f http://localhost:8001/health && echo "✅ AI Brain"
curl -f http://localhost:8000/health/ && echo "✅ Saleor E-commerce"
curl -f http://localhost:8085/health && echo "✅ Amazon Sourcing"
```

---

## **Container Status Summary**

### ✅ Running Containers (15/15)
- **Frontends**: 3000 (Bizoholic), 3001 (Portal), 3002 (CorelDove), 3005 (ThrillRing), 3009 (Admin), 3004 (Directory)
- **Backends**: 8000 (Saleor), 8001 (Brain), 8002 (CMS), 8003 (CRM), 8004 (Directory), 8085 (Sourcing)
- **Infrastructure**: 5432 (Postgres), 6379 (Redis), 8005 (SQL Admin), 8088 (Superset), 8200 (Vault)
- **Workflows**: 7233 (Temporal), 8009 (Temporal Integration), 8082 (Temporal UI)

### Ready for Production Deployment
All containers are healthy and properly configured for Dokploy deployment to VPS hosting the live websites.

---

*Last Updated: $(date)*
*Environment: Local Development → VPS Production*