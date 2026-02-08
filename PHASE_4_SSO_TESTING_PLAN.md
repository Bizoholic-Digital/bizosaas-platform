# Phase 4 - SSO Testing & Validation Plan

**Date:** November 16, 2025
**Status:** Ready to Begin
**Prerequisites:** ✅ Phase 3 Complete - All 7 frontends integrated

---

## Overview

Phase 4 focuses on comprehensive testing and validation of the centralized authentication system across all 7 frontend platforms. This ensures SSO works correctly, session management is reliable, and role-based access control functions as intended.

---

## Testing Environment Setup

### 1. Local Development Environment

**Prerequisites:**
```bash
# Ensure all frontends are running
cd bizosaas/frontend/apps/client-portal && npm run dev        # Port 3000
cd bizosaas/frontend/apps/bizoholic-frontend && npm run dev   # Port 3001
cd bizosaas/frontend/apps/coreldove-storefront && pnpm dev    # Port 3002
cd bizosaas/frontend/apps/bizosaas-admin && npm run dev       # Port 3003
cd bizosaas/frontend/apps/business-directory && npm run dev   # Port 3004
cd bizosaas/frontend/apps/thrillring-gaming && npm run dev    # Port 3006
cd bizosaas/frontend/apps/analytics-dashboard && npm run dev  # Port 3009
```

**Auth Service:**
- URL: `https://api.bizoholic.com/auth`
- Status: Production ready
- Health check: `GET /auth/health`

### 2. Test Credentials

#### Super Admin (Cross-Platform Access)
```
Email: admin@bizosaas.com
Password: AdminDemo2024!
Access: All 7 platforms, all tenants
```

#### Tenant Admins
```
Bizoholic:  admin@bizoholic.com   | AdminDemo2024!  | Platforms: Bizoholic, Client Portal
CoreLDove:  admin@coreldove.com   | AdminDemo2024!  | Platforms: CoreLDove Storefront
ThrillRing: admin@thrillring.com  | AdminDemo2024!  | Platforms: ThrillRing Gaming
BizOSaaS:   admin@tenant.com      | AdminDemo2024!  | Platforms: Admin, Directory, Analytics
```

#### Standard Users
```
General:    user@bizosaas.com     | UserDemo2024!   | Access: Limited features
Analyst:    analyst@bizosaas.com  | UserDemo2024!   | Access: Analytics Dashboard (readonly)
Gamer:      gamer@thrillring.com  | UserDemo2024!   | Access: ThrillRing Gaming
Customer:   user@coreldove.com    | UserDemo2024!   | Access: CoreLDove Storefront
```

---

## Test Suites

### Test Suite 1: Basic Authentication (Priority: Critical)

#### Test 1.1: Login Flow
**Objective:** Verify login works on each platform

**Steps:**
1. Navigate to each platform's login page
2. Enter valid credentials
3. Submit login form
4. Verify redirect to dashboard/home
5. Verify user info displayed correctly

**Platforms to Test:**
- [ ] Client Portal (`http://localhost:3000/login`)
- [ ] Bizoholic Frontend (`http://localhost:3001/login`)
- [ ] CoreLDove Storefront (`http://localhost:3002/login`)
- [ ] BizOSaaS Admin (`http://localhost:3003/login`)
- [ ] Business Directory (`http://localhost:3004/login`)
- [ ] ThrillRing Gaming (`http://localhost:3006/login`)
- [ ] Analytics Dashboard (`http://localhost:3009/login`)

**Success Criteria:**
✅ Login successful on all platforms
✅ User redirected to correct page
✅ User name/email displayed in UI
✅ No console errors

---

#### Test 1.2: Logout Flow
**Objective:** Verify logout clears session correctly

**Steps:**
1. Login to a platform
2. Click logout button
3. Verify redirect to login/home page
4. Verify user cannot access protected routes
5. Try accessing protected route directly

**Platforms to Test:**
- [ ] All 7 platforms

**Success Criteria:**
✅ Logout successful
✅ User redirected to public page
✅ Session cleared (no user data in context)
✅ Protected routes redirect to login

---

### Test Suite 2: Single Sign-On (Priority: Critical)

#### Test 2.1: SSO Login Propagation
**Objective:** Login on one platform = logged in on all

