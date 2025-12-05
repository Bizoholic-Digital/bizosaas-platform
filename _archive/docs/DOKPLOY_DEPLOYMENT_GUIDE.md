# 🚀 Dokploy Deployment Guide - Staged Project Deployment

## 📋 STEP-BY-STEP DEPLOYMENT PROCESS

**Environment**: Staging
**Total Containers**: 20 (6 + 8 + 6)
**Projects**: 3 organized project groups
**Domains**: Staging subdomains with SSL

---

## 🎯 DEPLOYMENT PHASES

### **Phase 1: Infrastructure Project (6 containers)**
**Project Name**: `bizosaas-infrastructure-staging`
**Purpose**: Core infrastructure services
**Dependencies**: None (foundation layer)

### **Phase 2: Backend Services Project (8 containers)**
**Project Name**: `bizosaas-backend-staging`
**Purpose**: APIs and backend services
**Dependencies**: Infrastructure project must be running

### **Phase 3: Frontend Applications Project (6 containers)**
**Project Name**: `bizosaas-frontend-staging`
**Purpose**: Web applications with staging domains
**Dependencies**: Backend services must be running

---

## 🌐 ACCESS DOKPLOY DASHBOARD

### **Step 1: Connect to Dokploy**
```bash
# Access Dokploy dashboard
URL: http://194.238.16.237:3000
Username: [Your admin username]
Password: [Your admin password]
```

---

## 🏗️ PHASE 1: INFRASTRUCTURE PROJECT DEPLOYMENT

### **Create Infrastructure Project**
1. **Access Projects**: Click "Projects" in Dokploy dashboard
2. **Create New Project**:
   - Name: `bizosaas-infrastructure-staging`
   - Description: "Core infrastructure services for staging environment"
3. **Click Create Project**

### **Deploy Infrastructure Services**
1. **Enter Project**: Click on `bizosaas-infrastructure-staging`
2. **Add Application**: Click "New Application"
3. **Application Type**: Select "Docker Compose"
4. **Application Name**: `infrastructure-services`
5. **Upload Configuration**: Upload `dokploy-infrastructure-staging.yml`
6. **Environment Variables**: No additional variables needed
7. **Deploy**: Click "Deploy" button
8. **Wait**: Allow 5-10 minutes for deployment

### **Verify Infrastructure Deployment**
```bash
# Check container status
Expected containers:
- bizosaas-postgres-staging (Port 5432)
- bizosaas-redis-staging (Port 6379)
- bizosaas-vault-staging (Port 8200)
- bizosaas-temporal-server-staging (Port 7233)
- bizosaas-temporal-ui-staging (Port 8082)
- bizosaas-temporal-integration-staging (Port 8009)

# Health check commands (run on VPS)
curl http://194.238.16.237:8200/v1/sys/health  # Vault
curl http://194.238.16.237:8082  # Temporal UI
curl http://194.238.16.237:8009/health  # Temporal Integration
```

---

## 🔧 PHASE 2: BACKEND SERVICES PROJECT DEPLOYMENT

### **Create Backend Project**
1. **Back to Dashboard**: Return to main Dokploy dashboard
2. **Create New Project**:
   - Name: `bizosaas-backend-staging`
   - Description: "Backend services and APIs for staging environment"
3. **Click Create Project**

### **Deploy Backend Services**
1. **Enter Project**: Click on `bizosaas-backend-staging`
2. **Add Application**: Click "New Application"
3. **Application Type**: Select "Docker Compose"
4. **Application Name**: `backend-services`
5. **Upload Configuration**: Upload `dokploy-backend-staging.yml`
6. **Environment Variables**: Add required API keys:
   ```bash
   OPENROUTER_API_KEY=your_openrouter_api_key
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   STRIPE_SECRET_KEY=your_stripe_secret_key
   PAYPAL_CLIENT_ID=your_paypal_client_id
   PAYPAL_CLIENT_SECRET=your_paypal_client_secret
   AMAZON_ACCESS_KEY=your_amazon_access_key
   AMAZON_SECRET_KEY=your_amazon_secret_key
   ```
