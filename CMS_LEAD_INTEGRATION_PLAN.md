# CMS & Lead Capture Integration Plan

**Date:** 2025-12-03 20:15 IST  
**Objective:** Integrate Bizoholic forms with Django CRM and Wagtail CMS with Client Portal

---

## Phase 1: Bizoholic Frontend → Django CRM Lead Capture

### Forms to Integrate
1. **Contact Form** (`/brands/bizoholic/app/contact/page.tsx`)
2. **Service Inquiry Forms** (across service pages)
3. **Newsletter Signup** (footer/homepage)
4. **Demo Request Form**
5. **Quote Request Form**

### Integration Pattern
```typescript
// Bizoholic Frontend Form
const handleSubmit = async (formData) => {
  // Send to Brain API Gateway
  const response = await fetch('/api/crm/lead-capture', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      source: 'bizoholic_contact_form',
      ...formData
    })
  });
};
```

### API Route Structure
```
/brands/bizoholic/app/api/crm/
  ├── lead-capture/route.ts    (Public - no auth required)
  ├── newsletter/route.ts       (Public)
  └── demo-request/route.ts     (Public)
```

### Brain API Endpoints
```
POST /api/public/crm/leads
  - No authentication required
  - Rate limiting enabled
  - CAPTCHA verification
  - Auto-assigns to default tenant
```

---

## Phase 2: Wagtail CMS → Client Portal Dashboard

### CMS Modules to Integrate

#### 1. Pages Management
```
/app/dashboard → CMS Tab → Pages
  - List all pages
  - Create new page
  - Edit existing page
  - Publish/Unpublish
  - Preview
  - Delete
```

#### 2. Blog/Posts Management
```
/app/dashboard → CMS Tab → Posts
  - List all blog posts
  - Create new post
  - Edit post
  - Manage categories
  - Manage tags
  - Schedule publishing
```

#### 3. Media Library
```
/app/dashboard → CMS Tab → Media
  - Upload images
  - Upload documents
  - Organize in folders
  - Search media
  - Delete media
```

#### 4. Navigation/Menus
```
/app/dashboard → CMS Tab → Navigation
  - Edit main menu
  - Edit footer menu
  - Drag-and-drop ordering
  - Add/remove items
```

#### 5. Forms Management
```
/app/dashboard → CMS Tab → Forms
  - List form submissions
  - View form data
  - Export submissions
  - Form builder (future)
```

#### 6. Templates
```
/app/dashboard → CMS Tab → Templates
  - List page templates
  - Create custom templates
  - Edit template structure
```

### API Routes Structure
```
/portals/client-portal/app/api/brain/wagtail/
  ├── pages/
  │   └── route.ts (GET, POST, PUT, DELETE)
  ├── posts/
  │   └── route.ts (GET, POST, PUT, DELETE)
  ├── media/
  │   └── route.ts (GET, POST, DELETE)
  ├── navigation/
  │   └── route.ts (GET, PUT)
  ├── forms/
  │   └── route.ts (GET)
  └── templates/
      └── route.ts (GET, POST, PUT, DELETE)
```

### Brain API Gateway Endpoints
```
Wagtail CMS Routes:
GET    /api/cms/pages?tenant_id=xxx
POST   /api/cms/pages
PUT    /api/cms/pages/{id}
DELETE /api/cms/pages/{id}

GET    /api/cms/posts?tenant_id=xxx
POST   /api/cms/posts
PUT    /api/cms/posts/{id}
DELETE /api/cms/posts/{id}

GET    /api/cms/media?tenant_id=xxx
POST   /api/cms/media (multipart/form-data)
DELETE /api/cms/media/{id}

GET    /api/cms/navigation?tenant_id=xxx
PUT    /api/cms/navigation

GET    /api/cms/forms?tenant_id=xxx
GET    /api/cms/forms/{id}/submissions

GET    /api/cms/templates?tenant_id=xxx
POST   /api/cms/templates
PUT    /api/cms/templates/{id}
DELETE /api/cms/templates/{id}
```

---

## Implementation Steps

### Step 1: Lead Capture Integration (Bizoholic → Django CRM)

