# Fix Summary: URLs and Dynamic Integration

## 1. "Start Free Trial" URL Fix
**Issue**: The "Start Free Trial" button on the homepage was pointing to `localhost:3001/auth/login`.
**Fix**:
1.  **Updated API Fallback**: Modified `app/api/brain/wagtail/homepage/route.ts` to default to `http://localhost:3003/register`.
2.  **Forced Frontend Override**: Updated `app/page.tsx` to explicitly set `hero_cta_url` to `http://localhost:3003/register`, ensuring the correct link is used even if the CMS returns an outdated URL.

## 2. Dynamic Integration (Wagtail)
**Status**: Integrated.
-   **Homepage Content**: The homepage fetches content from `/api/brain/wagtail/homepage`.
-   **Services Menu**: The header menu fetches services from `/api/brain/wagtail/services` (via `useNavigation` hook).
-   **Blog Posts**: The blog section fetches posts from `/api/brain/wagtail/blog`.

## 3. Header CTAs
**Status**: Hardcoded to Client Portal.
-   **Sign In**: `http://localhost:3003/login`
-   **Get Started**: `http://localhost:3003/register`
-   **Dashboard**: `http://localhost:3003/dashboard`

These links are infrastructure-level and correctly point to the Client Portal.

## ✅ Verification
1.  Refresh `http://localhost:3001`.
2.  Click "Start Free Trial" in the Hero section -> Should go to `http://localhost:3003/register`.
3.  Click "Get Started" in the Header -> Should go to `http://localhost:3003/register`.
