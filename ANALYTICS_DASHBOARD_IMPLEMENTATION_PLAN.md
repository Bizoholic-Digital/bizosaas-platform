# Analytics Dashboard Implementation Plan

**Date:** November 4, 2025
**Status:** 📋 READY FOR IMPLEMENTATION
**Architecture:** Next.js 15 + Embedded Superset + Brain Gateway Proxy + AI Chat Interface

---

## 🎯 OBJECTIVE

Implement the **Analytics Dashboard** frontend application that:
1. ✅ **Embeds Apache Superset** dashboards via the embedded SDK
2. ✅ **Routes through Brain Gateway** (`/api/analytics/*`) for unified authentication
3. ✅ **Provides AI-powered conversational analytics** via personal AI assistant
4. ✅ **Follows modular DDD architecture** (self-contained `lib/` structure)
5. ✅ **Deployed via Dokploy** on KVM4 at port 3007

---

## 📊 CURRENT STATE ANALYSIS

### ✅ Superset Backend (DEPLOYED)
- **Container:** `infrastructure-superset.1.2qv7tr4aib6gjyt8dftl6a8wt`
- **Status:** ✅ Running (health: starting)
- **Port:** 8088 (internal Docker network)
- **Admin:** `admin` / `Bizoholic2024Admin`
- **Database:** Connected to `infrastructureservices-sharedpostgres-3cwdm6`
- **Redis:** Connected to `infrastructureservices-bizosaasredis-w0gw3g`

### ✅ Existing Analytics Dashboard Code
- **Location:** `/bizoholic-backup/bizosaas/frontend/apps/analytics-dashboard/`
- **Framework:** Next.js 15.5.3 + React 19
- **Port:** 3009 (should be 3007 per roadmap)
- **Current State:** Basic dashboard with hardcoded mock data
- **Architecture:** ❌ NOT modular DDD (no `lib/` directory)
- **Superset Integration:** ❌ NOT integrated

### 🔍 What Needs to Be Done
1. **Migrate to modular DDD** - Create `lib/` structure
2. **Integrate Superset Embedded SDK** - Replace mock data with real dashboards
3. **Add Brain Gateway proxy** - Route `/api/analytics/*` through gateway
4. **Add AI conversational interface** - Integrate personal AI assistant
5. **Add authentication** - Secure dashboards behind login
6. **Build and deploy** - Push to GHCR and deploy via Dokploy

---

## 🏗️ ARCHITECTURE DESIGN

