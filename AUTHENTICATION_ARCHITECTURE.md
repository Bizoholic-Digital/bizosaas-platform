# Authentication Architecture Clarification

## Current Setup: NextAuth.js + Authentik SSO (NOT Clerk)

### Executive Summary

**The BizOSaaS platform uses NextAuth.js with Authentik SSO for authentication. Clerk is NOT used anywhere in the platform.**

---

## Authentication Stack

### Primary Authentication: NextAuth.js

**Location**: `/bizosaas-brain-core/client-portal/app/api/auth/[...nextauth]/route.ts`

**Supported Providers**:
1. **Credentials Provider** (Email/Password)
   - Direct authentication via Brain Gateway
   - Supports multi-tenant login
   - Brand-specific authentication

2. **GitHub OAuth**
   - Social login via GitHub
   - Auto-registration on first login

3. **Google OAuth**
   - Social login via Google
   - Auto-registration on first login

4. **Authentik SSO** (Primary Enterprise SSO)
   - OIDC-based authentication
   - Centralized identity management
   - Single sign-on across all services

---

## Service-Level Authentication Configuration

### 1. Client Portal
**File**: `docker-compose.client-portal.yml`

```yaml
environment:
  - AUTHENTIK_ISSUER=https://auth-sso.bizoholic.net/application/o/bizosaas-platform/
  - AUTHENTIK_CLIENT_ID=bizosaas-portal
  - AUTHENTIK_CLIENT_SECRET=BizOSaaS2024!AuthentikSecret
```

### 2. Admin Portal
**File**: `docker-compose.admin-portal.yml`

```yaml
environment:
  - AUTHENTIK_ISSUER=https://auth-sso.bizoholic.net/application/o/bizosaas-platform/
  - AUTHENTIK_CLIENT_ID=bizosaas-portal
  - AUTHENTIK_CLIENT_SECRET=BizOSaaS2024!AuthentikSecret
```

### 3. Business Directory
**File**: `docker-compose.business-directory.yml`

```yaml
environment:
  - AUTHENTIK_ISSUER=https://auth-sso.bizoholic.net/application/o/bizosaas-platform/
  - AUTHENTIK_CLIENT_ID=bizosaas-portal
  - AUTHENTIK_CLIENT_SECRET=BizOSaaS2024!AuthentikSecret
```

### 4. Bizoholic Frontend
**File**: `docker-compose.bizoholic-frontend.yml`

```yaml
environment:
  - AUTHENTIK_CLIENT_ID=${AUTHENTIK_CLIENT_ID}
  - AUTHENTIK_CLIENT_SECRET=${AUTHENTIK_CLIENT_SECRET}
  - AUTHENTIK_ISSUER=${AUTHENTIK_ISSUER}
```

### 5. Lago Billing
**File**: `configs/docker-compose.lago.yml`

```yaml
environment:
  - OIDC_CLIENT_SECRET=BizOSaaS2024!AuthentikSecret
```

---

## Authentik SSO Configuration

### Authentik Instance
- **URL**: https://auth-sso.bizoholic.net
- **Admin Credentials**: 
  - Username: `akadmin`
  - Password: `Bizoholic2025!Admin`

### OIDC Application
- **Application Name**: bizosaas-platform
- **Client ID**: bizosaas-portal
- **Client Secret**: BizOSaaS2024!AuthentikSecret
- **Issuer**: https://auth-sso.bizoholic.net/application/o/bizosaas-platform/

### Integrated Services
All services use Authentik for SSO:
- ✅ Client Portal
- ✅ Admin Portal
- ✅ Business Directory
- ✅ Bizoholic Frontend
- ✅ Lago Billing
- ✅ Vault (configured separately)

---

## Why NOT Clerk?

### Investigation Results
1. **No Clerk packages found** in any `package.json` files
2. **No Clerk configuration** in environment variables
3. **No Clerk imports** in any TypeScript/JavaScript files
4. **No Clerk API keys** in credentials or Vault

### Historical Context
Based on conversation history (Conversation 268b921a: "Reverting Clerk Configuration"), there was a previous attempt to use Clerk, but it was reverted in favor of the current NextAuth.js + Authentik setup.

**Reason for reversion**: Clerk live API keys were not working as expected, and the demo configuration was causing issues with the login form.

---

## Authentication Flow

### Standard Login Flow (Credentials)
```
User → Client Portal Login Page
  ↓
NextAuth.js Credentials Provider
  ↓
Brain Gateway /auth/sso/login
  ↓
PostgreSQL (user verification)
  ↓
JWT Token Generated
  ↓
Session Created
  ↓
Redirect to Dashboard
```

### SSO Login Flow (Authentik)
```
User → Client Portal Login Page
  ↓
"Sign in with Authentik" button
  ↓
Redirect to Authentik (auth-sso.bizoholic.net)
  ↓
User authenticates with Authentik
  ↓
OIDC callback to NextAuth.js
  ↓
JWT Token Generated
  ↓
Session Created
  ↓
Redirect to Dashboard
```

### Social Login Flow (GitHub/Google)
```
User → Client Portal Login Page
  ↓
"Sign in with GitHub/Google" button
  ↓
OAuth flow with provider
  ↓
NextAuth.js receives profile
  ↓
Brain Gateway /api/auth/social-login
  ↓
Auto-register or link existing user
  ↓
JWT Token Generated
  ↓
Session Created
  ↓
Redirect to Dashboard
```

---

## Recommendation

### ✅ **Use Only Authentik SSO**

**Reasons**:
1. **Already Implemented**: Fully configured and working
2. **Self-Hosted**: No external dependencies or costs
3. **Enterprise-Grade**: Supports OIDC, SAML, LDAP
4. **Centralized**: Single source of truth for all identities
5. **Integrated**: Works with Vault, Lago, and all portals
6. **Flexible**: Supports multiple authentication backends

### ❌ **Do NOT Add Clerk**

**Reasons**:
1. **Redundant**: Authentik already provides all SSO features
2. **Cost**: Clerk charges per user ($0.02/MAU after 10k users)
3. **Complexity**: Adding another auth provider increases maintenance
4. **Lock-in**: Vendor lock-in vs self-hosted Authentik
5. **Historical Issues**: Previous attempt failed and was reverted

---

## Current Status

| Service | Auth Method | Status |
|---------|-------------|--------|
| Client Portal | NextAuth.js + Authentik | ✅ Working |
| Admin Portal | NextAuth.js + Authentik | ✅ Working |
| Business Directory | NextAuth.js + Authentik | ✅ Working |
| Bizoholic Frontend | NextAuth.js + Authentik | ✅ Working |
| Lago Billing | Authentik OIDC | ✅ Working |
| Vault | Authentik OIDC | ✅ Working |
| Brain Gateway | JWT (issued by NextAuth) | ✅ Working |

---

## Credentials Reference

All Authentik credentials are stored in:
1. **Vault**: `secret/authentik`
2. **credentials.md**: Section "Authentik SSO"

---

## Conclusion

**The platform exclusively uses NextAuth.js with Authentik SSO. Clerk is not used and should not be added.**

This architecture provides:
- ✅ Enterprise-grade SSO
- ✅ Self-hosted control
- ✅ Zero per-user costs
- ✅ Full integration with all services
- ✅ Multiple authentication methods (credentials, OAuth, OIDC)

**No changes to authentication architecture are recommended.**
