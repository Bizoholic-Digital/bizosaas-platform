# BizOSaaS OpenSpec Documentation

**Platform**: BizOSaaS - AI-Powered Multi-Tenant SaaS Ecosystem
**Total Services**: 23 (Infrastructure: 6, Backend: 10, Frontend: 7)
**Architecture**: Microservices with Domain-Driven Design (DDD)
**Generated**: October 15, 2025

## 📋 Overview

This OpenSpec documentation provides comprehensive specifications for all services in the BizOSaaS platform. Each specification follows industry best practices with Domain-Driven Design principles for backend services.

## 🎯 Purpose

OpenSpec serves as the **single source of truth** for:
- Service architecture and design decisions
- Domain models and business logic
- API contracts and integration points
- Multi-tenancy implementation patterns
- Testing strategies and deployment requirements

## 📁 Directory Structure

```
openspec/
├── specs/
│   ├── infrastructure/        # 6 infrastructure services (100% complete)
│   │   ├── 01-postgresql.md
│   │   ├── 02-redis.md
│   │   ├── 03-vault.md
│   │   ├── 04-temporal-server.md
│   │   ├── 05-temporal-ui.md
│   │   └── 06-superset.md
│   ├── backend/              # 10 backend services (10% complete)
│   │   ├── 01-brain-gateway.md
│   │   ├── 02-ai-agents.md (pending)
│   │   ├── 03-quanttrade-backend.md (pending)
│   │   ├── 04-auth-service.md (pending)
│   │   ├── 05-wagtail-cms.md (pending)
│   │   ├── 06-saleor.md (pending)
│   │   ├── 07-django-crm.md (pending)
│   │   ├── 08-coreldove-backend.md (pending)
│   │   ├── 09-amazon-sourcing.md (pending)
│   │   └── 10-business-directory-backend.md (pending)
│   └── frontend/             # 7 frontend services (0% complete)
│       ├── 01-bizoholic-frontend.md (pending)
│       ├── 02-coreldove-frontend.md (pending)
│       ├── 03-thrillring-gaming.md (pending)
│       ├── 04-quanttrade-frontend.md (pending)
│       ├── 05-client-portal.md (pending)
│       ├── 06-admin-dashboard.md (pending)
│       └── 07-business-directory-frontend.md (pending)
├── templates/
│   ├── backend-service-ddd-template.md
│   ├── infrastructure-service-template.md (pending)
│   ├── frontend-service-template.md (pending)
│   └── api-endpoint-template.md (pending)
├── changes/                  # Active proposals
└── IMPLEMENTATION_STATUS.md  # Progress tracking

```

## ✅ Completed Specifications

### Infrastructure (6/6 - 100%)
All infrastructure services have comprehensive specifications:

1. **PostgreSQL** - Multi-tenant database with pgvector
2. **Redis** - Caching, sessions, message queuing, event streaming
3. **Vault** - Secrets management for 40+ API integrations
4. **Temporal Server** - Workflow orchestration engine
5. **Temporal UI** - Workflow monitoring (Infrastructure classification)
6. **Superset** - Business intelligence and analytics

### Backend (1/10 - 10%)
1. **Brain API Gateway** ✅ - Complete DDD implementation
   - Central routing hub for 13 services
   - 93 AI agents integration
   - Circuit breaker & rate limiting
   - Multi-tenant routing

### Templates (1/4 - 25%)
1. **Backend DDD Template** ✅ - Complete DDD structure
   - Bounded contexts
   - Aggregates, entities, value objects
   - Domain events
   - Repository pattern
   - CQRS implementation

## 🏗️ Architecture Principles

### Domain-Driven Design (DDD)
All backend services follow DDD principles:

**Domain Layer**:
- Entities (business objects with identity)
- Value Objects (immutable objects)
- Aggregates (consistency boundaries)
- Domain Events (state changes)
- Domain Services (business logic)

**Application Layer**:
- Use Cases / Commands
- Query Handlers (CQRS)
- Application Services
- DTOs

**Infrastructure Layer**:
- Repository Implementations
- External Service Adapters
- Database Migrations
- Message Queue Adapters

**API Layer**:
- REST Endpoints (FastAPI)
- Request/Response Models
- OpenAPI Documentation

### Multi-Tenancy Pattern
```sql
-- Every table includes tenant_id
ALTER TABLE campaigns ADD COLUMN tenant_id UUID NOT NULL;

-- Row-Level Security enforces isolation
CREATE POLICY tenant_isolation_policy ON campaigns
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);
```

### Event-Driven Architecture
```python
# Domain events published to Redis Streams
@dataclass
class CampaignCreatedEvent:
    campaign_id: UUID
    tenant_id: UUID
    timestamp: datetime

# Event consumers process asynchronously
async def handle_campaign_created(event: CampaignCreatedEvent):
    # Trigger follow-up actions
    await send_notification(event.campaign_id)
    await update_analytics(event.campaign_id)
```

## 🔄 Development Workflow

### 1. Create Feature Specification
```bash
openspec draft "Add user notifications to Client Portal"
```

This creates: `openspec/changes/client-portal-notifications.md`

### 2. AI-Assisted Development
AI assistants reference the spec while generating code:
```python
# AI reads: openspec/changes/client-portal-notifications.md
# Generates code following the specification
```

### 3. Implementation & Testing
Implement the feature locally, following the spec exactly.

### 4. Archive Specification
```bash
openspec archive client-portal-notifications
```

Moves spec to: `openspec/specs/frontend/client-portal.md#notifications`

