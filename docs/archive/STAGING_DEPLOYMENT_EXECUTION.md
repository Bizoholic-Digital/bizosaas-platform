# 🚀 Staging Deployment Execution Guide

## 🎯 IMMEDIATE DEPLOYMENT STEPS

### **Phase 1: Infrastructure Project Deployment** (15-20 minutes)

#### Step 1: Access Dokploy Dashboard
```bash
# Open browser and navigate to:
http://194.238.16.237:3000

# Login with your Dokploy credentials
```

#### Step 2: Create Infrastructure Project
1. **Click "Projects"** → **"Create Project"**
2. **Project Details:**
   - **Name**: `bizosaas-infrastructure-staging`
   - **Description**: `Infrastructure services for staging environment (6 containers)`
3. **Click "Create Project"**

#### Step 3: Add Infrastructure Application
1. **Inside the project, click "Create Application"**
2. **Select "Docker Compose"**
3. **Application Details:**
   - **Name**: `infrastructure-services`
   - **Source Type**: **File Upload**
   - **Upload File**: `dokploy-infrastructure-staging.yml`
4. **Click "Create Application"**

#### Step 4: Deploy Infrastructure
1. **Click "Deploy"** button
2. **Wait 15-20 minutes** for deployment
3. **Monitor deployment logs** in real-time
4. **Verify 6 containers are running**

---

### **Phase 2: Backend Services Project Deployment** (20-25 minutes)

#### Step 1: Create Backend Project
1. **Go back to Projects** → **"Create Project"**
2. **Project Details:**
   - **Name**: `bizosaas-backend-staging`
   - **Description**: `Backend services for staging environment (8 containers)`
3. **Click "Create Project"**

#### Step 2: Add Backend Application
1. **Inside the project, click "Create Application"**
2. **Select "Docker Compose"**
3. **Application Details:**
   - **Name**: `backend-services`
   - **Source Type**: **File Upload**
   - **Upload File**: `dokploy-backend-staging.yml`

#### Step 3: Configure Environment Variables
**CRITICAL**: Add these environment variables before deployment:
```
OPENROUTER_API_KEY=your_staging_key
OPENAI_API_KEY=your_staging_key
ANTHROPIC_API_KEY=your_staging_key
STRIPE_SECRET_KEY=your_test_key
PAYPAL_CLIENT_ID=your_sandbox_id
PAYPAL_CLIENT_SECRET=your_sandbox_secret
AMAZON_ACCESS_KEY=your_staging_key
AMAZON_SECRET_KEY=your_staging_key
DJANGO_SECRET_KEY=staging-secret-key-bizosaas
DJANGO_CRM_SECRET_KEY=staging-crm-secret-key
SALEOR_SECRET_KEY=staging-saleor-secret-key
```

#### Step 4: Deploy Backend Services
1. **Click "Deploy"** button
2. **Wait 20-25 minutes** for deployment
3. **Monitor deployment logs** in real-time
4. **Verify 8 containers are running**

---

### **Phase 3: Frontend Applications Project Deployment** (15-20 minutes)

#### Step 1: Create Frontend Project
1. **Go back to Projects** → **"Create Project"**
2. **Project Details:**
   - **Name**: `bizosaas-frontend-staging`
   - **Description**: `Frontend applications for staging environment (6 containers)`
3. **Click "Create Project"**

#### Step 2: Add Frontend Application
1. **Inside the project, click "Create Application"**
2. **Select "Docker Compose"**
3. **Application Details:**
   - **Name**: `frontend-applications`
   - **Source Type**: **File Upload**
   - **Upload File**: `dokploy-frontend-staging.yml`

#### Step 3: Configure Environment Variables
Add these frontend environment variables:
```
GTM_ID_PRODUCTION=GTM-XXXXXXX
HOTJAR_ID_PRODUCTION=hotjar_id
GTM_ID_CORELDOVE_PRODUCTION=GTM-XXXXXXX
GTM_ID_THRILLRING_PRODUCTION=GTM-XXXXXXX
BASIC_AUTH_USERS=admin:encrypted_password
ADMIN_BASIC_AUTH_USERS=superadmin:encrypted_password
```

#### Step 4: Deploy Frontend Applications
1. **Click "Deploy"** button
2. **Wait 15-20 minutes** for deployment
3. **Monitor deployment logs** in real-time
4. **Verify 6 containers are running**

---

## 🔍 VERIFICATION AND TESTING

### Step 1: Run Verification Script
```bash
cd /home/alagiri/projects/bizoholic
./verify-staging-deployment.sh
```

### Step 2: Manual Testing
```bash
# Test staging infrastructure
curl http://194.238.16.237:8200/v1/sys/health  # Vault
curl http://194.238.16.237:8082                # Temporal UI

# Test staging backend
curl http://194.238.16.237:8001/health         # Brain API
curl http://194.238.16.237:8005/health         # CorelDove Backend

# Test staging frontend domains
curl -I https://stg.bizoholic.com              # Marketing site
curl -I https://stg.coreldove.com              # E-commerce
curl -I https://stg.thrillring.com             # Gaming platform

# Test admin and client portals
curl -I https://stg.bizoholic.com/login/       # Client portal
curl -I https://stg.bizoholic.com/admin/       # Admin dashboard
```

