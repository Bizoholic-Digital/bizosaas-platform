# Architecture Clarification Summary - November 3, 2025

## 🎯 CRITICAL CLARIFICATION RECEIVED

**Your Guidance:** "The backend and frontend should be all routing through the fastapi centralized crewai ai agents api gateway and not directly integrating the frontend and the backend."

**Impact:** This changes the entire approach for CoreLdove Storefront and requires verification/correction of existing deployments.

---

## ✅ CORRECTED ARCHITECTURE

### ALL Frontends → Brain Gateway → Backend Services

```
NO DIRECT CONNECTIONS ALLOWED

Frontend A ──┐
Frontend B ──┤
Frontend C ──┼──→ Brain Gateway (8001) ──→ Backend Services
Frontend D ──┤
Frontend E ──┘
```

---

## 📋 STATUS OF DEPLOYED FRONTENDS

### 1. Business Directory (Port 3004) - ⚠️ NEEDS FIX
**Current Config:**
```env
NEXT_PUBLIC_API_BASE_URL=http://bizosaas-saleor-api-8003:8000  ← ❌ WRONG!
```

**Should Be:**
```env
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001
# Calls: /api/brain/business-directory/*
```

**Action Required:** Update environment variable in Dokploy, redeploy

---

### 2. Bizoholic Frontend (Port 3001) - ⚠️ PARTIALLY CORRECT
**Current Config:**
```env
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://backend-brain-gateway:8001  ✅ Good
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001/api  ✅ Good
WAGTAIL_API_BASE_URL=http://backend-wagtail-cms:8000/api/v2     ❌ WRONG!
```

**Should Be:**
```env
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001
# All CMS calls: /api/cms/* (gateway proxies to Wagtail)
```

**Action Required:** Remove direct Wagtail URL, ensure Brain Gateway has CMS proxy route

---

### 3. Client Portal (Port 3001/portal) - ✅ APPEARS CORRECT
**Current Config:**
- No direct backend URLs visible in env vars
- Likely already using Brain Gateway

**Action Required:** Verify API calls go through gateway

---

### 4. CoreLdove Storefront (Not Deployed) - ✅ WILL BE CORRECT
**Planned Config:**
```env
NEXT_PUBLIC_API_BASE_URL=http://backend-brain-gateway:8001
NEXT_PUBLIC_SALEOR_GRAPHQL_ENDPOINT=/api/saleor/graphql
```

**Requirements:**
1. Brain Gateway needs `/api/saleor/graphql` proxy route
2. Saleor GraphQL client configured to use gateway
3. No direct `NEXT_PUBLIC_SALEOR_API_URL`

---

## 🔧 BRAIN GATEWAY REQUIRED ROUTES

The Brain Gateway (FastAPI) must have these proxy routes:

```python
# /api/saleor/graphql       → backend-saleor-api:8000/graphql/
# /api/cms/*                → backend-wagtail-cms:4000/api/v2/*
# /api/brain/*              → backend-business-directory:8000/*
# /api/clients/*            → Client Portal backend APIs
# /api/ai-agents/*          → backend-ai-agents:8002/*
# /api/crm/*                → backend-django-crm:8003/*
# /api/auth/*               → backendservices-authservice:8007/*
```

---

## 📊 RECOMMENDED APPROACH FOR CORELDOVE

### ✅ YES - Use Saleor's Structure (Confirmed)

**Your Question:** "Should we be following the same or similar approach if that is the recommended for coreldove as we are going to be using the saleor's official nextjs frontend?"

**Answer:** **YES** - Use Saleor's architecture AS-IS with these modifications:

1. ✅ **Keep Saleor's `src/lib/` structure** (already modular DDD)
2. ✅ **Add our standard Dockerfile** (multi-stage build)
3. ✅ **Configure GraphQL client** to use Brain Gateway
4. ✅ **Environment variables** point to gateway (not direct Saleor)
5. ✅ **CoreLdove branding** (logo, colors, metadata)

### Key Configuration Change

