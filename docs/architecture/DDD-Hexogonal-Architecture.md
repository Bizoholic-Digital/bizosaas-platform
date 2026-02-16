# Bizosaas brain-first PRD with DDD and hexagonal architecture

This PRD defines the brain-first SaaS platform built on DDD and hexagonal architecture, orchestrating 93+ specialized AI agents with continuous data collection and self-optimization via RAG (retrieval-augmented generation) and KAG (knowledge-augmented governance). It focuses on an integration-first approach with optional starter modules, clean bounded contexts, and robust security, observability, and auditability.

---

## Product overview and goals

- **Core value:** Intelligent orchestrator (the “Brain”) unifying client stacks (WordPress, CRM, ecommerce, analytics) through agents, workflows, and a canonical data model.
- **Primary users:** Agency owners, client stakeholders, operators, admins, and super admins.
- **Objectives:**
  - **Interoperability:** Bring-your-own CMS/CRM/ecommerce/analytics through adapters.
  - **Explainable automation:** Agentic workflows with audit trails and HIL (human-in-the-loop) checkpoints.
  - **Continuous learning:** Unified RAG/KAG pipeline that collects, cleans, and leverages first- and third-party data.
  - **Security-first:** Tenant isolation, RBAC/ABAC, Vault-managed secrets, policy-as-code.
- **Non-goals:**
  - **Feature parity** with best-in-class CMS/CRM out of the gate.
  - **Overly heavy stacks** that impede agility in early phases.

---

## Architecture overview

- **Style:** DDD with hexagonal (ports and adapters) and event-driven orchestration.
- **Key decisions:**
  - **Modular monolith for Brain Core** with clear bounded contexts; stateless microservices for Gateway and Integrations.
  - **Hexagonal ports:** Stable domain ports for content, CRM, commerce, analytics, workflows; adapters per external tool.
  - **Temporal-backed workflows:** Durable, retry-safe orchestration; HIL steps for approvals and escalations.
  - **Event bus:** Lightweight (e.g., NATS/Redis Streams) for domain events, audit trail, and agent telemetry.
  - **Data pipeline:** Unified RAG index, KAG policy store, feature store for agents; object storage for artifacts.

---

## Bounded contexts and core services

- **Identity & access (Auth/RBAC/ABAC):**
  - **Responsibilities:** SSO/OIDC, MFA, roles, attributes, per-tenant policies (OPA).
  - **Ports:** Authentication, authorization, session, token issuance, policy evaluation.
- **Tenant & provisioning:**
  - **Responsibilities:** Tenant lifecycle, plan entitlements, usage metering, isolation boundaries.
  - **Ports:** Tenant registry, quota enforcement, lifecycle events.
- **Content (CMS canonical):**
  - **Responsibilities:** Canonical content entities, taxonomy, publishing states, SEO metadata.
  - **Ports:** Content CRUD, workflow hooks, indexing feed to RAG.
- **CRM canonical:**
  - **Responsibilities:** Contacts, accounts, deals, activities, pipeline stages, attribution.
  - **Ports:** CRM CRUD, enrichment, deduplication, analytics emitters.
- **Commerce canonical:**
  - **Responsibilities:** Catalog, pricing, orders, payments, fulfillment, returns.
  - **Ports:** Order ingest, inventory sync, checkout signals.
- **Analytics & telemetry:**
  - **Responsibilities:** Event ingestion, session analytics, conversion metrics, aggregation.
  - **Ports:** Event write, query/read models, dashboards feed, agent feedback loop.
- **Workflow & orchestration (Temporal):**
  - **Responsibilities:** Cross-tool orchestration, retries, compensations, HIL approvals, SLA tracking.
  - **Ports:** Workflow start/signal/query, Task routing to agents.
- **Agents platform:**
  - **Responsibilities:** Agent registry, assignment, policies, embeddings/RAG access, KAG guardrails, explainability.
  - **Ports:** Agent invoke, context fetch, feedback submit, decision logging.
- **Connectors & integrations:**
  - **Responsibilities:** Adapters for WordPress/Drupal/Joomla, HubSpot/Salesforce, Shopify/WooCommerce, GA4/Mixpanel/Matomo.
  - **Ports:** Connector install, secrets handshake (Vault), sync config, health checks.
