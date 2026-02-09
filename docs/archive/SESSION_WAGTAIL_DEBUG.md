# Session Validation & Wagtail Content Fixes

**Date**: December 1, 2025  
**Status**: 🔄 In Progress - Testing Required

## 🎯 Issues Being Fixed

### 1. Dashboard Tabs Redirecting to Login (`/api/auth/me` returning 401)
**Problem**: After successful login, clicking any dashboard tab redirects back to login page.

**Root Cause Analysis**:
The logs show:
```
POST /api/auth/login 200 ✅ Login succeeds
GET /api/auth/me 401 ❌ Session validation fails immediately
```

This indicates the session cookie is either:
1. Not being set correctly during login
2. Not being read correctly by `/api/auth/me`
3. The token format is invalid for the backend

**Fixes Applied**:
1. **Fixed Login Response Structure** (`app/api/auth/login/route.ts`):
   - The backend returns `{ user: {...}, tenant: {...}, access_token: "..." }`
   - But the login route was trying to access `data.user_id` instead of `data.user.id`
   - Updated to correctly extract nested user data

2. **Added Detailed Logging** (`app/api/auth/me/route.ts`):
   - Added console logs to track token presence, backend calls, and responses
   - This will help diagnose the exact failure point

3. **Improved Cookie Deletion** (already done in logout route):
   - Using explicit `maxAge: 0` and `expires: new Date(0)` for reliability

**Next Steps**:
1. Login again with `admin123`
2. Check frontend logs: `tail -f /tmp/bizoholic-frontend.log`
3. Look for `[/api/auth/me]` log messages to see what's failing
4. The logs will show:
   - Whether the token cookie exists
   - What the backend response is
   - Any error messages

---

### 2. Wagtail Content Not Loading (Showing Fallback Content)
**Problem**: Homepage shows only 3 hardcoded service cards instead of dynamic content from Wagtail CMS.

**Root Cause**: The frontend is likely:
1. Not calling the Wagtail API correctly
2. The API call is failing (404/403 errors seen in earlier logs)
3. Falling back to hardcoded content when the API fails

**Investigation Needed**:
1. Check which component renders the homepage services
2. Verify the Wagtail API endpoint being called
3. Ensure Wagtail has the content pages created
4. Check if authentication is required for Wagtail API

**Wagtail API Status**:
Earlier test showed:
```bash
curl http://localhost:8002/api/v2/pages/
# Returns: 403 Forbidden - "Authentication credentials were not provided."
```

This means Wagtail API requires authentication. We need to either:
1. Configure Wagtail to allow public read access for published pages
2. Pass authentication credentials when fetching content

**Files to Check**:
- Homepage component: `brands/bizoholic/frontend/app/page.tsx` or similar
- Wagtail API calls: Look for `/api/brain/wagtail/` or `/api/wagtail/` calls
- Wagtail settings: `shared/services/cms/config/settings/base.py`

---

## 🔍 Debugging Steps

### For Session Validation Issue:

1. **Login and Check Logs**:
   ```bash
   # In one terminal, watch the logs
   tail -f /tmp/bizoholic-frontend.log
   
   # In browser, login at http://localhost:3001/portal/login
   # Then try to click a dashboard tab
   ```

2. **Look for These Log Messages**:
   ```
   [/api/auth/me] Token present: true/false
   [/api/auth/me] Token length: XXX
   [/api/auth/me] Calling backend: http://localhost:8007/auth/me
   [/api/auth/me] Backend response status: 401
   [/api/auth/me] Backend error: {...}
   ```

3. **Check Browser DevTools**:
   - Application → Cookies → `http://localhost:3001`
   - Look for `access_token` cookie
   - Check if it exists and has a value after login

4. **Test Backend Directly**:
   ```bash
   # Get the token from browser DevTools
   TOKEN="<paste_token_here>"
   
   # Test the backend endpoint
   curl -H "Authorization: Bearer $TOKEN" http://localhost:8007/auth/me
   ```

### For Wagtail Content Issue:

1. **Find Homepage Component**:
   ```bash
   cd brands/bizoholic/frontend
   find . -name "page.tsx" -o -name "home*.tsx" | grep -v node_modules
   ```

2. **Check Wagtail API Calls**:
   ```bash
   # Search for Wagtail API calls in the codebase
   grep -r "wagtail" brands/bizoholic/frontend/app --include="*.tsx" --include="*.ts"
   ```

3. **Test Wagtail API**:
   ```bash
   # Check if Wagtail is accessible
   curl http://localhost:8002/api/v2/pages/
   
   # Check specific page types
   curl http://localhost:8002/api/v2/pages/?type=home.HomePage
   curl http://localhost:8002/api/v2/pages/?type=services.ServicePage
   ```

4. **Check Wagtail Admin**:
   - Go to `http://localhost:8002/admin/`
   - Login (if you have credentials)
   - Check if pages are published and have content

---

## 📋 Expected Outcomes

### After Session Fix:
- ✅ Login redirects to dashboard
- ✅ Dashboard tabs load without redirecting to login
- ✅ `/api/auth/me` returns 200 with user data
- ✅ Session persists across page refreshes
- ✅ Logout clears session and requires re-login

### After Wagtail Fix:
- ✅ Homepage loads dynamic services from Wagtail
- ✅ Service cards show real content, not fallback data
- ✅ Other pages (About, Services, etc.) load Wagtail content
- ✅ CMS tab in dashboard allows content management
- ✅ CRUD operations work from the portal

---

## 🚀 Next Actions

1. **Test Login Flow**:
   - Login with `admin123`
   - Watch the logs for `[/api/auth/me]` messages
   - Report what you see

2. **Share Log Output**:
   - Copy the relevant log lines showing the `/api/auth/me` calls
   - This will tell us exactly why it's failing

3. **Identify Homepage Component**:
   - Let me know which file renders the homepage
   - I'll check how it's fetching Wagtail content

4. **Check Wagtail Content**:
   - Confirm if content exists in Wagtail admin
   - Share the structure of pages you've created

Once we have this information, I can provide targeted fixes for both issues!

---

## 📝 Files Modified So Far

### Session Validation:
- ✅ `brands/bizoholic/frontend/app/api/auth/login/route.ts` - Fixed response data extraction
- ✅ `brands/bizoholic/frontend/app/api/auth/me/route.ts` - Added logging and improved error handling

### Wagtail Content:
- ⏳ Pending investigation - need to identify the components and API calls

---

## 💡 Quick Wins

If the session issue is just a token format problem, the fix is simple. If it's a deeper issue (like the backend rejecting valid tokens), we might need to:
1. Check the JWT secret consistency between services
2. Verify the token expiration settings
3. Ensure the auth service is using the correct authentication backend

For Wagtail, if it's just an authentication issue, we can:
1. Configure Wagtail to allow public API access for published pages
2. Or pass the user's auth token to Wagtail API calls
3. Set up proper API permissions in Wagtail settings