```typescript
// Saleor's default:
const client = new ApolloClient({
  uri: process.env.NEXT_PUBLIC_SALEOR_API_URL  // ❌ Direct to Saleor
})

// Our configuration:
const client = new ApolloClient({
  uri: `${process.env.NEXT_PUBLIC_API_BASE_URL}${process.env.NEXT_PUBLIC_SALEOR_GRAPHQL_ENDPOINT}`
  // ✅ Result: http://backend-brain-gateway:8001/api/saleor/graphql
})
```

---

## 🎯 BENEFITS OF CENTRALIZED GATEWAY

### Why This Architecture?

1. **Single Entry Point** - One URL for all frontends
2. **CrewAI Integration** - AI agents can enhance/intercept requests
3. **Centralized Auth** - JWT validation in one place
4. **Rate Limiting** - Protect backends from abuse
5. **Logging & Monitoring** - Single point for observability
6. **API Versioning** - Easy to version (/api/v1/, /api/v2/)
7. **Security** - Backends not directly exposed to frontends
8. **Flexibility** - Easy to swap backend implementations

### AI Agent Enhancement Example

```python
# Brain Gateway can enhance product searches with AI
@router.post("/api/saleor/graphql")
async def saleor_with_ai_enhancement(request: Request):
    body = await request.json()

    # If it's a product search, enhance with AI recommendations
    if "searchProducts" in body.get("query", ""):
        # CrewAI can analyze user preferences and enhance results
        enhanced_query = await ai_agent.enhance_search(body)
        body = enhanced_query

    # Forward to Saleor
    response = await saleor_backend.query(body)
    return response
```

---

## 📝 NEXT STEPS

### Immediate Actions

1. **Verify Brain Gateway Routes**
   ```bash
   ssh root@72.60.219.244
   docker exec backend-brain-gateway.1.* curl http://localhost:8001/api/saleor/graphql
   ```

2. **Fix Business Directory**
   - Update env var to use Brain Gateway
   - Ensure `/api/brain/*` routes exist

3. **Fix Bizoholic Frontend**
   - Remove direct Wagtail URL
   - Ensure `/api/cms/*` routes exist

4. **Deploy CoreLdove**
   - Clone Saleor storefront
   - Configure with gateway endpoints
   - Test GraphQL through gateway

---

## 📚 UPDATED DOCUMENTATION

Created/Updated Documents:

1. ✅ [CENTRALIZED_API_GATEWAY_ARCHITECTURE.md](CENTRALIZED_API_GATEWAY_ARCHITECTURE.md) - Gateway pattern
2. ✅ [SALEOR_FRONTEND_MODULAR_DDD_ANALYSIS.md](SALEOR_FRONTEND_MODULAR_DDD_ANALYSIS.md) - Saleor compatibility
3. ✅ [CORELDOVE_SALEOR_GATEWAY_CORRECTED.md](CORELDOVE_SALEOR_GATEWAY_CORRECTED.md) - Corrected config
4. ✅ [FRONTEND_ARCHITECTURE_PRINCIPLES.md](FRONTEND_ARCHITECTURE_PRINCIPLES.md) - Updated with gateway
5. ✅ [ARCHITECTURE_CLARIFICATION_SUMMARY.md](ARCHITECTURE_CLARIFICATION_SUMMARY.md) - This document

---

## ✅ FINAL CONFIRMATION

### Pattern Summary

**✅ Modular DDD:** Use Saleor's structure (already compliant)
**✅ Containerized:** Use our Docker multi-stage build
**✅ Presentation Layer:** All frontends fetch from APIs
**✅ Centralized Gateway:** ALL requests through Brain Gateway
**✅ No Direct Connections:** Frontends never talk to backends directly

### CoreLdove Specific

**Approach:** ✅ Use Saleor AS-IS + Our deployment + Gateway routing
**Time:** 1-2 days (vs 4+ days if we refactor)
**Risk:** LOW
**DDD Compliance:** YES
**Gateway Routing:** YES

---

**Status:** Architecture clarified and corrected
**Ready to Proceed:** YES, with Brain Gateway routing
**Next:** Verify gateway routes, then deploy CoreLdove Storefront
