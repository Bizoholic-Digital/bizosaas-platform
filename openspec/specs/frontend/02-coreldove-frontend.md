# CorelDove Frontend - Frontend Service

## Service Identity
- **Name**: CorelDove E-commerce Frontend
- **Type**: Frontend - E-commerce Storefront (Next.js 15)
- **Container**: `bizosaas-coreldove-frontend-staging`
- **Image**: `ghcr.io/bizoholic-digital/bizosaas-coreldove-frontend:staging`
- **Port**: `3002:3000`
- **Domain**: `stg.coreldove.com`
- **Status**: 🟡 HTTP 301 (HTTPS redirect without SSL)

## Purpose
E-commerce storefront with product catalog, shopping cart, checkout, and order management integrated with Saleor backend.

## Container Architecture
```
CorelDove Frontend Container
├── Next.js 15 (App Router)
├── E-commerce Components
├── Saleor GraphQL Client
└── Payment Integration (Stripe/PayPal)
```

## Key Features
- Product catalog with search/filter
- Shopping cart management
- Multi-step checkout
- Order tracking
- User account management
- Payment processing (Stripe, PayPal)

## API Integration
```typescript
// All routes through Brain Gateway
const BRAIN_API = process.env.NEXT_PUBLIC_API_BASE_URL // http://bizosaas-brain-staging:8001

// Product catalog
GET /api/brain/saleor/products

// Cart operations
POST /api/brain/saleor/checkout/create
POST /api/brain/saleor/checkout/add-line

// Order management
GET /api/brain/saleor/orders/{id}
```

## Deployment Pipeline
```
Local WSL2 Build → GitHub Push → GHCR Registry → Dokploy Staging → Dokploy Production
```

## Current Issue
🟡 **HTTP 301 Redirect**: Frontend configured for HTTPS but no SSL cert in Traefik
**Fix**: Add SSL certificate or force HTTP-only in development

---
**Status**: 🟡 Needs SSL Configuration
**Deployment**: Containerized Microservice
**Last Updated**: October 15, 2025
