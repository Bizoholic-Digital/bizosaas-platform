# Wagtail CMS Integration Plan

**Date**: December 1, 2025  
**Objective**: Make all frontend pages dynamic and manageable through Wagtail CMS

## 📊 Current State Analysis

### Wagtail Page Models Available:
1. **BizoholicHomePage** - Main homepage with hero, features, stats
2. **ServicePage** - Individual service pages with pricing, features
3. **ContentPage** - Blog posts and articles
4. **LandingPage** - Marketing landing pages with A/B testing
5. **CampaignPage** - Campaign management pages
6. **FAQPage** - FAQ and help content
7. **TenantAwarePage** - Base for multi-tenant pages

### Frontend Pages to Make Dynamic:
1. **Homepage** (`/`) - Use `BizoholicHomePage`
2. **Services** (`/services/*`) - Use `ServicePage`
3. **Blog** (`/blog`) - Use `ContentPage`
4. **About** (`/about`) - Use `ContentPage` or create `AboutPage`
5. **Pricing** (`/pricing`) - Use `LandingPage` with pricing blocks
6. **Contact** (`/contact`) - Use `LandingPage` or `ContentPage`
7. **Portfolio/Case Studies** - Use `ContentPage`
8. **Resources** - Use `ContentPage`

## 🎯 Implementation Strategy

### Phase 1: Fix Session & Enable Wagtail API (PRIORITY)
**Status**: In Progress

1. ✅ Fix `/api/auth/me` 401 errors
2. ⏳ Configure Wagtail API for public access
3. ⏳ Create Wagtail pages for existing content
4. ⏳ Update frontend to fetch from Wagtail

### Phase 2: Homepage Integration
**Goal**: Replace hardcoded homepage with Wagtail content

**Steps**:
1. Create `BizoholicHomePage` in Wagtail admin
2. Add hero content, features, and services
3. Update `app/page.tsx` to fetch from Wagtail API
4. Replace fallback content with dynamic data

**API Endpoint**: `/api/v2/pages/?type=cms.BizoholicHomePage&fields=*`

### Phase 3: Services Pages
**Goal**: Make all service pages dynamic

**Steps**:
1. Create `ServicePage` entries in Wagtail for each service:
   - AI Campaign Management
   - Content Generation
   - Performance Analytics
   - SEO Optimization
   - Social Media Marketing
   - Email Marketing
   - Creative Design
   - Marketing Automation
   - Strategy Consulting

2. Update service page components to fetch from Wagtail
3. Create a services index page listing all services

**API Endpoint**: `/api/v2/pages/?type=cms.ServicePage&fields=*`

### Phase 4: Blog & Content Pages
**Goal**: Dynamic blog with CMS management

**Steps**:
1. Create `ContentPage` entries for blog posts
2. Update blog listing page to fetch from Wagtail
3. Create dynamic blog post page using slug routing
4. Add pagination and filtering

**API Endpoint**: `/api/v2/pages/?type=cms.ContentPage&fields=*`

### Phase 5: CMS Portal Integration
**Goal**: Embed Wagtail admin in client portal

**Steps**:
1. Create `/portal/dashboard/cms` page
2. Embed Wagtail admin using iframe or API
3. Add CRUD operations for pages
4. Implement permission-based access

## 🔧 Technical Implementation

### 1. Wagtail API Configuration

**File**: `shared/services/cms/config/settings/base.py`

```python
# Enable Wagtail API
INSTALLED_APPS += [
    'wagtail.api.v2',
    'rest_framework',
]

# API Configuration
WAGTAIL_API_BASE_URL = 'http://localhost:8002/api/v2/'

# Allow public read access for published pages
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # For public pages
    ],
}

# CORS for frontend access
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3001',
    'http://localhost:3000',
]
```

### 2. Frontend API Client

**File**: `brands/bizoholic/frontend/lib/wagtail-client.ts`

```typescript
const WAGTAIL_API_URL = process.env.NEXT_PUBLIC_WAGTAIL_URL || 'http://localhost:8002'

export async function getHomePage() {
  const response = await fetch(
    `${WAGTAIL_API_URL}/api/v2/pages/?type=cms.BizoholicHomePage&fields=*`
  )
  if (!response.ok) throw new Error('Failed to fetch homepage')
  const data = await response.json()
  return data.items[0] // Return first (and only) homepage
}

export async function getServices() {
  const response = await fetch(
    `${WAGTAIL_API_URL}/api/v2/pages/?type=cms.ServicePage&fields=*`
  )
  if (!response.ok) throw new Error('Failed to fetch services')
  const data = await response.json()
  return data.items
}

export async function getServiceBySlug(slug: string) {
  const response = await fetch(
    `${WAGTAIL_API_URL}/api/v2/pages/?type=cms.ServicePage&slug=${slug}&fields=*`
  )
  if (!response.ok) throw new Error('Failed to fetch service')
  const data = await response.json()
  return data.items[0]
}

export async function getBlogPosts(page = 1, limit = 10) {
  const response = await fetch(
    `${WAGTAIL_API_URL}/api/v2/pages/?type=cms.ContentPage&fields=*&limit=${limit}&offset=${(page - 1) * limit}`
  )
  if (!response.ok) throw new Error('Failed to fetch blog posts')
  return response.json()
}
```

### 3. Homepage Component Update

**File**: `brands/bizoholic/frontend/app/page.tsx`

