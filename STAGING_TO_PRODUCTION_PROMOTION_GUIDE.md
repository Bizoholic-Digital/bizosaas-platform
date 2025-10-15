# 🚀 Staging to Production Promotion Guide

## 🎯 SINGLE VPS DEPLOYMENT PIPELINE

**Complete Pipeline**: `Local Containers → GitHub → Dokploy Staging → Dokploy Production`
**VPS**: `194.238.16.237` (Both staging and production)
**Dokploy**: `http://194.238.16.237:3000`

---

## 📊 DEPLOYMENT OVERVIEW

### **Container Distribution on Single VPS**
```
STAGING (20 containers):
├── Infrastructure (6) - Ports 5432, 6379, 8200, 7233, 8082, 8009
├── Backend (8)        - Ports 8001-8010, 8085
└── Frontend (6)       - Ports 3000-3005, 3009

PRODUCTION (20 containers):
├── Infrastructure (6) - Ports 5132, 6179, 8100, 7133, 8182, 8109
├── Backend (8)        - Ports 8101-8110, 8185
└── Frontend (6)       - Ports 3100-3105, 3109

TOTAL: 40 containers on single VPS
```

### **Domain Strategy**
```
STAGING DOMAINS:
- stg.bizoholic.com    → Staging marketing site
- stg.coreldove.com    → Staging e-commerce
- stg.thrillring.com   → Staging gaming platform

PRODUCTION DOMAINS:
- bizoholic.com        → Production marketing site
- coreldove.com        → Production e-commerce
- thrillring.com       → Production gaming platform

WORDPRESS PROTECTION:
- wp.bizoholic.com     → Current WordPress (protected)
- wp.coreldove.com     → Current WordPress (protected)
- wp.thrillring.com    → Current WordPress (protected)
```

---

## 🔄 COMPLETE DEPLOYMENT WORKFLOW

### **Phase 1: Local Development** (Daily)
```bash
# Developer workflow
1. Make changes to local containers
2. Test locally with docker-compose
3. Commit changes to GitHub
4. Push to main branch

# Local commands
docker-compose up -d  # Test locally
git add .
git commit -m "feat: new feature"
git push origin main
```

### **Phase 2: Automatic Staging Deployment** (5-10 minutes)
```bash
# Triggered automatically on GitHub push
1. GitHub webhook triggers Dokploy
2. Dokploy pulls latest code from GitHub
3. Dokploy builds containers from source
4. Deploy to staging projects:
   - bizosaas-infrastructure-staging
   - bizosaas-backend-staging
   - bizosaas-frontend-staging
5. Staging accessible at stg.* domains
```

### **Phase 3: Staging Testing** (Hours/Days)
```bash
# Manual and automated testing
1. Functional testing on staging
2. Performance testing
3. Security testing
4. User acceptance testing
5. Stakeholder approval
```

### **Phase 4: Production Promotion** (30-45 minutes)
```bash
# Manual or automated promotion
1. Tag release in GitHub
2. Trigger production deployment
3. Deploy to production projects:
   - bizosaas-infrastructure-production
   - bizosaas-backend-production
   - bizosaas-frontend-production
4. Production accessible at main domains
```

---

## 📋 STEP-BY-STEP STAGING DEPLOYMENT

### **Step 1: Configure DNS** (5 minutes)
```bash
# Add these DNS records to your DNS provider
stg.bizoholic.com     A    194.238.16.237
stg.coreldove.com     A    194.238.16.237
stg.thrillring.com    A    194.238.16.237

# Verify DNS propagation
dig stg.bizoholic.com
dig stg.coreldove.com
dig stg.thrillring.com
```

### **Step 2: Create Staging Projects in Dokploy** (20 minutes)

#### **2A: Infrastructure Project**
1. **Go to Dokploy**: `http://194.238.16.237:3000`
2. **Create Project**: Click "Projects" → "Create Project"
3. **Project Details**:
   - **Name**: `bizosaas-infrastructure-staging`
   - **Description**: `Infrastructure services for staging environment`
