# Complete Frontend Migration Roadmap

**Date:** November 2, 2025
**Status:** 🚀 In Progress
**Architecture:** Modular DDD Containerized Microservices

---

## 🎯 MIGRATION OBJECTIVE

Transform **ALL frontend applications** from monorepo workspace architecture to **fully self-contained modular microservices** following Domain-Driven Design (DDD) principles.

---

## 📊 FRONTEND SERVICES INVENTORY

### ✅ COMPLETED (6/6 Customer-Facing Services)

#### 1. Bizoholic Frontend ✅
- **Status:** ✅ **DEPLOYED AND RUNNING**
- **URL:** `https://stg.bizoholic.com/` (root domain)
- **Port:** 3001
- **Service:** `frontend-bizoholic-frontend`
- **Purpose:** Main marketing/landing page
- **Architecture:** Deployed (production-ready)
- **Response:** HTTP 200 OK
- **Deployment Status:** Running 1/1 replicas
- **Verified:** November 4, 2025

#### 2. Client Portal ✅
- **Status:** ✅ **DEPLOYED AND RUNNING**
- **URL:** `https://stg.bizoholic.com/portal`
- **Port:** 3002 (host) → 3001 (container)
- **Service:** `frontend-client-portal`
- **Purpose:** Multi-tenant client dashboard
- **Architecture:** Deployed (production-ready)
- **Response:** HTTP 307 (redirect - working)
- **Deployment Status:** Running 1/1 replicas
- **Verified:** November 4, 2025

#### 3. Business Directory ✅
- **Status:** ✅ **DEPLOYED AND RUNNING**
- **URL:** `https://stg.bizoholic.com/directory`
- **Port:** 3004
- **Service:** `frontend-business-directory`
- **Architecture:** Modular DDD (lib/ structure)
- **Image:** `ghcr.io/bizoholic-digital/bizosaas-business-directory:latest`
- **Build Context:** 715.8KB (99% reduction from 702MB)
- **Response:** HTTP 200 OK
- **Deployment Status:** Running 1/1 replicas
- **Verified:** November 4, 2025
- **Documentation:** [BUSINESS_DIRECTORY_MODULAR_MIGRATION_COMPLETE.md](BUSINESS_DIRECTORY_MODULAR_MIGRATION_COMPLETE.md)

#### 4. CoreLdove Storefront ✅
- **Status:** ✅ **DEPLOYED AND RUNNING**
- **URL:** `https://stg.coreldove.com` (standalone domain)
- **Port:** 3005 (host) → 3002 (container)
- **Service:** `frontend-coreldove-frontend`
- **Backend:** Saleor API (port 8000) - ✅ Running on KVM4
- **Technology:**
  - Next.js 15 + App Router
  - React 19 + Server Components
  - GraphQL + TypeScript Codegen
  - Stripe payment integration
  - Saleor Storefront template (v3.20)
- **Architecture:** ✅ **MODULAR DDD** - Saleor's `src/lib/` structure
- **Image:** `ghcr.io/bizoholic-digital/coreldove-storefront:v1.0.3`
- **Build Size:** 202MB (optimized standalone)
- **Deployment Date:** November 3, 2025
- **Deployment Status:** Running 1/1 replicas
- **Verified:** November 4, 2025
- **Documentation:** [CORELDOVE_DEPLOYMENT_GUIDE.md](CORELDOVE_DEPLOYMENT_GUIDE.md)

#### 5. ThrillRing Gaming ✅
- **Status:** ✅ **DEPLOYED AND RUNNING**
- **URL:** `https://stg.thrillring.com` (standalone domain)
- **Port:** 3006
- **Service:** `frontend-thrillring-gaming`
- **Purpose:** E-sports tournament platform
- **Technology:**
  - Next.js 15.5.3 + App Router
  - Framer Motion animations
  - Real-time tournament data
  - Recharts analytics
