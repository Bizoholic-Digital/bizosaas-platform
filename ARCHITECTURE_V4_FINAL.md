# BizOSaaS Platform Architecture V4 (Final)
## AI Agent Orchestration Platform with Hexagonal Architecture & External System Connectors

**Date**: 2025-12-11  
**Version**: 4.0 (Hexagonal + Connector-First + Admin Separation)  
**Architecture Pattern**: iPaaS + Hexagonal (Ports & Adapters) + Multi-Portal

---

## Executive Summary

### Platform Philosophy: "Brain-First, Connector-Everything, Hexagonal-Always"

**BizOSaaS is NOT a CRM, CMS, or E-commerce platform.**

BizOSaaS is an **AI Agent Orchestration Platform** that:
- ✅ Hosts 93+ specialized AI agents (CrewAI)
- ✅ Hosts workflow orchestration (Temporal)
- ✅ Hosts secrets management (HashiCorp Vault)
- ✅ Hosts authentication & authorization (FastAPI-Users + Authentik SSO)
- ✅ **Connects to** external CRM, CMS, Commerce, Analytics, Billing systems
- ✅ **Follows hexagonal architecture** (Ports & Adapters pattern)
- ✅ **Separates client and admin portals** for security and UX

---

## Part 1: Key Architectural Decisions

### Decision 1: Hexagonal Architecture (Ports & Adapters)

**Rationale**: Decouple business logic from infrastructure concerns

```
┌─────────────────────────────────────────────────────────────┐
│                    HEXAGONAL ARCHITECTURE                    │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              PRESENTATION LAYER (Adapters)              │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │ │
│  │  │ Client Portal│  │Admin Dashboard│  │  REST API    │  │ │
│  │  │  (Next.js)   │  │  (Next.js)    │  │  (FastAPI)   │  │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
│                            ↓                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                  DOMAIN LAYER (Core)                    │ │
│  │                                                          │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │           Domain Services (Business Logic)        │  │ │
│  │  │  • ConnectorService                               │  │ │
│  │  │  • SecretService                                  │  │ │
│  │  │  • AgentService                                   │  │ │
│  │  │  • WorkflowService                                │  │ │
│  │  └──────────────────────────────────────────────────┘  │ │
│  │                                                          │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │              Ports (Interfaces)                   │  │ │
│  │  │  • ConnectorPort                                  │  │ │
│  │  │  • SecretPort                                     │  │ │
│  │  │  • AgentPort                                      │  │ │
│  │  │  • WorkflowPort                                   │  │ │
│  │  │  • CRMPort, CMSPort, EcommercePort, etc.         │  │ │
│  │  └──────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
│                            ↓                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           INFRASTRUCTURE LAYER (Adapters)              │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │ │
│  │  │VaultAdapter  │  │TemporalAdptr │  │LLMAdapter    │  │ │
│  │  │(Production)  │  │              │  │              │  │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │ │
│  │  │EnvSecretAdptr│  │GoogleAnalytics│  │TrelloConnector│  │ │
│  │  │(Development) │  │Connector      │  │              │  │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Benefits**:
- ✅ Business logic independent of frameworks
- ✅ Easy to swap implementations (dev vs prod)
- ✅ Highly testable (mock adapters)
- ✅ Clear separation of concerns

### Decision 2: Separate Admin Dashboard

**Rationale**: Security, UX, and scalability

| Portal | Purpose | Users | Features |
|--------|---------|-------|----------|
| **Client Portal** | Tenant operations | Tenant users, Tenant admins | Dashboard, CRM view, CMS view, Analytics, Integrations (view only), Settings |
| **Admin Dashboard** | Platform management | Platform admins, Super admins | Tenant management, AI agent playground, Agent fine-tuning, System monitoring, Connector registry, Feature flags |

**Access Control**:
```
┌──────────────────┬─────────────┬──────────────┬────────────────┬──────────────┐
│ Feature          │ Tenant User │ Tenant Admin │ Platform Admin │ Super Admin  │
├──────────────────┼─────────────┼──────────────┼────────────────┼──────────────┤
│ View Dashboard   │      ✅     │      ✅      │       ✅       │      ✅      │
│ Manage Integ.    │      ❌     │      ✅      │       ✅       │      ✅      │
│ View AI Agents   │      ✅     │      ✅      │       ✅       │      ✅      │
│ Configure Agents │      ❌     │      ❌      │       ✅       │      ✅      │
│ Fine-tune Agents │      ❌     │      ❌      │       ❌       │      ✅      │
│ Platform Mgmt    │      ❌     │      ❌      │       ✅       │      ✅      │
│ Tenant Mgmt      │      ❌     │      ❌      │       ✅       │      ✅      │
│ System Settings  │      ❌     │      ❌      │       ❌       │      ✅      │
└──────────────────┴─────────────┴──────────────┴────────────────┴──────────────┘
```

### Decision 3: Secret Management Strategy

**Development**: `.env` files → `EnvSecretAdapter` (in-memory)
**Staging/Production**: HashiCorp Vault → `VaultAdapter`

```python
# Development
secret_service = SecretService(EnvSecretAdapter())

