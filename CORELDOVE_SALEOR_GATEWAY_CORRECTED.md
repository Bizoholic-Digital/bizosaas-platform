# CoreLdove Saleor Storefront - CORRECTED Architecture

**Date:** November 3, 2025
**Status:** ✅ Architecture Corrected - ALL Requests Through Brain Gateway
**Critical:** Saleor GraphQL routed through FastAPI CrewAI Brain Gateway

---

## 🚨 CRITICAL CORRECTION

**ALL frontends route through the Brain Gateway - no direct backend connections!**

```
CoreLdove Storefront → Brain Gateway → Saleor API
(Not: CoreLdove → Saleor directly)
```

---

## ✅ CORRECTED ENVIRONMENT CONFIGURATION

```env
# 🚨 PRIMARY ENDPOINT - Brain Gateway (ONLY ONE NEEDED)
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001

# Saleor GraphQL endpoint (proxied through gateway)
NEXT_PUBLIC_SALEOR_GRAPHQL_ENDPOINT=/api/saleor/graphql

# Storefront Configuration
NEXT_PUBLIC_STOREFRONT_NAME=CoreLdove
NEXT_PUBLIC_SALEOR_CHANNEL=default-channel

# Payment (frontend-only, not proxied)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...

# Deployment
BASE_PATH=/store
NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/store

# Feature Flags
NEXT_PUBLIC_ENABLE_ACCOUNT=true
NEXT_PUBLIC_ENABLE_CHECKOUT=true
```

---

## 🔧 SALEOR GRAPHQL CLIENT CONFIGURATION

### Update Saleor's Apollo Client

The official Saleor storefront uses Apollo Client. We need to configure it to use the Brain Gateway:

```typescript
// src/lib/graphql/client.ts (or wherever Saleor initializes Apollo)
import { ApolloClient, InMemoryCache, HttpLink } from '@apollo/client'

const httpLink = new HttpLink({
  // 🚨 CRITICAL: Use Brain Gateway, not direct Saleor URL
  uri: `${process.env.NEXT_PUBLIC_API_BASE_URL}${process.env.NEXT_PUBLIC_SALEOR_GRAPHQL_ENDPOINT}`,
  // Result: http://backend-brain-gateway:8001/api/saleor/graphql
})

const client = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
  headers: {
    'Content-Type': 'application/json',
  },
})

export default client
```

---

## 🧠 BRAIN GATEWAY SALEOR PROXY ROUTE

The Brain Gateway needs this route to proxy GraphQL to Saleor:

```python
# brain-gateway/app/routes/saleor.py

from fastapi import APIRouter, Request, Response
from httpx import AsyncClient
import logging

router = APIRouter(prefix="/api/saleor", tags=["saleor"])
logger = logging.getLogger(__name__)

@router.post("/graphql")
@router.get("/graphql")  # Some Saleor queries use GET
async def saleor_graphql_proxy(request: Request):
    """
    Proxy all GraphQL requests to Saleor API backend

    Frontend: /api/saleor/graphql
    Backend:  http://backend-saleor-api:8000/graphql/
    """
    try:
        # Get request body
        if request.method == "POST":
            body = await request.json()
        else:
            body = None

        # Forward to Saleor backend
        async with AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=request.method,
                url="http://backend-saleor-api:8000/graphql/",
                json=body if request.method == "POST" else None,
                params=dict(request.query_params) if request.method == "GET" else None,
                headers={
                    "Content-Type": "application/json",
                    # Forward auth headers if present
                    "Authorization": request.headers.get("Authorization", ""),
                },
            )

            logger.info(f"Saleor GraphQL: {request.method} → {response.status_code}")

            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
            )

    except Exception as e:
        logger.error(f"Saleor GraphQL proxy error: {e}")
        return {"error": "GraphQL proxy failed", "detail": str(e)}
```

---

## 📋 DEPLOYMENT CHECKLIST (Corrected)

### Pre-Deployment

- [ ] Brain Gateway has `/api/saleor/graphql` route
- [ ] Test route: `curl http://backend-brain-gateway:8001/api/saleor/graphql -d '{"query":"{ __schema { types { name } } }"}'`
- [ ] Saleor backend is running on port 8000
- [ ] PostgreSQL database is accessible to Saleor

