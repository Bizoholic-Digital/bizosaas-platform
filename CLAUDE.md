# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BizOSaaS Platform is a comprehensive multi-tenant SaaS ecosystem built with **Domain-Driven Design (DDD)** principles and modern microservices architecture. The platform includes 7 independent frontend applications (marketing sites, client portals, admin dashboards), FastAPI backend services, Wagtail CMS, n8n workflow automation, and **93+ CrewAI AI agents** that autonomously manage the entire platform.

**🏗️ Architecture Principles:**
- **DDD (Domain-Driven Design)**: Each frontend is a separate bounded context in its own container
- **Modular & Isolated**: Independent deployment, scaling, and maintenance
- **Autonomous AI**: 93+ CrewAI agents handle 80%+ of operations
- **Event-Driven**: Services communicate via Brain Gateway orchestration

**📚 CRITICAL REFERENCE DOCUMENT:**
See [BIZOSAAS_UNIFIED_FRONTEND_ARCHITECTURE.md](/home/alagiri/projects/BIZOSAAS_UNIFIED_FRONTEND_ARCHITECTURE.md) for complete frontend development standards, tech stack, authentication patterns, DDD architecture, CrewAI agent details, and deployment workflows.

## Core Tech Stack (2025)

### Frontend Standard Stack
- **Framework**: Next.js 15.5.3 + React 18.0.0 (NOT React 19 - ecosystem not ready)
- **Styling**: Tailwind CSS 3.4.0 + PostCSS
- **Component Libraries**:
  - shadcn/ui (Radix UI + Tailwind) - Base components
  - Aceternity UI - Animated marketing components
  - Magic UI - Interactive 3D effects
- **State Management**: Zustand 4.4.7
- **Server State**: @tanstack/react-query 5.15.0
- **Forms**: react-hook-form 7.48.2 + Zod 3.22.4
- **Icons**: Lucide React 0.400.0
- **Charts**: Recharts 2.8.0

### Backend Standard Stack
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with pgvector
- **Cache**: Redis
- **CMS**: Wagtail (Headless)
- **Workflows**: n8n
- **Container Orchestration**: Docker Swarm
- **Deployment**: Dokploy (Self-hosted PaaS)
- **Reverse Proxy**: Traefik with Let's Encrypt SSL

### Authentication Architecture
**CRITICAL: We use FastAPI Brain Gateway for ALL authentication (NOT NextAuth.js)**

- **Brain Gateway** (Port 8001): Multi-tenant auth + API gateway
- **Auth Pattern**: JWT with httpOnly cookies
- **Frontend**: React Context API (AuthContext + useAuth hook)
- **Multi-tenancy**: Tenant-scoped data with tenant switching
- **Security**: Rate limiting, CORS, CSRF protection

**Why NOT NextAuth.js?**
- Multi-tenancy already implemented in FastAPI
- Single source of truth across all clients (web, mobile, API)
- Better performance (fewer hops)
- Simpler Next.js (presentation layer only)

## Development Commands

### Shared Infrastructure Mode (Recommended)
```bash
# Setup environment (copies .env.example to .env)
npm run setup

# Start project with shared infrastructure (recommended)
npm run start:shared    # Uses start-project.sh script

# Alternative manual commands
npm run dev:project     # Start project-specific services only
npm run dev             # Alias for dev:project

# Individual services
npm run dev:crewai      # Start CrewAI service only
npm run dev:wordpress   # Start WordPress service only

# Management commands
npm run build           # Build project services
npm run start           # Start in daemon mode
npm run stop            # Stop all project services
npm run status          # Check service status

# Logging
npm run logs            # View all service logs
npm run logs:crewai     # View CrewAI logs only
npm run logs:wordpress  # View WordPress logs only

# Utilities
npm run check:shared    # Check shared infrastructure status
```

### Legacy Mode (Self-Contained)
```bash
# Use original docker-compose.yml (includes all infrastructure)
npm run dev:legacy

# Deploy to production
npm run deploy
```

### Testing
- No test suite configured yet (`npm test` returns placeholder)
- No linting configured yet (`npm lint` returns placeholder)

## Architecture

### Frontend Applications (Next.js) - DDD Bounded Contexts

