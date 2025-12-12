# 🧪 Local Testing & Deployment Workflow

**Date**: 2025-12-11 15:00 IST  
**Goal**: Test locally → Fix issues → Deploy to VPS via Dokploy

---

## 📋 Phase 1: Local Testing (Now)

### Step 1: Configure Local Authentik

**Access Authentik**:
```
URL: http://localhost:9000
```

**Manual Configuration Steps**:

#### 1.1 Login to Authentik
- If first time: Complete setup wizard
- Username: `akadmin` (default)
- Create admin password

#### 1.2 Create OAuth Provider
```
Navigate to: Applications → Providers → Create
Click: OAuth2/OpenID Provider

Fill in:
- Name: BizOSaaS Admin Dashboard Provider
- Authorization flow: default-provider-authorization-implicit-consent
- Client type: Confidential
- Client ID: bizosaas-admin-dashboard
- Client Secret: <Click "Generate" - SAVE THIS!>
- Redirect URIs/Origins (REGEX):
  http://localhost:3004/api/auth/callback/authentik
  
Advanced Protocol Settings:
- Scopes: Select all of:
  - openid
  - profile
  - email
  - groups (if available, or add manually)
- Subject mode: Based on the User's hashed ID
- Include claims in id_token: ✓ (checked)

Click: Create
```

**IMPORTANT**: Copy the Client Secret immediately!

#### 1.3 Create Application
```
Navigate to: Applications → Applications → Create

Fill in:
- Name: BizOSaaS Admin Dashboard
- Slug: bizosaas-admin
- Provider: BizOSaaS Admin Dashboard Provider (select from dropdown)
- Launch URL: http://localhost:3004

Click: Create
```

#### 1.4 Create Groups
```
Navigate to: Directory → Groups

Create Group 1:
- Click: Create
- Name: super_admin
- Is superuser: ✓ (checked)
- Attributes (click "Add entry" if needed):
  {
    "permissions": ["*"],
    "access_level": "platform"
  }
- Click: Create

Create Group 2:
- Click: Create
- Name: platform_admin
- Is superuser: ✗ (unchecked)
- Attributes:
  {
    "permissions": ["tenants:*", "monitoring:*", "analytics:*"],
    "access_level": "platform"
  }
- Click: Create
```

#### 1.5 Create Test User
```
Navigate to: Directory → Users → Create

Fill in:
- Username: superadmin
- Name: Super Administrator
- Email: superadmin@bizosaas.local
- Is active: ✓ (checked)

Click on "Set password" tab:
- Password: <choose-strong-password>
- Confirm password: <same-password>

Click on "Groups" tab:
- Select: super_admin
- Click: Add

Click: Create
```

**Save these credentials**:
- Username: `superadmin`
- Password: `<your-password>`

---

### Step 2: Update Admin Dashboard Environment

**Create .env.local**:
```bash
cd /home/alagiri/projects/bizosaas-platform/portals/admin-dashboard
cp .env.example .env.local
```

**Generate AUTH_SECRET**:
```bash
openssl rand -base64 32
```

**Edit .env.local** (replace placeholders):
```env
# Authentik SSO Configuration (Local Development)
AUTHENTIK_URL=http://localhost:9000
NEXT_PUBLIC_SSO_URL=http://localhost:9000
AUTHENTIK_ISSUER=http://localhost:9000/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<PASTE_CLIENT_SECRET_FROM_STEP_1.2>
AUTH_SECRET=<PASTE_OUTPUT_FROM_OPENSSL_COMMAND>

# Brain Gateway
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://localhost:8000

# Temporal UI
NEXT_PUBLIC_TEMPORAL_UI_URL=http://localhost:8233

# Vault UI  
NEXT_PUBLIC_VAULT_UI_URL=http://localhost:8200

# Environment
NODE_ENV=development

# Port
PORT=3004

# NextAuth URL
NEXTAUTH_URL=http://localhost:3004
NEXTAUTH_URL_INTERNAL=http://localhost:3004
```

---

### Step 3: Test Admin Dashboard Locally

**Restart Admin Dashboard**:
```bash
# Stop current server (Ctrl+C in the terminal)
cd /home/alagiri/projects/bizosaas-platform/portals/admin-dashboard
npm run dev
```

