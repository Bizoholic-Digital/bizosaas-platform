# 🚀 Complete CI/CD Deployment Pipeline
## Local Docker → GitHub → VPS Staging → Production

**Updated**: September 28, 2025  
**GitHub Account**: `alagirirajesh`  
**Email**: `alagiri.rajesh@gmail.com`  
**VPS**: `194.238.16.237` (Hostinger with Dokploy)  

---

## 📋 **CURRENT STATUS**

### ✅ **Git Repository Status**
- **Local Repository**: 176 files committed (48,204+ lines)
- **GitHub Repository**: `https://github.com/alagirirajesh/bizoholic` (needs creation)
- **Branch**: `development` (ready to push)
- **Author**: Corrected to `alagiri.rajesh@gmail.com`

### ✅ **Platform Components Ready**
- **Amazon Sourcing Service**: Enhanced with verified India data
- **CorelDove Frontend**: Complete e-commerce storefront  
- **BizOSaaS Central Hub**: AI orchestration service
- **Docker Compose**: 20+ orchestration files
- **CI/CD Pipeline**: Comprehensive GitHub Actions workflow

---

## 🔧 **STEP 1: GITHUB REPOSITORY SETUP**

### **1.1 Create GitHub Repository**
```bash
# Manual steps required:
1. Go to https://github.com/alagirirajesh
2. Click "New Repository"
3. Repository name: "bizoholic"
4. Description: "BizOSaaS AI Marketing Automation Platform"
5. Set to Public
6. Initialize with README: No (we have existing code)
7. Click "Create repository"
```

### **1.2 Generate Personal Access Token**
```bash
# GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
1. Click "Generate new token (classic)"
2. Note: "BizOSaaS Platform Deployment"
3. Expiration: 90 days (or No expiration)
4. Scopes: ✅ repo, ✅ workflow, ✅ admin:repo_hook
5. Click "Generate token"
6. COPY the token immediately (shows only once)
```

### **1.3 Update Remote and Push**
```bash
# Replace placeholder token with actual token
git remote set-url origin https://alagirirajesh:YOUR_ACTUAL_TOKEN@github.com/alagirirajesh/bizoholic.git

# Push to GitHub
git push -u origin development

# Verify push
git log --oneline -3
# Should show: 563177c feat: comprehensive BizOSaaS platform foundation...
```

---

## 🏗️ **STEP 2: VPS DOKPLOY CONFIGURATION**

### **2.1 VPS Connection Setup**
```bash
# VPS Access Details (from credentials.md)
VPS_IP="194.238.16.237"
VPS_USER="root"
VPS_PASSWORD="&k3civYG5Q6YPb"

# SSH Connection
ssh root@194.238.16.237
# Password: &k3civYG5Q6YPb

# Verify Dokploy is running
curl -s http://194.238.16.237:3000/api/health
```

### **2.2 Dokploy Project Configuration**
```yaml
# Create dokploy-bizosaas.yml in repository root
version: "1.0"
name: "bizosaas-platform"
description: "BizOSaaS AI Marketing Automation Platform"

project:
  name: "bizosaas"
  environment: "staging"
  
applications:
  - name: "bizosaas-backend"
    type: "docker-compose"
    source:
      type: "git"
      repository: "https://github.com/bizoholic-alagiri/bizoholic.git"
      branch: "development"
      path: "."
    build:
      dockerfile: "docker-compose.unified.yml"
    domains:
      - domain: "api.bizoholic.com"
        service: "bizosaas-brain"
        port: 8001
        
  - name: "bizosaas-frontend"
    type: "docker-compose"
    source:
      type: "git" 
      repository: "https://github.com/bizoholic-alagiri/bizoholic.git"
      branch: "development"
      path: "bizosaas-platform/frontend"
    domains:
      - domain: "portal.bizoholic.com"
        service: "client-portal"
        port: 3006
      - domain: "coreldove.bizoholic.com"
        service: "coreldove-frontend"
        port: 3007

environment:
  POSTGRES_PASSWORD: "SharedInfra2024!SuperSecure"
  OPENAI_API_KEY: "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"
  DJANGO_SECRET_KEY: "django-super-secret-2025"
  NODE_ENV: "production"
  NEXT_PUBLIC_API_BASE_URL: "https://api.bizoholic.com"
```

