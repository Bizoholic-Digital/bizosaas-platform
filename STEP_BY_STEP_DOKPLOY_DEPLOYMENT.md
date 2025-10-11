# 🚀 Step-by-Step Dokploy Deployment Guide

## 📋 PRE-DEPLOYMENT CHECKLIST

Before starting, ensure you have:
- [ ] Access to Dokploy at http://194.238.16.237:3000
- [ ] DNS configured for staging domains (stg.bizoholic.com, stg.coreldove.com, stg.thrillring.com)
- [ ] API keys ready (8 keys needed for Phase 2)
- [ ] GitHub repository accessible: https://github.com/Bizoholic-Digital/bizosaas-platform.git

**Estimated Total Time**: 90-120 minutes

---

## 🏗️ PHASE 1: CREATE INFRASTRUCTURE PROJECT (15-20 minutes)

### **Step 1: Access Dokploy Dashboard**
1. Open browser
2. Navigate to: `http://194.238.16.237:3000`
3. Log in with your credentials

### **Step 2: Create New Project**
1. Click **"Projects"** in the left sidebar
2. Click **"Create Project"** button (top right)
3. Fill in project details:
   - **Project Name**: `bizosaas-infrastructure-staging`
   - **Description**: `Core infrastructure services for BizOSaaS staging environment`
4. Click **"Create Project"**

### **Step 3: Enter the New Project**
1. You should see the new project in the projects list
2. Click on **"bizosaas-infrastructure-staging"** to enter it
3. You'll see an empty project page

### **Step 4: Create Docker Compose Application**
1. Click **"New Application"** or **"Add Service"** button
2. Select **"Docker Compose"** as the application type
3. Fill in application details:
   - **Application Name**: `infrastructure-services`
   - **Description**: `PostgreSQL, Redis, Vault, and Temporal services`
4. Click **"Next"** or **"Continue"**

### **Step 5: Configure Application**

#### **Option A: Use GitHub Repository (Recommended)**
1. **Source Type**: Select **"GitHub"** or **"Git Repository"**
2. **Repository URL**: `https://github.com/Bizoholic-Digital/bizosaas-platform.git`
3. **Branch**: `main`
4. **Docker Compose Path**: `/dokploy-infrastructure-staging.yml`
5. Click **"Next"**

#### **Option B: Upload Docker Compose File**
1. **Source Type**: Select **"Upload"** or **"Docker Compose"**
2. Click **"Upload File"** or **"Browse"**
3. Navigate to: `/home/alagiri/projects/bizoholic/dokploy-infrastructure-staging.yml`
4. Select the file and upload
5. Click **"Next"**

