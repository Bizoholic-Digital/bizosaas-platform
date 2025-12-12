# Authentik SSO Integration for Admin Dashboard
## Architecture V4 - RBAC & Authentication

**Date**: 2025-12-11  
**Purpose**: Integrate Authentik for SSO and RBAC in admin dashboard

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION FLOW                       │
│                                                              │
│  ┌──────────────┐                                           │
│  │    User      │                                           │
│  │  (Browser)   │                                           │
│  └──────┬───────┘                                           │
│         │ 1. Access admin dashboard                         │
│         ↓                                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Admin Dashboard (Next.js - Port 3004)               │  │
│  │  - Check auth cookie                                  │  │
│  │  - If not authenticated → redirect to Authentik      │  │
│  └──────┬───────────────────────────────────────────────┘  │
│         │ 2. Redirect to Authentik                          │
│         ↓                                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Authentik (SSO Server - Port 9000)                  │  │
│  │  - User login                                         │  │
│  │  - MFA (if enabled)                                   │  │
│  │  - Issue JWT token with roles                        │  │
│  └──────┬───────────────────────────────────────────────┘  │
│         │ 3. Redirect back with token                       │
│         ↓                                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Admin Dashboard                                      │  │
│  │  - Validate token with Brain Gateway                 │  │
│  │  - Check user role (platform_admin/super_admin)      │  │
│  │  - Set auth cookie                                    │  │
│  └──────┬───────────────────────────────────────────────┘  │
│         │ 4. All API calls via Brain Gateway               │
│         ↓                                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Brain Gateway (FastAPI - Port 8000)                 │  │
│  │  - Validate JWT token                                │  │
│  │  - Extract user roles                                │  │
│  │  - Enforce RBAC                                       │  │
│  │  - Route to services                                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Steps

### Step 1: Configure Authentik Application

**Create OAuth2/OIDC Provider in Authentik**:

1. Login to Authentik: `http://localhost:9000`
2. Go to **Applications** → **Providers** → **Create**
3. Select **OAuth2/OpenID Provider**
4. Configure:
   ```
   Name: BizOSaaS Admin Dashboard
   Client Type: Confidential
   Client ID: bizosaas-admin-dashboard
   Client Secret: <generate-secure-secret>
   Redirect URIs: http://localhost:3004/api/auth/callback
   Scopes: openid, profile, email, groups
   ```

5. Create Application:
   ```
   Name: BizOSaaS Admin Dashboard
   Slug: bizosaas-admin-dashboard
   Provider: <select provider created above>
   ```

6. Create Groups:
   ```
   - platform_admin (can manage tenants, view metrics)
   - super_admin (full access, can manage AI agents, system settings)
   ```

7. Assign Users to Groups

---

### Step 2: Admin Dashboard - NextAuth.js Integration

**Install Dependencies**:
```bash
cd portals/admin-dashboard
npm install next-auth @auth/core
```

**Create Auth Configuration** (`lib/auth.ts`):
```typescript
import NextAuth from "next-auth";
import type { NextAuthConfig } from "next-auth";

export const authConfig: NextAuthConfig = {
  providers: [
    {
      id: "authentik",
      name: "Authentik",
      type: "oidc",
      issuer: process.env.AUTHENTIK_ISSUER || "http://localhost:9000/application/o/bizosaas-admin-dashboard/",
      clientId: process.env.AUTHENTIK_CLIENT_ID || "bizosaas-admin-dashboard",
      clientSecret: process.env.AUTHENTIK_CLIENT_SECRET || "",
      authorization: {
        params: {
          scope: "openid profile email groups",
        },
      },
      profile(profile) {
        return {
          id: profile.sub,
          name: profile.name,
          email: profile.email,
          image: profile.picture,
          roles: profile.groups || [],
        };
      },
    },
  ],
  callbacks: {
    async jwt({ token, user, account }) {
      if (account && user) {
        token.accessToken = account.access_token;
        token.roles = user.roles;
      }
      return token;
    },
    async session({ session, token }) {
      session.accessToken = token.accessToken as string;
      session.user.roles = token.roles as string[];
      return session;
    },
    async authorized({ auth, request }) {
      const { pathname } = request.nextUrl;
      
      // Public routes
      if (pathname === "/login" || pathname === "/unauthorized") {
        return true;
      }
      
      // Check if user is authenticated
      if (!auth?.user) {
        return false;
      }
      
      // Check if user has admin role
      const roles = auth.user.roles || [];
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
};

export const { handlers, auth, signIn, signOut } = NextAuth(authConfig);
```

