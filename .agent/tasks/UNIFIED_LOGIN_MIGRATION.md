# Unified Login Component Migration Plan

## 📋 Overview

Migrate both Admin Dashboard and Client Portal to use the shared `UnifiedLoginForm` component for consistent authentication UX across all portals.

## 🎯 Objectives

1. ✅ Replace portal-specific login pages with shared component
2. ✅ Maintain existing authentication functionality (SSO for admin, credentials for client)
3. ✅ Ensure no breaking changes to authentication flow
4. ✅ Improve maintainability and consistency

## 📦 Prerequisites

- [x] Shared UI package created (`packages/shared-ui`)
- [x] UnifiedLoginForm component implemented
- [x] Admin Dashboard working with SSO
- [x] Client Portal working with credentials
- [ ] TypeScript configuration for monorepo imports
- [ ] Test both authentication flows

---

## 🔧 Phase 1: Setup Monorepo Configuration

### Task 1.1: Configure TypeScript Path Aliases

**File**: Root `tsconfig.json`

**Action**: Add path mapping for shared package

```json
{
  "compilerOptions": {
    "paths": {
      "@bizosaas/shared-ui": ["./packages/shared-ui"],
      "@bizosaas/shared-ui/*": ["./packages/shared-ui/*"]
    }
  }
}
```

**Verification**: TypeScript can resolve `@bizosaas/shared-ui` imports

---

### Task 1.2: Update Portal TypeScript Configs

**Files**: 
- `portals/admin-dashboard/tsconfig.json`
- `portals/client-portal/tsconfig.json`

**Action**: Extend root config and add shared-ui reference

```json
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"],
      "@bizosaas/shared-ui": ["../../packages/shared-ui"]
    }
  }
}
```

**Verification**: No TypeScript errors when importing from `@bizosaas/shared-ui`

---

### Task 1.3: Update Next.js Configurations

**Files**:
- `portals/admin-dashboard/next.config.js`
- `portals/client-portal/next.config.js`

**Action**: Add transpilePackages for shared-ui

```javascript
const nextConfig = {
  transpilePackages: ['@bizosaas/shared-ui'],
  // ... existing config
}
```

**Verification**: Next.js can compile shared-ui package

---

## 🎨 Phase 2: Migrate Admin Dashboard

### Task 2.1: Create New Login Page with UnifiedLoginForm

**File**: `portals/admin-dashboard/app/login/page.tsx`

**Action**: Replace existing login page

```typescript
import { signIn } from "@/lib/auth";
import { UnifiedLoginForm } from "@bizosaas/shared-ui";
import { PlatformBranding } from "@/components/ui/platform-branding";

export default function AdminLoginPage({
  searchParams,
}: {
  searchParams: { callbackUrl?: string };
}) {
  return (
    <UnifiedLoginForm
      mode="sso"
      platformName="Admin Dashboard"
      platformSubtitle="Platform Administration & Management"
      ssoProviderName="Authentik"
      ssoProviderId="authentik"
      defaultRedirectUrl="/dashboard"
      BrandingComponent={() => <PlatformBranding platform="BIZOSAAS" size="lg" />}
      onSSOLogin={async () => {
        "use server";
        await signIn("authentik", {
          redirectTo: searchParams.callbackUrl || "/dashboard",
        });
      }}
    />
  );
}
```

**Verification Steps**:
1. Navigate to `https://admin.bizoholic.net/login`
2. Verify SSO button is displayed
3. Click "Sign in with Authentik"
4. Verify redirect to Authentik SSO
5. After authentication, verify redirect to dashboard
6. Check that unauthorized users are redirected to login

**Rollback Plan**: Keep backup of original file as `page.tsx.backup`

---

### Task 2.2: Test Admin Authentication Flow

**Test Cases**:

1. **Unauthenticated Access**
   - [ ] Visit `/dashboard` → Redirects to `/login`
   - [ ] Visit `/login` → Shows SSO login page
   - [ ] No credentials form visible (SSO only)

2. **SSO Login**
   - [ ] Click "Sign in with Authentik"
   - [ ] Redirects to Authentik
   - [ ] After auth, returns to admin dashboard
   - [ ] Session persists on refresh

