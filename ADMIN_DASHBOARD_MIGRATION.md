# Admin Dashboard Migration Plan
## Moving from `/portals/admin-portal/bizosaas-admin` to `/portals/admin-dashboard`

**Date**: 2025-12-11  
**Goal**: Reuse existing admin dashboard and align with Architecture V4

---

## Current State Analysis

### ✅ What We Have (Existing Admin Dashboard)

**Location**: `/portals/admin-portal/bizosaas-admin`

**Features Already Implemented**:
1. ✅ **Dashboard** - Metrics, activities, system stats
2. ✅ **Tenant Management** (`/tenants`)
3. ✅ **User Management** (`/users`)
4. ✅ **AI Agents** (`/ai-agents`, `/agents`)
5. ✅ **Integrations** (`/integrations`)
6. ✅ **Workflows** (`/workflows`)
7. ✅ **CMS Management** (`/cms`)
8. ✅ **System Health** (`/system-health`)
9. ✅ **Monitoring** (`/monitoring`)
10. ✅ **Security** (`/security`)
11. ✅ **Settings** (`/settings`)
12. ✅ **Revenue** (`/revenue`)
13. ✅ **API Analytics** (`/api-analytics`)
14. ✅ **Dropshipping** (`/dropshipping`)
15. ✅ **Chat** (`/chat`)
16. ✅ **Admin Tools** (`/admin`)

**Tech Stack**:
- Next.js 15.5.3
- React 19.0.0
- TypeScript
- Tailwind CSS
- Shadcn UI components
- Radix UI primitives
- React Query
- React Table
- Recharts (for graphs)
- Zustand (state management)

**Port**: 3009

---

## Migration Strategy

### Option 1: Move and Rename ✅ (RECOMMENDED)

**Steps**:
1. Move `/portals/admin-portal/bizosaas-admin` → `/portals/admin-dashboard`
2. Update package.json name
3. Update port to 3004 (to avoid conflict with client portal on 3003)
4. Update environment variables
5. Align with Architecture V4 structure
6. Connect to Brain Gateway

**Benefits**:
- ✅ Reuse all existing work
- ✅ Fast implementation (90% done)
- ✅ Proven UI/UX
- ✅ All features already built

**Effort**: 1-2 days

### Option 2: Keep Both (NOT RECOMMENDED)

Keep admin-portal and create new admin-dashboard

**Issues**:
- ❌ Duplicate code
- ❌ Confusion
- ❌ More maintenance

---

## Detailed Migration Steps

### Step 1: Move Directory Structure

```bash
# Remove the incomplete create-next-app attempt
rm -rf portals/admin-dashboard

# Move existing admin to new location
mv portals/admin-portal/bizosaas-admin portals/admin-dashboard

# Remove old admin-portal directory
rm -rf portals/admin-portal
```

### Step 2: Update Configuration Files

**package.json**:
```json
{
  "name": "bizosaas-admin-dashboard",
  "version": "2.0.0",
  "description": "BizOSaaS Platform Admin Dashboard - Architecture V4",
  "scripts": {
    "dev": "next dev --port 3004",
    "build": "next build",
    "start": "next start --port 3004"
  }
}
```

