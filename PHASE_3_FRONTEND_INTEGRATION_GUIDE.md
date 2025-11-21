# Phase 3: Frontend Authentication Integration Guide

**Purpose:** Systematic guide for integrating centralized auth into all BizOSaaS frontends
**Reference Implementation:** Client Portal (fully integrated)
**Estimated Time Per Frontend:** 2-4 hours

---

## Prerequisites

Before integrating any frontend, ensure:
- ✅ Auth service is running at `https://api.bizoholic.com/auth`
- ✅ You have the auth API endpoints documented
- ✅ Client Portal implementation is working (reference)

---

## Integration Steps (All Frontends)

### Step 1: Install Dependencies

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/[FRONTEND_NAME]

# For Next.js frontends
npm install --save axios js-cookie

# For React/Vite frontends
npm install --save axios js-cookie react-router-dom
```

### Step 2: Create Auth Types

**File:** `src/types/auth.ts` (or `lib/auth/types.ts` for Next.js)

```typescript
export interface User {
  id: string
  email: string
  first_name?: string
  last_name?: string
  role: 'super_admin' | 'tenant_admin' | 'user' | 'readonly' | 'agent'
  tenant_id: string
  is_active: boolean
  is_verified: boolean
  last_login_at?: string
  allowed_services?: string[]
}

