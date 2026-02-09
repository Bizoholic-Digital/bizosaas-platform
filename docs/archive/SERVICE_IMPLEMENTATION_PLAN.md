# Service Implementation Plan

This document outlines the roadmap for implementing all services currently listed in the Client Portal sidebar menu.

## 1. Core Services (High Priority)

### 1.1 Dashboard (`/dashboard`)
*   **Status**: ✅ Partially Implemented (Cards, stickiness)
*   **Next Steps**: Connect "Active Connectors", "AI Tasks", "Traffic" cards to real analytics API.

### 1.2 Connectors (`/dashboard/connectors`)
*   **Status**: ✅ Implemented (Integration with Brain Gateway)
*   **Next Steps**: Add "Configure" modal for each connector to input API keys/credentials.

### 1.3 AI Agents (`/ai-agents`)
*   **Status**: ✅ Implemented (Chat & Configuration)
*   **Next Steps**: Persist configuration (Prompts, Tools) to backend database.

## 2. Content Management System (CMS)

### 2.1 Pages (`/dashboard/cms/pages`)
*   **Architecture**: Backend via Wagtail (Headless) or FastAPI + Postgres.
*   **Plan**: Create CRUD interface for managing generic web pages.
*   **Dependencies**: `brain-cms` service.

### 2.2 Blog Posts (`/dashboard/cms/posts`)
*   **Architecture**: Connect to WordPress via Connector OR native Wagtail.
*   **Plan**: If WordPress connector active -> Sync/Manage WP posts. Else -> Internal blog system.

### 2.3 Media Library (`/dashboard/cms/media`)
*   **Architecture**: S3-compatible storage (MinIO locally).
*   **Plan**: File upload/manager interface.

## 3. Customer Relationship Management (CRM)

### 3.1 Contacts & Companies (`/dashboard/crm/contacts`)
*   **Architecture**: `brain-crm` service (FastAPI + Postgres).
*   **Plan**: List view, Detail view, Import/Export from CSV/Zoho.

### 3.2 Deals & Pipeline (`/dashboard/crm/deals`)
*   **Architecture**: Kanban board UI.
*   **Plan**: Drag-and-drop stage management.

## 4. E-commerce

### 4.1 Products & Orders (`/dashboard/ecommerce`)
*   **Architecture**: Connect to Shopify/WooCommerce via Connectors.
*   **Plan**: Unified view of products/orders from all connected channels.

## 5. Marketing

### 5.1 Campaigns & Email (`/dashboard/marketing`)
*   **Architecture**: `brain-marketing` service (Integration with SendGrid/Mailgun).
*   **Plan**: Campaign builder, Email template editor.

### 5.2 Social Media (`/dashboard/marketing/social`)
*   **Architecture**: Integration with LinkedIn/Twitter/fb APIs.
*   **Plan**: Post scheduler and calendar view.

## 6. Analytics Implementation Strategy

### 6.1 Architecture
*   **Ingestion**: Redis Streams (for high volume event data).
*   **Processing**: Python Workers (Temporal Workflows) to aggregate stream data.
*   **Storage**: Postgres (Aggregated metrics tables).
*   **Visualization**: Recharts / Chart.js in Client Portal (frontend).

### 6.2 Data Flow
1.  **Event**: User visits site / clicks link.
2.  **Transport**: Frontend -> `brain-gateway` -> Redis Stream (`analytics_events`).
3.  **Worker**: Temporal Worker pulls batch -> Aggregates (e.g. hourly counts) -> Inserts to DB.
4.  **Query**: Frontend -> `brain-gateway` (`GET /analytics/traffic`) -> Selects from DB -> JSON Response.

## 7. Admin & Billing

### 7.1 Billing (`/dashboard/billing`)
*   **Architecture**: Stripe Integration.
*   **Plan**: Subscription management, Invoice history.

### 7.2 Settings (`/dashboard/settings`)
*   **Plan**: User profile, Team management (RBAC), API Keys.

---

## Recommended Execution Order
1.  **CMS & CRM Basics**: Implement data models in backend and basic CRUD in frontend.
2.  **Marketing & Analytics**: Implement Redis Stream ingestion and basic charts.
3.  **Unified E-commerce**: Read-only view of external data first.
4.  **Billing**: Stripe integration before launch.
