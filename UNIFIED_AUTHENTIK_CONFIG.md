# Single Authentik Instance - Unified SSO Configuration
## Multi-Tenant, Multi-Portal, Single Sign-On Architecture

**Date**: 2025-12-11  
**Status**: ✅ Reusing Existing Authentik Implementation  
**Architecture**: Single Authentik → Multiple Applications → Multi-Tenant Support

---

## 🎯 Architecture Overview

### Single Authentik Instance Serves:

```
┌────────────────────────────────────────────────────────────────────┐
│                    SINGLE AUTHENTIK INSTANCE                       │
│                    (sso.bizoholic.net / localhost:9000)            │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  OAuth2/OIDC Provider                                        │ │
│  │  - Multi-tenant support via groups                           │ │
│  │  - SSO for all applications                                  │ │
│  │  - MFA support                                               │ │
│  │  - User management                                           │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  Applications:                                                     │
│  ┌────────────────┬────────────────┬────────────────────────────┐ │
│  │ Client Portal  │ Admin Dashboard│ Brain Gateway API          │ │
│  │ (Port 3003)    │ (Port 3004)    │ (Port 8000)                │ │
│  │ Tenant Users   │ Platform Admins│ API Validation             │ │
│  └────────────────┴────────────────┴────────────────────────────┘ │
│                                                                    │
│  Groups (Multi-Tenant + Roles):                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ • super_admin (Platform-wide access)                       │  │
│  │ • platform_admin (Platform management)                     │  │
│  │ • tenant_{tenant_id}_admin (Tenant admin)                  │  │
│  │ • tenant_{tenant_id}_user (Tenant user)                    │  │
│  └────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Current Implementation Analysis

### ✅ Client Portal (Already Configured)

**File**: `portals/client-portal/app/api/auth/[...nextauth]/route.ts`

**Configuration**:
```typescript
AuthentikProvider({
    name: 'BizOSaaS SSO',
    clientId: process.env.AUTHENTIK_CLIENT_ID,
    clientSecret: process.env.AUTHENTIK_CLIENT_SECRET,
    issuer: process.env.AUTHENTIK_ISSUER || `${AUTHENTIK_URL}/application/o/bizosaas/`,
})
```

**Features**:
- ✅ SSO via Authentik
- ✅ Hybrid auth (SSO + Credentials fallback)
- ✅ Multi-tenant support via groups
- ✅ Role mapping from Authentik groups
- ✅ Production URL: `https://sso.bizoholic.net`

**Environment Variables**:
```env
AUTHENTIK_URL=https://sso.bizoholic.net
AUTHENTIK_CLIENT_ID=<client-portal-client-id>
AUTHENTIK_CLIENT_SECRET=<client-portal-secret>
AUTHENTIK_ISSUER=https://sso.bizoholic.net/application/o/bizosaas/
```

---

### ✅ Admin Dashboard (Just Implemented)

**File**: `portals/admin-dashboard/lib/auth.ts`

**Configuration**:
```typescript
{
    id: "authentik",
    name: "Authentik SSO",
    type: "oidc",
    issuer: process.env.AUTHENTIK_ISSUER || "http://localhost:9000/application/o/bizosaas-admin/",
    clientId: process.env.AUTHENTIK_CLIENT_ID || "bizosaas-admin-dashboard",
    clientSecret: process.env.AUTHENTIK_CLIENT_SECRET || "",
}
```

**Features**:
- ✅ SSO via Authentik
- ✅ RBAC (platform_admin, super_admin)
- ✅ Protected routes via middleware
- ✅ JWT token management

**Environment Variables** (to update):
```env
AUTHENTIK_ISSUER=https://sso.bizoholic.net/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<admin-dashboard-secret>
```

---

## 🔧 Unified Configuration Strategy

### Single Authentik Instance with Multiple Applications

**Authentik Applications to Configure**:

1. **BizOSaaS Client Portal**
   - Slug: `bizosaas`
   - Client ID: `bizosaas-client-portal`
   - Redirect URIs:
     - Local: `http://localhost:3003/api/auth/callback/authentik`
     - VPS: `https://app.bizoholic.net/api/auth/callback/authentik`
   - Groups: `tenant_{tenant_id}_admin`, `tenant_{tenant_id}_user`

