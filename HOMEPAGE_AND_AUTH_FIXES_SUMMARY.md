# Homepage and Client Portal Authentication Fixes

## Date: 2025-12-02

## Issues Fixed

### 1. Homepage Only Showing 3 Service Cards Instead of 9

**Root Cause:**
The fallback data in the API route handlers only contained 3 services instead of all 9.

**Files Modified:**
1. `/brands/bizoholic/frontend/app/api/brain/wagtail/homepage/route.ts`
2. `/brands/bizoholic/frontend/app/api/brain/wagtail/services/route.ts`
3. `/brands/bizoholic/frontend/app/page.tsx`

**Changes Made:**

#### A. Updated `homepage/route.ts` fallbackHomepage
- **Before:** Only had 3 features (AI Campaign Management, Content Generation, Performance Analytics)
- **After:** Now includes all 9 services:
  1. AI Campaign Management
  2. Content Generation
  3. Performance Analytics
  4. Marketing Automation
  5. Strategy Consulting
  6. Creative Design
  7. SEO Optimization
  8. Email Marketing
  9. Social Media Marketing
- Added `link` property to each feature for proper navigation

#### B. Updated `services/route.ts` fallbackServices
- **Before:** Only had 3 services with old names
- **After:** Now includes all 9 services matching the homepage features
- Updated service slugs, icons, badges, and pricing to match current offerings

#### C. Updated `page.tsx` rendering logic
- Removed `.slice(0, 6)` limit on `setServicePages(featuredServices)`
- Removed `.slice(0, 9)` limit on `content.features.map()`
- Now displays all services returned from the API or fallback data

**Result:** Homepage now displays all 9 service cards whether the Wagtail CMS is available or using fallback data.

---

### 2. Client Portal Logging Out on Tab Navigation

**Root Cause:**
Multiple issues causing authentication to fail on navigation:
1. `LoginForm` was using legacy API service instead of `useAuth` hook
2. `AuthProvider` redirect effect was triggering on every pathname change
3. Token mismatch between what was stored and what was checked

**Files Modified:**
1. `/portals/client-portal/components/auth/LoginForm.tsx`
2. `/portals/client-portal/components/auth/AuthProvider.tsx`

**Changes Made:**

#### A. Updated LoginForm.tsx
- **Before:** Used `apiService.login()` which stored `auth_token`
- **After:** Now uses `useAuth().login()` which stores `access_token`, `refresh_token`, and `user_data`
- Removed dependency on `../../lib/api`
- Imported `useAuth` from `./AuthProvider`
- Updated error handling to match new login flow

#### B. Updated AuthProvider.tsx redirect logic
- **Before:** 
  - Redirect effect ran on every `pathname` change
  - Immediately redirected if `user` was null
  - No attempt to restore session from localStorage before redirecting
  
- **After:**
  - Removed `pathname` from useEffect dependencies to prevent redirect loops
  - Added session restoration attempt before redirecting
  - Checks `localStorage` for `access_token` and `user_data` before redirect
  - Attempts to parse and restore user state if tokens exist
  - Only redirects if truly no valid session exists
  - Added console logging for debugging

**Result:** 
- Users stay logged in when navigating between tabs
- Session persists across page navigation
- No more unexpected logouts when clicking sidebar links
- Proper token storage and validation

---

## Testing Recommendations

### Homepage Services
1. Navigate to the homepage (localhost:3000)
2. Verify all 9 service cards are displayed
3. Click on each service card to ensure links work
4. Check that each service has proper icon, title, and description

### Client Portal Authentication
1. Navigate to client portal (localhost:3002 or appropriate port)
2. Log in with credentials
3. Click through all sidebar tabs:
   - Dashboard
   - My Services
   - Campaigns
   - Analytics
   - Billing
   - Team
   - Support
   - Settings
4. Verify you remain logged in on each tab
5. Refresh the page and verify session persists
6. Only logout when clicking "Sign Out" button

---

## Files Changed Summary

1. ✅ `/brands/bizoholic/frontend/app/page.tsx` - Removed slice limits
2. ✅ `/brands/bizoholic/frontend/app/api/brain/wagtail/homepage/route.ts` - Added all 9 features
3. ✅ `/brands/bizoholic/frontend/app/api/brain/wagtail/services/route.ts` - Added all 9 services
4. ✅ `/portals/client-portal/components/auth/LoginForm.tsx` - Use useAuth hook
5. ✅ `/portals/client-portal/components/auth/AuthProvider.tsx` - Fixed redirect logic

---

## Previous Fixes (Earlier in Session)

### Service Page TypeScript Errors
Fixed missing `ctaSecondary` prop and added `"use client"` directive to all service pages:
- ✅ `/app/services/creative-design/page.tsx`
- ✅ `/app/services/ai-campaign-management/page.tsx`
- ✅ `/app/services/seo-optimization/page.tsx`
- ✅ `/app/services/marketing-automation/page.tsx`
- ✅ `/app/services/strategy-consulting/page.tsx`
- ✅ `/app/services/performance-analytics/page.tsx`
- ✅ `/app/services/content-generation/page.tsx`

### Import Syntax Error
Fixed `Pen Tool` to `PenTool` in lucide-react imports.
