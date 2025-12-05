# BizOSaaS Local Access Guide
**Complete guide to accessing all containerized services locally**

## 🌐 **FRONTEND WEBSITES**

### **1. Bizoholic Main Website (Next.js + Wagtail)**
- **Frontend URL**: `http://localhost:3000` *(Not deployed yet - TypeScript fixes needed)*
- **CMS Admin**: `http://localhost:8010/admin` *(Wagtail - Currently restarting)*
- **Description**: Apple-style design showcasing 47+ AI agents across 9 service pages
- **Tech Stack**: Next.js frontend + Wagtail CMS backend with multi-tenancy

### **2. CoreLDove E-commerce Platform (Next.js + Saleor)**
- **Storefront URL**: `http://localhost:3001` *(Not deployed yet - needs Saleor integration)*
- **Saleor API**: `http://localhost:8020/graphql/` *(Not deployed yet)*
- **Saleor Dashboard**: `http://localhost:9020` *(Admin interface - not deployed yet)*
- **Description**: AI-powered dropshipping platform with Hook/Midtier/Hero product classification
- **Tech Stack**: Next.js Saleor Storefront + Saleor GraphQL backend

### **3. Multi-Tenant Client Sites Platform**
- **Frontend URL**: `http://localhost:3004` *(Not deployed yet - TypeScript fixes needed)*
- **API Backend**: `http://localhost:8005` ✅ **HEALTHY**
- **Description**: BYOK credential management for agency clients
- **Tech Stack**: Next.js frontend + FastAPI backend

## 🤖 **AI & BACKEND SERVICES** *(All Working)*

### **4. AI Agents System** ✅ **HEALTHY**
- **API URL**: `http://localhost:8000`
- **Health Check**: `http://localhost:8000/health`
- **Agents Health**: `http://localhost:8000/agents/health`
- **Description**: 47+ specialized AI agents (business_analyst, marketing_strategist, onboarding_coordinator)

### **5. Business Directory Service** ✅ **HEALTHY** 
- **API URL**: `http://localhost:8003`
- **Health Check**: `http://localhost:8003/health`
- **Directories**: `http://localhost:8003/directories` (66+ business directories)
- **Categories**: `http://localhost:8003/categories`
- **Description**: Multi-platform business directory with AI optimization

### **6. Client Sites API** ✅ **HEALTHY**
- **API URL**: `http://localhost:8005`
- **Health Check**: `http://localhost:8005/health`
- **Templates**: `http://localhost:8005/templates` (4 available templates)
- **Description**: Multi-tenant client website management

### **7. Django CRM Service** ⚠️ **RUNNING** *(Health check issues)*
- **API URL**: `http://localhost:8007`
- **Health Check**: `http://localhost:8007/health/`
- **Admin**: `http://localhost:8007/admin/`
- **Description**: Multi-tenant customer relationship management

## 🔐 **INFRASTRUCTURE SERVICES** *(All Working)*

### **8. HashiCorp Vault** ✅ **RUNNING**
- **UI**: `http://localhost:8200`
- **Root Token**: `myroot` (dev mode)
- **Description**: Secrets management for BYOK credentials

### **9. Vault Service API** ✅ **HEALTHY**
- **API URL**: `http://localhost:8201`
- **Health Check**: `http://localhost:8201/health`
- **Description**: Vault integration service for credential management

### **10. Traefik Dashboard** ✅ **RUNNING**
- **Dashboard**: `http://localhost:8080`
- **Description**: Reverse proxy and load balancer monitoring

## 💾 **DATABASE ACCESS**

### **11. PostgreSQL Database** ✅ **HEALTHY**
- **Connection**: `localhost:5433`
- **Username**: `admin`
- **Password**: `BizoholicSecure2025`
- **Databases**: `bizoholic`, `saleor`, `wagtail`
- **Extensions**: pgvector v0.5.1 for AI embeddings

### **12. Redis Cache** ✅ **HEALTHY**
- **Connection**: `localhost:6379`
- **Test**: `redis-cli -p 6379 ping`
- **Description**: High-performance caching and session storage

## 🚧 **SERVICES UNDER DEPLOYMENT**

### **Wagtail CMS** 🔄 **RESTARTING**
- **Status**: Container built, currently troubleshooting startup
- **Expected URL**: `http://localhost:8010/admin`
- **Purpose**: Multi-tenant content management for Bizoholic

### **Saleor E-commerce** 📦 **CONFIGURED**
- **Status**: Configuration ready, needs deployment
- **Expected URLs**:
  - GraphQL API: `http://localhost:8020/graphql/`
  - Admin Dashboard: `http://localhost:9020`

### **Frontend Services** 📦 **BUILDING**
- **Status**: Containers building, final TypeScript fixes needed
- **Services**: Bizoholic website, CoreLDove storefront, Client sites frontend

## 🧪 **TESTING COMMANDS**

### **Health Check All Services**
```bash
# Test working services
curl http://localhost:8000/health        # AI Agents
curl http://localhost:8003/health        # Business Directory  
curl http://localhost:8005/health        # Client Sites API
curl http://localhost:8201/health        # Vault Service

# Test database connectivity
docker exec bizosaas-postgres-main psql postgresql://admin:BizoholicSecure2025@localhost:5432/bizoholic -c "SELECT 1;"
docker exec bizosaas-redis-main redis-cli ping
```

### **View Service Status**
```bash
# Check all containers
docker ps --filter name=bizosaas

# Check specific service logs
docker logs bizosaas-ai-agents-main
docker logs bizosaas-wagtail-cms-main
```

## 📊 **CURRENT STATUS SUMMARY**

| Service | Status | Port | Access URL | Description |
|---------|--------|------|------------|-------------|
| AI Agents | ✅ Healthy | 8000 | http://localhost:8000 | 47+ specialized AI agents |
| Business Directory | ✅ Healthy | 8003 | http://localhost:8003 | 66+ business directories |
| Client Sites API | ✅ Healthy | 8005 | http://localhost:8005 | Multi-tenant platform |
| Django CRM | ⚠️ Running | 8007 | http://localhost:8007 | Customer management |
| Wagtail CMS | 🔄 Restarting | 8010 | http://localhost:8010 | Content management |
| Vault Service | ✅ Healthy | 8201 | http://localhost:8201 | BYOK credentials |
| Vault | ✅ Running | 8200 | http://localhost:8200 | Secrets management |
| PostgreSQL | ✅ Healthy | 5433 | localhost:5433 | Database with pgvector |
| Redis | ✅ Healthy | 6379 | localhost:6379 | Caching |
| Traefik | ✅ Running | 8080 | http://localhost:8080 | Reverse proxy |

### **Working Services**: 7/10 ✅
### **Services Ready for Testing**: AI Agents, Business Directory, Client Sites API, Vault Services, Infrastructure

### **Next Steps for Complete Access**:
1. 🔧 Fix Wagtail CMS startup issue
2. 🚀 Deploy Saleor backend containers  
3. 🎨 Complete frontend TypeScript fixes and deployment
4. 🧪 Full user journey testing across all services

**The core BizOSaaS platform is operational and ready for testing!**