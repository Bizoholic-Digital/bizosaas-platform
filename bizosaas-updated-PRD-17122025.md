# BizOSaaS Platform - Product Requirements Document
**Version**: 2.0  
**Date**: December 17, 2025  
**Status**: Active Development

## BizoSaaS Platform Explained

BizOSaaS is an AI-powered multi-tenant SaaS platform that leverages 93+ specialized CrewAI agents to automate business operations for clients. The platform provides a unified interface for managing CMS, CRM, and eCommerce integrations through intelligent automation.
The BizoSaaS Platform has the below sequence:
1. New clients will be taken through the onboarding wizard
2. The onboarding wizard will request for the list of all tools and services the client would like to integrate by providing them the list of all external tools and services like the CMSs, CRMs, Analytics, Search Consoles, etc integrations. 
3. For each of the external tools and services selected the onboarding wizard will list the consolidated list of all the fields required so that the client (user) can list it accordingly to be filled.
4. The list of fields should be as minimal as possible making the onboarding as easy as possible.
5. The onboarding wizard should be a step-by-step multi stage process. 
6. The user should be able to save as draft and continue at a later stage. 
7. The onboarding can start with like asking for the company name, google my business profile link or ask the user to select the business from the list which will be populated via the API making it easier for the user to select from the dropdown. The user will be able to connect and integrate with the Google My business profile only if the google account is linked to the gmail address used by the user to setup the account. this is the enable the security and stop companies to acquire the profiles of competitors. 
8. With the google my business profile, locality, industry, website (if already exists) the onboarding ai agent will start populating the data and provide it to the user for confirmation. 
9. On confirmation the process will proceed forward by analyzing and auditing the current online presence. 
10. While the analysis and the auditing is being done in the background via the workflows that we have setup we should be proceeding to keep the interaction going forward by asking for the goals, budget, target audience for the campaigns. 
11. Once the research is completed and the details are received the ai agent will do a feasibility check by comparing the output from the various research ai agent and the requirement of the client and provide as strategy that is best suited for the client to achieve the goal by suggesting if they should refine their goals, budgets, target audience etc which the client will get into a loop until the client is satisfied with the suggested strategy.
12. Once the strategy is confirmed the setup ai agents will start triggering the various workflows and executing it such that the campaigns are setup and the work starts across these multiple campaigns. 
13. The list of all tasks will be populated and shown to maintain the transparency for the client. 
14. The progress on the various tasks will be updated such that the clients are aware of the progress on the various tasks. 
15. This is nothing but a full fledged digital marketing agency where the clients are updated on a regular basis. 
16. The clients can also update the requirements and based on that the campaigns will be updated such that any changes will also effect the outcome of the campaigns which will also be updated and reported to the client for tier review and approval to proceed to update the tasks accordingly. 

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Core Services](#core-services)
3. [Architecture Overview](#architecture-overview)
4. [Platform Features](#platform-features)
5. [AI Agent Integration](#ai-agent-integration)
6. [Infrastructure Details](#infrastructure-details)
7. [Deployment Configuration](#deployment-configuration)

---

## Executive Summary

BizOSaaS is an AI-powered multi-tenant SaaS platform that leverages 93+ specialized CrewAI agents to automate business operations for clients. The platform provides a unified interface for managing CMS, CRM, and eCommerce integrations through intelligent automation.

**Key Differentiators**:
- 93+ specialized AI agents for comprehensive business automation
- Multi-tenant architecture with RBAC via Authentik
- Centralized Brain API Gateway routing all services
- Consolidated infrastructure for optimal resource utilization
- Guided onboarding with automated service integration

---

## Core Services

### Infrastructure Layer

| Service | Technology | Purpose | Port | Status |
|---------|-----------|---------|------|--------|
| **PostgreSQL** | pgvector/pgvector:pg16 | Multi-tenant database with vector support for RAG/KAG | 5433 | ✅ Active |
| **Redis** | redis:7-alpine | Caching, sessions, analytics streams | 6380 | ✅ Active |
| **Vault** | hashicorp/vault:1.15 | Secrets management | 8201 | ✅ Active |
| **Temporal** | temporalio/auto-setup:1.22.0 | Workflow orchestration (replaces n8n) | 7234 | ✅ Active |
| **Temporal UI** | temporalio/ui:2.21.0 | Workflow management interface | 8083 | ✅ Active |
| **RAG Service** | Python (FastAPI) | Knowledge-Augmented Generation with pgvector | N/A | ✅ Active |

### Observability Stack

| Service | Technology | Purpose | Port | Status |
|---------|-----------|---------|------|--------|
| **Loki** | grafana/loki:2.9.0 | Log aggregation | 3100 | ✅ Active |
| **Prometheus** | prom/prometheus:v2.47.0 | Metrics collection | 9090 | ✅ Active |
| **Grafana** | grafana/grafana:10.2.0 | Monitoring dashboards | 3003 | ✅ Active |

### Application Layer

| Service | Technology | Purpose | Port | Status |
|---------|-----------|---------|------|--------|
| **Brain Gateway** | FastAPI (Python) | Central API gateway with 93+ AI agents | 8001 | ✅ Active |
| **Auth Service** | FastAPI (Python) | Authentication & authorization | 8007 | ⚠️ Restarting |
| **Client Portal** | Next.js 14 | Client-facing dashboard | 3000 | ✅ Active |
| **Admin Dashboard** | Next.js 14 | Platform administration | 3004 | ⚠️ Unhealthy |
| **Authentik** | goauthentik/server:2024.10.1 | Identity & Access Management (IAM), Multi-tenant RBAC, SSO | 9000 | ✅ Active |
| **Plane** | makeplane/plane | Project management | 8082 | ⏳ Pending |
| **Lago** | getlago/api:v1.16.0 | Billing & subscriptions | 8088 | ⚠️ Restarting |

---

## Architecture Overview

### Consolidated Infrastructure

**Design Principle**: Single shared PostgreSQL and Redis instances to minimize resource overhead.

#### Database Architecture

**Single PostgreSQL Instance** (`bizosaas-postgres-staging`):
- **bizosaas_staging**: Brain Gateway, Auth Service (multi-tenant core)
- **plane_db**: Plane project management
- **lago**: Billing and subscriptions
- **authentik**: Identity and access management
- **temporal**: Workflow state management
- **dokploy**: Platform deployment management

**Single Redis Instance** (`bizosaas-redis-staging`):
- **DB 0**: Brain Gateway (API caching, sessions)
- **DB 1**: Auth Service (tokens, rate limiting)
- **DB 2**: Client Portal (UI state, sessions)
- **DB 3**: Admin Dashboard (admin sessions)
- **DB 4**: Plane (project cache)
- **DB 5**: Lago (billing cache)
- **DB 6**: Authentik (SSO sessions)
- **DB 7**: Temporal (workflow cache)
- **DB 8**: Prometheus (metrics buffer)
- **DB 9**: Grafana (dashboard cache)

#### Network Architecture

```
Internet → Traefik (Reverse Proxy)
    ↓
┌─────────────────────────────────────┐
│  Client Portal (Next.js)            │
│  Admin Dashboard (Next.js)          │
└─────────────┬───────────────────────┘
              │
              ↓
┌─────────────────────────────────────┐
│  Brain Gateway (FastAPI)            │
│  - 93+ AI Agents                    │
│  - Central API Router               │
└─────────────┬───────────────────────┘
              │
    ┌─────────┴─────────┬─────────────┬──────────┐
    ↓                   ↓             ↓          ↓
┌───────────┐      ┌──────────┐   ┌─────────┐  ┌──────────┐
│ Plane     │      │   Lago   │   │Authentik│  │Temporal  │
│(Project)  │      │(Billing) │   │  (IAM)  │  │(Workflow)│
└───────────┘      └──────────┘   └─────────┘  └──────────┘
    │                │              │            │
    └────────────────┴──────────────┴────────────┘
                     │
         ┌───────────┴───────────┐
         ↓                       ↓
┌─────────────────┐    ┌──────────────────┐
│   PostgreSQL    │    │      Redis       │
│  (Shared DB)    │    │  (Shared Cache)  │
└─────────────────┘    └──────────────────┘
```

### Dokploy Project Structure

| Project | Services | Purpose | Status |
|---------|----------|---------|--------|
| **bizosaas-infra** | Postgres, Redis, Vault, Temporal, Monitoring | Foundation infrastructure | ✅ Active |
| **bizosaas-core** | Brain Gateway, Auth Service | Core API services | ✅ Active |
| **bizosaas-frontend** | Client Portal | Client-facing UI | ✅ Active |
| **bizosaas-admin** | Admin Dashboard | Platform administration | ✅ Active |
| ~~**automation-hub**~~ | ~~n8n~~ | ~~Workflow automation~~ | ❌ Deprecated (replaced by Temporal) |
| ~~**database-services**~~ | ~~Standalone DBs~~ | ~~Database management~~ | ❌ Deprecated (consolidated) |

---

## Platform Features

### 1. Client Onboarding

**Guided Setup Process**:
1. **Account Creation**: Client registers via Client Portal
2. **Profile Configuration**: Business details, industry, goals
3. **Service Integration**: Connect CMS, CRM, eCommerce platforms via 21+ connectors
4. **Credential Management**: Secure storage via Vault
5. **AI Agent Activation**: Personal AI agent assigned
6. **Automation Setup**: AI agents configure workflows using connected data

**Supported Integrations**:
- **CMS**: WordPress, Shopify, WooCommerce
- **CRM**: FluentCRM, Zoho CRM
- **Advertising**: Google Ads, Facebook Ads, Pinterest, Snapchat
- **Analytics**: Google Analytics, Google Tag Manager
- **Communication**: WhatsApp, Telegram, Email
- **Project Management**: Plane, Trello
- **Billing**: Lago (built-in)

### 2. Multi-Tenant Architecture

**Authentik Integration**:
- **Tenant Isolation**: Each client has isolated data space
- **RBAC**: Role-based access control (Admin, Manager, User)
- **SSO**: Single sign-on across all services
- **API Keys**: Secure API access per tenant

### 3. Centralized API Gateway

**Brain Gateway Features**:
- **Unified Routing**: All external services route through gateway
- **Authentication**: JWT-based auth with Authentik
- **Rate Limiting**: Redis-backed rate limiting per tenant
- **Logging**: Structured logging to Loki
- **Metrics**: Prometheus metrics for all endpoints
- **AI Agent Orchestration**: Manages 93+ specialized agents
- **White-Labeling & Branding**: Centralized management of portal identity (logo, colors, fonts)

### 4. Smart Connector Discovery

**Automated Upsell & Integration Logic**:
- **WordPress Intelligence**: Automatically detects plugins (WooCommerce, FluentCRM) and prompts for connection.
- **Google Ecosystem**: Link GTM to Analytics/Ads via "Magic Discovery" flow.
- **Cross-Platform Mapping**: Intelligent detection of related services (e.g., Shopify to Facebook Pixel).

### 5. AI Agent Visibility & Governance

**Admin Dashboard (Global Visibility)**:
- View all active agents across all tenants.
- Monitor agent performance and cost.
- Global persona management and capability toggle.

**Client Portal (Contextual Visibility)**:
- **Personal Business Agent**: Primary interface for the client.
- **Task Transparency**: Clients see specific tasks performed by specialized agents (e.g., "SEO Agent optimized /blog/post-1").
- **Approval Loops**: Strategic agents present plans for client review before execution.

---

## AI Agent Integration

### Personal AI Agent

Each client gets a **Personal AI Agent** that:
- Understands client's business context
- Coordinates with specialized agents
- Provides natural language interface
- Learns from client interactions
- Automates routine tasks

### Specialized AI Agents (93+)

**Categories**:
1. **Content Management** (15 agents)
   - Blog post generation
   - SEO optimization
   - Image optimization
   - Content scheduling
   - etc.

2. **Customer Relationship** (20 agents)
   - Lead scoring
   - Email campaigns
   - Customer segmentation
   - Support ticket routing
   - etc.

3. **E-Commerce** (18 agents)
   - Inventory management
   - Price optimization
   - Order fulfillment
   - Product recommendations
   - etc.

4. **Analytics & Reporting** (12 agents)
   - Sales forecasting
   - Performance dashboards
   - Trend analysis
   - Custom reports
   - etc.

5. **Marketing Automation** (15 agents)
   - Social media posting
   - Ad campaign optimization
   - A/B testing
   - Conversion tracking
   - etc.

6. **Operations** (13 agents)
   - Workflow automation
   - Task scheduling
   - Resource allocation
   - Process optimization
   - etc.

> **Note**: Detailed agent specifications available in [`AI_AGENTS_SPECIFICATION.md`](file:///home/alagiri/projects/bizosaas-platform/AI_AGENTS_SPECIFICATION.md) (to be created)

---

## RAG & Knowledge Augmented Generation (KAG)

### AI-Powered Knowledge System

BizOSaaS implements a sophisticated **RAG (Retrieval-Augmented Generation)** and **KAG (Knowledge-Augmented Generation)** system to enhance AI agent capabilities with contextual knowledge.

#### Architecture

**Vector Database**: PostgreSQL with pgvector extension
**Embedding Model**: OpenAI Embeddings (configurable)
**Storage**: Shared `bizosaas-postgres-staging` database

#### Core Capabilities

| Feature | Description | Implementation |
|---------|-------------|----------------|
| **Document Ingestion** | Ingest client documents, knowledge bases, product catalogs | `RAGService.ingest_knowledge()` |
| **Context Retrieval** | Retrieve relevant context for AI agent queries | `RAGService.retrieve_context()` |
| **Hybrid Search** | Combine vector similarity + keyword search | `RAGService.hybrid_search()` |
| **Agent-Specific Knowledge** | Isolate knowledge per agent or share globally | Metadata filtering |
| **Multi-Tenant Isolation** | Separate knowledge bases per client | Tenant ID filtering |

#### Use Cases

1. **Product Knowledge**: AI agents access product catalogs, specifications, pricing
2. **Customer History**: AI agents retrieve past interactions, preferences, purchase history
3. **Business Policies**: AI agents reference company policies, SLAs, guidelines
4. **Market Intelligence**: AI agents analyze competitor data, market trends
5. **Technical Documentation**: AI agents access API docs, integration guides

#### Data Flow

```
Client Upload → Document Chunking → Embedding Generation → pgvector Storage
                                                                    ↓
AI Agent Query → Query Embedding → Similarity Search → Context Retrieval → LLM Response
```

**Implementation**: [`app/core/rag.py`](file:///home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/brain-gateway/app/core/rag.py)

---

## External Service Connectors

### Connector Architecture

BizOSaaS provides **21 pre-built connectors** to integrate with external services, tools, and platforms. All connectors follow a unified architecture with standardized interfaces.

#### Connector Registry System

**Central Registry**: [`ConnectorRegistry`](file:///home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/brain-gateway/app/connectors/registry.py)
- Auto-discovery of available connectors
- Factory pattern for instantiation
- Credential validation
- Status monitoring

#### Available Connectors

##### CMS & Website Management (3)
| Connector | Type | Capabilities | Status |
|-----------|------|--------------|--------|
| **WordPress** | CMS | Posts, pages, media, users, comments | ✅ Active |
| **WooCommerce** | eCommerce | Products, orders, customers, inventory | ✅ Active |
| **Shopify** | eCommerce | Products, orders, customers, analytics | ✅ Active |

##### CRM & Marketing (4)
| Connector | Type | Capabilities | Status |
|-----------|------|--------------|--------|
| **FluentCRM** | CRM | Contacts, campaigns, tags, segments | ✅ Active |
| **Zoho CRM** | CRM | Leads, contacts, deals, activities | ✅ Active |
| **Google Analytics** | Analytics | Traffic, conversions, user behavior | ✅ Active |
| **Google Tag Manager** | Tag Management | Tags, triggers, variables | ✅ Active |

##### Advertising Platforms (5)
| Connector | Type | Capabilities | Status |
|-----------|------|--------------|--------|
| **Google Ads** | Advertising | Campaigns, ad groups, keywords, performance | ✅ Active |
| **Facebook Ads** | Advertising | Campaigns, ad sets, ads, insights | ✅ Active |
| **Pinterest Ads** | Advertising | Campaigns, pins, analytics | ✅ Active |
| **Snapchat Ads** | Advertising | Campaigns, creatives, metrics | ✅ Active |
| **Google Shopping** | eCommerce Ads | Product feeds, campaigns, performance | ✅ Active |

##### Communication & Messaging (3)
| Connector | Type | Capabilities | Status |
|-----------|------|--------------|--------|
| **WhatsApp Business** | Messaging | Send messages, templates, webhooks | ✅ Active |
| **Telegram** | Messaging | Bots, channels, messages | ✅ Active |
| **Email (SMTP)** | Email | Send emails, templates | ✅ Built-in |

##### Project Management & Billing (3)
| Connector | Type | Capabilities | Status |
|-----------|------|--------------|--------|
| **Plane** | Project Management | Workspaces, projects, issues, cycles | ✅ Active |
| **Trello** | Project Management | Boards, lists, cards, members | ✅ Active |
| **Lago** | Billing | Customers, subscriptions, invoices, usage | ✅ Active |

##### Other Integrations (3)
| Connector | Type | Capabilities | Status |
|-----------|------|--------------|--------|
| **Stripe** | Payments | Payments, subscriptions, customers | ⏳ Planned |
| **Slack** | Communication | Channels, messages, notifications | ⏳ Planned |
| **Zapier** | Automation | Triggers, actions, webhooks | ⏳ Planned |

#### Connector Workflow

**Setup Process** (Temporal Workflow):
1. **Credential Validation**: Verify API keys, OAuth tokens
2. **Connection Test**: Test API connectivity
3. **Credential Storage**: Securely store in Vault
4. **Initial Sync**: Import existing data
5. **Webhook Setup**: Configure real-time updates

**Sync Process** (Temporal Workflow):
1. **Incremental Sync**: Fetch new/updated data
2. **Data Transformation**: Normalize to BizOSaaS schema
3. **Storage**: Save to PostgreSQL
4. **Indexing**: Update vector embeddings (RAG)
5. **Event Emission**: Notify AI agents of changes

**Implementation Files**:
- **Connector Base**: [`app/connectors/base.py`](file:///home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/brain-gateway/app/connectors/base.py)
- **Registry**: [`app/connectors/registry.py`](file:///home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/brain-gateway/app/connectors/registry.py)
- **Workflows**: [`app/workflows/connector_setup.py`](file:///home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/brain-gateway/app/workflows/connector_setup.py)
- **API Routes**: [`app/api/connectors.py`](file:///home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/brain-gateway/app/api/connectors.py)

#### Client Dashboard Integration

**Connector Management UI** (Client Portal):
- **Discovery**: Browse available connectors
- **Connect**: OAuth flow or API key input
- **Status**: Real-time connection health
- **Sync**: Manual or scheduled data sync
- **Logs**: View sync history and errors
- **Disconnect**: Revoke access and delete credentials

**Data Visibility**:
- Imported data accessible via unified API
- AI agents automatically leverage connected data
- Cross-platform insights and automation

---

## Infrastructure Details

### Resource Allocation (KVM2 - Current)

| Component | CPU | RAM | Storage | Notes |
|-----------|-----|-----|---------|-------|
| PostgreSQL | 0.4 cores | 1 GB | 10 GB | Shared across all services |
| Redis | 0.1 cores | 256 MB | 2 GB | 10 DB indexes allocated |
| Vault | 0.1 cores | 128 MB | 1 GB | Secrets management |
| Temporal | 0.4 cores | 1 GB | 4 GB | Server + UI |
| Monitoring | 0.3 cores | 512 MB | 5 GB | Prometheus, Grafana, Loki |
| Brain Gateway | 0.3 cores | 768 MB | 2 GB | FastAPI + AI agents |
| Auth Service | 0.2 cores | 512 MB | 1 GB | FastAPI |
| Plane | 0.5 cores | 1.28 GB | 3 GB | 4 containers |
| Lago | 0.4 cores | 1 GB | 3 GB | 3 containers |
| Authentik | 0.3 cores | 768 MB | 2 GB | 2 containers |
| **Total** | **2.6 cores** | **7.2 GB** | **33 GB** | |

**KVM2 Capacity**: 2 vCPU, 8 GB RAM  
**Utilization**: 130% CPU (oversubscribed), 90% RAM  
**Recommendation**: Upgrade to KVM4 (4 vCPU, 8 GB RAM) for production

### Upgrade Path

**Staging (Current)**: KVM2 (2 vCPU, 8 GB RAM) - $10/mo  
**Production (Recommended)**: KVM4 (4 vCPU, 8 GB RAM) - $25/mo  
**Future Scale**: KVM8 (8 vCPU, 32 GB RAM) - $50/mo

---

## Deployment Configuration

### Environment Variables

**Shared Infrastructure**:
```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=BizOSaaS2025!StagingDB
POSTGRES_HOST=bizosaas-postgres-staging
POSTGRES_PORT=5432

REDIS_HOST=bizosaas-redis-staging
REDIS_PORT=6379

VAULT_ADDR=http://bizosaas-vault-staging:8200
VAULT_ROOT_TOKEN=staging-root-token-bizosaas-2025
```

**Service-Specific**:
- **Plane**: `PLANE_SECRET_KEY`, `PLANE_API_URL`, `PLANE_WEB_URL`
- **Lago**: `LAGO_SECRET_KEY_BASE`, `LAGO_RSA_PRIVATE_KEY`, `LAGO_ENCRYPTION_*`
- **Authentik**: `AUTHENTIK_SECRET_KEY`, `AUTHENTIK_POSTGRESQL__*`, `AUTHENTIK_REDIS__*`
- **Brain Gateway**: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `DATABASE_URL`, `REDIS_URL`

### Docker Compose Files

| File | Purpose | Services |
|------|---------|----------|
| [`dokploy-infrastructure-staging.yml`](file:///home/alagiri/projects/bizosaas-platform/dokploy-infrastructure-staging.yml) | Core infrastructure | Postgres, Redis, Vault, Temporal, Monitoring |
| [`dokploy-plane-staging.yml`](file:///home/alagiri/projects/bizosaas-platform/dokploy-plane-staging.yml) | Project management | Plane (web, API, worker, beat) |
| [`dokploy-lago-staging.yml`](file:///home/alagiri/projects/bizosaas-platform/dokploy-lago-staging.yml) | Billing | Lago (API, worker, front) |
| [`docker-compose.observability.yml`](file:///home/alagiri/projects/bizosaas-platform/docker-compose.observability.yml) | Monitoring (deprecated) | Merged into infrastructure |

### Deployment Guides

- **VPS Deployment**: [`vps_deployment_guide.md`](file:///home/alagiri/.gemini/antigravity/brain/00290556-3d78-45fe-b4b6-8349408a72f9/vps_deployment_guide.md)
- **Infrastructure Consolidation**: [`infrastructure_consolidation_plan.md`](file:///home/alagiri/.gemini/antigravity/brain/00290556-3d78-45fe-b4b6-8349408a72f9/infrastructure_consolidation_plan.md)
- **Capacity Analysis**: [`kvm2_capacity_analysis.md`](file:///home/alagiri/.gemini/antigravity/brain/00290556-3d78-45fe-b4b6-8349408a72f9/kvm2_capacity_analysis.md)

---

## Current Status & Next Steps

### Completed ✅
- [x] **Consolidated Infrastructure**: Single Postgres/Redis stack for all core services (Authentik, Lago, Plane, Gateway).
- [x] **Authentik Integration**: SSO implemented for Grafana and other internal tools.
- [x] **White-Labeling**: Custom branding (Logo, Title, Primary Colors) dynamically applied via Admin Dashboard.
- [x] **Smart Connector Discovery**: Automated WooCommerce/FluentCRM detection for WordPress and Magic Discovery for Google.
- [x] **WordPress Connector Fix**: Resolved 500 error and aligned credential keys.
- [x] **Marketing Hub**: Full-featured campaign management dashboard in Client Portal.
- [x] **Connector Registry expansion**: 30+ service connectors implemented and registered.
- [x] **Onboarding Magic**: Real-world Google Business Profile search and auto-fill.
- [x] **Background Auditing**: Automated presence audits via Temporal workflows.
- [x] **Task Transparency**: Live sync of implementation tasks from Plane.
- [x] **MCP Orchestration**: Automatic provisioning of tools based on user selection.
- [x] **AI Agent specialized roles**: Defined 7 core AI agent types with specific tools and capabilities.

### In Progress ⏳
- [ ] **Feasibility Engine**: AI loop for campaign strategy validation against historical connector data.
- [ ] **Advanced AI Agent Collaboration**: Agents talking to each other for cross-platform automation.

### Pending 📋
- [ ] **Multi-tenant Billing**: Automated invoicing via Lago based on connector usage.
- [ ] **Extended Agent Marketplace**: Scalability for 93+ specialized agents.
- [ ] **Security Hardening**: Vault production SEAL and Authentik MFA enforcement.

---

## References

- **GitHub Repository**: [Bizoholic-Digital/bizosaas-platform](https://github.com/Bizoholic-Digital/bizosaas-platform)
- **Credentials**: [`credentials.md`](file:///home/alagiri/projects/bizosaas-platform/credentials.md)
- **CI/CD Pipeline**: [`.github/workflows/ci-cd.yml`](file:///home/alagiri/projects/bizosaas-platform/.github/workflows/ci-cd.yml)
- **Task Tracking**: [`task.md`](file:///home/alagiri/.gemini/antigravity/brain/00290556-3d78-45fe-b4b6-8349408a72f9/task.md)

---

**Document Owner**: Platform Architecture Team  
**Last Updated**: January 2, 2026  
**Next Review**: February 2026