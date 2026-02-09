# Authentik Migration - Implementation Plan
**Created**: 2026-01-24 07:03 UTC  
**Status**: 🔴 **CRITICAL - Production Down**  
**Priority**: P0 - Immediate Action Required

---

## 🚨 **Critical Issues**

### Issue #1: Incomplete Clerk → Authentik Migration
**Impact**: Both `app.bizoholic.net` and `admin.bizoholic.net` are non-functional  
**Root Cause**: Partial migration leaving Clerk middleware active without credentials

**Affected Components**:
- ❌ Middleware (still using Clerk)
- ❌ Login pages (still using Clerk components)
- ❌ Root pages (still using Clerk hooks)
- ❌ Package dependencies (Clerk still installed)
- ✅ Auth config (migrated to Authentik)

### Issue #2: Missing Authentik OAuth Application
**Impact**: Even after migration, authentication will fail  
**Root Cause**: Authentik application not configured with OAuth2 provider

---

## 🎯 **Migration Strategy**

### Phase 1: Complete Authentik Migration (Immediate)
**Goal**: Remove all Clerk dependencies and implement NextAuth + Authentik

### Phase 2: Configure Authentik OAuth (Immediate)
**Goal**: Set up OAuth2 application in Authentik for all portals

### Phase 3: Vault Integration (Next)
**Goal**: Move sensitive credentials to HashiCorp Vault

### Phase 4: Testing & Verification (Immediate)
**Goal**: Verify authentication flow works end-to-end

---

## 📝 **Detailed Tasks**

### **PHASE 1: Complete Authentik Migration**

#### Task 1.1: Update Client Portal Middleware
**File**: `/portals/client-portal/middleware.ts`  
**Action**: Replace Clerk middleware with NextAuth middleware

**Current State**:
```typescript
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
```

**Target State**:
```typescript
import { auth } from "@/lib/auth"
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"
```

**Implementation**:
- Remove Clerk imports
- Implement NextAuth session checking
- Protect `/dashboard/*` routes
- Redirect unauthenticated users to `/login`

---

#### Task 1.2: Update Admin Portal Middleware
**File**: `/portals/admin-dashboard/middleware.ts`  
**Action**: Same as Task 1.1

**Protected Routes**:
- `/dashboard/*`
- `/tenants/*`
- `/settings/*`
- `/users/*`

---

#### Task 1.3: Create NextAuth Login Page (Client Portal)
**File**: `/portals/client-portal/app/login/page.tsx`  
**Action**: Replace Clerk `<SignIn>` with custom NextAuth login

**Requirements**:
- Beautiful, modern UI (matching current design)
- "Sign in with Authentik" button
- Redirect to `/dashboard` after login
- Theme toggle support
- Animated gradient background (keep existing design)

**Implementation**:
```typescript
import { signIn } from "next-auth/react"
```

---

#### Task 1.4: Create NextAuth Login Page (Admin Portal)
**File**: `/portals/admin-dashboard/app/login/page.tsx`  
**Action**: Same as Task 1.3

---

#### Task 1.5: Update Root Page (Client Portal)
**File**: `/portals/client-portal/app/page.tsx`  
**Action**: Replace Clerk hooks with NextAuth

**Current**:
```typescript
import { useUser } from "@clerk/nextjs";
const { isSignedIn, isLoaded, user } = useUser();
```

**Target**:
```typescript
import { useSession } from "next-auth/react"
const { data: session, status } = useSession()
```

---

#### Task 1.6: Update Root Page (Admin Portal)
**File**: `/portals/admin-dashboard/app/page.tsx`  
**Action**: Already correct (simple redirect to `/dashboard`)

---

#### Task 1.7: Create API Auth Routes (Client Portal)
**File**: `/portals/client-portal/app/api/auth/[...nextauth]/route.ts`  
**Action**: Create NextAuth API route handler

**Implementation**:
```typescript
import { handlers } from "@/lib/auth"
export const { GET, POST } = handlers
```

---

#### Task 1.8: Create API Auth Routes (Admin Portal)
**File**: `/portals/admin-dashboard/app/api/auth/[...nextauth]/route.ts`  
**Action**: Same as Task 1.7

---

#### Task 1.9: Update Package Dependencies (Client Portal)
**File**: `/portals/client-portal/package.json`  
**Action**: 
- Remove `@clerk/nextjs`
- Ensure `next-auth` is installed
- Add `next-auth` if missing

---

#### Task 1.10: Update Package Dependencies (Admin Portal)
**File**: `/portals/admin-dashboard/package.json`  
**Action**: Same as Task 1.9

---

#### Task 1.11: Remove Clerk Components (Client Portal)
**Action**: Search and replace all Clerk imports

**Files to check**:
- All components in `/components`
- All pages in `/app`
- Layout files