```typescript
import { getHomePage, getServices } from '@/lib/wagtail-client'

export default async function HomePage() {
  try {
    const homepage = await getHomePage()
    const services = await getServices()
    
    return (
      <div>
        {/* Hero Section */}
        <section>
          <h1>{homepage.hero_title}</h1>
          <p>{homepage.hero_subtitle}</p>
          <a href={homepage.hero_cta_url}>{homepage.hero_cta_text}</a>
        </section>
        
        {/* Services Section */}
        <section>
          <h2>{homepage.features_title}</h2>
          <div className="grid">
            {services.map(service => (
              <ServiceCard key={service.id} service={service} />
            ))}
          </div>
        </section>
        
        {/* Additional content from StreamField */}
        <StreamFieldRenderer content={homepage.extra_content} />
      </div>
    )
  } catch (error) {
    // Fallback to hardcoded content
    return <FallbackHomePage />
  }
}
```

### 4. CMS Portal Page

**File**: `brands/bizoholic/frontend/app/portal/dashboard/cms/page.tsx`

```typescript
'use client'

import { useAuth } from '@/hooks/use-auth'
import { useEffect, useState } from 'react'

export default function CMSPage() {
  const { user } = useAuth()
  const [pages, setPages] = useState([])
  
  useEffect(() => {
    fetchPages()
  }, [])
  
  async function fetchPages() {
    const response = await fetch('/api/wagtail/pages')
    const data = await response.json()
    setPages(data.items)
  }
  
  return (
    <div>
      <h1>Content Management</h1>
      
      {/* Page List */}
      <div className="page-list">
        {pages.map(page => (
          <PageCard key={page.id} page={page} />
        ))}
      </div>
      
      {/* Create New Page Button */}
      <button onClick={() => createPage()}>
        Create New Page
      </button>
      
      {/* Embedded Wagtail Admin (Optional) */}
      <iframe 
        src="http://localhost:8002/admin/"
        className="w-full h-screen"
      />
    </div>
  )
}
```

## 📋 Content Creation Checklist

### In Wagtail Admin (http://localhost:8002/admin/)

1. **Create Homepage**:
   - Go to Pages → Add child page → Bizoholic Homepage
   - Fill in hero title, subtitle, CTA
   - Add features using StreamField
   - Add stats
   - Publish

2. **Create Service Pages** (9 total):
   For each service:
   - Go to Pages → Add child page → Service Page
   - Title: Service name
   - Service description: Full description
   - Icon: Choose icon name (e.g., "robot", "content", "chart")
   - Category: "AI Marketing", "Content", "Analytics", etc.
   - Featured: Check for top 3 services
   - Add content blocks (features, pricing, testimonials)
   - Publish

3. **Create Blog Posts**:
   - Go to Pages → Add child page → Content Page
   - Fill in author, publish date, featured image
   - Write content using StreamField
   - Add keywords for SEO
   - Publish

4. **Create About Page**:
   - Add child page → Content Page
   - Title: "About Bizoholic"
   - Add company story, team info, mission
   - Publish

5. **Create Pricing Page**:
   - Add child page → Landing Page
   - Add pricing blocks using StreamField
   - Add comparison table
   - Add FAQ section
   - Publish

## 🚀 Deployment Steps

### Step 1: Configure Wagtail API
```bash
# SSH into Wagtail container
docker exec -it bizosaas-wagtail-unified bash

# Update settings
vi /app/config/settings/base.py
# Add API configuration (see above)

# Restart Wagtail
docker restart bizosaas-wagtail-unified
```

### Step 2: Create Initial Content
1. Access Wagtail admin: http://localhost:8002/admin/
2. Login (create superuser if needed)
3. Create pages following checklist above

### Step 3: Update Frontend
1. Create `lib/wagtail-client.ts`
2. Update `app/page.tsx`
3. Update service pages
4. Test locally

### Step 4: Create CMS Portal
1. Create `/portal/dashboard/cms` page
2. Add page management UI
3. Implement CRUD operations
4. Test permissions

## 🧪 Testing Plan

### API Testing:
```bash
# Test homepage API
curl http://localhost:8002/api/v2/pages/?type=cms.BizoholicHomePage

# Test services API
curl http://localhost:8002/api/v2/pages/?type=cms.ServicePage

# Test blog API
curl http://localhost:8002/api/v2/pages/?type=cms.ContentPage
```

### Frontend Testing:
1. Homepage loads with Wagtail content
2. Services page shows dynamic services
3. Blog page lists posts from Wagtail
4. Individual pages load correctly
5. Fallback works if Wagtail is down

### CMS Portal Testing:
1. Can view all pages
2. Can create new pages
3. Can edit existing pages
4. Can delete pages
5. Changes reflect on frontend immediately

## 📝 Next Immediate Actions

1. **Fix Session Issue First** (blocking everything)
   - Debug `/api/auth/me` 401 errors
   - Get login working properly

2. **Configure Wagtail API**
   - Enable public read access
   - Test API endpoints

3. **Create Initial Content**
   - Homepage
   - 3-5 service pages
   - 2-3 blog posts

4. **Update Homepage**
   - Fetch from Wagtail
   - Replace hardcoded services
   - Test fallback

5. **Create CMS Portal Page**
   - Basic page list
   - Link to Wagtail admin
   - Add create/edit buttons

---

**Estimated Timeline**:
- Session fix: 1-2 hours
- Wagtail API config: 30 minutes
- Content creation: 2-3 hours
- Frontend integration: 3-4 hours
- CMS portal: 2-3 hours

**Total**: 1-2 days for full implementation

Let me know when you're ready to proceed with each phase!
