# Hexagonal Architecture & DDD Compliance Checklist

This checklist validates that the BizOSaaS platform follows DDD (Domain-Driven Design) and Hexagonal Architecture (Ports & Adapters) principles.

---

## 1. Core Domain Independence

| Check | Criteria | Status | Notes |
|-------|----------|--------|-------|
| ☐ | Brain Core business logic runs without external systems | 🔴 Not Met | Direct httpx calls to external services |
| ☐ | Swap WordPress → Drupal without changing core | 🟡 Partial | Connectors abstracted, but no port layer |
| ☐ | Domain models have no external dependencies | 🔴 Not Met | No formal domain models defined |

**Action Required:**
- Define domain entities (Content, Contact, Order, etc.) as pure Python classes
- Create port interfaces for each bounded context
- Inject adapters at runtime

---

## 2. Ports & Adapters Separation

| Check | Criteria | Status | Notes |
|-------|----------|--------|-------|
| ☐ | Ports defined as abstract interfaces | 🔴 Not Met | No abstract port classes |
| ☐ | Adapters implement port interfaces | 🔴 Not Met | Connectors are concrete, not implementing interfaces |
| ☐ | Brain Core depends on ports, not adapters | 🔴 Not Met | Direct imports of connector modules |

**Action Required:**
```python
# Example Port Definition
from abc import ABC, abstractmethod

class CMSPort(ABC):
    @abstractmethod
    async def get_posts(self, tenant_id: str) -> list[Post]:
        pass
    
    @abstractmethod
    async def publish_post(self, post: Post) -> bool:
        pass

# Example Adapter
class WordPressAdapter(CMSPort):
    async def get_posts(self, tenant_id: str) -> list[Post]:
        # WordPress-specific implementation
        pass
```

---

## 3. Bounded Contexts Isolation

| Check | Criteria | Status | Notes |
|-------|----------|--------|-------|
| ☐ | Each context has own models/services/events | 🟡 Partial | Some separation in ai-agents/agents/ |
| ☐ | No "God objects" crossing contexts | 🟡 Partial | Orchestrator touches multiple domains |
| ☐ | Ubiquitous language per context | 🔴 Not Met | Inconsistent terminology |
| ☐ | Context boundaries enforced via modules | 🟡 Partial | Directory structure shows intent |

**Platform Bounded Contexts (HOSTED):**
- ✅ AI Agents (`ai-agents/agents/`) - 47 agents + 10 crews
- ✅ Connectors (`brain-gateway/app/connectors/`) - 13 external system connectors
- ✅ Auth (`auth/`) - Authentication service (37KB FastAPI-Users)
- ✅ Workflows (`temporal-integration/`) - Temporal orchestration (14KB)
- ☐ Orchestration (`brain-gateway/domain/`) - Agent routing and coordination (TO CREATE)

**External System Connectors (NOT HOSTED - Data lives externally):**
- 🔴 CRM Connector Interface (no port layer) → Zoho, HubSpot, Salesforce
- 🔴 CMS Connector Interface (no port layer) → WordPress, Drupal, Webflow
- 🔴 Commerce Connector Interface (no port layer) → Shopify, WooCommerce, Saleor
- 🔴 Analytics Connector Interface (no port layer) → GA4, Mixpanel, Amplitude
- 🔴 Billing Connector Interface (no port layer) → Stripe, PayPal, Razorpay

**Note:** BizOSaaS does NOT store CRM/CMS/Commerce/Analytics data. All data remains in external systems and is accessed via connectors in real-time.

---

## 4. Event-Driven Communication

| Check | Criteria | Status | Notes |
|-------|----------|--------|-------|
| ☐ | Contexts communicate via domain events | 🔴 Not Met | No event bus |
| ☐ | No direct cross-context function calls | 🔴 Not Met | Direct imports used |
| ☐ | Events are immutable, timestamped | 🔴 Not Met | No events defined |
| ☐ | Event handlers are async | 🔴 Not Met | No handlers |

**Action Required:**
```python
# Domain Event
@dataclass(frozen=True)
class ContentPublished:
    content_id: str
    tenant_id: str
    published_at: datetime
    publisher_id: str

# Event Bus (Redis Streams)
async def publish_event(event: DomainEvent):
    await redis.xadd(f"events:{event.tenant_id}", event.to_dict())
```

---

## 5. Canonical Data Model

| Check | Criteria | Status | Notes |
|-------|----------|--------|-------|
| ☐ | 12 core entities defined | 🔴 Not Met | No canonical entities |
| ☐ | External data mapped to canonical | 🔴 Not Met | Raw data passed through |
| ☐ | Canonical schema is version-controlled | 🔴 Not Met | No schema files |

**Required Canonical Entities:**
1. Content
2. MediaAsset
3. Contact
4. Account
5. Deal
6. Product
7. Order
8. Event (analytics)
9. Segment
10. Workflow
11. AgentDecision
12. AuditRecord

---

## 6. Testability

| Check | Criteria | Status | Notes |
|-------|----------|--------|-------|
| ☐ | Domain logic unit-testable without externals | 🔴 Not Met | Would need mocking |
| ☐ | Ports can be mocked for tests | 🔴 Not Met | No ports to mock |
| ☐ | Integration tests verify adapter behavior | 🟡 Partial | Some test files exist |

---

## 7. Explainability & Audit

| Check | Criteria | Status | Notes |
|-------|----------|--------|-------|
| ☐ | Agent decisions log inputs/outputs/policies | 🟡 Partial | Agents have verbose mode |
| ☐ | Audit trail: Actor → Decision → Context → Policy | 🔴 Not Met | No audit logging |
| ☐ | Immutable, tamper-evident logs | 🔴 Not Met | No audit tables |
| ☐ | Evidence export for compliance | 🔴 Not Met | Not implemented |

---

## Overall Compliance Score

| Principle | Score | Target |
|-----------|-------|--------|
| Domain Independence | 15% | 100% |
| Ports & Adapters | 10% | 100% |
| Bounded Contexts | 45% | 100% |
| Event-Driven | 0% | 100% |
| Canonical Model | 5% | 100% |
| Testability | 25% | 100% |
| Explainability | 20% | 100% |
| **Overall** | **17%** | **100%** |

---

## Priority Actions to Achieve Compliance

### Immediate (Week 1-2)
1. Define canonical entities as Python dataclasses
2. Create abstract port interfaces for CMS, CRM, Commerce
3. Refactor connectors to implement port interfaces

### Short-term (Week 3-4)
4. Implement Redis Streams event bus
5. Define core domain events
6. Create audit logging middleware

### Medium-term (Week 5-8)
7. Complete bounded context isolation
8. Implement CQRS read/write separation
9. Add comprehensive test coverage

---

## Verification Process

1. **Architecture Review Workshop**
   - Walk through each bounded context
   - Verify ports/adapters separation
   - Check event flows

2. **Code Audit**
   - Ensure domain logic has no external imports
   - Confirm adapters implement interfaces

3. **Swap Test**
   - Replace WordPress adapter with Drupal
   - Brain Core should remain unchanged

4. **Event Traceability**
   - Verify workflows triggered by events
   - No hard-coded cross-context calls
