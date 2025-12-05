# Architecture V2: Modular Microservices & Scaled-Down Core

## 1. Required Service Stack
To support the "Headless Saas" + "All-in-WordPress" strategy while maintaining Enterprise capabilities (RBAC, AI Agents), we need the following **Minimum Viable Stack**:

### **Core Services (Containerized)**
1.  **Brain Gateway (FastAPI):**
    *   **Port:** 8000
    *   **Role:** Central API Gateway, Connector Registry, AI Orchestrator.
    *   **Why:** Connects the Client Portal to all backend logic and external tools.
2.  **Client Portal (Next.js):**
    *   **Port:** 3000
    *   **Role:** The "Control Plane". UI for connecting services, talking to AI, viewing dashboards.
    *   **Change:** UI components (CRM/CMS charts) now fetch data via Connectors, not local DB.
3.  **Auth Service (FastAPI/Go):**
    *   **Port:** 8008
    *   **Role:** Multi-tenancy, JWT management, RBAC (Role-Based Access Control).
    *   **Why:** Essential for security. Supports "Super Admin" vs "Tenant" views.

### **Infrastructure (Essential)**
4.  **Redis:**
    *   **Usage:** Caching for Brain Gateway, Message Broker for CrewAI agents (if async), Session storage.
    *   **Verdict:** **KEEP.** Essential for performance and AI state.
5.  **PostgreSQL:**
    *   **Usage:** Storing User/Tenant data, Connector Configs (encrypted tokens), Audit Logs.
    *   **Verdict:** **KEEP.** The "Brain" needs memory.
6.  **Temporal:**
    *   **Usage:** Durable execution of long-running workflows (e.g., "On Weekends, fetch Google Ads data, analyze with AI, then update WordPress").
    *   **Verdict:** **KEEP.** Critical for reliable "Agentic Workflows".
        *   *Why not n8n?* n8n is great for users to build flows visually, but Temporal is better for *us* to build robust, code-defined system workflows that users just "config". Hosting n8n per tenant is resource-heavy.

### **Observability (Logging)**
7.  **Grafana + Loki + Prometheus:**
    *   **Verdict:** Better than ELK. Lighter weight, native Docker integration.
    *   **Logs:** Loki collects logs from all containers.
    *   **Metrics:** Prometheus tracks API latency and Error rates.
    *   **UI:** Grafana provides the "System Health" dashboard in the Super Admin panel.

---

## 2. Connectors vs. Integrations
There is confusion because they often overlap. Here is the strict definition for our DDD architecture:

*   **Connectors (The "What"):**
    *   **Purpose:** Establish a secure link (OAuth/API Key) to an external Platform.
    *   **Examples:** WordPress, Zoho CRM, Google Ads.
    *   **Action:** "Connect Account".
    *   **UI Location:** `/dashboard/connectors`

*   **Integrations (The "How"):**
    *   **Purpose:** Technical methods to interacting with those connected platforms.
    *   **Sub-Menus:**
        *   *Webhooks:* "When an Order happens in Shopify -> Notify Brain".
        *   *API Keys:* Generate keys for *external* apps to call the Brain.
        *   *Automation Rules:* "If Lead Score > 50 -> Sync to Zoho".
    *   **UI Location:** `/dashboard/integrations`
    *   **Fix:** The "Integrations" page should not show generic cards. It should show a table of *active* webhooks and rules *linked* to your Connectors.

## 3. CRM Strategy: Connector-First
**Decision:** Do **NOT** build a custom CRM within BizOSaaS.
*   **Recommendation:** Rely 100% on **Connectors**.
    *   **WP Users:** Use **FluentCRM Connector**. It runs on their WP, we just view data.
    *   **SaaS Users:** Use **Zoho / HubSpot Connectors**.
*   **Benefit:** Focus your dev time on AI Agents and Orchestration options, not rebuilding common CRM forms.

## 4. AI Agent Controls & Tuning
The current AI tab is visible but lacks deep control. We must expose:
1.  **Agent Config:** Edit "Backstory", "Goal", and "Temperature" (Creativity).
2.  **Tool Selection:** Checkboxes to give an agent access to specific Connectors (e.g., "Give Marketing Agent access to Google Ads").
3.  **Knowledge Base:** Upload PDFs/Brand Voice docs for the agent to reference.

## 5. Next Steps Plan
1.  **Backend:** Ensure Brain Gateway is returning all 13 connectors (check `registry.py`).
2.  **UI Fix:** Update `ConnectorsPage` to correctly navigate to `[id]/page.tsx` for configuration.
3.  **Feature:** Build the "AI Agent Settings" page with controls for Tools and Backstory.
4.  **Refactor:** Update "Integrations" page to show Webhooks/Rules instead of duplicate connector cards.
