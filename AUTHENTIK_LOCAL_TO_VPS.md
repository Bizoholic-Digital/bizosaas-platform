# 🔄 Unified Authentik Architecture - Local to VPS Implementation
## Single SSO Instance for Entire Platform

**Date**: 2025-12-11 14:30 IST  
**Goal**: Reuse existing VPS Authentik (sso.bizoholic.net) for all authentication

---

## 🎯 Current Architecture Discovery

### ✅ What Exists

**VPS Authentik Instance**:
- URL: `https://sso.bizoholic.net`
- Status: ✅ Running in production
- Used by: Client Portal (already integrated)
- Port: 9000 (HTTP), 9443 (HTTPS)

**Local Authentik Instance**:
- URL: `http://localhost:9000`
- Status: ✅ Running (just started)
- Port: 9000 (HTTP), 9443 (HTTPS)
- Docker Compose: `bizosaas-brain-core/docker-compose.authentik.yml`

**Client Portal Integration** (Already Working):
```typescript
// portals/client-portal/app/api/auth/[...nextauth]/route.ts
const AUTHENTIK_URL = process.env.AUTHENTIK_URL || 
                      process.env.NEXT_PUBLIC_SSO_URL || 
                      'https://sso.bizoholic.net';

AuthentikProvider({
    name: 'BizOSaaS SSO',
    clientId: process.env.AUTHENTIK_CLIENT_ID,
    clientSecret: process.env.AUTHENTIK_CLIENT_SECRET,
    issuer: `${AUTHENTIK_URL}/application/o/bizosaas/`,
})
```

---

## 📋 Unified Architecture Strategy

### Single Authentik for All Environments

```
┌────────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT WORKFLOW                        │
│                                                                │
│  Local Development                                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. Develop & Test Locally                               │  │
│  │     - Use local Authentik (localhost:9000)               │  │
│  │     - Configure applications                             │  │
│  │     - Test authentication flows                          │  │
│  │     - Test RBAC                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                    │
│                           ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  2. Export Authentik Configuration                       │  │
│  │     - Export applications                                │  │
│  │     - Export groups                                      │  │
│  │     - Export users (optional)                            │  │
│  │     - Export flows                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                    │
│                           ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  3. Push to GitHub                                       │  │
│  │     - Code changes                                       │  │
│  │     - Authentik configuration (YAML)                     │  │
│  │     - Environment templates                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                    │
│                           ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  4. CI/CD Pipeline (GitHub Actions)                      │  │
│  │     - Build Docker images                                │  │
│  │     - Run tests                                          │  │
│  │     - Deploy to VPS                                      │  │
│  │     - Apply Authentik configuration                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                    │
│                           ↓                                    │
│  VPS Production                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  5. Production Authentik (sso.bizoholic.net)             │  │
│  │     - Import configuration                               │  │
│  │     - Update redirect URIs for production                │  │
│  │     - Serve all applications                             │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Implementation Plan

### Phase 1: Local Development Setup (Today)

#### 1.1 Configure Local Authentik

**Access**: http://localhost:9000

**Create Applications**:
1. **Admin Dashboard** (bizosaas-admin)
   - Client ID: `bizosaas-admin-dashboard`
   - Redirect URI: `http://localhost:3004/api/auth/callback/authentik`
   
2. **Client Portal** (bizosaas) - if not exists
   - Client ID: `bizosaas-client-portal`
   - Redirect URI: `http://localhost:3003/api/auth/callback/authentik`

**Create Groups**:
- `super_admin`
- `platform_admin`
- `tenant_{id}_admin`
- `tenant_{id}_user`

**Create Test Users**:
- `superadmin` → `super_admin`
- `platformadmin` → `platform_admin`
- `testuser` → `tenant_test_user`

---

#### 1.2 Update Admin Dashboard Configuration

**File**: `portals/admin-dashboard/.env.local`

```env
# Authentik SSO Configuration (Local Development)
AUTHENTIK_URL=http://localhost:9000
NEXT_PUBLIC_SSO_URL=http://localhost:9000
AUTHENTIK_ISSUER=http://localhost:9000/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<from-authentik-local>
AUTH_SECRET=<generate-with-openssl-rand-base64-32>

# Brain Gateway
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://localhost:8000

# NextAuth
NEXTAUTH_URL=http://localhost:3004
NEXTAUTH_URL_INTERNAL=http://localhost:3004
```

---

#### 1.3 Test Local Authentication

