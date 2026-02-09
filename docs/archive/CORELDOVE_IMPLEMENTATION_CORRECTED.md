# CoreLdove Storefront - Corrected Implementation Plan
**Date:** November 3, 2025
**Status:** ✅ Architecture Verified - Building with Standalone Pattern

---

## 🎯 CRITICAL DISCOVERY

After thorough analysis of existing frontends (Bizoholic, Business Directory, Client Portal), we discovered:

### ❌ WRONG ASSUMPTION
- I initially tried to create a pnpm workspace monorepo
- Thought we needed shared node_modules across apps
- Created workspace files that would add unnecessary complexity

### ✅ ACTUAL ARCHITECTURE
**Each frontend is a STANDALONE MICROSERVICE:**
- Own `node_modules` directory
- Own `package.json` with full dependencies
- Own `Dockerfile.production`
- Independently built and deployed
- No workspace dependencies

---

## 📊 EXISTING APPS ANALYSIS

### 1. Business Directory (Port 3004)
```
apps/business-directory/
├── Dockerfile.production       # Standalone build
├── package.json                # 73 dependencies
├── node_modules/               # ~450MB
├── app/                        # Next.js routes
├── components/                 # UI components
└── lib/                        # DDD structure ✅
    ├── api-client/
    ├── auth/
    ├── hooks/
    ├── ui/
    └── utils/
```

### 2. Bizoholic Frontend (Port 3001)
```
apps/bizoholic-frontend/
├── Dockerfile.production
├── package.json
├── node_modules/
├── app/
├── components/
└── hooks/
```

### 3. Client Portal (Port 3001/portal)
```
apps/client-portal/
├── Dockerfile.production
├── package.json
├── node_modules/
├── app/
├── components/
└── lib/                        # DDD structure ✅
```

---

## ✅ CORELDOVE PATTERN (CORRECT)

### Follow EXACT SAME Pattern:
```
apps/coreldove-storefront/
├── Dockerfile.production       # ✅ Already created
├── package.json                # ✅ Already configured
├── pnpm-lock.yaml              # ✅ Uses pnpm (Saleor's choice)
├── node_modules/               # ⏳ Will be built
├── src/
│   └── lib/                    # ✅ Already DDD (Saleor's structure)
│       ├── graphql/
│       ├── checkout/
│       ├── auth/
│       ├── regions/
│       └── util/
├── app/                        # ✅ Next.js App Router
└── next.config.js              # ✅ Configured (basePath, standalone)
```

---

## 🔧 DOCKERFILE ANALYSIS

### Existing Pattern (Business Directory)
```dockerfile
FROM node:18-alpine AS base

FROM base AS deps
COPY package.json package-lock.json ./
RUN npm install --legacy-peer-deps

FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
COPY --from=builder /app/.next/standalone ./
CMD ["node", "server.js"]
```

### CoreLdove Pattern (Same, but pnpm)
```dockerfile
FROM node:20-alpine AS base
RUN corepack enable pnpm

FROM base AS deps
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm run generate && pnpm run build

FROM base AS runner
COPY --from=builder /app/.next/standalone ./
CMD ["node", "server.js"]
```

---

## 📦 SIZE COMPARISON

### Docker Layer Caching Benefits:
```
First Build:
- Base image (node:20-alpine): ~150MB
- Dependencies layer: ~300MB (cached after first build)
- Build layer: ~50MB
- Final image: ~450MB

Subsequent Builds (if package.json unchanged):
- Uses cached dependency layer
- Only rebuilds source code
- Build time: ~2 minutes (vs ~10 minutes first time)
```

### Why Standalone Works:
1. **Docker Layer Caching** - Dependencies only download once
2. **Next.js Standalone** - Only includes necessary files (~50MB vs ~300MB)
3. **Independent Deployment** - No coordination needed
4. **True Microservices** - Each service scales independently

---

## 🚀 CURRENT BUILD STATUS

### Build Command:
```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/coreldove-storefront
docker build -f Dockerfile.production \
  -t ghcr.io/bizoholic-digital/coreldove-storefront:v1.0.0 \
  -t ghcr.io/bizoholic-digital/coreldove-storefront:latest \
  .
```

### Build Stages:
1. ✅ **Base stage** - node:20-alpine with pnpm
2. ✅ **Deps stage** - Install 850 packages (50 seconds)
3. ⏳ **Builder stage** - Copy node_modules, run generate & build
4. ⏳ **Runner stage** - Create final production image

