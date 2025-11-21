# Unified Frontend & Backend Architecture - Port Organization

## Current Architecture Issues

### Problems with Current Setup
1. **Static Bizoholic Website** on port 3000 - Should be Next.js consuming Wagtail headless
2. **Missing CoreLDove Frontend** - Should be on port 3003 consuming Saleor headless
3. **Wagtail Dual Ports** - Running on both 8006 and 8007, should be single headless backend
4. **Saleor Backend** - Running on 8020, should be properly positioned in backend tier

## 🎯 **NEW UNIFIED ARCHITECTURE**

### **FRONTEND TIER** (Customer-Facing UIs)
```
Port 3000 - Bizoholic Next.js Frontend (Headless Wagtail Consumer)
Port 3003 - CoreLDove Next.js Frontend (Headless Saleor Consumer) 
Port 3005 - BizoSaaS Unified Dashboard (Multi-Backend Consumer)
Port 3020 - Business Directory Frontend (FastAPI Consumer)
```

### **BACKEND TIER** (Headless APIs)
```
Port 4000 - Wagtail CMS Headless API (Content Management)
Port 4003 - Saleor GraphQL API (E-commerce Engine)
Port 4005 - Business Directory FastAPI (Directory Services)
Port 4010 - AI Agents FastAPI (Marketing Automation)
```

### **ADMIN TIER** (Management Interfaces)
```
Port 5000 - Wagtail Admin Interface (CMS Management)
Port 5003 - Saleor Admin Dashboard (E-commerce Management)
Port 5005 - BizoSaaS Super Admin (Platform Management)
Port 5020 - Directory Admin (Business Listings Management)
```

### **DATA TIER** (Internal Only - No External Access)
```
Port 5432 - PostgreSQL Primary Database
Port 5433 - PostgreSQL Secondary Database
Port 6379 - Redis Primary Cache
Port 6380 - Redis Sessions Store
```

## 🏗️ **DETAILED SERVICE ARCHITECTURE**

### **Bizoholic Marketing Platform**
```yaml
# Frontend: Next.js consuming headless Wagtail
bizoholic-frontend:
  port: 3000
  framework: Next.js 14
  backend: Wagtail Headless API (port 4000)
  domain: bizoholic.com
  features:
    - Marketing pages from Wagtail CMS
    - SEO-optimized content delivery
    - Lead capture forms
    - Service pages with dynamic content
    - Blog and case studies

# Backend: Wagtail Headless CMS
wagtail-headless:
  port: 4000
  framework: Django + Wagtail
  database: PostgreSQL (port 5432)
  cache: Redis (port 6379)
  api: REST + GraphQL
  features:
    - Page content management
    - Media library
    - SEO metadata
    - Form submissions
    - Multi-tenant content

# Admin: Wagtail Admin Interface  
wagtail-admin:
  port: 5000
  access: admin.bizoholic.com
  authentication: Required
  features:
    - Content editing
    - Media management
    - User permissions
    - Site settings
```

### **CoreLDove E-commerce Platform**
```yaml
# Frontend: Next.js consuming headless Saleor
coreldove-frontend:
  port: 3003
  framework: Next.js 14 + TailwindCSS
  backend: Saleor GraphQL API (port 4003)
  domain: coreldove.com
  features:
    - Product catalog
    - Shopping cart & checkout
    - User accounts
    - Order management
    - Payment processing

# Backend: Saleor Headless E-commerce
saleor-headless:
  port: 4003
  framework: Python + GraphQL
  database: PostgreSQL (port 5432)
  cache: Redis (port 6379)
  api: GraphQL
  features:
    - Product management
    - Inventory tracking
    - Order processing
    - Payment integration
    - Multi-channel support

# Admin: Saleor Admin Dashboard
saleor-admin:
  port: 5003
  access: admin.coreldove.com  
  authentication: Required
  features:
    - Product management
    - Order processing
    - Customer management
    - Analytics dashboard
```

### **BizoSaaS Unified Platform**
```yaml
# Frontend: Unified Next.js Dashboard
bizosaas-frontend:
  port: 3005
  framework: Next.js 14 + ShadCN UI
  backends:
    - Wagtail API (port 4000)
    - Saleor API (port 4003)
    - Directory API (port 4005)
    - AI Agents API (port 4010)
  domain: app.bizosaas.com
  features:
    - Cross-platform management
    - Unified authentication
    - Analytics dashboard
    - AI agent orchestration

# Backend: FastAPI Brain (Middleware)
fastapi-brain:
  port: 4005
  framework: FastAPI
  database: PostgreSQL (port 5432)
  cache: Redis (port 6379)
  features:
    - API orchestration
    - Authentication service
    - Data aggregation
    - Workflow automation
```

## 🔧 **IMPLEMENTATION PLAN**

### **Phase 1: Frontend Restructuring**

#### 1.1 Migrate Bizoholic to Next.js (Port 3000)
```bash
# Create new Next.js frontend for Bizoholic
cd /home/alagiri/projects/bizoholic/bizosaas/services/
mkdir bizoholic-frontend
cd bizoholic-frontend

# Initialize Next.js project
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"

# Configure to consume Wagtail headless API
```

