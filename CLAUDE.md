# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bizoholic is a comprehensive AI Marketing Agency SaaS platform built with a microservices architecture. The platform combines WordPress frontend, n8n workflow automation, CrewAI agents, and shared infrastructure to provide end-to-end marketing automation services.

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

### 2. WordPress Frontend (Port 3000)
- **Image**: `wordpress:6.4-php8.1-apache`
- **Purpose**: Bizoholic-specific client dashboards, lead forms, reporting interfaces
- **Custom Content**: Located in `n8n/wordpress/` directory
- **Database**: Uses shared PostgreSQL with dedicated WordPress database
- **Connection**: Uses `host.docker.internal` to connect to shared infrastructure

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