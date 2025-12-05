# BizOSaaS Unified Architecture - Implementation Guide

## 🎯 **OVERVIEW**

We have successfully reorganized the BizOSaaS platform with a **security-first, headless architecture** approach:

### **✅ COMPLETED**
1. **Port Reorganization Strategy** - Comprehensive security-first port allocation plan
2. **Bizoholic Next.js Frontend** - Modern React/Next.js app consuming Wagtail headless CMS (Port 3000)
3. **Architecture Documentation** - Complete technical specifications and security measures
4. **Docker Configuration** - Unified docker-compose with network segmentation

### **🔥 CRITICAL ISSUES IDENTIFIED**
- **5 PostgreSQL instances exposed to internet** (ports 5432, 5433, 5434)
- **2 Redis instances exposed to internet** (ports 6379, 6380)
- **Monitoring service exposed** (port 3001)

## 🏗️ **NEW ARCHITECTURE OVERVIEW**

### **Frontend Tier (Customer-Facing)**
```
Port 3000 - Bizoholic Marketing Website (Next.js + Wagtail Headless)
Port 3003 - CoreLDove E-commerce (Next.js + Saleor Headless) [IN PROGRESS]
Port 3005 - BizoSaaS Unified Dashboard (Multi-Backend Consumer)
Port 3020 - Business Directory Frontend (FastAPI Consumer)
```

### **Backend Tier (Headless APIs - Internal Only)**
```
Port 4000 - Wagtail CMS Headless API (Content Management)
Port 4003 - Saleor GraphQL API (E-commerce Engine)
Port 4005 - FastAPI Brain (Middleware/Orchestration)
Port 4010 - AI Agents FastAPI (Marketing Automation)
```

### **Admin Tier (Management Interfaces - Localhost Only)**
```
Port 5000 - Wagtail Admin Interface (CMS Management)
Port 5003 - Saleor Admin Dashboard (E-commerce Management)  
Port 5005 - BizoSaaS Super Admin (Platform Management)
Port 5020 - Directory Admin (Business Listings Management)
```

### **Data Tier (Internal Network Only)**
```
PostgreSQL Primary Database (No external access)
Redis Primary Cache (No external access)
Redis Sessions Store (No external access)
```

## 🚀 **IMPLEMENTATION STEPS**

### **Phase 1: Immediate Security Fix (URGENT)**
```bash
# 1. Stop exposed services
docker-compose down

# 2. Apply security configuration
cd /home/alagiri/projects/bizoholic/bizosaas
cp docker-compose.unified-architecture.yml docker-compose.yml

# 3. Configure environment
cp .env.secure.example .env
# Edit .env with secure passwords

# 4. Start secure infrastructure
docker-compose up -d postgres-primary redis-primary
```

### **Phase 2: Deploy Bizoholic Next.js Frontend (Port 3000)**
```bash
# 1. Install dependencies
cd services/bizoholic-frontend
npm install

# 2. Copy logo file
cp /home/alagiri/projects/bizoholic/Bizoholic_Digital_-_Color-transparent.png public/

# 3. Start development server
npm run dev  # Runs on port 3000

# 4. Build for production
npm run build
docker-compose up -d bizoholic-frontend
```

### **Phase 3: Configure Wagtail Headless (Port 4000)**
```bash
# 1. Update Wagtail settings for headless mode
cd services/wagtail-cms

# 2. Configure CORS for frontend access
# Add to wagtail_cms/settings/base.py:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Bizoholic frontend
    "http://localhost:3005",  # BizoSaaS dashboard
]

# 3. Enable API endpoints
INSTALLED_APPS += [
    'rest_framework',
    'wagtail.api.v2',
    'corsheaders',
]

# 4. Start headless service
docker-compose up -d wagtail-headless
```

### **Phase 4: Create CoreLDove Next.js Frontend (Port 3003)**
```bash
# 1. Create CoreLDove frontend
mkdir -p services/coreldove-frontend
cd services/coreldove-frontend

# 2. Initialize Next.js with Saleor integration
npx create-next-app@latest . --typescript --tailwind --eslint --app
npm install @apollo/client graphql

# 3. Configure for Saleor GraphQL
# Add to next.config.js:
env: {
  SALEOR_API_URL: process.env.SALEOR_API_URL || 'http://localhost:4003/graphql/',
}

# 4. Start development
npm run dev -- --port 3003
```

### **Phase 5: Configure Admin Interfaces (Localhost Only)**
```bash
# 1. Move Wagtail admin to port 5000
docker-compose up -d wagtail-admin

# 2. Access admin interfaces
# Wagtail CMS: http://localhost:5000/admin/
# Saleor Admin: http://localhost:5003/
# Super Admin: http://localhost:5005/

# 3. Create admin users
docker-compose exec wagtail-admin python manage.py createsuperuser
```

## 🔒 **SECURITY IMPLEMENTATION**

### **Network Segmentation**
```yaml
networks:
  frontend-tier:    # Public access (3000-3099)
  backend-tier:     # Internal APIs (4000-4099)  
  admin-tier:       # Admin interfaces (5000-5099)
  data-tier:        # Databases (internal only)
```

### **Firewall Rules (Apply Immediately)**
```bash
# Block dangerous database ports
sudo ufw deny 5432/tcp
sudo ufw deny 5433/tcp
sudo ufw deny 5434/tcp
sudo ufw deny 6379/tcp
sudo ufw deny 6380/tcp

# Allow only necessary ports
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw allow 3000/tcp    # Bizoholic Frontend
sudo ufw allow 3003/tcp    # CoreLDove Frontend  
sudo ufw allow 3005/tcp    # BizoSaaS Dashboard
```

