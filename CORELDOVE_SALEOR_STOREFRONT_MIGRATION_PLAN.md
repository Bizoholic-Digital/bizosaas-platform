# CoreLdove Saleor Storefront Migration Plan

**Date:** November 2, 2025
**Status:** 🔄 Planning Phase
**Architecture:** Saleor Next.js 15 + React 19 + GraphQL + Modular DDD

---

## 🎯 STRATEGIC OBJECTIVE

Repurpose the official **Saleor Next.js Storefront** as the CoreLdove e-commerce frontend, creating a production-ready online store that:

1. **Connects to CoreLdove backend** (Django + Saleor API at port 8003)
2. **Follows modular DDD architecture** (like Business Directory)
3. **Integrates with existing infrastructure** (Stripe, PostgreSQL, n8n workflows)
4. **Deploys independently** via Docker → GHCR → Dokploy
5. **Serves at** `stg.bizoholic.com/store` or `coreldove.bizoholic.com`

---

## 📊 CURRENT STATE ANALYSIS

### Existing CoreLdove Frontend
**Location:** `bizosaas/frontend/apps/coreldove-frontend/`
**Purpose:** Store setup wizard and admin interface
**Status:** Basic UI, not a customer-facing storefront
**Technology:** Next.js 15, React 19, Tailwind CSS

### Saleor Official Storefront
**Repository:** https://github.com/saleor/storefront
**Technology Stack:**
- Next.js 15 with App Router
- React 19 with Server Components
- TypeScript (strict mode)
- GraphQL with Codegen
- Tailwind CSS
- Stripe + Adyen payment support
- TypedDocumentString for type safety

**Key Features:**
✅ Product catalog with categories
✅ Shopping cart and checkout
✅ Customer accounts and authentication
✅ Order management
✅ Payment processing (Stripe/Adyen)
✅ Multi-channel support
✅ SEO optimized
✅ Mobile responsive
✅ GraphQL API integration

---

## 🏗️ MIGRATION STRATEGY

### Phase 1: Repository Setup (Day 1)

**1.1 Clone Saleor Storefront**
```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/

# Clone official Saleor storefront
git clone https://github.com/saleor/storefront.git coreldove-storefront-temp

# Copy to our structure
cp -r coreldove-storefront-temp/. coreldove-storefront/
rm -rf coreldove-storefront-temp

cd coreldove-storefront
```

**1.2 Rename Package**
Update `package.json`:
```json
{
  "name": "coreldove-storefront",
  "version": "1.0.0",
  "description": "CoreLdove E-commerce Storefront - Powered by Saleor"
}
```

**1.3 Initialize Git**
```bash
git init
git add .
git commit -m "Initial CoreLdove storefront from Saleor template"
```

### Phase 2: Saleor API Integration (Day 1-2)

**2.1 Environment Configuration**
Create `.env.local`:
```env
# Saleor API Connection
NEXT_PUBLIC_SALEOR_API_URL=http://bizosaas-saleor-api-8003:8000/graphql/
NEXT_PUBLIC_STOREFRONT_NAME=CoreLdove

# Channel Configuration
NEXT_PUBLIC_SALEOR_CHANNEL=default-channel

# Payment Gateways
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_CHECKOUT_APP_URL=http://localhost:3002

# Feature Flags
NEXT_PUBLIC_ENABLE_ACCOUNT=true
NEXT_PUBLIC_ENABLE_CHECKOUT=true
```

**2.2 Verify Backend Connection**
Check CoreLdove backend is running:
```bash
curl http://bizosaas-saleor-api-8003:8000/graphql/
```

**2.3 GraphQL Code Generation**
```bash
pnpm install
pnpm run generate  # Generates TypeScript types from GraphQL schema
```

### Phase 3: Modular DDD Architecture (Day 2)

**3.1 Create lib/ Directory**
Following Business Directory pattern:
```
coreldove-storefront/
├── lib/
│   ├── ui/              # UI components (from Saleor)
│   ├── graphql/         # GraphQL queries/mutations
│   ├── api/             # API client utilities
│   ├── hooks/           # Custom React hooks
│   ├── utils/           # Helper functions
│   └── types/           # TypeScript types
```

**3.2 Self-Contained Package Dependencies**
Ensure all Saleor dependencies are in `package.json`:
- `@apollo/client` or GraphQL client
- `@stripe/stripe-js`
- All Radix UI components
- `graphql-request` or similar
- `zod` for validation

