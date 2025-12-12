# 🎯 Authentik Configuration Guide - Step by Step
## Configure Admin Dashboard & Client Portal SSO

**Date**: 2025-12-11 13:52 IST  
**Status**: ✅ Authentik Running - Ready for Configuration

---

## ✅ Current Status

```
✓ Authentik Server:    HEALTHY (Port 9000)
✓ Authentik Worker:    HEALTHY
✓ Authentik Postgres:  HEALTHY
✓ Authentik Redis:     HEALTHY
✓ Admin Dashboard:     RUNNING (Port 3004)
```

**Access Authentik**: http://localhost:9000

---

## 📋 Configuration Steps

### Step 1: Initial Authentik Setup (First Time Only)

**Navigate to**: http://localhost:9000

**First Time Setup**:
1. You'll see the Authentik setup wizard
2. Create admin account:
   - Email: `admin@bizosaas.local`
   - Username: `akadmin`
   - Password: `<choose-strong-password>`
3. Complete the setup wizard

**If Already Setup**:
- Login with existing admin credentials
- Default username: `akadmin`

---

### Step 2: Create Admin Dashboard Application

#### 2.1 Create OAuth2/OIDC Provider

**Navigate to**: Applications → Providers → Create

**Click**: "Create" button

**Select**: "OAuth2/OpenID Provider"

**Fill in the form**:
```
Name: BizOSaaS Admin Dashboard Provider
Authorization flow: default-provider-authorization-implicit-consent
Client type: Confidential
Client ID: bizosaas-admin-dashboard
Client Secret: <click "Generate" button and SAVE THIS>
Redirect URIs/Origins (REGEX):
  http://localhost:3004/api/auth/callback/authentik
  https://admin\.bizoholic\.net/api/auth/callback/authentik

Signing Key: authentik Self-signed Certificate
```

**Advanced settings**:
```
Scopes: openid, profile, email, groups (select from dropdown)
Subject mode: Based on the User's hashed ID
Include claims in id_token: ✓ (checked)
```

**Click**: "Create"

**IMPORTANT**: Copy and save the Client Secret! You'll need it for .env.local

---

#### 2.2 Create Application

**Navigate to**: Applications → Applications → Create

**Fill in the form**:
```
Name: BizOSaaS Admin Dashboard
Slug: bizosaas-admin
Group: <leave empty or create "BizOSaaS" group>
Provider: BizOSaaS Admin Dashboard Provider (select from dropdown)
Launch URL: http://localhost:3004
```

**Click**: "Create"

---

### Step 3: Verify/Create Client Portal Application

#### 3.1 Check if Client Portal App Exists

**Navigate to**: Applications → Applications

**Look for**: Application with slug "bizosaas" or name containing "Client Portal"

**If EXISTS**:
1. Click on the application
2. Note the Provider
3. Click on the Provider
4. Note the Client ID and Client Secret
5. Verify Redirect URIs include:
   - `http://localhost:3003/api/auth/callback/authentik`
   - `https://app.bizoholic.net/api/auth/callback/authentik`

**If NOT EXISTS**: Create similar to Step 2, but with:
```
Provider Name: BizOSaaS Client Portal Provider
Client ID: bizosaas-client-portal
Redirect URIs:
  http://localhost:3003/api/auth/callback/authentik
  https://app\.bizoholic\.net/api/auth/callback/authentik

Application Name: BizOSaaS Client Portal
Slug: bizosaas
Launch URL: http://localhost:3003
```

---

### Step 4: Create Groups

**Navigate to**: Directory → Groups → Create

#### 4.1 Super Admin Group

**Click**: "Create" button

**Fill in**:
```
Name: super_admin
Is superuser: ✓ (checked)
Parent: <leave empty>
```

**Attributes** (click "Add entry"):
```json
{
  "permissions": ["*"],
  "access_level": "platform",
  "can_manage_tenants": true,
  "can_configure_agents": true
}
```

**Click**: "Create"

---

#### 4.2 Platform Admin Group

**Click**: "Create" button

**Fill in**:
```
Name: platform_admin
Is superuser: ✗ (unchecked)
Parent: <leave empty>
```

