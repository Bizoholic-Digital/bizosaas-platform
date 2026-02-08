# BizOSaaS Consolidated SQLAlchemy Admin

## 🎯 Overview

This is the **consolidated platform administration dashboard** that combines:
- **Official SQLAlchemy Admin** interface with Bizoholic Digital branding
- **Comprehensive workflow management** (migrated from port 3011)
- **Multi-tenant analytics and monitoring**
- **Revenue tracking and subscription analytics**
- **AI agent orchestration and control**
- **Security event monitoring**

## ✅ Features

### Core Administration
- ✅ **Official SQLAlchemy Admin** from https://github.com/aminalaee/sqladmin
- ✅ **Bizoholic Digital branding** with logo
- ✅ **9 Database Models**: Tenant, User, AIWorkflow, Campaign, SystemMetric, APIUsage, WorkflowExecution, RevenueMetric, SecurityEvent
- ✅ **Auto-discovery** of all database tables
- ✅ **CRUD operations** with search & filtering

### Advanced Features
- ✅ **Real-time workflow dashboard** (`/workflow-dashboard`)
- ✅ **Workflow control APIs** (`/workflow/{id}/action`)
- ✅ **Revenue analytics** (`/revenue-analytics`)
- ✅ **Platform statistics** (`/stats`)
- ✅ **Health monitoring** (`/health`)

## 🚀 Quick Start

### Development Mode
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python bizosaas_sqladmin.py
```

### Docker Mode (When Docker Daemon Available)
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# Manual Docker build (alternative)
docker build -t bizosaas-sqladmin:latest .
docker run -p 3009:3009 -v ./data:/app/data bizosaas-sqladmin:latest
```

**Note**: Docker daemon not currently running in this environment. All Docker files are prepared and ready for use when Docker is available.

## 🔗 Access Points

- **Main Admin Interface**: http://localhost:3009/admin
- **Workflow Dashboard API**: http://localhost:3009/workflow-dashboard
- **Revenue Analytics API**: http://localhost:3009/revenue-analytics
- **Platform Statistics**: http://localhost:3009/stats
- **Health Check**: http://localhost:3009/health

## 🗃️ Database Models

### Core Platform
- **Tenant**: Multi-tenant organizations
- **User**: Platform users with role-based access
- **Campaign**: Marketing campaigns with performance metrics

### AI & Workflows
- **AIWorkflow**: AI agent configurations and status
- **WorkflowExecution**: Execution history and performance

### Analytics & Monitoring
- **SystemMetric**: Infrastructure performance metrics
- **APIUsage**: API usage tracking and rate limiting
- **RevenueMetric**: Financial tracking and subscription analytics
- **SecurityEvent**: Security monitoring and audit logs

## 🎛️ API Endpoints

### Workflow Management
```bash
# Get workflow dashboard data
GET /workflow-dashboard

# Control workflow execution
POST /workflow/{workflow_id}/action?action=start|pause|stop

# Platform statistics
GET /stats
```

### Analytics
```bash
# Revenue and subscription analytics
GET /revenue-analytics

# System health check
GET /health
```

## 🔧 Configuration

### Environment Variables
- `BIZOSAAS_DATABASE_URL`: Database connection (defaults to SQLite)
- `PYTHONPATH`: Python path configuration

### Database Connection
- **Primary**: PostgreSQL at `localhost:5433/bizosaas`
- **Fallback**: SQLite at `./bizosaas_admin.db` (auto-created)

## 📋 Migration Notes

**September 20, 2025**: ✅ **CONSOLIDATION COMPLETE** - Successfully migrated all BizOSaaS admin features from port 3011 into this SQLAlchemy Admin on port 3009.

### What Was Migrated:
- ✅ Comprehensive workflow management UI
- ✅ AI agent monitoring and control
- ✅ Multi-tenant analytics dashboard
- ✅ Revenue and subscription tracking
- ✅ Security event monitoring
- ✅ Real-time system health monitoring
- ✅ **500 Errors Fixed**: Resolved SQLAlchemy ModelView configuration issues
- ✅ **Bizoholic Digital Branding**: Updated logo and title
- ✅ **Docker Ready**: Complete containerization setup prepared

### Port 3011 Status: 
**DEPRECATED** - All features successfully migrated to port 3009

### Current Status:
- **Admin Interface**: ✅ Working at http://localhost:3009/admin
- **500 Errors**: ✅ Completely resolved
- **Database Models**: ✅ All 9 models functioning (Tenant, User, AIWorkflow, Campaign, SystemMetric, APIUsage, WorkflowExecution, RevenueMetric, SecurityEvent)
- **Containerization**: ✅ Docker files ready (requires Docker daemon)

## 🏗️ Architecture

```
🎯 CONSOLIDATED PLATFORM ADMINISTRATION (Port 3009)
┌─────────────────────────────────────┐
│   SQLAlchemy Admin + Bizoholic      │
│  ✅ Database Administration         │
│  ✅ Workflow Management             │
│  ✅ AI Agent Monitoring             │
│  ✅ Multi-tenant Analytics          │
│  ✅ Revenue & Subscription Tracking │
│  ✅ Security Event Monitoring       │
│  ✅ Real-time Dashboard APIs        │
└─────────────────────────────────────┘
```

## 🛡️ Security

- **Multi-tenant isolation**: Row-level security on all tenant-scoped tables
- **Security event logging**: Comprehensive audit trail
- **API rate limiting**: Built-in usage monitoring
- **Secure defaults**: Production-ready configuration

---

**Developed by**: Bizoholic Digital  
**Platform**: BizOSaaS Multi-tenant SaaS Platform  
**Last Updated**: September 20, 2025