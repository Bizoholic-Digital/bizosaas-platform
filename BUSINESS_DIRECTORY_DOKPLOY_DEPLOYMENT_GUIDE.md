# Business Directory - Dokploy Deployment Guide
## DDD-Compliant Microservice Deployment to stg.bizoholic.com/directory/

**Date:** 2025-11-02  
**Status:** ✅ Ready for Deployment  
**Architecture:** DDD Microservices with Workspace Packages

---

## 🎯 DEPLOYMENT STRATEGY

### Build Approach: Repository Root Context

The Business Directory uses workspace packages from `/packages/*`, so the Docker build must run from the **repository root**, not the subdirectory.

**Critical Configuration:**
- **Build Context:** `/` (repository root)
- **Dockerfile Path:** `bizosaas/frontend/apps/business-directory/Dockerfile.production`
- **No GitHub Token Required:** Workspace packages resolve locally

---

## 📋 DOKPLOY UI CONFIGURATION

### Complete Settings

```
Application Name:        frontend-business-directory
Repository:             https://github.com/Bizoholic-Digital/bizosaas-platform
Branch:                 main
Build Context:          /
Dockerfile Path:        bizosaas/frontend/apps/business-directory/Dockerfile.production
```

### Environment Variables

```bash
NEXT_PUBLIC_API_BASE_URL=http://bizosaas-saleor-api-8003:8000
NODE_ENV=production
PORT=3004
HOSTNAME=0.0.0.0
NEXT_TELEMETRY_DISABLED=1
NEXT_PUBLIC_STAGING_URL=https://stg.bizoholic.com/directory
NEXT_PUBLIC_PRODUCTION_URL=https://www.bizoholic.net
```

### Network & Routing

```
Docker Network:         dokploy-network
Port:                   3004
Domain:                 stg.bizoholic.com
Path Prefix:            /directory
Strip Prefix:           ✅ YES
HTTPS:                  ✅ YES
```

---

## ✅ READY FOR DEPLOYMENT

All Phase 0 tasks complete:
- ✅ Component refactoring (workspace packages)
- ✅ Dockerfile optimization (.dockerignore)
- ✅ Git commit & push (8175db9)
- ✅ Architecture alignment (DDD compliant)

**Next Action:** Deploy via Dokploy UI using configuration above

---

**ESTIMATED TIME:** 15-20 minutes  
**SUCCESS RATE:** High (proven Client Portal pattern)
