# 🔌 Connector & Integration Enhancement Plan

**Date:** January 6, 2026  
**Status:** Analysis Complete, Ready for Implementation

---

## 📋 Executive Summary

The user has identified several gaps in the current connector/integration system:

1. **Google Magic Discovery** - Detects services but doesn't provide OAuth consent flow
2. **WordPress Connector** - "Failed to store credentials securely" error
3. **WordPress Plugin Discovery** - No automatic detection of installed plugins
4. **WordPress Content Management** - Need full CRUD for posts, pages, media, plugins
5. **Unified Consent Flow** - Similar approach needed for all OAuth connectors
6. **Integration with Zapier/Make/n8n** - Leverage existing MCP implementations

---

## 🔍 Current Architecture Analysis

### What's Already Implemented ✅

| Component | Status | Location |
|-----------|--------|----------|
| Connector Registry | ✅ Working | `brain-gateway/app/connectors/registry.py` |
| Base Connector Class | ✅ Working | `brain-gateway/app/connectors/base.py` |
| OAuth Mixin | ✅ Skeleton | `brain-gateway/app/connectors/oauth_mixin.py` |
| WordPress Connector | ✅ Partial | `brain-gateway/app/connectors/wordpress.py` |
| Google Connectors | ✅ Partial | `brain-gateway/app/connectors/google_*.py` |
| Secret Service | ✅ Working | `brain-gateway/app/domain/services/secret_service.py` |
| Vault Adapter | ⚠️ Connection Issue | `brain-gateway/adapters/vault_adapter.py` |
| API Endpoints | ✅ Working | `brain-gateway/app/api/connectors.py` |
| OAuth Router | ✅ Skeleton | `brain-gateway/app/routers/oauth.py` |
| Frontend Connectors UI | ✅ Working | `client-portal/components/ConnectorsContent.tsx` |

### Identified Gaps ❌

| Gap | Impact | Priority |
|-----|--------|----------|
| Vault not connected in production | HIGH - "Failed to store credentials" | P0 |
| OAuth callback doesn't save to Vault | HIGH - Google consent flow broken | P0 |
| No plugin discovery for WordPress | MEDIUM - Manual config required | P1 |
| No content management UI in portal | MEDIUM - Limited functionality | P1 |
| Google services don't trigger consent | HIGH - Discovery only, no action | P0 |
| MCP connectors not integrated | LOW - Future phase | P2 |

---

## 🛠️ Implementation Plan

### Phase 1: Fix Vault Connection & Credential Storage (P0) 
**Estimated Time: 2-4 hours**

#### 1.1 Diagnose Vault Connection Issue

**Problem:** When WordPress connector tries to store credentials, it fails with "Failed to store credentials securely"

**Root Cause Analysis:**
- The VaultAdapter at line 64-66 checks `self.client.is_authenticated()`
- If Vault is not running or token is wrong, this returns False
- The `store_secret` method then returns False, causing the 500 error

**Fix Steps:**
1. Verify Vault is running and accessible from brain-gateway container
```bash
# SSH to server
docker exec bizosaascore-braingateway-kdbono-brain-gateway-1 \
  curl -s http://vault:8200/v1/sys/health
```

2. Set `VAULT_TOKEN` environment variable in brain-gateway docker-compose
```yaml
environment:
  - VAULT_URL=http://vault:8200
  - VAULT_TOKEN=${VAULT_TOKEN:-root}  # Dev token
```

3. Initialize Vault KV v2 engine if not already done
```bash
docker exec vault vault secrets enable -path=secret kv-v2
```

4. Add fallback storage for development (PostgreSQL or file-based)

#### 1.2 Complete OAuth Callback Flow

**Problem:** OAuth router at line 75-77 has `# TODO: Save credentials to DB/Vault`

**Fix:**
```python
# In oauth.py, add after token exchange:
from app.dependencies import get_secret_service

@router.post("/callback")
async def oauth_callback(
    params: OAuthCallbackParams,
    secret_service: SecretService = Depends(get_secret_service)
):
    # ... existing code ...
    
    # Save credentials to Vault
    success = await secret_service.store_connector_credentials(
        tenant_id=params.tenant_id,
        connector_id=params.connector_id,
        credentials=token_data,
        metadata={"oauth": True, "provider": params.connector_id}
    )
    
    if not success:
        raise HTTPException(500, "Failed to store OAuth credentials")
    
    return {"status": "success", "message": "Connected successfully"}
```

---

### Phase 2: Implement Google OAuth Consent Flow (P0)
**Estimated Time: 3-4 hours**

#### 2.1 Add "Connect with Google" Button for Each Google Service