**3.3 Create Modular Dockerfile**
```dockerfile
# CoreLdove Storefront - Modular Microservice Dockerfile
# Architecture: Standalone containerized microservice following DDD principles
# Build from service directory

FROM node:20-alpine AS base

# Dependencies
FROM base AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml* ./
RUN corepack enable pnpm && pnpm install --frozen-lockfile

# Builder
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

RUN corepack enable pnpm && pnpm run build

# Runner
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3002
ENV HOSTNAME="0.0.0.0"

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
RUN mkdir .next && chown nextjs:nodejs .next

COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3002

CMD ["node", "server.js"]
```

### Phase 4: CoreLdove Branding (Day 2-3)

**4.1 Theme Customization**
Update `tailwind.config.ts`:
```typescript
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#0066CC',  // CoreLdove blue
          50: '#E6F0FF',
          // ... full palette
        },
        accent: '#FF6B35',     // CoreLdove orange
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
}
```

**4.2 Logo and Assets**
```bash
# Replace Saleor assets with CoreLdove branding
cp /path/to/coreldove-logo.svg public/logo.svg
cp /path/to/coreldove-favicon.ico public/favicon.ico
```

**4.3 Site Metadata**
Update `app/layout.tsx`:
```typescript
export const metadata: Metadata = {
  title: 'CoreLdove - Premium E-commerce Platform',
  description: 'Shop the best products on CoreLdove',
  // ... other metadata
}
```

### Phase 5: Payment Integration (Day 3)

**5.1 Stripe Configuration**
Already integrated in Saleor storefront:
- Update Stripe publishable key in `.env.local`
- Configure webhook endpoints for payment events
- Test checkout flow

**5.2 n8n Workflow Integration**
Create workflows for:
- Order confirmation emails
- Inventory updates
- Customer notifications
- Abandoned cart recovery

### Phase 6: Build & Deploy (Day 3-4)

**6.1 Build Docker Image**
```bash
cd bizosaas/frontend/apps/coreldove-storefront

docker build -f Dockerfile.production \
  -t ghcr.io/bizoholic-digital/coreldove-storefront:v1.0.0 \
  -t ghcr.io/bizoholic-digital/coreldove-storefront:latest \
  .
```

**6.2 Push to GHCR**
```bash
docker push ghcr.io/bizoholic-digital/coreldove-storefront:v1.0.0
docker push ghcr.io/bizoholic-digital/coreldove-storefront:latest
```

**6.3 Dokploy Deployment**
```
Application Name:        coreldove-storefront
Deployment Type:        Docker Image
Image:                  ghcr.io/bizoholic-digital/coreldove-storefront:latest
Port:                   3002
Domain:                 stg.bizoholic.com
Path Prefix:            /store
Strip Prefix:           YES

Environment Variables:
  NEXT_PUBLIC_SALEOR_API_URL=http://bizosaas-saleor-api-8003:8000/graphql/
  NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
  NEXT_PUBLIC_STOREFRONT_NAME=CoreLdove
  NEXT_PUBLIC_SALEOR_CHANNEL=default-channel
```

---

## 📦 DEPENDENCIES COMPARISON

### Saleor Storefront (Official)
```json
{
  "@apollo/client": "^3.x",
  "@stripe/stripe-js": "^2.x",
  "graphql": "^16.x",
  "next": "15.x",
  "react": "19.x",
  "@radix-ui/react-*": "^1.x",
  "tailwindcss": "^3.x"
}
```

### CoreLdove Frontend (Current)
```json
{
  "@stripe/stripe-js": "^7.9.0",
  "next": "15.5.3",
  "react": "19.0.0",
  "@radix-ui/react-*": "^1.x",
  "tailwindcss": "^3.4.17"
}
```

**Strategy:** Use Saleor's complete dependency set (already optimized)

---

## 🔄 INTEGRATION POINTS

### 1. Backend API (CoreLdove Django + Saleor)
**Endpoint:** `http://bizosaas-saleor-api-8003:8000/graphql/`
**Authentication:** JWT tokens
**Operations:**
- Product catalog queries
- Cart management
- Checkout mutations
- Order tracking

### 2. Payment Gateway (Stripe)
**Integration:** Saleor Checkout App
**Webhooks:**
- `payment_intent.succeeded`
- `payment_intent.payment_failed`
- `checkout.session.completed`