3. **Protected Routes**
   - [ ] `/api/health` → Accessible without auth ✅
   - [ ] `/dashboard` → Requires auth
   - [ ] `/tenants` → Requires auth
   - [ ] `/settings` → Requires auth

4. **Logout**
   - [ ] Logout button works
   - [ ] Redirects to login page
   - [ ] Cannot access protected routes

**Success Criteria**: All test cases pass

---

## 👥 Phase 3: Migrate Client Portal

### Task 3.1: Create Client Login Wrapper Component

**File**: `portals/client-portal/app/login/ClientLoginForm.tsx`

**Action**: Create client component wrapper

```typescript
'use client'

import { signIn } from 'next-auth/react'
import { UnifiedLoginForm } from '@bizosaas/shared-ui'
import { PlatformBranding } from '@/components/ui/platform-branding'

export function ClientLoginForm() {
  return (
    <UnifiedLoginForm
      mode="credentials"
      platformName="Client Portal"
      platformSubtitle="Access your projects and services"
      defaultRedirectUrl="/"
      showDemoCredentials={process.env.NODE_ENV === 'development'}
      BrandingComponent={() => <PlatformBranding platform="BIZOHOLIC" size="lg" />}
      onCredentialsLogin={async (email, password) => {
        const result = await signIn('credentials', {
          email,
          password,
          redirect: false,
        })
        
        return {
          ok: result?.ok || false,
          error: result?.error || 'Invalid credentials',
        }
      }}
    />
  )
}
```

**Why Wrapper?**: Client Portal uses client-side auth, needs 'use client' directive

---

### Task 3.2: Update Login Page

**File**: `portals/client-portal/app/login/page.tsx`

**Action**: Use the wrapper component

```typescript
import { ClientLoginForm } from './ClientLoginForm'

export default function LoginPage() {
  return <ClientLoginForm />
}
```

**Verification Steps**:
1. Navigate to client portal login
2. Verify email/password form is displayed
3. Verify demo credentials are shown (dev mode)
4. Test login with valid credentials
5. Verify redirect to home page
6. Test login with invalid credentials
7. Verify error message is displayed

**Rollback Plan**: Keep backup of original components

---

### Task 3.3: Test Client Authentication Flow

**Test Cases**:

1. **Unauthenticated Access**
   - [ ] Visit `/dashboard` → Redirects to `/login`
   - [ ] Visit `/login` → Shows credentials form
   - [ ] No SSO button visible (credentials only)

2. **Credentials Login**
   - [ ] Enter valid email/password
   - [ ] Click "Sign In"
   - [ ] Redirects to home page
   - [ ] Session persists on refresh

3. **Invalid Credentials**
   - [ ] Enter invalid email/password
   - [ ] Click "Sign In"
   - [ ] Error message displayed
   - [ ] Stays on login page

4. **Demo Credentials** (Dev Mode)
   - [ ] Demo credentials box visible
   - [ ] Pre-filled email/password work
   - [ ] Can override with custom credentials

5. **Remember Me**
   - [ ] Check "Remember me"
   - [ ] Login successful
   - [ ] Session persists longer

**Success Criteria**: All test cases pass

---

## 🧹 Phase 4: Cleanup and Optimization

### Task 4.1: Remove Old Login Components

**Files to Archive/Remove**:
- `portals/client-portal/components/auth/LoginForm.tsx`
- `portals/client-portal/components/auth/login-form.tsx`
- `portals/client-portal/components/auth/login-form-original.tsx`

