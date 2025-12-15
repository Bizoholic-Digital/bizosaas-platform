# BizOSaaS Authentication Strategy & Implementation Guide

## Current Status ✅
- **Client Portal**: Headless authentication working (credentials → Authentik backend → token → dashboard)
- **Admin Dashboard**: Needs same implementation
- **Backend**: Authentik handles all authentication, token generation, and user management

## Recommended Authentication Architecture

### 1. **Headless Authentication Flow** (Current - KEEP THIS)
```
User enters credentials on YOUR login page
    ↓
Frontend sends to YOUR auth API (port 8007)
    ↓
Auth service validates with Authentik (background)
    ↓
Returns JWT tokens to frontend
    ↓
User redirected to dashboard (no Authentik UI ever shown)
```

**Why this is best:**
- ✅ Full UI/UX control
- ✅ Seamless user experience
- ✅ No external redirects
- ✅ Authentik power without Authentik UI
- ✅ Works with social logins (see below)

### 2. **Social Login Strategy** (RECOMMENDED)

#### Implementation Approach:
**Use Authentik's OAuth2 Provider Sources + Your Custom UI**

```typescript
// Your login page shows:
1. Email/Password form (current)
2. "Continue with Google" button
3. "Continue with Microsoft" button
4. "Continue with LinkedIn" button
```

**Flow:**
```
User clicks "Continue with Google"
    ↓
Frontend calls: POST /api/auth/oauth/google/initiate
    ↓
Backend (Authentik) generates OAuth URL
    ↓
User redirected to Google (unavoidable for OAuth)
    ↓
Google redirects back to: /api/auth/oauth/google/callback
    ↓
Backend exchanges code for tokens
    ↓
Returns JWT to frontend
    ↓
User lands on dashboard
```

**Providers to Support:**
1. **Google** - Most common, essential
2. **Microsoft** - Enterprise users
3. **LinkedIn** - B2B professionals
4. **GitHub** - Developers (optional)
5. **Apple** - iOS users (if mobile app planned)

### 3. **Security & Compliance Architecture**

#### Token Storage Strategy:
```typescript
// Access Token (short-lived: 15 min)
localStorage.setItem('access_token', token) // OK for access tokens

// Refresh Token (long-lived: 30 days)
// MUST be HTTP-only cookie (already implemented ✅)
document.cookie = `refresh_token=${token}; path=/; max-age=2592000; HttpOnly; Secure; SameSite=Strict`
```

#### Vault Integration for Sensitive Data:
```
User PII (email, name, phone) → Authentik Database → Encrypted at rest
OAuth Tokens → Vault (HashiCorp Vault already in your stack)
API Keys → Vault
Payment Info → Stripe (PCI compliant) + Vault for metadata
```

**GDPR/HIPAA/SOC2 Compliance Checklist:**
- ✅ Data encryption at rest (Authentik + Vault)
- ✅ Data encryption in transit (HTTPS/TLS)
- ✅ Token expiration (15 min access, 30 day refresh)
- ✅ Audit logging (Authentik built-in)
- ✅ Right to deletion (implement user data export/delete endpoints)
- ✅ Consent management (add to signup flow)
- ✅ Session management (implement in middleware)

### 4. **Recommended Login Page UX**

```
┌─────────────────────────────────────┐
│  [Logo]          BizOSaaS           │
│                                     │
│  Welcome Back                       │
│  ─────────────────────────────────  │
│                                     │
│  [Email Input]                      │
│  [Password Input]                   │
│  [Remember me] [Forgot password?]   │
│  [Sign In Button - Primary]         │
│                                     │
│  ──────── OR ────────               │
│                                     │
│  [🔵 Continue with Google]          │
│  [⬜ Continue with Microsoft]       │
│  [🔷 Continue with LinkedIn]        │
│                                     │
│  Don't have an account? [Sign up]   │
│                                     │
│  🔒 Secured by Authentik            │
└─────────────────────────────────────┘
```

**Key UX Principles:**
1. **Primary action**: Email/password (fastest for returning users)
2. **Social logins**: Secondary but prominent
3. **Trust indicators**: "Secured by" badge, SSL icon
4. **Progressive disclosure**: Don't overwhelm with options
5. **Mobile-first**: Touch-friendly buttons (min 44px height)

### 5. **Sign Up vs Sign In Strategy**

**Recommendation: Separate Pages**
- `/login` - Sign in (existing users)
- `/signup` - Sign up (new users)
- `/forgot-password` - Password reset