### 3. n8n Workflows
**Triggers:**
- New order → Send confirmation email
- Payment success → Update inventory
- Order shipped → Notify customer
- Abandoned cart → Recovery email (24h delay)

### 4. Database (PostgreSQL)
**Shared:** `shared_postgres` container
**Database:** `coreldove_db`
**Connection:** Via Saleor backend (no direct frontend access)

---

## ✅ SUCCESS CRITERIA

1. ✅ **Storefront loads** at `stg.bizoholic.com/store`
2. ✅ **Products display** from CoreLdove backend
3. ✅ **Cart functions** (add, remove, update quantities)
4. ✅ **Checkout works** with Stripe test mode
5. ✅ **Orders persist** in CoreLdove database
6. ✅ **Email notifications** trigger via n8n
7. ✅ **Mobile responsive** design
8. ✅ **SEO optimized** metadata
9. ✅ **Zero workspace dependencies** (modular DDD)
10. ✅ **Independent deployment** via Docker

---

## 📁 DIRECTORY STRUCTURE (Post-Migration)

```
bizosaas/frontend/apps/
├── coreldove-frontend/          # Admin wizard (keep as-is)
│   ├── components/wizards/
│   └── ...
│
├── coreldove-storefront/        # NEW: Customer-facing store
│   ├── src/
│   │   ├── app/                # Next.js App Router
│   │   │   ├── (main)/
│   │   │   │   ├── page.tsx           # Homepage
│   │   │   │   ├── products/          # Product catalog
│   │   │   │   ├── cart/              # Shopping cart
│   │   │   │   └── checkout/          # Checkout flow
│   │   │   └── account/               # Customer account
│   │   ├── components/                # React components
│   │   │   ├── product/
│   │   │   ├── cart/
│   │   │   ├── checkout/
│   │   │   └── ui/
│   │   └── lib/                       # Self-contained libraries
│   │       ├── graphql/
│   │       ├── api/
│   │       ├── hooks/
│   │       └── utils/
│   ├── gql/                           # GraphQL queries
│   ├── public/                        # Static assets
│   ├── Dockerfile.production          # Modular standalone build
│   ├── package.json
│   ├── next.config.js
│   └── tailwind.config.ts
```

---

## 🚀 DEPLOYMENT TIMELINE

### Day 1: Foundation
- Clone Saleor storefront
- Configure package.json
- Set up environment variables
- Test GraphQL connection

### Day 2: Architecture
- Create lib/ structure
- Build modular Dockerfile
- Implement CoreLdove branding
- Test local build

### Day 3: Integration
- Configure Stripe payments
- Set up n8n workflows
- Test checkout flow
- Build production image

### Day 4: Deployment
- Push to GHCR
- Deploy to Dokploy
- Configure Traefik routing
- Verify production functionality

---

## 🔧 MAINTENANCE PLAN

### Keeping Up with Saleor Updates
```bash
# Add Saleor upstream
cd coreldove-storefront
git remote add upstream https://github.com/saleor/storefront.git

# Pull updates periodically
git fetch upstream
git merge upstream/main --no-commit
# Resolve conflicts, preserve CoreLdove customizations
```

### GraphQL Schema Updates
```bash
# Regenerate types when Saleor backend updates
pnpm run generate
```

---

## 📊 COMPARISON: Current vs New

### Current Setup (coreldove-frontend)
```
Purpose:        Admin setup wizard
Users:          Store administrators
Features:       Store configuration
Integration:    Basic API calls
Deployment:     Not production-ready
```

### New Storefront (coreldove-storefront)
```
Purpose:        Customer-facing e-commerce store
Users:          End customers
Features:       Full shopping experience
Integration:    Saleor GraphQL API + Stripe + n8n
Deployment:     Production-ready, containerized
```

---

## 🎯 NEXT STEPS

1. **Clone Saleor storefront** to `coreldove-storefront/`
2. **Configure API connection** to CoreLdove backend
3. **Apply modular DDD** architecture pattern
4. **Customize branding** for CoreLdove
5. **Test build** locally
6. **Deploy to staging** at `stg.bizoholic.com/store`
7. **Verify functionality** (products, cart, checkout)
8. **Launch production** store

---

**Architecture:** Saleor Next.js 15 + Modular DDD
**Pattern:** Business Directory (proven & deployed)
**Backend:** CoreLdove Django + Saleor API (port 8003)
**Deployment:** Docker → GHCR → Dokploy → stg.bizoholic.com/store