### **2.3 Domain DNS Configuration**
```bash
# Configure DNS A Records (in your domain provider)
api.bizoholic.com     → 194.238.16.237
portal.bizoholic.com  → 194.238.16.237  
coreldove.bizoholic.com → 194.238.16.237
admin.bizoholic.com   → 194.238.16.237

# Verify DNS propagation
nslookup api.bizoholic.com
dig +short portal.bizoholic.com
```

---

## ⚙️ **STEP 3: AUTOMATED CI/CD PIPELINE**

### **3.1 GitHub Actions Secrets Configuration**
```bash
# GitHub Repository → Settings → Secrets and variables → Actions
# Add these secrets:

# VPS Access
VPS_HOST: "194.238.16.237"
VPS_USER: "root" 
VPS_PASSWORD: "&k3civYG5Q6YPb"

# Dokploy API
DOKPLOY_URL: "http://194.238.16.237:3000"
DOKPLOY_API_KEY: "VumUVyBHPJQUlXiGnwVxeyKYBeGOLOttGjkgkGiwpSHLiEYegUBkCSTPFmQqMbtC"

# Application Secrets
POSTGRES_PASSWORD: "SharedInfra2024!SuperSecure"
OPENAI_API_KEY: "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"
DJANGO_SECRET_KEY: "django-super-secret-2025"

# Monitoring
SLACK_WEBHOOK_URL: "https://hooks.slack.com/your-webhook-url"
```

### **3.2 Enhanced GitHub Actions Workflow**
The existing `.github/workflows/ci-cd.yml` already includes:
- ✅ Security scanning and dependency checks
- ✅ Backend and frontend testing
- ✅ Docker image building and pushing
- ✅ Staging deployment to K3s
- ✅ Production deployment with blue-green strategy
- ✅ Performance testing and monitoring
- ✅ Automated rollback capabilities

### **3.3 Dokploy Webhook Integration**
```bash
# Create webhook deployment script
cat > .github/scripts/deploy-to-dokploy.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 Deploying to Dokploy VPS..."

# Trigger Dokploy deployment
curl -X POST \
  "$DOKPLOY_URL/api/projects/bizosaas/deploy" \
  -H "Authorization: Bearer $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "development",
    "force": true,
    "cleanup": true
  }'

# Wait for deployment
echo "⏳ Waiting for deployment to complete..."
sleep 60

# Health check
echo "🔍 Running health checks..."
curl -f https://api.bizoholic.com/health || {
  echo "❌ Health check failed"
  exit 1
}

echo "✅ Deployment successful!"
EOF

chmod +x .github/scripts/deploy-to-dokploy.sh
```

---

## 🔄 **STEP 4: DEVELOPMENT WORKFLOW**

### **4.1 Local Development → Testing → Push**
```bash
# 1. Make changes in local Docker containers
cd /home/alagiri/projects/bizoholic
docker-compose up -d

# Test changes locally
curl http://localhost:8001/health
curl http://localhost:3007/api/health

# 2. Commit and push changes
git add .
git commit -m "feat: your feature description"
git push origin development
```

### **4.2 Automated Deployment Pipeline**
```yaml
# Triggered automatically on push to development branch:

1. Code Quality Checks (2-3 minutes)
   ├── Security scanning (Trivy, CodeQL)
   ├── Dependency vulnerability checks
   └── Linting and formatting

2. Testing Suite (5-8 minutes)
   ├── Backend unit tests (Python/FastAPI)
   ├── Frontend tests (Next.js/React)
   ├── AI agent integration tests
   └── WordPress plugin tests

3. Container Building (3-5 minutes)
   ├── Docker image builds for all services
   ├── Push to GitHub Container Registry
   └── Tag with commit SHA

4. Staging Deployment (2-3 minutes)
   ├── Deploy to VPS via Dokploy
   ├── Health checks and smoke tests
   └── Performance validation

5. Notification (30 seconds)
   ├── Slack notification with deployment status
   ├── Email alerts for failures
   └── GitHub deployment status updates
```

