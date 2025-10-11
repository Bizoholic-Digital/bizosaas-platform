# 🚀 Immediate Staging Deployment Instructions

## 📋 **READY TO DEPLOY NOW**

All deployment files have been tested and verified. You can proceed with immediate deployment.

**VPS**: 194.238.16.237
**Dokploy**: http://194.238.16.237:3000
**Total**: 20 containers (6 + 8 + 6)

---

## 🏗️ **PHASE 1: INFRASTRUCTURE DEPLOYMENT** (15-20 minutes)

### **Step 1: Access Dokploy**
1. Open browser: `http://194.238.16.237:3000`
2. Login with your Dokploy credentials

### **Step 2: Create Infrastructure Project**
1. Click **"Projects"** → **"Create Project"**
2. **Project Name**: `bizosaas-infrastructure-staging`
3. **Description**: `Infrastructure services for staging environment (6 containers)`
4. Click **"Create Project"**

### **Step 3: Add Application**
1. Inside the project, click **"Create Application"**
2. Select **"Docker Compose"**
3. **Application Name**: `infrastructure-services`
4. **Source Type**: **File Upload**
5. **Upload File**: `dokploy-infrastructure-staging.yml`
6. Click **"Create Application"**

### **Step 4: Deploy Infrastructure**
1. Click **"Deploy"** button
2. **Wait 15-20 minutes** for deployment
3. **Monitor logs** in real-time
4. **Verify 6 containers** are running

### **Step 5: Verify Infrastructure**
Once deployed, verify these services are accessible:
```bash
curl http://194.238.16.237:8200/v1/sys/health  # Vault
curl http://194.238.16.237:8082                # Temporal UI
```

---

## 🔧 **PHASE 2: BACKEND SERVICES DEPLOYMENT** (20-25 minutes)

### **Step 1: Create Backend Project**
1. Go back to **Projects** → **"Create Project"**
2. **Project Name**: `bizosaas-backend-staging`
3. **Description**: `Backend services for staging environment (8 containers)`
4. Click **"Create Project"**

### **Step 2: Add Backend Application**
1. Inside the project, click **"Create Application"**
2. Select **"Docker Compose"**
3. **Application Name**: `backend-services`
4. **Source Type**: **File Upload**
5. **Upload File**: `dokploy-backend-staging-corrected.yml`

### **Step 3: Configure Environment Variables**
**IMPORTANT**: Add these environment variables before deployment:
```bash
OPENROUTER_API_KEY=your_staging_key_here
OPENAI_API_KEY=your_staging_key_here
ANTHROPIC_API_KEY=your_staging_key_here
STRIPE_SECRET_KEY=sk_test_your_test_key
PAYPAL_CLIENT_ID=your_sandbox_client_id
PAYPAL_CLIENT_SECRET=your_sandbox_client_secret
AMAZON_ACCESS_KEY=your_staging_access_key
AMAZON_SECRET_KEY=your_staging_secret_key
DJANGO_SECRET_KEY=staging-secret-key-bizosaas-2025
DJANGO_CRM_SECRET_KEY=staging-crm-secret-key-2025
SALEOR_SECRET_KEY=staging-saleor-secret-key-2025
```

### **Step 4: Deploy Backend Services**
1. Click **"Deploy"** button
2. **Wait 20-25 minutes** for deployment
3. **Monitor logs** in real-time
4. **Verify 8 containers** are running

### **Step 5: Verify Backend Services**
Once deployed, verify these services are accessible:
```bash
curl http://194.238.16.237:8001/health  # Brain API
curl http://194.238.16.237:8005/health  # CorelDove Backend
curl http://194.238.16.237:8004/health  # Directory API
```

---

## 🎨 **PHASE 3: FRONTEND APPLICATIONS DEPLOYMENT** (15-20 minutes)

### **Step 1: Create Frontend Project**
1. Go back to **Projects** → **"Create Project"**
2. **Project Name**: `bizosaas-frontend-staging`
3. **Description**: `Frontend applications for staging environment (6 containers)`
4. Click **"Create Project"**

### **Step 2: Add Frontend Application**
1. Inside the project, click **"Create Application"**
2. Select **"Docker Compose"**
3. **Application Name**: `frontend-applications`
4. **Source Type**: **File Upload**
5. **Upload File**: `dokploy-frontend-staging.yml`

### **Step 3: Configure Frontend Environment Variables**
Add these environment variables:
```bash
GTM_ID_PRODUCTION=GTM-STAGING123
HOTJAR_ID_PRODUCTION=staging_hotjar_id
GTM_ID_CORELDOVE_PRODUCTION=GTM-CORELDOVE123
GTM_ID_THRILLRING_PRODUCTION=GTM-THRILLRING123
BASIC_AUTH_USERS=admin:$2y$10$encrypted_password_here
ADMIN_BASIC_AUTH_USERS=superadmin:$2y$10$encrypted_admin_password
```

### **Step 4: Deploy Frontend Applications**
1. Click **"Deploy"** button
2. **Wait 15-20 minutes** for deployment
3. **Monitor logs** in real-time
4. **Verify 6 containers** are running