### Frontend Configuration

- [ ] Remove any `NEXT_PUBLIC_SALEOR_API_URL` (direct connection)
- [ ] Set `NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001`
- [ ] Set `NEXT_PUBLIC_SALEOR_GRAPHQL_ENDPOINT=/api/saleor/graphql`
- [ ] Update GraphQL client to use gateway URL
- [ ] Test GraphQL queries flow through gateway

### Docker Build

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/coreldove-storefront

# Build with corrected environment
docker build -f Dockerfile.production \
  -t ghcr.io/bizoholic-digital/coreldove-storefront:latest \
  --build-arg NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001 \
  --build-arg NEXT_PUBLIC_SALEOR_GRAPHQL_ENDPOINT=/api/saleor/graphql \
  .

# Push to registry
docker push ghcr.io/bizoholic-digital/coreldove-storefront:latest
```

### Dokploy Deployment

```
Application: coreldove-storefront
Image:       ghcr.io/bizoholic-digital/coreldove-storefront:latest
Port:        3002

Environment Variables:
  NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001
  NEXT_PUBLIC_SALEOR_GRAPHQL_ENDPOINT=/api/saleor/graphql
  NEXT_PUBLIC_STOREFRONT_NAME=CoreLdove
  NEXT_PUBLIC_SALEOR_CHANNEL=default-channel
  BASE_PATH=/store
  NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/store
```

---

## 🔍 VERIFICATION STEPS

### 1. Test Brain Gateway Route
```bash
# SSH to KVM4
ssh root@72.60.219.244

# Test Saleor GraphQL through gateway
docker exec backend-brain-gateway.1.m43ufno3d1iidhd5m3cas3zmg \
  curl -X POST http://localhost:8001/api/saleor/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ shop { name description } }"}'
```

### 2. Test from Frontend Container
```bash
# Once deployed, test from frontend
docker exec coreldove-storefront \
  curl http://backend-brain-gateway:8001/api/saleor/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ products(first: 5) { edges { node { id name } } } }"}'
```

### 3. Browser DevTools Check
```javascript
// In browser console on https://stg.bizoholic.com/store
// Check network tab - all GraphQL requests should go to:
// http://backend-brain-gateway:8001/api/saleor/graphql
// NOT to backend-saleor-api:8000
```

---

## ✅ BENEFITS OF GATEWAY ROUTING

1. **Centralized Auth** - Brain Gateway validates JWT before forwarding
2. **Rate Limiting** - Protect Saleor from abuse
3. **Logging** - All API calls logged in one place
4. **AI Enhancement** - CrewAI can intercept/enhance product searches
5. **Caching** - Gateway can cache frequent queries
6. **Monitoring** - Single point for metrics
7. **Security** - Saleor backend not directly exposed
8. **Flexibility** - Easy to swap Saleor for another e-commerce backend

---

## 🎯 SUMMARY

**Old (WRONG):**
```
CoreLdove Storefront → backend-saleor-api:8000/graphql/ ❌
```

**New (CORRECT):**
```
CoreLdove Storefront → backend-brain-gateway:8001/api/saleor/graphql → backend-saleor-api:8000/graphql/ ✅
```

**Key Points:**
- ✅ ALL frontends use Brain Gateway
- ✅ NO direct backend connections
- ✅ Gateway proxies GraphQL to Saleor
- ✅ Maintains full Saleor functionality
- ✅ Follows centralized architecture

---

**Next Steps:**
1. Verify Brain Gateway has Saleor proxy route
2. Clone Saleor storefront
3. Configure with gateway endpoint
4. Build and deploy
5. Test GraphQL queries through gateway

**Documentation:**
- [CENTRALIZED_API_GATEWAY_ARCHITECTURE.md](CENTRALIZED_API_GATEWAY_ARCHITECTURE.md)
- [SALEOR_FRONTEND_MODULAR_DDD_ANALYSIS.md](SALEOR_FRONTEND_MODULAR_DDD_ANALYSIS.md)
