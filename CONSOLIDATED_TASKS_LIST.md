# Consolidated Tasks Master List - BizOSaaS Platform

**Last Updated:** January 9, 2026  
**Status:** Initializing Implementation Phase

---

## 🚦 Project Status Overview

| Category | Total Tasks | Completed | Progress |
|----------|-------------|-----------|----------|
| **Client Portal (CP)** | 28 | 8 | 28% |
| **Admin Dashboard (AD)** | 14 | 2 | 14% |
| **Backend Testing (BT)** | 19 | 4 | 21% |
| **Monitoring (MO)** | 10 | 5 | 50% |
| **Service Health (SH)** | 10 | 1 | 10% |
| **Testing Suite (TS)** | 10 | 0 | 0% |
| **Cross-Portal (XP)** | 5 | 1 | 20% |
| **TOTAL** | **96** | **21** | **21.9%** |

---

## 📝 Master Task List

### 1. Client Portal (CP)
| Status | ID | Task | Priority | Est. | Progress/Notes |
|:---:|:---|:---|:---:|:---:|:---|
| [x] | CP-001 | Connector selection modal in Launch Discovery | P1 | 8h | Implemented DiscoveryModal with two-step flow |
| [ ] | CP-002 | Intelligent service recommendation engine | P1 | 12h | - |
| [x] | CP-003 | Dashboard cards clickable (Connectors, Tasks, Traffic) | P1 | 4h | Implemented Link wrappers and hover effects |
| [x] | CP-004 | CRM & Contacts connector display (FluentCRM, HubSpot) | P1 | 6h | Added toggle and unified view in CRM page |
| [ ] | CP-005 | Replicate connector display for CMS/eCommerce | P2 | 4h | - |
| [x] | CP-006 | Project navigation and "View All" button | P1 | 6h | Added view-all in dashboard and project footer |
| [ ] | CP-007 | Optimize mobile project view (scrollable) | P2 | 4h | - |
| [x] | CP-008 | Fix Plane.so project/task creation logic | P0 | 10h | Implemented perform_action in plane.py |
| [x] | CP-009 | Assignee dropdown with Plane.so user list | P1 | 8h | Added member fetching and dropdown in TaskForm |
| [ ] | CP-010 | Expand CMS content types (Categories, Media, CPTs) | P2 | 12h | - |
| [ ] | CP-011 | WordPress Plugin Marketplace integration | P2 | 16h | - |
| [ ] | CP-012 | Fix WP plugin detection logic (WooCommerce etc) | P2 | 6h | - |
| [ ] | CP-013 | Fix Marketing tab functionality (Real Data) | P1 | 10h | - |
| [ ] | CP-014 | Implement AI Insights actions (Execute with Agent) | P1 | 12h | - |
| [x] | CP-015 | Fix BYOK API key validation (OpenRouter etc) | P0 | 8h | Added /test endpoint & LLM connectors |
| [ ] | CP-016 | Enable "Create Custom Agent" functionality | P1 | 14h | - |
| [ ] | CP-017 | Implement "New Workflow" builder | P1 | 20h | - |
| [ ] | CP-018 | Fix Workflow CSS (DEMO badge, Worker icons) | P3 | 6h | - |
| [ ] | CP-019 | Enable Workflow configuration modal | P2 | 8h | - |
| [ ] | CP-020 | Implement Workflow state controls (Pause/Play) | P2 | 10h | - |
| [ ] | CP-021 | Add Workflow visualization page (DAG viewer) | P2 | 16h | - |
| [ ] | CP-022 | Build Workflow optimization engine | P2 | 18h | - |
| [ ] | CP-023 | Fix Portal Settings navigation (Clickable cards) | P2 | 4h | - |
| [ ] | CP-024 | Optimize mobile Settings layout | P3 | 6h | - |
| [ ] | CP-025 | RBAC for Platform Admin link | P1 | 4h | - |
| [ ] | CP-026 | Make recent activity clickable/redirectable | P2 | 8h | - |
| [x] | CP-027 | Remove gradients from all buttons | P3 | 4h | Removed gradients from UnifiedLoginForm buttons |
| [ ] | CP-028 | Fix CSS/Font visibility across themes | P2 | 8h | - |