**Current State:** Discovery shows services but no way to authorize them

**Frontend Changes (ConnectorsContent.tsx):**
```tsx
// Add OAuth handler for Google connectors
const handleOAuthConnect = async (connector: ConnectorConfig) => {
  const response = await fetch(`/api/connectors/oauth/authorize/${connector.id}`, {
    method: 'GET',
    headers: { /* auth headers */ }
  });
  const { url } = await response.json();
  
  // Open OAuth popup or redirect
  window.open(url, '_blank', 'width=600,height=700');
};

// In card footer, check if connector uses OAuth
{connector.auth_type === 'oauth' ? (
  <Button onClick={() => handleOAuthConnect(connector)}>
    <ExternalLink className="mr-2 h-4 w-4" /> Connect with Google
  </Button>
) : (
  <Button onClick={() => handleOpenConnect(connector)}>
    Connect
  </Button>
)}
```

#### 2.2 Add OAuth Callback Handler in Frontend

**New File: `client-portal/app/dashboard/integrations/callback/page.tsx`**
```tsx
'use client';

import { useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';

export default function OAuthCallbackPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  
  useEffect(() => {
    const code = searchParams.get('code');
    const state = searchParams.get('state');
    
    if (code && state) {
      // Parse state to get connector_id and tenant_id
      const [tenantId, connectorId] = state.split(':');
      
      // Exchange code for tokens via backend
      fetch('/api/connectors/oauth/callback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code,
          state,
          connector_id: connectorId,
          tenant_id: tenantId,
          redirect_uri: window.location.origin + '/dashboard/integrations/callback'
        })
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          // Close popup or redirect to connectors page
          window.opener?.postMessage({ type: 'oauth_success', connector: connectorId }, '*');
          window.close();
        }
      });
    }
  }, [searchParams]);
  
  return <div>Completing connection...</div>;
}
```

#### 2.3 Update Connector Config to Indicate Auth Type

**In base.py or each connector:**
```python
ConnectorConfig(
    id="google-analytics",
    name="Google Analytics 4",
    type=ConnectorType.ANALYTICS,
    auth_type="oauth",  # NEW FIELD
    oauth_config={
        "provider": "google",
        "scopes": ["https://www.googleapis.com/auth/analytics.readonly"]
    },
    # ...
)
```

---

### Phase 3: WordPress Plugin Discovery & Auto-Connect (P1)
**Estimated Time: 4-6 hours**

#### 3.1 Add Plugin Discovery Endpoint to WordPress Connector

**New method in `wordpress.py`:**
```python
KNOWN_PLUGINS = {
    "fluent-crm": {
        "id": "fluentcrm",
        "name": "FluentCRM",
        "connector_id": "fluentcrm"
    },
    "woocommerce": {
        "id": "woocommerce",
        "name": "WooCommerce",
        "connector_id": "woocommerce"
    },
    "mailchimp-for-woocommerce": {
        "id": "mailchimp",
        "name": "Mailchimp",
        "connector_id": "mailchimp"
    },
    # Add more known plugins...
}

async def discover_plugins(self) -> List[Dict[str, Any]]:
    """
    Discover installed plugins on the WordPress site.
    Returns list of plugins with connection suggestions.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            self._get_api_url("plugins"),
            headers=self._get_auth_header(),
            timeout=15.0
        )
        response.raise_for_status()
        
        plugins = response.json()
        discovered = []
        
        for plugin in plugins:
            plugin_slug = plugin.get("textdomain", "").lower()
            if plugin_slug in KNOWN_PLUGINS:
                discovered.append({
                    **KNOWN_PLUGINS[plugin_slug],
                    "status": plugin.get("status"),
                    "version": plugin.get("version"),
                    "can_auto_connect": True
                })
            else:
                discovered.append({
                    "id": plugin_slug,
                    "name": plugin.get("name"),
                    "status": plugin.get("status"),
                    "can_auto_connect": False
                })
        
        return discovered
```

#### 3.2 Add API Endpoint for Plugin Discovery

**In connectors.py:**
```python
@router.get("/{connector_id}/plugins")
async def discover_plugins(
    connector_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """Discover plugins for a connected WordPress site"""
    if connector_id != "wordpress":
        raise HTTPException(400, "Plugin discovery only for WordPress")
    
    tenant_id = user.tenant_id or "default_tenant"
    credentials = await secret_service.get_connector_credentials(tenant_id, connector_id)
    
    if not credentials:
        raise HTTPException(404, "WordPress not connected")
    
    connector = ConnectorRegistry.create_connector(connector_id, tenant_id, credentials)
    plugins = await connector.discover_plugins()
    
    return {"plugins": plugins}
```

