# Client Portal Integration with Bizoholic Frontend

## Date: 2025-12-02 17:42 IST

## Configuration Update
To support accessing the client portal via `http://localhost:3001/portal/dashboard`, we made the following changes:

### 1. Bizoholic Frontend (Port 3001)
Updated `next.config.js` to proxy requests:
```javascript
{
  source: '/portal/:path*',
  destination: 'http://localhost:3003/portal/:path*',
},
{
  source: '/portal',
  destination: 'http://localhost:3003/portal',
}
```

### 2. Client Portal (Port 3003)
Updated `next.config.js` to set base path:
```javascript
basePath: '/portal',
```

### 3. AuthProvider
Updated to use `router.push('/login')` which now automatically resolves to `/portal/login` thanks to the `basePath` configuration.

## Required Actions

### 1. Restart Bizoholic Frontend (Port 3001)
You must restart this service for the rewrite rules to take effect.
```bash
# In the terminal running Bizoholic frontend
# Ctrl+C to stop
npm run dev
```

### 2. Restart Client Portal (Port 3003)
You must restart this service for the basePath to take effect.
```bash
# In the terminal running Client Portal
# Ctrl+C to stop
npm run dev -- --port 3003
```

## Testing Instructions

1. **Open Incognito Window**
2. **Navigate to:** `http://localhost:3001/portal/dashboard`
3. **You should be redirected to:** `http://localhost:3001/portal/login`
4. **Log in**
5. **You should be redirected to:** `http://localhost:3001/portal/dashboard`
6. **Click tabs:**
   - URL should be `http://localhost:3001/portal/?tab=crm`
   - You should stay logged in

## Why This Works
- **Single Origin:** Everything is accessed via `localhost:3001`.
- **Proxying:** Bizoholic frontend forwards `/portal` requests to the client portal.
- **BasePath:** Client portal knows it lives under `/portal` and generates links accordingly.
- **Auth:** Cookies/LocalStorage are set on `localhost:3001`, so they are shared correctly.

**Please restart both servers and test!**
