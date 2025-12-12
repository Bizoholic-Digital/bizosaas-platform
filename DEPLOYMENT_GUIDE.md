# 🚀 Complete Deployment Guide - Local to VPS

**Date**: 2025-12-11 14:40 IST  
**Status**: Ready for Local Configuration → VPS Deployment

---

## ✅ What's Ready

### Files Created:
- ✅ `scripts/configure-authentik-local.sh` - Interactive local setup
- ✅ `.github/workflows/deploy-admin-dashboard.yml` - CI/CD pipeline
- ✅ `portals/admin-dashboard/Dockerfile` - Production build
- ✅ `docker-compose.admin-dashboard.yml` - VPS configuration
- ✅ `portals/admin-dashboard/next.config.js` - Updated for production

### Services Running:
- ✅ Local Authentik: http://localhost:9000
- ✅ VPS Authentik: https://sso.bizoholic.net
- ✅ Admin Dashboard: http://localhost:3004

---

## 📋 Step-by-Step Deployment

### PART 1: Local Configuration (30 minutes)

#### Step 1.1: Configure Local Authentik

**Option A: Manual Configuration**
```
1. Open browser: http://localhost:9000
2. Login or complete first-time setup
3. Follow the configuration in START_HERE_AUTHENTIK.md
```

**Option B: Use Helper Script**
```bash
cd /home/alagiri/projects/bizosaas-platform
./scripts/configure-authentik-local.sh
```

**What to Configure**:
1. **OAuth Provider**:
   - Name: BizOSaaS Admin Dashboard Provider
   - Client ID: `bizosaas-admin-dashboard`
   - Client Secret: <SAVE THIS>
   - Redirect URI: `http://localhost:3004/api/auth/callback/authentik`

2. **Application**:
   - Name: BizOSaaS Admin Dashboard
   - Slug: `bizosaas-admin`
   - Provider: BizOSaaS Admin Dashboard Provider

3. **Groups**:
   - `super_admin` (full access)
   - `platform_admin` (platform management)

4. **Test User**:
   - Username: `superadmin`
   - Email: `superadmin@bizosaas.local`
   - Group: `super_admin`

---

#### Step 1.2: Update Local Environment

**Create `.env.local`**:
```bash
cd portals/admin-dashboard
cp .env.example .env.local
```

**Edit `.env.local`** with values from Authentik:
```env
AUTHENTIK_URL=http://localhost:9000
NEXT_PUBLIC_SSO_URL=http://localhost:9000
AUTHENTIK_ISSUER=http://localhost:9000/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<from-authentik>
AUTH_SECRET=<generate-with-openssl-rand-base64-32>

NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3004
NEXTAUTH_URL_INTERNAL=http://localhost:3004
```

**Generate AUTH_SECRET**:
```bash
openssl rand -base64 32
```

---

#### Step 1.3: Test Local Authentication

**Restart Admin Dashboard**:
```bash
# Stop current server (Ctrl+C)
cd /home/alagiri/projects/bizosaas-platform/portals/admin-dashboard
npm run dev
```

**Test Login**:
1. Open: http://localhost:3004
2. Should redirect to login page
3. Click "Sign in with SSO"
4. Should redirect to: http://localhost:9000
5. Login with: `superadmin` / `<password>`
6. Should redirect back to dashboard

**Expected Result**: ✅ Logged in successfully!

---

### PART 2: Prepare for VPS Deployment (15 minutes)

#### Step 2.1: Create Production Environment Template

**Create `.env.production.template`**:
```bash
cd portals/admin-dashboard
cat > .env.production.template << 'EOF'
# Authentik SSO Configuration (Production)
AUTHENTIK_URL=https://sso.bizoholic.net
NEXT_PUBLIC_SSO_URL=https://sso.bizoholic.net
AUTHENTIK_ISSUER=https://sso.bizoholic.net/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<TO_BE_SET_ON_VPS>
AUTH_SECRET=<TO_BE_SET_ON_VPS>

# Brain Gateway
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.net

# Temporal UI
NEXT_PUBLIC_TEMPORAL_UI_URL=https://temporal.bizoholic.net

# Vault UI
NEXT_PUBLIC_VAULT_UI_URL=https://vault.bizoholic.net

# NextAuth
NEXTAUTH_URL=https://admin.bizoholic.net
NEXTAUTH_URL_INTERNAL=http://localhost:3004

# Environment
NODE_ENV=production
PORT=3004
EOF
```

