# Client Portal TailAdmin v2 Integration - Complete Implementation Plan

**Date:** November 4, 2025
**Status:** 🚀 READY TO IMPLEMENT
**Estimated Time:** 12-15 hours total
**Target:** https://stg.bizoholic.com/portal

---

## 📋 EXECUTIVE SUMMARY

### Current State Analysis

**1. Existing Client Portal (`/portal`):**
- ✅ Deployed at https://stg.bizoholic.com/portal
- ✅ Basic dashboard layout with sidebar navigation
- ✅ Analytics page (redirects to main dashboard)
- ✅ AI Assistant component already integrated
- ✅ Brain Gateway API integration
- ⚠️ **NO TailAdmin v2** (custom dashboard layout)
- ⚠️ **NO Superset embedding** (just custom metrics)
- ⚠️ Missing comprehensive auth flow

**2. Bizoholic Dashboard (`/dashboard` on stg.bizoholic.com):**
- ✅ Marketing automation features
- ✅ Campaign metrics and AI agent management
- ✅ Dashboard overview with real-time metrics
- ✅ Comprehensive component library
- **Location:** `/frontend/apps/bizoholic-frontend/components/dashboard/`

**3. FastAPI Auth Service:**
- ✅ Running at `backend-services-authservice:8007`
- ✅ Multi-tenant authentication
- ✅ JWT + Cookie authentication
- ✅ Role-based access control (RBAC)
- ✅ FastAPI-Users implementation

---

## 🎯 IMPLEMENTATION OBJECTIVES

### Primary Goals:
1. **Integrate TailAdmin v2** into Client Portal with modern UI/UX
2. **Merge `/dashboard` features** from bizoholic-frontend into client-portal
3. **Add Analytics Tab** with Superset dashboard embedding
4. **Add Conversational AI Tab** with enhanced chat interface
5. **Implement FastAPI Authentication** for all private pages
6. **Connect all features** to respective backends via Brain Gateway

---

## 🏗️ ARCHITECTURE DESIGN

### Unified Client Portal Structure

```
Client Portal (https://stg.bizoholic.com/portal)
├── Authentication Layer (FastAPI Auth Service)
│   ├── Login/Register pages
│   ├── JWT token management
│   └── Multi-tenant session handling
│
├── TailAdmin v2 Layout
│   ├── Collapsible sidebar navigation
│   ├── Top header with user profile
│   ├── Dark mode toggle
│   └── Responsive mobile menu
│
├── Dashboard Tab (Default)
│   ├── Overview metrics (from /dashboard)
│   ├── Campaign metrics
│   ├── AI agent status
│   ├── Recent activity
│   └── Quick actions
│
├── Analytics Tab (NEW - Superset Integration)
│   ├── Embedded Superset dashboards
│   ├── Custom metrics cards
│   ├── Real-time data visualization
│   └── Export/download functionality
│
├── AI Assistant Tab (ENHANCED)
│   ├── Conversational interface
│   ├── Natural language queries
│   ├── Task automation
│   └── Multi-agent orchestration
│
└── Additional Tabs (Existing)
    ├── Marketing campaigns
    ├── CRM & Leads
    ├── Content management
    ├── E-commerce
    ├── Billing
    └── Settings
```

### Backend Integration Flow

```
┌─────────────────────────────────────────────────────────┐
│        Client Portal (Next.js 15 + React 19)            │
│                Port 3002 → 3001 (container)             │
└─────────────────────────────────────────────────────────┘
                          ▼
              (All API calls route through)
                          ▼
┌─────────────────────────────────────────────────────────┐
│         Brain Gateway (FastAPI - Port 8001)             │
│                                                         │
│  Routes:                                                │
│  /api/auth/* → Auth Service (8007)                      │
│  /api/analytics/* → Superset (8088)                     │
│  /api/ai-agents/* → AI Agents Service (8002)            │
│  /api/marketing/* → Marketing Service                   │
│  /api/crm/* → CRM Service                               │
│  /api/content/* → Wagtail CMS (8000)                    │
│  /api/ecommerce/* → Saleor API (8000)                   │
└─────────────────────────────────────────────────────────┘
                          ▼
              (Microservices Backend)
                          ▼
┌───────────────┬───────────────┬───────────────────────┐
│ Auth Service  │  Superset BI  │  AI Agents Service    │
│   (8007)      │    (8088)     │       (8002)          │
└───────────────┴───────────────┴───────────────────────┘
```

---

## 📦 PHASE 1: TailAdmin v2 Setup (3-4 hours)