```bash
# 1. Ensure Authentik is running
docker compose -f bizosaas-brain-core/docker-compose.authentik.yml ps

# 2. Start admin dashboard
cd portals/admin-dashboard
npm run dev

# 3. Test login
# Navigate to: http://localhost:3004
# Should redirect to: http://localhost:9000
# Login with test user
# Should redirect back to dashboard
```

---

### Phase 2: Export Authentik Configuration

#### 2.1 Export Applications

**Navigate to**: Authentik UI → System → Blueprints

**Create Blueprint**:
```yaml
# authentik-config/applications.yaml
version: 1
metadata:
  name: bizosaas-applications
entries:
  - model: authentik_providers_oauth2.oauth2provider
    identifiers:
      name: BizOSaaS Admin Dashboard Provider
    attrs:
      client_id: bizosaas-admin-dashboard
      client_type: confidential
      redirect_uris: |
        http://localhost:3004/api/auth/callback/authentik
        https://admin.bizoholic.net/api/auth/callback/authentik
      authorization_flow: !Find [authentik_flows.flow, [slug, default-provider-authorization-implicit-consent]]
      
  - model: authentik_core.application
    identifiers:
      slug: bizosaas-admin
    attrs:
      name: BizOSaaS Admin Dashboard
      provider: !Find [authentik_providers_oauth2.oauth2provider, [name, BizOSaaS Admin Dashboard Provider]]
```

---

#### 2.2 Export Groups

```yaml
# authentik-config/groups.yaml
version: 1
metadata:
  name: bizosaas-groups
entries:
  - model: authentik_core.group
    identifiers:
      name: super_admin
    attrs:
      is_superuser: true
      attributes:
        permissions: ["*"]
        access_level: platform
        
  - model: authentik_core.group
    identifiers:
      name: platform_admin
    attrs:
      is_superuser: false
      attributes:
        permissions: ["tenants:*", "monitoring:*", "analytics:*"]
        access_level: platform
```

---

### Phase 3: VPS Integration

#### 3.1 Access VPS Authentik

**URL**: https://sso.bizoholic.net

**Check Existing Configuration**:
1. Login to Authentik admin
2. Check Applications → Applications
3. Verify existing "BizOSaaS" or "bizosaas" application
4. Note Client ID and Client Secret

---

#### 3.2 Add Admin Dashboard to VPS Authentik

**Navigate to**: Applications → Providers → Create

**Create Provider**:
```
Name: BizOSaaS Admin Dashboard Provider
Client ID: bizosaas-admin-dashboard
Client Secret: <generate-and-save>
Redirect URIs:
  https://admin.bizoholic.net/api/auth/callback/authentik
  http://localhost:3004/api/auth/callback/authentik (for testing)
Scopes: openid, profile, email, groups
```

**Create Application**:
```
Name: BizOSaaS Admin Dashboard
Slug: bizosaas-admin
Provider: BizOSaaS Admin Dashboard Provider
Launch URL: https://admin.bizoholic.net
```

---

#### 3.3 Update VPS Environment Variables

**On VPS** (via Dokploy or direct):

**Admin Dashboard**:
```env
AUTHENTIK_URL=https://sso.bizoholic.net
NEXT_PUBLIC_SSO_URL=https://sso.bizoholic.net
AUTHENTIK_ISSUER=https://sso.bizoholic.net/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<from-vps-authentik>
AUTH_SECRET=<from-vault-or-secure-storage>

NEXTAUTH_URL=https://admin.bizoholic.net
NEXTAUTH_URL_INTERNAL=https://admin.bizoholic.net
```

---

### Phase 4: CI/CD Integration

#### 4.1 Create GitHub Workflow

**File**: `.github/workflows/deploy-admin-dashboard.yml`

```yaml
name: Deploy Admin Dashboard

on:
  push:
    branches: [main, develop]
    paths:
      - 'portals/admin-dashboard/**'
      - 'authentik-config/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker Image
        run: |
          cd portals/admin-dashboard
          docker build -t bizosaas-admin-dashboard:${{ github.sha }} .
      
      - name: Push to Registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker push bizosaas-admin-dashboard:${{ github.sha }}
      
      - name: Deploy to VPS
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /path/to/bizosaas
            docker pull bizosaas-admin-dashboard:${{ github.sha }}
            docker compose up -d admin-dashboard
      
      - name: Apply Authentik Configuration
        run: |
          # Import blueprints to VPS Authentik
          curl -X POST https://sso.bizoholic.net/api/v3/managed/blueprints/ \
            -H "Authorization: Bearer ${{ secrets.AUTHENTIK_API_TOKEN }}" \
            -F "file=@authentik-config/applications.yaml"
```

