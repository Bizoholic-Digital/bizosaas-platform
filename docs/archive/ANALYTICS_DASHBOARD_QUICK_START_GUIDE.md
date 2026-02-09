# Analytics Dashboard - Quick Start Implementation Guide

**Date:** November 4, 2025
**Status:** 🚀 READY TO IMPLEMENT
**Estimated Time:** 10-13 hours total

---

## ✅ PHASE 1 COMPLETE: Setup (30 minutes)

### What's Done:
1. ✅ Copied analytics-dashboard from backup to working location
2. ✅ Created modular DDD `lib/` directory structure:
   - `lib/api/` - API clients
   - `lib/hooks/` - React hooks
   - `lib/ui/components/` - React components
   - `lib/ui/charts/` - Chart components
   - `lib/types/` - TypeScript types
   - `lib/utils/` - Utility functions
3. ✅ Updated package.json (port 3009 → 3007)
4. ✅ Added dependencies: @superset-ui/embedded-sdk, next-auth

### Location:
```
/home/alagiri/projects/bizoholic/bizosaas-platform/frontend/apps/analytics-dashboard/
```

---

## 🚀 NEXT STEPS: Implementation Phases

### Phase 2: Core Library Files (2-3 hours)

Run these commands to install dependencies and create core files:

```bash
cd /home/alagiri/projects/bizoholic/bizosaas-platform/frontend/apps/analytics-dashboard

# Install dependencies
npm install

# The following files need to be created (see details below):
```

#### Create: `lib/api/superset-api.ts`
```typescript
// See ANALYTICS_DASHBOARD_IMPLEMENTATION_PLAN.md lines 209-288
```

#### Create: `lib/ui/components/SupersetEmbed.tsx`
```typescript
// See ANALYTICS_DASHBOARD_IMPLEMENTATION_PLAN.md lines 291-373
```

#### Create: `lib/ui/components/AIChatInterface.tsx`
```typescript
// See ANALYTICS_DASHBOARD_IMPLEMENTATION_PLAN.md lines 568-667
```

#### Create: `lib/hooks/useAIChat.ts`
```typescript
// See ANALYTICS_DASHBOARD_IMPLEMENTATION_PLAN.md lines 671-736
```

#### Create: `app/analytics/page.tsx`
```typescript
// See ANALYTICS_DASHBOARD_IMPLEMENTATION_PLAN.md lines 377-418
```

---

### Phase 3: Brain Gateway Routes (2 hours)

**Critical:** Find Brain Gateway location first:

```bash
find /home/alagiri/projects/bizoholic/bizosaas-platform -name "brain-gateway" -o -name "brain_gateway" -type d
```

Once found, create:

#### `routes/analytics.py` (NEW FILE)
```python
# See ANALYTICS_DASHBOARD_IMPLEMENTATION_PLAN.md lines 434-561
```

Add to Brain Gateway `main.py`:
```python
from routes import analytics
app.include_router(analytics.router)
```

---

### Phase 4: Production Dockerfile (30 min)

#### Create: `Dockerfile.production`
```dockerfile
# See ANALYTICS_DASHBOARD_IMPLEMENTATION_PLAN.md lines 788-829
```

---

### Phase 5: Build & Push (1 hour)

```bash
cd /home/alagiri/projects/bizoholic/bizosaas-platform/frontend/apps/analytics-dashboard

# Build
docker build -f Dockerfile.production \
  -t ghcr.io/bizoholic-digital/bizosaas-analytics-dashboard:v1.0.0 \
  -t ghcr.io/bizoholic-digital/bizosaas-analytics-dashboard:latest \
  .

# Login to GHCR
echo "ghp_REDACTED" | docker login ghcr.io -u alagiri.rajesh@gmail.com --password-stdin

# Push
docker push ghcr.io/bizoholic-digital/bizosaas-analytics-dashboard:v1.0.0
docker push ghcr.io/bizoholic-digital/bizosaas-analytics-dashboard:latest
```

---

### Phase 6: Deploy to Dokploy (1 hour)

1. Go to: https://dk.bizoholic.com
2. Login: bizoholic.digital@gmail.com / 25IKC#1XiKABRo
3. Project: **frontend-services**
4. Click: **Add Service** → **Docker Image**

