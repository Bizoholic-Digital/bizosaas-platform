# Complete Data Flow Diagram - Brain API Gateway Integration

## 🔄 End-to-End Request Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION                             │
│  User clicks "Add Lead" button in CRM Dashboard                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FRONTEND COMPONENT                              │
│  CRMContent.tsx                                                      │
│  • setIsLeadModalOpen(true)                                         │
│  • LeadForm renders with empty initialData                          │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         FORM SUBMISSION                              │
│  LeadForm.tsx                                                        │
│  • User fills: first_name, last_name, email, company, etc.         │
│  • onSubmit(formData) called                                        │
│  • handleCreate('leads', formData) triggered                        │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      CLIENT-SIDE FETCH                               │
│  fetch('/api/brain/django-crm/leads', {                            │
│    method: 'POST',                                                   │
│    headers: { 'Content-Type': 'application/json' },                │
│    body: JSON.stringify(formData)                                   │
│  })                                                                  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      NEXT.JS API ROUTE                               │
│  /app/api/brain/django-crm/leads/route.ts                          │
│                                                                      │
│  export async function POST(request: NextRequest) {                 │
│    // 1. Get session                                                │
│    const session = await getServerSession(authOptions);            │
│                                                                      │
│    // 2. Extract credentials                                        │
│    const access_token = session?.access_token;                     │
│    const tenant_id = session?.user?.tenant_id;                     │
│                                                                      │
│    // 3. Prepare request                                            │
│    const headers = {                                                │
│      'Authorization': `Bearer ${access_token}`,                    │
│      'Content-Type': 'application/json'                            │
│    };                                                                │
│                                                                      │
│    // 4. Forward to Brain API                                       │
│    const response = await fetch(                                    │
│      `${BRAIN_API_URL}/api/crm/leads?tenant_id=${tenant_id}`,     │
│      { method: 'POST', headers, body: request.body }               │
│    );                                                                │
│                                                                      │
│    return NextResponse.json(await response.json());                │
│  }                                                                   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    BRAIN API GATEWAY (FastAPI)                       │
│  http://localhost:8001                                               │
│                                                                      │
│  @app.post("/api/crm/leads")                                        │
│  async def create_lead(                                              │
│      lead_data: LeadCreate,                                         │
│      tenant_id: str = Query(...),                                   │
│      token: str = Depends(verify_token)                            │
│  ):                                                                  │
│      # 1. Validate token with Auth Service                          │
│      user = await validate_token(token)                             │
│                                                                      │
│      # 2. Verify tenant access                                      │
│      if user.tenant_id != tenant_id:                                │
│          raise HTTPException(403, "Forbidden")                      │
│                                                                      │
│      # 3. Add tenant_id to lead data                                │
│      lead_data.tenant_id = tenant_id                                │
│                                                                      │
│      # 4. Forward to Django CRM                                     │
│      response = requests.post(                                       │
│          f"{DJANGO_CRM_URL}/api/leads/",                           │
│          json=lead_data.dict(),                                     │
│          headers={"Authorization": f"Bearer {token}"}              │
│      )                                                               │
│                                                                      │
│      return response.json()                                         │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DJANGO CRM SERVICE                                │
│  http://localhost:8002                                               │
│                                                                      │
│  @api_view(['POST'])                                                │
│  @permission_classes([IsAuthenticated])                            │
│  def create_lead(request):                                          │
│      # 1. Validate token (already done by decorator)                │
│      user = request.user                                            │
│                                                                      │
│      # 2. Extract data                                              │
│      data = request.data                                            │
│      tenant_id = data.get('tenant_id')                             │
│                                                                      │
│      # 3. Verify tenant access                                      │
│      if user.tenant_id != tenant_id:                                │
│          return Response({"error": "Forbidden"}, status=403)       │
│                                                                      │
│      # 4. Create lead in database                                   │
│      lead = Lead.objects.create(                                    │
│          tenant_id=tenant_id,                                       │
│          first_name=data['first_name'],                            │
│          last_name=data['last_name'],                              │
│          email=data['email'],                                       │
│          company=data['company'],                                   │
│          # ... other fields                                         │
│      )                                                               │
│                                                                      │
│      # 5. Return created lead                                       │
│      return Response(LeadSerializer(lead).data, status=201)        │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        DATABASE WRITE                                │
│  PostgreSQL                                                          │
│                                                                      │
│  INSERT INTO leads (                                                 │
│      id, tenant_id, first_name, last_name,                          │
│      email, company, created_at, updated_at                         │
│  ) VALUES (                                                          │
│      uuid_generate_v4(),                                            │
│      '123e4567-e89b-12d3-a456-426614174000',                       │
│      'John', 'Doe',                                                 │
│      'john@example.com', 'Acme Corp',                              │
│      NOW(), NOW()                                                    │
│  ) RETURNING *;                                                      │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       RESPONSE CHAIN                                 │
│                                                                      │
│  Database → Django CRM                                              │
│  {                                                                   │
│    "id": "789...",                                                  │
│    "tenant_id": "123...",                                           │
│    "first_name": "John",                                            │
│    "last_name": "Doe",                                              │
│    "email": "john@example.com",                                     │
│    "company": "Acme Corp",                                          │
│    "status": "new",                                                 │
│    "created_at": "2025-12-03T20:00:00Z"                            │
│  }                                                                   │
│                                                                      │
│  Django CRM → Brain API Gateway                                     │
│  (same JSON)                                                         │
│                                                                      │
│  Brain API Gateway → Next.js API Route                              │
│  (same JSON)                                                         │
│                                                                      │
│  Next.js API Route → Frontend                                       │
│  (same JSON)                                                         │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FRONTEND UPDATE                                 │
│  CRMContent.tsx                                                      │
│                                                                      │
│  if (response.ok) {                                                  │
│    // 1. Close modal                                                │
│    setIsLeadModalOpen(false);                                       │
│    setSelectedItem(null);                                           │
│                                                                      │
│    // 2. Refresh data                                               │
│    await refreshData();                                             │
│                                                                      │
│    // 3. UI updates automatically via React state                   │
│    // New lead appears in table                                     │
│  }                                                                   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         USER SEES RESULT                             │
│  • Modal closes                                                      │
│  • Table refreshes                                                   │
│  • New lead "John Doe" appears in the list                          │
│  • Success! ✅                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔒 Security Layers

