# BizOSaaS Microservices Architecture with DDD Principles

**Date:** October 30, 2025
**Status:** CORRECTED ARCHITECTURE
**Previous Error:** Attempted monorepo approach - INCORRECT
**Correct Approach:** Containerized microservices with shared npm packages

---

## Core Architectural Principles

### 1. Domain-Driven Design (DDD)
- Each service represents a bounded context
- Services are independently deployable
- Each service has its own database/data store
- Services communicate via APIs and message queues

### 2. Microservices Architecture
- **Independent deployment** - Each service can be deployed without affecting others
- **Technology agnostic** - Services can use different tech stacks
- **Isolated failures** - One service failure doesn't cascade
- **Independent scaling** - Scale services based on their specific load

### 3. Shared Components via npm Packages
- Reduce code redundancy through shared libraries
- Packages published to GitHub Packages (npm registry)
- Each microservice installs packages like any other npm dependency
- **NO monorepo** - Services are completely independent

---

## BizOSaaS Service Architecture

### Frontend Microservices (7 Services)
Each frontend is a **separate microservice** with its own:
- Git repository directory
- Docker container
- Deployment configuration
- Domain/subdomain
- Independent CI/CD pipeline

```
1. Bizoholic Frontend       → bizoholic.com
2. CoreLDove Frontend        → coreldove.com
3. ThrillRing Frontend       → thrillring.com
4. Client Portal             → portal.bizosaas.com
5. Business Directory        → directory.bizosaas.com
6. Analytics Dashboard       → analytics.bizosaas.com
7. Admin Dashboard           → admin.bizosaas.com
```

### Backend Microservices (15+ Services)
```
1. Auth Service              → auth.bizosaas.com
2. AI Agents Service         → ai.bizosaas.com
3. Brain Gateway             → gateway.bizosaas.com
4. Wagtail CMS               → cms.bizosaas.com
5. Django CRM                → crm.bizosaas.com
6. Amazon Sourcing           → sourcing.bizosaas.com
7. Business Directory API    → directory-api.bizosaas.com
8. CoreLDove Backend         → api.coreldove.com
9. Payment Service           → payments.bizosaas.com
10. Notification Service     → notifications.bizosaas.com
... and more
```

---

## Shared Packages Strategy

### Package Publishing Workflow

```bash
# 1. Build the package
cd packages/auth
npm run build

# 2. Publish to GitHub Packages
npm publish

# 3. Services install from npm registry
cd ../../bizosaas/misc/services/bizoholic-frontend
npm install @bizosaas/auth@latest
```

### Package Versioning
- Use semantic versioning (semver)
- Breaking changes: Major version bump
- New features: Minor version bump
- Bug fixes: Patch version bump

### Current Shared Packages (6 Total)

#### 1. @bizosaas/auth
**Purpose:** Authentication, authorization, session management
**Used by:** All 7 frontends
**Contents:**
- AuthContext and AuthProvider
- useAuth hook
- Next.js middleware
- Login/logout logic
- httpOnly cookie handling

#### 2. @bizosaas/ui-components
**Purpose:** Reusable UI components (shadcn/ui based)
**Used by:** All 7 frontends
**Contents:**
- Button, Card, Input, Label, Toast
- Form components
- Layout components
- Theme provider

#### 3. @bizosaas/api-client
**Purpose:** HTTP client for backend APIs
**Used by:** All 7 frontends
**Contents:**
- Axios configuration
- Request/response interceptors
- Error handling
- Type-safe API methods

#### 4. @bizosaas/hooks
**Purpose:** Reusable React hooks
**Used by:** All 7 frontends
**Contents:**
- useLocalStorage
- useDebounce
- useMediaQuery
- useClickOutside
- Custom business logic hooks

#### 5. @bizosaas/utils
**Purpose:** Utility functions
**Used by:** All frontends and some backends
**Contents:**
- cn() - className utility
- Date formatting
- String manipulation
- Validation helpers

#### 6. @bizosaas/animated-components
**Purpose:** Framer Motion based animations
**Used by:** Marketing frontends (Bizoholic, CoreLDove, ThrillRing)
**Contents:**
- MovingBorder button
- Spotlight effect
- ShimmerButton
- TextReveal
- FadeIn animations

---

## Docker Build Strategy

### CORRECT Approach: Microservice Dockerfiles

Each service has its own Dockerfile that:
1. Uses multi-stage build for optimization
2. Installs dependencies from npm registry
3. Builds only that service
4. Creates minimal production image

#### Example: Bizoholic Frontend Dockerfile

```dockerfile
# Stage 1: Dependencies
FROM node:18-alpine AS deps
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY .npmrc ./

# Install dependencies (including @bizosaas packages from GitHub Packages)
RUN npm ci --only=production

# Stage 2: Builder
FROM node:18-alpine AS builder
WORKDIR /app

COPY package*.json ./
COPY .npmrc ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 3: Runner
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"]
```