### **Step 5: Verify Frontend Domains**
Once deployed, verify these domains are accessible:
```bash
# Test staging domains (may need DNS update first)
curl -I https://stg.bizoholic.com       # Marketing site
curl -I https://stg.coreldove.com       # E-commerce
curl -I https://stg.thrillring.com      # Gaming platform
```

---

## 🌐 **DNS CONFIGURATION REQUIRED**

### **Update These DNS Records**
```bash
# Add these A records to your DNS provider:
stg.bizoholic.com     A    194.238.16.237
stg.thrillring.com    A    194.238.16.237

# Already correct:
stg.coreldove.com     A    194.238.16.237
```

### **Verify DNS Propagation**
```bash
dig stg.bizoholic.com
dig stg.coreldove.com
dig stg.thrillring.com
```

---

## 🔍 **COMPLETE VERIFICATION**

### **Run Automated Verification**
After all deployments are complete:
```bash
./verify-staging-deployment.sh
```

### **Manual Health Checks**
```bash
# Infrastructure
curl http://194.238.16.237:8200/v1/sys/health
curl http://194.238.16.237:8082

# Backend
curl http://194.238.16.237:8001/health
curl http://194.238.16.237:8005/health
curl http://194.238.16.237:8004/health

# Frontend (after DNS updates)
curl -I https://stg.bizoholic.com
curl -I https://stg.coreldove.com
curl -I https://stg.thrillring.com
```

---

## 🎯 **SUCCESS CRITERIA**

### **Infrastructure Success (6/6 containers)**
- ✅ PostgreSQL running on port 5432
- ✅ Redis running on port 6379
- ✅ Vault accessible on port 8200
- ✅ Temporal Server running on port 7233
- ✅ Temporal UI accessible on port 8082
- ✅ Temporal Integration running on port 8009

### **Backend Success (8/8 containers)**
- ✅ Brain API responding on port 8001
- ✅ Wagtail CMS responding on port 8002
- ✅ Django CRM responding on port 8003
- ✅ Directory API responding on port 8004
- ✅ CorelDove Backend responding on port 8005
- ✅ AI Agents responding on port 8010
- ✅ Amazon Sourcing responding on port 8085
- ✅ Saleor responding on port 8000

### **Frontend Success (6/6 containers)**
- ✅ Bizoholic Marketing at https://stg.bizoholic.com
- ✅ Client Portal at https://stg.bizoholic.com/login/
- ✅ CorelDove E-commerce at https://stg.coreldove.com
- ✅ Business Directory at https://stg.bizoholic.com/directory/
- ✅ ThrillRing Gaming at https://stg.thrillring.com
- ✅ Admin Dashboard at https://stg.bizoholic.com/admin/

---

## ⏱️ **TOTAL DEPLOYMENT TIME**

| Phase | Duration | Containers | Status |
|-------|----------|------------|--------|
| Infrastructure | 15-20 min | 6 | Ready to deploy |
| Backend | 20-25 min | 8 | Ready to deploy |
| Frontend | 15-20 min | 6 | Ready to deploy |
| Verification | 10 min | - | Automated script ready |
| **Total** | **60-75 min** | **20** | **All files tested & ready** |

---

## 🚨 **TROUBLESHOOTING**

### **If Infrastructure Deployment Fails**
1. Check Dokploy logs for specific errors
2. Verify VPS has sufficient resources
3. Ensure Docker daemon is running
4. Check network connectivity

### **If Backend Deployment Fails**
1. Verify infrastructure is running first
2. Check environment variables are set correctly
3. Verify GitHub repository access
4. Check Docker image build logs

### **If Frontend Deployment Fails**
1. Verify backend services are running
2. Check environment variables
3. Verify domain DNS configuration
4. Check SSL certificate generation

### **If Domains Don't Work**
1. Update DNS records as specified above
2. Wait for DNS propagation (5-15 minutes)
3. Check Traefik routing in Dokploy logs
4. Verify SSL certificate generation

---

## 🎉 **POST-DEPLOYMENT**

### **Once All 20 Containers Are Running**
1. **Test all functionality** in staging environment
2. **Document any issues** and fixes needed
3. **Prepare production deployment** using production configs
4. **Plan WordPress migration** strategy

### **Next Steps**
1. **Production Deployment**: Deploy additional 20 production containers
2. **Domain Migration**: Switch main domains from WordPress
3. **Traffic Testing**: Load test the complete platform
4. **Go Live**: Make production environment active

---

## 📞 **SUPPORT**

If you encounter any issues during deployment:
1. Check the comprehensive logs in Dokploy dashboard
2. Use the verification scripts to identify specific problems
3. Refer to the troubleshooting section above
4. All deployment files have been tested and validated

**All 20 containers are ready for immediate deployment!** 🚀

---

*Generated on October 11, 2025*
*Immediate Deployment Instructions*
*🤖 Generated with [Claude Code](https://claude.com/claude-code)*