### Frontend Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                Analytics Dashboard (Port 3007)                   │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Next.js 15 App Router (React 19 + TypeScript)             │  │
│  │                                                            │  │
│  │  /dashboard (route)                                        │  │
│  │  ├─ Embedded Superset Dashboards (iframe with SDK)         │  │
│  │  ├─ Real-time metrics cards                                │  │
│  │  ├─ Activity feed from Brain API                           │  │
│  │  └─ Navigation to detailed analytics                       │  │
│  │                                                            │  │
│  │  /analytics (route)                                        │  │
│  │  ├─ Superset dashboard embedding                           │  │
│  │  ├─ Guest token authentication                             │  │
│  │  └─ Multi-tenant row-level security                        │  │
│  │                                                            │  │
│  │  /chat (route) - AI Conversational Analytics               │  │
│  │  ├─ Personal AI assistant interface                        │  │
│  │  ├─ Natural language queries → SQL generation              │  │
│  │  ├─ Auto-generate charts from conversations                │  │
│  │  └─ Export results to Superset dashboards                  │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  lib/ (Modular DDD Architecture)                           │  │
│  │                                                            │  │
│  │  lib/api/                                                  │  │
│  │  ├─ brain-api.ts (Brain Gateway client)                    │  │
│  │  ├─ superset-api.ts (Superset embedded API)                │  │
│  │  └─ analytics-api.ts (Analytics endpoints)                 │  │
│  │                                                            │  │
│  │  lib/hooks/                                                │  │
│  │  ├─ useSupersetDashboard.ts (Dashboard embedding)          │  │
│  │  ├─ useAnalytics.ts (Real-time metrics)                    │  │
│  │  └─ useAIChat.ts (Conversational interface)                │  │
│  │                                                            │  │
│  │  lib/ui/                                                   │  │
│  │  ├─ components/ (Reusable React components)                │  │
│  │  │  ├─ DashboardCard.tsx                                   │  │
│  │  │  ├─ SupersetEmbed.tsx                                   │  │
│  │  │  ├─ MetricsCard.tsx                                     │  │
│  │  │  ├─ ActivityFeed.tsx                                    │  │
│  │  │  └─ AIChatInterface.tsx                                 │  │
│  │  └─ charts/ (Custom chart components)                      │  │
│  │                                                            │  │
│  │  lib/types/                                                │  │
│  │  ├─ analytics.ts (Analytics data types)                    │  │
│  │  ├─ dashboard.ts (Dashboard config types)                  │  │
│  │  └─ superset.ts (Superset SDK types)                       │  │
│  │                                                            │  │
│  │  lib/utils/                                                │  │
│  │  ├─ superset-embed.ts (Embedding utilities)                │  │
│  │  ├─ auth.ts (Token management)                             │  │
│  │  └─ formatting.ts (Data formatting)                        │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                              ▼
                    (HTTPS - Brain Gateway Proxy)
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│          Brain Gateway (Port 8001) - API Router                  │
│                                                                  │
│  /api/analytics/superset/* → http://infrastructure-superset:8088 │
│  /api/analytics/dashboards → Superset REST API                   │
│  /api/analytics/guest-token → Guest token generation             │
│  /api/analytics/metrics → Real-time aggregated data              │
│  /api/analytics/chat → AI conversational analytics               │
│  /api/analytics/query → Natural language → SQL generation        │
│                                                                  │
│  Responsibilities:                                               │
│  - Authentication/Authorization (JWT validation)                 │
│  - Multi-tenant isolation (tenant_id from JWT)                   │
│  - Rate limiting                                                 │
│  - Request logging                                               │
│  - Superset guest token generation                               │
│  - AI RAG/KAG context injection                                  │
└──────────────────────────────────────────────────────────────────┘
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│              Apache Superset (Port 8088)                         │
│                                                                  │
│  - Business Intelligence dashboards                              │
│  - 50+ visualization types                                       │
│  - SQL Lab (query editor)                                        │
│  - Row-Level Security (multi-tenant)                             │
│  - Guest token embedding (iframe security)                       │
│  - PostgreSQL + Redis backend                                    │
└──────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Request (Analytics Dashboard)
          ↓
Next.js Frontend (Port 3007)
          ↓
Brain Gateway Proxy (/api/analytics/*)
          ↓
Superset API (Port 8088)
          ↓
PostgreSQL (shared-postgres)
          ↓
Return Data
          ↓
Render in Frontend (Superset iframes + custom components)
```

---

## 📋 IMPLEMENTATION TASKS

### Phase 1: Create Modular DDD Structure (1 hour)

**Location:** `/bizosaas-platform/frontend/apps/analytics-dashboard/`

#### 1.1 Create lib/ Directory Structure
```bash
cd /home/alagiri/projects/bizoholic/bizosaas-platform/frontend/apps/analytics-dashboard

mkdir -p lib/{api,hooks,ui/components,ui/charts,types,utils}
```

#### 1.2 Move Existing Components to lib/
```bash
# Analyze existing app/ structure
# Move reusable logic to lib/
# Keep app/ routes lean (presentation only)
```

#### 1.3 Create Package Configuration
```json
// package.json - Update to port 3007
{
  "name": "analytics-dashboard",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev --port 3007",
    "build": "next build",
    "start": "next start --port 3007"
  }
}
```

---

### Phase 2: Implement Superset Integration (2-3 hours)

#### 2.1 Install Superset Embedded SDK
```bash
npm install --save @superset-ui/embedded-sdk
npm install --save axios @tanstack/react-query
```

#### 2.2 Create Superset API Client
```typescript
// lib/api/superset-api.ts

export interface SupersetGuestTokenRequest {
  user: {
    username: string
    first_name: string
    last_name: string
  }
  resources: Array<{
    type: 'dashboard'
    id: string
  }>
  rls: Array<{ clause: string }>
}

export interface SupersetDashboard {
  id: string
  dashboard_title: string
  url: string
  published: boolean
}

export class SupersetAPI {
  private baseURL: string

  constructor() {
    // Route through Brain Gateway
    this.baseURL = process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL + '/api/analytics/superset'
  }

  /**
   * Fetch guest token for embedding Superset dashboards
   */
  async getGuestToken(dashboardId: string, tenantId: string): Promise<string> {
    const response = await fetch(`${this.baseURL}/guest-token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAuthToken()}` // From NextAuth
      },
      body: JSON.stringify({
        dashboard_id: dashboardId,
        tenant_id: tenantId,
        rls: [{ clause: `tenant_id = '${tenantId}'` }]
      })
    })

    if (!response.ok) {
      throw new Error('Failed to fetch guest token')
    }

    const data = await response.json()
    return data.token
  }

  /**
   * List available dashboards for current tenant
   */
  async listDashboards(tenantId: string): Promise<SupersetDashboard[]> {
    const response = await fetch(`${this.baseURL}/dashboards?tenant_id=${tenantId}`, {
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`
      }
    })

    if (!response.ok) {
      throw new Error('Failed to fetch dashboards')
    }

    return response.json()
  }
}

function getAuthToken(): string {
  // Get JWT token from NextAuth session
  // Implementation depends on your auth setup
  return localStorage.getItem('auth_token') || ''
}
```

#### 2.3 Create Superset Embedding Component
```typescript
// lib/ui/components/SupersetEmbed.tsx

'use client'

import { useEffect, useRef, useState } from 'react'
import { embedDashboard } from '@superset-ui/embedded-sdk'
import { SupersetAPI } from '@/lib/api/superset-api'

interface SupersetEmbedProps {
  dashboardId: string
  tenantId: string
  height?: string
}

export function SupersetEmbed({ dashboardId, tenantId, height = '600px' }: SupersetEmbedProps) {
  const embedRef = useRef<HTMLDivElement>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const initEmbed = async () => {
      if (!embedRef.current) return

      try {
        setLoading(true)
        const supersetAPI = new SupersetAPI()
        const guestToken = await supersetAPI.getGuestToken(dashboardId, tenantId)

        await embedDashboard({
          id: dashboardId,
          supersetDomain: process.env.NEXT_PUBLIC_SUPERSET_DOMAIN || 'http://localhost:8088',
          mountPoint: embedRef.current,
          fetchGuestToken: () => Promise.resolve(guestToken),
          dashboardUiConfig: {
            hideTitle: false,
            hideChartControls: false,
            hideTab: false,
            filters: {
              expanded: true
            }
          }
        })

        setLoading(false)
      } catch (err) {
        console.error('Failed to embed Superset dashboard:', err)
        setError('Failed to load analytics dashboard')
        setLoading(false)
      }
    }

    initEmbed()
  }, [dashboardId, tenantId])

  if (loading) {
    return (
      <div className="flex items-center justify-center" style={{ height }}>
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-gray-600">Loading dashboard...</span>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center" style={{ height }}>
        <div className="text-center">
          <p className="text-red-600 font-medium">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return <div ref={embedRef} style={{ height }} />
}
```

#### 2.4 Create Dashboard Page with Embedded Superset
```typescript
// app/analytics/page.tsx

'use client'

import { SupersetEmbed } from '@/lib/ui/components/SupersetEmbed'
import { useSession } from 'next-auth/react'
import { redirect } from 'next/navigation'

export default function AnalyticsPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') {
    return <div>Loading...</div>
  }

  if (!session) {
    redirect('/auth/signin')
  }

  // Get tenant ID from session
  const tenantId = session.user.tenant_id || 'default'

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Analytics Dashboard
        </h1>

        {/* Embedded Superset Dashboard */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <SupersetEmbed
            dashboardId="1" // Replace with actual dashboard ID
            tenantId={tenantId}
            height="800px"
          />
        </div>
      </div>
    </div>
  )
}
```

---

### Phase 3: Add Brain Gateway Proxy Routes (2 hours)

**Location:** `/bizosaas-platform/backend/services/brain-gateway/`

#### 3.1 Find Brain Gateway Service
```bash
# First, locate the Brain Gateway codebase
find /home/alagiri/projects -name "brain-gateway" -type d 2>/dev/null
```

#### 3.2 Add Superset Proxy Routes
```python
# routes/analytics.py (NEW FILE)

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import httpx
import os
from typing import List, Dict, Any

from core.auth import get_current_user, User
from core.config import settings

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

SUPERSET_URL = os.getenv("SUPERSET_URL", "http://infrastructure-superset:8088")

class GuestTokenRequest(BaseModel):
    dashboard_id: str
    tenant_id: str
    rls: List[Dict[str, str]]

class GuestTokenResponse(BaseModel):
    token: str

@router.post("/superset/guest-token", response_model=GuestTokenResponse)
async def get_superset_guest_token(
    request: GuestTokenRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate Superset guest token for embedding dashboards.

    - Validates user authentication
    - Ensures tenant isolation via RLS
    - Proxies request to Superset
    """

    # Verify tenant matches current user
    if request.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Access denied to this tenant")

    # Prepare Superset guest token request
    superset_request = {
        "user": {
            "username": current_user.email,
            "first_name": current_user.first_name or "",
            "last_name": current_user.last_name or ""
        },
        "resources": [{
            "type": "dashboard",
            "id": request.dashboard_id
        }],
        "rls": request.rls
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPERSET_URL}/api/v1/security/guest_token/",
            json=superset_request,
            headers={
                "Authorization": f"Bearer {settings.SUPERSET_ADMIN_TOKEN}"
            }
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to generate guest token"
            )

        data = response.json()
        return GuestTokenResponse(token=data["token"])

@router.get("/superset/dashboards")
async def list_dashboards(
    current_user: User = Depends(get_current_user)
):
    """
    List Superset dashboards available to current tenant.
    """

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPERSET_URL}/api/v1/dashboard/",
            headers={
                "Authorization": f"Bearer {settings.SUPERSET_ADMIN_TOKEN}"
            },
            params={
                "q": f'{{"filters":[{{"col":"owners","opr":"rel_o_m","value":{current_user.tenant_id}}}]}}'
            }
        )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch dashboards")

        return response.json()

@router.get("/metrics/summary")
async def get_metrics_summary(
    current_user: User = Depends(get_current_user)
):
    """
    Get aggregated metrics summary for the dashboard.
    Fetches real-time data from various platform services.
    """

    # TODO: Implement actual metrics aggregation from:
    # - Django CRM (leads, contacts, deals)
    # - Saleor (orders, revenue)
    # - Wagtail CMS (page views, form submissions)
    # - Business Directory (listings, searches)

    return {
        "total_users": 0,
        "total_revenue": 0,
        "total_leads": 0,
        "conversion_rate": 0,
        "recent_activity": []
    }
```

#### 3.3 Register Analytics Routes
```python
# main.py

from routes import analytics

app.include_router(analytics.router)
```

---

### Phase 4: Add AI Conversational Analytics Interface (3-4 hours)

#### 4.1 Create AI Chat Component
```typescript
// lib/ui/components/AIChatInterface.tsx

'use client'

import { useState } from 'react'
import { useAIChat } from '@/lib/hooks/useAIChat'

export function AIChatInterface() {
  const [message, setMessage] = useState('')
  const { messages, sendMessage, isLoading } = useAIChat()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim()) return

    await sendMessage(message)
    setMessage('')
  }

  return (
    <div className="flex flex-col h-[600px] bg-white rounded-lg shadow-lg">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900">
          AI Analytics Assistant
        </h2>
        <p className="text-sm text-gray-500 mt-1">
          Ask me anything about your business metrics
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-12">
            <p className="text-lg font-medium">Ask me about your analytics</p>
            <div className="mt-4 space-y-2 text-sm">
              <p className="text-gray-400">Try asking:</p>
              <ul className="space-y-1">
                <li>"What's my total revenue this month?"</li>
                <li>"Show me top performing products"</li>
                <li>"How many leads did I get yesterday?"</li>
                <li>"Create a chart of sales by category"</li>
              </ul>
            </div>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[70%] rounded-lg px-4 py-2 ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg px-4 py-2">
              <div className="flex items-center space-x-2">
                <div className="animate-pulse">Thinking...</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="px-6 py-4 border-t border-gray-200">
        <div className="flex items-center space-x-2">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask about your analytics..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !message.trim()}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  )
}
```

#### 4.2 Create AI Chat Hook
```typescript
// lib/hooks/useAIChat.ts

import { useState } from 'react'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export function useAIChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const sendMessage = async (content: string) => {
    // Add user message
    setMessages(prev => [...prev, { role: 'user', content }])
    setIsLoading(true)

    try {
      // Call Brain Gateway AI analytics endpoint
      const response = await fetch('/api/analytics/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getAuthToken()}`
        },
        body: JSON.stringify({
          message: content,
          conversation_history: messages
        })
      })

      if (!response.ok) {
        throw new Error('Failed to get AI response')
      }

      const data = await response.json()

      // Add assistant response
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response
      }])
    } catch (error) {
      console.error('AI chat error:', error)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request.'
      }])
    } finally {
      setIsLoading(false)
    }
  }

  return {
    messages,
    sendMessage,
    isLoading
  }
}