---

#### Step 2.2: Commit Changes to Git

```bash
cd /home/alagiri/projects/bizosaas-platform

# Add all new files
git add .github/workflows/deploy-admin-dashboard.yml
git add portals/admin-dashboard/Dockerfile
git add portals/admin-dashboard/.env.production.template
git add docker-compose.admin-dashboard.yml
git add scripts/configure-authentik-local.sh
git add portals/admin-dashboard/next.config.js

# Commit
git commit -m "feat: add admin dashboard with Authentik SSO integration

- Add Dockerfile for production build
- Add GitHub Actions workflow for automated deployment
- Add docker-compose configuration for VPS
- Add Authentik configuration script
- Update next.config.js for standalone output
- Add production environment template"

# Push to GitHub
git push origin main
```

---

### PART 3: VPS Configuration (30 minutes)

#### Step 3.1: Configure VPS Authentik

**Access VPS Authentik**:
```
URL: https://sso.bizoholic.net
Login: <use credentials from credentials.md>
```

**Create Admin Dashboard Application**:
1. Navigate to: Applications → Providers → Create
2. Create OAuth2/OIDC Provider:
   - Name: BizOSaaS Admin Dashboard Provider
   - Client ID: `bizosaas-admin-dashboard`
   - Client Secret: <GENERATE AND SAVE>
   - Redirect URIs:
     - `https://admin.bizoholic.net/api/auth/callback/authentik`
     - `http://localhost:3004/api/auth/callback/authentik` (for testing)
   - Scopes: openid, profile, email, groups

3. Create Application:
   - Name: BizOSaaS Admin Dashboard
   - Slug: `bizosaas-admin`
   - Provider: BizOSaaS Admin Dashboard Provider
   - Launch URL: `https://admin.bizoholic.net`

4. **SAVE THE CLIENT SECRET!**

---

#### Step 3.2: Set Up VPS Environment

**SSH to VPS**:
```bash
ssh <user>@<vps-ip>
# Use credentials from credentials.md
```

**Create Environment File**:
```bash
cd /opt/bizosaas-platform
mkdir -p secrets

# Create .env file for admin dashboard
cat > secrets/admin-dashboard.env << 'EOF'
AUTHENTIK_URL=https://sso.bizoholic.net
NEXT_PUBLIC_SSO_URL=https://sso.bizoholic.net
AUTHENTIK_ISSUER=https://sso.bizoholic.net/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<PASTE_FROM_STEP_3.1>
AUTH_SECRET=<GENERATE_NEW>

NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.net
NEXT_PUBLIC_TEMPORAL_UI_URL=https://temporal.bizoholic.net
NEXT_PUBLIC_VAULT_UI_URL=https://vault.bizoholic.net

NEXTAUTH_URL=https://admin.bizoholic.net
NEXTAUTH_URL_INTERNAL=http://localhost:3004

NODE_ENV=production
PORT=3004
EOF

# Generate AUTH_SECRET
openssl rand -base64 32
# Add it to the .env file
```

---

#### Step 3.3: Configure GitHub Secrets

**Navigate to GitHub**:
```
https://github.com/<your-org>/bizosaas-platform/settings/secrets/actions
```

**Add Secrets**:
1. `VPS_HOST` - Your VPS IP or domain
2. `VPS_USER` - SSH username
3. `VPS_SSH_KEY` - Private SSH key for VPS access

---

### PART 4: Deploy to VPS (Automated)

#### Step 4.1: Trigger Deployment

**Option A: Automatic (on push to main)**
```bash
# Already done in Step 2.2
# GitHub Actions will automatically deploy
```

**Option B: Manual Trigger**
```
1. Go to: https://github.com/<your-org>/bizosaas-platform/actions
2. Select: "Deploy Admin Dashboard to VPS"
3. Click: "Run workflow"
4. Select branch: main
5. Click: "Run workflow"
```