- **Audit & compliance:**
  - **Responsibilities:** Immutable audit logs, compliance exports, DLP checks, policy violations.
  - **Ports:** Log append, evidence export, anomaly alerts.
- **Billing & plans:**
  - **Responsibilities:** Subscriptions, invoices, payments, entitlements, plan caps.
  - **Ports:** Metering, invoicing, entitlements check.

---

## AI agents system (93+ agents) and continuous learning

### Agent categories and responsibilities

| Category | Purpose | Key inputs | Outputs | Notes |
|---|---|---|---|---|
| Content ops | Drafting, editing, SEO, localization | CMS entries, taxonomy, SERP data | Drafts, SEO metadata, publish tasks | HIL review gates |
| CRM growth | Lead scoring, segmentation, outreach | Contacts, events, attribution | Scored leads, sequences, tasks | KAG policy for consent |
| Commerce | Pricing, bundling, merchandising | Catalog, orders, behavior | Price recs, bundles, promos | Guardrails on margins |
| Analytics | Attribution, funnel, anomaly | Events, sessions, conversions | Reports, alert signals | p95 latency SLOs |
| Integrations | Sync, schema mapping, health | External APIs, schemas | Sync jobs, status | Per-adapter resilience |
| Automation | Cross-tool workflows | Temporal signals, policies | Executed playbooks | Explainability required |
| Governance | Policy checks, DLP, compliance | Policies, data samples | Violations, remediations | Evidence to audit log |
| Support | Ticket triage, FAQ, summaries | Activity logs, docs | Responses, escalations | RAG over knowledge base |
| Operations | Scaling hints, cache tuning | Metrics, traces | Infra recommendations | SLO-based actions |
| Marketing | Campaigns, A/B tests, content | CRM segments, CMS | Campaigns, insights | Consent-aware actions |

- **Agent registry:** YAML/JSON definitions include purpose, inputs, outputs, required ports, policies, entitlements, and HIL steps.
- **Agent orchestration:** Temporal workflows route tasks to agents; agents return decisions with confidence scores and explanations.
- **RAG pipeline:** 
  - **Index sources:** CMS content, CRM notes, tickets, docs, web pages (permissioned), analytics summaries.
  - **Embedding stores:** Per-tenant vector indexes; shard-aware with TTL and reindex policies.
  - **Retrieval:** Context packs tailored to task, freshness scoring, citation trails.
- **KAG (knowledge-augmented governance):**
  - **Policy store:** Consent rules, PII handling, brand guidelines, security controls.
  - **Runtime checks:** Pre- and post-action validations; block/modify actions; attach remediation notes.
- **Self-optimization loop:**
  - **Feedback signals:** Success metrics, user ratings, overrides, exception counts.
  - **Policy updates:** Auto-suggest guardrail adjustments; human approval required.
  - **Model hints:** Feature store updates; retraining/trimming via scheduled jobs with drift detection.

---

## Canonical data model and events

- **Canonical entities:** Content, MediaAsset, Contact, Account, Deal, Product, Order, Event, Segment, Workflow, AgentDecision, AuditRecord.
- **Events (examples):**
  - **ContentPublished, ContentIndexed**
  - **LeadCaptured, LeadScored, OutreachSent**
  - **OrderCreated, PaymentCaptured, FulfillmentStarted**
  - **EventIngested, ConversionRecorded**
  - **WorkflowStarted, HILApprovalRequired, WorkflowCompleted**
  - **PolicyViolationDetected, AuditEvidenceAppended**
- **CQRS strategy:**
  - **Write models:** Strict validation, workflows trigger.
  - **Read models:** Aggregations for dashboards; materialized views optimized for GraphQL queries.

---

## Client portal information architecture

### Top-level menus and sub-features

- **Dashboard**
  - **Overview:** KPIs, projects, recent decisions
  - **Widgets:** Content, CRM, commerce, analytics cards
  - **Customization:** Per-tenant layouts, saved views
- **CRM**
  - **Contacts & accounts:** CRUD, deduplication, enrichment
  - **Deals & pipeline:** Stages, forecasts, win-loss insights
  - **Activities:** Emails, calls, tasks, sequences
  - **Segments:** Dynamic cohorts, consent flags
