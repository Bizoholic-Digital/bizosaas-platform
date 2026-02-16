# Docker Image Naming Convention

**Repository**: `ghcr.io/bizoholic-digital/bizosaas-client-portal`

---

## Naming Convention

### Format
```
ghcr.io/bizoholic-digital/bizosaas-client-portal:<environment>-<version>
```

### Environments
- `staging` - Staging environment (stg.bizoholic.com)
- `prod` - Production environment (bizoholic.com)
- `dev` - Development/testing builds

### Version Format
- Semantic versioning: `v<major>.<minor>.<patch>`
- Example: `v2.1.4`

---

## Tag Examples

### Staging
```bash
# Specific version
ghcr.io/bizoholic-digital/bizosaas-client-portal:staging-v2.1.4

# Latest staging
ghcr.io/bizoholic-digital/bizosaas-client-portal:staging-latest
```

### Production
```bash
# Specific version
ghcr.io/bizoholic-digital/bizosaas-client-portal:prod-v2.1.4

# Latest production
ghcr.io/bizoholic-digital/bizosaas-client-portal:prod-latest
```

### Development
```bash
# Specific version
ghcr.io/bizoholic-digital/bizosaas-client-portal:dev-v2.1.4

# Latest development
ghcr.io/bizoholic-digital/bizosaas-client-portal:dev-latest
```

---

## Build Commands

### Staging Build
```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/client-portal

docker build \
  --no-cache \
  --build-arg NODE_ENV=production \
  --build-arg NEXT_PUBLIC_API_URL=https://api.bizoholic.com/api \
  --build-arg NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com/api \
  --build-arg NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/api/auth \
  --build-arg NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/portal \
  --build-arg BASE_PATH=/portal \
  -t ghcr.io/bizoholic-digital/bizosaas-client-portal:staging-v2.1.4 \
  -t ghcr.io/bizoholic-digital/bizosaas-client-portal:staging-latest \
  .
```

### Production Build
```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/client-portal

docker build \
  --no-cache \
  --build-arg NODE_ENV=production \
  --build-arg NEXT_PUBLIC_API_URL=https://api.bizoholic.com/api \
  --build-arg NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com/api \
  --build-arg NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/api/auth \
  --build-arg NEXT_PUBLIC_APP_URL=https://bizoholic.com/portal \
  --build-arg BASE_PATH=/portal \
  -t ghcr.io/bizoholic-digital/bizosaas-client-portal:prod-v2.1.4 \
  -t ghcr.io/bizoholic-digital/bizosaas-client-portal:prod-latest \
  .
```

### Development Build
```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/client-portal

docker build \
  --build-arg NODE_ENV=development \
  --build-arg NEXT_PUBLIC_API_URL=http://localhost:8001/api \
  --build-arg NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://localhost:8001/api \
  --build-arg NEXT_PUBLIC_AUTH_API_URL=http://localhost:8001/api/auth \
  --build-arg NEXT_PUBLIC_APP_URL=http://localhost:3001 \
  --build-arg BASE_PATH= \
  -t ghcr.io/bizoholic-digital/bizosaas-client-portal:dev-v2.1.4 \
  -t ghcr.io/bizoholic-digital/bizosaas-client-portal:dev-latest \
  .
```

---

## Push Commands

### Staging
```bash
docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:staging-v2.1.4
docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:staging-latest
```

### Production
```bash
docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:prod-v2.1.4
docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:prod-latest
```

### Development
```bash
docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:dev-v2.1.4
docker push ghcr.io/bizoholic-digital/bizosaas-client-portal:dev-latest
```

---

## Version History

| Version | Environment | Date | Changes |
|---------|-------------|------|---------|
| staging-v2.1.4 | Staging | 2025-11-12 | Fixed API URL embedding with Dockerfile ARG/ENV |
| staging-v2.1.3 | Staging | 2025-11-12 | Initial attempt with build args (used cache) |
| staging-v2.1.2 | Staging | 2025-11-12 | Added server-side auth, middleware protection |
| staging-v2.0.32 | Staging | 2025-11-11 | Previous stable version |

---

## Environment-Specific Configurations

### Staging
- **Domain**: `stg.bizoholic.com`
- **Portal URL**: `https://stg.bizoholic.com/portal`
- **API Base**: `https://api.bizoholic.com/api`
- **Base Path**: `/portal`

### Production (Future)
- **Domain**: `bizoholic.com`
- **Portal URL**: `https://bizoholic.com/portal`
- **API Base**: `https://api.bizoholic.com/api`
- **Base Path**: `/portal`

### Development
- **Domain**: `localhost`
- **Portal URL**: `http://localhost:3001`
- **API Base**: `http://localhost:8001/api`
- **Base Path**: ` ` (empty)

---

## Deployment Instructions

### Staging Deployment (Dokploy)
1. Update service image: `ghcr.io/bizoholic-digital/bizosaas-client-portal:staging-v2.1.4`
2. Environment variables should already be set correctly
3. Redeploy service
4. Verify at: https://stg.bizoholic.com/portal/

### Production Deployment (Future)
1. Test thoroughly in staging first
2. Update service image: `ghcr.io/bizoholic-digital/bizosaas-client-portal:prod-v2.1.4`
3. Update environment variables for production domain
4. Redeploy service
5. Verify at: https://bizoholic.com/portal/

---

## Notes

- Always use `--no-cache` for production builds to ensure fresh builds
- Always tag with both specific version and environment-latest
- Never skip semantic versioning
- Test in staging before deploying to production
- Document all changes in version history above
