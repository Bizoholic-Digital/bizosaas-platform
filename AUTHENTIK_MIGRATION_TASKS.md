# Authentik Migration - Task Checklist
**Created**: 2026-01-24 07:03 UTC  
**Status**: 🔴 **IN PROGRESS**

---

## 🎯 **Quick Status**

| Phase | Status | Progress | Priority |
|-------|--------|----------|----------|
| Phase 1: Code Migration | ✅ Completed | 12/12 | P0 - Critical |
| Phase 2: Authentik Config | 🟡 Pending | 0/4 | P0 - Critical |
| Phase 3: Vault Integration | 🟡 Pending | 0/3 | P1 - High |
| Phase 4: Testing | 🟡 Pending | 0/5 | P0 - Critical |

---

## ✅ **PHASE 1: Code Migration** (0/12)

### Client Portal Updates
- [x] **Task 1.1**: Update middleware.ts (Remove Clerk, add NextAuth)
- [x] **Task 1.3**: Create NextAuth login page
- [x] **Task 1.5**: Update root page (Replace Clerk hooks)
- [x] **Task 1.7**: Create API auth routes
- [x] **Task 1.9**: Update package.json (Remove Clerk)
- [x] **Task 1.11**: Remove all Clerk components

### Admin Portal Updates
- [x] **Task 1.2**: Update middleware.ts (Remove Clerk, add NextAuth)
- [x] **Task 1.4**: Create NextAuth login page
- [x] **Task 1.6**: Verify root page (Already correct)
- [x] **Task 1.8**: Create API auth routes
- [x] **Task 1.10**: Update package.json (Remove Clerk)
- [x] **Task 1.12**: Remove all Clerk components

---

## ✅ **PHASE 2: Authentik Configuration** (0/4)

- [ ] **Task 2.1**: Access Authentik admin panel
  - URL: https://auth-sso.bizoholic.net/if/admin/
  - Username: `akadmin`
  - Password: `Bizoholic2025!Admin`

- [ ] **Task 2.2**: Create OAuth2/OIDC Provider
  - Name: BizOSaaS Platform Provider
  - Client ID: `bizosaas-portal`
  - Client Secret: `BizOSaaS2024!AuthentikSecret`
  - Redirect URIs: 3 portals

- [ ] **Task 2.3**: Create Authentik Application
  - Name: BizOSaaS Platform
  - Slug: `bizosaas-platform`
  - Link to provider from Task 2.2

- [ ] **Task 2.4**: Create test users
  - Admin user: `admin@bizoholic.net`
  - Client user: `client@bizoholic.net`

---

## ✅ **PHASE 3: Vault Integration** (0/3)

- [ ] **Task 3.1**: Store Authentik credentials in Vault
  - Path: `secret/bizosaas/authentik`
  - Keys: client_id, client_secret, issuer, bootstrap_password

- [ ] **Task 3.2**: Store NextAuth secrets in Vault
  - Path: `secret/bizosaas/nextauth`
  - Keys: secret, url, admin_url

- [ ] **Task 3.3**: Update portal environment variables
  - Configure Vault integration
  - Test secret retrieval

---

## ✅ **PHASE 4: Testing & Verification** (0/5)

- [ ] **Task 4.1**: Test client portal login flow
  - Navigate to https://app.bizoholic.net
  - Click "Sign in with Authentik"
  - Verify redirect to Authentik
  - Login with test user
  - Verify redirect to dashboard

- [ ] **Task 4.2**: Test admin portal login flow
  - Same as Task 4.1 for https://admin.bizoholic.net

- [ ] **Task 4.3**: Test session persistence
  - Refresh page
  - Navigate between pages
  - Verify session remains active

- [ ] **Task 4.4**: Test logout flow
  - Click logout
  - Verify redirect to login
  - Verify dashboard is protected

- [ ] **Task 4.5**: Test cross-portal SSO
  - Login to client portal
  - Open admin portal
  - Verify automatic login

---

## 🚨 **Blockers & Issues**

| ID | Issue | Status | Resolution |
|----|-------|--------|------------|
| - | None yet | - | - |

---

## 📝 **Notes & Decisions**

### 2026-01-24 07:03 UTC
- Created migration plan
- Identified root cause: Incomplete Clerk → Authentik migration
- Both portals are down due to Clerk middleware without credentials
- Priority: Complete Phase 1 & 2 immediately to restore service

---

## 🎯 **Next Actions**

1. **Immediate**: Start Phase 1 - Code Migration
2. **Immediate**: Complete Phase 2 - Authentik Configuration
3. **Next**: Phase 3 - Vault Integration
4. **Final**: Phase 4 - Testing

---

**Progress**: 12/24 tasks completed (50%)  
**ETA**: 2.5 hours remaining
**Last Updated**: 2026-01-24 07:35 UTC