**Attributes**:
```json
{
  "permissions": ["tenants:*", "monitoring:*", "analytics:*"],
  "access_level": "platform",
  "can_manage_tenants": true,
  "can_configure_agents": false
}
```

**Click**: "Create"

---

#### 4.3 Tenant Admin Group (Example)

**Click**: "Create" button

**Fill in**:
```
Name: tenant_acme_admin
Is superuser: ✗ (unchecked)
Parent: <leave empty>
```

**Attributes**:
```json
{
  "tenant_id": "acme",
  "permissions": ["tenant:manage", "users:manage", "integrations:manage"],
  "access_level": "tenant",
  "can_manage_users": true
}
```

**Click**: "Create"

---

#### 4.4 Tenant User Group (Example)

**Click**: "Create" button

**Fill in**:
```
Name: tenant_acme_user
Is superuser: ✗ (unchecked)
Parent: <leave empty>
```

**Attributes**:
```json
{
  "tenant_id": "acme",
  "permissions": ["tenant:view", "dashboard:view"],
  "access_level": "tenant",
  "can_manage_users": false
}
```

**Click**: "Create"

---

### Step 5: Create Test Users

**Navigate to**: Directory → Users → Create

#### 5.1 Super Admin User

**Click**: "Create" button

**Fill in**:
```
Username: superadmin
Name: Super Administrator
Email: superadmin@bizosaas.local
Is active: ✓ (checked)
Path: users
```

**Set Password**:
- Click "Set password" tab
- Password: `<choose-strong-password>`
- Confirm password: `<same-password>`

**Groups**:
- Click "Groups" tab
- Select: `super_admin`
- Click "Add"

**Click**: "Create"

---

#### 5.2 Platform Admin User

**Click**: "Create" button

**Fill in**:
```
Username: platformadmin
Name: Platform Administrator
Email: platformadmin@bizosaas.local
Is active: ✓ (checked)
```

**Set Password**: `<choose-strong-password>`

**Groups**: `platform_admin`

**Click**: "Create"

---

#### 5.3 Tenant Admin User

**Click**: "Create" button

**Fill in**:
```
Username: acmeadmin
Name: Acme Administrator
Email: admin@acme.com
Is active: ✓ (checked)
```

**Set Password**: `<choose-strong-password>`

**Groups**: `tenant_acme_admin`

**Click**: "Create"

---

#### 5.4 Tenant User

**Click**: "Create" button

**Fill in**:
```
Username: acmeuser
Name: Acme User
Email: user@acme.com
Is active: ✓ (checked)
```

**Set Password**: `<choose-strong-password>`

**Groups**: `tenant_acme_user`

**Click**: "Create"

---

### Step 6: Update Admin Dashboard Environment

**Open terminal**:
```bash
cd /home/alagiri/projects/bizosaas-platform/portals/admin-dashboard
cp .env.example .env.local
```

**Edit `.env.local`**:
```env
# Authentik SSO Configuration (Same instance as client portal)
AUTHENTIK_URL=http://localhost:9000
NEXT_PUBLIC_SSO_URL=http://localhost:9000
AUTHENTIK_ISSUER=http://localhost:9000/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<PASTE-CLIENT-SECRET-FROM-STEP-2.1>
AUTH_SECRET=<GENERATE-BELOW>

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

**Generate AUTH_SECRET**:
```bash
openssl rand -base64 32
```

**Copy the output and paste it as AUTH_SECRET in .env.local**

---

### Step 7: Restart Admin Dashboard

**Stop the current server** (Ctrl+C in the terminal running npm run dev)

**Start again**:
```bash
cd /home/alagiri/projects/bizosaas-platform/portals/admin-dashboard
npm run dev
```

---

### Step 8: Test Authentication

#### 8.1 Test Admin Dashboard

**Open browser**: http://localhost:3004

**Expected Flow**:
1. Should redirect to `/login` page
2. Click "Sign in with SSO" button
3. Should redirect to Authentik: `http://localhost:9000/...`
4. Login with:
   - Username: `superadmin`
   - Password: `<password-from-step-5.1>`
5. Should redirect back to: `http://localhost:3004/dashboard`
6. Should see admin dashboard with user info

**If successful**: ✅ Admin dashboard SSO working!