**Action**: 
1. Move to `_archive/` folder (don't delete yet)
2. Update any imports if needed
3. Verify no broken imports

**Verification**: `npm run build` succeeds for both portals

---

### Task 4.2: Update Documentation

**Files to Update**:
- `README.md` (root)
- `portals/admin-dashboard/README.md`
- `portals/client-portal/README.md`

**Action**: Document the shared login component usage

**Content**:
```markdown
## Authentication

Both portals use the shared `UnifiedLoginForm` component from `@bizosaas/shared-ui`.

### Admin Dashboard
- **Mode**: SSO only (Authentik)
- **Access**: Platform administrators only

### Client Portal  
- **Mode**: Credentials (email/password)
- **Access**: All registered users
```

---

### Task 4.3: Add E2E Tests

**File**: `tests/e2e/auth.spec.ts`

**Action**: Create automated tests for both portals

```typescript
describe('Authentication', () => {
  describe('Admin Dashboard', () => {
    it('should redirect to SSO login', async () => {
      // Test SSO flow
    })
  })
  
  describe('Client Portal', () => {
    it('should login with credentials', async () => {
      // Test credentials flow
    })
  })
})
```

---

## 🚀 Phase 5: Deployment

### Task 5.1: Deploy to Staging

**Steps**:
1. Merge to `staging` branch
2. Trigger Dokploy deployment
3. Wait for build completion
4. Run smoke tests

**Verification**:
- [ ] Admin Dashboard login works on staging
- [ ] Client Portal login works on staging
- [ ] No console errors
- [ ] No broken styles

---

### Task 5.2: Production Deployment

**Prerequisites**:
- [ ] All staging tests passed
- [ ] Code review completed
- [ ] Backup plan ready

**Steps**:
1. Merge `staging` to `main`
2. Tag release: `v1.1.0-unified-login`
3. Deploy to production
4. Monitor for errors

**Rollback Plan**:
```bash
# If issues occur
git revert <commit-hash>
git push origin main
# Redeploy via Dokploy
```

---

## 📊 Success Metrics

### Functional Requirements
- [ ] Admin Dashboard SSO login works
- [ ] Client Portal credentials login works
- [ ] All protected routes require authentication
- [ ] Public routes (like `/api/health`) remain accessible
- [ ] Session management works correctly
- [ ] Logout functionality works

### Non-Functional Requirements
- [ ] No increase in bundle size (shared code reduces duplication)
- [ ] Login page loads in < 1 second
- [ ] No TypeScript errors
- [ ] No ESLint warnings
- [ ] Consistent UI/UX across portals

### Code Quality
- [ ] Code duplication reduced
- [ ] Maintainability improved
- [ ] Type safety maintained
- [ ] Documentation updated

---

## 🐛 Troubleshooting Guide

### Issue: Import errors for @bizosaas/shared-ui

**Solution**:
```bash
# Clear Next.js cache
rm -rf .next
rm -rf node_modules/.cache

# Rebuild
npm run build
```

### Issue: Styles not loading

**Solution**:
- Verify `transpilePackages` in next.config.js
- Check CSS imports in UnifiedLoginForm
- Clear browser cache

### Issue: SSO redirect loop

**Solution**:
- Check `NEXTAUTH_URL` environment variable
- Verify Authentik callback URL configuration
- Check middleware public routes

### Issue: Credentials login fails

**Solution**:
- Verify credentials provider in NextAuth config
- Check API endpoint `/api/auth/callback/credentials`
- Verify database connection

---

## 📅 Timeline

| Phase | Tasks | Estimated Time | Dependencies |
|-------|-------|----------------|--------------|
| Phase 1 | Monorepo Setup | 30 minutes | None |
| Phase 2 | Admin Migration | 1 hour | Phase 1 |
| Phase 3 | Client Migration | 1 hour | Phase 1 |
| Phase 4 | Cleanup | 30 minutes | Phase 2, 3 |
| Phase 5 | Deployment | 1 hour | Phase 4 |
| **Total** | | **4 hours** | |

---

## 🎯 Next Steps

1. **Review this plan** - Confirm approach and timeline
2. **Start Phase 1** - Configure monorepo TypeScript paths
3. **Test incrementally** - Verify each phase before proceeding
4. **Deploy to staging** - Test in production-like environment
5. **Production deployment** - Roll out to users

---

## 📝 Notes

- Keep original login pages as backups until migration is verified
- Test on both desktop and mobile browsers
- Monitor error logs during deployment
- Have rollback plan ready at each phase
- Document any issues encountered for future reference

---

**Created**: 2025-12-12  
**Status**: Ready for Implementation  
**Priority**: High  
**Assigned**: Development Team