### 1.1 Install TailAdmin v2 Dependencies

```bash
cd /home/alagiri/projects/bizoholic/bizosaas-platform/frontend/apps/client-portal

# Add Superset embedding
npm install @superset-ui/embedded-sdk

# Add ApexCharts for TailAdmin dashboards
npm install apexcharts react-apexcharts

# Ensure we have latest shadcn components
npm install @radix-ui/react-tabs @radix-ui/react-dropdown-menu
```

### 1.2 Create TailAdmin v2 Layout Structure

**File:** `lib/layouts/TailAdminLayout.tsx`

```typescript
'use client'

import { useState } from 'react'
import { usePathname } from 'next/navigation'
import { TailAdminSidebar } from './TailAdminSidebar'
import { TailAdminHeader } from './TailAdminHeader'
import { useAuth } from '@/components/auth/AuthProvider'

interface TailAdminLayoutProps {
  children: React.ReactNode
}

export function TailAdminLayout({ children }: TailAdminLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const { user, isAuthenticated } = useAuth()
  const pathname = usePathname()

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <LoginRedirect />
  }

  return (
    <div className="dark:bg-boxdark-2 dark:text-bodydark">
      {/* Page Wrapper */}
      <div className="flex h-screen overflow-hidden">
        {/* Sidebar */}
        <TailAdminSidebar
          sidebarOpen={sidebarOpen}
          setSidebarOpen={setSidebarOpen}
        />

        {/* Content Area */}
        <div className="relative flex flex-1 flex-col overflow-y-auto overflow-x-hidden">
          {/* Header */}
          <TailAdminHeader
            sidebarOpen={sidebarOpen}
            setSidebarOpen={setSidebarOpen}
          />

          {/* Main Content */}
          <main>
            <div className="mx-auto max-w-screen-2xl p-4 md:p-6 2xl:p-10">
              {children}
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}
```

### 1.3 Create TailAdmin Sidebar Component

**File:** `lib/layouts/TailAdminSidebar.tsx`

Key features:
- Collapsible navigation
- Active route highlighting
- Icon-based menu items
- Nested submenu support
- Dark mode compatible

Menu items:
- 📊 Dashboard (default)
- 📈 Analytics (NEW - with Superset)
- 🤖 AI Assistant (enhanced)
- 📣 Marketing
- 👥 CRM & Leads
- 📝 Content
- 🛒 E-commerce
- 💳 Billing
- ⚙️ Settings

### 1.4 Create TailAdmin Header Component

**File:** `lib/layouts/TailAdminHeader.tsx`

Features:
- User profile dropdown
- Notifications bell
- Search bar
- Dark mode toggle
- Breadcrumb navigation

---

## 📦 PHASE 2: Merge Dashboard Features (2-3 hours)

### 2.1 Copy Components from Bizoholic Frontend

**Source:** `/frontend/apps/bizoholic-frontend/components/dashboard/`
**Destination:** `/frontend/apps/client-portal/lib/ui/components/dashboard/`

Components to migrate:
- `dashboard-overview.tsx` → Real-time metrics
- `campaign-metrics.tsx` → Marketing campaign data
- `ai-agent-status.tsx` → AI agent monitoring
- `recent-activity.tsx` → Activity feed
- `quick-actions.tsx` → Action shortcuts

### 2.2 Update Dashboard Page

**File:** `app/portal/page.tsx` (or `app/page.tsx` with basePath)

```typescript
import { Suspense } from 'react'
import { TailAdminLayout } from '@/lib/layouts/TailAdminLayout'
import { DashboardOverview } from '@/lib/ui/components/dashboard/dashboard-overview'
import { CampaignMetrics } from '@/lib/ui/components/dashboard/campaign-metrics'
import { AIAgentStatus } from '@/lib/ui/components/dashboard/ai-agent-status'
import { RecentActivity } from '@/lib/ui/components/dashboard/recent-activity'
import { QuickActions } from '@/lib/ui/components/dashboard/quick-actions'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

export default function DashboardPage() {
  return (
    <TailAdminLayout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold">Dashboard</h1>

        {/* Overview Metrics */}
        <Suspense fallback={<LoadingSkeleton />}>
          <DashboardOverview />
        </Suspense>

        {/* Tabs for different views */}
        <Tabs defaultValue="overview" className="space-y-4">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="campaigns">Campaigns</TabsTrigger>
            <TabsTrigger value="agents">AI Agents</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <QuickActions />
              <RecentActivity />
            </div>
          </TabsContent>

          <TabsContent value="campaigns">
            <CampaignMetrics />
          </TabsContent>

          <TabsContent value="agents">
            <AIAgentStatus />
          </TabsContent>
        </Tabs>
      </div>
    </TailAdminLayout>
  )
}
```