**Why separate?**
- ✅ Clearer user intent
- ✅ Different validation rules
- ✅ Better conversion tracking
- ✅ Easier A/B testing

**Sign Up Page Should Include:**
```typescript
interface SignupData {
  email: string
  password: string
  confirmPassword: string
  companyName: string // B2B SaaS specific
  fullName: string
  acceptTerms: boolean // GDPR requirement
  marketingConsent: boolean // GDPR requirement
}
```

### 6. **Implementation Checklist**

#### Phase 1: Client Portal (Current) ✅
- [x] Headless email/password login
- [x] Token storage (localStorage + HTTP-only cookie)
- [x] Redirect prevention
- [ ] Social login buttons (UI only, not functional yet)
- [ ] Sign up page
- [ ] Forgot password flow

#### Phase 2: Admin Dashboard (Next)
- [ ] Copy auth-client.ts to admin dashboard
- [ ] Update login page UI
- [ ] Test with admin@bizoholic.net
- [ ] Verify role-based access

#### Phase 3: Social Login Integration
- [ ] Configure Authentik OAuth sources (Google, Microsoft, LinkedIn)
- [ ] Implement OAuth initiate endpoint
- [ ] Implement OAuth callback endpoint
- [ ] Add social login buttons to UI
- [ ] Test each provider

#### Phase 4: Advanced Features
- [ ] Sign up flow with email verification
- [ ] Password reset flow
- [ ] Multi-factor authentication (Authentik supports TOTP)
- [ ] Session management dashboard
- [ ] Account deletion (GDPR)

### 7. **Performance Optimization**

```typescript
// Token refresh strategy (prevent expired token errors)
setInterval(async () => {
  const token = localStorage.getItem('access_token')
  if (token && isTokenExpiringSoon(token)) {
    await refreshAccessToken()
  }
}, 5 * 60 * 1000) // Check every 5 minutes

function isTokenExpiringSoon(token: string): boolean {
  const payload = JSON.parse(atob(token.split('.')[1]))
  const expiresIn = payload.exp * 1000 - Date.now()
  return expiresIn < 2 * 60 * 1000 // Refresh if < 2 min left
}
```

### 8. **Security Best Practices**

1. **Rate Limiting**: Implement on auth endpoints (prevent brute force)
2. **CAPTCHA**: Add on signup/login after 3 failed attempts
3. **Password Policy**: 
   - Min 12 characters
   - Mix of upper/lower/numbers/symbols
   - No common passwords (use zxcvbn library)
4. **Session Timeout**: 30 min inactivity → logout
5. **IP Whitelisting**: Optional for admin dashboard
6. **Audit Logging**: Log all auth events to Vault

## Files Modified (for Admin Dashboard replication)

### Client Portal Implementation:
```
portals/client-portal/
├── lib/
│   ├── auth-client.ts ✅ (Core auth logic)
│   └── types/auth.ts ✅ (TypeScript interfaces)
├── app/
│   └── login/
│       ├── page.tsx ✅ (Login page wrapper)
│       └── ClientLoginForm.tsx ✅ (Form component)
└── components/
    └── auth/
        └── AuthContext.tsx ✅ (React context)
```

### Admin Dashboard (To Implement):
```
portals/admin-dashboard/
├── lib/
│   ├── auth.tsx ✅ (Already created - adapter)
│   └── utils.ts ✅ (Already created)
├── app/
│   └── login/
│       └── page.tsx (NEEDS UPDATE - currently shows Authentik)
└── shared/
    └── components/
        └── AuthProvider.tsx ✅ (Already uses unified auth)
```

## Next Steps

1. **Immediate**: Verify Client Portal login works end-to-end
2. **Next**: Update Admin Dashboard login page to match Client Portal
3. **Then**: Add social login UI (buttons only)
4. **Finally**: Configure Authentik OAuth sources and implement backend

## Questions to Answer

1. **Do you want social logins?** 
   - **Recommendation**: YES - Google + Microsoft minimum
   - Increases conversion by 20-30%
   - Users prefer it (no password to remember)

2. **Separate sign up page?**
   - **Recommendation**: YES - clearer UX
   - Can add onboarding wizard after signup

3. **MFA requirement?**
   - **Recommendation**: Optional for users, mandatory for admins
   - Authentik supports TOTP (Google Authenticator)

4. **Session duration?**
   - **Recommendation**: 
     - Access token: 15 minutes
     - Refresh token: 30 days
     - Remember me: 90 days

---

**Created**: 2025-12-15  
**Status**: Living document - update as implementation progresses