---

#### 8.2 Test RBAC (Role-Based Access Control)

**Test 1: Super Admin Access**
- Login with `superadmin`
- Should have full access to all features

**Test 2: Platform Admin Access**
- Logout
- Login with `platformadmin`
- Should have access to platform management
- Should NOT have access to super admin features

**Test 3: Unauthorized Access**
- Logout
- Login with `acmeuser` (tenant user)
- Should see "Access Denied" page
- Should NOT be able to access admin dashboard

---

#### 8.3 Test Client Portal (If Configured)

**Open browser**: http://localhost:3003

**Login with**:
- Username: `acmeuser`
- Password: `<password-from-step-5.4>`

**Should**:
- Redirect to Authentik
- Login successfully
- Redirect back to client portal
- See tenant-specific data

---

## ✅ Verification Checklist

- [ ] Authentik accessible at http://localhost:9000
- [ ] Admin dashboard provider created
- [ ] Admin dashboard application created
- [ ] Client portal application exists/created
- [ ] Groups created (super_admin, platform_admin, tenant groups)
- [ ] Test users created and assigned to groups
- [ ] Admin dashboard .env.local updated
- [ ] AUTH_SECRET generated
- [ ] Admin dashboard restarted
- [ ] Admin dashboard login working
- [ ] RBAC working (different access for different roles)
- [ ] Client portal login working (if applicable)

---

## 🎯 Summary of Credentials

### Authentik Admin
- URL: http://localhost:9000
- Username: `akadmin`
- Password: `<your-admin-password>`

### Test Users

| Username | Email | Role | Portal Access |
|----------|-------|------|---------------|
| superadmin | superadmin@bizosaas.local | Super Admin | Admin Dashboard |
| platformadmin | platformadmin@bizosaas.local | Platform Admin | Admin Dashboard |
| acmeadmin | admin@acme.com | Tenant Admin | Client Portal |
| acmeuser | user@acme.com | Tenant User | Client Portal |

### Application Credentials

**Admin Dashboard**:
- Client ID: `bizosaas-admin-dashboard`
- Client Secret: `<from-step-2.1>`
- Redirect URI: `http://localhost:3004/api/auth/callback/authentik`

**Client Portal**:
- Client ID: `bizosaas-client-portal` (or existing)
- Client Secret: `<from-step-3>`
- Redirect URI: `http://localhost:3003/api/auth/callback/authentik`

---

## 🔧 Troubleshooting

### Issue: "Redirect URI mismatch"
**Solution**: 
1. Go to Authentik → Applications → Providers
2. Edit the provider
3. Verify Redirect URIs exactly match:
   - `http://localhost:3004/api/auth/callback/authentik`

### Issue: "Invalid client"
**Solution**:
1. Verify Client ID in .env.local matches Authentik
2. Verify Client Secret is correct
3. Restart admin dashboard

### Issue: "Access Denied" for admin user
**Solution**:
1. Go to Authentik → Directory → Users
2. Select the user
3. Click "Groups" tab
4. Verify user is in `super_admin` or `platform_admin` group

### Issue: Can't access Authentik UI
**Solution**:
```bash
# Check if Authentik is running
docker ps --filter "name=authentik"

# Check logs
cd bizosaas-brain-core
docker compose -f docker-compose.authentik.yml logs authentik-server

# Restart if needed
docker compose -f docker-compose.authentik.yml restart
```

---

## 🎉 Next Steps

After successful configuration:

1. ✅ Document credentials securely
2. ✅ Test all authentication flows
3. ✅ Configure additional tenants as needed
4. ✅ Set up VPS deployment (update redirect URIs)
5. ✅ Configure SSL/TLS for production
6. ✅ Set up Authentik backup

---

## 📞 Quick Reference

**Authentik UI**: http://localhost:9000  
**Admin Dashboard**: http://localhost:3004  
**Client Portal**: http://localhost:3003  

**Documentation**:
- `UNIFIED_AUTHENTIK_CONFIG.md` - Complete guide
- `AUTHENTIK_FINAL_STATUS.md` - Status and next steps
- This file - Step-by-step configuration

---

**Ready to configure?** Start with Step 1 and follow through to Step 8!
