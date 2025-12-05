# AI Agent System - Troubleshooting Guide

**Date:** December 4, 2024, 9:27 PM IST

---

## 🔍 Current Status

### ✅ Files Created
1. `/app/ai-agents/page.tsx` - Agent Library
2. `/app/ai-agents/[agentId]/page.tsx` - Agent Configuration
3. `/app/ai-agents/byok/page.tsx` - BYOK Management
4. `/components/sidebar.tsx` - Updated with AI Agents menu

### 🐛 Reported Issues
1. ❓ AI Agents menu not visible in sidebar
2. ⚠️ Possible errors in BYOK page

---

## 🔧 Troubleshooting Steps

### Issue 1: AI Agents Menu Not Showing

**Possible Causes:**
1. User is not logged in as admin/super_admin
2. AuthProvider not returning correct role
3. Sidebar component not re-rendering

**Solution:**

The sidebar code is correct and should show the menu for admin users:

```typescript
// Check if user is admin or super_admin
const isAdmin = user?.role === 'admin' || user?.role === 'super_admin'

const navigation = [
    // ... other items
    ...(isAdmin ? [{
        name: 'AI Agents',
        href: '/ai-agents',
        icon: Sparkles,
        badge: '93'
    }] : []),
    // ... other items
]
```

**To Verify:**
1. Check user role in browser console:
   ```javascript
   // In browser console
   localStorage.getItem('user')
   ```

2. Ensure user has role 'admin' or 'super_admin'

3. Try logging out and back in

4. Check if AuthProvider is working:
   ```typescript
   // Add console.log in sidebar
   console.log('User:', user)
   console.log('Is Admin:', isAdmin)
   ```

---

### Issue 2: BYOK Page Errors

**Status:** File appears correct, no syntax errors found

**Verification:**
- File starts with `'use client'` (correct)
- All imports are valid
- Component exports correctly
- TypeScript types are correct

---

## 🚀 Quick Test

### Test 1: Check if pages are accessible

```bash
# Start dev server
cd /home/alagiri/projects/bizosaas-platform/portals/client-portal
npm run dev

# Navigate to:
# http://localhost:3003/ai-agents
# http://localhost:3003/ai-agents/campaign_manager
# http://localhost:3003/ai-agents/byok
```

### Test 2: Verify user role

```javascript
// In browser console after login
const user = JSON.parse(localStorage.getItem('user') || '{}')
console.log('User role:', user.role)
console.log('Should see AI Agents menu:', user.role === 'admin' || user.role === 'super_admin')
```

### Test 3: Force admin role (for testing)

If you need to test as admin, you can temporarily modify the sidebar:

```typescript
// Temporarily set to true for testing
const isAdmin = true // user?.role === 'admin' || user?.role === 'super_admin'
```

---

## 📝 Common Issues & Solutions

### 1. Menu Not Showing
**Cause:** User role is not 'admin' or 'super_admin'  
**Solution:** Update user role in database or auth system

### 2. 404 on /ai-agents
**Cause:** Next.js hasn't picked up new routes  
**Solution:** Restart dev server

### 3. Import Errors
**Cause:** Missing dependencies  
**Solution:** 
```bash
npm install lucide-react
npm install @radix-ui/react-dialog
npm install @radix-ui/react-progress
```

### 4. Type Errors
**Cause:** Missing type definitions or strict type checking
**Solution:** 
- Ensure all files in `/lib/ai/` are present
- For `SERVICE_CATALOG` errors, ensure `ServiceConfig` interface uses `readonly string[]` to match `as const` definition:
  ```typescript
  interface ServiceConfig {
      // ...
      keyTypes: readonly string[];
      requiredKeys: readonly string[];
  }
  ```

---

## 🔍 Debug Checklist

- [ ] User is logged in
- [ ] User role is 'admin' or 'super_admin'
- [ ] Dev server is running
- [ ] No console errors in browser
- [ ] All dependencies installed
- [ ] All files in `/lib/ai/` exist
- [ ] Sidebar component is being used in layout
- [ ] AuthProvider is wrapping the app

---

## 📊 Expected Behavior

### When logged in as Admin:
1. Sidebar shows "AI Agents" menu item with "93" badge
2. Clicking opens `/ai-agents` page
3. Agent library shows all 93 agents
4. Can click any agent to configure
5. BYOK tab works and shows management page

### When logged in as Regular User:
1. "AI Agents" menu item is hidden
2. Direct navigation to `/ai-agents` should redirect or show access denied

---

## 🛠️ Manual Verification

### Step 1: Check File Structure
```bash
ls -la /home/alagiri/projects/bizosaas-platform/portals/client-portal/app/ai-agents/
# Should show:
# - page.tsx
# - [agentId]/
# - byok/
```

### Step 2: Check Lib Files
```bash
ls -la /home/alagiri/projects/bizosaas-platform/portals/client-portal/lib/ai/
# Should show:
# - types.ts
# - agent-registry.ts
# - byok-manager.ts
# - agent-orchestrator.ts
# - index.ts
# - README.md
```

### Step 3: Test Import
```bash
cd /home/alagiri/projects/bizosaas-platform/portals/client-portal
node -e "console.log(require('./lib/ai/index.ts'))"
```

---

## 🎯 Next Actions

1. **Check build output** for any errors
2. **Verify user role** in auth system
3. **Test navigation** to /ai-agents directly
4. **Check browser console** for errors
5. **Restart dev server** if needed

---

## 📞 Support

If issues persist:
1. Check browser console for errors
2. Check terminal for build errors
3. Verify all dependencies are installed
4. Ensure database has correct user roles
5. Try clearing browser cache and localStorage

---

**Last Updated:** December 4, 2024, 9:27 PM IST