**Replace**:
- `useUser()` → `useSession()`
- `<SignIn>` → Custom login button
- `<SignUp>` → Custom signup button
- `<UserButton>` → Custom user menu

---

#### Task 1.12: Remove Clerk Components (Admin Portal)
**Action**: Same as Task 1.11

---

### **PHASE 2: Configure Authentik OAuth**

#### Task 2.1: Access Authentik Admin Panel
**URL**: https://auth-sso.bizoholic.net/if/admin/  
**Credentials**: 
- Username: `akadmin`
- Password: `Bizoholic2025!Admin`

---

#### Task 2.2: Create OAuth2/OIDC Provider
**Navigation**: Applications → Providers → Create

**Configuration**:
```yaml
Name: BizOSaaS Platform Provider
Type: OAuth2/OpenID Provider
Client Type: Confidential
Client ID: bizosaas-portal
Client Secret: BizOSaaS2024!AuthentikSecret
Redirect URIs:
  - https://admin.bizoholic.net/api/auth/callback/authentik
  - https://app.bizoholic.net/api/auth/callback/authentik
  - https://directory.bizoholic.net/api/auth/callback/authentik
Signing Key: Auto-generated certificate
Scopes: openid, profile, email
Subject Mode: Based on User's hashed ID
Include claims in id_token: Yes
```

---

#### Task 2.3: Create Authentik Application
**Navigation**: Applications → Applications → Create

**Configuration**:
```yaml
Name: BizOSaaS Platform
Slug: bizosaas-platform
Provider: BizOSaaS Platform Provider (from Task 2.2)
Launch URL: https://app.bizoholic.net
```

---

#### Task 2.4: Create Test Users
**Navigation**: Directory → Users → Create

**Test Users**:
1. **Admin User**:
   - Username: `admin@bizoholic.net`
   - Email: `admin@bizoholic.net`
   - Name: `Admin User`
   - Groups: `admins`

2. **Client User**:
   - Username: `client@bizoholic.net`
   - Email: `client@bizoholic.net`
   - Name: `Client User`
   - Groups: `clients`

---

### **PHASE 3: Vault Integration**

#### Task 3.1: Store Authentik Credentials in Vault
**Vault Path**: `secret/bizosaas/authentik`

**Secrets to Store**:
```json
{
  "client_id": "bizosaas-portal",
  "client_secret": "BizOSaaS2024!AuthentikSecret",
  "issuer": "https://auth-sso.bizoholic.net/application/o/bizosaas-platform/",
  "bootstrap_password": "Bizoholic2025!Admin"
}
```

---

#### Task 3.2: Store NextAuth Secrets in Vault
**Vault Path**: `secret/bizosaas/nextauth`

**Secrets to Store**:
```json
{
  "secret": "BizOSaaS2025!Secret!NextAuth",
  "url": "https://app.bizoholic.net",
  "admin_url": "https://admin.bizoholic.net"
}
```

---

#### Task 3.3: Update Portal Environment Variables
**Action**: Configure portals to read from Vault

**Option 1**: Use Vault Agent Injector (Recommended)  
**Option 2**: Use environment variable substitution at runtime

---

### **PHASE 4: Testing & Verification**

#### Task 4.1: Test Client Portal Login Flow
**Steps**:
1. Navigate to https://app.bizoholic.net
2. Should redirect to `/login`
3. Click "Sign in with Authentik"
4. Should redirect to Authentik login page
5. Enter test credentials
6. Should redirect back to `/dashboard`
7. Verify session is active

**Expected Result**: ✅ Successful login and redirect

---

#### Task 4.2: Test Admin Portal Login Flow
**Steps**: Same as Task 4.1 but for https://admin.bizoholic.net

---

#### Task 4.3: Test Session Persistence
**Steps**:
1. Log in to client portal
2. Refresh page
3. Should remain logged in
4. Navigate to different pages
5. Session should persist

---

#### Task 4.4: Test Logout Flow
**Steps**:
1. Log in to portal
2. Click logout
3. Should redirect to `/login`
4. Attempting to access `/dashboard` should redirect to login

---

#### Task 4.5: Test Cross-Portal SSO
**Steps**:
1. Log in to client portal
2. Open admin portal in new tab
3. Should automatically be logged in (SSO)

**Note**: This may require additional configuration

---

## 🏗️ **Architecture Optimization Review**

### Current Architecture Issues

#### Issue #1: Dual Authentication Systems
**Problem**: Running both Clerk and Authentik creates confusion  
**Solution**: ✅ Complete migration to Authentik (this plan)

#### Issue #2: Hardcoded Secrets
**Problem**: Secrets in environment variables, not in Vault  
**Solution**: Phase 3 of this plan

