# Local Containers → VPS Staging Projects Mapping

## VPS Project Structure (Dokploy)
1. **bizosaas_infrastructure_staging** (6 services)
2. **bizosaas_backend_staging** (8 services)
3. **bizosaas_frontend_staging** (6 services)

---

## Infrastructure Project (6 services) - Already Deployed ✅

These use standard images, no custom builds needed:

| Service | Local Image | VPS Container | Status |
|---------|-------------|---------------|--------|
| PostgreSQL | `postgres:15-alpine` | `bizosaas-postgres-staging` | ✅ Running |
| Redis | `redis:7-alpine` | `bizosaas-redis-staging` | ✅ Running |
| Vault | `hashicorp/vault:1.15` | `bizosaas-vault-staging` | ✅ Running |
| Temporal Server | `temporalio/auto-setup:1.22.0` | `bizosaas-temporal-server-staging` | ✅ Running |
| Temporal UI | `temporalio/ui:2.21.0` | `bizosaas-temporal-ui-staging` | ✅ Running |
| Superset | `bizosaas-platform-apache-superset:latest` | `bizosaas-superset-staging` | ✅ Running |

**Action**: No push needed - infrastructure already working

---

## Backend Project (8 services) - NEEDS IMAGES

| # | Service | Local Image | GHCR Target | Port |
|---|---------|-------------|-------------|------|
| 1 | Brain API | `bizosaas-brain-gateway:latest` | `ghcr.io/bizoholic-digital/bizosaas-platform/brain-api:staging` | 8001 |
| 2 | Wagtail CMS | `bizosaas-wagtail-cms:latest` | `ghcr.io/bizoholic-digital/bizosaas-platform/wagtail-cms:staging` | 8002 |
| 3 | Django CRM | `bizoholic-django-crm:latest` | `ghcr.io/bizoholic-digital/bizosaas-platform/django-crm:staging` | 8003 |
| 4 | Business Directory | `bizosaas-business-directory-backend:latest` | `ghcr.io/bizoholic-digital/bizosaas-platform/business-directory-backend:staging` | 8004 |
| 5 | CorelDove Backend | `bizoholic-coreldove-backend:latest` | `ghcr.io/bizoholic-digital/bizosaas-platform/coreldove-backend:staging` | 8005 |
| 6 | Auth Service | `bizoholic-auth-service:latest` | `ghcr.io/bizoholic-digital/bizosaas-platform/auth-service:staging` | 8006 |
| 7 | AI Agents | `bizoholic-ai-agents:latest` | `ghcr.io/bizoholic-digital/bizosaas-platform/ai-agents:staging` | 8008 |
| 8 | Amazon Sourcing | `bizosaas/amazon-sourcing:latest` | `ghcr.io/bizoholic-digital/bizosaas-platform/amazon-sourcing:staging` | 8009 |

**Action**: Push these 8 images to GHCR

---

## Frontend Project (6 services) - NEEDS IMAGES

| # | Service | Local Image | GHCR Target | Port |
|---|---------|-------------|-------------|------|
| 1 | Client Portal | `bizosaas-client-portal:latest` | `ghcr.io/bizoholic-digital/bizosaas-platform/client-portal:staging` | 3000 |
| 2 | Bizoholic Frontend | `bizosaas-bizoholic-frontend:latest` | `ghcr.io/bizoholic-digital/bizosaas-platform/bizoholic-frontend:staging` | 3001 |
| 3 | CorelDove Frontend | `bizosaas-coreldove-frontend:latest` | `ghcr.io/bizoholic-digital/bizosaas-platform/coreldove-frontend:staging` | 3002 |
| 4 | Business Directory | `bizosaas-business-directory:latest` | `ghcr.io/bizoholic-digital/bizosaas-platform/business-directory-frontend:staging` | 3003 |
| 5 | ThrillRing Gaming | ⚠️ `node:20-alpine` (not built) | N/A - needs building | 3004 |
| 6 | Admin Dashboard | `bizosaas-bizosaas-admin:latest` | `ghcr.io/bizoholic-digital/bizosaas-platform/admin-dashboard:staging` | 3005 |

**Action**: Push 5 images (ThrillRing needs to be built first)

---

## Summary

**Total Services**: 20
- Infrastructure: 6 ✅ (already deployed)
- Backend: 8 🔄 (need to push)
- Frontend: 5 🔄 (need to push, +1 needs building)

**Images to Push**: 13 (8 backend + 5 frontend)
**Images Already in GHCR**: 1 (brain-api has old version)
**Images Needing Build**: 1 (ThrillRing Gaming)
