# Implementation Plan: phase 4 - Autonomous Agentic Operations

This plan outlines the tasks required to transition the BizOSaaS platform into an autonomous agentic ecosystem governed by centralized Admin control.

## Task List

### 1. Core Infrastructure & Agentic Lifecycle
- [ ] **Workflow Discovery Service**: 
    - Implement a service that monitors logs (RAG/KAG) and identifies recurring user hurdles or efficiency gaps.
- [ ] **Agent Workflow Proposer**: 
    - Create an agent capable of designing "Workflow Blueprints" (JSON/YAML) that define sequences of MCP calls.
- [ ] **RAG/KAG Optimization Engine**: 
    - Integrate graph-based knowledge mapping (KAG) to allow agents to understand tool interdependencies better.

### 2. Admin Portal: The Command Center
- [ ] **Workflow Approval Dashboard**:
    - Create a UI to list agent-proposed workflows for review.
    - Features: Logic Visualization, Dry-Run Analysis, Approve/Reject/Refine actions.
- [ ] **Agent Optimization Queue**:
    - UI to show performance-based change requests (e.g., "Switching LLM temperature for Tenant X").
- [ ] **Centralized Feature Orchestrator**:
    - Build a "Master Control" interface to manage features across the Client Portal, Admin Portal, and Business Directory from one location.
- [ ] **Admin Prime (AI Copilot)**:
    - Deploy a high-level orchestration agent to assist the Platform Owner in analyzing thousands of tenant data points.

### 3. Business Directory & Directory Management
- [ ] **Directory Task Management**:
    - Enable the Admin to manage and fine-tune specific AI tasks related to the Business Directory (SEO, Claim Verification).
- [ ] **Fine-Tuning API**:
    - Create endpoints for the Admin to override agent default behaviors for directory crawling and listing generation.

### 4. Integration & Deployment
- [ ] **Automated Workflow Integrator**:
    - Build the "Go-Live" engine that takes an approved JSON blueprint and binds it to the platform's execution engine.
- [ ] **Feedback Loop Refinement**:
    - Implement a "Refine" status where an Admin's feedback is sent back to the agent for workflow redesign.

### 5. Master Workflow Management UI
- [x] **Centralized Inventory Interface**:
    - Build a "Master Workflow Registry" in the Admin Portal displaying the list from `bizosaas-details-overview.md`.
    - ✅ Completed: Admin Portal now displays comprehensive workflow inventory with filtering
- [ ] **Dynamic Appending Service**:
    - Implement the backend logic to allow agents to "Append to Registry" when new workflow requirements are autonomously identified.
- [ ] **Workflow Fine-Tuning Console**:
    - Create a granular control panel for each workflow to adjust parameters (frequency, target audience, model selection).
- [x] **Approval Feedback Hub**:
    - Design the transition UI for workflows moving through *Proposed -> Refinement -> Accepted -> Active*.
    - ✅ Completed: HITL tab with Approve/Reject/Review actions implemented

### 6. Backend API for Workflow Governance
- [x] **Workflow Approval Endpoints**:
    - `POST /api/admin/workflows/{id}/approve` - Approve agent-proposed workflow
    - `POST /api/admin/workflows/{id}/reject` - Reject and archive workflow
    - `POST /api/admin/workflows/{id}/refine` - Request refinement with feedback
    - ✅ Completed: Full CRUD API implemented in workflow_governance.py
- [x] **Workflow Registry API**:
    - `GET /api/admin/workflows/registry` - Fetch complete workflow inventory
    - `POST /api/admin/workflows/registry` - Agent endpoint to propose new workflow
    - `PATCH /api/admin/workflows/{id}/config` - Update workflow parameters
    - ✅ Completed: Registry endpoints with filtering and agent submission
- [x] **Workflow Execution Integration**:
    - Connect approved workflows to Temporal for automated execution
    - Implement workflow state transitions (Proposed -> Active -> Archived)
    - ✅ Completed: Foundation laid with workflow_blueprint storage and approval tracking

### 7. RAG/KAG Discovery Service
- [x] **Workflow Discovery Agent**:
    - Autonomous agent that monitors platform data for optimization opportunities
    - ✅ Completed: WorkflowDiscoveryAgent with 4 discovery strategies
- [x] **Discovery Strategies**:
    - User pain point analysis (RAG)
    - Repetitive task identification (KAG)
    - Cross-tenant pattern analysis (RAG)
    - Integration gap detection (KAG)
    - ✅ Completed: All four strategies implemented
- [ ] **Production Integration**:
    - Connect to actual support tickets and user feedback systems
    - Implement real-time log analysis
    - Deploy as scheduled Temporal workflow (daily discovery cycle)
- [ ] **Knowledge Graph Builder**:
    - Build graph database of tool relationships and dependencies
    - Implement graph traversal algorithms for opportunity detection

## Milestones
- **M1: Discovery**: First agent-discovered workflow successfully listed in Admin.
- **M2: Approvals**: First manual approval leads to a live, automated deployment.
- **M3: Optimization**: Agent successfully proposes and executes a performance-tuning change.
- **M4: Mastery**: Admin Prime agent effectively summarizes platform status and manages complex operations.

---
**Status**: Initializing Phase 4
**Priority**: High