4. **Add Application**:
   - **Type**: Docker Compose
   - **Name**: `infrastructure-services`
   - **Source**: Upload File
   - **Upload**: `dokploy-infrastructure-github.yml`
5. **Deploy**: Click "Deploy" and wait 5-10 minutes

#### **2B: Backend Services Project**
1. **Create Project**: `bizosaas-backend-staging`
2. **Add Application**: Upload `dokploy-backend-github.yml`
3. **Environment Variables** (CRITICAL):
   ```
   OPENROUTER_API_KEY=your_staging_key
   OPENAI_API_KEY=your_staging_key
   ANTHROPIC_API_KEY=your_staging_key
   STRIPE_SECRET_KEY=your_test_key
   PAYPAL_CLIENT_ID=your_sandbox_id
   PAYPAL_CLIENT_SECRET=your_sandbox_secret
   AMAZON_ACCESS_KEY=your_staging_key
   AMAZON_SECRET_KEY=your_staging_key
   ```
4. **Deploy**: Wait 10-15 minutes

#### **2C: Frontend Applications Project**
1. **Create Project**: `bizosaas-frontend-staging`
2. **Add Application**: Upload `dokploy-frontend-github.yml`
3. **Deploy**: Wait 10-15 minutes
4. **Configure Domains**: SSL certificates auto-generated

### **Step 3: Verify Staging Deployment** (10 minutes)
```bash
# Test staging infrastructure
curl http://194.238.16.237:8200/v1/sys/health  # Vault
curl http://194.238.16.237:8082                # Temporal UI

# Test staging backend
curl http://194.238.16.237:8001/health         # Brain API
curl http://194.238.16.237:8005/health         # CorelDove Backend

# Test staging frontend
curl -I https://stg.bizoholic.com              # Marketing site
curl -I https://stg.coreldove.com              # E-commerce
curl -I https://stg.thrillring.com             # Gaming platform

# Complete verification
cd /home/alagiri/projects/bizoholic
./verify-all-20-containers.sh
```

---

## 🎯 PRODUCTION DEPLOYMENT PROCESS

### **Step 1: Prepare Production Environment** (15 minutes)

#### **Production Environment Variables**
```bash
# Production API keys (REAL keys, not test)
OPENROUTER_API_KEY_PRODUCTION=prod_key_here
OPENAI_API_KEY_PRODUCTION=prod_key_here
ANTHROPIC_API_KEY_PRODUCTION=prod_key_here

# Production payment keys (LIVE keys)
STRIPE_SECRET_KEY_PRODUCTION=sk_live_xxxxx
STRIPE_PUBLISHABLE_KEY_PRODUCTION=pk_live_xxxxx
PAYPAL_CLIENT_ID_PRODUCTION=live_client_id
PAYPAL_CLIENT_SECRET_PRODUCTION=live_secret

# Production analytics
GTM_ID_PRODUCTION=GTM-XXXXXXX
HOTJAR_ID_PRODUCTION=hotjar_id

# Production security
DJANGO_SECRET_KEY_PRODUCTION=super_secure_key
BASIC_AUTH_USERS=admin:encrypted_password
ADMIN_BASIC_AUTH_USERS=superadmin:encrypted_password
```

### **Step 2: Create Production Projects** (30 minutes)

#### **2A: Production Infrastructure**
1. **Create Project**: `bizosaas-infrastructure-production`
2. **Upload**: `dokploy-infrastructure-production.yml`
3. **Deploy**: Wait for 6 containers

#### **2B: Production Backend**
1. **Create Project**: `bizosaas-backend-production`
2. **Upload**: `dokploy-backend-production.yml`
3. **Add Environment Variables**: Production keys (above)
4. **Deploy**: Wait for 8 containers

#### **2C: Production Frontend**
1. **Create Project**: `bizosaas-frontend-production`
2. **Upload**: `dokploy-frontend-production.yml`
3. **Deploy**: Wait for 6 containers

### **Step 3: Configure Production Domains** (15 minutes)

