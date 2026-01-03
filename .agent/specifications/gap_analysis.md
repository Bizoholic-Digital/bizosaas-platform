# BizOSaaS Platform - Gap Analysis & Implementation Spec (v2.0)

This document analyzes the current implementation against the **`bizosaas-updated-PRD-17122025.md`** and provides a roadmap for completion using Spec-Driven Development principles.

---

## 🔍 Implementation Gaps

| Module | Status | Missing Feature | Priority |
| :--- | :--- | :--- | :--- |
| **Onboarding** | ⚠️ Partial | Persistent Draft Storage (SQLAlchemy Models) | **High** |
| **Onboarding** | ⚠️ Partial | Feasibility Loop (Strategy AI refinement) | **High** |
| **Integrations** | ⚠️ Partial | Stripe, Slack, Zapier Connectors | Medium |
| **Billing** | ❌ Missing | Multi-tenant Lago usage-based billing integration | **High** |
| **AI Agents** | ⚠️ Partial | "Personal Business Agent" long-term memory/learning | Medium |
| **Transparency** | ⚠️ Partial | Task-level sync for *all* agents to Plane issues | Medium |
| **Monitoring** | ⚠️ Partial | Global Agent Persona Toggle in Admin Dashboard | Low |

---

## 🛠️ Required Implementation Specs

### 1. Persistent Onboarding (Onboarding DB Model)
*   **Problem**: Currently using `MOCK_STORE` (in-memory). Drafts are lost on restart.
*   **Requirement**: 
    *   Create `OnboardingSession` model in SQLAlchemy.
    *   Store JSON blobs of partial state.
    *   Link to `tenant_id`.

### 2. Strategy Feasibility Engine (Campaign Strategy Loop)
*   **Problem**: PRD Step 11 requires a loop where AI checks goals against data.
*   **Requirement**:
    *   New `campaigns/validate-strategy` endpoint.
    *   Temporal Workflow: `StrategyValidationWorkflow`.
    *   Integration: Call specialized "Analyst Agent" to compare CRM/Ads history with new goals.

### 3. Usage-Based Billing for Connectors
*   **Problem**: Connectors are implemented, but clients aren't billed for API usage.
*   **Requirement**:
    *   Add "Events" logging in the `ConnectorBase` class.
    *   Sync event counts to **Lago** at the end of each day.
    *   Define Billable Metrics (e.g., "WordPress Post Synced", "Ad Optimized").

---

## 🚀 Recommended Post-MVP Features (Analysis-Driven)

These features were identified as high-value for US SMBs but are not yet in the PRD:

### 🌟 1. AI Content Compliance Guard
*   **Feature**: A dedicated agent that scans every generated blog post or ad creative for US legal compliance (ADA, FTC Truth in Advertising).
*   **Benefit**: Reduces legal risk for clients automatically.

### 🌟 2. Natural Language Analytics (Text-to-Chart)
*   **Feature**: Use the existing Analytics agents to allow users to ask questions like *"What was my ROI for Google Ads in Miami last week?"* and receive a dynamic chart.
*   **Benefit**: Replaces complex GA4 dashboards with simple conversation.

### 🌟 3. competitor Intelligence RAG
*   **Feature**: Ingest competitor websites into a dedicated Vector namespace. 
*   **Benefit**: Allows AI agents to write copy that specifically targets competitor weaknesses found in their online presence.

### 🌟 4. "Agent Shadows" (Manual Override)
*   **Feature**: Allow users to see the "thought process" of an agent before it executes.
*   **Benefit**: Increases trust in the "Task Transparency" requirement of the PRD.

---

## 📋 OpenSpec Roadmap Targets

1.  **`/api/onboarding/persist`**: Move from MOCK_STORE to PostgreSQL.
2.  **`/api/campaigns/strategy`**: Implementation of the Strategy Loop.
3.  **`BillingAgent`**: Specialized agent to update Lago usage meters.