- **Architecture:** ✅ **MODULAR DDD** - `lib/` structure with PostCSS
- **Image:** `ghcr.io/bizoholic-digital/bizosaas-thrillring-gaming:v1.0.7`
- **Build Size:** 20.5KB CSS (properly generated with Tailwind)
- **Deployment Date:** November 3, 2025
- **Response:** HTTP 200 OK
- **Deployment Status:** Running 1/1 replicas
- **Verified:** November 4, 2025
- **Key Fix:** Added postcss.config.js for Tailwind CSS generation
- **Design:** Solid colors only (bg-purple-600, bg-gray-900) - no gradients

#### 6. Saleor Dashboard (Official Admin) ✅
- **Status:** ✅ **DEPLOYED AND RUNNING**
- **URL:** `https://stg.coreldove.com/dashboard/`
- **Port:** 9000 (host) → 80 (container)
- **Service:** `frontendservices-saleordashboard-84ku62`
- **Purpose:** Saleor e-commerce administration
- **Technology:**
  - Official Saleor Dashboard image (v3.20)
  - React SPA + GraphQL client
  - Nginx static file serving
  - JWT authentication via Saleor Core
- **Architecture:** ✅ **OFFICIAL IMAGE** - Pre-built containerized admin
- **Image:** `ghcr.io/saleor/saleor-dashboard:latest`
- **API Connection:** `https://api.coreldove.com/graphql/` (Saleor Core)
- **Deployment Date:** November 3, 2025
- **Deployment Status:** Running 1/1 replicas
- **Verified:** November 4, 2025
- **Admin Credentials:** admin@coreldove.com / Admin2025 (✅ Login Fixed Nov 4)
- **Login Fix:** Added ALLOWED_HOSTS and SECRET_KEY environment variables
- **CrewAI Integration:** Webhook-based (planned, documentation complete)
- **Documentation:**
  - [SALEOR_DASHBOARD_LOGIN_FIXED.md](SALEOR_DASHBOARD_LOGIN_FIXED.md)
  - [SALEOR_DASHBOARD_CONFIGURATION_VERIFICATION.md](SALEOR_DASHBOARD_CONFIGURATION_VERIFICATION.md)
  - [SALEOR_WEBHOOK_CREWAI_INTEGRATION_PLAN.md](SALEOR_WEBHOOK_CREWAI_INTEGRATION_PLAN.md)

---

### 🔄 IN PROGRESS (0/3)

---

### ⏳ PENDING MIGRATION (3/9)

#### 7. Analytics Dashboard
- **Current Status:** No lib/, No Dockerfile
- **Purpose:** Business intelligence and metrics
- **Port:** Unknown (suggest 3007)
- **URL:** Not deployed
- **Priority:** MEDIUM
- **Dependencies:** Unknown
- **Migration Effort:** MEDIUM
- **Estimated Time:** 2-3 days

#### 8. BizOSaaS Admin
- **Current Status:** No lib/, No Dockerfile
- **Purpose:** Platform administration
- **Port:** Unknown (suggest 3007)
- **URL:** Not deployed
- **Priority:** LOW (internal tool)
- **Dependencies:** Unknown
- **Migration Effort:** MEDIUM
- **Estimated Time:** 2-3 days

#### 9. CoreLdove Setup Wizard
- **Current Status:** No lib/, No Dockerfile
- **Purpose:** Merchant onboarding & store setup wizard
- **Port:** 3003 (changed from 3002 to avoid conflict)
- **URL:** `stg.coreldove.com/setup` (planned)
- **Priority:** MEDIUM (merchant onboarding)
- **Features:** Multi-step wizard, Brain API integration
- **Migration Effort:** LOW
- **Estimated Time:** 1-2 days

---

## 🏗️ MIGRATION PATTERN (Proven with Business Directory)

### Standard Migration Process

#### Phase 1: Analysis (30 min)
```bash
# Check for workspace dependencies
grep -r "@bizoholic-digital/" app/ components/ lib/ 2>/dev/null

# List all component files
find . -name "*.tsx" -o -name "*.ts" | grep -v node_modules
```

#### Phase 2: Create lib/ Structure (1 hour)
```bash
mkdir -p lib/{ui,hooks,utils,api,types}

# Copy from workspace packages (if any)
cp -r ../../packages/ui-components/src/* lib/ui/
cp -r ../../packages/hooks/src/* lib/hooks/
```

