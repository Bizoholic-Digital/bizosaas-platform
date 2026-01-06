# 📗 Master Deployment Solution Guide
This document contains the definitive fixes for the BizOSaaS platform (Staging Environment). 

## 🚨 The Primary Recurring Issue: 502 Bad Gateway
**Cause**: Port and Routing Conflict.
1. **Redundant Service**: The `client-portal` was defined in two stacks, confusing Traefik.
2. **Port Mismatch**: Dokploy expected internal port `3003`/`3004`, but the app was listening on `3000`.

## ✅ The Permanent Fix (Applied Jan 6, 2026)

### 1. Unified Networking & Ports
- **Client Portal**: Listening on internal port **3003**, mapped to external **3003**.
- **Admin Dashboard**: Listening on internal port **3004**, mapped to external **3004**.
- **Brain Gateway**: Listening on internal port **8000**.
- **Priority**: Custom Traefik priority is set to `5000` to override any Dokploy defaults.

### 2. Redeploy Sequence (Do this in order)
If everything goes down or you get a 502, simply redeploy in this exact order:
1. **Stack**: `bizosaascore-braingateway-kdbono` (The Brain)
2. **Stack**: `bizosaasfrontend-clientportal-r1a5il` (Client Portal)
3. **Stack**: `bizosaasfrontend-adminportal-do3e1r` (Admin Dashboard)

## 🛠️ Essential VPS Troubleshooting Commands
If web pages are not loading, SSH to the VPS and run:

### Check Routing (Is Traefik seeing the portal?)
```bash
# Search Traefik logs for the specific domain
docker logs dokploy-traefik_traefik.0zd884g5tjahfhu08ns41jefn.z0qiobivsuoa0l5p618zy7ihz | grep "app.bizoholic.net"
```

### Check Container Internal Port (Is the app actually listening?)
```bash
# Should return "Ready" and show port 3003/3004
docker logs bizosaasfrontend-clientportal-r1a5il-client-portal-1
```

### Force Cleanup (If Dokploy says "Container Name Already in Use")
```bash
docker rm -f bizosaas-admin-dashboard-staging
docker rm -f bizosaas-client-portal-staging
```

## 🔐 Auth Troubleshooting (Clerk)
If the login form doesn't appear:
1. Ensure `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` is set in the Dokploy environment variables.
2. Check `credentials.md` for the latest verified keys.

## 📡 Health Check URLs
Verify these from your browser:
- **API**: [https://api.bizoholic.net/docs](https://api.bizoholic.net/docs)
- **Client**: [https://app.bizoholic.net/api/health](https://app.bizoholic.net/api/health)
- **Admin**: [https://admin.bizoholic.net/api/health](https://admin.bizoholic.net/api/health)