- **CMS**
  - **Content library:** Drafts, published, versions
  - **Workflows:** Draft→review→publish with HIL steps
  - **SEO tools:** Titles, meta, schema, link recommendations
  - **Media:** Uploads, tagging, usage analytics
- **AI agents**
  - **Directory:** Browse 93+ agents, capabilities, entitlements
  - **Playbooks:** Prebuilt workflows (e.g., blog→social→CRM)
  - **Explainability:** Decision logs, rationales, citations
  - **Policies:** Guardrails per agent; override with approval
- **Connectors**
  - **Marketplace:** WordPress, Drupal, Joomla, HubSpot, Salesforce, Shopify, Woo, GA4, Mixpanel, Matomo
  - **Setup:** OAuth/API keys via Vault, scopes, test connections
  - **Health:** Status, rate limits, error reporting, retries
- **Integrations**
  - **Sync profiles:** Field mapping, directionality, schedules
  - **Webhooks:** Triggers, signatures, replay
  - **Data quality:** Schema drift alerts, transform rules
- **Projects & tasks**
  - **Boards:** Kanban, Gantt
  - **Assignments:** Agents and humans
  - **SLA tracking:** Due times, escalations
- **Billing**
  - **Subscriptions:** Plans, entitlements, upgrades
  - **Invoices:** History, payment methods
  - **Usage:** Agent minutes, workflow runs, storage
- **Settings**
  - **Profile & preferences:** Timezone, notifications
  - **Security:** MFA, API tokens, session policies
  - **Tenant config:** Branding, domains, feature flags
- **Admin**
  - **Users & roles:** RBAC/ABAC, invitations, groups
  - **Policy management:** OPA policies, KAG rules
  - **Audit & compliance:** Logs, exports, DLP reports
  - **Observability:** Metrics, alerts, error budgets
- **Super admin**
  - **Tenants:** Create/suspend/delete, migrations
  - **Global configs:** Connectors defaults, rate limits
  - **Platform analytics:** Adoption, performance
  - **Security center:** Vault, keys, rotations, attestations

---

## APIs and gateway design

- **Gateway:**
  - **Responsibilities:** AuthN/Z, rate limiting, tenancy scoping, request shaping, audit stamping.
  - **Interfaces:** REST for core ops, GraphQL for flexible, cross-domain reads.
- **REST (FastAPI):**
  - **Use cases:** Auth/SSO, RBAC/ABAC, Vault ops, Temporal workflows (start/signal/query), audit appends, connector lifecycle.
- **GraphQL (Strawberry on FastAPI):**
  - **Use cases:** Aggregated queries for dashboards, content+CRM joins, analytics reads, agent decision logs.
  - **Guardrails:** Query depth/complexity limits, caching for common resolvers, N+1 prevention via dataloaders, field-level authorization.
- **Webhooks & events:**
  - **Inbound:** CMS publish, orders, CRM updates.
  - **Outbound:** Workflow completion, policy violations, sync status.

---

## Security, compliance, and governance

- **Identity & SSO:** OIDC/SAML, MFA, short-lived tokens; per-tenant IDP options.
- **RBAC/ABAC:** Roles plus attributes; policy-as-code (OPA/Styra); deny-by-default APIs.
- **Secrets management:** Vault for connectors and platform secrets; scoped leases, rotation schedules, access logs.
- **Network security:** TLS everywhere, mTLS between services; WAF at gateway; IP allowlists for admin portals.
- **Data protection:** PII tagging, DLP checks via governance agents; per-tenant encryption keys (BYOK option in roadmap).
- **Audit:** Immutable logs with tamper-evident hashing; export packs for compliance (e.g., evidence bundles).

---

## Observability, performance, and SLOs

- **Metrics/traces/logs:** OpenTelemetry; Prometheus metrics; Loki logs; Grafana dashboards.
- **Key SLOs:**
  - **Gateway p95 latency:** ≤ 250 ms for read, ≤ 400 ms for write.
  - **Workflow completion reliability:** ≥ 99% within SLA windows.
  - **Agent decision turnaround:** p95 ≤ 2 s with cached context; ≤ 5 s with fresh RAG.
  - **Connector health uptime:** ≥ 99% excluding third-party outages.