Each frontend is a **separate domain** in its **own container**:

| Domain | Container | Path | Port | Purpose |
|--------|-----------|------|------|---------|
| **Bizoholic** (Marketing) | Independent | `bizosaas/misc/services/bizoholic-frontend` | 3001 | Marketing agency services |
| **CoreLDove** (Ecommerce) | Independent | `bizosaas/ecommerce/services/coreldove-frontend` | 3002 | E-commerce storefront |
| **ThrillRing** (Gaming) | Independent | `bizosaas/frontend/apps/thrillring-gaming` | 3003 | Gaming platform |
| **Client Portal** (SaaS) | Independent | `bizosaas/frontend/apps/client-portal` | 3000 | Multi-tenant dashboard |
| **Business Directory** (Listings) | Independent | `bizosaas/frontend/apps/business-directory` | 3004 | Business profiles |
| **BizOSaaS Admin** (Platform) | Independent | `bizosaas/frontend/apps/bizosaas-admin` | 3009 | Super admin |
| **Analytics** (Insights) | Independent | `bizosaas/frontend/apps/analytics-dashboard` | 3005 | Data visualization |

**DDD Principles Applied:**
- ✅ Each domain has its own container (isolated)
- ✅ Independent deployment and scaling
- ✅ Separate codebases (modular)
- ✅ Domain-specific logic encapsulated
- ✅ Communicate via Brain Gateway (loose coupling)

**All frontends use:**
- Next.js 15.5.3 + React 18.0.0
- FastAPI Brain Gateway authentication
- AuthContext pattern (NOT NextAuth.js)
- shadcn/ui + Aceternity UI + Magic UI
- Docker deployment via GHCR
- **93+ CrewAI agents** via Brain Gateway

### Backend Services (FastAPI/Python)

| Service | Container | Port | Purpose |
|---------|-----------|------|---------|
| **Brain Gateway** | Independent | 8001 | Multi-tenant auth + API gateway + Agent orchestration |
| **FastAPI Core** | Independent | 8000 | Main backend services |
| **Wagtail CMS** | Independent | 8002 | Headless CMS for content |
| **CrewAI Agents** | Independent | 8003 | 93+ AI agents (autonomous operations) |
| **n8n Workflows** | Independent | 5678 | Workflow automation engine |

### 93+ CrewAI AI Agents (Autonomous Platform)

The platform is **autonomously managed** by 93+ specialized CrewAI agents organized into domains:

- 🤖 **Marketing Ecosystem** (15 agents) - Campaign strategy, competitor analysis, budget optimization
- 🤖 **Content Generation** (12 agents) - Blog posts, social captions, email campaigns, ad copy
- 🤖 **SEO Optimization** (10 agents) - Keyword research, technical audits, backlink analysis
- 🤖 **Social Media Management** (8 agents) - Content scheduling, engagement, influencer discovery
- 🤖 **Campaign Optimization** (9 agents) - Google/Facebook/LinkedIn ads optimization
- 🤖 **Analytics & Reporting** (11 agents) - GA4 analysis, predictive analytics, forecasting
- 🤖 **Customer Service** (7 agents) - Chatbot, ticket routing, satisfaction analysis
- 🤖 **Lead Generation** (6 agents) - Lead scoring, nurture sequences, qualification
- 🤖 **Email Marketing** (5 agents) - Subject line optimization, send time, segmentation
- 🤖 **Reputation Management** (4 agents) - Review responses, sentiment monitoring
- 🤖 **Additional Domains** (21 agents) - Web analytics, CRO, influencer marketing, etc.

**How It Works:**
```
Frontend → Brain Gateway → CrewAI Orchestrator → Agents (parallel execution)
                                                    ↓
                                            Results aggregated
                                                    ↓
                                        Frontend receives response
```

**Key Benefits:**
- ✨ 80%+ of operations automated
- ✨ 24/7 autonomous operation
- ✨ Consistent quality (no human error)
- ✨ Scales infinitely
- ✨ Data-driven decisions

See [BIZOSAAS_UNIFIED_FRONTEND_ARCHITECTURE.md](/home/alagiri/projects/BIZOSAAS_UNIFIED_FRONTEND_ARCHITECTURE.md) Section 1.1 for complete agent documentation.

