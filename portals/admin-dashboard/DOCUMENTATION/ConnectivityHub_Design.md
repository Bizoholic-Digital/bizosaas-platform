# Connectivity Hub - Design & Purpose (Admin Dashboard)

## Purpose
The Connectivity Hub in the Admin Dashboard is the centralized control plane for all external integrations across the BizOSaaS platform. While the Client Portal allows individual tenants to connect their own accounts, the Admin Connectivity Hub provides global oversight and control.

## Key Features

### 1. Global Connector Management
- **Lifecycle Control**: Enable or disable specific connectors platform-wide (e.g., disable "Facebook Ads" if the API integration is undergoing maintenance).
- **Version Control**: Manage and upgrade connector versions (Mcp versions).
- **Global Config**: Set platform-level default configurations or restricted fields.

### 2. Connectivity Health Monitoring
- **Real-time Status**: View the health of API connections to major providers (Google, Meta, OpenAI, etc.).
- **Error Tracking**: Global log of connection failures across all tenants to identify systemic issues with a specific connector.
- **Rate Limit Monitoring**: Track global API usage to avoid hitting provider-level rate limits.

### 3. Analytics & Demand (Ref AD-012)
- **Usage Stats**: See which connectors are most popular.
- **Revenue Impact**: If certain connectors are part of premium plans, track their conversion/retention impact.
- **Marketplace Demand**: Track searches and requests for uninstalled connectors to prioritize development.

### 4. Direct Support & Debugging
- **Tenant Impersonation (Debug)**: Allow admins to view the connection status for a specific tenant to help debug integration issues.
- **Manual Sync Trigger**: Capacity to trigger a global sync or a specific tenant-service sync if needed.

## UI/UX Design Goals
- **High-level Dashboard**: Aggregate status cards showing "Total Active Connections", "Degraded Services", and "Top Used Connectors".
- **Functional Grid**: Similar to the Client Portal's grid but with "Manage" and "Logs" actions instead of just "Connect".
- **Detailed Audit View**: A searchable table of all tenant-service connections with status, last sync time, and error codes.
