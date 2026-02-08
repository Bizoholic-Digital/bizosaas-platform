# Business Directory Integration Plan

**Date**: 2026-01-16  
**Status**: Integration in Progress  
**Objective**: Integrate existing business-directory frontend with onboarding flow and directory landing pages

---

## 🎯 Discovery Summary

### What Already Exists ✅

#### 1. **Full-Featured Business Directory Frontend**
**Location**: `/portals/business-directory/business-directory/`

**Features**:
- ✅ Complete Next.js 14 application with App Router
- ✅ Advanced search with filters (category, rating, price, distance)
- ✅ Interactive Google Maps integration with clustering
- ✅ Enhanced business profiles with galleries, reviews, events
- ✅ Mobile-responsive design with TailAdmin v2
- ✅ SEO-optimized with structured data
- ✅ API routes with fallback data

**Key Components**:
- `advanced-search-bar.tsx` - Real-time autocomplete
- `interactive-map.tsx` - Google Maps with custom markers
- `enhanced-business-profile.tsx` - Comprehensive business pages
- `advanced-filters.tsx` - Multi-faceted filtering

#### 2. **API Integration Architecture**
**Backend Expectation**: `http://localhost:8001/api/brain/business-directory/*`

**Endpoints Expected**:
- `/search` - Search businesses with filters
- `/categories` - Get business categories
- `/businesses` - List businesses
- `/businesses/featured` - Featured businesses
- `/businesses/[id]` - Business details

**Current Status**: Uses fallback mock data when backend unavailable

---

## 🔄 Integration Strategy

### Phase 1: Connect Onboarding to Directory (IMMEDIATE)

#### What We Built Today
✅ Smart website fallback in `CompanyIdentityStep.tsx`
✅ Generates: `{business-slug}.bizoholic.net`
✅ Slug generation utility: `/lib/business-slug.ts`

#### What Needs to Happen
1. **Create Directory Listing on Onboarding**
   - When business selected without website → create directory entry
   - Store in database with `websiteType: 'directory'`
   - Generate landing page at subdomain

2. **Route Directory URLs to Business Directory App**
   - Configure wildcard subdomain routing
   - `*.bizoholic.net` → business-directory app
   - Extract slug from subdomain → fetch business data

3. **Sync Google Places Data to Directory**
   - Use existing Places API integration from onboarding
   - Create directory listing with Places data
   - Store in `directory_listings` table

---

### Phase 2: Backend API Implementation (WEEK 1)

#### Create Brain Gateway Directory Service

**New File**: `/bizosaas-brain-core/brain-gateway/app/api/directory.py`

```python
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.models.directory import DirectoryListing, SearchFilters
from app.services.directory import DirectoryService

router = APIRouter(prefix="/api/brain/business-directory", tags=["directory"])

@router.get("/search")
async def search_businesses(
    query: Optional[str] = None,
    location: Optional[str] = None,
    category: Optional[str] = None,
    page: int = 1,
    limit: int = 20
):
    """Search businesses with filters"""
    service = DirectoryService()
    results = await service.search(
        query=query,
        location=location,
        category=category,
        page=page,
        limit=limit
    )
    return results

@router.get("/businesses/{slug}")
async def get_business_by_slug(slug: str):
    """Get business details by slug for landing page"""
    service = DirectoryService()
    business = await service.get_by_slug(slug)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business

@router.post("/businesses")
async def create_directory_listing(
    business_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Create directory listing from onboarding"""
    service = DirectoryService()
    listing = await service.create_from_places_data(business_data)
    return listing
```

#### Database Migration

**New File**: `/bizosaas-brain-core/brain-gateway/migrations/001_directory_tables.sql`

```sql
-- Already specified in DIRECTORY_FEATURE_SPEC.md
-- Tables: directory_listings, directory_analytics, directory_claim_requests
```

---

### Phase 3: Landing Page Generation (WEEK 2)

#### Option A: Use Existing Business Directory App

**Pros**:
- ✅ Already built with all features
- ✅ Professional design
- ✅ SEO optimized
- ✅ Mobile responsive

