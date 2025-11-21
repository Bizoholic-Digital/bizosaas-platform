# Saleor Dashboard Login Fix - API_URL Configuration

**Date:** November 3, 2025
**Issue:** "Login went wrong. Please try again."
**Root Cause:** Wrong API_URL configuration

---

## Problem Analysis

### Current Configuration (WRONG)
```
API_URL=http://10.0.1.47:8000/graphql/
```

### Why This Doesn't Work

1. **Client-Side Application:** Saleor Dashboard is a React SPA that runs in the user's browser
2. **Internal IP:** `10.0.1.47` is an internal Docker network IP on KVM4
3. **Not Publicly Accessible:** This IP is only reachable from within KVM4's Docker network
4. **Browser Cannot Connect:** User's browser cannot reach internal Docker IPs

### Architecture Flow (Current - BROKEN)
```
User Browser
    ↓ Loads Dashboard from HTTPS
https://stg.coreldove.com/dashboard/
    ↓ Dashboard tries to call API from browser
http://10.0.1.47:8000/graphql/  ← FAILS (unreachable)
    ✗ Connection timeout or refused
```

---

## Solution: Use Public API URL

### Required Configuration
The Saleor API must be exposed via a public domain through Traefik.

### Option 1: API Subdomain (RECOMMENDED)
```
API_URL=https://api.coreldove.com/graphql/
```

**Setup Required:**
1. Configure Traefik routing for Saleor API
2. Add domain to Saleor Core `ALLOWED_CLIENT_HOSTS`
3. Update Dashboard environment variable

### Option 2: Path-Based Routing
```
API_URL=https://stg.coreldove.com/api/graphql/
```

**Setup Required:**
1. Add Traefik route with `/api` prefix
2. Configure path stripping middleware
3. Update Dashboard environment variable

### Option 3: Direct IP + Port (NOT RECOMMENDED - Security Risk)
```
API_URL=http://72.60.219.244:8000/graphql/
```

**Issues:**
- Exposes port 8000 publicly
- No SSL encryption
- Security vulnerability
- Not recommended for production

---

## Implementation Steps

### Step 1: Verify Current Saleor API Traefik Configuration

Check if Saleor API already has Traefik routing:

```bash
ssh root@72.60.219.244
docker inspect backend-saleor-api.1.2b4cetxidpwq0i5l3nbgmi10p | grep -i traefik
```

### Step 2: Configure Traefik Routing for Saleor API

**Via Dokploy UI:**

1. Navigate to Saleor API service in Dokploy
2. Go to **Routing** tab
3. Add domain configuration:
   ```yaml
   Host: api.coreldove.com
   Path: /
   Container Port: 8000
   HTTPS: Enabled
   Certificate Resolver: letsencrypt
   ```

**OR via Docker labels (if managing manually):**

```yaml
traefik.enable=true
traefik.http.routers.saleor-api.rule=Host(`api.coreldove.com`)
traefik.http.routers.saleor-api.entrypoints=websecure
traefik.http.routers.saleor-api.tls=true
traefik.http.routers.saleor-api.tls.certresolver=letsencrypt
traefik.http.services.saleor-api.loadbalancer.server.port=8000
```

### Step 3: Update DNS

Add DNS A record pointing to KVM4:
```
api.coreldove.com → 72.60.219.244
```

### Step 4: Update Saleor Core CORS Configuration

Add the dashboard domain to Saleor Core's allowed hosts:

```bash
ssh root@72.60.219.244

# Update Saleor Core environment variables via Dokploy:
# Add to Saleor API service environment:
ALLOWED_CLIENT_HOSTS=stg.coreldove.com,api.coreldove.com

# Restart Saleor API service
docker service update --force backend-saleor-api
```

### Step 5: Update Saleor Dashboard API_URL

**Via Dokploy UI:**

1. Navigate to `frontend-services` → `saleor-dashboard`
2. Go to **Environment** tab
3. Update API_URL:
   ```
   API_URL=https://api.coreldove.com/graphql/
   ```
4. Click **Save** and **Restart** service

**Verify via SSH:**
```bash
docker inspect frontendservices-saleordashboard-84ku62 | grep API_URL
```

### Step 6: Test API Accessibility

```bash
# From local machine
curl -I https://api.coreldove.com/graphql/

# Expected: HTTP/2 200
```

### Step 7: Create Saleor Superuser

