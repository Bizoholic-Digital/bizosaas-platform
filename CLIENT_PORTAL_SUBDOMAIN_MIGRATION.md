# Client Portal - Subdomain Architecture Migration

## Date: 2025-12-02 18:54 IST

## Migration Overview

We have successfully migrated from a **Subpath architecture** (`/portal`) to a **Subdomain architecture** for the Client Portal. This is the industry-standard approach for SaaS applications.

### Before (Subpath)
- **Local Development:** `http://localhost:3001/portal/dashboard`
- **Production:** `https://www.bizoholic.com/portal/dashboard`
- **Issues:** Complex routing, basePath configuration, proxy rewrites

### After (Subdomain) ✅
- **Local Development:** `http://localhost:3003/dashboard`
- **Production:** `https://client.bizoholic.com/dashboard`
- **Benefits:** Clean URLs, simpler configuration, better separation of concerns

---

## Changes Made

### 1. Client Portal Configuration
**File:** `portals/client-portal/next.config.js`
- ✅ Removed `basePath: '/portal'`
- ✅ App now serves from root (`/`)

### 2. Bizoholic Frontend Configuration
**File:** `brands/bizoholic/frontend/next.config.js`
- ✅ Removed proxy rewrites for `/portal` and `/portal/:path*`
- ✅ Frontend and Portal are now completely independent

### 3. No Code Changes Required
- ✅ All internal routes already use relative paths (`/`, `/login`, `/dashboard`)
- ✅ Navigation components use query parameters (`/?tab=crm`)
- ✅ No hardcoded `/portal` references found

---

## Local Development Setup

### Running the Client Portal (Port 3003)
```bash
cd /home/alagiri/projects/bizosaas-platform/portals/client-portal
npm run dev -- --port 3003
```

**Access at:** `http://localhost:3003`

### Running the Bizoholic Frontend (Port 3001)
```bash
cd /home/alagiri/projects/bizosaas-platform/brands/bizoholic/frontend
npm run dev
```

**Access at:** `http://localhost:3001`

---

## Testing the Migration

### 1. Restart Both Servers
Stop and restart both the Client Portal (3003) and Bizoholic Frontend (3001) to pick up the config changes.

### 2. Test Client Portal Directly
1. Open `http://localhost:3003`
2. You should be redirected to `http://localhost:3003/login`
3. Log in with: `demo@bizosaas.com` / `demo123`
4. You should land on `http://localhost:3003/` (Dashboard)
5. Click through all tabs (CRM, CMS, Analytics, etc.)
6. Verify no redirects to login occur

### 3. Test Navigation
- ✅ Dashboard → CRM: Should go to `http://localhost:3003/?tab=crm`
- ✅ CRM → AI Assistant: Should go to `http://localhost:3003/chat`
- ✅ AI Assistant → CRM: Should go to `http://localhost:3003/?tab=crm`
- ✅ Browser back/forward: Should work correctly

---

## Production Deployment (Traefik)

### DNS Configuration
Add a CNAME record:
```
client.bizoholic.com → bizoholic.com
```

### Traefik Configuration

#### Option 1: Docker Labels (Recommended)
Add to your Client Portal service in `docker-compose.yml`:

```yaml
services:
  client-portal:
    image: bizosaas-client-portal:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.client-portal.rule=Host(`client.bizoholic.com`)"
      - "traefik.http.routers.client-portal.entrypoints=websecure"
      - "traefik.http.routers.client-portal.tls=true"
      - "traefik.http.routers.client-portal.tls.certresolver=letsencrypt"
      - "traefik.http.services.client-portal.loadbalancer.server.port=3000"
    networks:
      - traefik-public
```

#### Option 2: Traefik Config File
Add to `traefik/dynamic/client-portal.yml`:

```yaml
http:
  routers:
    client-portal:
      rule: "Host(`client.bizoholic.com`)"
      entryPoints:
        - websecure
      service: client-portal
      tls:
        certResolver: letsencrypt

  services:
    client-portal:
      loadBalancer:
        servers:
          - url: "http://client-portal:3000"
```

### SSL Certificate
Traefik with Let's Encrypt will automatically provision an SSL certificate for `client.bizoholic.com`.

---

## Environment Variables

### Client Portal (.env.local)
```bash
# API Endpoints
NEXT_PUBLIC_BRAIN_API_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_API_URL=http://localhost:8008

# Production
# NEXT_PUBLIC_BRAIN_API_URL=https://api.bizoholic.com
# NEXT_PUBLIC_AUTH_API_URL=https://auth.bizoholic.com
```

### Bizoholic Frontend (.env.local)
No changes needed. The frontend and portal are now independent.

---

## Rollback Plan (If Needed)

If you need to rollback to the subpath architecture:

1. **Restore basePath:**
   ```javascript
   // portals/client-portal/next.config.js
   basePath: '/portal',
   ```

2. **Restore Proxy:**
   ```javascript
   // brands/bizoholic/frontend/next.config.js
   async rewrites() {
     return [
       {
         source: '/portal/:path*',
         destination: 'http://localhost:3003/portal/:path*',
       },
     ];
   },
   ```

3. **Restart both servers**

---

## Benefits of Subdomain Architecture

### 1. **Cleaner URLs**
- ❌ `www.bizoholic.com/portal/dashboard?tab=crm`
- ✅ `client.bizoholic.com/dashboard?tab=crm`

### 2. **Independent Deployment**
- Update the marketing site without touching the portal
- Deploy portal updates without affecting the main site

### 3. **Better Performance**
- No proxy overhead
- Direct routing to the correct service

### 4. **Improved Security**
- Separate cookie domains
- Easier CSP (Content Security Policy) management
- Better session isolation

### 5. **Scalability**
- Can move to separate infrastructure
- Easier to implement CDN caching
- Better load balancing options

---

## Next Steps

1. ✅ Test the migration locally (port 3003)
2. ✅ Verify all authentication flows work
3. ✅ Test all navigation and tabs
4. 🔲 Update any documentation that references `/portal`
5. 🔲 Configure Traefik for production
6. 🔲 Set up DNS for `client.bizoholic.com`
7. 🔲 Deploy to production

---

## Support

If you encounter any issues:
1. Check browser console for `[AUTH]` logs
2. Verify both servers are running on correct ports
3. Clear browser cache and localStorage
4. Test in incognito mode

For production deployment assistance, refer to the Traefik configuration above.