**Steps:**
1. Clear all cookies and storage
2. Login to Client Portal (`localhost:3000`)
3. Without logging in again, navigate to:
   - Bizoholic Frontend (`localhost:3001`)
   - CoreLDove Storefront (`localhost:3002`)
   - BizOSaaS Admin (`localhost:3003`)
   - Business Directory (`localhost:3004`)
   - ThrillRing Gaming (`localhost:3006`)
   - Analytics Dashboard (`localhost:3009`)
4. Verify user is already logged in on all platforms

**Success Criteria:**
✅ Single login works across all platforms
✅ User info displayed correctly on all platforms
✅ No additional login required
✅ Session shared via cookies

**Test Variations:**
- Start login from different platforms (test from each)
- Use different user roles (super_admin, tenant_admin, user)

---

#### Test 2.2: SSO Logout Propagation
**Objective:** Logout on one platform = logged out on all

**Steps:**
1. Login to all 7 platforms (via SSO)
2. Verify logged in on all platforms
3. Logout from Analytics Dashboard (`localhost:3009`)
4. Navigate to other 6 platforms
5. Verify logged out on all platforms

**Success Criteria:**
✅ Logout from one platform clears session everywhere
✅ All platforms redirect to login
✅ No user data remains in any platform
✅ Cookies cleared properly

---

### Test Suite 3: Role-Based Access Control (Priority: High)

#### Test 3.1: Super Admin Access
**Objective:** Verify super admin has access to all platforms and features

**Credentials:** `admin@bizosaas.com` / `AdminDemo2024!`

**Test Matrix:**
| Platform | Access Expected | Features to Verify |
|----------|----------------|-------------------|
| Client Portal | ✅ Full | Tenant management, all tenants visible |
| Bizoholic Frontend | ✅ Full | Admin features visible |
| CoreLDove Storefront | ✅ Full | Store management |
| BizOSaaS Admin | ✅ Full | Platform settings, all features |
| Business Directory | ✅ Full | All listings, management features |
| ThrillRing Gaming | ✅ Full | Tournament management |
| Analytics Dashboard | ✅ Full | All dashboards, cross-tenant data |

**Steps:**
1. Login as super admin
2. Navigate to each platform
3. Verify all admin features visible
4. Test creating/editing features (if applicable)
5. Verify cross-tenant data access (Analytics Dashboard)

**Success Criteria:**
✅ Super admin can access all 7 platforms
✅ All admin features visible and functional
✅ No permission errors
✅ Cross-tenant data visible where appropriate

---

#### Test 3.2: Tenant Admin Access
**Objective:** Verify tenant admins see only their tenant's data

**Test Cases:**

**Case A: Bizoholic Tenant Admin**
- Credentials: `admin@bizoholic.com` / `AdminDemo2024!`
- Should Access: Client Portal, Bizoholic Frontend
- Should NOT Access: CoreLDove-specific, ThrillRing-specific features
- Test: Verify tenant isolation in Client Portal

**Case B: CoreLDove Tenant Admin**
- Credentials: `admin@coreldove.com` / `AdminDemo2024!`
- Should Access: CoreLDove Storefront
- Should NOT Access: Other tenants' stores
- Test: Verify store data isolation

**Case C: ThrillRing Tenant Admin**
- Credentials: `admin@thrillring.com` / `AdminDemo2024!`
- Should Access: ThrillRing Gaming
- Should NOT Access: Other tenants' tournaments
- Test: Verify tournament data isolation

**Success Criteria:**
✅ Tenant admins see only their tenant's data
✅ Cannot access other tenants' features
✅ Appropriate features visible for their role
✅ No unauthorized access errors

---

#### Test 3.3: Standard User Access
**Objective:** Verify standard users have limited access

**Credentials:** `user@bizosaas.com` / `UserDemo2024!`

**Expected Access:**
- [ ] Client Portal - ✅ Own profile, limited features
- [ ] Bizoholic Frontend - ✅ Public content
- [ ] CoreLDove Storefront - ✅ Shopping features
- [ ] BizOSaaS Admin - ❌ Should redirect or show "Access Denied"
- [ ] Business Directory - ✅ Search, view listings
- [ ] ThrillRing Gaming - ✅ View tournaments, register
- [ ] Analytics Dashboard - ❌ Should redirect or show limited data

**Success Criteria:**
✅ Users can access appropriate platforms
✅ Admin features hidden from standard users
✅ No privilege escalation possible
✅ Clear error messages for unauthorized access

---

#### Test 3.4: Readonly User Access
**Objective:** Verify readonly users cannot modify data

**Credentials:** `analyst@bizosaas.com` / `UserDemo2024!`