**Cons**:
- ⚠️ Heavy for simple landing pages
- ⚠️ Requires full Next.js deployment

**Implementation**:
1. Deploy business-directory app to `directory.bizoholic.net`
2. Configure wildcard DNS: `*.bizoholic.net` → directory app
3. Extract slug from subdomain in middleware
4. Fetch business data from brain-gateway API
5. Render enhanced business profile page

#### Option B: Create Lightweight Landing Page Service

**Pros**:
- ✅ Faster page loads
- ✅ Lower hosting costs
- ✅ Simpler deployment

**Cons**:
- ⚠️ Need to build templates
- ⚠️ Less features initially

**Implementation**:
1. Create simple Next.js app or static site generator
2. Fetch business data from API
3. Render minimal but SEO-optimized page
4. Upsell to full directory listing

#### **RECOMMENDATION**: Option A (Use Existing App)

**Rationale**:
- Already built and tested
- Professional appearance creates trust
- Rich features encourage upgrades
- Can always optimize later

---

### Phase 4: Domain Configuration (WEEK 2)

#### Current Setup
- `bizoholic.net` → BizoSaaS platform
- `app.bizoholic.net` → Client Portal
- `admin.bizoholic.net` → Admin Dashboard
- `api.bizoholic.net` → Brain Gateway

#### New Configuration
- `directory.bizoholic.net` → Business Directory App
- `*.bizoholic.net` → Wildcard to Directory App
- `{slug}.bizoholic.net` → Individual business pages

#### DNS Configuration
```
Type: CNAME
Host: directory
Value: [deployment-url]

Type: CNAME  
Host: *
Value: directory.bizoholic.net
```

#### Traefik/Nginx Configuration
```yaml
# docker-compose.yml or traefik config
services:
  business-directory:
    image: ghcr.io/bizoholic-digital/business-directory:latest
    labels:
      - "traefik.http.routers.directory.rule=Host(`directory.bizoholic.net`) || HostRegexp(`{subdomain:[a-z0-9-]+}.bizoholic.net`)"
      - "traefik.http.routers.directory.priority=1"
```

---

## 📋 Implementation Checklist

### Week 1: Backend Integration
- [ ] Create `directory.py` API router in brain-gateway
- [ ] Implement `DirectoryService` class
- [ ] Run database migrations for directory tables
- [ ] Create directory listing on onboarding completion
- [ ] Test API endpoints with Postman/curl
- [ ] Update onboarding to call directory creation API

### Week 2: Frontend Deployment
- [ ] Deploy business-directory app to staging
- [ ] Configure wildcard DNS for `*.bizoholic.net`
- [ ] Set up Traefik routing rules
- [ ] Test subdomain routing
- [ ] Implement slug extraction middleware
- [ ] Connect frontend to brain-gateway API

### Week 3: Integration Testing
- [ ] End-to-end test: Onboarding → Directory creation
- [ ] Test: Visit `{slug}.bizoholic.net` → See business page
- [ ] Test: Search in directory app → Find businesses
- [ ] Test: Google indexing of directory pages
- [ ] Performance testing (page load \u003c 2s)
- [ ] Mobile responsiveness testing

### Week 4: Polish \u0026 Launch
- [ ] Add "Claim this business" flow
- [ ] Implement analytics tracking
- [ ] Set up monitoring and alerts
- [ ] Create admin interface for directory management
- [ ] Launch marketing campaign
- [ ] Monitor conversion rates

---

## 🔗 Integration Points

### 1. Onboarding Wizard → Directory Creation

**File**: `/portals/client-portal/components/wizard/OnboardingSteps/CompanyIdentityStep.tsx`

**Current Code** (Line 133-155):
```typescript
// Generate directory URL if business doesn't have a website
const directoryUrl = !details.website 
    ? generateDirectoryUrl(details.companyName || searchQuery, details.location)
    : null;

onUpdate({
    companyName: details.companyName || searchQuery,
    location: details.location,
    website: details.website || directoryUrl || '',
    websiteType: details.website ? 'owned' : 'directory',
    phone: details.phone,
    gmbLink: details.gmbLink
});
```