# Production
secret_service = SecretService(VaultAdapter(
    vault_url="http://vault:8200",
    vault_role_id=os.getenv("VAULT_ROLE_ID"),
    vault_secret_id=os.getenv("VAULT_SECRET_ID")
))
```

---

## Part 2: Complete System Architecture

### 2.1 Portal Structure

```
portals/
├── client-portal/              # Tenant-facing (Port 3003)
│   ├── app/
│   │   ├── dashboard/          # Main dashboard
│   │   ├── crm/                # CRM data view (from external CRM)
│   │   ├── cms/                # CMS content view (from external CMS)
│   │   ├── analytics/          # Analytics dashboards
│   │   ├── integrations/       # View connector status
│   │   └── settings/           # Tenant settings
│   ├── components/             # 47+ UI components
│   └── lib/                    # Utilities
│
├── admin-dashboard/            # Platform admin (Port 3004) [TO BE CREATED]
│   ├── app/
│   │   ├── platform/           # Platform management
│   │   │   ├── tenants/        # Tenant CRUD
│   │   │   ├── health/         # Service health
│   │   │   ├── monitoring/     # Resource monitoring
│   │   │   └── billing/        # Billing overview
│   │   ├── ai-agents/          # AI agent management
│   │   │   ├── playground/     # Full agent playground
│   │   │   ├── metrics/        # Performance metrics
│   │   │   ├── fine-tuning/    # Model fine-tuning
│   │   │   ├── prompts/        # Prompt engineering
│   │   │   └── config/         # Model configuration
│   │   ├── connectors/         # Connector management
│   │   │   ├── registry/       # Global connector registry
│   │   │   ├── oauth-apps/     # OAuth app configuration
│   │   │   ├── rate-limits/    # API rate limits
│   │   │   └── health/         # Connector health
│   │   └── system/             # System settings
│   │       ├── feature-flags/  # Feature flags
│   │       ├── environment/    # Environment config
│   │       ├── security/       # Security policies
│   │       └── audit/          # Audit logs
│   └── components/             # Admin-specific components
│
└── shared/                     # Shared components
    ├── ui/                     # Shadcn components
    ├── hooks/                  # React hooks
    ├── utils/                  # Utilities
    └── types/                  # TypeScript types