---

## 📦 PHASE 3: Analytics Tab with Superset (3-4 hours)

### 3.1 Create Superset API Client

**File:** `lib/api/superset-api.ts`

```typescript
import axios, { AxiosInstance } from 'axios'

export class SupersetAPI {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL + '/api/analytics/superset',
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    })

    // Add auth interceptor
    this.client.interceptors.request.use((config) => {
      const token = this.getAuthToken()
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })
  }

  private getAuthToken(): string | null {
    if (typeof window === 'undefined') return null
    return sessionStorage.getItem('auth_token')
  }

  async getGuestToken(params: {
    dashboardId: string
    tenantId: string
    userId: string
  }): Promise<string> {
    const response = await this.client.post('/guest-token', {
      resources: [{ type: 'dashboard', id: params.dashboardId }],
      rls: [{ clause: `tenant_id = '${params.tenantId}'` }],
      user: { username: params.userId },
    })
    return response.data.token
  }

  async listDashboards(tenantId: string) {
    const response = await this.client.get('/dashboards', {
      params: { tenant_id: tenantId },
    })
    return response.data.result || []
  }
}

export const supersetAPI = new SupersetAPI()
```

### 3.2 Create Superset Embed Component

**File:** `lib/ui/components/SupersetEmbed.tsx`

```typescript
'use client'

import { useEffect, useRef, useState } from 'react'
import { embedDashboard } from '@superset-ui/embedded-sdk'
import { supersetAPI } from '@/lib/api/superset-api'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Skeleton } from '@/components/ui/skeleton'
import { Button } from '@/components/ui/button'
import { AlertCircle, RefreshCw } from 'lucide-react'

export interface SupersetEmbedProps {
  dashboardId: string
  tenantId: string
  userId: string
  height?: string
  className?: string
}

export function SupersetEmbed({
  dashboardId,
  tenantId,
  userId,
  height = '800px',
  className = '',
}: SupersetEmbedProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!containerRef.current) return

    let mounted = true

    const loadDashboard = async () => {
      try {
        setLoading(true)
        setError(null)

        const guestToken = await supersetAPI.getGuestToken({
          dashboardId,
          tenantId,
          userId,
        })

        if (!mounted) return

        const supersetDomain = process.env.NEXT_PUBLIC_SUPERSET_DOMAIN || 'http://localhost:8088'

        await embedDashboard({
          id: dashboardId,
          supersetDomain,
          mountPoint: containerRef.current!,
          fetchGuestToken: () => Promise.resolve(guestToken),
          dashboardUiConfig: {
            hideTitle: false,
            filters: { expanded: true },
          },
        })

        if (!mounted) return
        setLoading(false)
      } catch (err) {
        if (!mounted) return
        setError(err instanceof Error ? err.message : 'Failed to load dashboard')
        setLoading(false)
      }
    }

    loadDashboard()

    return () => {
      mounted = false
      if (containerRef.current) {
        containerRef.current.innerHTML = ''
      }
    }
  }, [dashboardId, tenantId, userId])

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    )
  }

  return (
    <div className={`relative ${className}`} style={{ height }}>
      {loading && (
        <div className="absolute inset-0 space-y-4">
          <Skeleton className="h-12 w-full" />
          <Skeleton className="h-64 w-full" />
        </div>
      )}
      <div
        ref={containerRef}
        className="h-full w-full"
        style={{ visibility: loading ? 'hidden' : 'visible' }}
      />
    </div>
  )
}
```

### 3.3 Create Analytics Page

**File:** `app/analytics/page.tsx`