**next.config.js**:
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_BRAIN_GATEWAY_URL: process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8000',
    NEXT_PUBLIC_AUTH_URL: process.env.NEXT_PUBLIC_AUTH_URL || 'http://localhost:8008',
  },
  async rewrites() {
    return [
      {
        source: '/api/brain/:path*',
        destination: 'http://localhost:8000/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
```

**.env.local** (create):
```env
# Brain Gateway
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://localhost:8000

# Auth Service
NEXT_PUBLIC_AUTH_URL=http://localhost:8008

# Temporal UI
NEXT_PUBLIC_TEMPORAL_UI_URL=http://localhost:8233

# Vault UI
NEXT_PUBLIC_VAULT_UI_URL=http://localhost:8200

# Environment
NODE_ENV=development
```

### Step 3: Align with Architecture V4

**Create new pages aligned with V4 structure**:

```
app/
├── dashboard/              # ✅ Already exists
├── platform/               # NEW - Platform Management
│   ├── tenants/           # Move from /tenants
│   ├── health/            # Move from /system-health
│   ├── monitoring/        # Move from /monitoring
│   └── billing/           # Move from /revenue
├── ai-agents/             # ✅ Already exists
│   ├── playground/        # Enhance existing
│   ├── metrics/           # NEW
│   ├── fine-tuning/       # NEW
│   └── prompts/           # NEW
├── connectors/            # Move from /integrations
│   ├── registry/          # NEW
│   ├── oauth-apps/        # NEW
│   ├── rate-limits/       # NEW
│   └── health/            # NEW
└── system/                # NEW - System Settings
    ├── feature-flags/     # NEW
    ├── environment/       # NEW
    ├── security/          # Move from /security
    └── audit/             # NEW
```

### Step 4: Connect to Brain Gateway

**Create API client** (`lib/api-client.ts`):
```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth interceptor
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
```

**Create service hooks** (`lib/hooks/use-tenants.ts`):
```typescript
import { useQuery, useMutation } from '@tanstack/react-query';
import apiClient from '@/lib/api-client';

export function useTenants() {
  return useQuery({
    queryKey: ['tenants'],
    queryFn: async () => {
      const { data } = await apiClient.get('/api/admin/tenants');
      return data;
    },
  });
}

export function useCreateTenant() {
  return useMutation({
    mutationFn: async (tenantData: any) => {
      const { data } = await apiClient.post('/api/admin/tenants', tenantData);
      return data;
    },
  });
}
```

### Step 5: Add Missing Features

**Features to add** (from Architecture V4):

1. **AI Agent Fine-Tuning Interface**
   - Model selection
   - Temperature controls
   - Prompt templates
   - A/B testing

2. **Connector OAuth App Configuration**
   - Manage OAuth client IDs/secrets
   - Configure redirect URIs
   - Test OAuth flows

3. **Feature Flags Management**
   - Enable/disable features
   - Gradual rollout
   - A/B testing

4. **Audit Logs Viewer**
   - View all system actions
   - Filter by user/action/date
   - Export logs

### Step 6: Update Navigation

**Update sidebar** (`components/admin-sidebar.tsx`):
```typescript
const navigation = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: HomeIcon,
  },
  {
    name: 'Platform',
    icon: ServerIcon,
    children: [
      { name: 'Tenants', href: '/platform/tenants' },
      { name: 'Health', href: '/platform/health' },
      { name: 'Monitoring', href: '/platform/monitoring' },
      { name: 'Billing', href: '/platform/billing' },
    ],
  },
  {
    name: 'AI Agents',
    icon: BotIcon,
    children: [
      { name: 'Playground', href: '/ai-agents/playground' },
      { name: 'Metrics', href: '/ai-agents/metrics' },
      { name: 'Fine-Tuning', href: '/ai-agents/fine-tuning' },
      { name: 'Prompts', href: '/ai-agents/prompts' },
    ],
  },
  {
    name: 'Connectors',
    icon: PlugIcon,
    children: [
      { name: 'Registry', href: '/connectors/registry' },
      { name: 'OAuth Apps', href: '/connectors/oauth-apps' },
      { name: 'Rate Limits', href: '/connectors/rate-limits' },
      { name: 'Health', href: '/connectors/health' },
    ],
  },
  {
    name: 'System',
    icon: SettingsIcon,
    children: [
      { name: 'Feature Flags', href: '/system/feature-flags' },
      { name: 'Environment', href: '/system/environment' },
      { name: 'Security', href: '/system/security' },
      { name: 'Audit Logs', href: '/system/audit' },
    ],
  },
];
```

### Step 7: Add Role-Based Access Control

**Create middleware** (`middleware.ts`):
```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Check if user is authenticated
  const token = request.cookies.get('auth_token');
  
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  // Check if user has admin role
  // This should verify with Brain Gateway
  const userRole = request.cookies.get('user_role')?.value;
  
  if (userRole !== 'platform_admin' && userRole !== 'super_admin') {
    return NextResponse.redirect(new URL('/unauthorized', request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/platform/:path*',
    '/ai-agents/:path*',
    '/connectors/:path*',
    '/system/:path*',
  ],
};
```

---

## Timeline

### Day 1: Migration & Setup
- [x] Move directory structure
- [ ] Update configuration files
- [ ] Update package.json
- [ ] Create .env.local
- [ ] Test basic startup

### Day 2: Integration & Alignment
- [ ] Connect to Brain Gateway
- [ ] Create API client
- [ ] Update navigation structure
- [ ] Add RBAC middleware
- [ ] Test authentication flow

### Day 3: Feature Enhancement
- [ ] Add AI agent fine-tuning interface
- [ ] Add connector OAuth configuration
- [ ] Add feature flags management
- [ ] Add audit logs viewer

### Day 4: Testing & Polish
- [ ] Test all features
- [ ] Fix bugs
- [ ] Update documentation
- [ ] Deploy to staging

**Total Time**: 4 days (vs 3 weeks for new build)

---

## Success Criteria

- [ ] Admin dashboard accessible on port 3004
- [ ] All existing features working
- [ ] Connected to Brain Gateway (port 8000)
- [ ] RBAC enforced (only platform admins can access)
- [ ] New features added (fine-tuning, OAuth config, feature flags, audit logs)
- [ ] No conflicts with client portal (port 3003)
- [ ] All navigation aligned with Architecture V4
- [ ] Documentation updated

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking existing features | High | Test thoroughly before migration |
| Port conflicts | Medium | Use port 3004, document clearly |
| Auth integration issues | High | Test with Brain Gateway early |
| Missing dependencies | Low | Review package.json carefully |

---

## Next Steps

1. ✅ Cancel create-next-app command (DONE)
2. ⏳ Move directory structure
3. ⏳ Update configuration
4. ⏳ Test basic functionality
5. ⏳ Connect to Brain Gateway
6. ⏳ Add missing features
7. ⏳ Deploy and test

**Estimated Completion**: 4 days (90% faster than building from scratch!)