**Create API Route** (`app/api/auth/[...nextauth]/route.ts`):
```typescript
import { handlers } from "@/lib/auth";

export const { GET, POST } = handlers;
```

**Create Middleware** (`middleware.ts`):
```typescript
import { auth } from "@/lib/auth";

export default auth((req) => {
  const { pathname } = req.nextUrl;
  
  // Public routes
  if (pathname === "/login" || pathname === "/unauthorized") {
    return;
  }
  
  // Check authentication
  if (!req.auth) {
    const url = new URL("/login", req.url);
    url.searchParams.set("callbackUrl", pathname);
    return Response.redirect(url);
  }
  
  // Check authorization
  const roles = req.auth.user?.roles || [];
  const hasAdminRole = roles.includes("platform_admin") || roles.includes("super_admin");
  
  if (!hasAdminRole) {
    return Response.redirect(new URL("/unauthorized", req.url));
  }
});

export const config = {
  matcher: [
    "/((?!api/auth|_next/static|_next/image|favicon.ico|login|unauthorized).*)",
  ],
};
```

**Create Login Page** (`app/login/page.tsx`):
```typescript
import { signIn } from "@/lib/auth";
import { Button } from "@/components/ui/button";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950">
      <div className="max-w-md w-full space-y-8 p-8 bg-white dark:bg-gray-900 rounded-lg shadow-lg">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
            BizOSaaS Admin
          </h2>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Platform Administration Dashboard
          </p>
        </div>
        
        <form
          action={async () => {
            "use server";
            await signIn("authentik");
          }}
        >
          <Button type="submit" className="w-full">
            Sign in with SSO
          </Button>
        </form>
      </div>
    </div>
  );
}
```

**Create Unauthorized Page** (`app/unauthorized/page.tsx`):
```typescript
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function UnauthorizedPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950">
      <div className="max-w-md w-full space-y-8 p-8 bg-white dark:bg-gray-900 rounded-lg shadow-lg text-center">
        <h2 className="text-3xl font-bold text-red-600">Access Denied</h2>
        <p className="text-gray-600 dark:text-gray-400">
          You don't have permission to access the admin dashboard.
          Please contact your administrator.
        </p>
        <Link href="/login">
          <Button>Back to Login</Button>
        </Link>
      </div>
    </div>
  );
}
```

**Update Environment Variables** (`.env.local`):
```env
# Authentik SSO
AUTHENTIK_ISSUER=http://localhost:9000/application/o/bizosaas-admin-dashboard/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<your-secret-here>
AUTH_SECRET=<generate-with-openssl-rand-base64-32>

# Brain Gateway
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://localhost:8000
```

---

### Step 3: Brain Gateway - JWT Validation

**Create Auth Middleware** (`app/middleware/auth.py`):
```python
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import httpx
from typing import List, Optional

security = HTTPBearer()

class AuthMiddleware:
    def __init__(self, authentik_url: str):
        self.authentik_url = authentik_url
        self.jwks_url = f"{authentik_url}/.well-known/jwks.json"
        self.jwks_cache = None
    
    async def get_jwks(self):
        """Fetch JWKS from Authentik"""
        if not self.jwks_cache:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.jwks_url)
                self.jwks_cache = response.json()
        return self.jwks_cache
    
    async def verify_token(
        self,
        credentials: HTTPAuthorizationCredentials = Security(security)
    ) -> dict:
        """Verify JWT token and return user info"""
        token = credentials.credentials
        
        try:
            # Get JWKS
            jwks = await self.get_jwks()
            
            # Decode and verify token
            # Note: In production, use proper JWT verification with JWKS
            decoded = jwt.decode(
                token,
                options={"verify_signature": False}  # TODO: Implement proper verification
            )
            
            return {
                "user_id": decoded.get("sub"),
                "email": decoded.get("email"),
                "name": decoded.get("name"),
                "roles": decoded.get("groups", []),
            }
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    def require_role(self, required_roles: List[str]):
        """Decorator to require specific roles"""
        async def role_checker(
            credentials: HTTPAuthorizationCredentials = Security(security)
        ):
            user = await self.verify_token(credentials)
            user_roles = user.get("roles", [])
            
            if not any(role in user_roles for role in required_roles):
                raise HTTPException(
                    status_code=403,
                    detail=f"Required roles: {required_roles}"
                )
            
            return user
        
        return role_checker

# Initialize
auth_middleware = AuthMiddleware(
    authentik_url="http://localhost:9000/application/o/bizosaas-admin-dashboard"
)
```

