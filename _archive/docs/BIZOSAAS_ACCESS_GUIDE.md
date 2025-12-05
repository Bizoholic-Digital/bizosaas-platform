# BizoSaaS Multi-Company Platform Access Guide

## 🚀 Quick Setup

### 1. Update Your Hosts File

Add these entries to your hosts file:

**Windows:** `C:\Windows\System32\drivers\etc\hosts`  
**Mac/Linux:** `/etc/hosts`

```bash
# BizoSaaS Multi-Company Platform
172.25.198.116 bizoholic.local
172.25.198.116 www.bizoholic.local
172.25.198.116 saas.bizoholic.local
172.25.198.116 platform.bizoholic.local
172.25.198.116 api.bizoholic.local
172.25.198.116 cms.bizoholic.local
172.25.198.116 agents.bizoholic.local

# CoreLDove E-commerce Platform
172.25.198.116 coreldove.local
172.25.198.116 api.coreldove.local
172.25.198.116 admin.coreldove.local

# ThrillRing Platform (Coming Soon)
172.25.198.116 thrillring.local

# QuantTrade Platform (Coming Soon) 
172.25.198.116 trade.bizoholic.local
```

## 🌐 Platform Access URLs

### **Bizoholic - Main Company Website**

| Service | URL | Description | Status |
|---------|-----|-------------|--------|
| **Main Website** | http://bizoholic.local | Corporate website and portfolio | ✅ Active |
| **BizoSaaS Platform** | http://saas.bizoholic.local | Multi-tenant SaaS platform | ✅ Active |
| **API Gateway** | http://api.bizoholic.local | REST API endpoints | ✅ Active |
| **CMS Admin** | http://cms.bizoholic.local | Content management system | ✅ Active |
| **AI Agents Hub** | http://agents.bizoholic.local | Development team agents | ✅ Active |

#### **AI Development Team Agents:**
- **Senior Developer:** http://agents.bizoholic.local/senior
- **Junior Developer:** http://agents.bizoholic.local/junior
- **QA Agent:** http://agents.bizoholic.local/qa
- **DevOps Agent:** http://agents.bizoholic.local/devops
- **Documentation Agent:** http://agents.bizoholic.local/docs

---

### **CoreLDove - E-commerce & Dropshipping Platform**

| Service | URL | Description | Status |
|---------|-----|-------------|--------|
| **E-commerce Store** | http://coreldove.local | NextJS frontend with Tailwind CSS | 🔄 Starting |
| **Admin Dashboard** | http://admin.coreldove.local | Medusa.js admin interface | 🔄 Starting |
| **API Backend** | http://api.coreldove.local | Medusa.js e-commerce API | 🔄 Starting |

#### **CoreLDove Features:**
- **Frontend:** NextJS + Tailwind CSS + ShadCN components
- **Backend:** Medusa.js headless e-commerce
- **Features:** Product catalog, cart, checkout, order management
- **Sample Products:** Premium headphones, fitness trackers

#### **Default Admin Credentials:**
- **Email:** admin@coreldove.local
- **Password:** admin123

---

## 🧪 Testing Guide

### **1. Test Bizoholic Website**
```bash
# Test main website
curl -H "Host: bizoholic.local" http://172.25.198.116/

# Expected: Website Builder Service JSON response
```

### **2. Test CoreLDove E-commerce**
```bash
# Test frontend (may take 2-3 minutes to start)
curl -H "Host: coreldove.local" http://172.25.198.116/

# Test API health
curl -H "Host: api.coreldove.local" http://172.25.198.116/health

# Test admin panel
curl -H "Host: admin.coreldove.local" http://172.25.198.116/
```

### **3. Test AI Agents**
```bash
# Test Senior Developer Agent
curl -H "Host: agents.bizoholic.local" http://172.25.198.116/senior/health

# Test BizoSaaS API
curl -H "Host: api.bizoholic.local" http://172.25.198.116/health
```

---

## 🛠 Service Status & Troubleshooting

### **Current Service Status:**

