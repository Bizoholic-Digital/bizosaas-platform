# 🚀 IMMEDIATE ACTION PLAN - Authentik Integration

**Time**: 2025-12-11 14:30 IST  
**Goal**: Get admin dashboard working with Authentik SSO (local + VPS)

---

## ✅ Current Status

```
✓ Local Authentik:     RUNNING (http://localhost:9000)
✓ VPS Authentik:       RUNNING (https://sso.bizoholic.net)
✓ Admin Dashboard:     RUNNING (http://localhost:3004)
✓ Client Portal:       INTEGRATED with Authentik ✅
```

---

## 🎯 TODAY'S TASKS (2 hours)

### Task 1: Configure Local Authentik (30 min)

**Step 1.1: Access Authentik**
```
URL: http://localhost:9000
Action: Complete first-time setup or login
```

**Step 1.2: Create Admin Dashboard Application**
```
1. Navigate to: Applications → Providers → Create
2. Type: OAuth2/OpenID Provider
3. Name: BizOSaaS Admin Dashboard Provider
4. Client ID: bizosaas-admin-dashboard
5. Client Secret: <GENERATE AND SAVE>
6. Redirect URI: http://localhost:3004/api/auth/callback/authentik
7. Scopes: openid, profile, email, groups
8. Click: Create
```

**Step 1.3: Create Application**
```
1. Navigate to: Applications → Applications → Create
2. Name: BizOSaaS Admin Dashboard
3. Slug: bizosaas-admin
4. Provider: BizOSaaS Admin Dashboard Provider
5. Launch URL: http://localhost:3004
6. Click: Create
```

**Step 1.4: Create Groups**
```
1. Navigate to: Directory → Groups → Create
2. Create: super_admin (is_superuser: ✓)
3. Create: platform_admin (is_superuser: ✗)
```

**Step 1.5: Create Test User**
```
1. Navigate to: Directory → Users → Create
2. Username: superadmin
3. Email: superadmin@bizosaas.local
4. Password: <SET-PASSWORD>
5. Groups: super_admin
6. Click: Create
```

---

### Task 2: Update Admin Dashboard (10 min)

**Step 2.1: Update Environment**
```bash
cd /home/alagiri/projects/bizosaas-platform/portals/admin-dashboard
cp .env.example .env.local
```

**Step 2.2: Edit .env.local**
```env
AUTHENTIK_URL=http://localhost:9000
NEXT_PUBLIC_SSO_URL=http://localhost:9000
AUTHENTIK_ISSUER=http://localhost:9000/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<PASTE-FROM-STEP-1.2>
AUTH_SECRET=<GENERATE-BELOW>

NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3004
NEXTAUTH_URL_INTERNAL=http://localhost:3004
```

**Step 2.3: Generate AUTH_SECRET**
```bash
openssl rand -base64 32
# Copy output and paste as AUTH_SECRET
```

---

### Task 3: Test Local Authentication (10 min)

**Step 3.1: Restart Admin Dashboard**
```bash
# Stop current server (Ctrl+C)
cd /home/alagiri/projects/bizosaas-platform/portals/admin-dashboard
npm run dev
```

**Step 3.2: Test Login**
```
1. Open: http://localhost:3004
2. Should redirect to: /login
3. Click: "Sign in with SSO"
4. Should redirect to: http://localhost:9000
5. Login with: superadmin / <password>
6. Should redirect back to: http://localhost:3004/dashboard
```

**Expected Result**: ✅ Logged in to admin dashboard!

---

### Task 4: Configure VPS Authentik (30 min)

**Step 4.1: Access VPS Authentik**
```
URL: https://sso.bizoholic.net
Action: Login with admin credentials (from credentials.md)
```

**Step 4.2: Check Existing Applications**
```
1. Navigate to: Applications → Applications
2. Look for: "BizOSaaS" or "bizosaas" (client portal)
3. Note: This confirms VPS Authentik is working
```

**Step 4.3: Create Admin Dashboard Application**
```
Same as Task 1.2 and 1.3, but with:
- Redirect URI: https://admin.bizoholic.net/api/auth/callback/authentik
- Also add: http://localhost:3004/api/auth/callback/authentik (for testing)
```

**Step 4.4: Save Credentials**
```
Client ID: bizosaas-admin-dashboard
Client Secret: <SAVE-SECURELY>
```

---

### Task 5: Update VPS Deployment (40 min)

**Step 5.1: Update VPS Environment**
```
On VPS (via Dokploy or SSH):
- Update admin dashboard environment variables
- Set AUTHENTIK_URL=https://sso.bizoholic.net
- Set AUTHENTIK_CLIENT_SECRET=<from-step-4.3>
- Set AUTH_SECRET=<secure-value>
```

**Step 5.2: Deploy Admin Dashboard**
```
- Build Docker image
- Deploy to VPS
- Verify deployment
```

**Step 5.3: Test VPS Authentication**
```
1. Open: https://admin.bizoholic.net
2. Should redirect to: https://sso.bizoholic.net
3. Login with admin user
4. Should redirect back to dashboard
```

**Expected Result**: ✅ Admin dashboard working on VPS!

---

## 📋 Quick Checklist

### Local Setup
- [ ] Access http://localhost:9000
- [ ] Create admin dashboard provider
- [ ] Create admin dashboard application
- [ ] Create super_admin group
- [ ] Create test user
- [ ] Save Client Secret
- [ ] Update .env.local
- [ ] Generate AUTH_SECRET
- [ ] Restart admin dashboard
- [ ] Test login at http://localhost:3004

### VPS Setup
- [ ] Access https://sso.bizoholic.net
- [ ] Create admin dashboard provider
- [ ] Create admin dashboard application
- [ ] Save Client Secret
- [ ] Update VPS environment variables
- [ ] Deploy admin dashboard
- [ ] Test login at https://admin.bizoholic.net

---

## 🔧 Commands Reference

**Start Authentik (Local)**:
```bash
cd bizosaas-brain-core
docker compose -f docker-compose.authentik.yml up -d
```

**Check Authentik Status**:
```bash
docker ps --filter "name=authentik"
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

---

## 📞 URLs

- **Local Authentik**: http://localhost:9000
- **VPS Authentik**: https://sso.bizoholic.net
- **Local Admin**: http://localhost:3004
- **VPS Admin**: https://admin.bizoholic.net
- **Client Portal**: http://localhost:3003 (local) / https://app.bizoholic.net (VPS)

---

## 🎯 Success Criteria

✅ **Local**:
- Can login to admin dashboard via Authentik
- SSO flow working
- User info displayed correctly

✅ **VPS**:
- Admin dashboard deployed
- Can login via sso.bizoholic.net
- Same user can access both client portal and admin dashboard

✅ **Overall**:
- Single Authentik instance per environment
- Consistent authentication
- RBAC working

---

## 📚 Documentation

- **Setup Guide**: `AUTHENTIK_SETUP_GUIDE.md`
- **Architecture**: `AUTHENTIK_LOCAL_TO_VPS.md`
- **Quick Start**: This file

---

## 🚀 START HERE

**Step 1**: Open http://localhost:9000  
**Step 2**: Follow Task 1 above  
**Step 3**: Continue through Task 5  

**Time Required**: 2 hours  
**Difficulty**: Medium  
**Impact**: High (unified SSO for entire platform)

---

**Ready? Let's go!** 🎉
