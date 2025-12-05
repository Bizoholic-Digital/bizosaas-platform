# BizOSaaS Ecosystem Tech Stack Reference

**Last Updated**: September 2025  
**Version**: 2.0 (Saleor Integration)

This document serves as the authoritative reference for the technology stack across the BizOSaaS ecosystem including Bizoholic Marketing, BizOSaaS Platform, and CoreLDove E-commerce.

## Architecture Overview

```
BizOSaaS Ecosystem Architecture
├── Core Platform (BizOSaaS)
│   ├── Multi-tenant SaaS platform
│   ├── BYOK (Bring Your Own Keys) architecture
│   ├── AI-powered marketing automation
│   └── Unified authentication system
├── Marketing Platform (Bizoholic)
│   ├── WordPress-based marketing sites
│   ├── Lead generation and nurturing
│   └── Content management
└── E-commerce Platform (CoreLDove)
    ├── Saleor-based e-commerce engine
    ├── AI product sourcing and optimization
    └── Integrated storefront and admin
```

## Core Technology Stack

### Frontend Technologies

#### Next.js 14 (App Router)
- **Usage**: Primary frontend framework for BizOSaaS and CoreLDove
- **Features**: Server-side rendering, static generation, API routes
- **Path**: `/frontend/` for main BizOSaaS dashboard
- **CoreLDove Integration**: Custom storefront connected to Saleor GraphQL API

#### React 18+ with TypeScript
- **Usage**: Component development across all frontends
- **State Management**: React hooks, Context API, Zustand for complex state
- **UI Framework**: ShadCN/UI with Tailwind CSS

#### Styling & UI
- **CSS Framework**: Tailwind CSS v3
- **Component Library**: ShadCN/UI (customized)
- **Icons**: Lucide React, Heroicons
- **Theme System**: Next-themes for dark/light mode support

### Backend Technologies

#### FastAPI (Python 3.11+)
- **Usage**: All microservices and API development
- **Features**: Async/await, automatic OpenAPI docs, dependency injection
- **Services**:
  - AI Agents Service (`/services/ai-agents/`)
  - Marketing Automation Service (`/services/marketing-automation-service/`)
  - Auth Service (`/services/auth-service-v2/`)
  - CoreLDove Bridge Service (`/services/coreldove-bridge-saleor/`)
  - Product Sourcing Service (`/services/coreldove-sourcing/`)
  - BYOK Health Monitor (`/services/byok-health-monitor/`)

#### Saleor E-commerce Platform
- **Version**: 3.20 (Official Docker Images)
- **Usage**: CoreLDove e-commerce backend
- **Components**:
  - Saleor API: GraphQL backend (`ghcr.io/saleor/saleor:3.20`)
  - Saleor Dashboard: Admin interface (`ghcr.io/saleor/saleor-dashboard:3.20`)
  - Celery Workers: Background task processing
  - Celery Beat: Scheduled tasks
- **Integration**: Custom bridge service connects Saleor to BizOSaaS ecosystem

#### CrewAI Framework
- **Usage**: Multi-agent AI workflows and automation
- **Agents**: Marketing, analytics, operations, ecommerce agents
- **Path**: `/services/ai-agents/agents/`

### Database & Storage

#### PostgreSQL 15+ with Extensions
- **Primary Database**: Multi-tenant architecture with RLS (Row Level Security)
- **Extensions**: 
  - `pgvector` for AI embeddings and similarity search
  - `uuid-ossp` for UUID generation
  - `hstore` for key-value storage
- **Databases**:
  - `bizosaas`: Main multi-tenant database
  - `coreldove_saleor`: Dedicated Saleor database
- **Connection**: Async with SQLAlchemy 2.0+ and asyncpg

#### Redis / Dragonfly
- **Usage**: Caching, session storage, event streaming
- **Features**: Redis Streams for event-driven architecture
- **Instances**:
  - Shared Redis: Main caching layer
  - CoreLDove Redis: E-commerce specific caching

### AI & ML Technologies

#### Large Language Models
- **Primary**: OpenAI GPT-4 and GPT-3.5-turbo
- **Alternative**: Anthropic Claude (via API)
- **Usage**: Content generation, analysis, optimization