```

### 2.2 Brain Gateway Structure (Hexagonal)

```
brain-gateway/
├── app/
│   ├── domain/                         # CORE BUSINESS LOGIC
│   │   ├── services/                   # Domain services
│   │   │   ├── connector_service.py    # Connector orchestration
│   │   │   ├── secret_service.py       # Secret management
│   │   │   ├── agent_service.py        # Agent orchestration
│   │   │   └── workflow_service.py     # Workflow orchestration
│   │   └── models/                     # Domain models
│   │       ├── connector.py
│   │       ├── credential.py
│   │       ├── agent.py
│   │       └── workflow.py
│   │
│   ├── ports/                          # INTERFACES (Contracts)
│   │   ├── connector_port.py           # Connector interface
│   │   ├── secret_port.py              # Secret management interface
│   │   ├── agent_port.py               # Agent interface
│   │   ├── workflow_port.py            # Workflow interface
│   │   ├── crm_port.py                 # CRM operations
│   │   ├── cms_port.py                 # CMS operations
│   │   ├── ecommerce_port.py           # E-commerce operations
│   │   ├── analytics_port.py           # Analytics operations
│   │   └── task_port.py                # Task management
│   │
│   ├── adapters/                       # INFRASTRUCTURE IMPLEMENTATIONS
│   │   ├── env_secret_adapter.py       # Dev: In-memory secrets
│   │   ├── vault_adapter.py            # Prod: HashiCorp Vault
│   │   ├── temporal_adapter.py         # Temporal workflows
│   │   └── llm_adapter.py              # LLM providers
│   │
│   ├── connectors/                     # CONNECTOR IMPLEMENTATIONS
│   │   ├── base.py                     # Base connector
│   │   ├── oauth_mixin.py              # OAuth functionality
│   │   ├── registry.py                 # Connector registry
│   │   ├── google_analytics.py         # GA4 connector
│   │   ├── trello.py                   # Trello connector
│   │   ├── wordpress.py                # WordPress connector
│   │   └── ... (50+ connectors)
│   │
│   ├── routers/                        # API ENDPOINTS (Presentation)
│   │   ├── oauth.py                    # OAuth flows
│   │   ├── connectors.py               # Connector management
│   │   ├── agents.py                   # AI agent interactions
│   │   ├── admin.py                    # Admin operations
│   │   └── webhooks.py                 # Webhook handlers
│   │
│   ├── workflows/                      # TEMPORAL WORKFLOWS
│   │   ├── connector_setup.py          # Connector setup workflow
│   │   └── connector_sync.py           # Data sync workflow
│   │
│   ├── activities.py                   # Temporal activities
│   ├── dependencies.py                 # Dependency injection
│   └── middleware/                     # Middleware
│       ├── auth.py                     # Authentication
│       ├── tenant.py                   # Tenant context
│       └── audit.py                    # Audit logging
│
├── main.py                             # FastAPI application
├── worker.py                           # Temporal worker
└── requirements.txt                    # Dependencies
```

### 2.3 Data Flow: OAuth Connector Setup (Hexagonal)

```
┌─────────────────┐
│  Client Portal  │
│  (Presentation) │
└────────┬────────┘
         │ 1. Click "Connect Google Analytics"
         ↓
┌─────────────────────────────────┐
│   Brain Gateway (Router)        │
│   POST /oauth/authorize/ga4     │
└────────┬────────────────────────┘
         │ 2. Delegate to domain service
         ↓
┌─────────────────────────────────┐
│  ConnectorService (Domain)      │
│  - Validates input              │
│  - Orchestrates OAuth flow      │
└────────┬────────────────────────┘
         │ 3. Get auth URL via port
         ↓
┌─────────────────────────────────┐
│  ConnectorPort (Interface)      │
│  get_auth_url()                 │
└────────┬────────────────────────┘
         │ 4. Implementation
         ↓
┌─────────────────────────────────┐
│  GoogleAnalyticsConnector       │
│  (Adapter - implements          │
│   OAuthMixin + ConnectorPort)   │
│  - Builds Google OAuth URL      │
└────────┬────────────────────────┘
         │ 5. Return URL to user
         ↓
┌─────────────────────────────────┐
│  User redirected to Google      │
│  Authorizes app                 │
└────────┬────────────────────────┘
         │ 6. Google redirects back with code
         ↓
┌─────────────────────────────────┐
│  Brain Gateway (Router)         │
│  POST /oauth/callback           │
└────────┬────────────────────────┘
         │ 7. Delegate to service
         ↓
┌─────────────────────────────────┐
│  ConnectorService (Domain)      │
│  - Exchange code for tokens     │
└────────┬────────────────────────┘
         │ 8. Store credentials
         ↓
┌─────────────────────────────────┐
│  SecretService (Domain)         │
│  - Encrypts sensitive data      │
│  - Adds metadata                │
└────────┬────────────────────────┘
         │ 9. Persist via port
         ↓
┌─────────────────────────────────┐
│  SecretPort (Interface)         │
│  store_secret()                 │
└────────┬────────────────────────┘
         │ 10. Implementation
         ↓