---

## 📊 Architecture Comparison

### Before (Current)
```
Local:
- Admin Dashboard → No SSO
- Client Portal → Local Authentik (maybe)

VPS:
- Client Portal → sso.bizoholic.net
- Admin Dashboard → Not deployed
```

### After (Target)
```
Local Development:
- Admin Dashboard → localhost:9000 (Authentik)
- Client Portal → localhost:9000 (Authentik)
- Test, develop, export config

VPS Production:
- Admin Dashboard → sso.bizoholic.net
- Client Portal → sso.bizoholic.net
- Same configuration, different URLs
```

---

## 🔄 Development Workflow

### Daily Development

```bash
# 1. Start local Authentik
cd bizosaas-brain-core
docker compose -f docker-compose.authentik.yml up -d

# 2. Develop admin dashboard
cd portals/admin-dashboard
npm run dev

# 3. Test authentication
# http://localhost:3004 → http://localhost:9000 → back to dashboard

# 4. Make changes
# - Update code
# - Test locally
# - Commit to git

# 5. Push to GitHub
git add .
git commit -m "feat: add admin dashboard feature"
git push origin main

# 6. CI/CD automatically deploys to VPS
# - Builds Docker image
# - Deploys to VPS
# - Updates Authentik configuration
```

---

## ✅ Implementation Checklist

### Local Setup
- [ ] Authentik running on localhost:9000
- [ ] Admin dashboard application created in local Authentik
- [ ] Groups created (super_admin, platform_admin)
- [ ] Test users created
- [ ] Admin dashboard .env.local updated
- [ ] Admin dashboard login working locally

### Configuration Export
- [ ] Applications exported to YAML
- [ ] Groups exported to YAML
- [ ] Flows exported (if customized)
- [ ] Configuration committed to git

### VPS Integration
- [ ] Access VPS Authentik (sso.bizoholic.net)
- [ ] Admin dashboard application created
- [ ] Production redirect URIs added
- [ ] Environment variables updated on VPS
- [ ] Admin dashboard deployed to VPS
- [ ] Production login working

### CI/CD
- [ ] GitHub workflow created
- [ ] Secrets configured
- [ ] Automatic deployment working
- [ ] Authentik config sync working

---

## 🎯 Next Steps (Priority Order)

### Step 1: Configure Local Authentik (30 min)
```bash
# Access: http://localhost:9000
# Follow: AUTHENTIK_SETUP_GUIDE.md
# Create: Admin dashboard application
# Create: Groups and users
# Test: Local authentication
```

### Step 2: Test Local Integration (15 min)
```bash
# Update: .env.local
# Start: npm run dev
# Test: http://localhost:3004
# Verify: SSO login working
```

### Step 3: Export Configuration (15 min)
```bash
# Export: Applications to YAML
# Export: Groups to YAML
# Commit: To git repository
```

### Step 4: VPS Integration (30 min)
```bash
# Access: https://sso.bizoholic.net
# Create: Admin dashboard application
# Update: VPS environment variables
# Deploy: Admin dashboard to VPS
# Test: Production login
```

### Step 5: CI/CD Setup (30 min)
```bash
# Create: GitHub workflow
# Configure: Secrets
# Test: Automatic deployment
```

**Total Time**: ~2 hours

---

## 📞 Quick Reference

**Local Authentik**: http://localhost:9000  
**VPS Authentik**: https://sso.bizoholic.net  
**Admin Dashboard (Local)**: http://localhost:3004  
**Admin Dashboard (VPS)**: https://admin.bizoholic.net  

**Documentation**:
- `AUTHENTIK_SETUP_GUIDE.md` - Step-by-step local setup
- `UNIFIED_AUTHENTIK_CONFIG.md` - Complete architecture
- This file - Local to VPS implementation

---

## 🎉 Benefits

✅ **Single SSO** for entire platform  
✅ **Consistent** authentication across environments  
✅ **Easy testing** locally before VPS deployment  
✅ **Automated deployment** via CI/CD  
✅ **Configuration as code** (YAML blueprints)  
✅ **No redundancy** - one Authentik per environment  
✅ **Better security** - centralized auth management  

---

**Ready to start?** 

1. Configure local Authentik: http://localhost:9000
2. Follow: `AUTHENTIK_SETUP_GUIDE.md`
3. Test locally
4. Deploy to VPS
