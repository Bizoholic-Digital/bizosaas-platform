# Business Directory - Modular Microservices Realignment Plan
## Transitioning from Monorepo to Modular Containerized Architecture

**Date:** 2025-11-02
**Status:** 📋 Planning Phase
**Objective:** Align Business Directory with established modular DDD microservices pattern

---

## 🎯 PROBLEM STATEMENT

### Current Architecture (WRONG):
```
Business Directory
├── Uses workspace packages (@bizoholic-digital/*)
├── Builds from repository root
└── Depends on /packages/* directory
```

**Issues:**
- ❌ Conflicts with established modular pattern
- ❌ Can't build from service directory
- ❌ Workspace packages not in npm registry
- ❌ Different from all other services

### Target Architecture (CORRECT):
```
Business Directory (Standalone Microservice)
├── All code self-contained
├── Builds from own directory
├── No workspace dependencies
└── Follows coreldove-backend pattern
```

**Benefits:**
- ✅ Consistent with 14+ existing services
- ✅ True modular DDD bounded context
- ✅ Independent deployment
- ✅ No external dependencies

---

## 📊 CURRENT DEPENDENCY ANALYSIS

### Workspace Packages Used:
1. `@bizoholic-digital/ui-components` - UI library (Button, Card, Input, etc.)
2. `@bizoholic-digital/auth` - Authentication utilities
3. `@bizoholic-digital/api-client` - API communication
4. `@bizoholic-digital/hooks` - React hooks
5. `@bizoholic-digital/utils` - Utility functions
6. `@bizoholic-digital/animated-components` - Animation components

### Component Files Using Workspace Packages:
- 8 component files import from `@bizoholic-digital/*`
- All imports in `/components` directory
- Primarily using `ui-components` package

---

## 🏗️ MIGRATION STRATEGY

### Phase 1: Copy Workspace Code Locally
**Duration:** 30 minutes
**Risk:** Low

1. **Create local `lib/ui` directory**
   ```bash
   mkdir -p bizosaas/frontend/apps/business-directory/lib/ui
   ```

2. **Copy UI components from workspace**
   ```bash
   cp -r packages/ui-components/src/* \
         bizosaas/frontend/apps/business-directory/lib/ui/
   ```

3. **Copy utilities and hooks**
   ```bash
   cp -r packages/utils/src/* \
         bizosaas/frontend/apps/business-directory/lib/utils/

   cp -r packages/hooks/src/* \
         bizosaas/frontend/apps/business-directory/lib/hooks/
   ```

### Phase 2: Update Imports
**Duration:** 20 minutes
**Risk:** Low

Replace workspace imports with local imports:

**Before:**
```typescript
import { Button, Card } from '@bizoholic-digital/ui-components';
import { useDebounce } from '@bizoholic-digital/hooks';
```

**After:**
```typescript
import { Button, Card } from '@/lib/ui';
import { useDebounce } from '@/lib/hooks';
```

**Files to Update:** (8 files)
- components/business/business-card.tsx
- components/business/enhanced-business-profile.tsx
- components/search/search-bar.tsx
- components/search/advanced-search-bar.tsx
- components/search/advanced-filters.tsx
- components/layout/header.tsx
- app/search/page.tsx
- (and 1 more)

### Phase 3: Update package.json
**Duration:** 10 minutes
**Risk:** Low

**Remove** workspace dependencies:
```json
{
  "dependencies": {
    // REMOVE these:
    // "@bizoholic-digital/ui-components": "^1.0.0",
    // "@bizoholic-digital/auth": "^1.0.0",
    // "@bizoholic-digital/api-client": "^1.0.0",
    // "@bizoholic-digital/hooks": "^1.0.0",
    // "@bizoholic-digital/utils": "^1.0.0",
    // "@bizoholic-digital/animated-components": "^1.0.0",

    // KEEP these:
    "next": "15.5.3",
    "react": "19.0.0",
    // ... all other dependencies
  }
}
```

Add dependencies that workspace packages used:
```json
{
  "dependencies": {
    "class-variance-authority": "^0.7.0",
    "tailwind-merge": "^2.2.0",
    "clsx": "^2.0.0"
    // ... check workspace package.json for full list
  }
}
```

### Phase 4: Create Modular Dockerfile
**Duration:** 15 minutes
**Risk:** Low

