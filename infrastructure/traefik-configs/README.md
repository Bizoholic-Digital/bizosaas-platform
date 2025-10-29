# Traefik Configuration Backup

**Date:** 2025-10-29
**Server:** KVM4 (72.60.219.244)
**Purpose:** Working Traefik configurations for frontend services

## Files

### frontend-bizoholic-frontend.yml
- **Domain:** stg.bizoholic.com
- **Service:** frontend-bizoholic-frontend
- **Status:** ✅ WORKING
- **Features:**
  - Frontend routing on port 3000 (internal)
  - API proxy to brain-gateway (priority 20)
  - Let's Encrypt SSL/TLS
  - HTTP to HTTPS redirect

## Deployment Location

These files should be placed in:
```
/etc/dokploy/traefik/dynamic/
```

## Important Notes

1. **Port Configuration:**
   - Frontend service URL: `http://frontend-bizoholic-frontend:3000` (internal port)
   - Published port is 3001, but Traefik connects to internal port 3000

2. **API Routing:**
   - `/api/*` requests routed directly to brain-gateway
   - Priority 20 for API routes, priority 10 for frontend routes

3. **Restore Instructions:**
   ```bash
   scp frontend-bizoholic-frontend.yml root@72.60.219.244:/etc/dokploy/traefik/dynamic/
   ```

## Changes History

- 2025-10-29: Initial working configuration created
  - Fixed port from 3001 to 3000
  - Added API routing to brain-gateway
  - Configured priorities and SSL