### Step 3: SSL Certificate Verification
```bash
# Check SSL certificates are auto-generated
openssl s_client -connect stg.bizoholic.com:443 -servername stg.bizoholic.com < /dev/null
openssl s_client -connect stg.coreldove.com:443 -servername stg.coreldove.com < /dev/null
openssl s_client -connect stg.thrillring.com:443 -servername stg.thrillring.com < /dev/null
```

---

## 🎯 SUCCESS CRITERIA

### Infrastructure Success (6/6 containers)
- ✅ PostgreSQL accessible on port 5432
- ✅ Redis accessible on port 6379
- ✅ Vault health check passing on port 8200
- ✅ Temporal Server running on port 7233
- ✅ Temporal UI accessible on port 8082
- ✅ Temporal Integration service on port 8009

### Backend Success (8/8 containers)
- ✅ Brain API responding on port 8001
- ✅ Wagtail CMS responding on port 8002
- ✅ Django CRM responding on port 8003
- ✅ Directory API responding on port 8004
- ✅ CorelDove Backend responding on port 8005
- ✅ AI Agents responding on port 8010
- ✅ Amazon Sourcing responding on port 8085
- ✅ Saleor responding on port 8000

### Frontend Success (6/6 containers)
- ✅ Bizoholic Marketing: https://stg.bizoholic.com
- ✅ Client Portal: https://stg.bizoholic.com/login/
- ✅ CorelDove E-commerce: https://stg.coreldove.com
- ✅ Business Directory: https://stg.bizoholic.com/directory/
- ✅ ThrillRing Gaming: https://stg.thrillring.com
- ✅ Admin Dashboard: https://stg.bizoholic.com/admin/

### SSL & Security Success
- ✅ All staging domains have valid SSL certificates
- ✅ Basic authentication working for admin areas
- ✅ HTTPS redirection working
- ✅ Security headers properly configured

---

## 🚨 TROUBLESHOOTING

### Common Issues and Solutions

#### Issue 1: Container Build Failures
```bash
# Check GitHub repository access
curl -I https://api.github.com/repos/Bizoholic-Digital/bizosaas-platform

# Verify Dockerfile paths in repository
```

#### Issue 2: Database Connection Issues
```bash
# Check PostgreSQL container logs
docker logs bizosaas-postgres-staging

# Test database connectivity
docker exec -it bizosaas-postgres-staging psql -U admin -d bizosaas_staging
```

#### Issue 3: SSL Certificate Issues
```bash
# Check Traefik logs for certificate generation
docker logs traefik

# Verify domain DNS resolution
dig stg.bizoholic.com
dig stg.coreldove.com
dig stg.thrillring.com
```

#### Issue 4: Memory/Resource Issues
```bash
# Check VPS resource usage
free -h
df -h
docker stats

# If resources are low, consider reducing replica counts
```

---

## ⏱️ DEPLOYMENT TIMELINE

| Phase | Duration | Containers | Critical Path |
|-------|----------|------------|---------------|
| **Infrastructure** | 15-20 min | 6 | PostgreSQL → Redis → Vault → Temporal |
| **Backend Services** | 20-25 min | 8 | Brain API → CRM → E-commerce → AI Agents |
| **Frontend Apps** | 15-20 min | 6 | Marketing → E-commerce → Gaming + Admin |
| **Verification** | 10-15 min | - | Health checks → SSL → Domain testing |
| **Total** | **60-80 min** | **20** | **Complete staging environment** |

---

## 🎉 POST-DEPLOYMENT ACTIONS

### Step 1: Document Deployment
- ✅ Record all container IDs and ports
- ✅ Document any configuration changes
- ✅ Save environment variable configurations
- ✅ Update DNS records if needed

### Step 2: Performance Baseline
```bash
# Create performance baseline measurements
curl -w "@curl-format.txt" -o /dev/null -s https://stg.bizoholic.com
curl -w "@curl-format.txt" -o /dev/null -s https://stg.coreldove.com
curl -w "@curl-format.txt" -o /dev/null -s https://stg.thrillring.com
```

### Step 3: Prepare Production Deployment
- ✅ Test all functionality in staging
- ✅ Create production environment variables
- ✅ Plan production domain switching strategy
- ✅ Prepare production deployment configurations

---

## 🎯 READY FOR PRODUCTION

Once staging verification passes **100%**, we'll be ready to proceed with:

1. **Production Infrastructure Project** (6 containers)
2. **Production Backend Services Project** (8 containers)
3. **Production Frontend Applications Project** (6 containers)
4. **Domain switching** from WordPress to new platform
5. **SSL certificate management** for production domains

**Total Production Deployment**: 40 containers (20 staging + 20 production) on single VPS

---

*Generated on October 11, 2025*
*Ready for immediate staging deployment execution*
*🤖 Generated with [Claude Code](https://claude.com/claude-code)*