┌─────────────────────────────────┐
│  VaultAdapter (Infrastructure)  │
│  - Connects to HashiCorp Vault  │
│  - Stores encrypted credentials │
└─────────────────────────────────┘
```

**Key Points**:
- ✅ Router only handles HTTP concerns
- ✅ Business logic in domain services
- ✅ Ports define contracts
- ✅ Adapters implement infrastructure
- ✅ Easy to swap implementations (dev/prod)

---

## Part 3: External Systems (NOT Hosted)

### What BizOSaaS CONNECTS TO

| Category | Examples | Integration Method |
|----------|----------|----------------------|
| **CRM Systems** | Zoho CRM, HubSpot, Salesforce, Pipedrive, Freshsales | REST API + OAuth 2.0 |
| **CMS Systems** | WordPress, Drupal, Webflow, Contentful, Strapi | REST API + API Keys |
| **E-commerce** | Shopify, WooCommerce, BigCommerce, Magento, Saleor | REST/GraphQL API |
| **Analytics** | Google Analytics 4, Mixpanel, Amplitude, Posthog | REST API + OAuth |
| **Email Marketing** | Mailchimp, SendGrid, Klaviyo, ActiveCampaign | REST API |
| **Advertising** | Google Ads, Meta Ads, LinkedIn Ads, TikTok Ads | REST API + OAuth |
| **Social Media** | Facebook, Instagram, LinkedIn, Twitter, Pinterest | REST API + OAuth |
| **Payment/Billing** | Stripe, PayPal, Square, Razorpay | REST API + Webhooks |
| **Communication** | Twilio, WhatsApp Business, Telegram, Slack | REST API |
| **Storage** | AWS S3, Google Cloud Storage, Cloudflare R2 | SDK/REST API |
| **LLM Providers** | OpenAI, Anthropic, Google AI, Azure OpenAI, Groq | REST API |

**Important**: BizOSaaS does NOT store CRM contacts, CMS content, or e-commerce products. It only stores:
- User/tenant metadata
- Connector configurations
- Audit logs
- Workflow state
- AI agent conversations

---

## Part 4: AI Agent Layer (93+ Agents)

### Agent Categories

| Category | Count | Examples |
|----------|-------|----------|
| **Marketing** | 9 | MarketingStrategist, ContentCreator, SEOSpecialist, SocialMediaManager |
| **E-commerce** | 13 | ProductSourcing, PriceOptimization, InventoryManagement, FraudDetection |
| **Analytics** | 8 | DigitalPresenceAudit, PerformanceAnalytics, ReportGenerator, ROIAnalysis |
| **CRM** | 7 | ContactIntelligence, LeadScoring, SalesAssistant, SentimentAnalysis |
| **Operations** | 8 | LeadQualification, ClientOnboarding, ProjectCoordination, QualityAssurance |
| **Workflow Crews** | 10 | OnboardingCrew, CampaignStrategyCrew, ContentApprovalCrew |
| **Orchestration** | 3 | HierarchicalCrewOrchestrator, WorkflowEngine, AgentCoordinator |

### Agent-Connector Interaction

```python
# Example: ContentCreator agent publishing to WordPress

class ContentCreatorAgent:
    def __init__(self, connector_service: ConnectorService):
        self.connector_service = connector_service
    
    async def publish_blog_post(self, tenant_id: str, post_data: dict):
        # 1. Get WordPress connector via service
        result = await self.connector_service.sync_connector_data(
            tenant_id=tenant_id,
            connector_id="wordpress",
            resource_type="posts",
            params={"action": "create", "data": post_data}
        )
        
        # 2. Return result
        return result
