# Implementation Plan: Development Prioritization Strategy

## Phase 1: Core Service Stabilization (Current)
**Goal:** Ensure the backbone services deploy and run predictably in staging.

### 1. Stabilize Core Deployments
- [ ] **Brain Gateway:** ✅ Fixed environment defaults and MCP TTY issues.
- [ ] **AI Agents:** Ensure sync with gateway API changes.
- [ ] **Client Portal:** Verify GTM-first discovery flow once gateway is stable.
- [ ] **Admin Dashboard:** Ensure standard deployment without 502 errors.

### 2. Pause Meta Workflows (To Reduce Noise)
- [ ] Disable automatic triggers for `production-readiness-testing.yml`.
- [ ] Disable automatic triggers for `ci-brain-gateway.yml`.
- [ ] Disable automatic triggers for `security-scan.yml`.
- *Note: These will still be available via `workflow_dispatch` (manual trigger).*

## Phase 2: Quality Hardening
**Goal:** Tighten the gates once feature development reaches a milestone.

### 1. Restore & Fix CI
- [ ] Fix existing `pytest` failures in Brain Gateway.
- [ ] Enable CI as a requirement for Pull Requests.

### 2. Production Readiness Enforcement
- [ ] Repair bash arithmetic and service wait logic in `production-readiness-testing.yml`.
- [ ] Ensure ZAP scans pass with defined baseline rules.
- [ ] Set "Production Readiness" as a mandatory check for `main` branch merges.

## Phase 3: Launch Optimization
**Goal:** Performance, monitoring, and automated recovery.

### 1. Scaling & Monitoring
- [ ] Integrate Grafana/Loki checks into deployment health.
- [ ] Finalize billing integration (Lago) readiness checks.

### 2. Performance Tuning
- [ ] Optimize CI build times using GitHub Actions caching.
- [ ] Implement automated rollback on deployment failure.
