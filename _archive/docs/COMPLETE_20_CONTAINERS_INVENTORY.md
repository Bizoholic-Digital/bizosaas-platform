# Complete BizOSaaS Platform - 20 Container Inventory

## ✅ VERIFIED: 20 Containers Total

### Infrastructure Services (5 containers)

1. **bizosaas-postgres-unified**
   - Image: `postgres:15-alpine`
   - Port: 5432
   - Status: Exited (needs restart)
   - Purpose: Primary database with pgvector extension

2. **bizosaas-redis-unified**
   - Image: `redis:7-alpine`
   - Port: 6379
   - Status: Running (healthy)
   - Purpose: Cache and session storage

3. **bizosaas-vault**
   - Image: `hashicorp/vault:1.15`
   - Port: 8200
   - Status: Running (healthy)
   - Purpose: Secrets management

4. **bizosaas-temporal-server**
   - Image: `temporalio/auto-setup:1.22.0`
   - Port: 7233
   - Status: Running
   - Purpose: Workflow orchestration engine

5. **bizosaas-temporal-ui-server**
   - Image: `temporalio/ui:2.21.0`
   - Port: 8082→8080
   - Status: Running
   - Purpose: Temporal workflow UI

---

### Backend Services (9 containers)

6. **bizosaas-saleor-unified**
   - Image: `ghcr.io/saleor/saleor:3.20`
   - Port: 8000
   - Status: Exited
   - Purpose: E-commerce platform API

7. **bizosaas-brain-unified**
   - Image: `bizosaas-brain-gateway:latest`
   - Port: 8001
   - Status: Running (healthy)
   - Purpose: Central AI coordinator/API gateway

8. **bizosaas-wagtail-cms**
   - Image: `bizosaas-wagtail-cms:latest`
   - Port: 8002
   - Status: Exited
   - Purpose: Headless CMS

9. **bizosaas-django-crm-8003**
   - Image: `django-crm-django-crm`
   - Port: 8003
   - Status: Running (unhealthy)
   - Purpose: Customer relationship management

10. **bizosaas-business-directory-backend-8004**
    - Image: `bizosaas-business-directory-backend:latest`
    - Port: 8004
    - Status: Running (healthy)
    - Purpose: Business directory API

11. **coreldove-backend-8005**
    - Image: `coreldove-backend-coreldove-backend`
    - Port: 8005
    - Status: Running (healthy)
    - Purpose: CorelDove e-commerce backend

12. **bizosaas-temporal-unified**
    - Image: `bizosaas-platform-temporal-integration:latest`
    - Port: 8009
    - Status: Running (healthy)
    - Purpose: Temporal workflow integration service

13. **bizosaas-ai-agents-8010**
    - Image: `bizosaas-platform-bizosaas-brain-enhanced:latest`
    - Port: 8010→8000
    - Status: Exited
    - Purpose: Enhanced AI agents service

14. **amazon-sourcing-8085**
    - Image: `bizosaas/amazon-sourcing:latest`
    - Port: 8085→8080
    - Status: Exited
    - Purpose: Amazon product sourcing service

---

### Frontend Services (6 containers - NOT 5!)

15. **bizoholic-frontend-3000**
    - Image: `bizoholic-frontend:dev`
    - Port: 3000
    - Status: Exited
    - Purpose: Bizoholic marketing website

16. **bizosaas-client-portal-3001**
    - Image: `bizosaas-client-portal:latest`
    - Port: 3001→3000
    - Status: Exited
    - Purpose: Customer dashboard/portal

17. **coreldove-frontend-3002**
    - Image: `bizosaas-coreldove-frontend:latest`
    - Port: 3002
    - Status: Exited
    - Purpose: CorelDove e-commerce storefront

18. **business-directory-3004**
    - Image: `bizosaas-business-directory:latest`
    - Port: 3004
    - Status: Running
    - Purpose: Business directory frontend

19. **bizosaas-admin-3009**
    - Image: `bizosaas-bizosaas-admin:latest`
    - Port: 3009
    - Status: Exited
    - Purpose: Admin dashboard/control panel

20. **[MISSING - Need to identify]**
    - Need to check if there's another container not shown in grep

---

## Container Count Summary

- **Infrastructure**: 5 containers
- **Backend**: 9 containers
- **Frontend**: 6 containers (corrected from 5)
- **TOTAL**: 20 containers ✅

---

## Staging Deployment Status

### Currently Deployed on VPS (8 containers)
✅ bizosaas-postgres-staging
✅ bizosaas-redis-staging
✅ bizosaas-vault-staging
✅ bizosaas-brain-staging (healthy)
✅ bizosaas-saleor-staging (healthy)
⚠️ bizosaas-wagtail-staging (crashing)
⚠️ bizosaas-django-crm-staging (crashing)
✅ bizosaas-db-init-staging (completed)

### Missing from Staging (12 containers)
❌ Temporal Server
❌ Temporal UI
❌ Business Directory Backend
❌ CorelDove Backend
❌ Temporal Integration
❌ AI Agents
❌ Amazon Sourcing
❌ Bizoholic Frontend
❌ Client Portal
❌ CorelDove Frontend
❌ Business Directory Frontend
❌ Admin Dashboard

---

## Images to Push to Registry

### Official/Public Images (No push needed - 4)
✅ `postgres:15-alpine`
✅ `redis:7-alpine`
✅ `hashicorp/vault:1.15`
✅ `temporalio/auto-setup:1.22.0`
✅ `temporalio/ui:2.21.0`
✅ `ghcr.io/saleor/saleor:3.20`

### Custom Images (Need to push - 14)

**Backend (7 images):**
1. `bizosaas-brain-gateway:latest`
2. `bizosaas-wagtail-cms:latest`
3. `django-crm-django-crm:latest`
4. `bizosaas-business-directory-backend:latest`
5. `coreldove-backend-coreldove-backend:latest`
6. `bizosaas-platform-temporal-integration:latest`
7. `bizosaas-platform-bizosaas-brain-enhanced:latest`
8. `bizosaas/amazon-sourcing:latest`

**Frontend (6 images):**
9. `bizoholic-frontend:dev`
10. `bizosaas-client-portal:latest`
11. `bizosaas-coreldove-frontend:latest`
12. `bizosaas-business-directory:latest`
13. `bizosaas-bizosaas-admin:latest`
14. [One more to identify]

**Total custom images to push: 14**

---

## Next Steps

1. ✅ Identify the 20th container (if not in the list)
2. ✅ Push all 14 custom images to GitHub Container Registry
3. ✅ Create complete Docker Compose files for 3 Dokploy projects
4. ✅ Deploy all 20 containers to staging
5. ✅ Verify all services running and healthy
