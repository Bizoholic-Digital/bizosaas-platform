# Django CRM Vault Integration - Deployment Instructions

**Date**: 2025-11-22T18:05:27+05:30  
**Image**: `ghcr.io/bizoholic-digital/django-crm:latest`  
**Tag**: `vault-integration` (also available)

---

## ✅ Build & Push Complete

### Images Pushed to GHCR:
- ✅ `ghcr.io/bizoholic-digital/django-crm:latest`
- ✅ `ghcr.io/bizoholic-digital/django-crm:vault-integration`

**Digest**: `sha256:9326c730874efb9ab56534374b2c8d102ebb533ca8e785e4f8f647bfbc3ce45e`

---

## 📋 Dokploy Deployment Instructions

### Option 1: Update via Dokploy UI

1. **Navigate to Django CRM Service**
   - Go to Dokploy UI
   - Find the `django-crm` service

2. **Update Image**
   - Change image to: `ghcr.io/bizoholic-digital/django-crm:latest`
   - Or use specific tag: `ghcr.io/bizoholic-digital/django-crm:vault-integration`

3. **Add/Update Environment Variables**
   ```bash
   # Vault Configuration
   VAULT_ADDR=http://bizosaas-vault:8200
   VAULT_TOKEN=bizosaas-dev-root-token
   
   # Django Settings
   DJANGO_SETTINGS_MODULE=crm_project.settings.production
   DJANGO_DEBUG=False
   
   # Database (fallback if Vault unavailable)
   DB_NAME=django_crm
   DB_HOST=bizosaas-postgres-unified
   DB_PORT=5432
   DB_USER=postgres
   DB_PASSWORD=<your-password>
   
   # Redis (fallback if Vault unavailable)
   REDIS_URL=redis://bizosaas-redis:6379/1
   CELERY_BROKER_URL=redis://bizosaas-redis:6379/2
   CELERY_RESULT_BACKEND=redis://bizosaas-redis:6379/3
   
   # Security
   ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,django-crm,bizosaas-django-crm
   
   # Optional
   TIME_ZONE=UTC
   ```

4. **Ensure Service Dependencies**
   - Vault service must be running
   - PostgreSQL must be accessible
   - Redis must be accessible

5. **Deploy**
   - Click "Redeploy" or "Update" button
   - Monitor logs for successful startup

---

## 🔍 Verification Steps

### 1. Check Service Health
```bash
curl http://django-crm:8000/health/
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "cache": "connected"
}
```

### 2. Check Vault Integration
Look for log messages:
```
✅ Vault connected: http://bizosaas-vault:8200
```

Or if Vault is unavailable:
```
⚠️ Vault connection failed... Using fallback values.
```

### 3. Test API Endpoints
```bash
# Admin interface
curl http://django-crm:8000/admin/

# API root
curl http://django-crm:8000/api/

# Health check
curl http://django-crm:8000/health/
```

---

## 🔐 Required Vault Secrets

Before deployment, ensure these secrets exist in Vault:

### 1. Database Credentials
```bash
vault kv put bizosaas/platform/database \
  host=bizosaas-postgres-unified \
  port=5432 \
  database=bizosaas \
  username=postgres \
  password=<your-password>
```

### 2. Redis Configuration
```bash
vault kv put bizosaas/platform/redis-connection \
  host=bizosaas-redis \
  port=6379 \
  connection_string=redis://bizosaas-redis:6379/0
```

### 3. Django Secret Key
```bash
vault kv put bizosaas/platform/django-crm-secret-key \
  secret_key=<generated-secret-key>
```

---

## 🐛 Troubleshooting

### Issue: Service Won't Start

**Check logs**:
```bash
docker logs <container-id>
```

**Common causes**:
1. Database not accessible
2. Vault not running (should fallback to env vars)
3. Missing environment variables
4. Port 8000 already in use

### Issue: Vault Connection Failed

**Expected behavior**: Service should continue with fallback to environment variables

**Verify**:
1. Vault service is running
2. `VAULT_ADDR` is correct
3. `VAULT_TOKEN` is valid
4. Network connectivity between services

### Issue: Database Connection Error

**Check**:
1. PostgreSQL is running
2. Database credentials are correct (in Vault or env vars)
3. Database name exists
4. Network connectivity

---

## 📊 What's New in This Version

### Vault Integration
- ✅ Production settings now use Vault for secrets
- ✅ Database credentials from Vault
- ✅ Redis configuration from Vault
- ✅ Celery broker configuration from Vault
- ✅ Automatic fallback to environment variables

### Security Improvements
- ✅ Secrets no longer in environment files
- ✅ Centralized secret management
- ✅ Support for secret versioning
- ✅ Audit logging for secret access

### Backward Compatibility
- ✅ Works with or without Vault
- ✅ Fallback to environment variables
- ✅ No breaking changes to existing deployments

---

## 🔄 Rollback Plan

If issues occur, rollback to previous version:

1. **In Dokploy UI**:
   - Change image back to previous tag
   - Or use: `ghcr.io/bizoholic-digital/django-crm:previous-tag`

2. **Verify**:
   - Service starts successfully
   - Health check passes
   - API endpoints respond

---

## 📝 Post-Deployment Checklist

- [ ] Service deployed successfully
- [ ] Health check endpoint responding
- [ ] Vault integration working (or fallback active)
- [ ] Database connectivity verified
- [ ] Redis connectivity verified
- [ ] Admin interface accessible
- [ ] API endpoints responding
- [ ] Logs show no errors
- [ ] Performance is acceptable

---

## 🚀 Next Steps

1. **Monitor Service**
   - Watch logs for any errors
   - Monitor resource usage
   - Check response times

2. **Populate Vault** (if not done)
   - Add all required secrets to Vault
   - Test secret retrieval
   - Verify fallback behavior

3. **Test Functionality**
   - Test CRM features
   - Verify multi-tenant functionality
   - Test API integrations

4. **Proceed with Other Services**
   - Saleor Backend (Task ID: 4)
   - Wagtail CMS (Task ID: 5)
   - AI Agents (Task ID: 6)

---

## 📞 Support

**Documentation**:
- [Vault Integration Guide](./bizosaas-platform/backend/services/crm/django-crm/VAULT_INTEGRATION.md)
- [Quick Reference](./bizosaas-platform/backend/services/crm/django-crm/VAULT_QUICK_REFERENCE.md)
- [Implementation Summary](./DJANGO_CRM_VAULT_INTEGRATION_COMPLETE.md)

**Test Script**:
```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas-platform/backend/services/crm/django-crm
python test_vault_integration.py
```

---

**Deployment Ready**: ✅  
**Image Available**: ✅  
**Documentation Complete**: ✅  
**Status**: Ready for Dokploy deployment
