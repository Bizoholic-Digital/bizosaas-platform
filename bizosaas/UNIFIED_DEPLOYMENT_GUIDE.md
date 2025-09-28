# BizOSaaS Platform - Unified Deployment Guide

## 🚀 **UNIFIED STACK OVERVIEW**

The BizOSaaS platform has been consolidated into a single, production-ready Docker Compose stack with proper port allocation and TailAdmin v2 integration.

---

## 📋 **CORRECT PORT ALLOCATION**

| Port | Service | Description | Technology |
|------|---------|-------------|------------|
| **3000** | **BizOSaaS Admin Dashboard** | TailAdmin v2 + Apache Superset Analytics | `misc/services/frontend-nextjs` |
| **3001** | **Bizoholic Marketing Frontend** | Digital Marketing Platform | `misc/services/bizoholic-frontend` |
| **3002** | **CoreLDove E-commerce Frontend** | AI-Powered E-commerce Storefront | `ecommerce/services/coreldove-frontend` |
| **8001** | **FastAPI Brain Gateway** | AI API Gateway & Orchestration | `ai/services/bizosaas-brain` |
| **8007** | **Auth Service v2** | Unified Authentication System | `core/services/auth-service-v2` |
| **8082** | **Wagtail CMS** | Headless CMS for Marketing Content | `core/services/wagtail-cms` |
| **8010** | **Saleor Backend** | E-commerce GraphQL API | Official Saleor Docker Image |
| **8088** | **Apache Superset** | Analytics & Business Intelligence | `analytics/services/apache-superset` |
| **5000** | **SQL Admin Dashboard** | Database Management (SuperAdmin) | `core/services/sqladmin-dashboard` |
| **5432** | **PostgreSQL** | Primary Database with pgvector | `ankane/pgvector:v0.5.1` |
| **6379** | **Redis** | Cache & Session Storage | `redis:7-alpine` |
| **8080** | **Traefik Dashboard** | Reverse Proxy Management | `traefik:v3.0` |

---

## 🏗️ **LOCAL DEVELOPMENT SETUP**

### **1. Prerequisites**
```bash
# Ensure Docker and docker-compose are installed
docker --version
docker-compose --version

# Clone the repository (if not already done)
git clone <repository-url>
cd bizosaas-platform
```

### **2. Environment Configuration**
```bash
# Copy and configure environment variables
cp .env.unified.example .env

# Edit .env file with your API keys
nano .env
```

### **3. Start the Platform**
```bash
# Start the entire platform
./start-bizosaas-unified.sh

# Monitor logs
docker-compose -f docker-compose.unified.yml logs -f

# Check container status
docker-compose -f docker-compose.unified.yml ps
```

### **4. Stop the Platform**
```bash
# Stop all services
./stop-bizosaas-unified.sh

# Stop and remove all data (if needed)
docker-compose -f docker-compose.unified.yml down -v
```

---

## 🌐 **FRONTEND ACCESS & AUTHENTICATION FLOW**

### **Authentication Flow**
1. **Visit**: `http://localhost:3000` (BizOSaaS Admin)
2. **Login**: Use credentials to authenticate via Auth Service v2
3. **Dashboard**: Redirected to TailAdmin v2 dashboard with Apache Superset analytics
4. **Navigation**: Access other platforms via platform tabs

### **Platform Navigation**
- **BizOSaaS Admin**: `http://localhost:3000` (Login → TailAdmin v2 Dashboard)
- **Bizoholic Marketing**: `http://localhost:3001` (Marketing Website)
- **CoreLDove E-commerce**: `http://localhost:3002` (E-commerce Storefront)

### **Role-Based Access Control**
```
SuperAdmin (Global Access):
├── BizOSaaS Admin Dashboard (Port 3000) ✓
├── Bizoholic Marketing (Port 3001) ✓  
├── CoreLDove E-commerce (Port 3002) ✓
└── SQL Admin Dashboard (Port 5000) ✓

TenantAdmin (Business Access):  
├── BizOSaaS Admin Dashboard (Port 3000) ✓
├── Bizoholic Marketing (Port 3001) ✓
├── CoreLDove E-commerce (Port 3002) ✓
└── SQL Admin Dashboard (Port 5000) ❌

Manager (Platform Access):
├── Bizoholic Marketing (Port 3001) ✓
├── CoreLDove E-commerce (Port 3002) ✓
├── BizOSaaS Admin Dashboard (Port 3000) ❌
└── SQL Admin Dashboard (Port 5000) ❌
```

---

## 🐳 **CONTAINER STRUCTURE**

### **Infrastructure Services**
- **postgres**: Multi-database setup (bizosaas, wagtail, saleor)
- **redis**: Centralized cache and session storage
- **traefik**: Reverse proxy with SSL termination

### **Backend Services**
- **bizosaas-brain**: FastAPI gateway connecting all services
- **auth-service-v2**: FastAPI-Users v2 authentication system
- **wagtail-cms**: Django CMS for marketing content
- **saleor-backend**: GraphQL e-commerce API
- **apache-superset**: Analytics and business intelligence
- **sqladmin-dashboard**: PostgreSQL administration

### **Frontend Services**
- **bizosaas-admin**: NextJS TailAdmin v2 with real-time features
- **bizoholic-marketing**: NextJS marketing website consuming Wagtail
- **coreldove-ecommerce**: NextJS storefront consuming Saleor GraphQL