1. ✅ Create public API route in Bizoholic
2. ✅ Update contact form to submit to API
3. ✅ Add rate limiting
4. ✅ Add CAPTCHA verification
5. ✅ Test lead capture flow

### Step 2: Wagtail API Routes (Client Portal)

1. ✅ Create `/api/brain/wagtail/pages/route.ts`
2. ✅ Create `/api/brain/wagtail/posts/route.ts`
3. ✅ Create `/api/brain/wagtail/media/route.ts`
4. ✅ Create `/api/brain/wagtail/navigation/route.ts`
5. ✅ Create `/api/brain/wagtail/forms/route.ts`
6. ✅ Create `/api/brain/wagtail/templates/route.ts`

### Step 3: CMS Components (Client Portal)

1. ✅ Create `CMSContent.tsx` component
2. ✅ Create `PageForm.tsx`
3. ✅ Create `PostForm.tsx`
4. ✅ Create `MediaUploader.tsx`
5. ✅ Create `NavigationEditor.tsx`
6. ✅ Create `FormSubmissionsViewer.tsx`
7. ✅ Create `TemplateEditor.tsx`

### Step 4: Dashboard Integration

1. ✅ Add CMS tab to dashboard
2. ✅ Add sub-tabs for each CMS module
3. ✅ Integrate CMSContent component
4. ✅ Add RBAC permissions for CMS access

### Step 5: Testing & Validation

1. ⏳ Test lead capture from Bizoholic
2. ⏳ Verify leads appear in Client Portal CRM
3. ⏳ Test page creation in CMS
4. ⏳ Verify pages appear on Bizoholic frontend
5. ⏳ Test media upload
6. ⏳ Test navigation editing
7. ⏳ End-to-end CMS workflow

---

## Data Flow: Lead Capture

```
Bizoholic Contact Form
    ↓
POST /api/crm/lead-capture
    ↓
Brain API Gateway
POST /api/public/crm/leads
    ↓
Django CRM Service
    ↓
Database: leads table
    ↓
Client Portal CRM Dashboard
(Leads appear automatically)
```

## Data Flow: CMS Page Creation

```
Client Portal CMS Tab
    ↓
User creates new page
    ↓
POST /api/brain/wagtail/pages
    ↓
Brain API Gateway
POST /api/cms/pages?tenant_id=xxx
    ↓
Wagtail Service
    ↓
Database: wagtailcore_page table
    ↓
Bizoholic Frontend
(Page appears in navigation)
```

---

## Security Considerations

### Lead Capture (Public Endpoints)
- ✅ Rate limiting: 10 requests/minute per IP
- ✅ CAPTCHA verification (Google reCAPTCHA v3)
- ✅ Input validation & sanitization
- ✅ Honeypot fields for bot detection
- ✅ Email verification for newsletter

### CMS Endpoints (Authenticated)
- ✅ Session-based authentication
- ✅ Tenant isolation
- ✅ RBAC permissions (only admins can edit)
- ✅ Content versioning
- ✅ Audit logging

---

## File Structure

```
/brands/bizoholic/
  └── app/
      ├── api/
      │   └── crm/
      │       ├── lead-capture/route.ts
      │       ├── newsletter/route.ts
      │       └── demo-request/route.ts
      └── contact/
          └── page.tsx (updated)

/portals/client-portal/
  ├── app/
  │   └── api/
  │       └── brain/
  │           └── wagtail/
  │               ├── pages/route.ts
  │               ├── posts/route.ts
  │               ├── media/route.ts
  │               ├── navigation/route.ts
  │               ├── forms/route.ts
  │               └── templates/route.ts
  └── components/
      ├── CMSContent.tsx
      ├── PageForm.tsx
      ├── PostForm.tsx
      ├── MediaUploader.tsx
      ├── NavigationEditor.tsx
      ├── FormSubmissionsViewer.tsx
      └── TemplateEditor.tsx
```

---

## Next Actions

1. **Immediate:** Create lead capture API in Bizoholic
2. **Immediate:** Update Bizoholic contact form
3. **Short-term:** Create Wagtail API routes
4. **Short-term:** Create CMS components
5. **Medium-term:** Add advanced CMS features (page builder, etc.)

---

**Status:** Ready to implement  
**Estimated Time:** 3-4 hours  
**Priority:** High