```
Layer 1: NextAuth Session
    ↓
    • User must be logged in
    • Session contains valid JWT
    • Session not expired

Layer 2: Next.js API Route
    ↓
    • getServerSession() validates session
    • Extracts access_token & tenant_id
    • No client-side token exposure

Layer 3: Brain API Gateway
    ↓
    • Validates JWT with Auth Service
    • Checks token expiry
    • Verifies tenant_id matches user

Layer 4: Backend Service (Django CRM)
    ↓
    • Re-validates JWT
    • Checks user permissions
    • Enforces tenant isolation in database query

Layer 5: Database
    ↓
    • Row-level security (RLS)
    • All queries filtered by tenant_id
    • No cross-tenant data access possible
```

---

## 📊 Performance Optimization

### Caching Strategy
```
1. Browser Cache
   • Static assets (JS, CSS, images)
   • Service worker for offline support

2. Next.js Cache
   • API routes: cache: 'no-store' (always fresh)
   • Static pages: ISR with revalidation

3. Brain API Cache
   • Redis cache for frequently accessed data
   • Cache invalidation on mutations
   • TTL: 5 minutes for list endpoints

4. Database Cache
   • PostgreSQL query cache
   • Materialized views for complex queries
   • Index optimization
```

### Request Optimization
```
1. Parallel Fetching
   • useEffect fetches all endpoints simultaneously
   • Promise.all() for concurrent requests

2. Pagination
   • Limit: 20 items per page
   • Cursor-based pagination for large datasets

3. Selective Loading
   • Only fetch data for active tab
   • Lazy load images and heavy components

4. Debouncing
   • Search input: 300ms debounce
   • Filter changes: 500ms debounce
```

---

## 🎯 Data Consistency

### Optimistic Updates (Future Enhancement)
```typescript
const handleCreate = async (type: string, data: any) => {
  // 1. Optimistic update
  const tempId = `temp-${Date.now()}`;
  const optimisticItem = { id: tempId, ...data };
  setCrmData(prev => ({
    ...prev,
    [type]: [...prev[type], optimisticItem]
  }));

  try {
    // 2. API call
    const response = await fetch(`/api/brain/django-crm/${type}`, {
      method: 'POST',
      body: JSON.stringify(data)
    });

    if (response.ok) {
      // 3. Replace temp with real data
      const realItem = await response.json();
      setCrmData(prev => ({
        ...prev,
        [type]: prev[type].map(item => 
          item.id === tempId ? realItem : item
        )
      }));
    } else {
      // 4. Rollback on error
      setCrmData(prev => ({
        ...prev,
        [type]: prev[type].filter(item => item.id !== tempId)
      }));
    }
  } catch (error) {
    // Rollback
  }
};
```

---

**Last Updated:** 2025-12-03 20:10 IST
