# Admin Dashboard - Frontend Service

## Service Identity
- **Name**: BizOSaaS Admin Dashboard
- **Type**: Frontend - Platform Administration (Next.js 15 + TailAdmin v2 + Mosaic)
- **Container**: `bizosaas-admin-dashboard-staging`
- **Image**: `ghcr.io/bizoholic-digital/bizosaas-admin-dashboard:staging`
- **Port**: `3009:3000`
- **Domain**: `stg.bizoholic.com/admin`
- **Status**: ✅ Running (not tested)

## Purpose
Super admin interface for platform-wide management, cross-tenant analytics, user administration, and system monitoring.

## Container Architecture
```
Admin Dashboard Container
├── Next.js 15 (App Router)
├── TailAdmin v2 (Base Framework)
├── Mosaic Components (Advanced UI)
├── Windster Dashboards (Analytics)
└── Super Admin RBAC
```

## Key Features
- **User Management**: Manage all platform users
- **Tenant Management**: Create and manage tenants
- **System Monitoring**: Platform health and metrics
- **Cross-Tenant Analytics**: Aggregate reporting
- **Service Management**: Monitor all 23 services
- **Workflow Management**: Temporal workflow monitoring

## Role-Based Access Control
```typescript
// Only super_admin role can access
middleware.ts:
export function middleware(request: NextRequest) {
  const token = request.cookies.get('access_token')
  
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  
  const decoded = jwtDecode(token.value)
  
  if (!decoded.roles.includes('super_admin')) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 403 }
    )
  }
  
  return NextResponse.next()
}
```

## Advanced UI Components (Mosaic/Windster)
```typescript
// Analytics dashboard with advanced charts
import { LineChart, BarChart, PieChart } from '@/components/mosaic'

export default function AnalyticsDashboard() {
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
      <LineChart
        title="Revenue Trend"
        data={revenueData}
        className="col-span-2"
      />
      <PieChart
        title="User Distribution"
        data={userDistribution}
      />
      <BarChart
        title="Service Health"
        data={serviceHealth}
        className="col-span-3"
      />
    </div>
  )
}
```

---
**Status**: ✅ Running (needs testing)
**Deployment**: Containerized Microservice
**Last Updated**: October 15, 2025