**Pattern:** Follow `coreldove-backend/Dockerfile`

```dockerfile
# Business Directory Microservice - Modular Architecture
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps

# Build the application
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1
ENV NODE_ENV production

RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
RUN mkdir .next && chown nextjs:nodejs .next

COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3004
ENV PORT 3004
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

**Key Changes:**
- ❌ No `COPY packages ./packages`
- ❌ No workspace package resolution
- ✅ Builds from service directory (WORKDIR /app)
- ✅ Simple COPY . . pattern

### Phase 5: Update Build Process
**Duration:** 10 minutes
**Risk:** Low

**OLD Build (Monorepo):**
```bash
cd /home/alagiri/projects/bizosaas-platform
docker build -f bizosaas/frontend/apps/business-directory/Dockerfile.production .
```

**NEW Build (Modular):**
```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/business-directory
docker build -f Dockerfile.production -t ghcr.io/bizoholic-digital/bizosaas-business-directory:latest .
```

**Benefits:**
- ✅ Builds from service directory
- ✅ No repository root needed
- ✅ Smaller build context
- ✅ Faster builds

### Phase 6: Test & Verify
**Duration:** 20 minutes
**Risk:** Medium

1. **Local Build Test**
   ```bash
   cd bizosaas/frontend/apps/business-directory
   npm install
   npm run build
   ```

2. **Docker Build Test**
   ```bash
   docker build -f Dockerfile.production -t test-bd:latest .
   ```

3. **Component Verification**
   - Verify all UI components render correctly
   - Test navigation and routing
   - Check basePath (/directory) works

### Phase 7: Deploy to GHCR & Dokploy
**Duration:** 15 minutes
**Risk:** Low

Same as before, but with modular build:

```bash
cd bizosaas/frontend/apps/business-directory

docker build -f Dockerfile.production \
  -t ghcr.io/bizoholic-digital/bizosaas-business-directory:v1.0.0 \
  -t ghcr.io/bizoholic-digital/bizosaas-business-directory:latest \
  .

docker push ghcr.io/bizoholic-digital/bizosaas-business-directory:v1.0.0
docker push ghcr.io/bizoholic-digital/bizosaas-business-directory:latest
```

---

## 📋 EXECUTION CHECKLIST

### Pre-Migration
- [ ] Backup current code
- [ ] Document current workspace package versions
- [ ] Review UI component dependencies

### Migration Tasks
- [ ] Copy workspace packages to local lib/
- [ ] Update all 8 component imports
- [ ] Remove workspace dependencies from package.json
- [ ] Add direct npm dependencies
- [ ] Create new modular Dockerfile
- [ ] Update .dockerignore (if needed)
- [ ] Test local npm build
- [ ] Test Docker build

### Post-Migration
- [ ] Build and push to GHCR
- [ ] Update Dokploy configuration
- [ ] Deploy to stg.bizoholic.com/directory
- [ ] Verify functionality
- [ ] Update documentation

---

## 🎯 SUCCESS CRITERIA

1. ✅ **No workspace dependencies** in package.json
2. ✅ **Builds from service directory** (not repository root)
3. ✅ **Docker build succeeds** without /packages access
4. ✅ **Deploys to Dokploy** using GHCR image
5. ✅ **All features work** at stg.bizoholic.com/directory
6. ✅ **Consistent with** coreldove-backend pattern

---

## ⏱️ TIMELINE

**Total Estimated Time:** 2 hours
**Recommended Approach:** Execute all phases in sequence

| Phase | Task | Duration | Complexity |
|-------|------|----------|------------|
| 1 | Copy workspace code | 30 min | Low |
| 2 | Update imports | 20 min | Low |
| 3 | Update package.json | 10 min | Low |
| 4 | Create Dockerfile | 15 min | Low |
| 5 | Update build process | 10 min | Low |
| 6 | Test & verify | 20 min | Medium |
| 7 | Deploy to GHCR | 15 min | Low |

---

## 🚀 READY TO EXECUTE

All phases documented and ready for implementation.

**Next Action:** Begin Phase 1 - Copy workspace packages locally

---

**Architecture:** Modular DDD Microservices
**Pattern:** coreldove-backend (proven & deployed)
**Deployment:** Docker → GHCR → Dokploy → stg.bizoholic.com/directory
