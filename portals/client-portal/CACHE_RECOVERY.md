# BizOSaaS Client Portal - Cache Recovery Guide

## 🚨 Problem: Application Error in Standard Browser (Works in Incognito)

If you're seeing "Application error: a client-side exception has occurred" with React Error #185 in your standard browser window, but the site works perfectly in incognito mode, you have a **browser cache corruption issue**.

### Root Cause
Your browser has cached old JavaScript bundles (`4bd1b696-100b9d70ed4e49c1.js`, `3148-b8aabfc9e4caf9d5.js`) that contain infinite render loops. A Service Worker is intercepting requests and serving these corrupted files instead of fetching the new, fixed code from the server.

---

## ✅ Solution: Multi-Step Cache Recovery

### Option 1: Automated Cache Buster (RECOMMENDED)

1. **Navigate to the Cache Buster page:**
   ```
   https://app.bizoholic.net/cache-buster.html
   ```

2. **Wait for the automated recovery:**
   - The page will automatically clear all browser storage
   - You'll see progress for each step (Service Workers, Caches, LocalStorage, etc.)
   - When complete, click "Continue to Portal"

3. **Verify the fix:**
   - You should now see the onboarding page without errors
   - If you still see errors, proceed to Option 2

---

### Option 2: Manual Browser Cache Clear

If the automated tool doesn't work, manually clear your browser data:

#### Chrome/Edge:
1. Press `F12` to open DevTools
2. Go to **Application** tab
3. In the left sidebar, click **Storage**
4. Click **Clear site data** button
5. Ensure all checkboxes are selected:
   - ✅ Unregister service workers
   - ✅ Local and session storage
   - ✅ IndexedDB
   - ✅ Web SQL
   - ✅ Cookies
   - ✅ Cache storage
6. Click **Clear site data**
7. Close DevTools and refresh the page (`Ctrl+Shift+R` or `Cmd+Shift+R`)

#### Firefox:
1. Press `F12` to open DevTools
2. Go to **Storage** tab
3. Right-click on the domain in the left sidebar
4. Select **Delete All**
5. Close DevTools and refresh (`Ctrl+Shift+R` or `Cmd+Shift+R`)

#### Safari:
1. Open **Develop** menu (if not visible, enable in Preferences > Advanced)
2. Select **Empty Caches**
3. Then: **Develop** > **Clear Local Storage**
4. Refresh the page (`Cmd+Shift+R`)

---

### Option 3: Hard Refresh (Quick Try)

Sometimes a simple hard refresh works:

- **Windows/Linux:** `Ctrl + Shift + R` or `Ctrl + F5`
- **Mac:** `Cmd + Shift + R`

This forces the browser to bypass cache for the current page load.

---

### Option 4: Nuclear Option (If all else fails)

1. **Close ALL browser windows** (completely quit the browser)
2. **Reopen the browser**
3. **Go directly to:**
   ```
   https://app.bizoholic.net/cache-buster.html
   ```
4. **Follow the automated recovery**

---

## 🔍 Verification

After clearing the cache, you should see:
- ✅ No "Application error" message
- ✅ No React Error #185 in console
- ✅ The onboarding page loads correctly
- ✅ Different JavaScript bundle names (not `4bd1b696-*` or `3148-*`)

---

## 🛠️ For Developers

### Why This Happens
1. Next.js generates content-hashed JavaScript bundles (`[hash].js`)
2. Service Workers cache these bundles for offline support
3. When code changes, new bundles are generated with new hashes
4. If the Service Worker doesn't update properly, it serves old bundles
5. Old bundles may contain bugs (like infinite render loops) that crash the app

### Prevention
- Always test in incognito mode during development
- Use `Cache-Control: no-cache` headers for HTML files
- Implement proper Service Worker update strategies
- Version your Service Worker file itself
- Add cache-busting query parameters to critical assets

### Technical Details
The corrupted bundles contain an infinite loop in the render phase:
```
at Array.map (<anonymous>)
at o (3148-b8aabfc9e4caf9d5.js:1:23509)
```

This suggests a component is calling `setState` or triggering re-renders in a loop, likely in:
- `useEffect` without proper dependencies
- Context providers with unstable values
- Middleware causing redirect loops

---

## 📞 Support

If you continue to experience issues after following all steps above:

1. **Check the browser console** for any remaining errors
2. **Try a different browser** to confirm it's cache-related
3. **Contact support** with:
   - Browser name and version
   - Screenshot of console errors
   - Steps you've already tried

---

## 🎯 Quick Reference

| Symptom | Solution |
|---------|----------|
| Works in incognito, not in standard window | Cache corruption - use cache-buster.html |
| Error mentions `4bd1b696-*.js` | Old bundle cached - clear browser data |
| React Error #185 | Infinite render loop - clear cache and reload |
| 307 redirect loop | Middleware issue - check authentication state |

---

**Last Updated:** 2026-01-27  
**Version:** RECOVERY_002