#### 3.3 Frontend: Plugin Selection Dialog

**New Component: `PluginDiscoveryDialog.tsx`**
- Opens after WordPress connection is successful
- Shows list of detected plugins with checkboxes
- Groups by: "Connectable" vs "Other Plugins"
- "Connect Selected" button triggers batch connection

---

### Phase 4: WordPress Content Management UI (P1)
**Estimated Time: 6-8 hours**

#### 4.1 Create WordPress Management Dashboard Section

**New Route: `/dashboard/wordpress`**

**Features:**
- Posts tab: List, Create, Edit, Delete posts
- Pages tab: List, Create, Edit, Delete pages
- Media tab: Upload, browse, delete media
- Plugins tab: View installed, toggle enable/disable

#### 4.2 API Endpoints Already Exist

The `wordpress.py` connector already has:
- `get_posts()`, `create_post()`, `update_post()`, `delete_post()`
- `get_pages()`, `create_page()`, `update_page()`, `delete_page()`
- `get_stats()` for counts

**Need to add:**
- Media endpoints (upload, list, delete)
- Plugin management endpoints

#### 4.3 Frontend Components

```
/dashboard/wordpress/
  ├── page.tsx (main dashboard)
  ├── components/
  │   ├── PostsTable.tsx
  │   ├── PagesTable.tsx
  │   ├── MediaGrid.tsx
  │   ├── PluginsTable.tsx
  │   └── PostEditor.tsx (rich text editor)
```

---

### Phase 5: MCP & Automation Platform Integration (P2)
**Estimated Time: 4-6 hours**

#### 5.1 Leverage Existing MCP Strategy

Per `MCP_INTEGRATION_STRATEGY.md`, MCPs are already planned for:
- **GitHub MCP** - Code management
- **Slack MCP** - Team communication
- **n8n** - Workflow automation

**Add new MCPs for:**
- **WordPress MCP** - Content management via MCP protocol
- **Zapier Webhook** - Trigger on connection events
- **Make.com Webhook** - Similar to Zapier

#### 5.2 OpenAPI-Based Auto-Discovery

For Paddle, n8n, etc. that expose OpenAPI specs:

```python
class OpenAPIConnector(BaseConnector):
    """Generic connector that reads from OpenAPI spec"""
    
    async def load_spec(self, spec_url: str):
        async with httpx.AsyncClient() as client:
            resp = await client.get(spec_url)
            self.spec = resp.json()
            self._generate_actions()
    
    def _generate_actions(self):
        """Auto-generate perform_action handlers from OpenAPI paths"""
        for path, methods in self.spec.get("paths", {}).items():
            for method, details in methods.items():
                action_name = details.get("operationId", f"{method}_{path}")
                # Register dynamic action
```

---

## 📊 Implementation Priority Matrix

| Phase | Priority | Complexity | Business Value | ETA |
|-------|----------|------------|----------------|-----|
| 1. Fix Vault | P0 | Low | Critical | Day 1 |
| 2. Google OAuth | P0 | Medium | High | Day 1-2 |
| 3. Plugin Discovery | P1 | Medium | High | Day 2-3 |
| 4. WordPress CMS UI | P1 | High | High | Day 3-5 |
| 5. MCP Integration | P2 | High | Medium | Week 2 |

---

## 🚀 Immediate Next Steps

1. **SSH to server and verify Vault health**
2. **Add VAULT_TOKEN to brain-gateway environment**
3. **Complete OAuth callback credential storage**
4. **Test Google Analytics connection flow end-to-end**
5. **Add plugin discovery to WordPress connector**

---

## 📁 Files to Modify

### Backend (brain-gateway)
- `app/routers/oauth.py` - Complete callback flow
- `app/connectors/wordpress.py` - Add plugin discovery
- `app/connectors/base.py` - Add auth_type field
- `app/api/connectors.py` - Add plugins endpoint
- `docker-compose.yml` - Add VAULT_TOKEN env var

### Frontend (client-portal)
- `components/ConnectorsContent.tsx` - OAuth button
- `app/dashboard/integrations/callback/page.tsx` - NEW
- `components/PluginDiscoveryDialog.tsx` - NEW
- `app/dashboard/wordpress/page.tsx` - NEW (CMS UI)

---

## ✅ Success Criteria

- [ ] WordPress connector stores credentials without error
- [ ] Google services show "Connect" button and complete OAuth flow
- [ ] After WordPress connect, plugin discovery dialog appears
- [ ] User can select and bulk-connect discovered plugins
- [ ] WordPress content (posts, pages) manageable from dashboard
- [ ] All credentials stored securely in Vault