### Shared Infrastructure Mode (Current)
The platform now uses shared development infrastructure with project-specific services:

#### Shared Services (External)
- **PostgreSQL Database**: `shared-postgres-dev` at `localhost:5432`
  - **Database**: `bizoholic` (dedicated database in shared instance)
  - **Features**: pgvector extension for AI embeddings, multi-tenant schema
- **Redis Cache**: `shared-redis-dev` at `localhost:6379`
  - **Purpose**: High-performance caching and session storage
- **n8n Workflow Engine**: `shared-n8n-dev` at `localhost:5678`
  - **Purpose**: Shared automation engine across all projects
  - **Workflows**: Can be project-specific or shared

#### Project-Specific Services
### 1. CrewAI Agent System (Port 8000)
- **Location**: `n8n/crewai/` directory
- **Language**: Python with FastAPI
- **Connection**: Uses `host.docker.internal` to connect to shared infrastructure
- **Agents**: Marketing ecosystem, report generation, reputation, social media, website audit
- **Key Dependencies**: `crewai==0.24.0`, `fastapi==0.104.1`, `langchain==0.1.0`

### 2. WordPress Frontend (Legacy - Being Replaced)
- **Image**: `wordpress:6.4-php8.1-apache`
- **Purpose**: Bizoholic-specific client dashboards (being migrated to Next.js Client Portal)
- **Custom Content**: Located in `n8n/wordpress/` directory
- **Status**: Phasing out in favor of Next.js Client Portal

### Legacy Architecture (Self-Contained)
For reference, the original architecture included all services locally:
- Local PostgreSQL with pgvector
- Local Dragonfly/Redis cache  
- Local n8n instance
- Local pgAdmin for development

## Database Schema

The database uses a multi-tenant architecture with these key schemas:

- **Multi-tenant Foundation**: `tenants`, `users`, `subscriptions`, `subscription_plans`
- **Business Data**: `clients`, `leads`, `campaigns`, `reports` (all tenant-scoped)
- **AI Components**: `ai_insights`, `vector_store` with pgvector support
- **Security**: `user_sessions`, `security_events`, `rate_limits`
- **Integrations**: `tenant_integrations` for API credentials per tenant

## Key Integrations

The platform is designed to integrate with:

- **AI Services**: OpenAI, Anthropic Claude, LangChain
- **Advertising Platforms**: Google Ads, Meta Ads, LinkedIn Marketing
- **Payment Processing**: Stripe with webhook support
- **Email Services**: SMTP (Resend), marketing automation
- **Analytics**: SERP API, Screaming Frog for SEO
- **CRM Systems**: HubSpot, Pipedrive

## Environment Configuration

Critical environment variables (see `n8n/ENV-TEMPLATE.env`):

**Required for basic functionality:**
- `POSTGRES_PASSWORD`
- `JWT_SECRET` 
- `OPENAI_API_KEY`
- `N8N_PASSWORD`

**Required for full functionality:**
- All advertising platform API keys
- Stripe payment keys
- SMTP credentials
- External service API keys

## File Structure

```
bizoholic/
├── package.json                 # Main project configuration and scripts
├── docker-compose.yml           # Legacy service orchestration (backup)
├── docker-compose.project.yml   # Project-specific services for shared infrastructure
├── start-project.sh            # Automated startup script with shared infrastructure checks
├── .env.example                # Environment configuration template (shared infrastructure)
├── n8n/                        # Main application directory
│   ├── crewai/                 # AI agent system (Python/FastAPI)
│   ├── workflows/              # n8n automation workflows
│   ├── wordpress/              # WordPress customizations
│   ├── database/              # Database migrations and init scripts
│   ├── automation/            # Deployment and setup scripts
│   └── ENV-TEMPLATE.env       # Legacy environment template
└── k8s-complete.yaml          # Kubernetes deployment (alternative)
```

## Development Workflow

### Frontend Development Workflow (CRITICAL)

**GitHub + GHCR as Single Source of Truth**