2. **BizOSaaS Admin Dashboard**
   - Slug: `bizosaas-admin`
   - Client ID: `bizosaas-admin-dashboard`
   - Redirect URIs:
     - Local: `http://localhost:3004/api/auth/callback/authentik`
     - VPS: `https://admin.bizoholic.net/api/auth/callback/authentik`
   - Groups: `super_admin`, `platform_admin`

3. **Brain Gateway API**
   - Slug: `bizosaas-api`
   - Client ID: `bizosaas-brain-gateway`
   - Redirect URIs: N/A (API only, token validation)
   - Groups: All (validates tokens from all applications)

---

## 🏗️ Multi-Tenant Group Structure

### Group Naming Convention

```
Format: {role_type}_{tenant_id}_{role}

Examples:
- super_admin (platform-wide)
- platform_admin (platform management)
- tenant_acme_admin (Acme Corp admin)
- tenant_acme_user (Acme Corp user)
- tenant_techstart_admin (TechStart LLC admin)
- tenant_techstart_user (TechStart LLC user)
```

### Group Attributes

**Super Admin**:
```json
{
  "permissions": ["*"],
  "access_level": "platform",
  "can_manage_tenants": true,
  "can_configure_agents": true
}
```

**Platform Admin**:
```json
{
  "permissions": ["tenants:*", "monitoring:*", "analytics:*"],
  "access_level": "platform",
  "can_manage_tenants": true,
  "can_configure_agents": false
}
```

**Tenant Admin**:
```json
{
  "permissions": ["tenant:manage", "users:manage", "integrations:manage"],
  "access_level": "tenant",
  "tenant_id": "acme",
  "can_manage_users": true
}
```

**Tenant User**:
```json
{
  "permissions": ["tenant:view", "dashboard:view"],
  "access_level": "tenant",
  "tenant_id": "acme",
  "can_manage_users": false
}
```

---

## 🔄 Updated Admin Dashboard Configuration

### Update to Match Client Portal Pattern

**File**: `portals/admin-dashboard/lib/auth.ts`

```typescript
import NextAuth from "next-auth";
import type { NextAuthConfig } from "next-auth";

// Use same Authentik URL as client portal
const AUTHENTIK_URL = process.env.AUTHENTIK_URL || process.env.NEXT_PUBLIC_SSO_URL || 'https://sso.bizoholic.net';

export const authConfig: NextAuthConfig = {
  providers: [
    {
      id: "authentik",
      name: "BizOSaaS SSO",
      type: "oidc",
      // Use same base URL, different application slug
      issuer: process.env.AUTHENTIK_ISSUER || `${AUTHENTIK_URL}/application/o/bizosaas-admin/`,
      clientId: process.env.AUTHENTIK_CLIENT_ID || "bizosaas-admin-dashboard",
      clientSecret: process.env.AUTHENTIK_CLIENT_SECRET || "",
      authorization: {
        params: {
          scope: "openid profile email groups",
        },
        url: `${AUTHENTIK_URL}/application/o/authorize/`,
      },
      token: `${AUTHENTIK_URL}/application/o/token/`,
      userinfo: `${AUTHENTIK_URL}/application/o/userinfo/`,
      profile(profile) {
        // Map Authentik groups to roles
        const groups = profile.groups || [];
        const roles = groups.filter((g: string) => 
          g === 'super_admin' || g === 'platform_admin'
        );
        
        return {
          id: profile.sub,
          name: profile.name,
          email: profile.email,
          image: profile.picture,
          roles: roles,
          tenant_id: profile.tenant_id,
        };
      },
    },
  ],
  callbacks: {
    async jwt({ token, user, account, profile }) {
      if (account && user) {
        token.accessToken = account.access_token;
        token.roles = user.roles;
        token.tenant_id = user.tenant_id;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.accessToken = token.accessToken as string;
        session.user.roles = token.roles as string[];
        session.user.tenant_id = token.tenant_id as string;
      }
      return session;
    },
    async authorized({ auth, request }) {
      const { pathname } = request.nextUrl;
      
      // Public routes
      if (pathname === "/login" || pathname === "/unauthorized" || pathname.startsWith("/api/auth")) {
        return true;
      }
      
      // Check if user is authenticated
      if (!auth?.user) {
        return false;
      }
      
      // Check if user has admin role
      const roles = (auth.user as any).roles || [];
      const hasAdminRole = roles.includes("platform_admin") || roles.includes("super_admin");
      
      if (!hasAdminRole) {
        return Response.redirect(new URL("/unauthorized", request.url));
      }
      
      return true;
    },
  },
  pages: {
    signIn: "/login",
    error: "/login",
  },
  session: {
    strategy: "jwt",
  },
  trustHost: true,
};

export const { handlers, auth, signIn, signOut } = NextAuth(authConfig);
```