Once API is accessible, create the admin account:

```bash
ssh root@72.60.219.244

# Create superuser
docker exec -it backend-saleor-api.1.2b4cetxidpwq0i5l3nbgmi10p \
  python manage.py createsuperuser \
  --email admin@coreldove.com \
  --no-input

# Set password
docker exec -it backend-saleor-api.1.2b4cetxidpwq0i5l3nbgmi10p \
  python manage.py shell -c "from saleor.account.models import User; u=User.objects.get(email='admin@coreldove.com'); u.set_password('CoreLdove2025!Admin'); u.save(); print('Password set successfully')"
```

### Step 8: Test Dashboard Login

1. Clear browser cache
2. Navigate to: https://stg.coreldove.com/dashboard/
3. Login with:
   - Email: `admin@coreldove.com`
   - Password: `CoreLdove2025!Admin`
4. Check browser console for errors

---

## Verification Checklist

- [ ] Traefik routing configured for Saleor API
- [ ] DNS record for `api.coreldove.com` pointing to KVM4
- [ ] SSL certificate issued by Let's Encrypt
- [ ] Saleor API accessible via `https://api.coreldove.com/graphql/`
- [ ] CORS configured: `ALLOWED_CLIENT_HOSTS` updated
- [ ] Dashboard environment variable updated: `API_URL=https://api.coreldove.com/graphql/`
- [ ] Dashboard service restarted
- [ ] Superuser created successfully
- [ ] Dashboard login works without errors
- [ ] No CORS errors in browser console
- [ ] GraphQL queries return data

---

## Troubleshooting

### Issue: API Still Not Accessible

**Check Traefik logs:**
```bash
docker logs traefik 2>&1 | grep api.coreldove
```

**Verify Traefik routes:**
```bash
docker exec traefik wget -qO- http://localhost:8080/api/http/routers | jq '.[] | select(.rule | contains("api.coreldove"))'
```

### Issue: CORS Errors in Browser

**Symptoms:** Browser console shows `Access-Control-Allow-Origin` errors

**Fix:**
```bash
# Ensure dashboard domain is in ALLOWED_CLIENT_HOSTS
docker exec backend-saleor-api.1.2b4cetxidpwq0i5l3nbgmi10p \
  env | grep ALLOWED_CLIENT_HOSTS
```

### Issue: Login Still Fails After Fix

**Check dashboard logs:**
```bash
docker logs frontendservices-saleordashboard-84ku62
```

**Check API logs:**
```bash
docker logs backend-saleor-api.1.2b4cetxidpwq0i5l3nbgmi10p 2>&1 | tail -50
```

**Test API directly from browser:**
```
Open: https://api.coreldove.com/graphql/
Should show GraphQL Playground or "Method Not Allowed" (normal for POST-only endpoints)
```

---

## Alternative: Quick Test Without DNS

If you don't want to wait for DNS propagation, you can test locally:

1. Add to your `/etc/hosts` (Linux/Mac) or `C:\Windows\System32\drivers\etc\hosts` (Windows):
   ```
   72.60.219.244 api.coreldove.com
   ```

2. Test: `curl -I https://api.coreldove.com/graphql/`

3. Try dashboard login

4. Remove hosts entry when DNS is ready

---

## Updated Credentials

After fixing the API_URL, update [credentials.md](file:///home/alagiri/projects/bizoholic/credentials.md:267):

```markdown
## Saleor Dashboard Access (CoreLdove E-Commerce)

**Dashboard URL:** https://stg.coreldove.com/dashboard/
**API URL:** https://api.coreldove.com/graphql/ ← UPDATED

**Status:** ✅ DEPLOYED (November 3, 2025)
- Container: `frontendservices-saleordashboard-84ku62`
- Image: `ghcr.io/saleor/saleor-dashboard:latest`
- API Connection: `https://api.coreldove.com/graphql/` ← UPDATED (publicly accessible)

**Admin Credentials:**
- Email: admin@coreldove.com
- Password: CoreLdove2025!Admin
```

---

## Summary

**Problem:** Internal Docker IP not accessible from browser
**Solution:** Expose Saleor API via public domain with Traefik
**Action Required:** Configure `api.coreldove.com` → Saleor API (port 8000)
**After Fix:** Update Dashboard `API_URL` environment variable

**Estimated Time:** 15-30 minutes (excluding DNS propagation)
