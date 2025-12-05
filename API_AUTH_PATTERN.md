# Session-Based Authentication Pattern for API Routes

This guide shows how to update API routes to use NextAuth session for authentication and tenant isolation.

## Pattern Template

### 1. Add Imports (Top of File)

```typescript
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
```

### 2. GET Method Pattern

```typescript
export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    const searchParams = request.nextUrl.searchParams
    
    // Build URL with params
    let url = `${BRAIN_API_URL}/api/your/endpoint`
    const params = new URLSearchParams()
    
    // Add tenant_id from session if available
    if (session?.user?.tenant_id) {
      params.set('tenant_id', session.user.tenant_id);
    }
    
    // Add other query params
    if (searchParams.get('param1')) params.set('param1', searchParams.get('param1')!)
    
    url += `?${params.toString()}`

    // Build headers with auth
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (session?.access_token) {
      headers["Authorization"] = `Bearer ${session.access_token}`;
    } else if (request.headers.get("authorization")) {
      headers["Authorization"] = request.headers.get("authorization")!;
    }

    const response = await fetch(url, {
      headers,
      cache: 'no-store',
    })
    
    // ... rest of method
  } catch (error) {
    // ... error handling
  }
}
```

### 3. POST/PUT/DELETE Method Pattern

```typescript
export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_URL}/api/your/endpoint`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': session?.access_token 
          ? `Bearer ${session.access_token}` 
          : (request.headers.get('authorization') || ''),
      },
      body: JSON.stringify(body)
    })
    
    // ... rest of method
  } catch (error) {
    // ... error handling
  }
}
```

## Routes to Update

### CRM Routes (Priority: High)
- [ ] `/app/api/brain/django-crm/contacts/route.ts`
- [ ] `/app/api/brain/django-crm/deals/route.ts`
- [ ] `/app/api/brain/django-crm/activities/route.ts`
- [ ] `/app/api/brain/django-crm/tasks/route.ts`
- [ ] `/app/api/brain/django-crm/opportunities/route.ts`

### CMS Routes (Priority: High)
- [ ] `/app/api/brain/wagtail/pages/route.ts`
- [ ] `/app/api/brain/wagtail/posts/route.ts`
- [ ] `/app/api/brain/wagtail/media/route.ts`
- [ ] `/app/api/brain/wagtail/forms/route.ts`
- [ ] `/app/api/brain/wagtail/templates/route.ts`

### Marketing Routes (Priority: Medium)
- [ ] `/app/api/brain/marketing/campaigns/route.ts`
- [ ] `/app/api/brain/marketing/email/route.ts`
- [ ] `/app/api/brain/marketing/social/route.ts`
- [ ] `/app/api/brain/marketing/automation/route.ts`
- [ ] `/app/api/brain/marketing/leads/route.ts`

### Analytics Routes (Priority: Medium)
- [ ] `/app/api/brain/analytics/overview/route.ts`
- [ ] `/app/api/brain/analytics/traffic/route.ts`

### Billing Routes (Priority: High)
- [ ] `/app/api/brain/billing/subscriptions/route.ts`
- [ ] `/app/api/brain/billing/invoices/route.ts`
- [ ] `/app/api/brain/billing/payment-methods/route.ts`
- [ ] `/app/api/brain/billing/usage/route.ts`

### Integration Routes (Priority: Medium)
- [ ] `/app/api/brain/integrations/webhooks/route.ts`
- [ ] `/app/api/brain/integrations/api-keys/route.ts`
- [ ] `/app/api/brain/integrations/third-party/route.ts`

## Quick Update Script

For each route file:

1. **Add imports** at the top
2. **In GET method**: 
   - Add `const session = await getServerSession(authOptions);` after try
   - Add tenant_id to params if session exists
   - Replace headers object with pattern above
3. **In POST/PUT/DELETE methods**:
   - Add `const session = await getServerSession(authOptions);` before fetch
   - Update Authorization header to use session token

## Testing Checklist

After updating each route:
- [ ] Verify imports are correct
- [ ] Check that `tenant_id` is added to GET requests
- [ ] Confirm Authorization header uses session token
- [ ] Test with authenticated user
- [ ] Verify fallback data still works
- [ ] Check error handling

## Benefits

✅ **Security**: Tokens handled server-side only  
✅ **Tenant Isolation**: Automatic tenant filtering  
✅ **Consistency**: Same pattern across all routes  
✅ **Maintainability**: Easy to update and debug  
✅ **Scalability**: Works with any number of tenants