**Test:**
1. Login as readonly user
2. Navigate to Analytics Dashboard
3. Verify dashboards are visible
4. Verify no edit/delete buttons
5. Try to modify data via direct API calls (should fail)

**Success Criteria:**
✅ Readonly users can view data
✅ No modification buttons visible
✅ API calls for modifications return 403 Forbidden
✅ Clear indication of readonly status

---

### Test Suite 4: Session Management (Priority: High)

#### Test 4.1: Session Persistence
**Objective:** Verify sessions survive page refresh

**Steps:**
1. Login to Client Portal
2. Navigate to dashboard
3. Refresh the page (F5)
4. Verify still logged in
5. Navigate to another platform
6. Refresh that page
7. Verify still logged in

**Success Criteria:**
✅ Session persists after page refresh
✅ User data loads correctly after refresh
✅ No "logged out" errors
✅ Fast session restoration (< 1 second)

---

#### Test 4.2: Token Refresh
**Objective:** Verify access tokens refresh automatically

**Steps:**
1. Login to any platform
2. Open browser DevTools → Network tab
3. Wait for access token to expire (~15 minutes)
4. Perform an authenticated action (navigate, API call)
5. Observe Network tab for refresh token request
6. Verify new access token received
7. Verify action completes successfully

**Success Criteria:**
✅ Access token refreshes automatically
✅ No user interruption during refresh
✅ Refresh happens before token expires
✅ No "unauthorized" errors during normal use

---

#### Test 4.3: Concurrent Sessions
**Objective:** Verify multiple browser windows share session

**Steps:**
1. Login to Client Portal in Chrome
2. Open new Chrome window
3. Navigate to Bizoholic Frontend
4. Verify logged in (SSO)
5. In first window, logout
6. In second window, perform action
7. Verify logged out in second window too

**Success Criteria:**
✅ Sessions shared across browser windows
✅ Logout propagates to all windows
✅ Login state synchronized
✅ No conflicts between windows

---

### Test Suite 5: Tenant Switching (Priority: Medium)

#### Test 5.1: Switch Tenant in Client Portal
**Objective:** Verify tenant switching works correctly

**Prerequisites:** User must have access to multiple tenants

**Steps:**
1. Login as super admin or multi-tenant user
2. Navigate to Client Portal
3. Open tenant switcher
4. Verify list of accessible tenants displayed
5. Select different tenant
6. Verify page reloads
7. Verify new tenant's data displayed
8. Navigate to other platforms
9. Verify tenant switch propagated

**Success Criteria:**
✅ Tenant list shows correct tenants
✅ Switch updates session
✅ New tenant data displayed
✅ Switch propagates to all platforms
✅ No data leakage between tenants

---

### Test Suite 6: Error Handling (Priority: Medium)

#### Test 6.1: Invalid Credentials
**Objective:** Verify proper error messages for failed login

**Steps:**
1. Navigate to login page
2. Enter invalid email: `invalid@example.com`
3. Enter any password
4. Submit login form
5. Verify error message displayed
6. Verify user NOT logged in
7. Verify no console errors

**Success Criteria:**
✅ Clear error message displayed
✅ Error message is user-friendly
✅ Login form remains accessible
✅ No system errors exposed

---

#### Test 6.2: Network Errors
**Objective:** Verify graceful handling of network issues

**Steps:**
1. Open DevTools → Network tab
2. Enable "Offline" mode
3. Try to login
4. Verify appropriate error message
5. Disable offline mode
6. Retry login
7. Verify login successful

**Success Criteria:**
✅ Network errors handled gracefully
✅ User-friendly error messages
✅ Retry mechanism works
✅ No app crashes

---

#### Test 6.3: Expired Session
**Objective:** Verify handling of expired sessions

**Steps:**
1. Login to platform
2. Manually delete cookies (DevTools → Application → Cookies)
3. Try to access protected route
4. Verify redirect to login
5. Verify clear error message about expired session

**Success Criteria:**
✅ Expired sessions detected
✅ User redirected to login
✅ Clear message about session expiration
✅ No infinite redirect loops

---

### Test Suite 7: Security Testing (Priority: Critical)

#### Test 7.1: XSS Protection
**Objective:** Verify tokens not exposed to XSS attacks

**Steps:**
1. Login to any platform
2. Open DevTools → Console
3. Try to access localStorage for tokens
4. Try to access sessionStorage for tokens
5. Verify access tokens NOT in storage
6. Check Application → Cookies
7. Verify refresh token is HttpOnly