```

**Key Point**: Agents use domain services, NOT direct connector access. This maintains hexagonal architecture.

---

## Part 5: Implementation Roadmap

### Phase 1: Hexagonal Architecture Foundation ✅ (COMPLETED)
- [x] Create `SecretPort` interface
- [x] Implement `EnvSecretAdapter` (development)
- [x] Implement `VaultAdapter` (production)
- [x] Create `SecretService` domain service
- [x] Create `ConnectorService` domain service
- [x] Refactor OAuth router to use services

### Phase 2: Admin Dashboard Creation (IN PROGRESS)
- [ ] Create `admin-dashboard` portal structure
- [ ] Implement platform management features
- [ ] Build AI agent playground (enhanced)
- [ ] Add tenant management
- [ ] Implement system monitoring
- [ ] Add feature flags

### Phase 3: Vault Integration (Staging Prep)
- [ ] Set up HashiCorp Vault (Docker)
- [ ] Configure AppRole authentication
- [ ] Migrate credential storage from dev to Vault
- [ ] Implement secret rotation
- [ ] Add Vault health checks

### Phase 4: Temporal Workflow Setup
- [ ] Fix Temporal server setup (docker-compose)
- [ ] Verify worker connectivity
- [ ] Test connector setup workflow
- [ ] Test connector sync workflow
- [ ] Add workflow monitoring

### Phase 5: OAuth Completion
- [ ] Add real OAuth credentials (Google, Meta, etc.)
- [ ] Test end-to-end OAuth flows
- [ ] Implement token refresh
- [ ] Add OAuth error handling
- [ ] Wire manual integrations

### Phase 6: Full Platform Audit
- [ ] Wire all dashboard widgets to real data
- [ ] Connect CRM views to external CRMs
- [ ] Connect CMS views to external CMSs
- [ ] Verify all 93 agents are functional
- [ ] Performance testing
- [ ] Security audit

---

## Part 6: Key Architectural Principles

### 1. **Hexagonal Architecture (Ports & Adapters)**
- Domain logic is independent of frameworks
- Ports define contracts (interfaces)
- Adapters implement infrastructure
- Easy to test and swap implementations

### 2. **Connector-First Philosophy**
- BizOSaaS connects to external systems
- No duplication of CRM/CMS/Commerce data
- Real-time data fetching
- Credentials stored securely in Vault

### 3. **AI Agent Orchestration**
- 93+ specialized agents
- Agents use tools (connectors) to interact with external systems
- CrewAI for agent collaboration
- Temporal for long-running workflows

### 4. **Multi-Portal Strategy**
- Client Portal: Tenant operations
- Admin Dashboard: Platform management
- Shared components for consistency
- Role-based access control

### 5. **Secret Management**
- Development: `.env` → `EnvSecretAdapter`
- Production: HashiCorp Vault → `VaultAdapter`
- Automatic secret rotation
- Audit logging

### 6. **Event-Driven Architecture**
- Redis Streams for event bus
- Domain events for decoupling
- Async event handlers
- Temporal for complex workflows

---

## Part 7: Technology Stack

### Core Platform (Hosted)
| Component | Technology | Purpose |
|-----------|------------|---------|
| **API Gateway** | FastAPI | Brain Gateway - single entry point |
| **AI Agents** | CrewAI + LangChain | 93+ specialized agents |
| **Workflows** | Temporal | Long-running workflows, HITL |
| **Secrets** | HashiCorp Vault | Credential storage, rotation |
| **Auth** | FastAPI-Users + Authentik | Multi-tenant auth, SSO, RBAC |
| **Database** | PostgreSQL | Platform data (users, tenants, configs) |
| **Cache** | Redis | Sessions, cache, event streams |
| **Event Bus** | Redis Streams | Event-driven communication |
| **Observability** | Prometheus/Grafana/Loki | Metrics, logs, dashboards |

### Portals (Hosted)
| Portal | Technology | Port | Purpose |
|--------|------------|------|---------|
| **Client Portal** | Next.js 15 (PWA) | 3003 | Tenant operations |
| **Admin Dashboard** | Next.js 15 | 3004 | Platform management |

### External Systems (NOT Hosted)
- CRM: Zoho, HubSpot, Salesforce, etc.
- CMS: WordPress, Drupal, Webflow, etc.
- E-commerce: Shopify, WooCommerce, etc.
- Analytics: Google Analytics, Mixpanel, etc.
- LLMs: OpenAI, Anthropic, Google AI, etc.

---

## Conclusion

This architecture provides:
- ✅ **Hexagonal design** for maintainability and testability
- ✅ **Connector-first** approach for external system integration
- ✅ **Separate portals** for security and UX
- ✅ **Secret management** strategy (dev → staging → prod)
- ✅ **AI agent orchestration** with 93+ specialized agents
- ✅ **Scalable infrastructure** with clear separation of concerns

**Next Steps**: Proceed with Phase 2 (Admin Dashboard) and Phase 3 (Vault Integration) while continuing to refine the hexagonal architecture.