7. **Deploy**: Click "Deploy" button
8. **Wait**: Allow 10-15 minutes for deployment

### **Verify Backend Deployment**
```bash
# Check backend services
Expected containers:
- bizosaas-brain-staging (Port 8001) - Main API hub
- bizosaas-wagtail-staging (Port 8002)
- bizosaas-django-crm-staging (Port 8003)
- bizosaas-directory-api-staging (Port 8004)
- coreldove-backend-staging (Port 8005)
- bizosaas-ai-agents-staging (Port 8010)
- amazon-sourcing-staging (Port 8085)
- bizosaas-saleor-staging (Port 8000)

# Health check commands
curl http://194.238.16.237:8001/health  # Brain API (most important)
curl http://194.238.16.237:8003/health  # Django CRM
curl http://194.238.16.237:8005/health  # CorelDove API
```

---

## 📱 PHASE 3: FRONTEND APPLICATIONS PROJECT DEPLOYMENT

### **Create Frontend Project**
1. **Back to Dashboard**: Return to main Dokploy dashboard
2. **Create New Project**:
   - Name: `bizosaas-frontend-staging`
   - Description: "Frontend applications with staging domains"
3. **Click Create Project**

### **Deploy Frontend Applications**
1. **Enter Project**: Click on `bizosaas-frontend-staging`
2. **Add Application**: Click "New Application"
3. **Application Type**: Select "Docker Compose"
4. **Application Name**: `frontend-applications`
5. **Upload Configuration**: Upload `dokploy-frontend-staging.yml`
6. **Deploy**: Click "Deploy" button
7. **Wait**: Allow 10-15 minutes for deployment

---

## 🌐 CONFIGURE STAGING DOMAINS

### **DNS Configuration Required First**
```bash
# Add these DNS records to your domain provider
stg.bizoholic.com     A    194.238.16.237
stg.coreldove.com     A    194.238.16.237
stg.thrillring.com    A    194.238.16.237
```

### **Configure Domains in Dokploy**

#### **Bizoholic Staging Domain**
1. **Select Application**: Click on `bizoholic-frontend` in frontend project
2. **Domains Tab**: Click "Domains" tab
3. **Add Domain**:
   - **Host**: `stg.bizoholic.com`
   - **Path**: `/` (leave empty)
   - **Port**: `3000`
   - **HTTPS**: Enable
   - **Certificate**: Let's Encrypt
4. **Save Domain**

#### **CorelDove Staging Domain**
1. **Select Application**: Click on `coreldove-frontend`
2. **Add Domain**:
   - **Host**: `stg.coreldove.com`
   - **Path**: `/`
   - **Port**: `3002`
   - **HTTPS**: Enable
   - **Certificate**: Let's Encrypt
3. **Save Domain**

#### **ThrillRing Staging Domain**
1. **Select Application**: Click on `thrillring-gaming`
2. **Add Domain**:
   - **Host**: `stg.thrillring.com`
   - **Path**: `/`
   - **Port**: `3005`
   - **HTTPS**: Enable
   - **Certificate**: Let's Encrypt
3. **Save Domain**

#### **Client Portal Path Configuration**
1. **Select Application**: Click on `client-portal`
2. **Add Domain**:
   - **Host**: `stg.bizoholic.com`
   - **Path**: `/login`
   - **Internal Path**: `/`
   - **Port**: `3001`
   - **Strip Path**: Yes
   - **HTTPS**: Enable
3. **Save Domain**

#### **Admin Dashboard Path Configuration**
1. **Select Application**: Click on `admin-dashboard`
2. **Add Domain**:
   - **Host**: `stg.bizoholic.com`
   - **Path**: `/admin`
   - **Internal Path**: `/`
   - **Port**: `3009`
   - **Strip Path**: Yes
   - **HTTPS**: Enable
3. **Save Domain**

---

## ✅ VERIFICATION & TESTING

### **Container Status Verification**
1. **Check All Projects**: Verify all 3 projects show "Running" status
2. **Container Count**: Confirm 20 total containers across all projects
3. **Health Status**: All containers should show "Healthy" status

