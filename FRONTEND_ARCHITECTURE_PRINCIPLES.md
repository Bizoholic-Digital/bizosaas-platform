# Frontend Architecture Principles

**Date:** November 3, 2025
**Status:** ✅ Confirmed Architecture Pattern

---

## 🎯 CORE PRINCIPLE: PRESENTATION LAYER ONLY

**ALL FRONTENDS ARE PRESENTATION LAYERS**

Frontend applications serve **ONLY** as presentation/UI layers. All content, data, and business logic is dynamically served from respective backend services.

---

## 📊 FRONTEND → BACKEND MAPPING (✅ VERIFIED ON KVM4)

### 1. Business Directory Frontend → Business Directory Backend ✅ DEPLOYED
```
Frontend:  ghcr.io/bizoholic-digital/bizosaas-business-directory:latest
Container: frontend-business-directory (Port 3004)
Backend:   backend-business-directory:8000 (HEALTHY)
API URL:   NEXT_PUBLIC_API_BASE_URL=http://bizosaas-saleor-api-8003:8000
Pattern:   React components fetch business data via REST API
Content:   All business listings, reviews, categories (DYNAMIC)
Status:    ✅ Running 12+ hours, Modular DDD architecture
```

### 2. Bizoholic Frontend → Wagtail CMS Backend ✅ DEPLOYED
```
Frontend:  ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:v3.1.3
Container: frontend-bizoholic-frontend (Port 3001)
Backend:   backend-wagtail-cms:8000 (HEALTHY) + backend-brain-gateway:8001
API URLs:
  - WAGTAIL_API_BASE_URL=http://backend-wagtail-cms:8000/api/v2
  - NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://backend-brain-gateway:8001
  - NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001/api
Pattern:   Next.js fetches CMS content from Wagtail + Brain Gateway APIs
Content:   Marketing pages, blog, services (DYNAMIC from Wagtail CMS)
Status:    ✅ Running 2+ days, Full presentation layer
Site URL:  https://stg.bizoholic.com
```

### 3. Client Portal → Multi-Service Backend ✅ DEPLOYED
```
Frontend:  ghcr.io/bizoholic-digital/bizosaas-client-portal:v1.0.0-foundation-dashboard
Container: frontend-client-portal (Port 3001)
Backends:
  - backend-ai-agents:8002 (HEALTHY)
  - backend-brain-gateway:8001 (HEALTHY)
  - backendservices-authservice:8007 (HEALTHY)
Base Path: /portal
Pattern:   NextAuth + JWT with multiple backend services
Content:   Client dashboards, AI agents, analytics (DYNAMIC per tenant)
Status:    ✅ Running 45+ hours, HEALTHY
Site URL:  https://stg.bizoholic.com/portal
```

### 4. CoreLdove Storefront → Saleor API Backend ⏳ NOT DEPLOYED
```
Frontend:  coreldove-storefront (Port 3002) - PLANNED
Backend:   backend-saleor-api:8000 ✅ RUNNING
API URL:   http://backend-saleor-api:8000/graphql/ (Saleor 3.20)
Pattern:   GraphQL queries for products, cart, checkout
Content:   Product catalog, prices, inventory (DYNAMIC from Saleor)
Status:    Backend ready, frontend not deployed yet
Strategy:  Clone Saleor Next.js storefront template
```

### 5. ThrillRing Gaming → Gaming/Tournament Backend
```
Frontend:  thrillring-gaming (Port 3005)
Backend:   bizosaas-api-gateway:8080/api/gaming/
Pattern:   REST API + WebSocket (Socket.io) for real-time
Content:   Tournaments, leaderboards, matches (DYNAMIC + REAL-TIME)
```

### 6. Analytics Dashboard → Analytics Backend
```
Frontend:  analytics-dashboard (Port 3006)
Backend:   bizosaas-api-gateway:8080/api/analytics/
Pattern:   REST API for metrics, charts data
Content:   Business metrics, reports, KPIs (DYNAMIC from data warehouse)
```

### 7. BizOSaaS Admin → Admin Backend
```
Frontend:  bizosaas-admin (Port 3007)
Backend:   bizosaas-api-gateway:8080/api/admin/
Pattern:   REST API with admin authentication
Content:   Platform settings, user management (DYNAMIC)
```

### 8. CoreLdove Admin → CoreLdove Backend
```
Frontend:  coreldove-admin (Port 3003)
Backend:   bizosaas-coreldove-backend-8003:8003/api/
Pattern:   REST API for store configuration
Content:   Store setup, product import wizards (DYNAMIC)
```

---

## 🏗️ ARCHITECTURAL LAYERS

