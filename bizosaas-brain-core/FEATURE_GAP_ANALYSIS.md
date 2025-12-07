# Feature Implementation & Gap Analysis

## 1. Connector Configuration Gaps
**Status:** 13 Connectors implemented in Backend, but UI not reflecting configuration screens.
*   **Issue:** The `/dashboard/connectors` page was listing them but not navigating to `/dashboard/connectors/[id]` correctly.
*   **Fix Applied:** We updated the `onClick` handler in `ConnectorsPage` to route to the details page.
*   **Remaining Work:** Verify `ConnectorDetailsPage` is fetching the specific schema for each connector type (e.g., `Google Ads` needs Developer Token, `WordPress` needs App Password).

## 2. AI Agent Control Panel
**Status:** `AIChat` component exists but lacks "Tuning" controls.
**Requirement:** Users need to "Fine-tune" agents.
**Proposal:** Create `/dashboard/ai-agents/[agentId]/settings` page.
*   **Settings to Expose:**
    *   `Role Description`: "You are a witty marketing expert..."
    *   `Tools`: Toggle "Google Ads Access", "WordPress Posting Access".
    *   `Schedule`: "Run every Monday at 9AM" (Temporal integration).

## 3. Integrations vs Connectors UI
**Status:** The "Integrations" tab currently duplicates the "Connectors" view (Webhooks, API Keys showing generic cards).
**Refactor Plan:**
*   `/dashboard/integrations/webhooks`: Show a Table of active listeners (e.g., "Stripe Payment Success -> Trigger Email Agent").
*   `/dashboard/integrations/api-keys`: Show a Table of generated keys for external use.
*   `/dashboard/integrations/automation`: Show a Flow Builder (React Flow) or simple Rule List ("If X then Y").

## 4. Backend Service Checklist
To support "Modular Microservices":
*   [x] **Brain Gateway (API):** Ready with 13 Connectors.
*   [ ] **Auth Service:** Needs to be verified running on port 8008.
*   [ ] **Temporal Worker:** Needs to be running to execute the "Async Actions" defined in Connectors (e.g., `perform_action` on a schedule).
*   [ ] **Database:** Postgres needs to be persistent (currently using mock dicts in some connectors).

## 5. Client Portal "Headless" Wiring
The following Tabs are visible but need wiring to `brainApi`:
*   **CMS Tab:**
    *   *Pages:* Wire to `brainApi.connectors.sync('wordpress', 'pages')`
    *   *Posts:* Wire to `brainApi.connectors.sync('wordpress', 'posts')`
*   **CRM Tab:**
    *   *Contacts:* Wire to `brainApi.connectors.sync('fluentcrm', 'contacts')` or `zoho`
*   **E-commerce Tab:**
    *   *Products:* Wire to `brainApi.connectors.sync('woocommerce', 'products')` or `shopify`
    *   *Orders:* Wire to `brainApi.connectors.sync('woocommerce', 'orders')`

## 6. Observability
*   **Logs:** We should use **Loki** (simpler than ELK) for log aggregation.
*   **Metrics:** **Prometheus** for tracking "API Calls per Connector" (billing metric).
*   **Dashboard:** **Grafana** to visualize "System Health" for Super Admins.
*   **Missing:** **Audit Logging**. We need to track *Who* changed *What* (e.g., "User X updated Agent Config").

## 7. Enterprise Security Implementation (High Priority)
To meet Enterprise Requirements (RBAC, SSO, SOC2):
*   [ ] **HashiCorp Vault Integration:**
    *   Deploy Vault Container (Done).
    *   Update `brain-gateway` to fetch API Keys (OpenAI, Stripe) from Vault using `hvac` library.
    *   Do NOT store API keys in Postgres plaintext.
*   [ ] **Advanded Auth & SSO:**
    *   Refactor `auth-service` to use **`fastapi-sso`** library for robust Google/Microsoft/GitHub login.
    *   Ensure JWT contains `permissions` list for Frontend RBAC.
*   [ ] **Audit Logging System:**
    *   Create `AuditLog` table in Postgres (event, user_id, tenant_id, timestamp, metadata).
    *   Implement **Middleware** in `brain-gateway` to auto-log POST/PUT/DELETE actions.
*   [ ] **Strict Multi-Tenancy:**
    *   Implement `TenantContextMiddleware` to extract `tenant_id` from JWT.
    *   Enforce `WHERE tenant_id = X` on ALL database queries via DAO layer.
