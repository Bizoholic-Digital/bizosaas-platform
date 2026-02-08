# 🚀 Deployment Checklist

## Pre-Deployment

- [x] Admin Dashboard build fixed
- [x] All API clients implemented
- [x] All routers registered in Brain Gateway
- [x] Frontend components updated
- [x] Forms integrated with API clients
- [x] Error handling implemented
- [ ] Environment variables documented
- [ ] Test credentials prepared

## Environment Variables

### Client Portal
```bash
BRAIN_GATEWAY_URL=http://brain-gateway:8000
# Production:
# BRAIN_GATEWAY_URL=https://api.bizoholic.net
```

### Brain Gateway
```bash
# Already configured in docker-compose
```

## Deployment Steps

### 1. Rebuild Services
```bash
cd /home/alagiri/projects/bizosaas-platform

# Option A: Docker Compose
docker-compose up -d --build brain-gateway client-portal admin-dashboard

# Option B: Individual services
docker-compose up -d --build brain-gateway
docker-compose up -d --build client-portal
docker-compose up -d --build admin-dashboard
```

### 2. Verify Health
```bash
# Brain Gateway
curl http://localhost:8000/health
curl http://localhost:8000/metrics

# Client Portal
curl http://localhost:3000/api/health

# Admin Dashboard
curl http://localhost:3001/api/health
```

### 3. Test Connector Flow
1. Open Client Portal: http://localhost:3000
2. Navigate to **Connectors** tab
3. Click "Connect" on WordPress
4. Enter test credentials
5. Verify connection status

### 4. Test CRUD Operations
1. **CMS**: Create a test page
2. **CRM**: Create a test contact
3. **E-commerce**: View products (if WooCommerce connected)

## Post-Deployment Verification

- [ ] All services healthy
- [ ] Connectors page loads
- [ ] Can connect to WordPress
- [ ] Can create/edit/delete pages
- [ ] Can create/edit/delete contacts
- [ ] Can view products and orders
- [ ] No console errors
- [ ] No 404s in network tab

## Rollback Plan

If issues occur:
```bash
# Revert to previous version
git checkout <previous-commit>
docker-compose up -d --build
```

## Monitoring

Watch logs during deployment:
```bash
# Brain Gateway
docker logs -f brain-gateway

# Client Portal
docker logs -f client-portal

# Admin Dashboard
docker logs -f bizosaas-admin-dashboard
```

## Known Issues to Watch

1. **CORS errors**: Check Brain Gateway CORS settings
2. **404 on /api/brain/***: Verify proxy routes exist
3. **"No connector configured"**: Normal until user connects
4. **Timeout errors**: Check network connectivity to external APIs

## Success Criteria

✅ All services start without errors  
✅ Health endpoints return 200  
✅ Can access Client Portal UI  
✅ Can connect at least one connector  
✅ Can perform CRUD operations  
✅ No JavaScript errors in console  

---

**Ready to Deploy**: YES ✅  
**Estimated Downtime**: < 2 minutes  
**Rollback Time**: < 1 minute