**Add API Call**:
```typescript
// After generating directory URL
if (!details.website && directoryUrl) {
    // Create directory listing
    await fetch('/api/brain/business-directory/businesses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            slug: generateBusinessSlug(details.companyName, details.location),
            name: details.companyName,
            location: details.location,
            phone: details.phone,
            google_place_id: placeId,
            google_data: details,
            website_type: 'directory'
        })
    });
}
```

### 2. Directory App → Brain Gateway API

**File**: `/portals/business-directory/business-directory/app/api/brain/business-directory/search/route.ts`

**Current**: Tries backend, falls back to mock data

**Update**: Point to correct brain-gateway URL
```typescript
const BACKEND_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://api.bizoholic.net';
```

### 3. Subdomain Routing → Business Page

**New File**: `/portals/business-directory/business-directory/middleware.ts`

```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
    const hostname = request.headers.get('host') || '';
    
    // Extract subdomain
    const subdomain = hostname.split('.')[0];
    
    // If subdomain is not 'directory' or 'www', treat as business slug
    if (subdomain && subdomain !== 'directory' && subdomain !== 'www') {
        // Rewrite to business page
        return NextResponse.rewrite(
            new URL(`/business/${subdomain}`, request.url)
        );
    }
    
    return NextResponse.next();
}

export const config = {
    matcher: '/:path*',
};
```

---

## 🚀 Deployment Strategy

### Option 1: Dokploy Deployment (RECOMMENDED)

1. **Build Docker Image**
   ```bash
   cd /portals/business-directory/business-directory
   docker build -t ghcr.io/bizoholic-digital/business-directory:latest .
   docker push ghcr.io/bizoholic-digital/business-directory:latest
   ```

2. **Create Dokploy Project**
   - Name: `business-directory`
   - Image: `ghcr.io/bizoholic-digital/business-directory:latest`
   - Port: 3010
   - Domain: `directory.bizoholic.net`

3. **Environment Variables**
   ```
   NEXT_PUBLIC_API_BASE_URL=https://api.bizoholic.net
   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIzaSyBZxfvuglTrcCIZZfSVDTltjBWTgEuRLto
   ```

### Option 2: Vercel Deployment

1. **Connect GitHub Repo**
2. **Configure Build**
   - Framework: Next.js
   - Root Directory: `portals/business-directory/business-directory`
   - Build Command: `npm run build`

3. **Add Custom Domain**
   - `directory.bizoholic.net`
   - Configure wildcard: `*.bizoholic.net`

---

## 📊 Success Metrics

### Technical Metrics
- [ ] Page load time \u003c 2 seconds
- [ ] SEO score \u003e 90 (Lighthouse)
- [ ] Mobile score \u003e 95 (Lighthouse)
- [ ] API response time \u003c 500ms
- [ ] Uptime \u003e 99.9%

### Business Metrics
- [ ] Directory listings created per day
- [ ] Subdomain page views
- [ ] Claim requests submitted
- [ ] Conversion to premium listings
- [ ] Google search impressions

---

## 🎓 Key Decisions

### 1. Use Existing Business Directory App ✅
**Reason**: Already built, professional, feature-rich

### 2. Start with `bizoholic.net` Subdomains ✅
**Reason**: Quick to deploy, can migrate to `bizolocal.com` later

### 3. Create Listings on Onboarding ✅
**Reason**: Immediate value, no manual work required

### 4. Deploy via Dokploy ✅
**Reason**: Consistent with platform architecture

---

## 📞 Next Steps

1. **Review this integration plan** with team
2. **Prioritize**: Backend API vs Frontend deployment
3. **Assign tasks** for Week 1 implementation
4. **Set up staging environment** for testing
5. **Schedule demo** after Week 2 completion

---

**Estimated Timeline**: 4 weeks to full launch  
**Estimated Effort**: 60-80 hours  
**Risk Level**: Low (most components already built)  
**Revenue Impact**: High (immediate lead generation + upsell path)

---

*Last Updated: 2026-01-16 13:10 UTC*