- **Error budgets:** Track policy violations, failed workflows, connector retries; trigger rollbacks or feature flags.

---

## Release plan, acceptance criteria, and KPIs

### Phases

- **Phase 1 (0–8 weeks): Brain-first MVP**
  - **Deliverables:** Gateway, REST core, GraphQL reads, Auth/RBAC, Vault, Temporal, WordPress adapter, GA4 adapter, Agent registry v1, RAG index v1.
  - **Acceptance criteria:**
    - **Auth:** SSO with MFA; role-based access works per tenant.
    - **Adapters:** WordPress content sync and publish workflow with HIL.
    - **RAG:** Retrieval from CMS + docs; citations in explainability view.
    - **Audit:** Every agent action stamped with actor, context, decision, policy checks.
- **Phase 2 (8–16 weeks): Integrations expansion**
  - **Deliverables:** HubSpot/Shopify adapters, analytics dashboards, CRM canonical, segments, campaign playbooks, governance agents v1, KAG store v1.
  - **Acceptance criteria:**
    - **CRM:** Lead capture, scoring, outreach with consent checks.
    - **Commerce:** Order ingest and attribution to campaigns.
    - **Governance:** Block actions violating policies; remediation paths logged.
- **Phase 3 (16–24 weeks): Scale and optimization**
  - **Deliverables:** Additional adapters (Drupal/Joomla/Salesforce/Mixpanel), feature store, auto-optimizing agent policies, advanced observability.
  - **Acceptance criteria:**
    - **Performance:** Meet SLOs; error budgets respected.
    - **Self-optimization:** Agents adjust thresholds with HIL approvals; measurable uplift.

### KPIs

- **Time-to-value:** Median time from connector install to first successful workflow completion.
- **Adoption:** Number of active tenants, adapters per tenant, agent invocations per day.
- **Quality:** Workflow success rate, policy violation rate, human override rate.
- **Business:** Conversion lift from AI-driven campaigns, churn rate, NPS.

---

## Notes on the 93+ agents catalog

- **Implementation guidance:**
  - **Registry-first:** Maintain agents in a central registry with metadata (category, ports, inputs/outputs, policies, HIL steps).
  - **Composable workflows:** Agents should be composable; avoid monolithic “do-everything” agents.
  - **Explainability mandatory:** Each agent returns a decision, confidence, retrieved context sources, and policy checks.
- **Representative distribution (example):**
  - **Content ops (15–20)**
  - **CRM growth (12–15)**
  - **Commerce (8–12)**
  - **Analytics (10–12)**
  - **Integrations (10–12)**
  - **Automation (8–10)**
  - **Governance (6–8)**
  - **Support (6–8)**
  - **Operations (4–6)**
  - **Marketing (6–8)**
- **Governance overlay:** KAG policies applied to all agent categories; HIL required for sensitive actions (publishing, outreach, pricing changes).

---

## Final recommendations

- **Stay brain-first with DDD + hexagonal:** Keep the Brain Core modular, expose ports, and implement adapters for top tools.
- **Hybrid API strategy:** REST for critical core; GraphQL for flexible reads and cross-domain queries.
- **RAG/KAG as first-class citizens:** Treat retrieval and governance as core infrastructure, not add-ons.
- **Explainability and audit by default:** Every automated action must be traceable, justifiable, and reversible.
- **Phased rollouts:** Prioritize WordPress + GA4 + CRM basics, then scale integrations and agent breadth.

If you want, I can provide a lightweight schema map (entities and relationships) and a sample agent registry template you can drop into your repo to standardize definitions across the 93+ agents.


## How to verify 

Got it — you want to make sure your **client portal + brain platform** is not only feature-rich but also architecturally sound, specifically aligned with **DDD (Domain-Driven Design)** and **Hexagonal Architecture (Ports & Adapters)**. Let’s tackle this in two parts:

---

## 🛠️ Additional Features to Make the Client Portal More Robust
Beyond CMS, CRM, analytics, AI agents, and the playground, here are enhancements that strengthen usability, governance, and adaptability:

