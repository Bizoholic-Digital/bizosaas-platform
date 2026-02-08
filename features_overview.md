# BizOSaaS Platform — Features Overview (2026)

_This overview outlines the current major features based on the most recent lean hexagonal architecture:_

---

## 1. bizosaas-platforms/brain-gateway

**Central orchestrator—manages all SaaS/AI logic and integrations.**

### Features
- Hexagonal architecture: Ports/adapters pattern for extensibility
- Multi-tenancy and RBAC: Data and workflow isolation
- Workflow Orchestration: Pluggable MCP/Temporal integration
- Service adapters: Redis/NeonDB/Plane.so integration via config
- Authentication: JWT, session, audit, RLS enforcement
- Real-time dashboard feeds via WebSocket
- Automated circuit breaker and health monitoring

---

## 2. bizosaas-platforms/ai-agents

**Plug-in AI agent service layer, tightly integrated with brain-gateway.**

### Features
- Agents register and self-discover via gateway
- Autonomous and collaborative workflows
- Human-in-the-loop support (HITL)
- RAG/LLM/GPT agents, scoring bots, composable routines
- Event-triggered & scheduled workflows (MCP-ready)
- Hot plugging: Add/remove agents with zero impact

---

## 3. bizosaas-platforms/portals/client-portal

**Modern, multi-tenant dashboard for end-users.**

### Features
- Real-time analytics, campaign dashboards, reporting
- Built-in AI assistant/chat
- API-driven workflow panels
- Mobile/tablet/desktop responsive with dark/light themes
- Enhanced authentication with session/RLS
- Extensible modules: Add data panels easily

---

## 4. bizosaas-platforms/portals/admin-portal

**Powerful admin/operator dashboard.**

### Features
- Tenant/user/role management with bulk actions
- Agent/service health controls with workflow/panel orchestration
- Audit logging, secure vault integration, notification/incident monitoring
- Configuration panel for adapters and onboarding
- Live monitoring, onboarding, and privileged access assignment

---

## 5. MCP / Workflow Integrations

- **Dynamic workflows (MCP+Temporal+)**: Setup, schedule, and audit all business routines from both client and admin portals via gateway adapters.
- **Config-driven cloud resources**: Easily connect new external services (Redis, NeonDB, Plane.so) via configuration.
- **Real-time workflow logs/feeds**: Visible and RBAC-scoped in all portals.

---

## Summary Table

| Module        | Key Features                            |
|---------------|-----------------------------------------|
| brain-gateway | Hexagonal core, workflows, adapters, RBAC, real-time|
| ai-agents     | AI agent register/composition, HITL, scheduled/event|
| client-portal | Multi-tenant dashboard, panels, AI chat, extensible |
| admin-portal  | Admin RBAC, config, audit logs, agent controls      |
| MCP/Workflow  | Dynamic orchestration, real-time feeds, config ops  |

---

## Guidance For New Features

- Integrate new services by adding adapters in brain-gateway.
- Deploy only core gateway (external infra is config-driven).
- Extend portals via new API routes and panels—no legacy coupling.

---

**For further detail, see each folder's README and full source. This file should be merged near the top of README.md for quick access to new features.**