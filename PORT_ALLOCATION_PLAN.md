# BizOSaaS Platform - Unified Port Allocation Plan

## 🔄 **INFRASTRUCTURE SERVICES (Keep Current)**
- **5432**: PostgreSQL Database (pgvector/pgvector:pg16) ✅
- **6379**: Redis Cache (redis:7-alpine) ✅  
- **9200/9300**: Elasticsearch (elasticsearch:7.16.2) ✅
- **8003**: Saleor E-commerce API (ghcr.io/saleor/saleor:latest) ✅
- **8088**: Apache Superset Analytics ✅
- **8081**: Temporal Web UI ✅
- **80/443/8080**: Traefik Gateway ✅
- **5000**: Docker Registry ✅

## 🎯 **FRONTEND APPLICATIONS** 
- **3006**: Client Portal (Next.js 15.5.3) - Multi-tenant dashboard
- **3008**: Bizoholic Frontend (Next.js 15.5.3) - Marketing website  
- **3009**: BizOSaaS Admin (Next.js 15.5.3) - Admin dashboard
- **3012**: CorelDove Frontend (Next.js 15.5.3) - E-commerce storefront

## 🚀 **CORE BACKEND SERVICES**
- **8001**: Brain AI Service (CrewAI orchestration + 40+ agents)
- **8007**: Authentication Service (FastAPI-Users v2)
- **8002**: Analytics Service (Performance + Business Intelligence)
- **8004**: Identity Service (User management + RBAC)
- **8005**: Wagtail CMS Service (Content management)
- **8006**: Integration Service (Third-party APIs)

## 💰 **BUSINESS LOGIC SERVICES** 
- **8010**: Billing Service (Stripe + usage tracking)
- **8011**: Subscription Management Service
- **8012**: Multi-Payment Gateway Service (Stripe, PayPal, Razorpay)
- **8013**: Revenue Analytics Service
- **8014**: Tax Compliance Service (Indian + International)

## 🤖 **AI & AUTOMATION SERVICES**
- **8020**: Automation Box Service (Workflow engine)
- **8021**: Progressive Activation Service (User onboarding)
- **8022**: Workflow Visualization Service (Real-time monitoring)
- **8023**: Vertical Intelligence Service (Industry-specific AI)
- **8024**: Performance Optimization Service
- **8025**: Platform Integration Service

## 🛠️ **OPERATIONAL SERVICES**
- **8030**: Webhook Management Service
- **8031**: Stripe Webhook Handler
- **8032**: Context Manager Service
- **8033**: Pricing Engine Service

## 🔧 **MICROSERVICES (From docker-compose.yml)**
- **3007**: Campaign Service (Marketing automation) - **MOVED FROM 3006**
- **3010**: Analytics Service (Alternative port)
- **3011**: Contact Service
- **3013**: Integration Service
- **3014**: LLM Gateway Service
- **3015**: Media Service
- **3016**: Site Builder Service
- **3017**: Subscription Service
- **3018**: Tenant Service
- **3019**: User Profile Service

## 📊 **SERVICE CATEGORIZATION BY DOMAIN**

### **Authentication & Identity (8007, 8004)**
- FastAPI-Users v2 authentication
- Role-based access control
- Session management

### **AI & Intelligence (8001, 8020-8025)**
- Brain AI orchestration
- CrewAI agent management
- Workflow automation
- Performance optimization

### **Commerce & Billing (8010-8014)**
- Payment processing
- Subscription management
- Revenue tracking
- Tax compliance

### **Content & CMS (8005, 8032)**
- Wagtail content management
- Media handling
- Content workflows

### **Integration & APIs (8006, 8030-8033)**
- Third-party integrations
- Webhook management
- API gateway functions

## 🔄 **PORT CONFLICT RESOLUTION**

### **Conflicts Resolved:**
- Campaign Service: **3006 → 3007** (Client Portal gets 3006)
- All stub services consolidated into full implementations
- No port conflicts with existing infrastructure

### **Reserved Ranges:**
- **3000-3099**: Frontend applications and user interfaces
- **8000-8039**: Backend services and APIs  
- **5000-5999**: Infrastructure services (DB, Cache, etc.)
- **9000-9999**: Analytics and monitoring services

## 🚀 **DEPLOYMENT PRIORITY ORDER**

### **Phase 1: Core Services (Week 1)**
1. **8001**: Brain AI Service (CrewAI + agents)
2. **8007**: Authentication Service 
3. **3007**: Campaign Service
4. **8010**: Billing Service

### **Phase 2: Business Logic (Week 2)** 
5. **8020**: Automation Box Service
6. **8021**: Progressive Activation Service
7. **8012**: Multi-Payment Gateway Service
8. **8022**: Workflow Visualization Service

### **Phase 3: Integration & Optimization (Week 3)**
9. **8006**: Integration Service
10. **8030**: Webhook Management Service
11. **8024**: Performance Optimization Service
12. **8025**: Platform Integration Service

### **Phase 4: Advanced Features (Week 4)**
13. **8013**: Revenue Analytics Service
14. **8023**: Vertical Intelligence Service
15. **8014**: Tax Compliance Service
16. **Remaining microservices** (ports 3010-3019)

## 📋 **SERVICE DEPENDENCIES**

### **High Priority Dependencies:**
- **8001 (Brain AI)** → Requires PostgreSQL, Redis
- **8007 (Auth)** → Requires PostgreSQL, Redis
- **8010 (Billing)** → Requires PostgreSQL, Stripe API
- **3007 (Campaign)** → Requires 8001 (Brain AI), 8007 (Auth)

### **Integration Dependencies:**
- **Frontend Apps (3006-3012)** → Require 8007 (Auth), 8001 (Brain AI)
- **Billing Services (8010-8014)** → Require 8007 (Auth), PostgreSQL
- **AI Services (8020-8025)** → Require 8001 (Brain AI), PostgreSQL

This allocation ensures no port conflicts, logical service grouping, and optimal deployment ordering based on dependencies.