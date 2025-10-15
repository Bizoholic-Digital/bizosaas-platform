# Temporal UI - Infrastructure

## Service Identity
- **Name**: Temporal UI
- **Type**: Infrastructure - Workflow Monitoring Tool
- **Container**: `bizosaas-temporal-ui-staging`
- **Image**: `temporalio/ui:latest`
- **Port**: `8083:8080`
- **Status**: ✅ Running
- **Purpose**: Web-based interface for monitoring and debugging Temporal workflows

## Architecture Classification
**Decision**: Keep in Infrastructure (NOT Frontend)
- Developer/DevOps tool for internal team
- Not customer-facing
- Shows technical workflow internals
- Tightly coupled with Temporal Server

## Configuration
```yaml
services:
  temporal-ui:
    image: temporalio/ui:latest
    container_name: bizosaas-temporal-ui-staging
    depends_on:
      - temporal-server
    environment:
      - TEMPORAL_ADDRESS=bizosaas-temporal-server-staging:7233
      - TEMPORAL_CORS_ORIGINS=http://localhost:8083
    ports:
      - "8083:8080"
    networks:
      - dokploy-network
```

## Access
- **Internal URL**: `http://194.238.16.237:8083`
- **Access Control**: IP whitelist or VPN only (NOT public)
- **Users**: Developers, DevOps, System Administrators

## Features
- View running workflows
- Monitor workflow history
- Debug failed workflows
- Visualize workflow execution
- Terminate/restart workflows
- View activity details

## Custom Dashboard Integration
For end users, build custom UI in:
- **Admin Dashboard**: System-wide workflow management
- **Client Portal**: User-specific campaign status

Use Temporal Python SDK to query workflow status and present in user-friendly format.

---
**Status**: ✅ Production-Ready
**Classification**: Infrastructure Tool
**Last Updated**: October 15, 2025
