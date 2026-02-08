# Business Directory Frontend - Frontend Service

## Service Identity
- **Name**: Business Directory Frontend
- **Type**: Frontend - Business Listings (Next.js 15)
- **Container**: `bizosaas-business-directory-frontend-staging` (NOT DEPLOYED)
- **Image**: `ghcr.io/bizoholic-digital/bizosaas-business-directory-frontend:staging`
- **Port**: `TBD:3000`
- **Domain**: `stg.bizoholic.com/directory` OR `directory.bizoholic.com`
- **Status**: ❌ Not Deployed

## Purpose
Public business directory with search, filtering, business profiles, reviews, and multi-tenant business listings.

## Container Architecture
```
Business Directory Frontend Container
├── Next.js 15 (App Router)
├── Search Interface
├── Map Integration (Google Maps)
├── Review System
└── Category Browser
```

## Key Features
- **Business Search**: Full-text search with filters
- **Map View**: Geographic business search
- **Business Profiles**: Detailed company information
- **Review System**: User reviews and ratings
- **Category Navigation**: Hierarchical categories
- **Featured Listings**: Premium business placement

## API Integration
```typescript
// Brain Gateway routing
const BRAIN_API = process.env.NEXT_PUBLIC_API_BASE_URL

// Search businesses
GET /api/brain/business-directory/businesses/search?q={query}&location={location}

// Get business details
GET /api/brain/business-directory/businesses/{id}

// Submit review
POST /api/brain/business-directory/reviews
```

## Deployment Required
```bash
# Build container
cd bizosaas/frontend/apps/business-directory-frontend
docker build -t ghcr.io/bizoholic-digital/bizosaas-business-directory-frontend:staging .
docker push ghcr.io/bizoholic-digital/bizosaas-business-directory-frontend:staging

# Deploy to Dokploy
# Add to dokploy-frontend-staging.yml
```

---
**Status**: ❌ Pending Deployment
**Priority**: MEDIUM (complete platform)
**Deployment**: Containerized Microservice (needs build)
**Last Updated**: October 15, 2025