```
Development Cycle:
1. Pull latest code from GitHub
2. Pull latest images from GHCR
3. Work locally (WSL2 containers)
4. Test locally
5. Commit changes to GitHub
6. Build Docker image
7. Push to GHCR with multiple tags:
   - :staging
   - :latest
   - :working-YYYY-MM-DD
8. Deploy to staging from GHCR
9. Test on staging
10. Tag as :production
11. Deploy to production from GHCR

❌ NEVER build Docker images on production
❌ NEVER skip GitHub/GHCR sync
✅ ALWAYS deploy from GHCR (never local builds)
✅ ALWAYS maintain at least 3 tags per image
✅ ALWAYS test on staging before production
```

### All Frontend Applications Must Include

Every frontend MUST have these authentication files:
```
src/
├── lib/
│   ├── types/auth.ts           # TypeScript types for auth
│   └── auth-client.ts          # API client for Brain Gateway
├── contexts/
│   └── AuthContext.tsx         # React Context + useAuth hook
├── middleware.ts               # Route protection
└── app/
    ├── layout.tsx              # Wrapped with <AuthProvider>
    └── (auth)/
        ├── login/page.tsx
        ├── signup/page.tsx
        └── forgot-password/page.tsx
```

See [BIZOSAAS_UNIFIED_FRONTEND_ARCHITECTURE.md](/home/alagiri/projects/BIZOSAAS_UNIFIED_FRONTEND_ARCHITECTURE.md) for complete implementation patterns.

### With Shared Infrastructure (Recommended)
1. **Shared Infrastructure**: Ensure shared infrastructure is running first
   ```bash
   cd /home/alagiri/projects/shared-development
   docker-compose up -d
   ```
2. **Environment Setup**: Copy `.env.example` to `.env` and configure required API keys
3. **Project Startup**: Use `npm run start:shared` for automated startup with checks
4. **Service Dependencies**: Project services connect to shared PostgreSQL and Redis
5. **WordPress Integration**: Custom plugins and themes in `n8n/wordpress/`
6. **Workflow Development**: Use shared n8n instance at `localhost:5678`

### Legacy Workflow (Self-Contained)
1. **Environment Setup**: Copy `.env.example` to `.env` and configure required API keys
2. **Database First**: Services depend on local PostgreSQL, ensure it starts first
3. **Service Dependencies**: CrewAI and n8n require both PostgreSQL and Redis
4. **Full Stack**: Use `npm run dev:legacy` to start all services locally

## Deployment

The platform supports multiple deployment strategies:

- **Docker Compose**: For local development and simple deployments
- **Dokploy**: Automated deployment with Git integration (preferred)
- **Kubernetes**: Complete K8s manifests available (`k8s-complete.yaml`)

For production deployment, use the Dokploy strategy with proper environment variables and SSL configuration.

## Security Considerations

- Multi-tenant row-level security (RLS) enabled on all tenant tables
- JWT-based authentication with session management
- API key encryption in `tenant_integrations` table
- Rate limiting and security event logging
- CORS configured for local development (adjust for production)

## AI Agent Endpoints

The CrewAI system exposes these key endpoints:

- `POST /agents/digital-presence-audit` - Analyze company digital presence
- `POST /agents/campaign-strategy` - Generate AI marketing strategies  
- `POST /agents/optimize-campaign` - Optimize existing campaigns
- `GET /agents/analysis/{analysis_id}` - Get analysis status/results
- `GET /health` - System health check

## Common Development Tasks

### With Shared Infrastructure
- **Adding New Agents**: Create in `n8n/crewai/agents/` directory
- **Database Changes**: Create migrations for shared PostgreSQL instance  
- **New Workflows**: Design in shared n8n UI at `localhost:5678`
- **WordPress Customization**: Modify themes/plugins in `n8n/wordpress/`
- **API Integration**: Configure in `tenant_integrations` table per tenant
- **Debugging**: Use `npm run logs:crewai` or `npm run logs:wordpress` for service-specific logs
- **Service Management**: Use `npm run status` to check running services

### Migration from Legacy
- **Backup Data**: Ensure important data is backed up before migration
- **Update Environment**: Use new `.env.example` as template
- **Test Configuration**: Use `npm run check:shared` to verify shared infrastructure
- **Gradual Migration**: Can use both modes during transition period