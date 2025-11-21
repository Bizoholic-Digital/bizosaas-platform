# Centralized API Gateway Architecture - CORRECTED

**Date:** November 3, 2025
**Status:** ✅ **CRITICAL ARCHITECTURE CLARIFICATION**
**Pattern:** ALL Frontends → FastAPI CrewAI Brain Gateway → Backend Services

---

## 🎯 CORE PRINCIPLE: CENTRALIZED API GATEWAY

**ALL FRONTENDS MUST ROUTE THROUGH THE API GATEWAY**

No frontend directly connects to backend services. All API calls go through the **FastAPI CrewAI AI Agents Brain Gateway** which routes to appropriate backend services.

---

## ✅ CORRECT ARCHITECTURE

### Single Entry Point Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│         (Next.js 15 Frontends - Port 3000-3007)             │
│                                                             │
│  1. Bizoholic Frontend (3001)                               │
│  2. Business Directory (3004)                               │
│  3. Client Portal (3001/portal)                             │
│  4. CoreLdove Storefront (3002) ← NEW                       │
│  5. CoreLdove Admin (3003)                                  │
│  6. ThrillRing Gaming (3005)                                │
│  7. Analytics Dashboard (3006)                              │
│  8. BizOSaaS Admin (3007)                                   │
│                                                             │
│  ALL use SINGLE environment variable:                       │
│  NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001 │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    (HTTP/HTTPS - REST/GraphQL)
                              ↓