#### **DNS Configuration**
```bash
# Point production domains to VPS
bizoholic.com         A    194.238.16.237
www.bizoholic.com     A    194.238.16.237
coreldove.com         A    194.238.16.237
www.coreldove.com     A    194.238.16.237
thrillring.com        A    194.238.16.237
www.thrillring.com    A    194.238.16.237

# Keep WordPress on subdomains
wp.bizoholic.com      A    194.238.16.237
wp.coreldove.com      A    194.238.16.237
wp.thrillring.com     A    194.238.16.237
```

#### **Traefik SSL Configuration**
- SSL certificates auto-generated by Let's Encrypt
- Production routing takes priority over staging
- WordPress sites remain accessible on wp.* subdomains

---

## 🔄 AUTOMATED PROMOTION WORKFLOW

### **GitHub Actions for Promotion**
```yaml
# .github/workflows/promote-to-production.yml
name: Promote to Production

on:
  workflow_dispatch:
    inputs:
      confirm_promotion:
        description: 'Type "PROMOTE" to confirm production deployment'
        required: true

jobs:
  promote:
    if: github.event.inputs.confirm_promotion == 'PROMOTE'
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Production Deployment
        run: |
          # Webhook to Dokploy production projects
          curl -X POST "${{ secrets.DOKPLOY_PRODUCTION_WEBHOOK }}"

      - name: Wait for Deployment
        run: sleep 600  # 10 minutes

      - name: Verify Production
        run: |
          curl -f https://bizoholic.com/api/health
          curl -f https://coreldove.com/api/health
          curl -f https://thrillring.com/api/health

      - name: Notify Team
        run: |
          # Send success notification
          echo "Production deployment successful!"
```

### **Manual Promotion Process**
```bash
# For manual promotion
1. Test staging thoroughly
2. Create GitHub release tag
3. Access Dokploy dashboard
4. Deploy production projects manually
5. Monitor deployment progress
6. Verify production health
7. Switch DNS if needed
```

---

## 📊 MONITORING AND VERIFICATION

### **Staging Monitoring**
```bash
# Staging health checks
curl http://194.238.16.237:8001/health  # Brain API
curl http://194.238.16.237:8200/v1/sys/health  # Vault
curl https://stg.bizoholic.com/api/health

# Staging logs
docker logs bizosaas-brain-staging
docker logs coreldove-backend-staging
```

### **Production Monitoring**
```bash
# Production health checks
curl http://194.238.16.237:8101/health  # Brain API (production port)
curl http://194.238.16.237:8100/v1/sys/health  # Vault (production port)
curl https://bizoholic.com/api/health

# Production logs
docker logs bizosaas-brain-production
docker logs coreldove-backend-production
```

### **Complete Platform Verification**
```bash
# Verify all 40 containers (20 staging + 20 production)
cd /home/alagiri/projects/bizoholic

# Create production verification script
cp verify-all-20-containers.sh verify-production-containers.sh
# Edit to use production ports (8101-8185 instead of 8001-8085)

# Run both verifications
./verify-all-20-containers.sh     # Staging
./verify-production-containers.sh  # Production
```

---

## 🔐 SECURITY CONSIDERATIONS