### 2. Admin Dashboard (AD)
| Status | ID | Task | Priority | Est. | Progress/Notes |
|:---:|:---|:---|:---:|:---:|:---|
| [ ] | AD-001 | Replicate Client Portal mobile layout | P3 | 6h | - |
| [ ] | AD-002 | Standardize page titles/subtitles | P3 | 4h | - |
| [ ] | AD-003 | Improve Agent Management UI (Mobile tabs) | P2 | 8h | - |
| [ ] | AD-004 | Specialist Agent mesh actions (Configure, Logs) | P1 | 12h | - |
| [ ] | AD-005 | Optimize Supervisor cards (Mobile overflow) | P3 | 4h | - |
| [x] | AD-006 | Fix Tenant Management UI (Mobile overflow) | P2 | 6h | Rewrote tenants/page.tsx with real API data |
| [ ] | AD-007 | Clickable Organization cards (Redirection) | P2 | 4h | - |
| [ ] | AD-008 | Fix Global User Management UI (Refinement) | P2 | 6h | - |
| [ ] | AD-009 | Replicate User fixes to Partner page | P2 | 4h | - |
| [ ] | AD-010 | Define Connectivity Hub purpose/design | P1 | 2h | - |
| [ ] | AD-011 | Implement Infrastructure monitoring view | P1 | 12h | - |
| [ ] | AD-012 | Implement Connector analytics view | P1 | 10h | - |
| [x] | AD-013 | Fix Security page client-side error | P0 | 4h | Added safety checks for missing user email |
| [ ] | AD-014 | Implement Admin Settings page | P1 | 12h | - |

### 3. Backend Testing (BT)
| Status | ID | Task | Priority | Est. | Progress/Notes |
|:---:|:---|:---|:---:|:---:|:---|
| [x] | BT-001 | Set up pytest for Brain Gateway | P0 | 6h | Pytest framework established in testing/backend |
| [x] | BT-002 | Create API testing framework (httpx) | P0 | 8h | Added test_integration.py with TestClient |
| [x] | BT-003 | Implement test database seeding & isolation | P0 | 10h | Implemented in test_integration.py fixtures |
| [x] | BT-004 | Unit Tests: AI Agent Services | P1 | 16h | Implemented test_agents.py and test_mcp.py |
| [ ] | BT-005 | Unit Tests: Connector Services | P1 | 20h | - |
| [ ] | BT-006 | Unit Tests: RAG/KAG Services | P1 | 12h | - |
| [ ] | BT-007 | Unit Tests: Workflow Services | P1 | 14h | - |
| [ ] | BT-008 | Unit Tests: MCP Orchestrator | P1 | 10h | - |
| [ ] | BT-009 | Integration: Gateway ↔ Database | P1 | 8h | - |
| [ ] | BT-010 | Integration: Gateway ↔ Redis | P1 | 6h | - |
| [ ] | BT-011 | Integration: Gateway ↔ Vault | P1 | 8h | - |
| [ ] | BT-012 | Integration: Gateway ↔ Temporal | P1 | 10h | - |
| [ ] | BT-013 | Integration: External Services (WP, CRM, etc) | P1 | 16h | - |
| [ ] | BT-014 | E2E API: Onboarding flow | P1 | 12h | - |
| [ ] | BT-015 | E2E API: Campaign creation flow | P1 | 10h | - |
| [ ] | BT-016 | E2E API: Data sync flows | P1 | 12h | - |
| [ ] | BT-017 | Performance: Set up Locust | P1 | 8h | - |
| [ ] | BT-018 | Performance: Multi-user load tests | P1 | 12h | - |
| [ ] | BT-019 | Database: Query profiling/optimization | P1 | 10h | - |