### **4.3 Production Promotion**
```bash
# Promote staging to production (manual trigger)
gh workflow run ci-cd.yml \
  --ref development \
  -f environment=production \
  -f skip_tests=false

# Or via GitHub UI:
# Actions → CI/CD Pipeline → Run workflow → Choose production
```

---

## 📊 **STEP 5: MONITORING & HEALTH CHECKS**

### **5.1 Automated Health Monitoring**
```bash
# Health check endpoints (configured in CI/CD)
https://api.bizoholic.com/health              # Central Hub API
https://portal.bizoholic.com/api/health       # Client Portal
https://coreldove.bizoholic.com/api/health    # E-commerce Frontend
https://admin.bizoholic.com/health            # Admin Dashboard

# Database and cache health
https://api.bizoholic.com/api/brain/db/health    # PostgreSQL
https://api.bizoholic.com/api/brain/cache/health # Redis
```

### **5.2 Performance Monitoring**
```yaml
# Automated performance tests in CI/CD
Load Testing:
  - k6 performance tests
  - 1000 concurrent users simulation
  - API response time validation (<200ms)
  
Stress Testing:
  - Database connection limits
  - Memory usage under load
  - CPU utilization tracking
  
Monitoring Stack:
  - Prometheus metrics collection
  - Grafana dashboards
  - Alert manager notifications
```

### **5.3 Backup and Recovery**
```bash
# Automated daily backups (via CI/CD cron)
Database Backup:
  - PostgreSQL dump to S3/BackBlaze
  - Redis snapshot backup
  - Retention: 30 days

Container Backup:
  - Docker image registry backup
  - Configuration backup
  - Environment variables backup (encrypted)

Recovery Testing:
  - Monthly automated recovery tests
  - RTO: 15 minutes (Recovery Time Objective)
  - RPO: 1 hour (Recovery Point Objective)
```

---

## 🎯 **COMPLETE DEPLOYMENT CHECKLIST**

### **Pre-Deployment**
- [ ] GitHub repository created with correct credentials
- [ ] GitHub Personal Access Token generated and configured
- [ ] VPS access verified (SSH to 194.238.16.237)
- [ ] Dokploy API access confirmed
- [ ] DNS records configured for all domains
- [ ] GitHub Actions secrets configured
- [ ] Local testing completed successfully

### **Deployment Execution**
- [ ] Push code to GitHub development branch
- [ ] Verify CI/CD pipeline execution
- [ ] Monitor deployment logs in GitHub Actions
- [ ] Confirm Dokploy deployment success
- [ ] Validate all health check endpoints
- [ ] Test core functionality (auth, payments, AI)
- [ ] Verify SSL certificates are active

### **Post-Deployment**
- [ ] Performance monitoring active
- [ ] Backup systems operational
- [ ] Error tracking and logging configured
- [ ] Team access and permissions verified
- [ ] Documentation updated with production URLs
- [ ] Customer communication (if applicable)

---

## 🚀 **IMMEDIATE NEXT STEPS**

1. **Create GitHub Repository**
   - Go to https://github.com/bizoholic-alagiri
   - Create "bizoholic" repository
   - Generate Personal Access Token

2. **Update Git Remote and Push**
   ```bash
   git remote set-url origin https://bizoholic-alagiri:YOUR_TOKEN@github.com/bizoholic-alagiri/bizoholic.git
   git push -u origin development
   ```

3. **Configure Dokploy Project**
   - Access Dokploy at dk.bizoholic.com
   - Create new project pointing to GitHub repo
   - Configure environment variables

4. **Test Complete Pipeline**
   - Make a small change locally
   - Commit and push to trigger CI/CD
   - Monitor deployment through to VPS

This establishes a complete professional development workflow:
**Local Docker → Git → GitHub → CI/CD → VPS Staging → Production**

---

*Pipeline Guide Version: 1.0 - September 28, 2025*  
*Status: Ready for Implementation*  
*Expected Setup Time: 2-4 hours*