#### 1.2 Create CoreLDove Next.js Frontend (Port 3003)
```bash
# Create CoreLDove frontend
mkdir coreldove-frontend
cd coreldove-frontend

# Initialize with Saleor integration
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir
npm install @apollo/client graphql
```

#### 1.3 Update BizoSaaS Frontend (Port 3005) 
- Already exists, enhance for multi-backend consumption

### **Phase 2: Backend API Restructuring**

#### 2.1 Wagtail Headless Configuration (Port 4000)
```python
# wagtail_cms/settings/headless.py
WAGTAIL_HEADLESS_PREVIEW = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Bizoholic frontend
    "http://localhost:3005",  # BizoSaaS dashboard
]

# Enable REST Framework and GraphQL
INSTALLED_APPS += [
    'rest_framework',
    'wagtail.api.v2',
    'corsheaders',
]

# API endpoints
WAGTAIL_API_BASE_URL = 'http://localhost:4000/api/'
```

#### 2.2 Saleor Headless Configuration (Port 4003)  
```python
# Move from port 8020 to 4003
# Configure CORS for CoreLDove frontend
ALLOWED_GRAPHQL_ORIGINS = [
    "http://localhost:3003",  # CoreLDove frontend
    "http://localhost:3005",  # BizoSaaS dashboard
]
```

### **Phase 3: Admin Interface Consolidation**

#### 3.1 Admin Ports Standardization
```yaml
# docker-compose.admin.yml
services:
  wagtail-admin:
    ports:
      - "127.0.0.1:5000:8000"
      
  saleor-admin:
    ports:
      - "127.0.0.1:5003:9000"
      
  bizosaas-admin:
    ports:
      - "127.0.0.1:5005:3000"
```

### **Phase 4: Security & Access Control**

#### 4.1 Network Segmentation
```yaml
# docker-compose.networks.yml
networks:
  frontend-tier:
    driver: bridge
    # Ports 3000-3099
    
  backend-tier:
    driver: bridge
    internal: true
    # Ports 4000-4099
    
  admin-tier:
    driver: bridge
    internal: true
    # Ports 5000-5099
    
  data-tier:
    driver: bridge
    internal: true
    # Ports 5432, 6379, etc.
```

## 🌐 **DOMAIN ROUTING STRATEGY**

### **Production Domains**
```nginx
# Public Customer-Facing
bizoholic.com          → Port 3000 (Bizoholic Next.js)
coreldove.com          → Port 3003 (CoreLDove Next.js)
app.bizosaas.com       → Port 3005 (BizoSaaS Dashboard)
directory.bizosaas.com → Port 3020 (Directory Frontend)

# API Endpoints  
api.bizoholic.com      → Port 4000 (Wagtail API)
api.coreldove.com      → Port 4003 (Saleor GraphQL)
api.bizosaas.com       → Port 4005 (FastAPI Brain)

# Admin Interfaces (VPN/Auth Required)
admin.bizoholic.com    → Port 5000 (Wagtail Admin)
admin.coreldove.com    → Port 5003 (Saleor Admin)
admin.bizosaas.com     → Port 5005 (Super Admin)
```

### **Development Domains (localhost)**
```
localhost:3000 → Bizoholic Frontend
localhost:3003 → CoreLDove Frontend  
localhost:3005 → BizoSaaS Dashboard
localhost:4000 → Wagtail API
localhost:4003 → Saleor GraphQL
localhost:5000 → Wagtail Admin
localhost:5003 → Saleor Admin
```

## 📋 **MIGRATION CHECKLIST**

### **Frontend Migration**
- [ ] Create Bizoholic Next.js app (port 3000)
- [ ] Create CoreLDove Next.js app (port 3003)
- [ ] Configure Wagtail headless API consumption
- [ ] Configure Saleor GraphQL integration
- [ ] Set up unified authentication
- [ ] Implement shared UI components

### **Backend Restructuring** 
- [ ] Move Wagtail to port 4000 (headless mode)
- [ ] Move Saleor to port 4003
- [ ] Configure CORS for new frontends
- [ ] Set up API authentication
- [ ] Enable GraphQL endpoints

### **Admin Consolidation**
- [ ] Move Wagtail admin to port 5000
- [ ] Move Saleor admin to port 5003
- [ ] Implement unified admin access
- [ ] Set up admin authentication

### **Security Implementation**
- [ ] Block direct database access
- [ ] Implement network segmentation
- [ ] Configure SSL certificates
- [ ] Set up VPN access for admin

## 🚀 **NEXT STEPS**

1. **Start with Bizoholic Frontend** - Create Next.js app consuming Wagtail
2. **Configure Wagtail Headless** - Enable API endpoints and CORS
3. **Create CoreLDove Frontend** - Next.js app consuming Saleor
4. **Implement Security Fixes** - Block database exposure immediately
5. **Set up Domain Routing** - Traefik configuration with SSL

This architecture provides:
- ✅ **Clean separation** between frontend and backend
- ✅ **Scalable headless architecture** 
- ✅ **Unified admin experience**
- ✅ **Security-first approach**
- ✅ **Domain-based routing**