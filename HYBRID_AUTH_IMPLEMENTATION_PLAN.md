# Hybrid Auth Implementation Plan - NextAuth + FastAPI via Brain Gateway

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                            │
│                    Port 3003 - Unified Dashboard                 │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    NextAuth.js                            │  │
│  │  - Session Management (JWT/Database)                      │  │
│  │  - Social Providers (GitHub, Google)                      │  │
│  │  - Credentials Provider → Brain Gateway                   │  │
│  └────────────────────┬─────────────────────────────────────┘  │
└────────────────────────┼──────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Brain AI Gateway (FastAPI)                          │
│              Port 8000 - Centralized Routing                     │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  /api/auth/* endpoints                                    │  │
│  │  - Proxy to Auth Service                                  │  │
│  │  - Token validation                                       │  │
│  │  - Session synchronization                                │  │
│  └────────────────────┬─────────────────────────────────────┘  │
└────────────────────────┼──────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Auth Service (FastAPI)                              │
│              Port 8008 - SSO Authentication                      │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  - User authentication                                    │  │
│  │  - JWT token generation                                   │  │
│  │  - Role & permission management                           │  │
│  │  - Multi-tenant support                                   │  │
│  │  - OAuth integration                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Authentication Flow

### 1. Email/Password Login
```
User enters credentials
  ↓
NextAuth Credentials Provider
  ↓
POST /api/auth/callback/credentials
  ↓
Brain Gateway: POST /api/auth/login
  ↓
Auth Service: Validate credentials
  ↓
Returns: { user, access_token, refresh_token }
  ↓
Brain Gateway: Forward to NextAuth
  ↓
NextAuth: Create session with JWT
  ↓
Store in session: { user, access_token, refresh_token }
  ↓
Redirect to dashboard
```

### 2. Social Login (GitHub/Google)
```
User clicks "Sign in with GitHub"
  ↓
NextAuth GitHub Provider
  ↓
OAuth flow with GitHub
  ↓
GitHub returns user profile
  ↓
NextAuth callback
  ↓
Brain Gateway: POST /api/auth/social-login
  ↓
Auth Service: Create/update user from OAuth
  ↓
Returns: { user, access_token, refresh_token }
  ↓
NextAuth: Create session
  ↓
Redirect to dashboard
```

### 3. Session Validation
```
User navigates to protected page
  ↓
NextAuth checks session
  ↓
If valid JWT: Allow access
  ↓
If expired: Refresh token via Brain Gateway
  ↓
Brain Gateway: POST /api/auth/refresh
  ↓
Auth Service: Validate refresh token
  ↓
Returns new access_token
  ↓
Update NextAuth session
  ↓
Continue navigation
```

## Implementation

### 1. NextAuth Configuration

**File:** `/portals/client-portal/app/api/auth/[...nextauth]/route.ts`

```typescript
import NextAuth, { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import GithubProvider from 'next-auth/providers/github';
import GoogleProvider from 'next-auth/providers/google';

const BRAIN_GATEWAY_URL = process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8000';

export const authOptions: NextAuthOptions = {
  providers: [
    // Credentials Provider - Email/Password via Brain Gateway
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
        brand: { label: "Brand", type: "text" }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          throw new Error('Email and password required');
        }

        try {
          // Call Brain Gateway which proxies to Auth Service
          const response = await fetch(`${BRAIN_GATEWAY_URL}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              email: credentials.email,
              password: credentials.password,
              brand: credentials.brand || 'bizoholic'
            })
          });

          if (!response.ok) {
            throw new Error('Invalid credentials');
          }

          const data = await response.json();

          // Return user object with tokens
          return {
            id: data.user.id,
            email: data.user.email,
            name: `${data.user.first_name} ${data.user.last_name}`,
            role: data.user.role,
            tenant_id: data.user.tenant_id,
            brand: credentials.brand || 'bizoholic',
            access_token: data.access_token,
            refresh_token: data.refresh_token
          };
        } catch (error) {
          console.error('Auth error:', error);
          return null;
        }
      }
    }),

    // GitHub Provider
    GithubProvider({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
      authorization: {
        params: {
          scope: 'read:user user:email'
        }
      }
    }),

    // Google Provider
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      authorization: {
        params: {
          prompt: "consent",
          access_type: "offline",
          response_type: "code"
        }
      }
    })
  ],

  callbacks: {
    // JWT Callback - Add custom fields to token
    async jwt({ token, user, account, profile }) {
      // Initial sign in
      if (user) {
        token.id = user.id;
        token.role = user.role;
        token.tenant_id = user.tenant_id;
        token.brand = user.brand;
        token.access_token = user.access_token;
        token.refresh_token = user.refresh_token;
      }

      // Handle social login
      if (account?.provider === 'github' || account?.provider === 'google') {
        try {
          // Register/login user via Brain Gateway
          const response = await fetch(`${BRAIN_GATEWAY_URL}/api/auth/social-login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              provider: account.provider,
              provider_id: account.providerAccountId,
              email: profile?.email,
              name: profile?.name,
              avatar: profile?.image,
              access_token: account.access_token
            })
          });

          if (response.ok) {
            const data = await response.json();
            token.id = data.user.id;
            token.role = data.user.role;
            token.tenant_id = data.user.tenant_id;
            token.brand = data.user.brand || 'bizoholic';
            token.access_token = data.access_token;
            token.refresh_token = data.refresh_token;
          }
        } catch (error) {
          console.error('Social login error:', error);
        }
      }

      // Check if token needs refresh
      if (token.access_token) {
        const tokenExpiry = (token as any).exp || 0;
        const now = Math.floor(Date.now() / 1000);
        
        // Refresh if token expires in less than 5 minutes
        if (tokenExpiry - now < 300) {
          try {
            const response = await fetch(`${BRAIN_GATEWAY_URL}/api/auth/refresh`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                refresh_token: token.refresh_token
              })
            });

            if (response.ok) {
              const data = await response.json();
              token.access_token = data.access_token;
            }
          } catch (error) {
            console.error('Token refresh error:', error);
          }
        }
      }

      return token;
    },

    // Session Callback - Add custom fields to session
    async session({ session, token }) {
      if (token) {
        session.user.id = token.id as string;
        session.user.role = token.role as string;
        session.user.tenant_id = token.tenant_id as string;
        session.user.brand = token.brand as string;
        session.access_token = token.access_token as string;
        session.refresh_token = token.refresh_token as string;
      }
      return session;
    },

    // Redirect Callback - Handle post-login redirects
    async redirect({ url, baseUrl }) {
      // Allow relative URLs
      if (url.startsWith('/')) return `${baseUrl}${url}`;
      // Allow same origin URLs
      if (new URL(url).origin === baseUrl) return url;
      return baseUrl;
    }
  },

  pages: {
    signIn: '/login',
    error: '/login',
  },

  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },

  secret: process.env.NEXTAUTH_SECRET,
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
```

### 2. Brain Gateway Auth Proxy

**File:** `/shared/services/brain-gateway/app/routers/auth.py`

```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import httpx
from typing import Optional

router = APIRouter(prefix="/api/auth", tags=["auth"])

AUTH_SERVICE_URL = "http://localhost:8008"

class LoginRequest(BaseModel):
    email: str
    password: str
    brand: Optional[str] = "bizoholic"

class SocialLoginRequest(BaseModel):
    provider: str
    provider_id: str
    email: str
    name: Optional[str]
    avatar: Optional[str]
    access_token: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/login")
async def login(request: LoginRequest):
    """
    Proxy login request to Auth Service
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/auth/login",
                json={
                    "email": request.email,
                    "password": request.password,
                    "brand": request.brand
                },
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/social-login")
async def social_login(request: SocialLoginRequest):
    """
    Handle social login via Auth Service
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/auth/social-login",
                json={
                    "provider": request.provider,
                    "provider_id": request.provider_id,
                    "email": request.email,
                    "name": request.name,
                    "avatar": request.avatar,
                    "access_token": request.access_token
                },
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=400, detail="Social login failed")

@router.post("/refresh")
async def refresh_token(request: RefreshTokenRequest):
    """
    Refresh access token via Auth Service
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/auth/refresh",
                json={"refresh_token": request.refresh_token},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.post("/logout")
async def logout(access_token: str = Depends(get_current_token)):
    """
    Logout user via Auth Service
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/auth/logout",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10.0
            )
            response.raise_for_status()
            return {"message": "Logged out successfully"}
        except httpx.HTTPError as e:
            raise HTTPException(status_code=400, detail="Logout failed")

@router.get("/me")
async def get_current_user(access_token: str = Depends(get_current_token)):
    """
    Get current user info via Auth Service
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/auth/me",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=401, detail="Unauthorized")

def get_current_token(authorization: str = Header(None)):
    """
    Extract token from Authorization header
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    return authorization.split(" ")[1]
```

### 3. Unified Login Component

**File:** `/portals/client-portal/app/login/page.tsx`

```typescript
'use client';

import { useState, useEffect } from 'react';
import { signIn } from 'next-auth/react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Github, Mail as Google, Lock, Mail } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';

// Brand configuration
const BRANDS = {
  bizoholic: {
    name: 'Bizoholic Digital',
    tagline: 'Digital Marketing Excellence',
    logo: '/brands/bizoholic/logo.png',
    primaryColor: '#2563eb',
  },
  coreldove: {
    name: 'CoreLDove',
    tagline: 'E-commerce Made Simple',
    logo: '/brands/coreldove/logo.png',
    primaryColor: '#dc2626',
  },
  thrillring: {
    name: 'ThrillRing',
    tagline: 'Entertainment & Events',
    logo: '/brands/thrillring/logo.png',
    primaryColor: '#7c3aed',
  },
  quanttrade: {
    name: 'QuantTrade',
    tagline: 'Algorithmic Trading Platform',
    logo: '/brands/quanttrade/logo.png',
    primaryColor: '#059669',
  },
  'business-directory': {
    name: 'Business Directory',
    tagline: 'Connect Local Businesses',
    logo: '/brands/directory/logo.png',
    primaryColor: '#ea580c',
  },
};

type Brand = keyof typeof BRANDS;

export default function UnifiedLoginPage() {
  const [brand, setBrand] = useState<Brand>('bizoholic');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  const router = useRouter();
  const searchParams = useSearchParams();

  // Detect brand from URL or localStorage
  useEffect(() => {
    const brandParam = searchParams?.get('brand') as Brand;
    const storedBrand = localStorage.getItem('selected_brand') as Brand;
    
    if (brandParam && BRANDS[brandParam]) {
      setBrand(brandParam);
      localStorage.setItem('selected_brand', brandParam);
    } else if (storedBrand && BRANDS[storedBrand]) {
      setBrand(storedBrand);
    }
  }, [searchParams]);

  const handleCredentialsLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const result = await signIn('credentials', {
        email,
        password,
        brand,
        redirect: false,
      });

      if (result?.error) {
        setError('Invalid credentials. Please try again.');
      } else if (result?.ok) {
        router.push('/');
        router.refresh();
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSocialLogin = async (provider: 'github' | 'google') => {
    setIsLoading(true);
    await signIn(provider, {
      callbackUrl: '/',
      redirect: true,
    });
  };

  const brandConfig = BRANDS[brand];

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 px-4">
      <Card className="w-full max-w-md shadow-xl">
        <CardHeader className="text-center space-y-4">
          {/* Brand Logo */}
          <div className="mx-auto h-16 w-16 flex items-center justify-center rounded-full" 
               style={{ backgroundColor: `${brandConfig.primaryColor}20` }}>
            <div className="text-3xl font-bold" style={{ color: brandConfig.primaryColor }}>
              {brandConfig.name.charAt(0)}
            </div>
          </div>
          
          <div>
            <CardTitle className="text-2xl font-bold">{brandConfig.name}</CardTitle>
            <p className="text-sm text-muted-foreground mt-1">{brandConfig.tagline}</p>
          </div>

          {/* Brand Switcher */}
          <div className="flex flex-wrap gap-2 justify-center">
            {Object.keys(BRANDS).map((b) => (
              <button
                key={b}
                onClick={() => {
                  setBrand(b as Brand);
                  localStorage.setItem('selected_brand', b);
                }}
                className={`px-3 py-1 text-xs rounded-full transition-all ${
                  brand === b
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {BRANDS[b as Brand].name}
              </button>
            ))}
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Social Login */}
          <div className="grid grid-cols-2 gap-3">
            <Button
              variant="outline"
              onClick={() => handleSocialLogin('github')}
              disabled={isLoading}
              className="w-full"
            >
              <Github className="h-4 w-4 mr-2" />
              GitHub
            </Button>
            <Button
              variant="outline"
              onClick={() => handleSocialLogin('google')}
              disabled={isLoading}
              className="w-full"
            >
              <Google className="h-4 w-4 mr-2" />
              Google
            </Button>
          </div>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <Separator />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-white dark:bg-gray-950 px-2 text-muted-foreground">
                Or continue with email
              </span>
            </div>
          </div>

          {/* Email/Password Form */}
          <form onSubmit={handleCredentialsLogin} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  id="email"
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="pl-10"
                  required
                  disabled={isLoading}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-10"
                  required
                  disabled={isLoading}
                />
              </div>
            </div>

            {error && (
              <div className="rounded-md bg-red-50 dark:bg-red-900/20 p-3">
                <p className="text-sm text-red-800 dark:text-red-200">{error}</p>
              </div>
            )}

            <Button
              type="submit"
              className="w-full"
              disabled={isLoading}
              style={{ backgroundColor: brandConfig.primaryColor }}
            >
              {isLoading ? 'Signing in...' : 'Sign in to Dashboard'}
            </Button>
          </form>

          {/* Demo Credentials */}
          <Card className="bg-blue-50 dark:bg-blue-950 border-blue-200 dark:border-blue-800">
            <CardContent className="p-3">
              <p className="text-xs font-semibold text-blue-800 dark:text-blue-200 mb-1">
                Demo Credentials
              </p>
              <div className="text-xs text-blue-700 dark:text-blue-300 space-y-1">
                <div><strong>Admin:</strong> admin@bizoholic.com / AdminDemo2024!</div>
                <div><strong>Client:</strong> client@bizosaas.com / ClientDemo2024!</div>
              </div>
            </CardContent>
          </Card>
        </CardContent>
      </Card>
    </div>
  );
}
```

### 4. Type Definitions

**File:** `/portals/client-portal/types/next-auth.d.ts`

```typescript
import 'next-auth';

declare module 'next-auth' {
  interface User {
    id: string;
    email: string;
    name: string;
    role: string;
    tenant_id: string;
    brand: string;
    access_token: string;
    refresh_token: string;
  }

  interface Session {
    user: {
      id: string;
      email: string;
      name: string;
      role: string;
      tenant_id: string;
      brand: string;
    };
    access_token: string;
    refresh_token: string;
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    id: string;
    role: string;
    tenant_id: string;
    brand: string;
    access_token: string;
    refresh_token: string;
  }
}
```

## Environment Variables

**File:** `/portals/client-portal/.env.local`

```bash
# NextAuth Configuration
NEXTAUTH_URL=http://localhost:3003
NEXTAUTH_SECRET=your-super-secret-key-change-in-production

# Brain Gateway
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://localhost:8000

# GitHub OAuth
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## Benefits of Hybrid Approach

1. ✅ **Best of Both Worlds**
   - NextAuth: Session management, social login, JWT handling
   - FastAPI: Centralized auth logic, multi-tenant, RBAC

2. ✅ **Centralized Control**
   - All auth logic in Auth Service
   - Brain Gateway as single entry point
   - Consistent across all brands

3. ✅ **Social Login Support**
   - GitHub, Google via NextAuth
   - Synced with FastAPI backend
   - Single source of truth

4. ✅ **Token Management**
   - JWT tokens from FastAPI
   - Stored in NextAuth session
   - Auto-refresh via Brain Gateway

5. ✅ **Multi-Brand Support**
   - Brand detection in login
   - Brand context in session
   - Brand-specific features

## Next Steps

1. ✅ Install NextAuth dependencies
2. ✅ Create NextAuth API route
3. ✅ Update Brain Gateway with auth proxy
4. ✅ Create unified login component
5. ✅ Add social OAuth apps (GitHub, Google)
6. ✅ Test authentication flow
7. ✅ Implement RBAC dashboard

Ready to implement?
