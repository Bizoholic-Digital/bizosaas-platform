# ✅ READY - Your Action Items

**Time**: 2025-12-11 15:25 IST  
**Status**: Environment prepared, ready for Authentik configuration

---

## ✅ What's Done

- ✓ Authentik running (http://localhost:9000)
- ✓ `.env.local` created
- ✓ AUTH_SECRET generated: `FzNC196uqLqZ6vNnGRj7wj/F3xHbp7pBocdauLITxCQ=`
- ✓ All documentation ready

---

## 🎯 YOUR NEXT STEPS (15 minutes)

### Step 1: Configure Authentik (10 min)

**Open in browser**: http://localhost:9000

**Follow these exact steps**:

#### 1.1 Login/Setup
- If first time: Complete setup wizard
- Username: `akadmin`
- Set admin password

#### 1.2 Create OAuth Provider
```
Navigate: Applications → Providers → Create
Select: OAuth2/OpenID Provider

COPY THESE VALUES EXACTLY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: BizOSaaS Admin Dashboard Provider
Authorization flow: default-provider-authorization-implicit-consent
Client type: Confidential
Client ID: bizosaas-admin-dashboard
Client Secret: <CLICK "GENERATE" BUTTON - SAVE THIS!!!>
Redirect URIs/Origins (REGEX):
  http://localhost:3004/api/auth/callback/authentik

Advanced Protocol Settings:
- Scopes: Select: openid, profile, email, groups
- Subject mode: Based on the User's hashed ID
- Include claims in id_token: ✓ (check this)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Click: Create

⚠️ CRITICAL: Copy the Client Secret NOW!
```

#### 1.3 Create Application
```
Navigate: Applications → Applications → Create

COPY THESE VALUES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: BizOSaaS Admin Dashboard
Slug: bizosaas-admin
Provider: BizOSaaS Admin Dashboard Provider (select from dropdown)
Launch URL: http://localhost:3004
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Click: Create
```

#### 1.4 Create Groups
```
Navigate: Directory → Groups → Create

Group 1 - Super Admin:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: super_admin
Is superuser: ✓ (CHECK THIS BOX!)
Attributes: {"permissions": ["*"], "access_level": "platform"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Click: Create

Group 2 - Platform Admin:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: platform_admin
Is superuser: ✗ (UNCHECK THIS BOX!)
Attributes: {"permissions": ["tenants:*"], "access_level": "platform"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Click: Create
```

#### 1.5 Create Test User
```
Navigate: Directory → Users → Create

User Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Username: superadmin
Name: Super Administrator
Email: superadmin@bizosaas.local
Is active: ✓ (CHECK THIS BOX!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tab: "Set password"
Password: Admin@123
Confirm: Admin@123

Tab: "Groups"
Select: super_admin
Click: Add

Click: Create
```

**SAVE THESE CREDENTIALS**:
- Username: `superadmin`
- Password: `Admin@123`

---

### Step 2: Update .env.local (3 min)

**Edit the file**:
```bash
cd /home/alagiri/projects/bizosaas-platform/portals/admin-dashboard
nano .env.local
# or
code .env.local
```

**Update these two lines** (replace placeholders):
```env
AUTHENTIK_CLIENT_SECRET=<PASTE_CLIENT_SECRET_FROM_STEP_1.2>
AUTH_SECRET=FzNC196uqLqZ6vNnGRj7wj/F3xHbp7pBocdauLITxCQ=
```

**The complete .env.local should look like**:
```env
# Authentik SSO Configuration (Same instance as client portal)
AUTHENTIK_URL=http://localhost:9000
NEXT_PUBLIC_SSO_URL=http://localhost:9000
AUTHENTIK_ISSUER=http://localhost:9000/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<YOUR_CLIENT_SECRET_HERE>
AUTH_SECRET=FzNC196uqLqZ6vNnGRj7wj/F3xHbp7pBocdauLITxCQ=

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

**Save the file** (Ctrl+X, Y, Enter in nano)

---

### Step 3: Start Admin Dashboard (2 min)

**Run**:
```bash
cd /home/alagiri/projects/bizosaas-platform/portals/admin-dashboard
npm run dev
```

**Wait for**:
```
✓ Ready in 2.5s
○ Local:        http://localhost:3004
```

---

### Step 4: Test Login (NOW!)

**Open browser**: http://localhost:3004

**Expected flow**:
1. Should see login page
2. Click: "Sign in with SSO"
3. Redirects to: http://localhost:9000
4. Login:
   - Username: `superadmin`
   - Password: `Admin@123`
5. Redirects back to: http://localhost:3004
6. **SUCCESS**: You should see the admin dashboard!

---

## 🔧 If Something Goes Wrong

### "Redirect URI mismatch"
```
Fix in Authentik:
- Go to: Applications → Providers → BizOSaaS Admin Dashboard Provider
- Edit Redirect URIs
- Should be exactly: http://localhost:3004/api/auth/callback/authentik
- No trailing slash!
- Save
```

### "Invalid client" or "Client authentication failed"
```
Check .env.local:
- AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard (exact match)
- AUTHENTIK_CLIENT_SECRET=<correct secret, no spaces>
- Restart admin dashboard after changes
```

### "Access Denied" after login
```
Check in Authentik:
- User 'superadmin' exists
- User is in 'super_admin' group
- Group name is exactly: super_admin (lowercase, no spaces)
```

### Still stuck?
```
Check logs:
1. Admin dashboard terminal (where npm run dev is running)
2. Browser console (F12 → Console tab)
3. Authentik logs: docker logs authentik-server --tail 50
```

---

## ✅ Success Checklist

- [ ] Opened http://localhost:9000
- [ ] Created OAuth Provider
- [ ] **SAVED Client Secret**
- [ ] Created Application (slug: bizosaas-admin)
- [ ] Created super_admin group
- [ ] Created platform_admin group
- [ ] Created superadmin user
- [ ] Added superadmin to super_admin group
- [ ] Updated .env.local with Client Secret
- [ ] Updated .env.local with AUTH_SECRET
- [ ] Started admin dashboard (npm run dev)
- [ ] Opened http://localhost:3004
- [ ] Clicked "Sign in with SSO"
- [ ] Logged in successfully
- [ ] **Dashboard is working!**

---

## 📋 After Local Testing Works

### Next: Deploy to VPS

1. **Fix any issues locally first**
2. **Commit to git**:
   ```bash
   git add .
   git commit -m "feat: admin dashboard with Authentik SSO"
   git push origin main
   ```

3. **Configure VPS Authentik** (https://sso.bizoholic.net)
   - Same steps as local
   - Different redirect URI: https://admin.bizoholic.net/api/auth/callback/authentik

4. **Deploy via Dokploy**
   - Upload docker-compose.admin-dashboard.yml
   - Set environment variables
   - Deploy

5. **Test production**: https://admin.bizoholic.net

---

## 📞 Quick Reference

**Authentik UI**: http://localhost:9000  
**Admin Dashboard**: http://localhost:3004  
**AUTH_SECRET**: `FzNC196uqLqZ6vNnGRj7wj/F3xHbp7pBocdauLITxCQ=`  

**Test Credentials**:
- Username: `superadmin`
- Password: `Admin@123`

---

## 🚀 START NOW

**Step 1**: Open http://localhost:9000  
**Step 2**: Follow the configuration steps above  
**Step 3**: Test at http://localhost:3004  

**Time**: 15 minutes  
**Let's go!** 🎉
