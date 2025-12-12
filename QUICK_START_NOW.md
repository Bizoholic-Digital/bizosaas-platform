# 🎯 QUICK START - Configure & Test Now

**Status**: ✅ Authentik Running | ✅ Admin Dashboard Running  
**Time**: 15 minutes to complete

---

## Step 1: Open Authentik (NOW)

**URL**: http://localhost:9000

**What to do**:
1. Login or complete first-time setup
2. Default username: `akadmin`

---

## Step 2: Create OAuth Provider (5 min)

```
Navigate: Applications → Providers → Create
Select: OAuth2/OpenID Provider

Copy these values EXACTLY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: BizOSaaS Admin Dashboard Provider
Authorization flow: default-provider-authorization-implicit-consent  
Client type: Confidential
Client ID: bizosaas-admin-dashboard
Client Secret: <CLICK "GENERATE" - SAVE THIS!!!>
Redirect URIs: http://localhost:3004/api/auth/callback/authentik
Scopes: openid, profile, email, groups
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Click: Create
```

**⚠️ CRITICAL**: Copy the Client Secret immediately!

---

## Step 3: Create Application (2 min)

```
Navigate: Applications → Applications → Create

Copy these values EXACTLY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: BizOSaaS Admin Dashboard
Slug: bizosaas-admin
Provider: BizOSaaS Admin Dashboard Provider (select from dropdown)
Launch URL: http://localhost:3004
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Click: Create
```

---

## Step 4: Create Groups (3 min)

```
Navigate: Directory → Groups → Create

Group 1:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: super_admin
Is superuser: ✓ (CHECK THIS BOX)
Attributes: {"permissions": ["*"], "access_level": "platform"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Click: Create

Group 2:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: platform_admin
Is superuser: ✗ (UNCHECK THIS BOX)
Attributes: {"permissions": ["tenants:*"], "access_level": "platform"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Click: Create
```

---

## Step 5: Create Test User (3 min)

```
Navigate: Directory → Users → Create

User Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Username: superadmin
Name: Super Administrator
Email: superadmin@bizosaas.local
Is active: ✓ (CHECK THIS BOX)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Click "Set password" tab:
Password: Admin@123 (or your choice)
Confirm: Admin@123

Click "Groups" tab:
Select: super_admin
Click: Add

Click: Create
```

**SAVE THESE**:
- Username: `superadmin`
- Password: `Admin@123`

---

## Step 6: Update .env.local (2 min)

**Run these commands**:
```bash
cd /home/alagiri/projects/bizosaas-platform/portals/admin-dashboard

# Generate AUTH_SECRET
openssl rand -base64 32

# This will output something like: xK7mP9nQ2rS5tU8vW1xY4zA6bC3dE0fG1hI2jK3lM4=
# COPY THIS OUTPUT!
```

**Edit .env.local**:
```bash
# If .env.local doesn't exist
cp .env.example .env.local

# Now edit it with your values
nano .env.local
# or
code .env.local
```

**Paste these values** (replace <PLACEHOLDERS>):
```env
AUTHENTIK_URL=http://localhost:9000
NEXT_PUBLIC_SSO_URL=http://localhost:9000
AUTHENTIK_ISSUER=http://localhost:9000/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<PASTE_FROM_STEP_2>
AUTH_SECRET=<PASTE_FROM_OPENSSL_COMMAND>

NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://localhost:8000
NEXT_PUBLIC_TEMPORAL_UI_URL=http://localhost:8233
NEXT_PUBLIC_VAULT_UI_URL=http://localhost:8200

NODE_ENV=development
PORT=3004

NEXTAUTH_URL=http://localhost:3004
NEXTAUTH_URL_INTERNAL=http://localhost:3004
```

**Save the file** (Ctrl+X, then Y, then Enter in nano)

---

## Step 7: Test Login (NOW!)

**Restart Admin Dashboard**:
```bash
# In the terminal running admin dashboard, press Ctrl+C to stop

# Then start again
cd /home/alagiri/projects/bizosaas-platform/portals/admin-dashboard
npm run dev
```

**Test Authentication**:
```
1. Open: http://localhost:3004
2. Should see login page
3. Click: "Sign in with SSO"
4. Should redirect to: http://localhost:9000
5. Login:
   - Username: superadmin
   - Password: Admin@123
6. Should redirect back to: http://localhost:3004
7. Should see: Dashboard!
```

---

## ✅ Success Checklist

- [ ] Opened http://localhost:9000
- [ ] Created OAuth Provider
- [ ] Saved Client Secret
- [ ] Created Application
- [ ] Created super_admin group
- [ ] Created platform_admin group
- [ ] Created superadmin user
- [ ] Generated AUTH_SECRET
- [ ] Updated .env.local
- [ ] Restarted admin dashboard
- [ ] Tested login at http://localhost:3004
- [ ] Successfully logged in!

---

## 🔧 If Something Goes Wrong

### "Redirect URI mismatch"
```
Check in Authentik provider:
- Should be: http://localhost:3004/api/auth/callback/authentik
- No trailing slash!
```

### "Invalid client"
```
Check .env.local:
- AUTHENTIK_CLIENT_ID matches Authentik
- AUTHENTIK_CLIENT_SECRET is correct
- No extra spaces
```

### "Access Denied"
```
Check in Authentik:
- User is in super_admin group
- Group name is exactly: super_admin (lowercase)
```

### Still stuck?
```
Check logs:
- Admin dashboard terminal
- Browser console (F12)
- Authentik logs: docker logs authentik-server
```

---

## 📞 Quick Links

- **Authentik**: http://localhost:9000
- **Admin Dashboard**: http://localhost:3004
- **Full Guide**: `LOCAL_TEST_AND_DEPLOY.md`

---

**START HERE**: http://localhost:9000

**Time to complete**: 15 minutes  
**Let's go!** 🚀
