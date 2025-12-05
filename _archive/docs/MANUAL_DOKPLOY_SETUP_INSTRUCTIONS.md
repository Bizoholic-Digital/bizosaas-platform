# 🚀 Manual Dokploy Setup Instructions

## 🎯 QUICK SETUP: Configure Dokploy with GitHub Integration

Since we can't push to GitHub due to secret scanning, here's how to manually configure Dokploy to deploy your 20 containers from your local setup:

---

## ⚡ IMMEDIATE ACTION PLAN

### **Option 1: Local File Upload to Dokploy (Fastest - 30 minutes)**

#### **Step 1: Access Dokploy Dashboard**
1. Go to: `http://194.238.16.237:3000`
2. Log in to your Dokploy dashboard

#### **Step 2: Create Infrastructure Project**
1. **Click "Projects"** → **"Create Project"**
2. **Project Name**: `bizosaas-infrastructure-staging`
3. **Description**: `Core infrastructure services for staging`
4. **Click "Create Project"**

5. **Add Application**:
   - **Click "New Application"**
   - **Type**: Docker Compose
   - **Name**: `infrastructure-services`
   - **Source**: Upload File
   - **Upload**: `/home/alagiri/projects/bizoholic/dokploy-infrastructure-github.yml`
   - **Click "Deploy"**

#### **Step 3: Create Backend Services Project**
1. **Create Project**: `bizosaas-backend-staging`
2. **Add Application**:
   - **Type**: Docker Compose
   - **Name**: `backend-services`
   - **Upload**: `/home/alagiri/projects/bizoholic/dokploy-backend-github.yml`

3. **IMPORTANT - Add Environment Variables**:
   ```
   OPENROUTER_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   STRIPE_SECRET_KEY=your_key_here
   PAYPAL_CLIENT_ID=your_key_here
   PAYPAL_CLIENT_SECRET=your_key_here
   AMAZON_ACCESS_KEY=your_key_here
   AMAZON_SECRET_KEY=your_key_here
   ```

4. **Click "Deploy"**

#### **Step 4: Create Frontend Applications Project**
1. **Create Project**: `bizosaas-frontend-staging`
2. **Add Application**:
   - **Type**: Docker Compose
   - **Name**: `frontend-applications`
   - **Upload**: `/home/alagiri/projects/bizoholic/dokploy-frontend-github.yml`
3. **Click "Deploy"**

#### **Step 5: Configure Staging Domains**
**CRITICAL**: Ensure DNS is configured first:
```
stg.bizoholic.com     A    194.238.16.237
stg.coreldove.com     A    194.238.16.237
stg.thrillring.com    A    194.238.16.237
```

---

### **Option 2: Modified Configs Without GitHub Build (Alternative)**

If Option 1 doesn't work due to GitHub context, use these modified configs:

#### **Infrastructure (No Changes Needed)**
Use existing: `dokploy-infrastructure-staging.yml`

#### **Backend (Use Local Images)**
Create `dokploy-backend-local.yml`:
```yaml
version: '3.8'
services:
  brain-api:
    image: bizosaas-brain-gateway:latest  # Use local image
    container_name: bizosaas-brain-staging
    ports:
      - "8001:8001"
    # ... rest of config same as dokploy-backend-github.yml

  coreldove-backend:
    image: coreldove-backend-coreldove-backend:latest
    # ... etc for all services
```

#### **Frontend (Use Local Images)**
Create `dokploy-frontend-local.yml`:
```yaml
version: '3.8'
services:
  bizoholic-frontend:
    image: bizoholic-frontend:dev  # Use local image
    container_name: bizoholic-frontend-staging
    ports:
      - "3000:3000"
    # ... rest of config same as dokploy-frontend-github.yml
```

---

## 📋 CONTAINER MAPPING

### **Current Local → Dokploy Staging**

#### **Infrastructure (6 containers)**
- `bizosaas-postgres-unified` → `bizosaas-postgres-staging`
- `bizosaas-redis-unified` → `bizosaas-redis-staging`
- `bizosaas-vault` → `bizosaas-vault-staging`
- `bizosaas-temporal-server` → `bizosaas-temporal-server-staging`
- `bizosaas-temporal-ui-server` → `bizosaas-temporal-ui-staging`
- `bizosaas-temporal-unified` → `bizosaas-temporal-integration-staging`

#### **Backend Services (8 containers)**
- `bizosaas-brain-unified` → `bizosaas-brain-staging`
- `bizosaas-wagtail-cms` → `bizosaas-wagtail-staging`
- `bizosaas-django-crm-8003` → `bizosaas-django-crm-staging`
- `bizosaas-business-directory-backend-8004` → `bizosaas-directory-api-staging`
- `coreldove-backend-8005` → `coreldove-backend-staging`
- `bizosaas-ai-agents-8010` → `bizosaas-ai-agents-staging`
- `amazon-sourcing-8085` → `amazon-sourcing-staging`
- `bizosaas-saleor-unified` → `bizosaas-saleor-staging`