### **Staging Security**
- Test API keys (safe to expose in logs)
- Debug mode enabled
- Basic SSL (Let's Encrypt)
- Internal access for testing

### **Production Security**
- Live API keys (encrypted, never logged)
- Debug mode disabled
- Enhanced SSL with security headers
- Basic auth for admin areas
- Rate limiting enabled
- Production logging (no sensitive data)

### **Network Isolation**
```
STAGING NETWORK: bizosaas-staging-network
PRODUCTION NETWORK: bizosaas-production-network
WORDPRESS NETWORK: existing networks (untouched)
```

---

## ⚡ PERFORMANCE OPTIMIZATION

### **Single VPS Resource Management**
```
TOTAL VPS RESOURCES:
- CPU: 16+ cores recommended
- RAM: 32+ GB recommended
- Storage: 200+ GB recommended
- Network: High bandwidth for SSL and API calls

RESOURCE ALLOCATION:
- Staging: 30% of resources (testing environment)
- Production: 60% of resources (live environment)
- Existing Services: 10% of resources (WordPress, etc.)
```

### **Container Optimization**
```
SHARED RESOURCES:
✅ Docker daemon (single instance)
✅ Traefik proxy (handles all routing)
✅ Let's Encrypt (SSL for all domains)
✅ Base OS (shared kernel)

ISOLATED RESOURCES:
🔒 Container filesystems
🔒 Database schemas
🔒 Environment variables
🔒 Network namespaces
🔒 Log files
```

---

## 📈 SCALING STRATEGY

### **Current Setup (Single VPS)**
- 40 containers on one VPS
- Shared resources
- Cost-effective
- Good for MVP and early growth

### **Future Scaling Options**
```
OPTION 1: Vertical Scaling
- Upgrade VPS resources
- Add more CPU/RAM/Storage
- Keep single-server architecture

OPTION 2: Horizontal Scaling
- Separate staging and production VPS
- Load balancing across servers
- Database clustering

OPTION 3: Cloud Migration
- Move to Kubernetes
- Auto-scaling
- Multi-region deployment
```

---

## 🎯 SUCCESS CRITERIA

### **Staging Success**
- ✅ All 20 staging containers running
- ✅ All staging domains accessible (stg.*)
- ✅ All staging health checks passing
- ✅ SSL certificates valid
- ✅ Performance acceptable for testing

### **Production Success**
- ✅ All 20 production containers running
- ✅ All production domains accessible (main domains)
- ✅ All production health checks passing
- ✅ SSL certificates valid and secure
- ✅ Performance equal or better than WordPress
- ✅ WordPress sites still accessible (wp.*)

### **Complete Pipeline Success**
- ✅ 40 total containers running simultaneously
- ✅ Staging and production completely isolated
- ✅ Easy promotion from staging to production
- ✅ Zero downtime deployments
- ✅ Professional CI/CD workflow established

---

## 🚀 DEPLOYMENT TIMELINE

### **Week 1: Staging Setup**
- [x] DNS configuration (staging subdomains)
- [x] Staging project creation in Dokploy
- [ ] Staging deployment and testing
- [ ] Staging verification and optimization

### **Week 2: Staging Testing**
- [ ] Comprehensive functionality testing
- [ ] Performance testing
- [ ] Security testing
- [ ] User acceptance testing
- [ ] Bug fixes and optimization

### **Week 3: Production Preparation**
- [ ] Production environment variable setup
- [ ] Production project creation
- [ ] DNS configuration for production domains
- [ ] WordPress subdomain migration

### **Week 4: Production Deployment**
- [ ] Production deployment
- [ ] DNS switching for production domains
- [ ] Performance monitoring
- [ ] User migration from WordPress
- [ ] Production optimization

---

## 💰 COST ANALYSIS

### **Current Setup**
- **Infrastructure Cost**: $0 (using existing VPS)
- **Domain Cost**: ~$30/year for 3 domains
- **SSL Cost**: $0 (Let's Encrypt)
- **Total**: ~$30/year

### **Operational Benefits**
- Single VPS to manage
- Shared resource utilization
- No additional hosting costs
- Simplified backup and maintenance

---

## 🎉 CONCLUSION

**This optimized deployment strategy provides:**

✅ **Professional CI/CD Pipeline**: Local → GitHub → Staging → Production
✅ **Cost-Effective**: Single VPS for both environments
✅ **Safe Deployment**: Staging testing before production
✅ **WordPress Protection**: Existing sites remain safe
✅ **Scalable Architecture**: Can grow with your needs
✅ **Industry Standard**: Professional deployment workflow

**Ready to deploy your complete 40-container BizOSaaS platform!** 🚀

---

*Generated on October 11, 2025*
*Complete Single VPS Deployment Strategy*
*🤖 Generated with [Claude Code](https://claude.com/claude-code)*