- **Personal AI Assistant Layer**
  - Conversational interface to orchestrate the 93+ agents.
  - Context-aware queries (e.g., “show me leads from last campaign”).
  - Explainability dashboard (why an agent made a decision).

- **Playground / Fine-tuning**
  - Sandbox for clients to test workflows with their own API keys.
  - Adjustable parameters (confidence thresholds, retry policies).
  - Performance metrics (latency, accuracy, override frequency).

- **Data Feedback Loop**
  - Continuous collection of signals (agent success/failure, overrides, client ratings).
  - Aggregated insights across tenants (with strict isolation).
  - Auto-suggest optimizations (e.g., “increase retry for GA4 connector”).

- **Governance & Compliance**
  - Policy management (consent, PII handling, brand rules).
  - Audit trail exports (tamper-evident logs).
  - DLP checks before publishing or outreach.

- **Multi-tenancy Enhancements**
  - Tenant branding (custom logos, domains).
  - Feature flags per tenant.
  - Usage metering (agent minutes, workflows, storage).

- **Observability**
  - Per-tenant dashboards (errors, latency, agent usage).
  - SLA tracking (workflow completion, connector uptime).
  - Alerts for anomalies.

---

## ✅ How to Check if Your Platform Follows Hexagonal Architecture + DDD

Here’s a **checklist** you can use to confirm alignment:

### 1. **Core Domain Independence**
- **Question:** Can your business logic (Brain Core, agent orchestration, workflows) run without any external system (CMS, CRM, DB)?  
- **Check:** Replace WordPress with Drupal adapter → Brain Core should remain unchanged.  
- ✅ If yes → you’re following hexagonal principles.

### 2. **Ports & Adapters Separation**
- **Question:** Are external systems accessed only through defined interfaces (ports)?  
- **Check:** Inspect code — Brain Core should depend on interfaces, not concrete implementations.  
- ✅ Adapters (WordPress, HubSpot, GA4) should implement ports, not leak into domain logic.

### 3. **Bounded Contexts (DDD)**
- **Question:** Are domains clearly separated (CMS, CRM, Commerce, Analytics, Identity)?  
- **Check:** Each bounded context has its own models, services, and events.  
- ✅ No “God objects” or cross-context coupling.

### 4. **Event-Driven Communication**
- **Question:** Do contexts communicate via domain events, not direct calls?  
- **Check:** Example: “ContentPublished” event triggers CRM workflow via Temporal, not a direct CMS→CRM call.  
- ✅ If events drive workflows, you’re aligned with DDD.

### 5. **Canonical Data Model**
- **Question:** Is there a unified schema (Content, Contact, Order, Event) inside the Brain Core?  
- **Check:** External data is mapped into canonical entities before use.  
- ✅ Prevents schema sprawl and keeps core stable.

### 6. **Testability**
- **Question:** Can you unit-test the Brain Core without external systems?  
- **Check:** Mock ports/adapters → domain logic should still run.  
- ✅ If yes, you’re hexagonal.

### 7. **Explainability & Audit**
- **Question:** Does every agent decision log inputs, outputs, and policies?  
- **Check:** Audit trail shows “Agent X → Decision Y → Context Z → Policy Check”.  
- ✅ This ensures governance and aligns with DDD’s emphasis on ubiquitous language.

---

## 🚀 Recommended Confirmation Process
1. **Architecture Review Workshops**  
   - Walk through each bounded context.  
   - Verify ports/adapters separation.  
   - Check event flows.

2. **Code Audits**  
   - Ensure domain logic doesn’t import external SDKs directly.  
   - Confirm adapters implement interfaces.

3. **Integration Tests**  
   - Swap one adapter (e.g., WordPress → Drupal).  
   - Brain Core should remain unchanged.

4. **Domain Event Traceability**  
   - Validate that workflows are triggered by events, not hard-coded calls.

---

👉 In short:  
- **Hexagonal check:** Core depends only on ports, adapters are swappable.  
- **DDD check:** Clear bounded contexts, domain events, canonical models, ubiquitous language.  
- If you can swap external tools without touching the Brain Core, and your domain logic is testable in isolation, you’re on the right path.

---

Would you like me to **draft a practical audit checklist** (step-by-step items your dev team can tick off) so you can formally validate that Bizosaas is hexagonal + DDD compliant?