**Test Authentication Flow**:
```
1. Open browser: http://localhost:3004
2. Should redirect to: http://localhost:3004/login
3. Click: "Sign in with SSO" button
4. Should redirect to: http://localhost:9000/...
5. Login with:
   - Username: superadmin
   - Password: <your-password>
6. Should redirect back to: http://localhost:3004
7. Should see: Admin dashboard with user info
```

**Expected Result**: ✅ Successfully logged in!

---

### Step 4: Test RBAC & Features

**Test 1: Super Admin Access**
```
- Should see full dashboard
- Check navigation menu
- Verify all sections accessible
```

**Test 2: User Info Display**
```
- Check if user name is displayed
- Verify role is shown correctly
- Check if logout works
```

**Test 3: Protected Routes**
```
- Try accessing /dashboard directly
- Should require authentication
- Unauthorized users should see access denied
```

---

## 🔧 Troubleshooting Local Issues

### Issue 1: "Redirect URI mismatch"
**Solution**:
```
1. Check Authentik provider settings
2. Verify redirect URI is exactly: http://localhost:3004/api/auth/callback/authentik
3. No trailing slash
4. Check .env.local NEXTAUTH_URL matches
```

### Issue 2: "Invalid client"
**Solution**:
```
1. Verify Client ID in .env.local matches Authentik
2. Verify Client Secret is correct (no extra spaces)
3. Restart admin dashboard after .env.local changes
```

### Issue 3: "Access Denied" for admin user
**Solution**:
```
1. Check user is in super_admin or platform_admin group
2. Verify group names match exactly (case-sensitive)
3. Check middleware.ts for role checking logic
```

### Issue 4: Login redirects to wrong URL
**Solution**:
```
1. Check NEXTAUTH_URL in .env.local
2. Should be: http://localhost:3004
3. Check AUTHENTIK_ISSUER ends with /application/o/bizosaas-admin/
```

---

## 📋 Phase 2: Prepare for VPS Deployment

### Step 5: Fix Any Local Issues

**Document all fixes**:
```
- List of issues encountered
- Solutions applied
- Code changes made
- Configuration updates
```

**Test again after fixes**:
```
- Clear browser cache
- Restart admin dashboard
- Test full authentication flow
- Verify all features work
```

---

### Step 6: Commit Changes to Git

**Check what's changed**:
```bash
cd /home/alagiri/projects/bizosaas-platform
git status
```

**Add all files**:
```bash
git add .github/workflows/deploy-admin-dashboard.yml
git add portals/admin-dashboard/Dockerfile
git add portals/admin-dashboard/lib/
git add portals/admin-dashboard/app/
git add portals/admin-dashboard/types/
git add portals/admin-dashboard/middleware.ts
git add portals/admin-dashboard/next.config.js
git add portals/admin-dashboard/.env.example
git add docker-compose.admin-dashboard.yml
git add scripts/configure-authentik-local.sh
git add DEPLOYMENT_GUIDE.md
git add READY_TO_DEPLOY.md
git add AUTHENTIK_*.md
git add START_HERE_AUTHENTIK.md

# Don't add .env.local (it's gitignored)
```

**Commit**:
```bash
git commit -m "feat: add admin dashboard with Authentik SSO integration

- Implement NextAuth + Authentik SSO
- Add RBAC middleware (super_admin, platform_admin)
- Create login and unauthorized pages
- Add API client with JWT authentication
- Create production Dockerfile
- Add GitHub Actions deployment workflow
- Add docker-compose for VPS deployment
- Add comprehensive documentation
- Tested locally and working

Closes #<issue-number-if-any>"
```

**Push to GitHub**:
```bash
git push origin main
```

---

## 📋 Phase 3: Deploy to VPS via Dokploy

### Step 7: Configure VPS Authentik

**Access VPS Authentik**:
```
URL: https://sso.bizoholic.net
Login: <use credentials from credentials.md>
```

**Create Admin Dashboard Application** (same as local, but different URLs):

#### 7.1 Create OAuth Provider
```
Navigate to: Applications → Providers → Create
Type: OAuth2/OpenID Provider

Fill in:
- Name: BizOSaaS Admin Dashboard Provider
- Client ID: bizosaas-admin-dashboard
- Client Secret: <Generate - SAVE THIS!>
- Redirect URIs:
  https://admin\.bizoholic\.net/api/auth/callback/authentik
  http://localhost:3004/api/auth/callback/authentik (for testing)
- Scopes: openid, profile, email, groups

Click: Create
```