#### ✅ **Working Services:**
- `website-builder-service` (bizoholic.local)
- `bizosaas-backend-simple` (API services)
- Development team agents (Senior, Junior, QA, DevOps, Docs)
- Billing and dashboard services

#### 🔄 **Starting Services (May Need Time):**
- `coreldove-frontend` (Pending - needs CPU resources)
- `coreldove-medusa` (Pending - needs CPU resources)

### **Common Issues & Solutions:**

#### **Issue: "This site can't be reached"**
**Solution:**
1. Verify hosts file entries
2. Check if using correct IP: `172.25.198.116`
3. Ensure no typos in domain names

#### **Issue: "404 Page Not Found"**
**Solution:**
1. Service may be starting up (wait 2-3 minutes)
2. Check service status: `kubectl get pods -n bizosaas-dev`
3. Try alternative URL path

#### **Issue: "Connection refused"**
**Solution:**
1. Service may need more resources
2. Check pod logs: `kubectl logs [pod-name] -n bizosaas-dev`
3. Restart browser/clear cache

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    K3s Cluster                         │
│                 IP: 172.25.198.116                     │
└─────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   Traefik Ingress │
                    │   Load Balancer   │
                    └─────────┬─────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼──────┐    ┌────────▼────────┐    ┌──────▼──────┐
│   Bizoholic  │    │   CoreLDove     │    │ ThrillRing  │
│   (Parent)   │    │  (E-commerce)   │    │  (Events)   │
├──────────────┤    ├─────────────────┤    ├─────────────┤
│ Website      │    │ NextJS Frontend │    │ Coming Soon │
│ BizoSaaS     │    │ Medusa Backend  │    │             │
│ AI Agents    │    │ Admin Panel     │    │             │
└──────────────┘    └─────────────────┘    └─────────────┘
```

---

## 🚀 Getting Started (Step-by-Step)

### Step 1: Update Hosts File
Copy the hosts entries above to your system's hosts file.

### Step 2: Test Bizoholic Website
Open your browser and go to: **http://bizoholic.local**
- Should show the Website Builder Service interface
- Contains links to BizoSaaS platform and other companies

### Step 3: Explore BizoSaaS Platform
Visit: **http://saas.bizoholic.local**
- Multi-tenant SaaS platform interface
- API-driven backend services

### Step 4: Test AI Development Agents
Visit: **http://agents.bizoholic.local/senior**
- Senior Developer Agent interface
- Try other agents: /junior, /qa, /devops, /docs

### Step 5: Wait for CoreLDove (If Starting)
- **Frontend:** http://coreldove.local
- **Admin:** http://admin.coreldove.local  
- **API:** http://api.coreldove.local
- Services may take 2-5 minutes to fully start

---

## 🔧 Advanced Monitoring

### **Check Service Status:**
```bash
# View all pods
kubectl get pods -n bizosaas-dev

# Check specific service logs
kubectl logs -f deployment/website-builder-service -n bizosaas-dev

# Monitor resource usage
kubectl top nodes
kubectl top pods -n bizosaas-dev
```

### **Quick Service Health Checks:**
```bash
# Bizoholic Website
curl -s http://172.25.198.116/ -H "Host: bizoholic.local" | head -5

# BizoSaaS API
curl -s http://172.25.198.116/health -H "Host: api.bizoholic.local"

# Senior Developer Agent
curl -s http://172.25.198.116/senior/health -H "Host: agents.bizoholic.local"
```

---

## 📞 Support & Next Steps

### **If you encounter issues:**
1. **Check hosts file** - Ensure correct IP and domains
2. **Wait for startup** - Some services need 2-5 minutes  
3. **Check service status** - Use kubectl commands above
4. **Review logs** - Check pod logs for specific errors

### **What's Working Now:**
- ✅ Bizoholic main website
- ✅ BizoSaaS platform access
- ✅ AI development team agents
- ✅ Multi-domain routing infrastructure

### **What's Starting:**
- 🔄 CoreLDove e-commerce frontend
- 🔄 CoreLDove Medusa.js backend
- 🔄 CoreLDove admin interface

**Happy testing! 🎉**

The platform is ready for exploration and development!