function getAuthToken(): string {
  return localStorage.getItem('auth_token') || ''
}
```

#### 4.3 Add AI Chat Route to Brain Gateway
```python
# routes/analytics.py (ADD TO EXISTING FILE)

from services.ai_agents import PersonalAssistantAgent

@router.post("/chat")
async def analytics_chat(
    request: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """
    AI conversational analytics interface.

    - Processes natural language queries
    - Generates SQL from user questions
    - Executes queries with tenant isolation
    - Returns formatted results
    """

    message = request.get("message", "")
    conversation_history = request.get("conversation_history", [])

    # Initialize Personal AI Assistant with RAG/KAG context
    assistant = PersonalAssistantAgent(
        tenant_id=current_user.tenant_id,
        user_context={
            "email": current_user.email,
            "role": current_user.role
        }
    )

    # Process query through RAG/KAG for context
    response = await assistant.process_analytics_query(
        query=message,
        conversation_history=conversation_history
    )

    return {
        "response": response.get("answer", ""),
        "sql_query": response.get("sql", None),
        "chart_config": response.get("chart", None)
    }
```

---

### Phase 5: Build Modular Dockerfile (30 min)

```dockerfile
# Dockerfile.production

FROM node:20-alpine AS base

# Dependencies
FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --legacy-peer-deps

# Builder
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Runner
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3007

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

RUN mkdir .next && chown nextjs:nodejs .next

COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3007

CMD ["node", "server.js"]
```

---

### Phase 6: Build & Deploy (1-2 hours)

#### 6.1 Build Docker Image
```bash
cd /home/alagiri/projects/bizoholic/bizosaas-platform/frontend/apps/analytics-dashboard

# Build
docker build -f Dockerfile.production \
  -t ghcr.io/bizoholic-digital/bizosaas-analytics-dashboard:v1.0.0 \
  -t ghcr.io/bizoholic-digital/bizosaas-analytics-dashboard:latest \
  .

# Push to GHCR
echo "ghp_REDACTED" | docker login ghcr.io -u alagiri.rajesh@gmail.com --password-stdin

docker push ghcr.io/bizoholic-digital/bizosaas-analytics-dashboard:v1.0.0
docker push ghcr.io/bizoholic-digital/bizosaas-analytics-dashboard:latest
```

#### 6.2 Deploy via Dokploy UI
1. Go to: `https://dk.bizoholic.com`
2. Project: **frontend-services**
3. Click: **Add Service** → **Docker Image**
4. Configuration:
   ```
   Name: analytics-dashboard
   Image: ghcr.io/bizoholic-digital/bizosaas-analytics-dashboard:latest
   Port: 3007 → 3001 (container internal)
   Network: dokploy-network
   ```

5. Environment Variables:
   ```
   NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://backend-brain-gateway:8001
   NEXT_PUBLIC_SUPERSET_DOMAIN=http://infrastructure-superset:8088
   NEXTAUTH_URL=https://stg.bizoholic.com/analytics
   NEXTAUTH_SECRET=<generate-random-secret>
   ```

6. Traefik Labels:
   ```
   traefik.enable=true
   traefik.http.routers.analytics-dashboard.rule=Host(`stg.bizoholic.com`) && PathPrefix(`/analytics`)
   traefik.http.routers.analytics-dashboard.entrypoints=websecure
   traefik.http.routers.analytics-dashboard.tls=true
   traefik.http.services.analytics-dashboard.loadbalancer.server.port=3001
   ```

7. Click: **Deploy**

---

## 📊 SUCCESS CRITERIA

### Analytics Dashboard
- ✅ Service running and healthy
- ✅ Accessible at `https://stg.bizoholic.com/analytics`
- ✅ Superset dashboards embedded correctly
- ✅ Guest token authentication working
- ✅ Multi-tenant RLS enforced
- ✅ AI chat interface responding
- ✅ Natural language → SQL working
- ✅ Real-time metrics displayed
- ✅ Authentication protecting routes

### Brain Gateway
- ✅ `/api/analytics/superset/*` routes working
- ✅ Guest token generation functional
- ✅ Dashboard listing working
- ✅ AI chat endpoint responding
- ✅ RAG/KAG context injection working
- ✅ Tenant isolation enforced

### Architecture
- ✅ Modular DDD (`lib/` structure)
- ✅ Self-contained service
- ✅ No workspace dependencies
- ✅ Build context < 1MB
- ✅ Docker image < 300MB

---

## 🎯 NEXT STEPS AFTER COMPLETION

1. **BizOSaaS Admin Dashboard** - Implement with conversational AI interface
2. **Client Portal Chat Interface** - Add AI assistant to Client Portal
3. **CoreLdove Setup Wizard** - Complete migration
4. **MinIO Object Storage** - Deploy for media storage
5. **Authentication Verification** - Document auth implementation across all frontends
6. **AI RAG/KAG Audit** - Verify integration across all services

---

## 📄 DOCUMENTATION TO UPDATE

After implementation:
1. [COMPLETE_FRONTEND_MIGRATION_ROADMAP.md](COMPLETE_FRONTEND_MIGRATION_ROADMAP.md) - Mark analytics dashboard as complete
2. [FRONTEND_ARCHITECTURE_PRINCIPLES.md](FRONTEND_ARCHITECTURE_PRINCIPLES.md) - Add analytics dashboard example
3. [credentials.md](../bizoholic/credentials.md) - Add Superset guest token credentials
4. Create: `ANALYTICS_DASHBOARD_DEPLOYMENT_COMPLETE.md`

---

**Total Estimated Time:** 10-13 hours
**Priority:** HIGH (user-facing analytics)
**Complexity:** MEDIUM-HIGH (Superset SDK + AI chat integration)
**Dependencies:** Brain Gateway routes, Superset running, NextAuth configured

**Status:** 📋 READY FOR IMPLEMENTATION
**Last Updated:** November 4, 2025