#### 7.2 Create Application
```
Navigate to: Applications → Applications → Create

Fill in:
- Name: BizOSaaS Admin Dashboard
- Slug: bizosaas-admin
- Provider: BizOSaaS Admin Dashboard Provider
- Launch URL: https://admin.bizoholic.net

Click: Create
```

**SAVE THE CLIENT SECRET!**

---

### Step 8: Deploy via Dokploy UI

**Access Dokploy**:
```
URL: <your-dokploy-url>
Login: <your-credentials>
```

**Create New Service**:
```
1. Click: "Create Service" or "Add Application"
2. Type: Docker Compose or Git Repository
3. Name: bizosaas-admin-dashboard
```

**Configure Git Repository** (if using Git deploy):
```
Repository: https://github.com/<your-org>/bizosaas-platform
Branch: main
Build Context: ./portals/admin-dashboard
Dockerfile: Dockerfile
```

**Or Upload docker-compose.admin-dashboard.yml**:
```
1. Copy content of docker-compose.admin-dashboard.yml
2. Paste in Dokploy compose editor
3. Update image name if needed
```

**Set Environment Variables**:
```
AUTHENTIK_URL=https://sso.bizoholic.net
NEXT_PUBLIC_SSO_URL=https://sso.bizoholic.net
AUTHENTIK_ISSUER=https://sso.bizoholic.net/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<FROM_STEP_7.1>
AUTH_SECRET=<GENERATE_NEW_WITH_OPENSSL>

NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.net
NEXT_PUBLIC_TEMPORAL_UI_URL=https://temporal.bizoholic.net
NEXT_PUBLIC_VAULT_UI_URL=https://vault.bizoholic.net

NEXTAUTH_URL=https://admin.bizoholic.net
NEXTAUTH_URL_INTERNAL=http://localhost:3004

NODE_ENV=production
PORT=3004
```

**Configure Domain**:
```
Domain: admin.bizoholic.net
SSL: Enable (Let's Encrypt)
```

**Deploy**:
```
1. Click: "Deploy" or "Start"
2. Monitor logs
3. Wait for deployment to complete
```

---

### Step 9: Verify VPS Deployment

**Check Deployment**:
```
1. Open: https://admin.bizoholic.net
2. Should redirect to: https://sso.bizoholic.net
3. Login with admin user
4. Should redirect back to: https://admin.bizoholic.net
5. Verify dashboard loads correctly
```

**Check Logs** (in Dokploy):
```
- Look for any errors
- Verify NextAuth is working
- Check Authentik connection
```

**Test Features**:
```
- Navigation works
- User info displayed
- Logout works
- Re-login works
```

---

## ✅ Success Checklist

### Local Testing
- [ ] Authentik configured (localhost:9000)
- [ ] Admin dashboard application created
- [ ] Groups created (super_admin, platform_admin)
- [ ] Test user created
- [ ] .env.local updated
- [ ] Local login working
- [ ] Dashboard accessible
- [ ] All features tested
- [ ] No errors in console

### Git & Deployment
- [ ] All changes committed
- [ ] Pushed to GitHub
- [ ] No sensitive data in git

### VPS Deployment
- [ ] VPS Authentik configured
- [ ] Admin dashboard application created
- [ ] Environment variables set in Dokploy
- [ ] Domain configured
- [ ] SSL enabled
- [ ] Deployed successfully
- [ ] Production login working
- [ ] Dashboard accessible
- [ ] No errors in logs

---

## 🎯 Current Status

**Ready for**: Local testing  
**Next Step**: Configure Authentik at http://localhost:9000  
**Time Required**: 30-45 minutes  

---

## 📞 Quick Commands

**Open Authentik**:
```bash
# Check if running
docker ps | grep authentik

# If not running
cd bizosaas-brain-core
docker compose -f docker-compose.authentik.yml up -d

# Open in browser
open http://localhost:9000
```

**Generate AUTH_SECRET**:
```bash
openssl rand -base64 32
```

**Start Admin Dashboard**:
```bash
cd portals/admin-dashboard
npm run dev
```

**Test Login**:
```
http://localhost:3004
```

---

**Ready to start?** Let's configure Authentik first! 🚀