### 4. Monitoring & Observability (MO)
| Status | ID | Task | Priority | Est. | Progress/Notes |
|:---:|:---|:---|:---:|:---:|:---|
| [x] | MO-001 | Install OpenTelemetry SDK | P0 | 4h | Added to requirements.txt |
| [x] | MO-002 | Configure Exporters (Prometheus/OTLP) | P0 | 6h | Implemented OTLPSpanExporter in main.py |
| [x] | MO-003 | Instrument API Endpoints | P0 | 8h | Added FastAPIInstrumentor to main.py |
| [x] | MO-004 | Instrument AI Agent execution | P1 | 10h | Added OTel spans and metrics to chat_with_agent |
| [ ] | MO-005 | Instrument Connector operations | P1 | 8h | - |
| [ ] | MO-006 | Define Custom Metrics (Success/Latency) | P1 | 6h | - |
| [ ] | MO-007 | Implement Metrics Collectors | P1 | 8h | - |
| [x] | MO-008 | Set up Grafana Dashboards | P1 | 12h | Created Platform Overview JSON dashboard |
| [ ] | MO-009 | Standardize Structured Logging (JSON) | P2 | 6h | - |
| [ ] | MO-010 | Configure Log Aggregation (Loki) | P2 | 6h | - |

### 5. Service Health (SH)
| Status | ID | Task | Priority | Est. | Progress/Notes |
|:---:|:---|:---|:---:|:---:|:---|
| [x] | SH-001 | Create Health Check API Endpoint | P0 | 8h | Upgraded /health with dependency checks |
| [ ] | SH-002 | Dependency Health Graph | P1 | 10h | - |
| [ ] | SH-003 | Metrics Aggregation API | P1 | 8h | - |
| [ ] | SH-004 | System Status Dashboard (Admin) | P1 | 12h | - |
| [ ] | SH-005 | Detailed Service Views (Logs/Metrics) | P1 | 10h | - |
| [ ] | SH-006 | OTel Metrics Visualization | P1 | 14h | - |
| [ ] | SH-007 | Real-time monitoring (WebSockets) | P1 | 12h | - |
| [ ] | SH-008 | API Endpoint Status Analytics | P1 | 10h | - |
| [ ] | SH-009 | Define Automated Alerting Rules | P1 | 6h | - |
| [ ] | SH-010 | Implement Notifications (Email/Webhook) | P1 | 10h | - |

### 6. Testing Suite (TS)
| Status | ID | Task | Priority | Est. | Progress/Notes |
|:---:|:---|:---|:---:|:---:|:---|
| [ ] | TS-001 | Expand Playwright E2E Suite | P1 | 20h | - |
| [ ] | TS-002 | Accessibility Testing (Axe) | P1 | 12h | - |
| [ ] | TS-003 | Mobile Device Testing Suite | P1 | 14h | - |
| [ ] | TS-004 | Postman/Newman Collection | P2 | 16h | - |
| [ ] | TS-005 | API Contract Testing | P2 | 12h | - |
| [ ] | TS-006 | Security Scans (OWASP ZAP) | P1 | 10h | - |
| [ ] | TS-007 | Auth Testing (JWT/RBAC) | P1 | 8h | - |
| [ ] | TS-008 | CI/CD Integration (GitHub Actions) | P1 | 8h | - |
| [ ] | TS-009 | Automated Test Reporting | P2 | 4h | - |
| [ ] | TS-010 | Finalize Testing Guidelines Documentation | P2 | 6h | - |

### 7. Cross-Portal Improvements (XP)
| Status | ID | Task | Priority | Est. | Progress/Notes |
|:---:|:---|:---|:---:|:---:|:---|
| [ ] | XP-001 | Clarify "System Status" indicators | P2 | 4h | - |
| [ ] | XP-002 | Sidebar integration for System Health | P2 | 6h | - |
| [x] | XP-003 | Fix Notification Bell functionality | P0 | 10h | Implemented dropdown in both portals |
| [ ] | XP-004 | Implement automated link checker | P2 | 8h | - |
| [ ] | XP-005 | UI/UX automated audit tool | P2 | 12h | - |

---

## 📅 Summary & Timeline

- **Total Tasks:** 96
- **Total Effort:** ~784 Effective Hours
- **Critical Path:** BT-00x → MO-00x → SH-00x
- **UI/UX Stability:** CP-00x → AD-00x → XP-00x

**Update Instructions:**
1. Change `[ ]` to `[x]` when completed.
2. Update the "Completed" count and "Progress %" in the Status Overview table.
3. Add implementation notes or PR links in the "Progress/Notes" column.
