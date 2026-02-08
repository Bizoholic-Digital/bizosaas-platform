# Tasks: Shopify + Marketplace Integration (BizoSaaS)

## 📋 Integration Roadmap

### 🏢 Milestone 0: Agency Site & Client Integration (Bizoholic.com)
- [x] **Task 0.1: WordPress Agency Site Optimization**
  - [x] Implement Microsoft Clarity tracking for user behavior analysis (Detection Logic Live & Verifiable).
  - [x] Sync WordPress "Knowledge Base" with RAG service for agent contextual awareness (Implemented `sync_wordpress_to_rag`).
- [/] **Task 0.3: Bedrock + Sage Migration (In Progress)**
  - [x] Migrate `bizoholic.com` to modern Roots stack (Header, Footer, Styles ported to Sage).
  - [x] Implement "Client Portal" button in Sage header (Unified Login Flow entry point).
  - [/] Finalize Sage theme build and asset compilation (Live site confirmed as legacy WP-Content).
- [ ] **Task 0.2: Unified Client Login Flow**
  - [ ] Add "Client Portal" login button to Bizoholic header.
  - [x] Implement SSO between WordPress (Authentik) and Client Portal (Next.js/Clerk) (Verified config).

### 🏁 Milestone 1: Shopify Hub Activation
- [x] **Task 1.1: Database Schema Expansion**
  - [x] Add `external_id` and `sync_metadata` to `McpRegistry` to track source versions.
  - [x] Create `MarketplaceProductMap` table to track product IDs across different platforms (Shopify ID <-> Flipkart ID).
- [x] **Task 1.2: Shopify Webhook Controller**
  - [x] Implement endpoint in `brain-gateway` to receive Shopify webhooks (`https://api.bizoholic.net/webhooks/shopify`).
  - [x] Handle `products/update`, `inventory/update`, and `orders/create`.
- [x] **Task 1.3: Background Sync Workers**
  - [x] Implement Temporal workflow for "Periodic Catalog Sync" (Shopify -> BizoSaaS).
  - [x] Implement Temporal workflow for "Real-time Order Injection" (Marketplace -> Shopify).

### 🇮🇳 Milestone 2: Indian Marketplace MCPs
- [x] **Task 2.1: Flipkart Seller API Integration**
  - [x] Transition from scraper prototype to official Flipkart Seller API (Implemented `flipkart.py` connector).
  - [x] Implement "Smart Fulfillment" logic sync (Automated Order Relay live).
- [x] **Task 2.2: Meesho Connector (High Priority)**
  - [x] Build proprietary Meesho MCP (Gap in market).
  - [x] Support automated order fetching (Done) and status updates.
- [x] **Task 2.3: Ajio & Myntra Modules**
  - [x] Implement connector foundations for Ajio and Myntra (Stubs created).
  - [x] Focus on high-touch fashion metadata integration (Added fashion category schemas).
- [x] **Task 2.4: AI Catalog Agent Service**
  - [x] Use LLMs to convert Shopify descriptions to Marketplace-specific templates (Implemented in `app/activities/marketplace.py`).

### 🚚 Milestone 3: Multichannel Orchestration (Phase 2)
- [x] **Task 3.1: Global Order Dashboard API**
  - [x] Implement `/multi-channel/orders` in `brain-gateway` to aggregate platform sales.
- [x] **Task 3.2: Unified Inventory Lock (Urgent)**
  - [x] Implement `InventoryService` and `MarketplaceInventoryLockWorkflow`.
  - [x] Automatically push "Out of stock" to all marketplaces when Shopify levels hit 0.
- [x] **Task 3.3: Return Flow Automation**
  - [x] Implement `process_marketplace_return` activity for RTO/Return sync.
  - [x] Sync return statuses from Indian marketplaces back to Shopify order notes.

### 🍱 Milestone 4: Marketplace Dashboard (Admin Portal)
- [x] **Task 4.1: Connector Hub UI**
  - [x] Card-based view in Admin Portal to manage and authenticate each marketplace (Live at `/dashboard/integrations`).
- [x] **Task 4.2: Health & Sync Latency Monitor**
  - [x] Real-time chart showing last sync time for each marketplace (Implemented in Dashboard).

### 💰 Milestone 5: Financial Reconciliation & Profitability
- [x] **Task 5.1: Settlement Reconciler**
  - [x] Match marketplace settlement files (CSV) with original Shopify orders (Implemented in `marketplace_finance.py`).
  - [x] Identify discrepancies in payout vs. expected revenue.
- [x] **Task 5.2: Channel Profitability Dashboard**
  - [x] Calculate Net Margin per SKU including marketplace commissions and RTO costs (Implemented in `marketplace_finance.py`).
  - [x] Real-time ROI analysis comparing Shopify (Direct) vs Marketplaces.

### 📣 Milestone 6: AI Marketing & Multi-channel Campaigns
- [x] **Task 6.1: Automated Social Media Integration**
  - [x] Shopify Product -> AI Post Generation -> Instagram/Meta/Pinterest API (Implemented in `MarketingCampaignWorkflow`).
- [x] **Task 6.2: cross-Channel Ad Orchestration**
  - [x] BizoSaaS AI Agent manages budget based on channel performance (Verified with `test_activity_ads.py`).

---

## 🛠️ Tech Stack for Implementation
- **Back-end**: FastAPI + SQLAlchemy + Temporal.
- **MCP Framework**: Model Context Protocol (Python SDK).
- **Messaging**: Redis (Streaming webhooks).
- **APIs**: Shopify Admin API (GraphQL), Flipkart Seller API, Meesho Supplier API.
