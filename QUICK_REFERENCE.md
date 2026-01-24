# Quick Reference Guide - Authentik Migration
**Date**: 2026-01-24 07:03 UTC

---

## 🚀 **Quick Start**

### **What's Wrong?**
Both `app.bizoholic.net` and `admin.bizoholic.net` are down due to incomplete Clerk → Authentik migration.

### **What's the Fix?**
Complete the migration by updating code and configuring Authentik OAuth.

### **How Long?**
4.5-5.5 hours total work.

---

## 📚 **Document Guide**

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **ISSUE_ANALYSIS_SUMMARY.md** | Executive overview | Start here for big picture |
| **AUTHENTIK_MIGRATION_PLAN.md** | Detailed 24-task plan | Implementation guide |
| **AUTHENTIK_MIGRATION_TASKS.md** | Task checklist | Track progress |
| **ARCHITECTURE_OPTIMIZATION.md** | Future improvements | After migration complete |

---

## ✅ **Step-by-Step Quick Guide**

### **Step 1: Understand the Problem** (5 minutes)
Read: `ISSUE_ANALYSIS_SUMMARY.md`

**Key Points**:
- Middleware still uses Clerk
- Clerk credentials removed
- Authentication fails
- Both portals down

---

### **Step 2: Start Code Migration** (2-3 hours)
Follow: `AUTHENTIK_MIGRATION_PLAN.md` → Phase 1

**Files to Update**:

#### Client Portal
```bash
portals/client-portal/
├── middleware.ts              # Replace Clerk with NextAuth
├── app/login/page.tsx         # Custom login page
├── app/page.tsx               # Replace useUser() hook
├── app/api/auth/[...nextauth]/route.ts  # NEW - Create this
└── package.json               # Remove @clerk/nextjs
```

#### Admin Portal
```bash
portals/admin-dashboard/
├── middleware.ts              # Replace Clerk with NextAuth
├── app/login/page.tsx         # Custom login page
├── app/api/auth/[...nextauth]/route.ts  # NEW - Create this
└── package.json               # Remove @clerk/nextjs
```

**Track Progress**: Check off tasks in `AUTHENTIK_MIGRATION_TASKS.md`

---

### **Step 3: Configure Authentik** (30 minutes)
Follow: `AUTHENTIK_MIGRATION_PLAN.md` → Phase 2

**Access Authentik**:
1. Go to: https://auth-sso.bizoholic.net/if/admin/
2. Login: `akadmin` / `Bizoholic2025!Admin`

**Create OAuth Provider**:
- Applications → Providers → Create
- Type: OAuth2/OpenID
- Client ID: `bizosaas-portal`
- Client Secret: `BizOSaaS2024!AuthentikSecret`
- Redirect URIs:
  - `https://admin.bizoholic.net/api/auth/callback/authentik`
  - `https://app.bizoholic.net/api/auth/callback/authentik`
  - `https://directory.bizoholic.net/api/auth/callback/authentik`

**Create Application**:
- Applications → Applications → Create
- Name: `BizOSaaS Platform`
- Slug: `bizosaas-platform`
- Provider: Select the one created above

**Create Test Users**:
- Directory → Users → Create
- Create: `admin@bizoholic.net` and `client@bizoholic.net`

---

### **Step 4: Deploy Changes** (10 minutes)

```bash
# Commit changes
git add .
git commit -m "Complete Authentik migration - remove Clerk dependencies"
git push origin main

# Dokploy will auto-deploy
# Monitor at: https://dk.bizoholic.com
```

---

### **Step 5: Test Authentication** (1 hour)
Follow: `AUTHENTIK_MIGRATION_PLAN.md` → Phase 4

**Test Checklist**:
- [ ] Visit https://app.bizoholic.net
- [ ] Should redirect to `/login`
- [ ] Click "Sign in with Authentik"
- [ ] Should redirect to Authentik
- [ ] Login with test user
- [ ] Should redirect to `/dashboard`
- [ ] Refresh page - session should persist
- [ ] Repeat for https://admin.bizoholic.net

---

### **Step 6: Vault Integration** (Optional - 1 hour)
Follow: `AUTHENTIK_MIGRATION_PLAN.md` → Phase 3

Store credentials in Vault for better security.

---

## 🔧 **Common Issues & Fixes**

### **Issue: "Invalid redirect URI"**
**Cause**: Redirect URI not configured in Authentik  
**Fix**: Add exact URI to Authentik provider settings

### **Issue: "Invalid client secret"**
**Cause**: Mismatch between env var and Authentik  
**Fix**: Verify `AUTH_AUTHENTIK_SECRET` matches Authentik provider

### **Issue: "Session not persisting"**
**Cause**: Missing `NEXTAUTH_SECRET`  
**Fix**: Set `NEXTAUTH_SECRET` in environment variables

### **Issue: "Build errors after removing Clerk"**
**Cause**: Clerk components still imported somewhere  
**Fix**: Search for `@clerk` imports and remove them

---

## 📊 **Progress Tracking**

Use `AUTHENTIK_MIGRATION_TASKS.md` to track:
- [ ] Phase 1: Code Migration (0/12)
- [ ] Phase 2: Authentik Config (0/4)
- [ ] Phase 3: Vault Integration (0/3)
- [ ] Phase 4: Testing (0/5)

---

## 🆘 **Need Help?**

### **Authentik Issues**
- Docs: https://goauthentik.io/docs/
- Admin Panel: https://auth-sso.bizoholic.net/if/admin/

### **NextAuth Issues**
- Docs: https://next-auth.js.org/
- Provider Docs: https://next-auth.js.org/providers/authentik

### **Deployment Issues**
- Dokploy: https://dk.bizoholic.com
- Check logs in Dokploy UI

---

## 🎯 **Success Checklist**

- [ ] Both portals accessible
- [ ] Login works via Authentik
- [ ] No Clerk references in code
- [ ] No client-side errors
- [ ] Sessions persist across refreshes
- [ ] Logout works correctly

---

## 📝 **After Migration**

Once authentication is working:

1. **Add Health Checks** (1-2 hours)
   - See: `ARCHITECTURE_OPTIMIZATION.md` → Change #5

2. **Deploy Monitoring** (2-3 hours)
   - See: `ARCHITECTURE_OPTIMIZATION.md` → Change #1

3. **Implement User Sync** (2-3 hours)
   - See: `ARCHITECTURE_OPTIMIZATION.md` → Change #3

4. **Configure RBAC** (1-2 hours)
   - See: `ARCHITECTURE_OPTIMIZATION.md` → Change #4

---

**Last Updated**: 2026-01-24 07:03 UTC
