# BizOSaaS Platform - Port Allocation Guide

**CRITICAL**: This document must be updated whenever new services are added to prevent port conflicts.

## Current Port Assignments

### Frontend Applications

| Port | Service | URL | Description | Status |
|------|---------|-----|-------------|--------|
| 3006 | Client Portal | http://localhost:3006 | Tenant-specific dashboard | ✅ Active |
| 3007 | CorelDove Frontend | http://localhost:3007 | E-commerce storefront | ✅ Active |
| 3008 | Bizoholic Frontend | http://localhost:3008 | Marketing agency website | ✅ Active |
| 3009 | **BizOSaaS SQLAlchemy Admin** | http://localhost:3009/admin | **🎯 CONSOLIDATED: Database + Workflow + Analytics Admin** | ✅ Active |
| 3010 | Business Directory | http://localhost:3010 | **Business directory listings** | ✅ Active |
| 3011 | **DEPRECATED** | ~~http://localhost:3011~~ | ~~Super Admin Dashboard~~ **→ MIGRATED TO 3009** | ❌ Shutdown |
| 3012 | CoreLDove Frontend (Clean) | http://localhost:3012 | **Fixed e-commerce storefront** | ✅ Active |

### Backend Services

| Port | Service | URL | Description | Status |
|------|---------|-----|-------------|--------|
| 8001 | FastAPI AI Central Hub | http://localhost:8001 | **Main backend orchestration** | ✅ Active |
| 8000 | Django CRM | http://localhost:8000 | Customer relationship management | ⚠️ Check |
| 8002 | Wagtail CMS | http://localhost:8002 | Content management system | ⚠️ Check |
| 8003 | Saleor E-commerce | http://localhost:8003 | E-commerce backend | ⚠️ Check |

### Database & Infrastructure

| Port | Service | URL | Description | Status |
|------|---------|-----|-------------|--------|
| 5432 | PostgreSQL | localhost:5432 | Main database | ⚠️ Check |
| 5433 | BizOSaaS PostgreSQL | localhost:5433 | BizOSaaS specific database | ✅ Active |
| 6379 | Redis | localhost:6379 | Cache and sessions | ✅ Active |
| 6380 | Saleor Redis | localhost:6380 | Saleor-specific cache | ⚠️ Check |

## Service Architecture

### 🎯 **CONSOLIDATED BizOSaaS SQLAlchemy Admin (Port 3009)**
- **Primary Purpose**: **ALL-IN-ONE Platform Administration** 
- **🔥 MAJOR ENHANCEMENT**: **Migrated ALL workflow management features from port 3011**
- **Key Features**:
  - ✅ **Official SQLAdmin interface with default theme**
  - ✅ **Comprehensive Workflow Management Dashboard**
  - ✅ **AI Agent orchestration and monitoring**
  - ✅ **Multi-tenant analytics and insights**
  - ✅ **Real-time system health monitoring**
  - ✅ **Revenue and subscription analytics**
  - ✅ **Security audit and compliance tracking**
  - ✅ **API usage analytics and rate limiting**
  - ✅ **Workflow execution control (start/pause/stop)**
  - ✅ **Auto-discovery of all database tables**
  - ✅ **Full CRUD operations with search & filtering**
- **Access**: http://localhost:3009/admin
- **API Endpoints**: 
  - `/workflow-dashboard` - Real-time workflow monitoring
  - `/workflow/{id}/action` - Control workflow execution
  - `/revenue-analytics` - Financial metrics
  - `/stats` - Platform statistics
- **Authentication**: Platform owner access
- **Models**: Tenant, User, AIWorkflow, Campaign, SystemMetric, APIUsage, WorkflowExecution, RevenueMetric, SecurityEvent

### ❌ **DEPRECATED: Port 3011** 
- **Status**: **SHUTDOWN & MIGRATED**
- **Reason**: All features successfully consolidated into SQLAlchemy Admin (port 3009)
- **Migration Date**: September 20, 2025

### Business Directory (Port 3010)
- **Primary Purpose**: Business listings and directory services
- **Status**: ✅ Restored and functional
- **Note**: Was temporarily broken due to port conflict

## Port Conflict Prevention Rules

### 🚨 MANDATORY RULES:

1. **Always check this guide** before starting new services
2. **Update this document** immediately when adding new services
3. **Use environment variables** for port configuration when possible
4. **Test port availability** with `netstat -tulpn | grep :PORT` before starting
5. **Document service dependencies** and required co-running services

### 🔧 Service Startup Order:

1. **Infrastructure First**: PostgreSQL, Redis
2. **Backend Services**: FastAPI Hub, Django, Wagtail, Saleor
3. **Frontend Applications**: Admin dashboards, then client-facing apps

### 📱 Quick Access URLs:

```bash
# 🎯 CONSOLIDATED PLATFORM ADMINISTRATION
http://localhost:3009/admin

# DEPRECATED (Migrated to 3009)
# http://localhost:3011

# Business Directory
http://localhost:3010

# E-commerce (Fixed)
http://localhost:3012

# Client Portal
http://localhost:3006

# Marketing Site
http://localhost:3008
```

## Workflow Management Features

The BizOSaaS Admin (port 3011) includes comprehensive workflow management:

### ✅ Currently Implemented:
- **Workflow Status Overview**: Real-time monitoring of all AI workflows
- **AI Agent Management**: Control and monitor AI agent executions
- **Multi-tenant Analytics**: Cross-tenant performance metrics
- **System Health Monitoring**: Platform-wide infrastructure status
- **Integration Dashboard**: Third-party service monitoring

### 📋 Planned Features:
- Revenue & subscription analytics
- User & tenant management interface
- API usage & rate limiting dashboard
- Security audit & compliance monitoring

## Port Range Reservations

- **3000-3099**: Frontend applications and admin interfaces
- **8000-8099**: Backend API services
- **5000-5999**: Database services
- **6000-6999**: Cache and messaging services
- **7000-7999**: Monitoring and logging services

## Emergency Procedures

### Port Conflict Resolution:
1. Stop conflicting service: `pkill -f "port XXXX"`
2. Check this guide for correct assignment
3. Start service on correct port
4. Update documentation if needed
5. Test all dependent services

### Service Health Check:
```bash
# Check all ports
netstat -tulpn | grep -E ":(3006|3007|3008|3009|3010|3011|3012|8001)"

# Test specific service
curl -s http://localhost:PORT/health || curl -s http://localhost:PORT/
```

---

**Last Updated**: September 20, 2025  
**Updated By**: Claude Code Assistant  
**Next Review**: When adding new services

**⚠️ CRITICAL**: Always update this document when making port changes!