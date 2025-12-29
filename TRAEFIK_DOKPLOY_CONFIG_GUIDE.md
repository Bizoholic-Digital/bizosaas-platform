# Traefik + Dokploy Configuration for Client Portal (Staging)

**Last Updated:** 2025-12-29

---

## Purpose
Correct routing of the client portal at `https://stg.bizoholic.com/portal` depends on:
1. The application being built and run with `BASE_PATH=/portal` and `PORT=3003`.
2. Proper Traefik labels set in Dokploy for the client-portal staging service.

---

## Required Traefik Labels (Dokploy UI)
Add these in the **Labels** section for the Docker service:

```
traefik.enable=true
traefik.http.routers.client-portal.rule=Host(`stg.bizoholic.com`) && PathPrefix(`/portal`)
traefik.http.routers.client-portal.entrypoints=websecure
traefik.http.routers.client-portal.tls=true
traefik.http.routers.client-portal.tls.certresolver=letsencrypt
traefik.http.routers.client-portal.service=client-portal
traefik.http.services.client-portal.loadbalancer.server.port=3003
traefik.docker.network=dokploy-network
```

---

## Dokploy Steps
1. Go to: https://dk4.bizoholic.com/dashboard
2. Find **client-portal** service (staging environment).
3. Paste the above labels in the configuration area for labels/Traefik.
4. Save.
5. Click **Redeploy**.
6. After deploy, check:
   - https://stg.bizoholic.com/portal
   - Should load without proxy or 502 errors.
---

## Troubleshooting
- If problems persist, ensure your Docker image exposes port 3003 and is built with `BASE_PATH=/portal` at build time.
- Inspect container logs to confirm the application is running and listening on the right port.

See also: CLIENT_PORTAL_502_TRAEFIK_LABELS_MISSING.md in this folder for additional diagnosis info.