export interface Tenant {
  id: string
  name: string
  slug: string
  status: 'active' | 'suspended' | 'trial' | 'cancelled'
  allowed_platforms?: string[]
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface SignupData {
  email: string
  password: string
  first_name?: string
  last_name?: string
  tenant_id?: string
}

export interface AuthResponse {
  user: User
  access_token?: string
}
```

### Step 3: Create Auth Client

**File:** `src/lib/auth/auth-client.ts` (or `src/services/auth.ts`)

```typescript
import axios from 'axios'
import Cookies from 'js-cookie'
import type { User, Tenant, LoginCredentials, SignupData, AuthResponse } from './types'

const API_URL = process.env.NEXT_PUBLIC_AUTH_API_URL ||
                process.env.REACT_APP_AUTH_API_URL ||
                'https://api.bizoholic.com/auth'

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true, // Important for cookie-based auth
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests if using JWT
api.interceptors.request.use((config) => {
  const token = Cookies.get('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authClient = {
  /**
   * Login with email/password
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await api.post('/jwt/login', credentials)

    // Store token in cookie
    if (response.data.access_token) {
      Cookies.set('access_token', response.data.access_token, {
        expires: 7, // 7 days
        secure: true,
        sameSite: 'lax'
      })
    }

    return response.data
  },

  /**
   * Register new user
   */
  async signup(data: SignupData): Promise<AuthResponse> {
    const response = await api.post('/register', data)
    return response.data
  },

  /**
   * Logout current user
   */
  async logout(): Promise<void> {
    try {
      await api.post('/jwt/logout')
    } finally {
      Cookies.remove('access_token')
    }
  },

  /**
   * Get current authenticated user
   */
  async getCurrentUser(): Promise<{ user: User } | null> {
    try {
      const response = await api.get('/users/me')
      return { user: response.data }
    } catch (error) {
      return null
    }
  },

  /**
   * Get user's tenants
   */
  async getTenants(): Promise<Tenant[]> {
    try {
      const response = await api.get('/tenants')
      return response.data
    } catch (error) {
      return []
    }
  },

  /**
   * Switch to different tenant
   */
  async switchTenant(tenantId: string): Promise<void> {
    await api.put(`/tenants/${tenantId}/switch`)
  },

  /**
   * Request password reset
   */
  async forgotPassword(email: string): Promise<void> {
    await api.post('/forgot-password', { email })
  },

  /**
   * Reset password with token
   */
  async resetPassword(token: string, password: string): Promise<void> {
    await api.post('/reset-password', { token, password })
  }
}
```

### Step 4: Create Auth Context (React/Next.js)

**File:** `src/lib/auth/AuthContext.tsx` (or `src/contexts/AuthContext.tsx`)

```typescript
'use client' // For Next.js 13+ App Router

import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { useRouter } from 'next/navigation' // or 'react-router-dom'
import { authClient, type LoginCredentials, type SignupData, type Tenant } from './auth-client'
import type { User } from './types'

interface AuthContextType {
  user: User | null
  loading: boolean
  isAuthenticated: boolean
  login: (credentials: LoginCredentials) => Promise<void>
  signup: (data: SignupData) => Promise<void>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
  tenants: Tenant[]
  currentTenant: Tenant | null
  switchTenant: (tenantId: string) => Promise<void>
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [tenants, setTenants] = useState<Tenant[]>([])
  const router = useRouter()

  // Check authentication status on mount
  useEffect(() => {
    checkAuth()
  }, [])

  // Load tenants when user is authenticated
  useEffect(() => {
    if (user) {
      loadTenants()
    }
  }, [user])

  const checkAuth = async () => {
    try {
      const response = await authClient.getCurrentUser()
      setUser(response?.user || null)
    } catch (error) {
      console.error('Auth check failed:', error)
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  const loadTenants = async () => {
    try {
      const userTenants = await authClient.getTenants()
      setTenants(userTenants)
    } catch (error) {
      console.error('Failed to load tenants:', error)
    }
  }

  const login = async (credentials: LoginCredentials) => {
    try {
      setLoading(true)
      const response = await authClient.login(credentials)
      setUser(response.user)
      router.push('/dashboard') // Adjust route as needed
    } catch (error) {
      setUser(null)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const signup = async (data: SignupData) => {
    try {
      setLoading(true)
      const response = await authClient.signup(data)
      setUser(response.user)
      router.push('/dashboard') // Adjust route as needed
    } catch (error) {
      setUser(null)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const logout = async () => {
    try {
      setLoading(true)
      await authClient.logout()
      setUser(null)
      setTenants([])
      router.push('/login')
    } catch (error) {
      console.error('Logout failed:', error)
    } finally {
      setLoading(false)
    }
  }

  const refreshUser = async () => {
    await checkAuth()
  }

  const switchTenant = async (tenantId: string) => {
    try {
      await authClient.switchTenant(tenantId)
      await refreshUser()
      await loadTenants()
    } catch (error) {
      console.error('Failed to switch tenant:', error)
      throw error
    }
  }

  const currentTenant = tenants.find(t => t.id === user?.tenant_id) || null

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAuthenticated: !!user,
        login,
        signup,
        logout,
        refreshUser,
        tenants,
        currentTenant,
        switchTenant
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
```

### Step 5: Wrap App with AuthProvider

**For Next.js App Router:** `src/app/layout.tsx`

```typescript
import { AuthProvider } from '@/lib/auth/AuthContext'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
```

**For Next.js Pages Router:** `src/pages/_app.tsx`

```typescript
import { AuthProvider } from '@/lib/auth/AuthContext'
import type { AppProps } from 'next/app'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  )
}
```

**For React/Vite:** `src/main.tsx` or `src/App.tsx`

```typescript
import { AuthProvider } from './contexts/AuthContext'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
)
```

### Step 6: Create Protected Route Component

**File:** `src/components/ProtectedRoute.tsx`

```typescript
'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth/AuthContext'

interface ProtectedRouteProps {
  children: React.ReactNode
  requiredRole?: string[]
}

export function ProtectedRoute({ children, requiredRole }: ProtectedRouteProps) {
  const { user, loading, isAuthenticated } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login')
    }

    if (!loading && isAuthenticated && requiredRole) {
      if (!requiredRole.includes(user?.role || '')) {
        router.push('/unauthorized')
      }
    }
  }, [loading, isAuthenticated, user, requiredRole, router])

  if (loading) {
    return <div>Loading...</div>
  }

  if (!isAuthenticated) {
    return null
  }

  if (requiredRole && !requiredRole.includes(user?.role || '')) {
    return null
  }

  return <>{children}</>
}
```

### Step 7: Create Login Page

**File:** `src/app/login/page.tsx` (Next.js) or `src/pages/Login.tsx` (React)

```typescript
'use client'

import { useState } from 'react'
import { useAuth } from '@/lib/auth/AuthContext'

export default function LoginPage() {
  const { login } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await login({ email, password })
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="max-w-md w-full space-y-8">
        <h2 className="text-3xl font-bold">Sign In</h2>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium">
              Email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium">
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
      </div>
    </div>
  )
}
```

### Step 8: Create Tenant Switcher Component

**File:** `src/components/TenantSwitcher.tsx`

```typescript
'use client'

import { useState } from 'react'
import { useAuth } from '@/lib/auth/AuthContext'

export function TenantSwitcher() {
  const { tenants, currentTenant, switchTenant } = useAuth()
  const [loading, setLoading] = useState(false)

  const handleSwitch = async (tenantId: string) => {
    if (tenantId === currentTenant?.id) return

    setLoading(true)
    try {
      await switchTenant(tenantId)
    } catch (error) {
      console.error('Failed to switch tenant:', error)
    } finally {
      setLoading(false)
    }
  }

  if (tenants.length <= 1) {
    return null // Don't show if user only has one tenant
  }

  return (
    <div className="relative">
      <select
        value={currentTenant?.id || ''}
        onChange={(e) => handleSwitch(e.target.value)}
        disabled={loading}
        className="px-3 py-2 border border-gray-300 rounded-md"
      >
        {tenants.map((tenant) => (
          <option key={tenant.id} value={tenant.id}>
            {tenant.name}
          </option>
        ))}
      </select>
    </div>
  )
}
```

### Step 9: Update Environment Variables

**File:** `.env.local` (Next.js) or `.env` (Vite)

```bash
# Auth Service URL
NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/auth
# or for Vite:
REACT_APP_AUTH_API_URL=https://api.bizoholic.com/auth

# App URL (for redirects)
NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com
```

### Step 10: Add Middleware for Protected Routes (Next.js Only)

**File:** `src/middleware.ts`

```typescript
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const token = request.cookies.get('access_token')

  // Public routes that don't require authentication
  const publicRoutes = ['/login', '/signup', '/forgot-password', '/reset-password']
  const isPublicRoute = publicRoutes.some(route => pathname.startsWith(route))

  // Redirect unauthenticated users to login
  if (!token && !isPublicRoute && !pathname.startsWith('/api')) {
    const url = request.nextUrl.clone()
    url.pathname = '/login'
    url.searchParams.set('returnUrl', pathname)
    return NextResponse.redirect(url)
  }

  // Redirect authenticated users away from login page
  if (token && isPublicRoute) {
    const url = request.nextUrl.clone()
    url.pathname = '/dashboard'
    return NextResponse.redirect(url)
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico|.*\\..*|manifest.json).*)',
  ],
}
```

---

## Testing Checklist

After integration, test each frontend:

- [ ] Login with valid credentials
- [ ] Login redirects to dashboard
- [ ] Logout clears session
- [ ] Protected routes require authentication
- [ ] Unauthenticated users redirect to login
- [ ] Tenant switcher appears (if user has multiple tenants)
- [ ] Tenant switching works correctly
- [ ] User data persists across page refreshes
- [ ] Token auto-refresh works (if implemented)
- [ ] Error handling for failed login
- [ ] Password reset flow (if applicable)

---

## Frontend-Specific Customizations

### Bizoholic Frontend
- **Base Path:** `/` (root)
- **Primary Route:** `/dashboard`
- **Special Requirements:** Marketing dashboard integration

### BizOSaaS Admin
- **Base Path:** `/admin` (or root)
- **Primary Route:** `/admin/dashboard`
- **Special Requirements:** Admin-only access (role check)

### Business Directory
- **Base Path:** `/directory`
- **Primary Route:** `/directory/dashboard`
- **Special Requirements:** Public listings + private dashboard

### CoreLDove Frontend
- **Base Path:** `/`
- **Primary Route:** `/dashboard`
- **Special Requirements:** E-commerce specific user roles

### ThrillRing Gaming
- **Base Path:** `/`
- **Primary Route:** `/dashboard` or `/gaming`
- **Special Requirements:** Gaming-specific user profiles

### Analytics Dashboard
- **Base Path:** `/analytics` (or root)
- **Primary Route:** `/analytics/dashboard`
- **Special Requirements:** Data visualization access control

---

## Common Issues & Solutions

### Issue: CORS errors
**Solution:** Ensure `withCredentials: true` in axios config and auth service has proper CORS headers

### Issue: Cookies not being set
**Solution:** Check `secure`, `sameSite`, and domain settings in cookie options

### Issue: Token not included in requests
**Solution:** Verify axios interceptor is configured correctly

### Issue: Infinite redirect loops
**Solution:** Check middleware logic and ensure public routes are properly excluded

### Issue: User state not persisting
**Solution:** Verify token storage and getCurrentUser() is called on mount

---

## Next Steps

1. Complete all 6 frontend integrations
2. Test SSO across platforms (login once, access all)
3. Test tenant switching works across all frontends
4. Verify role-based access control
5. Mark Phase 3 as 100% complete

---

**Created:** November 16, 2025
**Reference:** Client Portal implementation
**Auth Service:** https://api.bizoholic.com/auth