---

## 📊 **TAILADMIN V2 INTEGRATION**

### **Dashboard Features**
- ✅ **Real-time Metrics**: Live updates via WebSocket
- ✅ **Apache Superset Integration**: Embedded analytics dashboards
- ✅ **AI Agent Monitoring**: 88 AI agents status and performance
- ✅ **Platform Navigation Tabs**: Cross-platform access with status indicators
- ✅ **Role-Based UI**: Dynamic interface based on user permissions
- ✅ **Quick Actions**: Context-aware administrative functions

### **TailAdmin v2 Location**
```
Source: /misc/services/frontend-nextjs/
Docker: bizosaas-admin container on port 3000
Features: Complete TailAdmin v2 implementation with:
├── Real-time dashboard components
├── Apache Superset embedded analytics
├── AI agent monitoring system
├── Multi-platform navigation
└── WebSocket-based live updates
```

---

## 🚀 **PRODUCTION DEPLOYMENT (Dokploy)**

### **1. VPS Preparation**
```bash
# On your VPS server
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER
sudo systemctl enable docker
sudo systemctl start docker
```

### **2. Deploy to Dokploy**
```bash
# Push to repository
git add .
git commit -m "feat: unified stack deployment ready"
git push origin main

# In Dokploy dashboard:
1. Create new application
2. Connect to Git repository
3. Set environment variables from .env.unified.example
4. Use docker-compose.unified.yml as deployment file
5. Deploy
```

### **3. Production Environment Variables**
```bash
# Critical production changes in .env
JWT_SECRET=your-super-secure-jwt-secret-here
ADMIN_SECRET=your-super-admin-secret-here
POSTGRES_PASSWORD=your-secure-db-password-here

# SSL Configuration (via Traefik)
DOMAIN=yourdomain.com
EMAIL=admin@yourdomain.com
```

### **4. Domain Configuration**
```nginx
# DNS Configuration
admin.yourdomain.com     → Port 3000 (BizOSaaS Admin)
bizoholic.yourdomain.com → Port 3001 (Marketing)
coreldove.yourdomain.com → Port 3002 (E-commerce)
api.yourdomain.com       → Port 8001 (API Gateway)
```

---

## 🔧 **TROUBLESHOOTING**

### **Common Issues**
```bash
# Port conflicts
sudo lsof -i :3000
sudo lsof -i :3001
sudo lsof -i :3002

# Container logs
docker-compose -f docker-compose.unified.yml logs bizosaas-admin
docker-compose -f docker-compose.unified.yml logs bizoholic-marketing
docker-compose -f docker-compose.unified.yml logs coreldove-ecommerce

# Database connectivity
docker exec -it bizosaas-postgres psql -U admin -d bizosaas
docker exec -it bizosaas-redis redis-cli ping

# Network issues
docker network ls | grep bizosaas
docker network inspect bizosaas-network
```

### **Health Checks**
```bash
# Service health endpoints
curl http://localhost:8001/health  # Brain API
curl http://localhost:8007/health  # Auth Service
curl http://localhost:3000/api/health  # Admin Dashboard

# Container status
docker-compose -f docker-compose.unified.yml ps
```

---

## ✅ **SUCCESS VERIFICATION**

### **Local Development**
1. ✅ All containers start without errors
2. ✅ Login at `localhost:3000` works
3. ✅ TailAdmin v2 dashboard loads with analytics
4. ✅ Platform navigation tabs show correct statuses
5. ✅ Cross-platform authentication works
6. ✅ Apache Superset analytics are accessible

### **Production Deployment**
1. ✅ All services are accessible via domains
2. ✅ SSL certificates are properly configured
3. ✅ Database connections are secure
4. ✅ Authentication flow works across platforms
5. ✅ Real-time features are functioning
6. ✅ Analytics dashboards load properly

---

## 📁 **KEY FILES CHANGED**

### **Docker Configuration**
- `docker-compose.unified.yml` - Main production stack
- `start-bizosaas-unified.sh` - Unified startup script
- `stop-bizosaas-unified.sh` - Unified stop script
- `.env.unified.example` - Environment template

### **Dockerfiles Updated**
- `misc/services/frontend-nextjs/Dockerfile` - Port 3000 (TailAdmin v2)
- `misc/services/bizoholic-frontend/Dockerfile` - Port 3001
- `ecommerce/services/coreldove-frontend/Dockerfile` - Port 3002

### **Database Configuration**
- `infrastructure/database/create-multiple-dbs.sh` - Multi-database setup

---

## 🎉 **FINAL RESULT**

**✅ Unified Production-Ready Stack**
- Single Docker Compose configuration
- Correct port allocation per PRD
- Existing TailAdmin v2 integration
- Apache Superset analytics
- Role-based access control
- Cross-platform authentication
- Ready for local testing and Dokploy deployment

**🔄 Complete Flow:**
1. **Port 3000**: Login → TailAdmin v2 Dashboard (Apache Superset analytics)
2. **Port 3001**: Bizoholic Marketing (Wagtail CMS content)  
3. **Port 3002**: CoreLDove E-commerce (Saleor GraphQL)
4. **All platforms**: Unified auth via FastAPI Brain Gateway (Port 8001)

**🚀 Ready for deployment to Dokploy production environment!**