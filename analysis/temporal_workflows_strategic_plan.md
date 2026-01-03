# Strategic Temporal Workflow Plan - BizOSaaS Platform

## 1. Core Workflow Inventory

### CMS & Content Workflows
| Workflow Name | Purpose | Trigger |
|---------------|---------|---------|
| `SyncWordPressContent` | Incremental sync of posts/pages to Vector DB | Scheduled (Every 4h) / Manual |
| `OptimizeMediaAssets` | Lossless compression and WebP conversion for synced media | Hook from `SyncWordPressContent` |
| `PublishCrossPlatform` | Publish a single piece of content to multiple CMS/Socials | User Action |

### E-commerce & Inventory Workflows
| Workflow Name | Purpose | Trigger |
|---------------|---------|---------|
| `ReconcileInventory` | Master inventory reconciliation between Woo, Shopify, Amazon | Scheduled (Every 15m) |
| `SyncMerchantOrders` | Fetch orders from all connected marketplaces for central dashboard | Scheduled (Every 10m) |
| `ProcessOrderFulfillment` | Update tracking info across platforms when an order is shipped | Hook from Fulfillment Service |

### Marketing & Analytics Workflows
| Workflow Name | Purpose | Trigger |
|---------------|---------|---------|
| `RefreshAdPerformance` | Recompute ROAS for Google/Meta/TikTok ads | Scheduled (Daily) |
| `SyncCRMContacts` | Bi-directional sync between WordPress leads and FluentCRM/HubSpot | Hook from lead form / Scheduled |
| `GenerateMarketingReport` | AI-summarized weekly performance report | Scheduled (Weekly) |

### Infrastructure & Operations Workflows
| Workflow Name | Purpose | Trigger |
|---------------|---------|---------|
| `TenantProvisioning` | Orchestrate creation of Database, Vault path, and Clerk org | Onboarding Action |
| `AutomatedSystemBackup` | Backup all platform databases and unseal keys | Scheduled (Daily) |
| `SecurityAuditScan` | Scan all tenant connections for rotated/invalid tokens | Scheduled (Weekly) |

## 2. AI Monitoring & Workflow Proposer (The "Orchestrator Agent")

### Objective
Maintain an autonomous agent that monitors platform logs, performance metrics, and human activity to identify bottlenecks that could be solved by a new workflow.

### Architecture
1.  **Monitor**: Continuesly watch for repeated high-latency tasks or bulk operations.
2.  **Analyze**: If a manual repeated process is detected, the agent drafts a Temporal Workflow (DSL format).
3.  **Draft Mode**: The workflow is stored in the `DraftWorkflows` collection in the DB.
4.  **HITL (Human In The Loop)**:
    *   The Admin Dashboard displays a notification: "New Workflow Optimization Proposed: `BatchImageOptimizer`".
    *   Super Admin reviews the proposed logic and triggers.
    *   Once Approved, the agent generates the boilerplate code and registers the workflow in the Temporal Cluster.

## 3. Human In The Loop (HITL) Workflow System

### UI in Admin Dashboard
*   **Location**: `/dashboard/workflows/drafts`
*   **Features**:
    *   `Diff View`: See what the workflow replaces or improves.
    *   `Simulation`: Run a test pass in a sandbox tenant.
    *   `Approval Toggle`: Move from `Draft` -> `Production`.

## 4. Immediate Priority: Google OAuth Simplification

### The Flow
1.  **UI**: "Connect Google Business" button redirects to `/api/auth/google/start`.
2.  **Workflows**:
    *   `GoogleOAuthCallbackWorkflow`: Standardizes token exchange.
    *   `GoogleServiceProvisioningWorkflow`: Child workflow that initializes GBP, Search Console, and Ads if scopes are available.

## 5. Next Implementation Steps
1.  Define the `DraftWorkflow` DB schema.
2.  Implement the `/api/workflows/proposals` endpoint for the AI Agent.
3.  Build the HITL Approval interface in the Admin Dashboard.
