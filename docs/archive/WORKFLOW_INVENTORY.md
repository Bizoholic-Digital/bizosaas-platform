# BizOSaaS Workflow Inventory

This document outlines all currently defined and planned workflows, categorized by target portal (Client vs. Admin) and identifying Human-In-The-Loop (HITL) requirements.

## 🏢 Client Portal Workflows
*Targeted at individual business owners and agency clients.*

| Workflow Name | Description | HITL Requirement | Status |
| :--- | :--- | :--- | :--- |
| **Campaign Strategy & Generation** | AI analyzes goals and generates multi-channel ad copy/assets. | **Yes**: Client must approve creative & budget. | Planned |
| **SEO Content Pipeline** | Researcher + Writer + Editor agents produce optimized blog posts. | **Yes**: Client review before publishing to WordPress/CMS. | Planned |
| **Autonomous Lead Nurturing** | Real-time lead scoring and automated email/CRM follow-ups. | No (Autonomous) | In Progress |
| **Order Processing & Fraud** | E-commerce order validation, inventory check, and shipping labels. | **Yes**: Manual review for high-value or high-risk orders. | Planned |
| **Digital Presence Audit** | 4-agent crew performs technical, SEO, and social audits. | No (Automated Report) | Implemented (Core) |
| **Social Media Scheduling** | Automated cross-platform posting and engagement monitoring. | Optional (Approval mode) | Planned |

## 🛠️ Admin Portal Workflows
*Targeted at platform owners and Master Partners for system-wide orchestration.*

| Workflow Name | Description | HITL Requirement | Status |
| :--- | :--- | :--- | :--- |
| **Multi-Tenant Billing Cycle** | Aggregates Lago usage, generates invoices, and processes Stripe. | **Yes**: Admin approval for disputes/overrides. | Planned |
| **AI Partner Assignment** | New client intake → Capacity evaluation → Skill-based partner mapping. | Optional (Auto-assign available) | In Progress |
| **Role Migration (Partner)** | Validating performance metrics before promoting Client to Partner. | **Yes**: Admin must execute final role change. | Planned |
| **System Scale & Health** | Automated resource monitoring and container scaling via Dokploy/Temporal. | No (Autonomous) | Planned |
| **Global Ticket Triage** | AI triage of support tickets across all tenants to expert agents. | **Yes**: Human support agent escalation. | Planned |
| **Affiliate Payout Review** | Quarterly review of referral earnings and automated payout execution. | **Yes**: Final payout validation by Finance. | Planned |

## 🏗️ Implementation Guidelines
1. **Engine**: All workflows use **Temporal** for durability and state management.
2. **Logic**: AI logic is implemented via **CrewAI** (Multi-agent) or **LangChain** (Single-agent) in `bizosaas-brain-core`.
3. **HITL Interface**:
   - Client HITL tasks appear in the "Pending Actions" section of the Client Portal.
   - Admin HITL tasks appear in the "Optimization & Approvals" tab of the Admin Dashboard.
