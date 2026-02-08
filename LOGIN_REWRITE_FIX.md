# Login 404 Fix - Rewrite Rule Removal

## Root Cause Identified
The persistent 404 error was caused by a **conflicting rewrite rule** in `next.config.js`.

### The Problem
The configuration contained this rule:
```javascript
{
  source: '/api/auth/:path*',
  destination: 'http://localhost:8001/api/auth/:path*',
}
```

This rule was **intercepting all NextAuth internal requests** (like `/api/auth/session`, `/api/auth/signin`) and forwarding them to the Brain Gateway. Since the Brain Gateway doesn't handle these specific NextAuth routes, it returned 404 errors, breaking the entire authentication system.

### The Fix
I have **removed this rewrite rule** from `next.config.js`.

Now:
1.  **NextAuth Requests** (session, signin, etc.) go correctly to `app/api/auth/[...nextauth]/route.ts`.
2.  **Authentication Logic** inside `route.ts` then manually calls the Auth Service (or Brain Gateway) as needed.
3.  **Brain Gateway Rewrites** (`/api/brain/*`) remain active for other features.

## Verification Steps

1.  **Wait for Startup**: The Client Portal is restarting. Give it a moment.
2.  **Access Login**: Go to `http://localhost:3003/login`. It should now load correctly.
3.  **Perform Login**: Enter credentials and sign in.
4.  **Check Dashboard**: You should be redirected to the dashboard.

## Current Status
*   ✅ **Client Portal**: Restarting on port 3003 with fixed config.
*   ✅ **Auth Service**: Running on port 8008.
*   ✅ **Configuration**: `next.config.js` corrected.