```typescript
import { Suspense } from 'react'
import { TailAdminLayout } from '@/lib/layouts/TailAdminLayout'
import { SupersetEmbed } from '@/lib/ui/components/SupersetEmbed'
import { AnalyticsDashboard } from '@/components/analytics/analytics-dashboard'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

export default function AnalyticsPage() {
  // Get tenant and user from auth context
  const tenantId = 'current-tenant-id' // TODO: Get from auth
  const userId = 'current-user-id' // TODO: Get from auth

  return (
    <TailAdminLayout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold">Analytics</h1>

        <Tabs defaultValue="overview" className="space-y-4">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="dashboards">Dashboards</TabsTrigger>
            <TabsTrigger value="reports">Reports</TabsTrigger>
          </TabsList>

          <TabsContent value="overview">
            <Suspense fallback={<LoadingSkeleton />}>
              <AnalyticsDashboard />
            </Suspense>
          </TabsContent>

          <TabsContent value="dashboards">
            <div className="space-y-4">
              <SupersetEmbed
                dashboardId="1"
                tenantId={tenantId}
                userId={userId}
                height="800px"
                className="border rounded-lg"
              />
            </div>
          </TabsContent>

          <TabsContent value="reports">
            <div>Reports content here</div>
          </TabsContent>
        </Tabs>
      </div>
    </TailAdminLayout>
  )
}
```

---

## 📦 PHASE 4: AI Assistant Tab (2-3 hours)

### 4.1 Enhance Existing AI Assistant

**File:** `app/chat/page.tsx`

```typescript
import { TailAdminLayout } from '@/lib/layouts/TailAdminLayout'
import { AIAssistant } from '@/components/ai-assistant/AIAssistant'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function ChatPage() {
  return (
    <TailAdminLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">AI Assistant</h1>
          <p className="text-muted-foreground">
            Ask questions, automate tasks, and get insights powered by AI
          </p>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">📊 Analytics Queries</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                "Show me revenue trends for Q4"
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm">🎯 Campaign Optimization</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                "Which campaigns are underperforming?"
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm">🤖 Task Automation</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                "Create a new email campaign for Black Friday"
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Main AI Chat Interface */}
        <Card className="h-[600px]">
          <CardContent className="p-0 h-full">
            <AIAssistant />
          </CardContent>
        </Card>
      </div>
    </TailAdminLayout>
  )
}
```

---

## 📦 PHASE 5: FastAPI Authentication (2-3 hours)

### 5.1 Create Auth Service Client

**File:** `lib/api/auth-api.ts`

```typescript
import axios from 'axios'

const authClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL + '/api/auth',
  withCredentials: true, // Send cookies
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData extends LoginCredentials {
  tenant_name: string
  full_name: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: {
    id: string
    email: string
    tenant_id: string
    role: string
  }
}

export const authAPI = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await authClient.post('/auth/jwt/login', credentials)
    // Store token in sessionStorage
    if (response.data.access_token) {
      sessionStorage.setItem('auth_token', response.data.access_token)
    }
    return response.data
  },

  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await authClient.post('/auth/register', data)
    return response.data
  },

  async logout() {
    await authClient.post('/auth/jwt/logout')
    sessionStorage.removeItem('auth_token')
  },

  async getCurrentUser() {
    const response = await authClient.get('/users/me')
    return response.data
  },

  async refreshToken() {
    const response = await authClient.post('/auth/jwt/refresh')
    if (response.data.access_token) {
      sessionStorage.setItem('auth_token', response.data.access_token)
    }
    return response.data
  },
}
```

### 5.2 Create Protected Route Wrapper

**File:** `lib/auth/ProtectedRoute.tsx`

```typescript
'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/components/auth/AuthProvider'
import { Skeleton } from '@/components/ui/skeleton'

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, isLoading, router])

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="space-y-4">
          <Skeleton className="h-12 w-64" />
          <Skeleton className="h-64 w-96" />
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return null
  }

  return <>{children}</>
}
```

### 5.3 Update Root Layout

**File:** `app/layout.tsx`

```typescript
import { AuthProvider } from '@/components/auth/AuthProvider'
import { ProtectedRoute } from '@/lib/auth/ProtectedRoute'
import './globals.css'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <AuthProvider>
          <ProtectedRoute>
            {children}
          </ProtectedRoute>
        </AuthProvider>
      </body>
    </html>
  )
}
```

### 5.4 Create Login Page

**File:** `app/login/page.tsx`

```typescript
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { authAPI } from '@/lib/api/auth-api'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await authAPI.login({ email, password })
      router.push('/')
    } catch (err) {
      setError('Invalid email or password')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-2xl">Welcome back</CardTitle>
          <CardDescription>Sign in to your account</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Signing in...' : 'Sign in'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
```

---

## 📦 PHASE 6: Brain Gateway Routes (1 hour)

### 6.1 Add Superset Proxy Routes

**File:** `/backend/services/brain-gateway/routes/analytics.py` (CREATE NEW)