### Expected Output:
```
Successfully built abc123def456
Successfully tagged ghcr.io/bizoholic-digital/coreldove-storefront:v1.0.0
Successfully tagged ghcr.io/bizoholic-digital/coreldove-storefront:latest
```

---

## 📋 DEPLOYMENT PLAN

### Step 1: Verify Build Completion
```bash
docker images | grep coreldove-storefront
# Should show:
# ghcr.io/bizoholic-digital/coreldove-storefront  v1.0.0   450MB
# ghcr.io/bizoholic-digital/coreldove-storefront  latest   450MB
```

### Step 2: Push to GHCR
```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u bizoholic-digital --password-stdin
docker push ghcr.io/bizoholic-digital/coreldove-storefront:v1.0.0
docker push ghcr.io/bizoholic-digital/coreldove-storefront:latest
```

### Step 3: Deploy to KVM4 via Dokploy
```
Server: 72.60.219.244
Application: coreldove-storefront
Image: ghcr.io/bizoholic-digital/coreldove-storefront:latest
Port: 3002
Path: /store

Environment Variables:
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001
NEXT_PUBLIC_SALEOR_API_URL=http://backend-brain-gateway:8001/api/saleor/graphql
NEXT_PUBLIC_STOREFRONT_URL=https://stg.bizoholic.com/store
NEXT_PUBLIC_STOREFRONT_NAME=CoreLdove
NEXT_PUBLIC_SALEOR_CHANNEL=default-channel
NODE_ENV=production
PORT=3002
```

### Step 4: Verify Brain Gateway Routes
```bash
ssh root@72.60.219.244

# Test Saleor GraphQL proxy
docker exec backend-brain-gateway.1.* curl -X POST \
  http://localhost:8001/api/saleor/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ shop { name } }"}'
```

### Step 5: Test Storefront
```
URL: https://stg.bizoholic.com/store
Expected: CoreLdove homepage loads
Check: Network tab shows API calls to backend-brain-gateway
```

---

## 🎯 WHY THIS PATTERN IS CORRECT

### 1. **True Microservices Architecture**
- Each frontend can be deployed independently
- No "big bang" deployments
- Easy rollback per service

### 2. **Team Autonomy**
- Business Directory team can upgrade Next.js without affecting Bizoholic
- CoreLdove can use pnpm while others use npm
- No coordination overhead

### 3. **Docker Optimization**
- Layer caching prevents re-downloading dependencies
- Multi-stage builds keep images small
- Standalone mode = minimal production footprint

### 4. **DDD Compliance**
- Each app has `lib/` structure for domain logic
- Clear separation of concerns
- Self-contained business logic

### 5. **Deployment Simplicity**
- Simple Dockerfile per app
- No workspace complexity
- Standard Docker commands

---

## 📚 DOCUMENTATION CREATED

1. ✅ [FRONTEND_ARCHITECTURE_ANALYSIS.md](FRONTEND_ARCHITECTURE_ANALYSIS.md) - Detailed analysis
2. ✅ [ARCHITECTURE_CLARIFICATION_SUMMARY.md](ARCHITECTURE_CLARIFICATION_SUMMARY.md) - Brain Gateway routing
3. ✅ [CORELDOVE_SALEOR_GATEWAY_CORRECTED.md](CORELDOVE_SALEOR_GATEWAY_CORRECTED.md) - Saleor-specific config
4. ✅ [CORELDOVE_IMPLEMENTATION_CORRECTED.md](CORELDOVE_IMPLEMENTATION_CORRECTED.md) - This document

---

## ✅ SUMMARY

### What We Learned:
1. ❌ No pnpm workspace needed
2. ❌ No shared node_modules
3. ✅ Each app is standalone microservice
4. ✅ Each app follows same DDD pattern
5. ✅ CoreLdove follows same pattern

### What We're Doing:
1. ✅ Using CoreLdove's existing standalone Dockerfile
2. ✅ Building with pnpm (Saleor's choice)
3. ⏳ Building Docker image now
4. ⏳ Will push to GHCR
5. ⏳ Will deploy to KVM4

### Next Steps:
1. Wait for build to complete (~10 minutes first time)
2. Verify images created
3. Push to GitHub Container Registry
4. Deploy to KVM4 via Dokploy
5. Test Brain Gateway routing

---

**Status:** Build in progress - Following correct standalone microservice pattern ✅