### 3-Tier Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  (Next.js 15 Frontends - React 19 - TypeScript - Tailwind)  │
│                                                             │
│  • Bizoholic Frontend        • Client Portal                │
│  • Business Directory ✅    • ThrillRing Gaming            │
│  • CoreLdove Storefront      • Analytics Dashboard          │
│  • CoreLdove Admin           • BizOSaaS Admin               │
│                                                             │
│  Responsibilities:                                          │
│  - Render UI components                                     │
│  - Handle user interactions                                 │
│  - Client-side routing                                      │
│  - Form validation (presentation)                           │
│  - State management (UI state only)                         │
│  - API calls to backend                                     │
└─────────────────────────────────────────────────────────────┘
                              ▼
                    (HTTP/HTTPS - REST/GraphQL)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     BUSINESS LOGIC LAYER                    │
│      (Django/FastAPI Backends - Python - PostgreSQL)        │
│                                                             │
│  • Saleor API (8003)         • Brain API (8000)             │
│  • CoreLdove Backend (8003)  • API Gateway (8080)           │
│  • Client Service            • Gaming Service               │
│  • Analytics Service         • Admin Service                │
│                                                             │
│  Responsibilities:                                          │
│  - Business rules and logic                                 │
│  - Data validation                                          │
│  - Authentication/Authorization                             │
│  - API endpoints                                            │
│  - Workflow orchestration                                   │
│  - Integration with external services                       │
└─────────────────────────────────────────────────────────────┘
                              ▼
                      (PostgreSQL Protocol)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       DATA LAYER                            │
│         (PostgreSQL - Redis - MinIO - n8n)                  │
│                                                             │
│  • shared_postgres (5432)    • shared_redis (6379)          │
│  • shared_minio (9000)       • shared_n8n (5678)            │
│                                                             │
│  Responsibilities:                                          │
│  - Data persistence                                         │
│  - Caching                                                  │
│  - File storage                                             │
│  - Workflow automation                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ WHAT FRONTENDS SHOULD DO

### ✅ Allowed Responsibilities

1. **UI Rendering**
   - Display data received from backend APIs
   - Render React components
   - Handle responsive layouts
   - Manage themes and styling

2. **User Interactions**
   - Handle form inputs
   - Validate format (client-side for UX)
   - Manage UI state (modals, tabs, etc.)
   - Handle navigation

3. **API Communication**
   - Fetch data from backend APIs
   - Send user actions to backend
   - Handle loading/error states
   - Cache API responses (client-side)

4. **Client-Side State**
   - UI state (sidebar open/closed)
   - Form state (draft data)
   - Temporary selections
   - Client-side filters/sorting

---

## ❌ WHAT FRONTENDS SHOULD NOT DO

### ❌ Prohibited Responsibilities

1. **❌ Business Logic**
   - Pricing calculations
   - Inventory management
   - Order processing
   - Payment processing

2. **❌ Data Storage**
   - No direct database connections
   - No hardcoded content/data
   - No persistent storage (except auth tokens)

3. **❌ Authentication Logic**
   - No password hashing
   - No session management (backend handles)
   - Only store/forward JWT tokens

4. **❌ Authorization**
   - No role-based access control logic
   - Backend determines permissions
   - Frontend only hides/shows UI based on backend response

---

## 🔄 DATA FLOW PATTERN

### Example: Business Directory Search

```typescript
// ✅ CORRECT: Frontend as Presentation Layer

// Frontend (React Component)
export default function BusinessSearch() {
  const [results, setResults] = useState<Business[]>([])
  const [loading, setLoading] = useState(false)

  const handleSearch = async (query: string) => {
    setLoading(true)
    try {
      // Fetch from backend API
      const response = await fetch(
        `${API_BASE_URL}/api/brain/business-directory/search?query=${query}`
      )
      const data = await response.json()

      // Display data received from backend
      setResults(data.businesses)
    } catch (error) {
      console.error('Search failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <SearchInput onSearch={handleSearch} />
      {loading ? <LoadingSpinner /> : <BusinessList businesses={results} />}
    </div>
  )
}

// Backend (Django API)
@api_view(['GET'])
def search_businesses(request):
    query = request.GET.get('query', '')
    location = request.GET.get('location', '')

    # Business logic executed on backend
    businesses = Business.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        location__icontains=location,
        is_active=True
    ).select_related('category').prefetch_related('reviews')

    # Apply business rules
    for business in businesses:
        business.is_premium = check_premium_status(business)
        business.rating = calculate_average_rating(business.reviews.all())

    # Serialize and return
    serializer = BusinessSerializer(businesses, many=True)
    return Response({'businesses': serializer.data})
```

### Example: CoreLdove Product Catalog

```typescript
// ✅ CORRECT: Saleor GraphQL Query

// Frontend (React Component)
'use client'

import { graphql } from '@/gql'
import { useQuery } from '@apollo/client'

const GET_PRODUCTS = graphql(`
  query GetProducts($channel: String!, $first: Int!) {
    products(channel: $channel, first: $first) {
      edges {
        node {
          id
          name
          description
          pricing {
            priceRange {
              start {
                gross {
                  amount
                  currency
                }
              }
            }
          }
          thumbnail {
            url
          }
        }
      }
    }
  }