### **Step 6: Deploy Infrastructure**
1. Review the configuration
2. Click **"Deploy"** button
3. Wait for deployment to start (you'll see build logs)
4. **Expected wait time**: 5-10 minutes for all containers to start

### **Step 7: Monitor Deployment**
1. Watch the logs as containers build and start
2. Look for successful startup messages
3. Wait for all 6 containers to show **"Running"** status:
   - bizosaas-postgres-staging
   - bizosaas-redis-staging
   - bizosaas-vault-staging
   - bizosaas-temporal-server-staging
   - bizosaas-temporal-ui-staging
   - bizosaas-temporal-integration-staging

### **Step 8: Verify Infrastructure Deployment**

#### **Check Container Status in Dokploy**
1. In the application view, you should see all 6 containers listed
2. Each should show **"Running"** status with green indicator
3. Check logs for any errors

#### **Test Services Externally**
Open terminal and run:
```bash
# Test Vault
curl http://194.238.16.237:8200/v1/sys/health

# Test Temporal UI
curl http://194.238.16.237:8082

# Test Temporal Integration
curl http://194.238.16.237:8009/health
```

**Expected**: HTTP 200 responses

#### **Check in Browser**
1. Temporal UI: `http://194.238.16.237:8082`
2. Vault UI: `http://194.238.16.237:8200/ui`

**✅ Phase 1 Complete!** Infrastructure is running.

---

## 🔧 PHASE 2: CREATE BACKEND SERVICES PROJECT (20-30 minutes)

### **Step 1: Return to Projects Dashboard**
1. Click **"Projects"** in the left sidebar
2. You should now see your infrastructure project listed

### **Step 2: Create Backend Services Project**
1. Click **"Create Project"** button
2. Fill in project details:
   - **Project Name**: `bizosaas-backend-staging`
   - **Description**: `Backend services and APIs for BizOSaaS staging`
3. Click **"Create Project"**

### **Step 3: Enter the Backend Project**
1. Click on **"bizosaas-backend-staging"** to enter it
2. You'll see an empty project page

### **Step 4: Create Backend Application**
1. Click **"New Application"** button
2. Select **"Docker Compose"** as the application type
3. Fill in application details:
   - **Application Name**: `backend-services`
   - **Description**: `Brain API, CRM, AI Agents, E-commerce APIs`
4. Click **"Next"**

### **Step 5: Configure Backend Application**

#### **Option A: Use GitHub Repository (Recommended)**
1. **Source Type**: Select **"GitHub"** or **"Git Repository"**
2. **Repository URL**: `https://github.com/Bizoholic-Digital/bizosaas-platform.git`
3. **Branch**: `main`
4. **Docker Compose Path**: `/dokploy-backend-staging.yml`
5. Click **"Next"**

#### **Option B: Upload Docker Compose File**
1. **Source Type**: Select **"Upload"**
2. Upload file: `/home/alagiri/projects/bizoholic/dokploy-backend-staging.yml`
3. Click **"Next"**

### **Step 6: Configure Environment Variables**

**CRITICAL**: You must add these 8 environment variables:

Click **"Environment Variables"** or **"Add Environment Variable"**

Add each of these (replace with your actual keys):

```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxx
PAYPAL_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxx
PAYPAL_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxx
AMAZON_ACCESS_KEY=AKIAxxxxxxxxxxxxxxxxxxxxx
AMAZON_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxx
```

**How to add each variable:**
1. Click **"Add Environment Variable"** or **"+"**
2. **Key**: (e.g., `OPENROUTER_API_KEY`)
3. **Value**: (your actual API key)
4. Repeat for all 8 variables
5. Click **"Save"** or **"Next"**

**Don't have API keys yet?** See `phase2-env-template.txt` for instructions on how to obtain them.

### **Step 7: Deploy Backend Services**
1. Review configuration and environment variables
2. Click **"Deploy"** button
3. Watch the build logs
4. **Expected wait time**: 10-15 minutes for all 8 containers to build and start

### **Step 8: Monitor Backend Deployment**
Watch for all 8 containers to show **"Running"** status:
- bizosaas-brain-staging (Port 8001) ⭐ MOST CRITICAL
- bizosaas-wagtail-staging (Port 8002)
- bizosaas-django-crm-staging (Port 8003)
- bizosaas-directory-api-staging (Port 8004)
- coreldove-backend-staging (Port 8005)
- bizosaas-ai-agents-staging (Port 8010)
- amazon-sourcing-staging (Port 8085)
- bizosaas-saleor-staging (Port 8000)

### **Step 9: Verify Backend Deployment**

#### **Test Critical Services**
Open terminal and run:
```bash
# Test Brain API (MOST IMPORTANT)
curl http://194.238.16.237:8001/health

# Test Django CRM
curl http://194.238.16.237:8003/health/

# Test CorelDove Backend
curl http://194.238.16.237:8005/health

# Test AI Agents
curl http://194.238.16.237:8010/health
```

**Expected**: All should return HTTP 200

#### **Run Comprehensive Backend Verification**
```bash
cd /home/alagiri/projects/bizoholic
./verify-backend-deployment.sh
```

**Expected**: 100% pass rate

**✅ Phase 2 Complete!** Backend services are running.

---

## 📱 PHASE 3: CREATE FRONTEND APPLICATIONS PROJECT (30-40 minutes)

### **Step 1: Verify DNS Configuration First**

**CRITICAL**: Before proceeding, ensure DNS is configured!

Check DNS propagation:
```bash
dig stg.bizoholic.com
dig stg.coreldove.com
dig stg.thrillring.com
```

**Expected output**: Each should show:
```
;; ANSWER SECTION:
stg.bizoholic.com.    300    IN    A    194.238.16.237
```

If DNS not propagated yet, **WAIT** before proceeding (can take 5-30 minutes).

### **Step 2: Create Frontend Project**
1. Return to **"Projects"** dashboard
2. Click **"Create Project"**
3. Fill in project details:
   - **Project Name**: `bizosaas-frontend-staging`
   - **Description**: `Next.js frontend applications with staging domains`
4. Click **"Create Project"**

### **Step 3: Enter Frontend Project**
1. Click on **"bizosaas-frontend-staging"**
2. Empty project page appears

### **Step 4: Create Frontend Application**
1. Click **"New Application"**
2. Select **"Docker Compose"**
3. Fill in details:
   - **Application Name**: `frontend-applications`
   - **Description**: `Marketing sites, portals, e-commerce frontends`
4. Click **"Next"**

### **Step 5: Configure Frontend Application**

#### **Option A: Use GitHub Repository (Recommended)**
1. **Source Type**: **"GitHub"** or **"Git Repository"**
2. **Repository URL**: `https://github.com/Bizoholic-Digital/bizosaas-platform.git`
3. **Branch**: `main`
4. **Docker Compose Path**: `/dokploy-frontend-staging.yml`
5. Click **"Next"**

#### **Option B: Upload Docker Compose File**
1. **Source Type**: **"Upload"**
2. Upload: `/home/alagiri/projects/bizoholic/dokploy-frontend-staging.yml`
3. Click **"Next"**

### **Step 6: Deploy Frontend Applications**
1. Review configuration
2. Click **"Deploy"**
3. Watch build logs
4. **Expected wait time**: 10-15 minutes for 6 containers to build and start

### **Step 7: Monitor Frontend Deployment**
Wait for all 6 containers to show **"Running"** status:
- bizoholic-frontend-staging (Port 3000)
- client-portal-staging (Port 3001)
- coreldove-frontend-staging (Port 3002)
- business-directory-staging (Port 3004)
- thrillring-gaming-staging (Port 3005)
- admin-dashboard-staging (Port 3009)

### **Step 8: Configure Domain Routing**

Now we need to configure domains for each frontend container.

#### **8A: Configure Bizoholic Marketing Frontend**
1. In the frontend project, click on **"bizoholic-frontend-staging"** container
2. Go to **"Domains"** tab or **"Settings"** → **"Domains"**
3. Click **"Add Domain"** or **"+"**
4. Fill in domain configuration:
   - **Host/Domain**: `stg.bizoholic.com`
   - **Port**: `3000`
   - **Path**: `/` (or leave empty)
   - **HTTPS/SSL**: ✓ Enable
   - **Certificate Provider**: Let's Encrypt (or Auto SSL)
5. Click **"Save"** or **"Add Domain"**
6. Wait 1-2 minutes for SSL certificate generation

#### **8B: Configure CorelDove E-commerce Frontend**
1. Click on **"coreldove-frontend-staging"** container
2. Go to **"Domains"** tab
3. Click **"Add Domain"**
4. Configuration:
   - **Host**: `stg.coreldove.com`
   - **Port**: `3002`
   - **Path**: `/`
   - **HTTPS**: ✓ Enable
   - **Certificate**: Let's Encrypt
5. Click **"Save"**
6. Wait for SSL certificate

#### **8C: Configure ThrillRing Gaming Frontend**
1. Click on **"thrillring-gaming-staging"** container
2. Go to **"Domains"** tab
3. Click **"Add Domain"**
4. Configuration:
   - **Host**: `stg.thrillring.com`
   - **Port**: `3005`
   - **Path**: `/`
   - **HTTPS**: ✓ Enable
   - **Certificate**: Let's Encrypt
5. Click **"Save"**
6. Wait for SSL certificate

#### **8D: Configure Client Portal (Path-based routing)**
1. Click on **"client-portal-staging"** container
2. Go to **"Domains"** tab
3. Click **"Add Domain"**
4. Configuration:
   - **Host**: `stg.bizoholic.com`
   - **Path**: `/login` (or `/login/`)
   - **Internal Path**: `/` (if available)
   - **Port**: `3001`
   - **Strip Path**: ✓ Yes (if available)
   - **HTTPS**: ✓ Enable
5. Click **"Save"**

#### **8E: Configure Admin Dashboard (Path-based routing)**
1. Click on **"admin-dashboard-staging"** container
2. Go to **"Domains"** tab
3. Click **"Add Domain"**
4. Configuration:
   - **Host**: `stg.bizoholic.com`
   - **Path**: `/admin` (or `/admin/`)
   - **Internal Path**: `/`
   - **Port**: `3009`
   - **Strip Path**: ✓ Yes
   - **HTTPS**: ✓ Enable
5. Click **"Save"**

### **Step 9: Verify Frontend Deployment**

#### **Test Staging Domains in Browser**
1. Open browser and test each domain:
   - https://stg.bizoholic.com
   - https://stg.coreldove.com
   - https://stg.thrillring.com
   - https://stg.bizoholic.com/login/
   - https://stg.bizoholic.com/admin/

2. Check for:
   - ✓ HTTPS (padlock icon)
   - ✓ Valid SSL certificate
   - ✓ Page loads successfully
   - ✓ No certificate warnings

#### **Test from Terminal**
```bash
# Test all staging domains
curl -I https://stg.bizoholic.com
curl -I https://stg.coreldove.com
curl -I https://stg.thrillring.com
curl -I https://stg.bizoholic.com/login/
curl -I https://stg.bizoholic.com/admin/
```

**Expected**: All return `HTTP/2 200 OK`

#### **Run Comprehensive Frontend Verification**
```bash
cd /home/alagiri/projects/bizoholic
./verify-frontend-deployment.sh
```

**Expected**: 100% pass rate

**✅ Phase 3 Complete!** Frontend applications are running with SSL!

---

## ✅ FINAL VERIFICATION - ALL 20 CONTAINERS

### **Run Complete Platform Verification**
```bash
cd /home/alagiri/projects/bizoholic
./verify-all-20-containers.sh
```

**Expected Output**:
```
✓ Infrastructure: 6/6 containers running
✓ Backend: 8/8 containers running
✓ Frontend: 6/6 containers running
✓ Total: 20/20 containers operational
✓ Success Rate: 100%
✓ ALL SYSTEMS OPERATIONAL
```

### **Verify WordPress Sites Still Working**

**CRITICAL CHECK**: Ensure we didn't break anything!

Test your production WordPress sites:
```bash
curl -I https://bizoholic.com      # Should return 200 OK
curl -I https://coreldove.com      # Should return 200 OK
curl -I https://thrillring.com     # Should return 200 OK
```

Or open in browser and verify they still work perfectly.

**✅ If WordPress sites work → Deployment successful with zero disruption!**

---

## 🎉 DEPLOYMENT COMPLETE!

### **What You've Achieved**

**3 New Dokploy Projects Created:**
1. ✅ bizosaas-infrastructure-staging (6 containers)
2. ✅ bizosaas-backend-staging (8 containers)
3. ✅ bizosaas-frontend-staging (6 containers)

**20 Containers Deployed:**
- ✅ Infrastructure: PostgreSQL, Redis, Vault, Temporal (6)
- ✅ Backend: Brain API, CRMs, AI Agents, E-commerce APIs (8)
- ✅ Frontend: Marketing sites, Portals, E-commerce stores (6)

**5 Staging Domains Configured:**
- ✅ https://stg.bizoholic.com (with SSL)
- ✅ https://stg.coreldove.com (with SSL)
- ✅ https://stg.thrillring.com (with SSL)
- ✅ https://stg.bizoholic.com/login/ (path-based)
- ✅ https://stg.bizoholic.com/admin/ (path-based)

**WordPress Sites Protected:**
- ✅ bizoholic.com (untouched, still working)
- ✅ coreldove.com (untouched, still working)
- ✅ thrillring.com (untouched, still working)

---

## 🧪 NEXT STEPS: STAGING TESTING

### **Week 1: Functional Testing**
- [ ] Test all features on staging domains
- [ ] Verify API functionality
- [ ] Test authentication flows
- [ ] Check e-commerce functionality
- [ ] Test admin dashboard features

### **Week 2: Performance & Security**
- [ ] Performance testing
- [ ] Load testing
- [ ] Security testing
- [ ] SSL configuration audit
- [ ] Database performance

### **Week 3-4: User Acceptance**
- [ ] Stakeholder testing
- [ ] User acceptance testing
- [ ] Bug fixes and optimization
- [ ] Production migration planning

---

## 🆘 TROUBLESHOOTING

### **Container Won't Start**
1. Check logs in Dokploy UI
2. Verify environment variables are set correctly
3. Check if dependent services are running
4. Review `backend-services-troubleshooting.md`

### **Domain Not Accessible**
1. Verify DNS propagation: `dig stg.bizoholic.com`
2. Check SSL certificate status in Dokploy
3. Wait 5 minutes for Let's Encrypt
4. Review `FRONTEND_DOMAIN_CONFIGURATION_GUIDE.md`

### **Health Check Failing**
1. Check service logs
2. Verify database connectivity
3. Check environment variables
4. Run phase-specific verification scripts

---

## 📊 DEPLOYMENT SUMMARY

**Total Deployment Time**: 90-120 minutes
**Projects Created**: 3 new projects
**Containers Deployed**: 20 containers
**Domains Configured**: 5 staging domains
**SSL Certificates**: 5 automatic Let's Encrypt certificates
**WordPress Sites Affected**: 0 (zero disruption)
**Success Rate**: Expected 95%+

**Congratulations! Your BizOSaaS staging environment is now live!** 🎉

---

*Generated on October 10, 2025*
*Safe Deployment Guide*
*🤖 Generated with [Claude Code](https://claude.com/claude-code)*
