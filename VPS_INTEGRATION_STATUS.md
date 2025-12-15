# VPS Integration Status & Action Plan

**Date**: 2025-12-15  
**VPS**: 194.238.16.237 (Hostinger)

---

## Current State

### ✅ Running Services (Healthy)

| Service | Container | Status | Ports | Notes |
|---------|-----------|--------|-------|-------|
| **Temporal** | brain-temporal | Up 5 days | 7233 | ✅ Working |
| **Temporal UI** | brain-temporal-ui | Up 5 days | 8080 | ✅ Accessible at temporal-ui.bizoholic.net |
| **Vault** | brain-vault | Up 5 days | 8200 | ✅ Accessible at vault.bizoholic.net |
| **Brain Gateway** | brain-gateway | Up 5 days | 8000 | ⚠️ Missing /metrics endpoint |
| **Authentik** | authentik-server | Up 47 hours | - | ✅ Healthy |
| **Authentik Worker** | authentik-worker | Up 5 days | - | ✅ Healthy |
| **Authentik DB** | authentik-postgres | Up 5 days | 5432 | ✅ Healthy |
| **Client Portal** | client-portal | Up 55 min | 3000 | ⚠️ Missing Brain API env var |

### ❌ Issues

| Service | Container | Status | Issue |
|---------|-----------|--------|-------|
| **Admin Dashboard** | bizosaas-admin-dashboard | Unhealthy | Health check failing on `/api/health` |
| **Lago API** | lago-api | Restarting | Database connection issues |
| **Lago DB** | lago-db | Restarting | Restart loop |
| **Lago Worker** | lago-worker | Restarting | Depends on API/DB |

---

## Environment Variables Analysis

### Client Portal (Current)
```bash
AUTHENTIK_URL=https://sso.bizoholic.net
NEXT_PUBLIC_GRAPHQL_URL=https://api.bizoholic.net/graphql
NEXTAUTH_URL=https://app.bizoholic.net
```

### Client Portal (Missing)
```bash
NEXT_PUBLIC_BRAIN_API_URL=https://api.bizoholic.net
NEXT_PUBLIC_TEMPORAL_UI_URL=https://temporal-ui.bizoholic.net
NEXT_PUBLIC_VAULT_UI_URL=https://vault.bizoholic.net
```

### Admin Dashboard (Current - from docker-compose)
```bash
AUTHENTIK_URL=https://sso.bizoholic.net
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.net
NEXT_PUBLIC_TEMPORAL_UI_URL=https://temporal.bizoholic.net
NEXT_PUBLIC_VAULT_UI_URL=https://vault.bizoholic.net
NEXTAUTH_URL=https://admin.bizoholic.net
```

---

## Action Items

### Priority 1: Fix Admin Dashboard Health Check

**Problem**: `/api/health` endpoint doesn't exist

**Solution**: Create health check endpoint

```typescript
// portals/admin-dashboard/app/api/health/route.ts
export async function GET() {
  return Response.json({ status: 'ok', timestamp: new Date().toISOString() })
}
```

### Priority 2: Add Brain API Metrics Endpoint

**Problem**: Prometheus scraping `/metrics` returns 404

**Solution**: Add Prometheus metrics to Brain Gateway

```python
# bizosaas-brain-core/brain-gateway/main.py
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)  # Adds /metrics
```

### Priority 3: Update Client Portal Environment Variables

**Problem**: Missing Brain API URL configuration

**Solution**: Update docker-compose or Dokploy env vars

```yaml
# Add to client-portal environment
NEXT_PUBLIC_BRAIN_API_URL: https://api.bizoholic.net
NEXT_PUBLIC_TEMPORAL_UI_URL: https://temporal-ui.bizoholic.net
NEXT_PUBLIC_VAULT_UI_URL: https://vault.bizoholic.net
```

### Priority 4: Wire Frontend to Brain Gateway

**Current**: Client Portal has GraphQL URL but not REST API
**Needed**: Centralized API client routing all requests through Brain Gateway

**Files to Create**:
1. `portals/client-portal/lib/api/brain-client.ts` - Centralized API client
2. `portals/client-portal/lib/api/crm.ts` - CRM operations
3. `portals/client-portal/lib/api/cms.ts` - CMS operations
4. `portals/client-portal/lib/api/analytics.ts` - Analytics operations

### Priority 5: Connect Temporal & Vault Adapters

**Current**: Adapters exist but not wired to production URLs

**Solution**: Update Brain Gateway dependencies to use production endpoints

```python
# bizosaas-brain-core/brain-gateway/app/dependencies.py
from app.adapters.temporal_adapter import TemporalAdapter
from app.adapters.vault_adapter import VaultAdapter

async def get_temporal_client():
    return await TemporalAdapter.connect(
        host="brain-temporal:7233",  # Internal Docker network
        namespace="default"
    )

async def get_vault_client():
    return VaultAdapter(
        vault_url="http://brain-vault:8200",
        vault_token=os.getenv("VAULT_TOKEN")
    )
```

---

## Implementation Plan

### Phase 1: Fix Immediate Issues (30 min)

- [x] Create health endpoint for Admin Dashboard
- [x] Add metrics endpoint to Brain Gateway
- [ ] Redeploy Admin Dashboard
- [ ] Verify health check passes

### Phase 2: Wire Brain Gateway Integration (2 hours)

- [ ] Create centralized Brain API client
- [ ] Update Client Portal env vars
- [ ] Wire Temporal adapter to production
- [ ] Wire Vault adapter to production
- [ ] Test end-to-end flow

### Phase 3: Connect All Modules (4-6 hours)

- [ ] Wire Dashboard widgets to Brain API
- [ ] Wire CRM to Brain → Django CRM
- [ ] Wire CMS to Brain → Wagtail
- [ ] Wire Analytics to Brain → GA4
- [ ] Wire Billing to Brain → Lago

### Phase 4: Temporal Workflows (2 hours)

- [ ] Deploy connector setup workflow
- [ ] Deploy connector sync workflow
- [ ] Test workflow execution
- [ ] Monitor in Temporal UI

---

## DNS/Routing Verification

| Domain | Target | Status |
|--------|--------|--------|
| app.bizoholic.net | Client Portal (3000) | ✅ Working |
| admin.bizoholic.net | Admin Dashboard (3004) | ⚠️ Unhealthy |
| api.bizoholic.net | Brain Gateway (8000) | ✅ Working |
| sso.bizoholic.net | Authentik | ✅ Working |
| temporal-ui.bizoholic.net | Temporal UI (8080) | ✅ Working |
| vault.bizoholic.net | Vault (8200) | ✅ Working |

---

## Next Steps

1. **Create health endpoint** for Admin Dashboard
2. **Add metrics** to Brain Gateway
3. **Update environment variables** for Client Portal
4. **Create API client library** for frontend
5. **Wire all modules** to Brain Gateway
6. **Test end-to-end** integration

---

*Last Updated: 2025-12-15 09:54 UTC*