#### **Frontend Applications (6 containers)**
- `bizoholic-frontend-3000` → `bizoholic-frontend-staging`
- `bizosaas-client-portal-3001` → `client-portal-staging`
- `coreldove-frontend-3002` → `coreldove-frontend-staging`
- `business-directory-3004` → `business-directory-staging`
- `thrillring-gaming-3005` → `thrillring-gaming-staging`
- `bizosaas-admin-3009` → `admin-dashboard-staging`

---

## ✅ VERIFICATION STEPS

### **After Each Project Deployment**

#### **Infrastructure Verification**
```bash
curl http://194.238.16.237:8200/v1/sys/health  # Vault
curl http://194.238.16.237:8082                # Temporal UI
curl http://194.238.16.237:8009/health         # Temporal Integration
```

#### **Backend Verification**
```bash
curl http://194.238.16.237:8001/health  # Brain API (CRITICAL)
curl http://194.238.16.237:8003/health  # Django CRM
curl http://194.238.16.237:8005/health  # CorelDove Backend
curl http://194.238.16.237:8010/health  # AI Agents
```

#### **Frontend Verification** (after DNS configured)
```bash
curl -I https://stg.bizoholic.com       # Marketing site
curl -I https://stg.coreldove.com       # E-commerce store
curl -I https://stg.thrillring.com      # Gaming platform
curl -I https://stg.bizoholic.com/login/  # Client portal
curl -I https://stg.bizoholic.com/admin/  # Admin dashboard
```

#### **Complete Verification**
```bash
cd /home/alagiri/projects/bizoholic
./verify-all-20-containers.sh
```

---

## 🔄 DEPLOYMENT FLOW

### **Successful Deployment Sequence**
```
1. Infrastructure Project (15-20 min)
   ↓ (wait for all 6 containers healthy)
2. Backend Services Project (20-30 min)
   ↓ (wait for all 8 containers healthy)
3. Frontend Applications Project (30-40 min)
   ↓ (configure domains and SSL)
4. Complete Verification (5-10 min)
```

### **Total Expected Time**: 70-100 minutes

---

## 🆘 TROUBLESHOOTING

### **Common Issues**

#### **"Build context not found" Error**
- **Solution**: Use Option 2 (local images) instead of GitHub build
- **Alternative**: Upload individual Dockerfiles to Dokploy

#### **"Container won't start" Error**
- **Check**: Dependencies are running (infrastructure → backend → frontend)
- **Check**: Environment variables are set correctly
- **Check**: Ports are available

#### **"Domain not accessible" Error**
- **Check**: DNS propagation with `dig stg.bizoholic.com`
- **Wait**: 5-30 minutes for DNS propagation
- **Check**: SSL certificate generation (automatic)

#### **"Health check failing" Error**
- **Check**: Service logs in Dokploy UI
- **Check**: Database connectivity
- **Check**: API keys are valid

---

## 📊 SUCCESS CRITERIA

### **Deployment Complete When:**
- ✅ All 20 containers show "Running" status in Dokploy
- ✅ All health checks return HTTP 200
- ✅ All staging domains accessible via HTTPS
- ✅ SSL certificates valid (green padlock)
- ✅ `verify-all-20-containers.sh` passes 100%
- ✅ WordPress production sites still working

---

## 🎯 NEXT STEPS AFTER STAGING SUCCESS

### **Week 1-2: Staging Testing**
- Comprehensive functionality testing
- Performance testing
- Security testing
- User acceptance testing

### **Week 3: Production Migration**
- Create production Dokploy projects
- Update domains (remove `stg.` prefix)
- Switch environment variables to production
- Enable monitoring and analytics

### **Ongoing: Automated Pipeline**
- Set up GitHub webhooks for auto-deployment
- Configure automated testing
- Implement blue-green deployment
- Set up monitoring and alerting

---

## 💡 RECOMMENDATIONS

### **For Best Results:**
1. **Start with Option 1** (GitHub build) if possible
2. **Fall back to Option 2** (local images) if needed
3. **Configure DNS first** before frontend deployment
4. **Deploy sequentially** (Infrastructure → Backend → Frontend)
5. **Verify each phase** before proceeding to next
6. **Keep WordPress sites untouched** during deployment

### **After Successful Staging:**
1. **Test thoroughly** for 1-2 weeks
2. **Document any issues** and fixes
3. **Plan production migration** carefully
4. **Set up monitoring** and alerting
5. **Train team** on new deployment process

---

## ✅ READY TO PROCEED

**You now have everything needed to deploy your 20 containers to Dokploy staging!**

**Files ready for upload:**
- `dokploy-infrastructure-github.yml` (or `dokploy-infrastructure-staging.yml`)
- `dokploy-backend-github.yml` (or create `dokploy-backend-local.yml`)
- `dokploy-frontend-github.yml` (or create `dokploy-frontend-local.yml`)

**Start with Infrastructure project and work your way up!** 🚀

---

*Generated on October 11, 2025*
*Manual Dokploy Setup Guide*
*🤖 Generated with [Claude Code](https://claude.com/claude-code)*