### Key Points:
- **NO workspace copying** - Each service is self-contained
- **npm registry packages** - Shared packages come from GitHub Packages
- **Independent builds** - Each service builds without knowing about others
- **Minimal images** - Only production dependencies included

---

## Deployment Architecture

### Independent Deployment Pipeline

```
Developer Push → GitHub → GitHub Actions → Build Docker Image →
Push to GHCR → Dokploy → Deploy to K3s → Service Running
```

### Each Service:
1. Has its own GitHub Actions workflow
2. Builds its own Docker image
3. Pushes to GitHub Container Registry (GHCR)
4. Deployed independently via Dokploy
5. Scales independently based on load

### Service Communication

```
Frontend (bizoholic.com)
    ↓ HTTP/REST
Auth Service (auth.bizosaas.com)
    ↓ JWT Validation
    ↓
Backend Services
    ↓ Message Queue (RabbitMQ/Redis)
    ↓
AI Agents / Background Jobs
```

---

## Current Status

### ✅ Completed
- [x] 6 shared packages created and working
- [x] npm workspaces configured for LOCAL development
- [x] Bizoholic frontend using shared packages
- [x] Local build successful (5.2s)
- [x] Code reduction: 93% (150 lines → 10 lines)

### ⚠️ CORRECTION NEEDED
- [ ] Remove monorepo Dockerfile
- [ ] Configure GitHub Packages authentication
- [ ] Publish all 6 packages to GitHub Packages
- [ ] Update service Dockerfiles to use published packages
- [ ] Update deployment documentation

### 🎯 Next Actions
1. Set up .npmrc for GitHub Packages authentication
2. Publish packages: @bizosaas/auth, ui-components, api-client, hooks, utils, animated-components
3. Update Bizoholic package.json to use published versions
4. Create proper microservice Dockerfile for Bizoholic
5. Test independent Docker build
6. Deploy to Dokploy
7. Repeat for remaining 6 frontends

---

## Development Workflow

### Local Development (npm workspaces)
```bash
# Work on shared packages locally
cd /home/alagiri/projects/bizosaas-platform
npm install  # Links all workspace packages

# Make changes to shared package
cd packages/auth
# ... make changes ...
npm run build

# Changes immediately available to services
cd ../../bizosaas/misc/services/bizoholic-frontend
npm run dev  # Uses local workspace version
```

### Production Build (published packages)
```bash
# Publish updated package
cd packages/auth
npm version patch  # or minor/major
npm run build
npm publish

# Services pull from registry
cd ../../bizosaas/misc/services/bizoholic-frontend
npm update @bizosaas/auth
docker build -t bizoholic-frontend .
```

---

## Benefits of This Architecture

### 1. True Microservices
- Services are truly independent
- No coupling through monorepo structure
- Can be moved to separate repositories if needed

### 2. Efficient CI/CD
- Only changed services need rebuilding
- Parallel deployment possible
- Fast build times (no copying entire monorepo)

### 3. Reduced Redundancy
- Shared packages eliminate duplicate code
- 93% code reduction across services
- Single source of truth for common functionality

### 4. DDD Compliance
- Each service represents a bounded context
- Clear boundaries between domains
- Independent data stores per service

### 5. Scalability
- Scale services independently
- Add new services without affecting existing ones
- Easy to move services to different infrastructure

---

## Comparison: Monorepo vs Microservices

| Aspect | ❌ Monorepo | ✅ Microservices + npm |
|--------|-----------|---------------------|
| **Build** | Copy all packages into each service | Install from registry |
| **Deployment** | Coupled deployments | Independent deployments |
| **CI/CD** | Slow (builds everything) | Fast (builds only service) |
| **Docker Image** | Large (includes all code) | Small (only service code) |
| **DDD Compliance** | Poor (tight coupling) | Excellent (loose coupling) |
| **Repository** | Single repo required | Can split into multiple repos |
| **Team Autonomy** | Limited | Full autonomy per service |
| **Scaling** | Scale everything together | Scale services independently |

---

## Conclusion

The **correct architecture** for BizOSaaS is:

1. **Containerized microservices** following DDD principles
2. **Shared npm packages** published to GitHub Packages
3. **Independent deployments** via Dokploy/K3s
4. **npm workspaces** for LOCAL development only
5. **No monorepo builds** - each service builds independently

This approach gives us:
- ✅ 93% code reduction through shared packages
- ✅ True microservices independence
- ✅ DDD compliance with bounded contexts
- ✅ Fast, efficient builds and deployments
- ✅ Easy scaling and maintenance

---

**Next Document:** [GITHUB_PACKAGES_SETUP.md](./GITHUB_PACKAGES_SETUP.md)
