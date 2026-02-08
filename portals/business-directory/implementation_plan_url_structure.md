# Implementation Plan: Business Directory URL Structure & Routing Refactor

## 1. Overview
We are restructuring the Business Directory URL schema to provide cleaner, more organized routing for businesses, products, and taxonomies. This change also fixes current routing conflicts and prepares the platform for future subdomain features.

### New URL Structure
- **Business Profile**: `/biz/[slug]` (e.g., `/biz/acme-corp`)
- **Product Details**: `/p/[slug]` (e.g., `/p/premium-widget`)
- **Categories**: `/c/[slug]` (e.g., `/c/restaurants`)
- **Tags**: `/t/[slug]` (e.g., `/t/delivery`)
- **Legacy Redirects**: `/business/[slug]` -> `/biz/[slug]`

## 2. Admin Portal Requirements
The Platform Admin must be able to manage this structure:
- **Prefix Configuration**: Ability to change default prefixes (e.g., `/biz` -> `/company`) via Environment Variables or Admin UI.
- **Routing Mode**: Switch between Subfolder Mode (current) and Subdomain Mode (future) per tenant/listing.

## 3. Implementation Steps

### Phase 1: Route Refactoring (Immediate)

#### 1. Fix Middleware & Routing
- [ ] **Middleware Update**: Update `middleware.ts` to stop aggressive wildcard rewriting.
  - Remove logic that treats everything as a business slug.
  - Implement explicit routing for `/biz`, `/p`, `/c`, `/t`.
- [ ] **Next.js Route Migration**:
  - Move `app/[slug]` -> `app/biz/[slug]`
  - Move `app/categories/[slug]` -> `app/c/[slug]` (or keep as alias)
  - Create `app/p/[slug]` for products
  - Create `app/t/[slug]` for tags

#### 2. Update Internal Links & Components
- [ ] Update `BusinessCard` component to link to `/biz/${slug}`.
- [ ] Update `CategoryCard` to link to `/c/${slug}`.
- [ ] Update `Header`, `Footer`, and `Search` components.
- [ ] Ensure `sitemap.xml` and `robots.txt` reflect new paths.

#### 3. Legacy Support
- [ ] Create redirect for old `/business/[slug]` routes to new `/biz/[slug]` structure to preserve any indexed links.

### Phase 2: Admin Controls (Next)

#### 1. Configuration Service
- [ ] Add `NEXT_PUBLIC_ROUTE_PREFIX_BIZ` env var (default: 'biz').
- [ ] Add `NEXT_PUBLIC_ROUTE_PREFIX_PRODUCT` env var (default: 'p').

#### 2. Admin UI
- [ ] Add "Routing" tab in Admin Dashboard > Directory settings.
- [ ] Display current routing schema.

## 4. Technical Details

### Revised Middleware Logic
```typescript
export function middleware(request: NextRequest) {
    const pathname = request.nextUrl.pathname;
    
    // Skip internal paths
    if (pathname.startsWith('/_next') || pathname.startsWith('/api')) return NextResponse.next();

    // Handle legacy redirects
    if (pathname.startsWith('/business/')) {
        return NextResponse.redirect(new URL(pathname.replace('/business/', '/biz/'), request.url));
    }

    // Future: Subdomain logic here
    
    return NextResponse.next();
}
```

### Route Structure
```
app/
  biz/
    [slug]/
      page.tsx
  p/
    [slug]/
      page.tsx
  c/
    [slug]/
      page.tsx
  t/
    [slug]/
      page.tsx
```