### **Domain Access Testing**
```bash
# Test all staging domains
curl -I https://stg.bizoholic.com
curl -I https://stg.coreldove.com
curl -I https://stg.thrillring.com
curl -I https://stg.bizoholic.com/login/
curl -I https://stg.bizoholic.com/admin/

# Expected response: HTTP/2 200 OK
```

### **SSL Certificate Verification**
```bash
# Check SSL certificates
openssl s_client -connect stg.bizoholic.com:443 -servername stg.bizoholic.com
openssl s_client -connect stg.coreldove.com:443 -servername stg.coreldove.com
openssl s_client -connect stg.thrillring.com:443 -servername stg.thrillring.com

# Look for: Verify return code: 0 (ok)
```

---

## 🔧 TROUBLESHOOTING

### **Common Issues & Solutions**

#### **Container Won't Start**
1. **Check Logs**: Click on container → Logs tab
2. **Verify Dependencies**: Ensure infrastructure is running first
3. **Environment Variables**: Verify all required API keys are set
4. **Resource Limits**: Check if VPS has sufficient resources

#### **Domain Not Accessible**
1. **DNS Propagation**: Check if DNS has propagated (use online DNS checkers)
2. **SSL Generation**: Wait 5-10 minutes for Let's Encrypt certificate
3. **Firewall**: Ensure ports 80/443 are open on VPS
4. **Traefik Config**: Verify Traefik labels are correct

#### **Internal Service Communication**
1. **Network**: Ensure all containers are on same network
2. **Service Names**: Use container names for internal communication
3. **Port Mapping**: Verify internal ports match container configuration

---

## 📊 DEPLOYMENT SUCCESS METRICS

### **Expected Results**
- ✅ **3 Projects Created**: Infrastructure, Backend, Frontend
- ✅ **20 Containers Running**: All containers healthy and operational
- ✅ **5 Domains Active**: 3 primary + 2 path-based routes
- ✅ **SSL Certificates**: All domains secured with HTTPS
- ✅ **API Connectivity**: All services communicating properly

### **Performance Benchmarks**
- **Page Load Time**: < 3 seconds
- **API Response Time**: < 500ms
- **SSL Grade**: A+ rating
- **Uptime**: 99.9%+

---

## 🎯 POST-DEPLOYMENT CHECKLIST

### **Functional Testing**
- [ ] Marketing website loads: `https://stg.bizoholic.com`
- [ ] E-commerce store works: `https://stg.coreldove.com`
- [ ] Gaming platform loads: `https://stg.thrillring.com`
- [ ] Client portal accessible: `https://stg.bizoholic.com/login/`
- [ ] Admin dashboard works: `https://stg.bizoholic.com/admin/`

### **Technical Validation**
- [ ] All 20 containers running and healthy
- [ ] SSL certificates active on all domains
- [ ] API routing through Brain API functioning
- [ ] Database connectivity verified
- [ ] Authentication flows working

### **Security Verification**
- [ ] HTTPS enforced on all domains
- [ ] No HTTP access allowed
- [ ] API authentication working
- [ ] Path traversal protection active
- [ ] CORS policies configured correctly

---

## 🚀 NEXT STEPS

### **1-2 Week Staging Testing Period**
- **Comprehensive Testing**: Test all features and user flows
- **Performance Monitoring**: Monitor response times and resource usage
- **Security Testing**: Conduct security audits and penetration testing
- **User Acceptance**: Get stakeholder approval for production migration

### **Production Migration Preparation**
- **DNS Planning**: Prepare production domain configuration
- **Environment Switch**: Update environment variables for production
- **Monitoring Setup**: Configure production monitoring and alerting
- **Backup Strategy**: Implement production backup procedures

**Staging deployment complete! Ready for comprehensive testing before production migration! 🎉**

---

*Generated on October 10, 2025*
*BizOSaaS Platform Development Team*
*🤖 Generated with [Claude Code](https://claude.com/claude-code)*