#### AI Frameworks
- **CrewAI**: Multi-agent coordination and workflows
- **LangChain**: LLM application development
- **Embedding Models**: OpenAI text-embedding-ada-002

### Security & Authentication

#### HashiCorp Vault
- **Usage**: Secure credential storage and secrets management
- **Features**: BYOK credential resolution, API key encryption
- **Integration**: Python client with async support

#### FastAPI-Users
- **Usage**: Complete authentication system
- **Features**: JWT tokens, multi-tenant support, OAuth providers
- **Database**: SQLAlchemy models with user management

#### BYOK Architecture
- **Dual-mode credential resolution**: Platform-managed vs customer-provided keys
- **Health monitoring**: Automated credential validation and alerts
- **Billing integration**: Usage-based pricing with BYOK discounts

### Infrastructure & DevOps

#### Docker & Docker Compose
- **Containerization**: All services containerized
- **Development**: Docker Compose for local development
- **Key Files**:
  - `docker-compose.yml`: Main services
  - `docker-compose.coreldove-saleor.yml`: CoreLDove with Saleor
  - Individual service Dockerfiles

#### Orchestration
- **Development**: Docker Compose with shared infrastructure
- **Monitoring**: Health checks and service dependencies
- **Networking**: Custom bridge networks for service isolation

### Integration & APIs

#### Platform APIs
- **Google Ads API**: Campaign management and analytics
- **Meta Ads API**: Facebook/Instagram advertising
- **LinkedIn Marketing API**: B2B advertising platform
- **Amazon Product Advertising API**: Product sourcing

#### Workflow Automation
- **N8N**: Visual workflow automation engine
- **Temporal**: Reliable workflow orchestration (planned)
- **Integration**: Bridge services for external API connections

### Development Tools & Standards

#### Code Quality
- **Python**: Black formatting, isort imports, flake8 linting
- **TypeScript**: ESLint, Prettier formatting
- **Git Hooks**: Pre-commit hooks for code quality

#### API Documentation
- **FastAPI**: Automatic OpenAPI/Swagger documentation
- **GraphQL**: Saleor GraphQL playground and introspection

## Service Architecture

### Core Services (Port Assignments)

```yaml
Core_BizOSaaS_Services:
  frontend: 3000              # Next.js main dashboard
  ai_agents: 8000             # AI orchestration service
  auth_service: 8003          # Authentication & user management
  marketing_automation: 8020  # Consolidated marketing service
  byok_health_monitor: 8080   # BYOK credential monitoring
  
CoreLDove_Services:
  saleor_api: 8020           # Saleor GraphQL API
  saleor_dashboard: 9020     # Saleor admin interface
  coreldove_storefront: 3001 # Custom storefront
  coreldove_bridge: 8021     # Saleor-BizOSaaS bridge
  coreldove_sourcing: 8010   # AI product sourcing
  
Infrastructure_Services:
  postgresql: 5432           # Shared database
  redis: 6379               # Shared cache
  coreldove_redis: 6390     # E-commerce cache
  vault: 8200               # Secrets management
```

### Database Schema Design

#### Multi-tenant Foundation
```sql
-- Core tenant management
tenants, users, subscriptions, subscription_plans

-- Business data (tenant-scoped)
clients, leads, campaigns, reports

-- AI and vector storage
ai_insights, vector_store (with pgvector)

-- Security and sessions
user_sessions, security_events, rate_limits

-- Integrations and credentials
tenant_integrations, byok_credentials
```

#### Saleor Integration
```sql
-- Saleor-specific tables (in coreldove_saleor database)
-- Uses standard Saleor schema with custom metadata fields

-- Bridge tables (in main bizosaas database)
tenant_products (links tenants to Saleor products)
ai_workflows (workflow orchestration)
market_intelligence (AI-powered insights)
```

## Environment Configuration

### Required Environment Variables

#### Core Platform
```bash
# Database
POSTGRES_HOST=host.docker.internal
POSTGRES_USER=admin
POSTGRES_PASSWORD=securepassword
POSTGRES_DB=bizosaas

# Redis
REDIS_HOST=host.docker.internal
REDIS_PORT=6379

# Authentication
JWT_SECRET=your_jwt_secret
FASTAPI_USERS_SECRET=your_fastapi_users_secret

# Vault
VAULT_URL=http://host.docker.internal:8200
VAULT_TOKEN=your_vault_token
```