#### Issue #3: No Centralized User Management
**Problem**: User data scattered across Clerk, Authentik, and database  
**Solution**: 
- Use Authentik as single source of truth
- Sync user data to database via webhooks
- Implement user provisioning workflow

#### Issue #4: Missing Session Management
**Problem**: No admin tools to revoke sessions  
**Solution**: 
- Implement session management in admin portal
- Use Authentik's session API
- Add "Force Logout" feature

---

### Recommended Architecture Changes

#### Change #1: Implement Authentik Webhooks
**Purpose**: Sync user creation/updates to database

**Implementation**:
```
Authentik → Webhook → Backend API → Database
```

**Events to Listen**:
- `user.create`
- `user.update`
- `user.delete`
- `user.login`
- `user.logout`

---

#### Change #2: Add API Gateway Layer
**Purpose**: Centralize authentication and authorization

**Current**:
```
Portal → Backend API (with auth check)
```

**Proposed**:
```
Portal → API Gateway (auth check) → Backend API
```

**Benefits**:
- Single point of authentication
- Rate limiting
- Request logging
- API versioning

---

#### Change #3: Implement RBAC in Authentik
**Purpose**: Centralize permission management

**Current**: Roles stored in database  
**Proposed**: Roles managed in Authentik groups

**Groups to Create**:
- `super_admins`
- `admins`
- `partners`
- `clients`

**Permissions**: Mapped to OAuth scopes

---

#### Change #4: Add Monitoring & Alerting
**Purpose**: Detect authentication failures early

**Metrics to Track**:
- Failed login attempts
- Session creation rate
- Token refresh failures
- OAuth callback errors

**Tools**:
- Prometheus (metrics)
- Grafana (dashboards)
- Loki (logs)
- Alertmanager (alerts)

---

## 📊 **Success Criteria**

### Phase 1 Success
- [ ] All Clerk code removed from both portals
- [ ] NextAuth middleware protecting routes
- [ ] Custom login pages implemented
- [ ] No build errors
- [ ] No runtime errors in browser console

### Phase 2 Success
- [ ] Authentik OAuth application created
- [ ] Test users can log in via Authentik
- [ ] OAuth callback working correctly
- [ ] Sessions persisting across page refreshes

### Phase 3 Success
- [ ] All secrets stored in Vault
- [ ] Portals reading from Vault
- [ ] No hardcoded credentials in code

### Phase 4 Success
- [ ] All test cases passing
- [ ] Both portals accessible and functional
- [ ] SSO working across portals
- [ ] No authentication errors

---

## 🚀 **Deployment Strategy**

### Step 1: Code Changes (Local)
1. Create feature branch: `feature/complete-authentik-migration`
2. Implement all Phase 1 tasks
3. Test locally (if possible)
4. Commit changes

### Step 2: Authentik Configuration (Production)
1. Log in to Authentik admin
2. Complete Phase 2 tasks
3. Document all settings
4. Take screenshots for reference

### Step 3: Deploy Code Changes
1. Push branch to GitHub
2. Create Pull Request
3. Review changes
4. Merge to main
5. Dokploy auto-deploys

### Step 4: Vault Configuration
1. Access Vault UI
2. Complete Phase 3 tasks
3. Update portal environment variables in Dokploy

### Step 5: Testing
1. Run all Phase 4 tests
2. Fix any issues
3. Verify production stability

---

## ⏱️ **Time Estimates**

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Phase 1 | 12 tasks | 2-3 hours |
| Phase 2 | 4 tasks | 30 minutes |
| Phase 3 | 3 tasks | 1 hour |
| Phase 4 | 5 tasks | 1 hour |
| **Total** | **24 tasks** | **4.5-5.5 hours** |

---

## 🔗 **Dependencies**

### External Services
- ✅ Authentik SSO (https://auth-sso.bizoholic.net)
- ✅ Vault (https://vault.bizoholic.net)
- ✅ Dokploy (https://dk.bizoholic.com)

### Code Dependencies
- `next-auth` (v5 beta)
- `next` (v14+)
- `react` (v18+)

### Access Required
- Authentik admin credentials
- Vault root token or admin credentials
- Dokploy API key
- GitHub repository access

---

## 📞 **Rollback Plan**

If migration fails:

### Option 1: Revert to Clerk (Quick)
1. Revert Git commits
2. Restore Clerk environment variables
3. Redeploy previous version

### Option 2: Fix Forward (Recommended)
1. Identify specific failure
2. Fix issue
3. Redeploy
4. Test again

---

## 📝 **Notes**

- **Backup**: Take database backup before starting
- **Downtime**: Expect 5-10 minutes of downtime during deployment
- **Communication**: Notify users of maintenance window
- **Testing**: Test in staging environment if available

---

**Last Updated**: 2026-01-24 07:03 UTC  
**Next Review**: After Phase 1 completion  
**Owner**: Development Team