---

## 📝 Environment Variables (Unified)

### Local Development

**Admin Dashboard** (`.env.local`):
```env
# Authentik SSO Configuration (Same instance as client portal)
AUTHENTIK_URL=http://localhost:9000
NEXT_PUBLIC_SSO_URL=http://localhost:9000
AUTHENTIK_ISSUER=http://localhost:9000/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<get-from-authentik>
AUTH_SECRET=<generate-with-openssl-rand-base64-32>

# Brain Gateway
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://localhost:8000

# NextAuth
NEXTAUTH_URL=http://localhost:3004
NEXTAUTH_URL_INTERNAL=http://localhost:3004
```

**Client Portal** (`.env.local`):
```env
# Authentik SSO Configuration (Same instance)
AUTHENTIK_URL=http://localhost:9000
NEXT_PUBLIC_SSO_URL=http://localhost:9000
AUTHENTIK_ISSUER=http://localhost:9000/application/o/bizosaas/
AUTHENTIK_CLIENT_ID=bizosaas-client-portal
AUTHENTIK_CLIENT_SECRET=<get-from-authentik>
AUTH_SECRET=<same-as-admin-or-different>

# Brain Gateway
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://localhost:8000

# NextAuth
NEXTAUTH_URL=http://localhost:3003
NEXTAUTH_URL_INTERNAL=http://localhost:3003
```

### VPS Production

**Admin Dashboard** (`.env.production`):
```env
# Authentik SSO Configuration (Same instance as client portal)
AUTHENTIK_URL=https://sso.bizoholic.net
NEXT_PUBLIC_SSO_URL=https://sso.bizoholic.net
AUTHENTIK_ISSUER=https://sso.bizoholic.net/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<from-vault>
AUTH_SECRET=<from-vault>

# Brain Gateway
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.net

# NextAuth
NEXTAUTH_URL=https://admin.bizoholic.net
NEXTAUTH_URL_INTERNAL=https://admin.bizoholic.net
```

**Client Portal** (`.env.production`):
```env
# Authentik SSO Configuration (Same instance)
AUTHENTIK_URL=https://sso.bizoholic.net
NEXT_PUBLIC_SSO_URL=https://sso.bizoholic.net
AUTHENTIK_ISSUER=https://sso.bizoholic.net/application/o/bizosaas/
AUTHENTIK_CLIENT_ID=bizosaas-client-portal
AUTHENTIK_CLIENT_SECRET=<from-vault>
AUTH_SECRET=<from-vault>

# Brain Gateway
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.net

# NextAuth
NEXTAUTH_URL=https://app.bizoholic.net
NEXTAUTH_URL_INTERNAL=https://app.bizoholic.net
```

---

## 🚀 Implementation Steps

### Step 1: Start Authentik (Local)

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas-brain-core
docker compose -f docker-compose.authentik.yml up -d

# Wait for ready
docker compose -f docker-compose.authentik.yml logs -f authentik-server
# Look for: "Application startup complete"
```

**Access**: `http://localhost:9000`

---

### Step 2: Configure Authentik Applications

#### Application 1: Client Portal (Already Exists - Verify)

**Check if exists**: Applications → Applications → Look for "BizOSaaS" or "bizosaas"

**If exists**: Verify settings match
**If not exists**: Create new application

**Settings**:
```
Name: BizOSaaS Client Portal
Slug: bizosaas
Provider: Create new OAuth2/OIDC Provider
  - Client ID: bizosaas-client-portal
  - Client Secret: <generate>
  - Redirect URIs:
    - http://localhost:3003/api/auth/callback/authentik
    - https://app.bizoholic.net/api/auth/callback/authentik
  - Scopes: openid, profile, email, groups
```

#### Application 2: Admin Dashboard (New)