`)

export default function ProductCatalog() {
  const { data, loading } = useQuery(GET_PRODUCTS, {
    variables: { channel: 'default-channel', first: 20 }
  })

  if (loading) return <LoadingSkeleton />

  return (
    <div className="grid grid-cols-4 gap-4">
      {data?.products.edges.map(({ node: product }) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}

// Backend (Saleor GraphQL API)
// Handles:
// - Product queries from database
// - Pricing calculations based on channel, discounts, taxes
// - Inventory availability
// - Image optimization
// - Authorization (public vs authenticated pricing)
```

---

## 🎯 MIGRATION FOCUS AREAS

When migrating frontends to modular DDD, ensure:

### 1. API Client Layer (lib/api/)
```typescript
// lib/api/client.ts
export const apiClient = {
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,

  async get(endpoint: string) {
    const response = await fetch(`${this.baseURL}${endpoint}`)
    return response.json()
  },

  async post(endpoint: string, data: any) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    return response.json()
  }
}
```

### 2. Type Definitions (lib/types/)
```typescript
// lib/types/business.ts
// Types match backend API responses exactly

export interface Business {
  id: string
  name: string
  description: string
  category: Category
  rating: number      // Calculated by backend
  is_premium: boolean // Determined by backend
  reviews: Review[]
}
```

### 3. React Query Hooks (lib/hooks/)
```typescript
// lib/hooks/useBusinessSearch.ts
import { useQuery } from '@tanstack/react-query'
import { businessAPI } from '@/lib/api'

export function useBusinessSearch(query: string) {
  return useQuery({
    queryKey: ['businesses', 'search', query],
    queryFn: () => businessAPI.searchBusinesses({ query }),
    enabled: query.length > 0
  })
}
```

### 4. UI Components (lib/ui/)
```typescript
// lib/ui/components/business-card.tsx
// Pure presentation component

interface BusinessCardProps {
  business: Business // Data from backend
}

export function BusinessCard({ business }: BusinessCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{business.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <p>{business.description}</p>
        <div className="flex items-center">
          <StarRating rating={business.rating} />
          {business.is_premium && <Badge>Premium</Badge>}
        </div>
      </CardContent>
    </Card>
  )
}
```

---

## 📋 ENVIRONMENT VARIABLES PATTERN

Each frontend connects to its backend via environment variables:

```env
# Business Directory
NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-api:8000

# CoreLdove Storefront
NEXT_PUBLIC_SALEOR_API_URL=http://bizosaas-saleor-api-8003:8000/graphql/
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...

# Bizoholic Frontend
NEXT_PUBLIC_CMS_API_URL=http://bizosaas-api-gateway:8080/api/bizoholic/

# Client Portal
NEXT_PUBLIC_API_URL=http://bizosaas-api-gateway:8080/api/clients/
NEXT_PUBLIC_WS_URL=ws://bizosaas-api-gateway:8080/ws/

# ThrillRing Gaming
NEXT_PUBLIC_API_URL=http://bizosaas-api-gateway:8080/api/gaming/
NEXT_PUBLIC_SOCKET_URL=http://bizosaas-api-gateway:8080

# Analytics Dashboard
NEXT_PUBLIC_ANALYTICS_API_URL=http://bizosaas-api-gateway:8080/api/analytics/

# BizOSaaS Admin
NEXT_PUBLIC_ADMIN_API_URL=http://bizosaas-api-gateway:8080/api/admin/

# CoreLdove Admin
NEXT_PUBLIC_API_URL=http://bizosaas-coreldove-backend-8003:8003/api/
```

---

## ✅ MIGRATION CHECKLIST (Updated)

For each frontend migration:

- [ ] **No hardcoded content** - All data fetched from backend
- [ ] **API client configured** - Environment variables set
- [ ] **Type definitions** - Match backend API schemas
- [ ] **React Query setup** - Efficient data fetching/caching
- [ ] **Loading states** - Handle async data gracefully
- [ ] **Error handling** - Display backend errors properly
- [ ] **Authentication** - JWT tokens passed to backend
- [ ] **No business logic** - Pure presentation components
- [ ] **lib/ structure** - Self-contained modular architecture
- [ ] **Docker build** - Standalone container
- [ ] **Environment tested** - Backend connection verified

---

## 🚀 NEXT STEPS (Updated Approach)

### Priority 1: CoreLdove Storefront
✅ Uses Saleor GraphQL API (already dynamic)
✅ No hardcoded content
✅ Product data from Saleor backend

### Priority 2: Bizoholic Frontend
🔍 **VERIFY:** Does it fetch content from CMS/API or is content hardcoded?
📝 **ACTION:** If hardcoded, need to create/integrate CMS backend first

### Priority 3: Other Frontends
Each needs verification that backend API exists and is serving dynamic content.

---

**Architecture:** Presentation Layer Only (Dynamic Content from Backends)
**Pattern:** API-Driven, No Business Logic in Frontend
**Deployment:** Stateless Containers (No Data Persistence)
