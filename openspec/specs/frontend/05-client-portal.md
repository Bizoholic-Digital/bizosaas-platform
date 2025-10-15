# Client Portal - Frontend Service

## Service Identity
- **Name**: Client Portal (Multi-Tenant Dashboard)
- **Type**: Frontend - Tenant Management (Next.js 15 + TailAdmin v2)
- **Container**: `bizosaas-client-portal-staging`
- **Image**: `ghcr.io/bizoholic-digital/bizosaas-client-portal:staging`
- **Port**: `3001:3000`
- **Domain**: `stg.bizoholic.com/login`
- **Status**: ❌ Unhealthy Container

## Purpose
Multi-tenant client dashboard for managing campaigns, leads, content, and e-commerce operations with TailAdmin v2 UI framework.

## Container Architecture
```
Client Portal Container
├── Next.js 15 (App Router)
├── TailAdmin v2 (Dashboard UI)
├── Alpine.js (Interactions)
├── Multi-Tenant Context
└── Role-Based Access Control
```

## Key Features
- **CRM Management**: View and manage leads
- **Campaign Dashboard**: Monitor campaign performance
- **Content Management**: Edit pages via Wagtail
- **Order Tracking**: View e-commerce orders
- **Analytics**: Tenant-specific analytics
- **Profile Management**: Update account settings

## Multi-Tenancy Pattern
```typescript
// Tenant context from JWT token
const TenantProvider = ({ children }: { children: ReactNode }) => {
  const [tenantId, setTenantId] = useState<string>()
  
  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      const decoded = jwtDecode(token)
      setTenantId(decoded.tenant_id)
    }
  }, [])
  
  return (
    <TenantContext.Provider value={{ tenantId }}>
      {children}
    </TenantContext.Provider>
  )
}
```

## TailAdmin v2 Integration
```typescript
// Dashboard layout with sidebar
export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <div className="relative flex flex-1 flex-col overflow-y-auto overflow-x-hidden">
        <Header />
        <main className="mx-auto max-w-screen-2xl p-4 md:p-6 2xl:p-10">
          {children}
        </main>
      </div>
    </div>
  )
}
```

## API Integration (Tenant-Scoped)
```typescript
// All requests include tenant context
const fetchTenantData = async (endpoint: string) => {
  const response = await fetch(`/api/${endpoint}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'X-Tenant-ID': tenantId
    }
  })
  return response.json()
}

// Tenant-scoped endpoints
GET /api/brain/django-crm/leads?tenant_id={tenant_id}
GET /api/brain/wagtail/pages?tenant_id={tenant_id}
GET /api/brain/saleor/orders?tenant_id={tenant_id}
```

## Deployment Configuration
```yaml
# dokploy-frontend-staging.yml
client-portal-staging:
  image: ghcr.io/bizoholic-digital/bizosaas-client-portal:staging
  environment:
    - NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-staging:8001
    - NEXT_PUBLIC_AUTH_URL=http://bizosaas-auth-staging:8007
  ports:
    - "3001:3000"
  networks:
    - dokploy-network
```

---
**Status**: ❌ Needs Health Check Fix
**Deployment**: Containerized Microservice
**Last Updated**: October 15, 2025
