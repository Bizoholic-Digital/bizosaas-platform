# BizOSaaS Platform Overview

## High-Level Architecture
BizOSaaS is a multi-tenant platform built with a microservices approach:
- **Frontend**: Next.js (Admin Dashboard, Client Portal, Business Directory).
- **Brain Core**: FastAPI-based services for intelligence (RAG/KAG), billing (Lago), and auth (Authentik).
- **Task Orchestration**: Temporal.io managing complex AI workflows.
- **Data Persistence**: PostgreSQL (PostGIS/pgvector), Redis (Caching/Queue).

## Identity & Access Management
- **Authentik SSO**: Centralized identity provider for all dashboards.
- **NextAuth.js**: Integration layer for Next.js frontends.
- **Vault**: Secure storage for all platform secrets and API keys.

## Service Catalog
1. **Brain Gateway**: The central API hub and entry point.
2. **AI Agents**: CrewAI-powered autonomous agents for specialized business tasks.
3. **Documentation Site**: Docusaurus-based automated platform documentation.
4. **Client Portal**: Customer-facing dashboard for campaign management.
5. **Admin Dashboard**: Governance and platform management tool.

## Intelligence Bridge (Phase 11)
- **RAG/KAG Bridge**: Seamless context enrichment from vector databases into Agent execution.
- **Persona Layer**: Deep integration of brand voice and tone into all AI outputs.
- **Prompt Registry**: Centralized management of LLM prompts with fallback and versioning.

## Pricing & Monetization
- **Solo**: Focused on single-site automation.
- **Pro**: Advanced features for scaling businesses.
- **Agency**: Multi-tenant management for marketing agencies.

---
*Reference: [docs/architecture/](file:///home/alagiri/projects/bizosaas-platform/docs/architecture/)*
*Last Updated: 2026-02-18*