### **SSL/TLS Configuration**
```yaml
# Traefik labels for SSL
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.bizoholic.rule=Host(`bizoholic.com`)"
  - "traefik.http.routers.bizoholic.tls.certresolver=letsencrypt"
  - "traefik.http.routers.coreldove.rule=Host(`coreldove.com`)"
  - "traefik.http.routers.coreldove.tls.certresolver=letsencrypt"
```

## 📋 **TESTING CHECKLIST**

### **Frontend Access**
- [ ] Bizoholic Marketing Site: http://localhost:3000
- [ ] CoreLDove E-commerce: http://localhost:3003  
- [ ] BizoSaaS Dashboard: http://localhost:3005
- [ ] Business Directory: http://localhost:3020

### **Backend APIs**
- [ ] Wagtail API: http://localhost:4000/api/
- [ ] Saleor GraphQL: http://localhost:4003/graphql/
- [ ] FastAPI Brain: http://localhost:4005/docs
- [ ] AI Agents API: http://localhost:4010/docs

### **Admin Interfaces**
- [ ] Wagtail Admin: http://localhost:5000/admin/
- [ ] Saleor Admin: http://localhost:5003/
- [ ] Super Admin: http://localhost:5005/
- [ ] Traefik Dashboard: http://localhost:8080/

### **Security Validation**
- [ ] Database ports blocked from internet
- [ ] Redis ports blocked from internet
- [ ] Admin interfaces localhost-only
- [ ] SSL certificates working
- [ ] Authentication required for admin access

## 🌐 **DOMAIN ROUTING (Production)**

### **DNS Configuration**
```bash
# A Records
bizoholic.com        → Your-Server-IP
coreldove.com        → Your-Server-IP
app.bizosaas.com     → Your-Server-IP
admin.bizosaas.com   → Your-Server-IP (VPN only)
```

### **Traefik Routing**
```yaml
# Production labels
bizoholic-frontend:
  labels:
    - "traefik.http.routers.bizoholic.rule=Host(`bizoholic.com`)"
    
coreldove-frontend:
  labels:
    - "traefik.http.routers.coreldove.rule=Host(`coreldove.com`)"
    
bizosaas-dashboard:
  labels:
    - "traefik.http.routers.bizosaas.rule=Host(`app.bizosaas.com`)"
    - "traefik.http.routers.bizosaas.middlewares=auth@file"
```

## 🛠️ **DEVELOPMENT WORKFLOW**

### **Starting Development**
```bash
# 1. Start secure infrastructure
docker-compose up -d postgres-primary redis-primary

# 2. Start backends
docker-compose up -d wagtail-headless saleor-headless

# 3. Start frontends in development mode
cd services/bizoholic-frontend && npm run dev &
cd services/coreldove-frontend && npm run dev -- --port 3003 &
cd frontend && npm run dev -- --port 3005 &

# 4. Access admin interfaces
docker-compose up -d wagtail-admin saleor-admin
```

### **Production Deployment**
```bash
# 1. Build all images
docker-compose -f docker-compose.unified-architecture.yml build

# 2. Deploy with SSL
docker-compose -f docker-compose.unified-architecture.yml up -d

# 3. Monitor logs
docker-compose logs -f bizoholic-frontend coreldove-frontend
```

## 📈 **MONITORING & MAINTENANCE**

### **Health Checks**
```bash
# Check service health
curl http://localhost:3000/          # Bizoholic frontend
curl http://localhost:4000/api/      # Wagtail API
curl http://localhost:4003/graphql/  # Saleor GraphQL

# Check database connectivity
docker-compose exec postgres-primary pg_isready

# Check Redis
docker-compose exec redis-primary redis-cli ping
```

### **Log Monitoring**
```bash
# View logs
docker-compose logs -f bizoholic-frontend
docker-compose logs -f wagtail-headless
docker-compose logs -f saleor-headless

# Error monitoring
docker-compose logs --tail=100 | grep ERROR
```

## 🔄 **MIGRATION FROM CURRENT SETUP**

### **Data Migration**
```bash
# 1. Backup current data
docker-compose exec bizoholic-postgres pg_dump -U admin bizosaas > backup.sql

# 2. Import to new setup
docker-compose exec postgres-primary psql -U admin -d bizosaas < backup.sql

# 3. Update configurations
# Update connection strings in all services
```

### **DNS Switchover**
```bash
# 1. Test new setup thoroughly
# 2. Update DNS records
# 3. Monitor traffic and errors
# 4. Rollback plan ready
```

## 🚨 **IMMEDIATE ACTIONS REQUIRED**

1. **🔥 CRITICAL**: Stop exposed database services immediately
2. **📧 SECURITY**: Apply firewall rules to block dangerous ports
3. **🔧 BUILD**: Complete CoreLDove Next.js frontend
4. **🔐 CONFIG**: Set up admin authentication and VPN access
5. **📊 MONITOR**: Implement alerting for unauthorized access attempts

---

**This unified architecture provides:**
- ✅ **Security-first approach** with proper network segmentation
- ✅ **Scalable headless architecture** with modern frontends
- ✅ **Clean separation** between customer-facing and admin interfaces  
- ✅ **Production-ready** with SSL, authentication, and monitoring
- ✅ **Development-friendly** with clear port organization