**Success Criteria:**
✅ No access tokens in localStorage
✅ No access tokens in sessionStorage
✅ Refresh token is HttpOnly cookie
✅ Refresh token is Secure (HTTPS only)

---

#### Test 7.2: CSRF Protection
**Objective:** Verify CSRF attacks prevented

**Steps:**
1. Login to platform
2. Open DevTools → Application → Cookies
3. Note cookie attributes (SameSite, Secure, HttpOnly)
4. Verify SameSite attribute present
5. Try to make authenticated request from different domain
6. Verify request blocked

**Success Criteria:**
✅ Cookies have SameSite attribute
✅ Cookies have Secure flag (production)
✅ Cross-origin requests blocked
✅ Auth endpoints use CORS properly

---

#### Test 7.3: Token Expiration
**Objective:** Verify expired tokens handled correctly

**Steps:**
1. Login to platform
2. Wait for access token to expire (or manually expire)
3. Try to access protected API endpoint
4. Verify token refresh attempted
5. If refresh fails, verify redirect to login

**Success Criteria:**
✅ Expired tokens detected
✅ Automatic refresh attempted
✅ Fallback to login if refresh fails
✅ No sensitive data exposed

---

## Testing Tools & Scripts

### Manual Testing Checklist

Create a spreadsheet to track test results:

| Test ID | Test Name | Platform | Status | Notes |
|---------|-----------|----------|--------|-------|
| 1.1.1 | Login - Client Portal | Client Portal | ⏳ | |
| 1.1.2 | Login - Bizoholic | Bizoholic | ⏳ | |
| ... | ... | ... | ... | ... |

### Automated Testing Script (Future)

```typescript
// test/sso-integration.test.ts
describe('SSO Integration Tests', () => {
  test('Login on one platform logs in on all', async () => {
    // Test implementation
  });

  test('Logout on one platform logs out on all', async () => {
    // Test implementation
  });

  test('Tenant switching propagates correctly', async () => {
    // Test implementation
  });
});
```

---

## Test Execution Plan

### Phase 4.1: Basic Functionality (Day 1)
- [ ] Test Suite 1: Basic Authentication
- [ ] Test Suite 4: Session Management
- **Estimated Time:** 2-3 hours

### Phase 4.2: SSO Validation (Day 1-2)
- [ ] Test Suite 2: Single Sign-On
- [ ] Test Suite 5: Tenant Switching
- **Estimated Time:** 2-3 hours

### Phase 4.3: Security & RBAC (Day 2)
- [ ] Test Suite 3: Role-Based Access Control
- [ ] Test Suite 7: Security Testing
- **Estimated Time:** 3-4 hours

### Phase 4.4: Error Handling (Day 2-3)
- [ ] Test Suite 6: Error Handling
- [ ] Edge case testing
- **Estimated Time:** 2 hours

---

## Issue Tracking Template

When issues are found, use this template:

```markdown
## Issue: [Brief Description]

**Severity:** Critical / High / Medium / Low
**Test ID:** [e.g., 2.1]
**Platform:** [e.g., Client Portal]
**User Role:** [e.g., Super Admin]

**Steps to Reproduce:**
1.
2.
3.

**Expected Behavior:**


**Actual Behavior:**


**Screenshots:**


**Console Errors:**


**Fix Required:**

```

---

## Success Criteria for Phase 4 Completion

✅ **All Critical Tests Pass:**
- Login/Logout on all 7 platforms
- SSO login propagation
- SSO logout propagation
- Security tests (XSS, CSRF)

✅ **All High Priority Tests Pass:**
- RBAC for all user roles
- Session persistence
- Token refresh

✅ **Documentation Complete:**
- Test results documented
- Known issues logged
- Troubleshooting guide created

✅ **Ready for Production:**
- No critical bugs
- No high-priority bugs
- Medium/low bugs documented for future fix

---

## Next Steps After Testing

1. **Fix Critical Issues** - Address any blocker bugs
2. **Create User Documentation** - End-user guides for each platform
3. **Admin Training** - Train admins on managing users/tenants
4. **Production Deployment** - Deploy to staging → production
5. **Monitor** - Set up monitoring and alerting
6. **Iterate** - Gather feedback and improve

---

**Phase 4 Status:** Ready to Begin
**Estimated Duration:** 2-3 days
**Prerequisites:** ✅ All 7 frontends integrated
**Next Milestone:** Production-Ready SSO System

---

**Created:** November 16, 2025
**Last Updated:** November 16, 2025