---

#### Step 4.2: Monitor Deployment

**Watch GitHub Actions**:
```
https://github.com/<your-org>/bizosaas-platform/actions
```

**Check Logs**:
- Build step
- Push to registry
- Deploy to VPS
- Health check

---

#### Step 4.3: Verify Deployment

**Check VPS**:
```bash
ssh <user>@<vps-ip>

# Check if container is running
docker ps | grep admin-dashboard

# Check logs
docker logs bizosaas-admin-dashboard

# Check health
curl https://admin.bizoholic.net/api/health
```

**Test Login**:
```
1. Open: https://admin.bizoholic.net
2. Should redirect to: https://sso.bizoholic.net
3. Login with admin user
4. Should redirect back to dashboard
```

**Expected Result**: ✅ Admin dashboard live on VPS!

---

## 🎯 Success Checklist

### Local Setup
- [ ] Authentik running on localhost:9000
- [ ] Admin dashboard application configured
- [ ] Groups created (super_admin, platform_admin)
- [ ] Test user created
- [ ] .env.local updated
- [ ] Local login working

### Git & CI/CD
- [ ] All files committed to git
- [ ] Pushed to GitHub
- [ ] GitHub secrets configured
- [ ] Workflow file in place

### VPS Setup
- [ ] VPS Authentik application configured
- [ ] VPS environment file created
- [ ] Secrets properly set
- [ ] Docker network configured

### Deployment
- [ ] GitHub Actions workflow triggered
- [ ] Build successful
- [ ] Deployment successful
- [ ] Health check passed
- [ ] Production login working

---

## 🔧 Troubleshooting

### Issue: Local login not working
**Solution**:
```bash
# Check Authentik is running
docker ps | grep authentik

# Check redirect URI matches exactly
# In Authentik: http://localhost:3004/api/auth/callback/authentik
# In .env.local: NEXTAUTH_URL=http://localhost:3004
```

### Issue: VPS deployment fails
**Solution**:
```bash
# Check GitHub Actions logs
# Verify secrets are set correctly
# SSH to VPS and check docker logs
docker logs bizosaas-admin-dashboard
```

### Issue: Production login redirects incorrectly
**Solution**:
```bash
# Verify VPS Authentik redirect URI
# Should be: https://admin.bizoholic.net/api/auth/callback/authentik
# Check NEXTAUTH_URL in VPS environment
```

---

## 📊 Architecture Flow

```
┌─────────────────────────────────────────────────────────┐
│                  DEVELOPMENT FLOW                       │
│                                                         │
│  1. Configure Local Authentik                          │
│     ↓                                                   │
│  2. Test Locally (localhost:3004)                      │
│     ↓                                                   │
│  3. Commit & Push to GitHub                            │
│     ↓                                                   │
│  4. GitHub Actions Triggered                           │
│     ├─ Build Docker Image                              │
│     ├─ Push to Registry                                │
│     └─ Deploy to VPS                                   │
│     ↓                                                   │
│  5. VPS Running (admin.bizoholic.net)                  │
│     ├─ Uses sso.bizoholic.net                          │
│     └─ Same Authentik as client portal                 │
└─────────────────────────────────────────────────────────┘
```

---

## 🎉 Next Steps After Deployment

1. ✅ Test all authentication flows
2. ✅ Create additional admin users
3. ✅ Configure tenant groups
4. ✅ Set up monitoring
5. ✅ Configure backups
6. ✅ Document admin procedures

---

## 📞 Quick Reference

**Local**:
- Authentik: http://localhost:9000
- Admin Dashboard: http://localhost:3004

**VPS**:
- Authentik: https://sso.bizoholic.net
- Admin Dashboard: https://admin.bizoholic.net

**Documentation**:
- This file: Complete deployment guide
- `START_HERE_AUTHENTIK.md`: Quick start
- `AUTHENTIK_LOCAL_TO_VPS.md`: Architecture details

---

**Ready to deploy?** Start with Part 1: Local Configuration!
