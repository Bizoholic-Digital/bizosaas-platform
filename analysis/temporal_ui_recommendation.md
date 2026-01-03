# Temporal Workflow UI Recommendation

## Objective
To provide visibility and control over long-running background processes (e.g., content syncs, marketplace imports, listing optimizations) for both system administrators and end-users.

## User Persona Analysis

### 1. System Administrators (DevOps / Support)
*   **Needs**: Full visibility into workflow state, history, stack traces, and worker health. Ability to terminate, retry, or signal workflows.
*   **Tools**: Raw Temporal Web UI is ideal, but a simplified view in the Admin Dashboard is better for quick diagnosis without context switching.
*   **Location**: **Admin Dashboard** (`/dashboard/system-health` or `/dashboard/workflows`).

### 2. End-Users (Clients / Tenants)
*   **Needs**: "Is my sync finished?", "Why did it fail?", "How many products were imported?". They need human-readable status comparisons (e.g., "Shipped" vs "Processing") rather than technical terms (e.g., "ActivityTaskStarted").
*   **Tools**: A friendly "Activity Feed" or specific progress bars within the feature page (e.g., inside the Connectors card).
*   **Location**: **Client Portal** (`/dashboard/activity` and contextually within `/dashboard/connectors`).

## Recommendation

### A. Client Portal Implementation
**Strategy**: "Contextual Progress & Global Activity Feed"

1.  **feature-Specific Progress**:
    *   When a user clicks "Sync" on the **Amazon Connector**, show a progress bar *directly on the card*.
    *   Use Temporal Queries (e.g., `queryGetSyncProgress()`) to fetch real-time data: `{ "processed": 45, "total": 100, "status": "running" }`.

2.  **Global Activity Feed**:
    *   A notification center or sidebar showing recent async actions.
    *   Example:
        *   🟢 **Amazon Sync** - Completed (Syncing 402 products)
        *   🔵 **WordPress Post Import** - In Progress (45%)
        *   🔴 **Google Ads Campaign** - Failed (Invalid Token)

### B. Admin Dashboard Implementation
**Strategy**: "Orchestrator Control Plane"

1.  **Workflow Explorer**:
    *   A table listing all running workflows across *all tenants*.
    *   Columns: `Tenant`, `Type` (e.g., `SyncWorkflow`), `Status`, `StartTime`, `Duration`.
    *   Actions: `Terminate`, `Retry`, `View Logs`.

2.  **Direct Links**:
    *   Link to the self-hosted Temporal Web UI for deep debugging (stack traces).

## Technical Architecture

1.  **Backend (`brain-gateway`)**:
    *   Expose endpoints via gRPC client to Temporal.
    *   `GET /api/cms/workflows`: List workflows for current tenant.
    *   `GET /api/cms/workflows/{id}/status`: Query workflow state.
    *   `POST /api/cms/workflows/{id}/cancel`: Send cancellation signal.

2.  **Frontend**:
    *   Use `useQuery` with polling (every 3-5s) for active workflows.
    *   Optimistic UI updates when triggering actions.

## Next Steps
1.  Define the `SyncWorkflow` interface in `brain-service`.
2.  Implement `getProgress` query handler in the workflow.
3.  Add `/api/workflows` endpoints to `brain-gateway`.