**Create new application**:
```
Name: BizOSaaS Admin Dashboard
Slug: bizosaas-admin
Provider: Create new OAuth2/OIDC Provider
  - Client ID: bizosaas-admin-dashboard
  - Client Secret: <generate>
  - Redirect URIs:
    - http://localhost:3004/api/auth/callback/authentik
    - https://admin.bizoholic.net/api/auth/callback/authentik
  - Scopes: openid, profile, email, groups
```

---

### Step 3: Create/Verify Groups

**Platform-Level Groups**:
```
1. super_admin
   - Attributes: {"permissions": ["*"], "access_level": "platform"}

2. platform_admin
   - Attributes: {"permissions": ["tenants:*", "monitoring:*"], "access_level": "platform"}
```

**Tenant-Level Groups** (Example):
```
3. tenant_acme_admin
   - Attributes: {"tenant_id": "acme", "permissions": ["tenant:manage"], "access_level": "tenant"}

4. tenant_acme_user
   - Attributes: {"tenant_id": "acme", "permissions": ["tenant:view"], "access_level": "tenant"}
```

---

### Step 4: Update Admin Dashboard Configuration

**File**: `portals/admin-dashboard/lib/auth.ts`

Replace with the updated configuration above (matches client portal pattern).

---

### Step 5: Update Environment Variables

```bash
# Admin Dashboard
cd portals/admin-dashboard
cp .env.example .env.local
# Edit .env.local with Authentik credentials from Step 2

# Verify Client Portal
cd ../client-portal
# Check .env.local has correct Authentik configuration
```

---

### Step 6: Test Both Portals

**Test Admin Dashboard**:
```bash
cd portals/admin-dashboard
npm run dev
# Navigate to http://localhost:3004
# Should redirect to Authentik
# Login with super_admin or platform_admin user
# Should redirect back to dashboard
```

**Test Client Portal**:
```bash
cd portals/client-portal
npm run dev
# Navigate to http://localhost:3003
# Should redirect to Authentik
# Login with tenant user
# Should redirect back to portal
```

---

## 🎯 Multi-Tenant Flow

### User Login Flow

```
1. User navigates to portal (admin or client)
   ↓
2. Portal redirects to Authentik
   ↓
3. User logs in to Authentik
   ↓
4. Authentik validates credentials
   ↓
5. Authentik returns user info + groups
   ↓
6. Portal extracts:
   - Roles from groups (super_admin, platform_admin, etc.)
   - Tenant ID from group name (tenant_acme_admin → tenant_id: acme)
   ↓
7. Portal creates session with:
   - User info
   - Roles
   - Tenant ID
   ↓
8. Portal shows appropriate UI based on:
   - Role (admin vs user)
   - Tenant ID (tenant-specific data)
```

---

## ✅ Success Criteria

- [ ] Authentik running on localhost:9000
- [ ] Client portal application configured in Authentik
- [ ] Admin dashboard application configured in Authentik
- [ ] Groups created (super_admin, platform_admin, tenant groups)
- [ ] Test users assigned to groups
- [ ] Admin dashboard `.env.local` updated
- [ ] Admin dashboard login via Authentik working
- [ ] Client portal login via Authentik working
- [ ] Multi-tenant isolation working
- [ ] VPS configuration documented

---

## 📊 Next Steps

### Immediate (Today)
1. ✅ Start Authentik locally
2. ✅ Configure admin dashboard application in Authentik
3. ✅ Update admin dashboard auth configuration
4. ✅ Update environment variables
5. ✅ Test admin dashboard login
6. ✅ Test client portal login
7. ✅ Verify multi-tenant isolation

### Short-term (This Week)
1. ⏳ Update startup script to include Authentik
2. ⏳ Document VPS deployment
3. ⏳ Test end-to-end flows
4. ⏳ Add tenant creation workflow

### Medium-term (Next Week)
1. ⏳ Deploy to VPS
2. ⏳ Configure SSL/TLS
3. ⏳ Backup Authentik database
4. ⏳ Production testing

---

## 🎉 Conclusion

**Single Authentik Instance Benefits**:
- ✅ One SSO for all applications
- ✅ Centralized user management
- ✅ Multi-tenant support via groups
- ✅ Same configuration local + VPS
- ✅ Simplified maintenance
- ✅ Better security (one auth system)

**Next Command**:
```bash
# Start Authentik
cd bizosaas-brain-core
docker compose -f docker-compose.authentik.yml up -d

# Configure applications in Authentik UI
# http://localhost:9000
```