### 5. Commit Both Spec and Code
```bash
git add openspec/specs/frontend/client-portal.md
git add bizosaas/frontend/apps/client-portal/
git commit -m "feat(client-portal): Add user notifications

Implemented push notifications for campaign updates.
Spec: openspec/specs/frontend/client-portal.md#notifications"
git push origin staging
```

## 🎨 Specification Format

Each service spec includes:

### Service Identity
- Name, type, container, ports, status

### Purpose
- What the service does and why it exists

### Domain Model (Backend Only)
- Bounded context definition
- Aggregates and entities
- Value objects
- Domain events
- Domain services

### API Endpoints
- Routes, methods, parameters
- Request/response schemas
- Authentication requirements

### Configuration
- Environment variables
- Docker compose setup
- Dependencies

### Integration Points
- Services it depends on
- Services that depend on it
- Event publishing/consuming

### Testing Strategy
- Unit tests (domain)
- Integration tests (application)
- API tests (end-to-end)

### Deployment Checklist
- Prerequisites
- Configuration steps
- Validation procedures

## 🚀 Quick Start

### For New Developers
1. Read this README
2. Review completed specs in `openspec/specs/infrastructure/`
3. Study the Backend DDD Template: `openspec/templates/backend-service-ddd-template.md`
4. Reference PRD: `/home/alagiri/projects/bizoholic/comprehensive_prd_06092025.md`

### For AI Assistants
1. Always check OpenSpec before generating code
2. Follow architectural patterns from templates
3. Maintain consistency with existing services
4. Update specs when code changes

### For Architects
1. Use specs to validate implementation
2. Ensure DDD principles are followed
3. Review domain events and boundaries
4. Validate multi-tenant isolation

## 📊 Current Progress

| Category | Complete | Pending | Progress |
|----------|----------|---------|----------|
| Infrastructure | 6 | 0 | 100% ✅ |
| Backend | 1 | 9 | 10% 🟡 |
| Frontend | 0 | 7 | 0% 🔴 |
| Templates | 1 | 3 | 25% 🟡 |
| **Total** | **8** | **19** | **30%** |

## 🎯 Next Steps

### Immediate (Next 4 hours)
1. Complete Backend service specs (9 remaining)
2. Create Frontend service specs (7 services)
3. Complete service templates (3 remaining)

### Short-term (Next 2 days)
4. Validation specs for completed services
5. Service interdependency mapping
6. Integration diagrams and event flows

## 📚 Key References

### Internal Documentation
- **PRD**: `/home/alagiri/projects/bizoholic/comprehensive_prd_06092025.md`
- **Implementation Plan**: `/home/alagiri/projects/bizoholic/bizosaas/comprehensive_implementation_task_plan_06092025_updated.md`
- **Platform Status**: `/tmp/PLATFORM_STATUS_REPORT.md`
- **Architecture Analysis**: `/tmp/TEMPORAL_ARCHITECTURE_RECOMMENDATION.md`

### External Resources
- [OpenSpec Documentation](https://openspec.dev)
- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)
- [Domain-Driven Design (Eric Evans)](https://www.domainlanguage.com/ddd/)
- [Implementing Domain-Driven Design (Vaughn Vernon)](https://vaughnvernon.com/iddd/)

## 🔧 Key Decisions

### Architecture Decisions
✅ **Temporal UI in Infrastructure** (NOT Frontend)
✅ **OpenSpec on Local WSL2** (NOT VPS)
✅ **Specs version-controlled with code** (in Git)
✅ **DDD for all backend services**
✅ **Multi-tenancy with RLS** (Row-Level Security)
✅ **Event-driven architecture** (Redis Streams)

### Service Count: 23 Total
- Infrastructure: 6 services
- Backend: 10 services
- Frontend: 7 services

### AI Agents: 93 Total
- 4-Agent Pattern: 6 complex integrations
- 3-Agent Pattern: 8 medium integrations
- 2-Agent Pattern: 12 standard integrations
- Single Agent: 14 simple integrations

## 💡 Benefits of OpenSpec

### For Development Teams
- **Single Source of Truth**: All service specs in one place
- **Clear Requirements**: Reduce misunderstandings and rework
- **Consistent Architecture**: Templates ensure uniformity
- **Better Onboarding**: New developers understand system faster

### For AI Assistants
- **Context Awareness**: Understand service boundaries and contracts
- **Code Quality**: Generate code matching architectural patterns
- **Fewer Bugs**: Follow specifications exactly
- **Maintainability**: Consistent patterns across codebase

### For Business
- **Time Savings**: 3-6 hours/week productivity gain
- **Fewer Bugs**: 30-40% reduction in requirement-related bugs
- **Better Documentation**: Self-documenting architecture
- **Faster Onboarding**: New team members productive faster

## 🤝 Contributing

### Adding New Specifications
1. Use appropriate template from `openspec/templates/`
2. Follow existing naming conventions
3. Include all required sections
4. Add to `IMPLEMENTATION_STATUS.md`

### Updating Existing Specs
1. Create change proposal in `openspec/changes/`
2. Review with team
3. Update spec after implementation
4. Update changelog

### Creating Templates
1. Study existing successful services
2. Extract common patterns
3. Document best practices
4. Validate with team

## 📞 Support

### Questions or Issues?
- Review existing specs for examples
- Check templates for patterns
- Reference PRD for business context
- Consult DDD resources for architecture

---

**Generated**: October 15, 2025
**Version**: 1.0
**Status**: 30% Complete (8/27 specifications)
**Next Milestone**: Complete Backend services (target: 100%)