┌─────────────────────────────────────────────────────────────┐
│      🧠 FastAPI CrewAI AI Agents Brain Gateway (8001)       │
│              CENTRALIZED API GATEWAY LAYER                  │
│                                                             │
│  Responsibilities:                                          │
│  • Route requests to correct backend services               │
│  • Authentication & Authorization (JWT)                     │
│  • Rate limiting & throttling                               │
│  • Request/Response transformation                          │
│  • API versioning                                           │
│  • Logging & monitoring                                     │
│  • AI Agent orchestration (CrewAI)                          │
│  • GraphQL proxy for Saleor                                 │
│                                                             │
│  Routes:                                                    │
│  /api/brain/*           → Business Directory Backend        │
│  /api/saleor/*          → Saleor API (GraphQL proxy)        │
│  /api/cms/*             → Wagtail CMS                       │
│  /api/clients/*         → Client Portal APIs                │
│  /api/ai-agents/*       → AI Agents Service                 │
│  /api/crm/*             → Django CRM                        │
│  /api/auth/*            → Auth Service                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────┬─────────────┬─────────────┬──────────┐
        ↓             ↓             ↓             ↓          ↓
┌──────────────┐ ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌─────────┐
│ Saleor API   │ │ Wagtail  │ │Business │ │ Django   │ │   AI    │
│   (8000)     │ │   CMS    │ │Directory│ │   CRM    │ │ Agents  │
│              │ │  (4000)  │ │ (8000)  │ │  (8003)  │ │ (8002)  │
└──────────────┘ └──────────┘ └─────────┘ └──────────┘ └─────────┘
                              ↓
                    ┌──────────────────┐
                    │  PostgreSQL      │
                    │  Redis           │
                    │  MinIO           │
                    └──────────────────┘
```

---

## 🔄 REQUEST FLOW EXAMPLES

### Example 1: CoreLdove Product Catalog

```
User → CoreLdove Storefront (Port 3002)
  ↓
  Frontend makes request:
  fetch('http://backend-brain-gateway:8001/api/saleor/graphql', {
    query: `{ products { edges { node { id name price } } } }`
  })
  ↓
  Brain Gateway (Port 8001) receives request
  ↓
  Gateway routes to: backend-saleor-api:8000/graphql/
  ↓
  Saleor API queries database
  ↓
  Returns data to Gateway
  ↓
  Gateway returns to Frontend
  ↓
  User sees products
```

### Example 2: Business Directory Search

```
User → Business Directory (Port 3004)
  ↓
  Frontend makes request:
  fetch('http://backend-brain-gateway:8001/api/brain/business-directory/search?query=pizza')
  ↓
  Brain Gateway (Port 8001) receives request
  ↓
  Gateway routes to: backend-business-directory:8000/search
  ↓
  Business Directory Backend queries database
  ↓
  Returns results to Gateway
  ↓
  Gateway returns to Frontend
  ↓
  User sees search results
```

### Example 3: Bizoholic CMS Content

```
User → Bizoholic Frontend (Port 3001)
  ↓
  Frontend makes request:
  fetch('http://backend-brain-gateway:8001/api/cms/pages/home')
  ↓
  Brain Gateway (Port 8001) receives request
  ↓
  Gateway routes to: backend-wagtail-cms:4000/api/v2/pages
  ↓
  Wagtail CMS fetches page content
  ↓
  Returns content to Gateway
  ↓
  Gateway returns to Frontend
  ↓
  User sees homepage
```

---

## 📋 VERIFIED DEPLOYMENTS (Corrected)

### ✅ Already Using API Gateway Correctly

#### 1. Bizoholic Frontend
```env
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://backend-brain-gateway:8001
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001/api
WAGTAIL_API_BASE_URL=http://backend-wagtail-cms:8000/api/v2  ← ❌ WRONG!
```

**Fix Needed:** Remove direct Wagtail connection, use Gateway route instead:
```env
# CORRECT
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001
# All CMS calls: /api/cms/*
# Gateway proxies to Wagtail
```

#### 2. Business Directory
```env
NEXT_PUBLIC_API_BASE_URL=http://bizosaas-saleor-api-8003:8000  ← ❌ WRONG!
```

**Fix Needed:**
```env
# CORRECT
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001
# All business searches: /api/brain/business-directory/*
```

#### 3. Client Portal ✅ CORRECT
```env
# Already correct - no direct backend URLs shown
```

---

## 🚨 CRITICAL FIX: CoreLdove Storefront

### ❌ WRONG Approach (Direct to Saleor):
```env
# DON'T DO THIS:
NEXT_PUBLIC_SALEOR_API_URL=http://backend-saleor-api:8000/graphql/
```

### ✅ CORRECT Approach (Through Gateway):
```env
# CORRECT - All through Brain Gateway:
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001
NEXT_PUBLIC_SALEOR_GRAPHQL_ENDPOINT=/api/saleor/graphql
```

**GraphQL Client Configuration:**
```typescript
// src/lib/graphql/client.ts
import { ApolloClient, InMemoryCache } from '@apollo/client'

const client = new ApolloClient({
  uri: `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/saleor/graphql`,
  // NOT: process.env.NEXT_PUBLIC_SALEOR_API_URL
  cache: new InMemoryCache(),
  headers: {
    'Content-Type': 'application/json',
  },
})

export default client
```

---

## 🔧 BRAIN GATEWAY ROUTES (Required)

The Brain Gateway (FastAPI) needs these routes configured:

```python
# backend/brain-gateway/app/routes.py

from fastapi import APIRouter, Request
from httpx import AsyncClient

router = APIRouter()

# Saleor GraphQL Proxy
@router.post("/api/saleor/graphql")
async def saleor_graphql_proxy(request: Request):
    """
    Proxy GraphQL requests to Saleor API
    """
    body = await request.json()

    async with AsyncClient() as client:
        response = await client.post(
            "http://backend-saleor-api:8000/graphql/",
            json=body,
            headers={"Content-Type": "application/json"}
        )
        return response.json()

# Business Directory Proxy
@router.get("/api/brain/business-directory/search")
async def business_search_proxy(query: str, location: str = None):
    """
    Proxy business directory searches
    """
    params = {"query": query}
    if location:
        params["location"] = location

    async with AsyncClient() as client:
        response = await client.get(
            "http://backend-business-directory:8000/search",
            params=params
        )
        return response.json()

# Wagtail CMS Proxy
@router.get("/api/cms/{path:path}")
async def cms_proxy(path: str):
    """
    Proxy CMS requests to Wagtail
    """
    async with AsyncClient() as client:
        response = await client.get(
            f"http://backend-wagtail-cms:4000/api/v2/{path}"
        )
        return response.json()

# Auth Service
@router.post("/api/auth/login")
async def auth_login_proxy(request: Request):
    async with AsyncClient() as client:
        response = await client.post(
            "http://backendservices-authservice:8007/login",
            json=await request.json()
        )
        return response.json()
```

---

## 📊 ENVIRONMENT VARIABLES (Corrected for ALL Frontends)

### Standard Pattern (All Frontends)

```env
# PRIMARY API ENDPOINT (Only one needed!)
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001

# Optional: WebSocket for real-time features
NEXT_PUBLIC_WS_URL=ws://backend-brain-gateway:8001/ws

# Optional: Auth configuration
JWT_SECRET=*** (handled by gateway)
NEXTAUTH_URL=https://stg.bizoholic.com

# NO DIRECT BACKEND URLs NEEDED!
# ❌ Don't add: NEXT_PUBLIC_SALEOR_API_URL
# ❌ Don't add: WAGTAIL_API_BASE_URL
# ❌ Don't add: NEXT_PUBLIC_BUSINESS_API_URL
```

### CoreLdove Storefront Specific

```env
# Gateway endpoint
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001

# Saleor-specific configs (routing within gateway)
NEXT_PUBLIC_STOREFRONT_NAME=CoreLdove
NEXT_PUBLIC_SALEOR_CHANNEL=default-channel

# Stripe (frontend-only, not proxied)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...

# Base path for deployment
BASE_PATH=/store
NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/store
```

---

## ✅ BENEFITS OF API GATEWAY PATTERN

1. **Single Entry Point** - One URL to manage
2. **Centralized Auth** - JWT validation in one place
3. **Rate Limiting** - Protect backend services
4. **Request Logging** - Monitor all API traffic
5. **API Versioning** - Easy to version (/api/v1/, /api/v2/)
6. **Service Discovery** - Frontends don't need backend URLs
7. **Load Balancing** - Gateway can distribute load
8. **AI Integration** - CrewAI agents can intercept/enhance requests
9. **Security** - Backends not directly exposed
10. **Flexibility** - Easy to swap backend implementations

---

## 🚀 UPDATED DEPLOYMENT CHECKLIST

For each frontend deployment:

- [ ] Environment variable: `NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001`
- [ ] **NO** direct backend URLs (no Saleor, Wagtail, etc. URLs)
- [ ] API calls use `/api/{service}/{endpoint}` pattern
- [ ] Gateway routes configured for that service
- [ ] JWT tokens passed via headers (gateway validates)
- [ ] WebSocket connections (if needed) through gateway
- [ ] Test API calls flow through gateway (check logs)

---

## 📝 MIGRATION ACTIONS REQUIRED

### Immediate Fixes Needed:

1. **Bizoholic Frontend** - Remove direct Wagtail URL
   ```bash
   # Update env vars in Dokploy:
   - Remove: WAGTAIL_API_BASE_URL=http://backend-wagtail-cms:8000/api/v2
   + Use:    NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001
   # Update code to call /api/cms/* instead of direct Wagtail
   ```

2. **Business Directory** - Route through gateway
   ```bash
   # Update env vars:
   - Remove: NEXT_PUBLIC_API_BASE_URL=http://bizosaas-saleor-api-8003:8000
   + Use:    NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001
   # Update API calls to /api/brain/business-directory/*
   ```

3. **CoreLdove Storefront** - Configure GraphQL proxy
   ```bash
   # Setup:
   NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001
   # GraphQL endpoint: /api/saleor/graphql (proxied by gateway)
   ```

4. **Brain Gateway** - Add missing routes
   - Ensure Saleor GraphQL proxy exists
   - Ensure Business Directory proxy exists
   - Ensure Wagtail CMS proxy exists
   - Test all routes

---

## 🔍 VERIFICATION COMMANDS

### Check Gateway is Running
```bash
ssh root@72.60.219.244
docker ps | grep brain-gateway
# Should show: backend-brain-gateway (port 8001)
```

### Test Gateway Routes
```bash
# From inside a frontend container:
curl http://backend-brain-gateway:8001/health
curl http://backend-brain-gateway:8001/api/saleor/graphql -d '{"query": "{ __schema { types { name } } }"}'
curl http://backend-brain-gateway:8001/api/brain/business-directory/search?query=test
curl http://backend-brain-gateway:8001/api/cms/pages
```

---

## 🎯 SUMMARY

**Old (Wrong) Pattern:**
```
Frontend → Direct Backend Connection ❌
```

**New (Correct) Pattern:**
```
Frontend → Brain Gateway → Backend Services ✅
```

**Key Change:**
- **Single environment variable** for all frontends
- **Centralized routing** through Brain Gateway
- **No direct backend access** from frontends
- **Easier to manage** and monitor

---

**Architecture:** Centralized API Gateway (Brain Gateway)
**Entry Point:** ALL requests → http://backend-brain-gateway:8001
**Pattern:** Gateway routes to backends based on path (/api/{service}/*)
**Deployment:** ALL frontends use same NEXT_PUBLIC_API_BASE_URL