```python
from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient
import os

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

SUPERSET_URL = os.getenv("SUPERSET_URL", "http://infrastructure-superset:8088")

@router.post("/superset/guest-token")
async def create_guest_token(
    payload: dict,
    current_user = Depends(get_current_user)
):
    """Generate Superset guest token with RLS enforcement"""
    async with AsyncClient() as client:
        # Add tenant_id from authenticated user
        tenant_id = current_user.tenant_id
        payload["rls"] = [{"clause": f"tenant_id = '{tenant_id}'"}]

        response = await client.post(
            f"{SUPERSET_URL}/api/v1/security/guest_token/",
            json=payload,
            headers={"Authorization": f"Bearer {SUPERSET_ADMIN_TOKEN}"}
        )
        return response.json()

@router.get("/superset/dashboards")
async def list_dashboards(
    tenant_id: str,
    current_user = Depends(get_current_user)
):
    """List dashboards accessible to tenant"""
    # Validate user has access to tenant
    if current_user.tenant_id != tenant_id:
        raise HTTPException(403, "Access denied")

    async with AsyncClient() as client:
        response = await client.get(
            f"{SUPERSET_URL}/api/v1/dashboard/",
            params={"filters": f"tenant_id:{tenant_id}"},
            headers={"Authorization": f"Bearer {SUPERSET_ADMIN_TOKEN}"}
        )
        return response.json()
```

### 6.2 Update Brain Gateway Main

**File:** `/backend/services/brain-gateway/main.py`

Add:
```python
from routes import analytics

app.include_router(analytics.router)
```

---

## 📦 PHASE 7: Build & Deploy (1-2 hours)

### 7.1 Build Docker Image

```bash
cd /home/alagiri/projects/bizoholic/bizosaas-platform/frontend/apps/client-portal

# Build image
docker build -f Dockerfile.optimized \
  -t ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.0.0-tailadmin \
  -t ghcr.io/bizoholic-digital/bizosaas-client-portal:latest \
  .
```

### 7.2 Push to GHCR

```bash
echo "ghp_REDACTED" | docker login ghcr.io -u alagiri.rajesh@gmail.com --password-stdin

docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:v2.0.0-tailadmin
docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:latest
```

### 7.3 Deploy via Dokploy

1. Go to: https://dk.bizoholic.com
2. Login: bizoholic.digital@gmail.com / 25IKC#1XiKABRo
3. Navigate to: **frontend-services** project
4. Find: **client-portal** service
5. Click: **Redeploy** with new image tag

**Environment Variables** (add if missing):
```
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://backend-brain-gateway:8001
NEXT_PUBLIC_SUPERSET_DOMAIN=http://infrastructure-superset:8088
NEXT_PUBLIC_AUTH_SERVICE_URL=http://backend-services-authservice:8007
```

---

## ✅ VERIFICATION CHECKLIST

After deployment, verify:

- [ ] Can access https://stg.bizoholic.com/portal
- [ ] Login page redirects to dashboard after authentication
- [ ] TailAdmin v2 layout renders correctly (sidebar, header)
- [ ] Dashboard tab shows merged features from `/dashboard`
- [ ] Analytics tab loads with Superset dashboards embedded
- [ ] AI Assistant tab has enhanced conversational interface
- [ ] All navigation links work correctly
- [ ] Dark mode toggle functions
- [ ] User profile dropdown works
- [ ] Logout redirects to login page
- [ ] Protected routes redirect unauthenticated users
- [ ] Multi-tenant data isolation enforced
- [ ] No errors in browser console
- [ ] No errors in container logs

---

## 🎯 SUCCESS METRICS

When complete:
- ✅ Client Portal fully integrated with TailAdmin v2 UI
- ✅ All dashboard features from `/dashboard` available
- ✅ Superset analytics embedded and functional
- ✅ AI conversational interface enhanced
- ✅ FastAPI authentication securing all pages
- ✅ All backend services connected via Brain Gateway
- ✅ Multi-tenant isolation working correctly
- ✅ Professional, modern UI/UX matching TailAdmin standards

---

## 📞 SUPPORT & REFERENCES

**Documentation:**
- TailAdmin Next.js: https://github.com/TailAdmin/free-nextjs-admin-dashboard
- Superset Embedding: https://superset.apache.org/docs/installation/embedded-superset
- FastAPI Users: https://fastapi-users.github.io/fastapi-users/

**Credentials:** [credentials.md](/home/alagiri/projects/bizoholic/credentials.md)

**Status:** Ready to implement Phase 1
**Last Updated:** November 4, 2025
**Total Estimated Time:** 12-15 hours
