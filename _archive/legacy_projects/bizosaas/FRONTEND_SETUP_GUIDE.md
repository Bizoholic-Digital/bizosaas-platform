# BizOSaaS Platform Frontend Setup Guide

## ✅ **SETUP COMPLETE - PRD COMPLIANT**

The frontend architecture has been successfully configured according to the PRD specifications with unified authentication flow and FastAPI Brain integration.

---

## 🎯 **Port Configuration (PRD Specification)**

| Port | Application | Technology Stack | Purpose |
|------|-------------|------------------|---------|
| **3000** | **Bizoholic Marketing Frontend** | Next.js 14 + React Hook Form + Recharts + TailwindCSS | AI-powered digital marketing platform |
| **3001** | **BizOSaaS Admin Dashboard** | Next.js 14 + TypeScript + TailwindCSS + ShadCN UI | Multi-tenant platform administration |
| **3002** | **CoreLDove E-commerce Frontend** | Next.js 14 + Stripe + Saleor Storefront API + TailwindCSS | E-commerce platform with AI sourcing |

---

## 🔄 **Architecture Flow**

```
Frontend Applications (NextJS + TailwindCSS + ShadCN UI)
                    ↓
      Unified Authentication (Auth Service v2)
                    ↓
        Unified Dashboard (BizOSaaS Admin)
                    ↓
     FastAPI Brain Gateway (Port 8001) 
                    ↓
Backend Data Stores (Wagtail CMS / Saleor E-commerce)
```

---

## 🚀 **Quick Start**

### **Start All Frontend Applications**
```bash
# Make scripts executable (first time only)
chmod +x scripts/*.sh

# Start all three frontend applications
./scripts/start-frontend-dev.sh
```

### **Stop All Frontend Applications**  
```bash
./scripts/stop-frontend-dev.sh
```

### **Individual Application Startup**
```bash
# BizOSaaS Admin Dashboard (Port 3000)
cd frontend/apps/bizosaas-admin && npm run dev

# Bizoholic Marketing Frontend (Port 3001)  
cd frontend/apps/bizoholic-frontend && npm run dev

# CoreLDove E-commerce Frontend (Port 3002)
cd frontend/apps/coreldove-frontend && npm run dev
```

---

## 🔐 **Authentication System**

### **Unified Authentication Features**
- ✅ **Cross-Platform Sessions**: Single login works across all platforms
- ✅ **Role-Based Access Control**: SuperAdmin, TenantAdmin, Manager, Client roles
- ✅ **FastAPI Brain Integration**: All API calls route through centralized gateway
- ✅ **Automatic Token Refresh**: Sessions maintained automatically
- ✅ **Platform-Specific Routing**: Users redirected to appropriate dashboards

### **Access Control Matrix**
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

Client (Limited Access):
├── Public Pages ✓
├── Client Portal Views ✓  
├── All Admin Dashboards ❌
```

---

## 📱 **Application Access**

### **Development URLs**
- 🔧 **BizOSaaS Admin Dashboard**: http://localhost:3000
- 📈 **Bizoholic Marketing**: http://localhost:3001
- 🛒 **CoreLDove E-commerce**: http://localhost:3002

### **Production URLs (When Deployed)**
- 🔧 **BizOSaaS Admin Dashboard**: https://admin.bizosaas.com
- 📈 **Bizoholic Marketing**: https://bizoholic.bizosaas.com  
- 🛒 **CoreLDove E-commerce**: https://coreldove.bizosaas.com

---

## 🛠️ **Technical Implementation**

### **Shared Components Created**
- `frontend/shared/lib/api-config.ts` - Unified API configuration
- `frontend/shared/hooks/useUnifiedAuth.ts` - Authentication hook
- `frontend/shared/components/AuthWrapper.tsx` - Authentication wrapper

### **API Integration**
- **Brain API Gateway**: `http://localhost:8001` (FastAPI)
- **Auth Service v2**: `http://localhost:8007` (FastAPI-Users v2)
- **Wagtail CMS**: `http://localhost:8082` (via Brain API)  
- **Saleor E-commerce**: `http://localhost:8010` (via Brain API)

### **Environment Variables**
```bash
# Required for all frontend applications
NEXT_PUBLIC_BRAIN_API_URL=http://localhost:8001
NEXT_PUBLIC_AUTH_API_URL=http://localhost:8007
NEXT_PUBLIC_WAGTAIL_URL=http://localhost:8082
NEXT_PUBLIC_SALEOR_URL=http://localhost:8010

# Platform-specific (automatically set)
NEXT_PUBLIC_PLATFORM=bizosaas-admin|bizoholic-marketing|coreldove-ecommerce
```

---

## 🔧 **Development Workflow**

### **1. Prerequisites**
```bash
# Ensure FastAPI Brain is running
docker-compose up bizosaas-brain

# Ensure Auth Service v2 is running  
docker-compose up auth-service-v2

# Ensure backend data stores are running
docker-compose up wagtail-cms saleor-backend
```

### **2. Start Frontend Development**
```bash
# Install dependencies (first time)
cd frontend/apps/bizosaas-admin && npm install
cd ../bizoholic-frontend && npm install  
cd ../coreldove-frontend && npm install

# Start all frontends
./scripts/start-frontend-dev.sh
```

### **3. View Logs**
```bash
# View all logs
tail -f logs/bizosaas-admin.log
tail -f logs/bizoholic-marketing.log
tail -f logs/coreldove-ecommerce.log
```

---

## 🧪 **Testing the Setup**

### **1. Authentication Flow Test**
1. Visit http://localhost:3000 (should redirect to login if not authenticated)
2. Login with test credentials
3. Verify redirect to appropriate dashboard based on role
4. Navigate between platforms - should maintain session

### **2. API Integration Test**  
1. Open browser dev tools
2. Navigate to any frontend application
3. Check Network tab for API calls to Brain Gateway (port 8001)
4. Verify authentication headers and responses

### **3. Role-Based Access Test**
1. Login with different user roles
2. Verify access permissions match the matrix above
3. Test unauthorized access attempts

---

## 📋 **Troubleshooting**

### **Common Issues**

**Port conflicts:**
```bash
# Check what's running on ports
lsof -i :3000
lsof -i :3001  
lsof -i :3002

# Kill processes if needed
./scripts/stop-frontend-dev.sh
```

**Authentication errors:**
- Ensure Auth Service v2 is running on port 8007
- Check browser console for specific error messages
- Clear browser storage if needed

**API connection errors:**
- Ensure Brain API Gateway is running on port 8001
- Check Docker containers are healthy
- Verify network connectivity between services

### **Debug Commands**
```bash
# Check service health
curl http://localhost:8001/health  # Brain API
curl http://localhost:8007/health  # Auth Service

# View container logs
docker-compose logs bizosaas-brain
docker-compose logs auth-service-v2
```

---

## 🎉 **Success Indicators**

✅ **Setup is complete when:**
- All three frontend applications start without errors
- Authentication redirects work correctly  
- API calls route through Brain Gateway
- Role-based access control functions properly
- Cross-platform session management works

The BizOSaaS Platform frontend is now ready for development with full PRD compliance!

---

**🚀 Next Steps:**
1. Start backend services: `docker-compose up`
2. Start frontend applications: `./scripts/start-frontend-dev.sh`
3. Begin development on your specific platform features
4. Deploy using production Docker configuration when ready