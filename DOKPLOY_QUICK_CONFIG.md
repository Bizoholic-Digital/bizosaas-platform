# ⚡ Dokploy Quick Configuration - Bizoholic Frontend

**Use this guide while configuring in Dokploy UI**
**Token:** Use the actual token from `/home/alagiri/projects/bizoholic/credentials.md`

---

## 🎯 Copy-Paste Ready Configuration

### Basic Settings
```
Name: bizoholic-frontend
Type: Docker Image
Image: ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:working-2025-10-30
```

### Registry (Copy actual token from credentials.md)
```
Type: GitHub Container Registry (GHCR)
Username: alagirirajesh
Token: <paste from credentials.md>
```

### Environment Variables (Copy entire block)
```
NODE_ENV=production
PORT=3001
HOSTNAME=0.0.0.0
NEXT_TELEMETRY_DISABLED=1
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://brain-gateway.automationhub-n8n-91feb0-194-238-16-237.traefik.me
WAGTAIL_API_BASE_URL=http://wagtail-cms:8000/api/v2
AUTH_SERVICE_URL=http://auth-service:5000
NEXT_PUBLIC_SITE_URL=https://bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me
```

### Port
```
Container: 3001
Protocol: TCP
```

### Network
```
Network: bizosaas-network
```

### Domain
```
Domain: bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me
SSL: Yes
Force HTTPS: Yes
```

### Health Check
```
Enabled: Yes
Path: /
Port: 3001
Interval: 30s
Timeout: 10s
Retries: 3
```

### Resources
```
Memory Limit: 512Mi
Memory Reservation: 256Mi
CPU Limit: 0.5
CPU Reservation: 0.2
Replicas: 2
```

---

## ✅ Deployment Checklist

Before clicking Deploy:
- [ ] Image name correct
- [ ] Registry authenticated (use actual token)
- [ ] All environment variables added
- [ ] Port 3001 configured
- [ ] Network selected
- [ ] Domain configured
- [ ] Health check enabled
- [ ] Resources set

---

## 🚀 After Deployment

1. **Monitor logs** - Look for "Ready in Xms"
2. **Check health** - Should show green/healthy
3. **Test URL** - `https://bizoholic.automationhub-n8n-91feb0-194-238-16-237.traefik.me/`
4. **Verify routes** - Test `/` and `/login`

---

**Full details:** See [DOKPLOY_CONFIGURATION.md](./DOKPLOY_CONFIGURATION.md)