#### Saleor Configuration
```bash
# Saleor API
SALEOR_API_TOKEN=your_saleor_admin_token
SALEOR_SECRET_KEY=coreldove-saleor-secret-key-2025
DATABASE_URL=postgres://admin:securepassword@host.docker.internal:5432/coreldove_saleor

# Integration
BIZOSAAS_API_URL=http://host.docker.internal:8000
AI_AGENTS_URL=http://host.docker.internal:8000
```

#### External APIs (BYOK Compatible)
```bash
# Google Ads
GOOGLE_ADS_CLIENT_ID=your_client_id
GOOGLE_ADS_CLIENT_SECRET=your_client_secret
GOOGLE_ADS_DEVELOPER_TOKEN=your_developer_token

# Meta Ads
META_APP_ID=your_app_id
META_APP_SECRET=your_app_secret

# LinkedIn
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret

# Amazon Product Advertising
AMAZON_API_KEY=your_api_key
AMAZON_SECRET_KEY=your_secret_key
AMAZON_ASSOCIATE_TAG=your_associate_tag
```

## Development Workflow

### Starting the Platform

#### Shared Infrastructure First
```bash
cd /home/alagiri/projects/shared-development
docker-compose up -d postgres redis vault
```

#### BizOSaaS Core Platform
```bash
cd /home/alagiri/projects/bizoholic/bizosaas
npm run setup        # Copy environment template
npm run start:shared # Start with shared infrastructure
```

#### CoreLDove E-commerce
```bash
cd /home/alagiri/projects/bizoholic/bizosaas
./start-coreldove-saleor.sh  # Complete Saleor setup
```

### Key Development Commands
```bash
# Service management
npm run dev          # Start project services
npm run logs         # View service logs
npm run status       # Check service health

# Database operations
npm run db:migrate   # Run database migrations
npm run db:seed     # Seed development data

# Testing
npm run test        # Run test suite (when implemented)
npm run lint        # Code quality checks (when implemented)
```

## Integration Patterns

### BYOK Architecture Pattern
```python
# Dual-mode credential resolution
def get_platform_credentials(tenant_id: str, platform: str):
    if has_byok_credentials(tenant_id, platform):
        return get_tenant_credentials(tenant_id, platform)
    else:
        return get_platform_managed_credentials(platform)
```

### Event-Driven Communication
```python
# Redis Streams for cross-service events
await publish_event(
    stream="marketing.campaigns",
    event_type="campaign.created",
    data={"campaign_id": "...", "tenant_id": "..."}
)
```

### GraphQL Integration
```python
# Saleor GraphQL operations via bridge service
async def create_product_in_saleor(product_data: dict):
    result = await saleor_client.execute_async(
        PRODUCT_CREATE_MUTATION,
        variable_values={"input": product_data}
    )
    return result["productCreate"]["product"]
```

## Future Roadmap

### Planned Enhancements
- [ ] Terraform infrastructure as code
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Comprehensive monitoring with Prometheus/Grafana
- [ ] Advanced AI features and specialized agents
- [ ] Multi-cloud deployment options

### Technology Evaluations
- **Container Orchestration**: Evaluating k3s vs Docker Swarm
- **Service Mesh**: Considering Istio for microservices communication
- **Observability**: Planning integration of OpenTelemetry

---

## Quick Reference

### Architecture Decisions
- **E-commerce**: Saleor (official Docker images) instead of MedusaJS
- **Frontend**: Custom BizOSaaS frontend instead of official Saleor storefront
- **Auth**: Unified authentication across all platforms
- **AI**: CrewAI for multi-agent workflows
- **Database**: PostgreSQL with multi-tenant RLS
- **Cache**: Redis with service-specific instances

### Key Principles
1. **Containerization First**: All services in Docker containers
2. **Multi-tenant by Design**: Tenant isolation at database level
3. **BYOK Architecture**: Customer credential autonomy
4. **API-First Development**: GraphQL and REST APIs for all integrations
5. **Event-Driven Communication**: Async messaging between services
6. **AI-Powered Automation**: Intelligence embedded throughout the platform

This reference should be updated as the architecture evolves and new technologies are adopted.