#### Phase 3: Update Imports (1-2 hours)
```typescript
// Before
import { Button } from '@bizoholic-digital/ui-components'

// After
import { Button } from '@/lib/ui'
```

#### Phase 4: Dependency Management (30 min)
```json
{
  "dependencies": {
    // Add all required packages directly
    "@radix-ui/react-*": "^1.x",
    "class-variance-authority": "^0.7.0",
    "tailwindcss-animate": "^1.0.7"
  }
}
```

#### Phase 5: Create Modular Dockerfile (30 min)
```dockerfile
FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --legacy-peer-deps

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=<service-port>
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
RUN mkdir .next && chown nextjs:nodejs .next
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE <service-port>
CMD ["node", "server.js"]
```

#### Phase 6: Build & Deploy (1-2 hours)
```bash
# Build from service directory
cd bizosaas/frontend/apps/<service-name>
docker build -f Dockerfile.production \
  -t ghcr.io/bizoholic-digital/bizosaas-<service>:v1.0.0 \
  -t ghcr.io/bizoholic-digital/bizosaas-<service>:latest \
  .

# Push to GHCR
docker push ghcr.io/bizoholic-digital/bizosaas-<service>:v1.0.0
docker push ghcr.io/bizoholic-digital/bizosaas-<service>:latest

# Deploy via Dokploy UI
```

---

## 📅 RECOMMENDED MIGRATION SEQUENCE

### Week 1: Core Services

**Day 1-2: CoreLdove Storefront** 🔄
- Clone Saleor template
- Configure Saleor API
- Apply CoreLdove branding
- Deploy to staging

**Day 3-4: Bizoholic Frontend**
- Create lib/ structure
- Build modular Dockerfile
- Deploy main landing page
- **Impact:** HIGH (main entry point)

### Week 2: Customer-Facing Services

**Day 5-6: Client Portal**
- Analyze current deployment
- Create lib/ structure
- Migrate to modular DDD
- Redeploy with proper architecture

**Day 7-9: ThrillRing Gaming**
- Create lib/ structure
- Handle Socket.io setup
- Build and deploy
- **Impact:** MEDIUM (niche audience)

### Week 3: Admin Tools

**Day 10-11: Analytics Dashboard**
- Create lib/ structure
- Set up chart libraries
- Deploy to admin subdomain

**Day 12-13: BizOSaaS Admin**
- Create lib/ structure
- Deploy to admin subdomain

**Day 14: CoreLdove Admin Wizard**
- Change port to 3003
- Create lib/ structure
- Deploy alongside storefront

---

## 🎯 SUCCESS METRICS

### Architecture Goals
- ✅ **Zero workspace dependencies** - All services self-contained
- ✅ **Consistent pattern** - Same lib/ structure across all frontends
- ✅ **Independent deployment** - Each service builds from its directory
- ✅ **Minimal build context** - <1MB per service
- ✅ **Type safety** - TypeScript strict mode
- ✅ **Production-ready** - Docker → GHCR → Dokploy flow

### Deployment Goals
- ✅ **All services running** on staging
- ✅ **Traefik routing** configured for each service
- ✅ **Health checks** passing
- ✅ **Environment variables** properly set
- ✅ **SSL certificates** in place

---

## 📊 RESOURCE ALLOCATION

### Port Assignments
```
3000 - Bizoholic Frontend (landing page) ✅
3001 - Client Portal (customer dashboard) ✅
3002 - CoreLdove Storefront (e-commerce) ✅
3003 - CoreLdove Admin (setup wizard)
3004 - Business Directory (search & discovery) ✅
3006 - ThrillRing Gaming (tournaments) ✅
3007 - Analytics Dashboard (metrics)
3008 - BizOSaaS Admin (platform admin)
```

### URL Routing (Traefik)
```
stg.bizoholic.com/                    → Bizoholic Frontend ✅
stg.bizoholic.com/portal              → Client Portal ✅
stg.coreldove.com/                    → CoreLdove Storefront ✅
stg.bizoholic.com/admin/coreldove     → CoreLdove Admin
stg.bizoholic.com/directory           → Business Directory ✅
stg.thrillring.com/                   → ThrillRing Gaming ✅
stg.bizoholic.com/analytics           → Analytics Dashboard
stg.bizoholic.com/admin               → BizOSaaS Admin
```

