# 🚀 BizoholicSaaS Platform - Quick Start Testing Guide

## 🎯 **IMMEDIATE ACCESS - Start Here!**

### **1. Platform Validation (Run This First)**
```bash
cd /home/alagiri/projects/bizoholic/tests
./validate-platform.sh
```
This will show you all working services and access URLs.

### **2. Primary Access URLs**

#### **Admin Dashboard (Monitoring)**
- **URL**: http://localhost:30090/graph  
- **Access**: `kubectl port-forward -n bizosaas-dev svc/bizosaas-dashboard 30090:80`
- **Purpose**: System monitoring and metrics

#### **Database Access**
- **URL**: postgresql://localhost:30432/bizoholic
- **Credentials**: Username: `bizoholic`, Password: `bizoholic123`
- **Access**: `kubectl port-forward -n bizosaas-dev svc/bizosaas-postgresql-nodeport 30432:5432`

#### **Main Website**
- **URL**: http://localhost:30300 (if accessible)
- **Access**: `kubectl port-forward -n bizosaas-dev svc/bizoholic-marketing-website-service 30300:3080`

### **3. Core Services Status**

✅ **Currently Working:**
- Admin Dashboard (monitoring)
- PostgreSQL Database  
- Agency Portal
- Client Portal
- Billing System
- Marketing Website
- Coreldove E-commerce

❌ **Needs Attention:**
- AI Agents Service (CrashLoopBackOff)
- Strapi CMS (connection issues)
- Vault Services (initialization)

---

## 🧪 **Complete Testing Workflow**

### **Step 1: Platform Health Check**
```bash
# Run comprehensive validation
cd /home/alagiri/projects/bizoholic/tests
./validate-platform.sh

# Check specific service
kubectl get pods -n bizosaas-dev
kubectl get services -n bizosaas-dev
```

### **Step 2: Access Admin Dashboard**
```bash
# Forward port for admin dashboard
kubectl port-forward -n bizosaas-dev svc/bizosaas-dashboard 30090:80

# Open in browser
open http://localhost:30090/graph
```

### **Step 3: Database Testing**
```bash
# Forward database port
kubectl port-forward -n bizosaas-dev svc/bizosaas-postgresql-nodeport 30432:5432

# Connect to database
psql -h localhost -p 30432 -U bizoholic -d bizoholic

# Test queries
\dt  # List tables
SELECT * FROM tenants LIMIT 5;
SELECT * FROM ai_insights LIMIT 5;
```

### **Step 4: Test Core APIs**
```bash
# Test backend API (if accessible)
curl http://localhost:8000/health

# Test specific services
curl http://localhost:8001/health  # User Management
curl http://localhost:8002/health  # Campaign Management
```

### **Step 5: Fix AI Agents (If Needed)**
```bash
# Check AI agents logs
kubectl logs -n bizosaas-dev -l app=bizosaas-crewai-enhanced

# Restart AI agents service
kubectl rollout restart deployment/bizosaas-crewai-enhanced -n bizosaas-dev

# Test AI agents
cd /home/alagiri/projects/bizoholic/tests
./ai-agents-test.sh
```

---

## 🔑 **Credentials & Access Details**

### **Database Credentials**
- **Host**: localhost:30432
- **Database**: bizoholic  
- **Username**: bizoholic
- **Password**: bizoholic123

### **Service Credentials** (Auto-extracted from K3s)
- Check the comprehensive guide for specific service credentials
- Most services use JWT token authentication

### **Admin Access**
- Admin interfaces available through port forwarding
- No specific login required for monitoring dashboard

---

## 🎯 **What You Can Test Right Now**

### **✅ Immediately Available:**
1. **System Monitoring**: Admin dashboard shows resource usage
2. **Database Access**: Full PostgreSQL database with business data
3. **Service Health**: All core business services operational
4. **Portal Interfaces**: Agency and client portal UIs

### **🔧 Requires Setup:**
1. **AI Agents**: Fix CrashLoopBackOff issue first
2. **Strapi CMS**: Resolve connection issues
3. **Frontend Access**: May need ingress configuration

### **🎨 User Interface Access:**
1. **Agency Portal**: Business management interface
2. **Client Portal**: Customer-facing dashboard  
3. **Admin Dashboard**: System monitoring and metrics
4. **Database Admin**: Direct data access and management

---

## 🚨 **Troubleshooting Quick Fixes**

### **If Services Won't Start:**
```bash
# Restart specific service
kubectl rollout restart deployment/[service-name] -n bizosaas-dev

# Check logs
kubectl logs -n bizosaas-dev -l app=[service-name]

# Check resource limits
kubectl describe pod [pod-name] -n bizosaas-dev
```

### **If Port Forwarding Fails:**
```bash
# Find correct service name
kubectl get svc -n bizosaas-dev

# Try different port
kubectl port-forward -n bizosaas-dev svc/[service-name] [local-port]:[service-port]
```

### **If Database Connection Fails:**
```bash
# Check database pod status
kubectl get pod -n bizosaas-dev -l app=bizosaas-postgres

# Check service endpoint
kubectl get endpoints -n bizosaas-dev bizosaas-postgresql-nodeport
```

---

## 📊 **Expected Testing Results**

### **Working Features:**
- ✅ Database with 11+ tables of business data
- ✅ Multi-tenant architecture with RLS policies
- ✅ Monitoring dashboard with real-time metrics
- ✅ Portal interfaces for different user types
- ✅ E-commerce integration (Coreldove/Medusa)

### **Advanced Features (Once AI Agents Fixed):**
- 🤖 28 AI marketing agents
- 📈 Campaign creation and optimization
- 📧 Email marketing automation
- 🎯 Lead generation and nurturing
- 📊 Advanced analytics and reporting

---

## 📞 **Support**

If you encounter issues:
1. Run `./validate-platform.sh` for current status
2. Check the comprehensive testing guide at `/home/alagiri/projects/bizoholic/tests/COMPREHENSIVE_PLATFORM_ACCESS_TESTING_GUIDE.md`
3. Review service logs with `kubectl logs` commands
4. Check pod status with `kubectl get pods -n bizosaas-dev`

**Happy Testing! 🎉**