**Configuration:**
```yaml
Name: analytics-dashboard
Image: ghcr.io/bizoholic-digital/bizosaas-analytics-dashboard:latest
Port Mapping: 3007 → 3001 (container)
Network: dokploy-network

Environment Variables:
  NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://backend-brain-gateway:8001
  NEXT_PUBLIC_SUPERSET_DOMAIN=http://infrastructure-superset:8088
  NEXTAUTH_URL=https://stg.bizoholic.com/analytics
  NEXTAUTH_SECRET=<generate-with: openssl rand -base64 32>

Traefik Labels:
  traefik.enable=true
  traefik.http.routers.analytics-dashboard.rule=Host(`stg.bizoholic.com`) && PathPrefix(`/analytics`)
  traefik.http.routers.analytics-dashboard.entrypoints=websecure
  traefik.http.routers.analytics-dashboard.tls=true
  traefik.http.services.analytics-dashboard.loadbalancer.server.port=3001
```

5. Click: **Deploy**
6. Wait: ~2-3 minutes
7. Verify: https://stg.bizoholic.com/analytics

---

## 📋 VERIFICATION CHECKLIST

After deployment:

- [ ] Service shows as "running" in Dokploy
- [ ] Can access https://stg.bizoholic.com/analytics
- [ ] Superset dashboard embeds load
- [ ] AI chat interface responds
- [ ] Authentication works (redirect to login if not authenticated)
- [ ] Multi-tenant RLS enforced (users only see their data)
- [ ] No errors in browser console
- [ ] No errors in container logs

Check logs:
```bash
ssh root@72.60.219.244
docker service logs frontend-services-analytics-dashboard --tail 100 --follow
```

---

## 🔧 TROUBLESHOOTING

### Issue: Superset embed fails
**Solution:** Check Brain Gateway proxy routes are added and Superset is accessible at `http://infrastructure-superset:8088`

### Issue: AI chat not responding
**Solution:** Verify Personal AI Assistant is running in backend-ai-agents container

### Issue: Authentication redirect loop
**Solution:** Check NEXTAUTH_URL matches deployment URL exactly

### Issue: Build fails
**Solution:** Run `npm install` in the analytics-dashboard directory first

---

## 📊 SUPERSET CONFIGURATION

After Analytics Dashboard is deployed, configure Superset:

1. Access Superset: http://<KVM4-IP>:8088
2. Login: admin / Bizoholic2024Admin
3. Create Dashboards for each tenant
4. Configure Row-Level Security (RLS) filters
5. Generate dashboard IDs for embedding

---

## 📄 FILES TO CREATE

**Priority Order:**

1. **lib/api/superset-api.ts** - Superset SDK client (HIGH)
2. **lib/ui/components/SupersetEmbed.tsx** - Dashboard embedding (HIGH)
3. **app/analytics/page.tsx** - Main analytics page (HIGH)
4. **lib/hooks/useAIChat.ts** - AI chat hook (MEDIUM)
5. **lib/ui/components/AIChatInterface.tsx** - Chat UI (MEDIUM)
6. **Dockerfile.production** - Production build (HIGH)
7. **Brain Gateway routes/analytics.py** - Backend proxy (HIGH)

**Total Files:** 7 core files + supporting type definitions

---

## 💡 QUICK IMPLEMENTATION STRATEGY

**Option A: Step-by-Step (Recommended for learning)**
- Follow phases 2-6 in order
- Test each phase before moving to next
- ~10-13 hours total

**Option B: Fast Track (For experienced developers)**
- Create all 7 core files at once
- Build and deploy immediately
- Debug in production
- ~6-8 hours total

---

## 🎯 SUCCESS METRICS

When complete:
- ✅ Analytics Dashboard accessible at https://stg.bizoholic.com/analytics
- ✅ Superset dashboards embedded and interactive
- ✅ AI chat provides intelligent analytics insights
- ✅ Multi-tenant data isolation working
- ✅ All 3 admin tools deployed (Analytics + BizOSaaS Admin + Setup Wizard)
- ✅ Platform 100% complete (9/9 frontends)

---

## 📞 NEED HELP?

**Documentation References:**
- Full implementation: [ANALYTICS_DASHBOARD_IMPLEMENTATION_PLAN.md](ANALYTICS_DASHBOARD_IMPLEMENTATION_PLAN.md)
- Platform status: [PLATFORM_STATUS_COMPREHENSIVE_SUMMARY_2025-11-04.md](PLATFORM_STATUS_COMPREHENSIVE_SUMMARY_2025-11-04.md)
- Superset analysis: [APACHE_SUPERSET_ANALYSIS.md](../APACHE_SUPERSET_ANALYSIS.md)

**Credentials:**
- All access: [credentials.md](../bizoholic/credentials.md)

**Support:**
- GitHub: https://github.com/Bizoholic-Digital/bizosaas-platform
- Dokploy: https://dk.bizoholic.com

---

**Status:** Phase 1 Complete ✅
**Next:** Create core library files (Phase 2)
**Estimated Time Remaining:** 9-12 hours
**Last Updated:** November 4, 2025