### GHCR Image Registry
```
ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:latest ✅
ghcr.io/bizoholic-digital/bizosaas-client-portal:latest ✅
ghcr.io/bizoholic-digital/coreldove-storefront:latest ✅
ghcr.io/bizoholic-digital/coreldove-admin:latest
ghcr.io/bizoholic-digital/bizosaas-business-directory:latest ✅
ghcr.io/bizoholic-digital/bizosaas-thrillring-gaming:v1.0.7 ✅
ghcr.io/bizoholic-digital/bizosaas-analytics-dashboard:latest
ghcr.io/bizoholic-digital/bizosaas-admin:latest
```

---

## 🔧 SHARED INFRASTRUCTURE

All frontends connect to:

### Backend APIs
```
bizosaas-saleor-api-8003:8000         - Saleor GraphQL API
bizosaas-coreldove-backend-8003:8003  - CoreLdove Django backend
bizosaas-api-gateway:8080             - Main API gateway
```

### Databases
```
shared_postgres:5432                  - PostgreSQL (all services)
shared_redis:6379                     - Redis cache
```

### Support Services
```
shared_n8n:5678                       - Workflow automation
shared_minio:9000                     - Object storage
traefik:80/443                        - Reverse proxy
```

---

## 📝 DOCUMENTATION STATUS

### ✅ Completed
- [BUSINESS_DIRECTORY_MODULAR_MIGRATION_COMPLETE.md](BUSINESS_DIRECTORY_MODULAR_MIGRATION_COMPLETE.md)
- [CORELDOVE_SALEOR_STOREFRONT_MIGRATION_PLAN.md](CORELDOVE_SALEOR_STOREFRONT_MIGRATION_PLAN.md)
- [COMPLETE_FRONTEND_MIGRATION_ROADMAP.md](COMPLETE_FRONTEND_MIGRATION_ROADMAP.md) ← You are here

### 🔄 In Progress
- CoreLdove Storefront implementation

### ⏳ Pending
- Bizoholic Frontend migration guide
- Client Portal migration guide
- ThrillRing Gaming migration guide
- Analytics Dashboard migration guide
- BizOSaaS Admin migration guide
- CoreLdove Admin migration guide

---

## 🚀 NEXT IMMEDIATE ACTIONS

1. **Start CoreLdove Storefront** (Priority 1)
   ```bash
   cd bizosaas/frontend/apps/
   git clone https://github.com/saleor/storefront.git coreldove-storefront
   cd coreldove-storefront
   # Follow CORELDOVE_SALEOR_STOREFRONT_MIGRATION_PLAN.md
   ```

2. **Migrate Bizoholic Frontend** (Priority 2)
   ```bash
   cd bizosaas/frontend/apps/bizoholic-frontend
   mkdir -p lib/{ui,hooks,utils,api}
   # Create Dockerfile.production (already have one, verify it's modular)
   ```

3. **Document Progress**
   - Update this roadmap as each service completes
   - Create individual migration completion docs
   - Track issues and blockers

---

**Total Services:** 9 (6 customer-facing + 3 admin tools)
**Customer-Facing:** 6/6 ✅ **COMPLETE** (Bizoholic Frontend, Client Portal, Business Directory, CoreLdove Storefront, ThrillRing Gaming, Saleor Dashboard)
**Admin Tools:** 0/3 (Analytics Dashboard, BizOSaaS Admin, CoreLdove Setup Wizard)
**In Progress:** 0
**Remaining:** 3 admin tools (LOW priority - internal use)

**Customer-Facing Progress:** 100% ✅ **COMPLETE**
**Overall Progress:** 66.7% ✅
**Last Verified:** November 4, 2025

---

**Architecture Pattern:** Modular DDD Microservices
**Deployment Flow:** Docker → GHCR → Dokploy → Traefik → Production
**Reference Implementation:** Business Directory (COMPLETE)
