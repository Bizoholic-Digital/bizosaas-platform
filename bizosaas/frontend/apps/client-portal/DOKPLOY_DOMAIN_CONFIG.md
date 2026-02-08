# Client Portal - Dokploy Domain Configuration

## Container Status: Ready to Deploy ✅

The Docker image `ghcr.io/bizoholic-digital/bizosaas-client-portal:v1.0.0-foundation-dashboard` is now available in GHCR and ready to deploy.

## Port Configuration ✅

You've correctly configured:
- **Published Port**: 3000 (external)
- **Target Port**: 3001 (container internal)
- **Protocol**: TCP
- **Mode**: INGRESS

## Domain Configuration (After Container is Running)

Once your container is up and running, configure the domain in the **Domains Tab**:

### Option 1: Path-Based Routing (Recommended)

For URL: `https://stg.bizoholic.com/portal/`

**Domain Settings:**
- **Domain**: `stg.bizoholic.com`
- **Path**: `/portal` (or leave path empty and use Traefik labels below)
- **Port**: 3001 (IMPORTANT: Use container's internal port, not published port)
- **HTTPS**: Enabled
- **Certificate**: Auto (Let's Encrypt)

**Traefik Labels (Add in Advanced Settings or Labels section):**
```yaml
traefik.enable=true
traefik.http.routers.client-portal.rule=Host(`stg.bizoholic.com`) && PathPrefix(`/portal`)
traefik.http.routers.client-portal.entrypoints=websecure
traefik.http.routers.client-portal.tls=true
traefik.http.routers.client-portal.tls.certresolver=letsencrypt
traefik.http.middlewares.portal-stripprefix.stripprefix.prefixes=/portal
traefik.http.routers.client-portal.middlewares=portal-stripprefix
traefik.http.services.client-portal.loadbalancer.server.port=3001
```

### Option 2: Subdomain Routing (Alternative)

For URL: `https://portal.bizoholic.com/`

**Domain Settings:**
- **Domain**: `portal.bizoholic.com`
- **Port**: 3001
- **HTTPS**: Enabled
- **Certificate**: Auto (Let's Encrypt)

**Traefik Labels:**
```yaml
traefik.enable=true
traefik.http.routers.client-portal.rule=Host(`portal.bizoholic.com`)
traefik.http.routers.client-portal.entrypoints=websecure
traefik.http.routers.client-portal.tls=true
traefik.http.routers.client-portal.tls.certresolver=letsencrypt
traefik.http.services.client-portal.loadbalancer.server.port=3001
```

## Important Environment Variables

Make sure these are set in the **Environment Tab**:

### Required for Path-Based Routing (`/portal/`)
```bash
BASE_PATH=/portal
NEXT_PUBLIC_BASE_PATH=/portal
NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/portal
```

### Required for Subdomain Routing
```bash
BASE_PATH=
NEXT_PUBLIC_BASE_PATH=
NEXT_PUBLIC_APP_URL=https://portal.bizoholic.com
```

### Common Required Variables
```bash
NODE_ENV=production
PORT=3001

# Authentication (generate with: openssl rand -base64 32)
JWT_SECRET=your-jwt-secret-here
NEXTAUTH_SECRET=your-nextauth-secret-here
NEXTAUTH_URL=https://stg.bizoholic.com/portal

# Database
DATABASE_URL=postgresql://user:password@host:5432/database

# Brain Gateway API
BRAIN_GATEWAY_API_URL=https://api.bizoholic.com
BRAIN_GATEWAY_API_KEY=your-api-key-here

# Optional: Multi-tenant
ENABLE_MULTI_TENANT=true
DEFAULT_TENANT=default
```

## Verification Steps

After deploying and configuring the domain:

1. **Check Container Logs**:
   ```bash
   docker logs <container-id>
   ```
   Should see: `Server started on port 3001`

2. **Test Internal Access**:
   ```bash
   curl http://localhost:3000/
   ```

3. **Test External Access**:
   ```bash
   curl https://stg.bizoholic.com/portal/
   ```

4. **Check Traefik Dashboard** (if enabled):
   - Verify router `client-portal` exists
   - Verify middleware `portal-stripprefix` is attached
   - Verify service points to port 3001

## Troubleshooting

### Issue: 404 Not Found
- **Cause**: Path stripping not working
- **Fix**: Verify `portal-stripprefix` middleware is attached to router
- **Check**: Environment variables `BASE_PATH` and `NEXT_PUBLIC_BASE_PATH` are set correctly

### Issue: Assets Not Loading (CSS/JS)
- **Cause**: Base path not configured
- **Fix**: Ensure `NEXT_PUBLIC_BASE_PATH=/portal` is set
- **Verify**: Check browser DevTools Network tab for asset URLs

### Issue: API Calls Failing
- **Cause**: CORS or base path issues
- **Fix**:
  - Verify `NEXT_PUBLIC_APP_URL` matches your domain
  - Check Brain Gateway API CORS settings allow `stg.bizoholic.com`

### Issue: Authentication Not Working
- **Cause**: NEXTAUTH_URL mismatch
- **Fix**: Set `NEXTAUTH_URL=https://stg.bizoholic.com/portal` (with `/portal` suffix)

## Next Steps After Deployment

1. ✅ Deploy container from Dokploy UI
2. ⏳ Wait for container to start (check logs)
3. ⏳ Configure domain using Option 1 or Option 2 above
4. ⏳ Test access at `https://stg.bizoholic.com/portal/`
5. ⏳ Verify login functionality
6. ⏳ Test Brain Gateway API integration
7. ⏳ Monitor logs for any errors

## Quick Deploy Checklist

- [x] Docker image built and pushed to GHCR
- [x] Port configuration set (3000 → 3001)
- [ ] Container deployed and running
- [ ] Environment variables configured
- [ ] Domain configured with Traefik labels
- [ ] HTTPS certificate issued
- [ ] Access verified at domain
- [ ] Login tested
- [ ] API integration verified

---

**Current Status**: Image ready in GHCR ✅ | Port config done ✅ | Ready to deploy container!

**Recommended**: Use **Option 1** (Path-Based Routing at `/portal/`) for consistency with existing services.