**Update Admin Router** (`app/routers/admin.py`):
```python
from fastapi import APIRouter, Depends
from app.middleware.auth import auth_middleware

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/tenants")
async def list_tenants(
    user: dict = Depends(auth_middleware.require_role(["platform_admin", "super_admin"]))
):
    """List all tenants - requires platform_admin or super_admin role"""
    # Implementation
    return {"tenants": []}

@router.get("/agents/fine-tune")
async def get_agent_fine_tuning(
    user: dict = Depends(auth_middleware.require_role(["super_admin"]))
):
    """Get agent fine-tuning settings - requires super_admin role"""
    # Implementation
    return {"settings": {}}
```

---

### Step 4: API Client with Auth

**Update API Client** (`lib/api-client.ts`):
```typescript
import axios from 'axios';
import { getSession } from 'next-auth/react';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth interceptor
apiClient.interceptors.request.use(async (config) => {
  const session = await getSession();
  
  if (session?.accessToken) {
    config.headers.Authorization = `Bearer ${session.accessToken}`;
  }
  
  return config;
});

// Add error interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

---

## Role-Based Access Control Matrix

| Feature | Tenant User | Tenant Admin | Platform Admin | Super Admin |
|---------|-------------|--------------|----------------|-------------|
| View Dashboard | ❌ | ❌ | ✅ | ✅ |
| Manage Tenants | ❌ | ❌ | ✅ | ✅ |
| View Metrics | ❌ | ❌ | ✅ | ✅ |
| Manage AI Agents | ❌ | ❌ | ❌ | ✅ |
| Fine-tune Agents | ❌ | ❌ | ❌ | ✅ |
| System Settings | ❌ | ❌ | ❌ | ✅ |
| Feature Flags | ❌ | ❌ | ❌ | ✅ |
| Audit Logs | ❌ | ❌ | ✅ | ✅ |

---

## Testing

### Test Authentication Flow

1. Start Authentik: `docker compose up authentik`
2. Start Brain Gateway: `uvicorn main:app --reload --port 8000`
3. Start Admin Dashboard: `npm run dev` (port 3004)
4. Navigate to `http://localhost:3004`
5. Should redirect to Authentik login
6. Login with admin credentials
7. Should redirect back to dashboard
8. Verify JWT token in cookies
9. Test API calls to Brain Gateway

### Test RBAC

1. Create test users with different roles
2. Login as `platform_admin`
3. Verify access to tenant management
4. Verify NO access to agent fine-tuning
5. Login as `super_admin`
6. Verify access to all features

---

## Security Considerations

1. **JWT Verification**: Implement proper JWT signature verification using JWKS
2. **Token Refresh**: Implement token refresh flow
3. **HTTPS**: Use HTTPS in production
4. **Secure Cookies**: Set `secure`, `httpOnly`, `sameSite` flags
5. **CSRF Protection**: Enable CSRF protection
6. **Rate Limiting**: Add rate limiting to auth endpoints
7. **Audit Logging**: Log all authentication attempts

---

## Next Steps

1. [ ] Configure Authentik application
2. [ ] Install NextAuth.js dependencies
3. [ ] Create auth configuration
4. [ ] Create login/unauthorized pages
5. [ ] Implement middleware
6. [ ] Update Brain Gateway with JWT validation
7. [ ] Test authentication flow
8. [ ] Test RBAC
9. [ ] Deploy to staging
