# Frontend Page Structure and Authentication Plan

## Overview
All 7 frontends need proper page structure with public and private routes protected by authentication.

---

## 1. Bizoholic Frontend (Port 3001)
**Purpose:** Main marketing website and business portal

### Public Pages
- `/` - Homepage (landing page)
- `/about` - About us
- `/services` - Services listing
- `/contact` - Contact form
- `/login` - Login page
- `/signup` - Registration page
- `/forgot-password` - Password reset

### Private Pages (Requires Auth)
- `/dashboard` - Main dashboard
- `/profile` - User profile
- `/settings` - Account settings
- `/billing` - Billing & subscriptions
- `/support` - Support tickets
- `/reports` - Business reports

---

## 2. CoreLDove Storefront (Port 3002)
**Purpose:** E-commerce storefront (Saleor-based)

### Public Pages
- `/` - Homepage (product showcase)
- `/products` - Product catalog
- `/products/[slug]` - Product details
- `/categories` - Category listing
- `/cart` - Shopping cart
- `/login` - Customer login
- `/register` - Customer registration

### Private Pages (Requires Auth)
- `/account` - Customer account
- `/account/orders` - Order history
- `/account/addresses` - Saved addresses
- `/account/wishlist` - Wishlist
- `/checkout` - Checkout process
- `/account/settings` - Account settings

---

## 3. Client Portal (Port 3003)
**Purpose:** Multi-tenant client dashboard

### Public Pages
- `/login` - Login page
- `/signup` - Registration
- `/forgot-password` - Password reset

### Private Pages (Requires Auth)
- `/` - Redirects to dashboard
- `/dashboard` - Main dashboard
- `/analytics` - Analytics dashboard
- `/campaigns` - Marketing campaigns
- `/crm` - CRM interface
- `/chat` - AI chat interface
- `/automation` - Automation workflows
- `/reports` - Reports & insights
- `/settings` - Portal settings
- `/billing` - Billing management
- `/team` - Team management
- `/integrations` - Third-party integrations

---

## 4. Business Directory (Port 3004)
**Purpose:** Local business listings

### Public Pages
- `/` - Homepage with search
- `/search` - Search results
- `/categories` - Category listing
- `/listings/[id]` - Business details
- `/about` - About the directory
- `/contact` - Contact page
- `/login` - Business owner login
- `/register` - Business registration

### Private Pages (Requires Auth)
- `/dashboard` - Business dashboard
- `/my-listing` - Manage listing
- `/analytics` - Listing analytics
- `/reviews` - Manage reviews
- `/messages` - Customer messages
- `/billing` - Subscription management
- `/settings` - Account settings

---

## 5. BizOSaaS Admin (Port 3005)
**Purpose:** Super admin dashboard

### Public Pages
- `/login` - Admin login
- `/forgot-password` - Password reset

### Private Pages (Requires Auth + Admin Role)
- `/` - Admin dashboard
- `/users` - User management
- `/tenants` - Tenant management
- `/services` - Service monitoring
- `/analytics` - Platform analytics
- `/billing` - Billing overview
- `/support` - Support tickets
- `/settings` - Platform settings
- `/ai-agents` - AI agent management
- `/logs` - System logs
- `/webhooks` - Webhook management

---

## 6. ThrillRing Gaming (Port 3006)
**Purpose:** Gaming and tournament platform

### Public Pages
- `/` - Homepage
- `/games` - Game catalog
- `/tournaments` - Tournament listings
- `/leaderboard` - Global leaderboard
- `/about` - About platform
- `/login` - Player login
- `/register` - Player registration

### Private Pages (Requires Auth)
- `/dashboard` - Player dashboard
- `/profile` - Player profile
- `/my-games` - Owned games
- `/my-tournaments` - Joined tournaments
- `/wallet` - Gaming wallet
- `/achievements` - Achievements
- `/friends` - Friend list
- `/messages` - Messaging
- `/settings` - Gaming settings

---

## 7. Analytics Dashboard (Port 3007)
**Purpose:** Business intelligence platform

### Public Pages
- `/login` - Login page
- `/demo` - Demo dashboard (optional)

### Private Pages (Requires Auth)
- `/` - Main analytics dashboard
- `/reports` - Report builder
- `/dashboards` - Custom dashboards
- `/data-sources` - Data source management
- `/visualizations` - Visualization gallery
- `/alerts` - Alert configuration
- `/exports` - Export center
- `/settings` - Dashboard settings
- `/team` - Team collaboration

---

## Authentication Implementation Requirements

### 1. Middleware Configuration
Each frontend needs middleware.ts that:
- Checks for auth token
- Redirects unauthenticated users to /login
- Allows access to public routes
- Protects private routes

### 2. Auth Context Implementation
- AuthProvider wrapping the app
- useAuth hook for components
- Token refresh logic
- Logout functionality

### 3. Role-Based Access Control (RBAC)
- Check user roles for admin dashboards
- Tenant isolation for multi-tenant apps
- Permission-based UI rendering

### 4. Session Management
- JWT token in memory
- Refresh token in httpOnly cookie
- Auto-refresh before expiry
- Logout across all tabs

---

## Implementation Checklist

### For Each Frontend:
- [ ] Create all public pages
- [ ] Create all private pages
- [ ] Implement middleware.ts
- [ ] Add AuthProvider to layout
- [ ] Create login/signup forms
- [ ] Add logout functionality
- [ ] Test auth flow
- [ ] Verify route protection
- [ ] Test role-based access
- [ ] Ensure tenant isolation

---

## Testing Checklist

### Auth Flow Tests:
1. **Public Access Test**
   - Can access public pages without login
   - Cannot access private pages without login

2. **Login Flow Test**
   - Login redirects to dashboard
   - Token stored correctly
   - User info loaded

3. **Protected Route Test**
   - Private pages require auth
   - Redirect to login if not authenticated
   - Return to requested page after login

4. **Logout Test**
   - Clears tokens
   - Redirects to public page
   - Cannot access private pages after logout

5. **Token Refresh Test**
   - Auto-refreshes before expiry
   - Maintains session
   - Handles refresh failures

6. **Role-Based Access Test**
   - Admin-only pages protected
   - Correct UI based on permissions
   - Tenant data isolation

---

## Priority Order for Implementation

1. **Client Portal** - Most complex, already has some implementation
2. **BizOSaaS Admin** - Critical for platform management
3. **Bizoholic Frontend** - Main entry point
4. **Business Directory** - Customer-facing
5. **CoreLDove Storefront** - E-commerce critical
6. **ThrillRing Gaming** - Gaming platform
7. **Analytics Dashboard** - BI platform