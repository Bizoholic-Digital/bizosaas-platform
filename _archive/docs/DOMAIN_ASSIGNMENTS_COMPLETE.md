# BizOSaaS Platform - Domain Assignments & Traefik Configuration

**Date**: October 15, 2025, 5:50 PM
**Status**: Ready for Implementation
**Traefik Proxy**: Built-in with Dokploy

---

## 🌐 Domain Ownership & Assignment

### Production Domains (Assumed Purchased)

| Domain | Purpose | Service | Status |
|--------|---------|---------|--------|
| **bizoholic.com** | Marketing Website | Bizoholic Frontend | ✅ Assigned |
| **coreldove.com** | E-commerce Store | CorelDove Frontend | ✅ Assigned |
| **bizosaas.com** | Platform Root | Main Portal | ⚠️ Needs config |
| **portal.bizosaas.com** | Client Dashboard | Client Portal | ✅ Assigned |
| **admin.bizosaas.com** | Admin Dashboard | BizOSaaS Admin | ✅ Assigned |
| **thrillring.com** | Gaming Platform | ThrillRing Frontend | ⚠️ Optional |
| **quanttrade.com** | Trading Platform | QuantTrade Frontend | ⚠️ Optional |

### Staging Domains (Subdomains)

| Domain | Service | Port | Status |
|--------|---------|------|--------|
| **stg.bizoholic.com** | Bizoholic Staging | 3001 | ✅ Ready |
| **stg.coreldove.com** | CorelDove Staging | 3002 | ✅ Ready |
| **stg-portal.bizosaas.com** | Portal Staging | 3000 | ✅ Ready |
| **stg-admin.bizosaas.com** | Admin Staging | 3009 | ✅ Ready |
| **stg-business.bizosaas.com** | Business Directory | 3003 | ✅ Ready |
| **stg-gaming.thrillring.com** | ThrillRing Staging | 3005 | ⚠️ Needs build |
| **stg-trade.quanttrade.com** | QuantTrade Staging | 3012 | ⚠️ Disabled |

---

## 📊 Complete Service Map (23 Services)

### Infrastructure Layer (6 services) - NO PUBLIC DOMAINS

| # | Service | Container Name | Port | Access |
|---|---------|----------------|------|--------|
| 1 | PostgreSQL | bizosaas-postgres-staging | 5433 | Internal only |
| 2 | Redis | bizosaas-redis-staging | 6380 | Internal only |
| 3 | Vault | bizosaas-vault-staging | 8201 | Internal only |
| 4 | Temporal Server | bizosaas-temporal-server-staging | 7234 | Internal only |
| 5 | Temporal UI | bizosaas-temporal-ui-staging | 8083 | **Optional**: `temporal.bizosaas.com` |
| 6 | Superset | bizosaas-superset-staging | 8088 | **Optional**: `analytics.bizosaas.com` |

### Backend Layer (10 services) - NO PUBLIC DOMAINS (All via Brain Gateway)

| # | Service | Container Name | Port | Internal Route |
|---|---------|----------------|------|----------------|
| 1 | Saleor | bizosaas-saleor-staging | 8000 | `/api/brain/saleor/*` |
| 2 | Brain Gateway | bizosaas-brain-staging | 8001 | `/api/brain/*` |
| 3 | Wagtail CMS | bizosaas-wagtail-staging | 8002 | `/api/brain/wagtail/*` |
| 4 | Django CRM | bizosaas-django-crm-staging | 8003 | `/api/brain/django-crm/*` |
| 5 | Business Directory | bizosaas-business-directory-staging | 8004 | `/api/brain/business-directory/*` |
| 6 | CorelDove Backend | bizosaas-coreldove-backend-staging | 8005 | `/api/brain/coreldove/*` |
| 7 | Auth Service | bizosaas-auth-service-staging | 8006 | `/api/brain/auth/*` |
| 8 | AI Agents | bizosaas-ai-agents-staging | 8008 | `/api/brain/ai-agents/*` |
| 9 | Amazon Sourcing | bizosaas-amazon-sourcing-staging | 8009 | `/api/brain/amazon/*` |
| 10 | QuantTrade Backend | bizosaas-quanttrade-backend-staging | 8012 | `/api/brain/quanttrade/*` |

### Frontend Layer (7 services) - REQUIRE PUBLIC DOMAINS

| # | Service | Container Name | Port | Domain | Priority |
|---|---------|----------------|------|--------|----------|
| 1 | Client Portal | bizosaas-client-portal-staging | 3000 | `portal.bizosaas.com` | HIGH |
| 2 | Bizoholic | bizosaas-bizoholic-frontend-staging | 3001 | `bizoholic.com` | **CRITICAL** |
| 3 | CorelDove | bizosaas-coreldove-frontend-staging | 3002 | `coreldove.com` | HIGH |
| 4 | Business Directory | bizosaas-business-directory-frontend-staging | 3003 | `directory.bizosaas.com` | MEDIUM |
| 5 | ThrillRing Gaming | bizosaas-thrillring-gaming-staging | 3005 | `thrillring.com` | MEDIUM |
| 6 | Admin Dashboard | bizosaas-admin-dashboard-staging | 3009 | `admin.bizosaas.com` | HIGH |
| 7 | QuantTrade | (disabled) | 3012 | `quanttrade.com` | LOW |

---

## 🔧 Traefik Labels Configuration

### Complete Compose Files with Traefik Labels

#### Frontend Services with Traefik Configuration

```yaml
# dokploy-frontend-staging-with-domains.yml

services:
  # ==========================================
  # 1. CLIENT PORTAL (Port 3000)
  # ==========================================
  client-portal:
    image: bizosaas-client-portal:latest
    container_name: bizosaas-client-portal-staging
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-staging:8001
      - NEXT_TELEMETRY_DISABLED=1
    networks:
      - dokploy-network
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.client-portal.rule=Host(`portal.bizosaas.com`) || Host(`stg-portal.bizosaas.com`)"
      - "traefik.http.routers.client-portal.entrypoints=websecure"
      - "traefik.http.routers.client-portal.tls=true"
      - "traefik.http.routers.client-portal.tls.certresolver=letsencrypt"
      - "traefik.http.services.client-portal.loadbalancer.server.port=3000"

  # ==========================================
  # 2. BIZOHOLIC FRONTEND (Port 3001) - CRITICAL
  # ==========================================
  bizoholic-frontend:
    image: bizosaas-bizoholic-frontend:latest
    container_name: bizosaas-bizoholic-frontend-staging
    ports:
      - "3001:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-staging:8001
      - NEXT_TELEMETRY_DISABLED=1
    networks:
      - dokploy-network
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.bizoholic.rule=Host(`bizoholic.com`) || Host(`www.bizoholic.com`) || Host(`stg.bizoholic.com`)"
      - "traefik.http.routers.bizoholic.entrypoints=websecure"
      - "traefik.http.routers.bizoholic.tls=true"
      - "traefik.http.routers.bizoholic.tls.certresolver=letsencrypt"
      - "traefik.http.services.bizoholic.loadbalancer.server.port=3000"
      # Redirect www to non-www
      - "traefik.http.middlewares.bizoholic-redirect.redirectregex.regex=^https://www\\.bizoholic\\.com/(.*)"
      - "traefik.http.middlewares.bizoholic-redirect.redirectregex.replacement=https://bizoholic.com/$${1}"
      - "traefik.http.routers.bizoholic.middlewares=bizoholic-redirect"

  # ==========================================
  # 3. CORELDOVE FRONTEND (Port 3002)
  # ==========================================
  coreldove-frontend:
    image: bizosaas-coreldove-frontend:latest
    container_name: bizosaas-coreldove-frontend-staging
    ports:
      - "3002:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-staging:8001
      - NEXT_TELEMETRY_DISABLED=1
    networks:
      - dokploy-network
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.coreldove.rule=Host(`coreldove.com`) || Host(`www.coreldove.com`) || Host(`stg.coreldove.com`)"
      - "traefik.http.routers.coreldove.entrypoints=websecure"
      - "traefik.http.routers.coreldove.tls=true"
      - "traefik.http.routers.coreldove.tls.certresolver=letsencrypt"
      - "traefik.http.services.coreldove.loadbalancer.server.port=3000"

  # ==========================================
  # 4. BUSINESS DIRECTORY FRONTEND (Port 3003)
  # ==========================================
  business-directory-frontend:
    image: bizosaas-business-directory:latest
    container_name: bizosaas-business-directory-frontend-staging
    ports:
      - "3003:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-staging:8001
      - NEXT_TELEMETRY_DISABLED=1
    networks:
      - dokploy-network
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.business-directory.rule=Host(`directory.bizosaas.com`) || Host(`stg-business.bizosaas.com`)"
      - "traefik.http.routers.business-directory.entrypoints=websecure"
      - "traefik.http.routers.business-directory.tls=true"
      - "traefik.http.routers.business-directory.tls.certresolver=letsencrypt"
      - "traefik.http.services.business-directory.loadbalancer.server.port=3000"

  # ==========================================
  # 5. THRILLRING GAMING (Port 3005)
  # ==========================================
  thrillring-gaming:
    image: bizosaas-thrillring-gaming:latest
    container_name: bizosaas-thrillring-gaming-staging
    ports:
      - "3005:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-staging:8001
      - NEXT_TELEMETRY_DISABLED=1
    networks:
      - dokploy-network
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.thrillring.rule=Host(`thrillring.com`) || Host(`www.thrillring.com`) || Host(`stg-gaming.thrillring.com`)"
      - "traefik.http.routers.thrillring.entrypoints=websecure"
      - "traefik.http.routers.thrillring.tls=true"
      - "traefik.http.routers.thrillring.tls.certresolver=letsencrypt"
      - "traefik.http.services.thrillring.loadbalancer.server.port=3000"

  # ==========================================
  # 6. ADMIN DASHBOARD (Port 3009)
  # ==========================================
  admin-dashboard:
    image: bizosaas-bizosaas-admin:latest
    container_name: bizosaas-admin-dashboard-staging
    ports:
      - "3009:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-staging:8001
      - NEXT_TELEMETRY_DISABLED=1
    networks:
      - dokploy-network
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.admin.rule=Host(`admin.bizosaas.com`) || Host(`stg-admin.bizosaas.com`)"
      - "traefik.http.routers.admin.entrypoints=websecure"
      - "traefik.http.routers.admin.tls=true"
      - "traefik.http.routers.admin.tls.certresolver=letsencrypt"
      - "traefik.http.services.admin.loadbalancer.server.port=3000"
      # Add basic auth for admin (optional)
      # - "traefik.http.middlewares.admin-auth.basicauth.users=admin:$$apr1$$..."
      # - "traefik.http.routers.admin.middlewares=admin-auth"

networks:
  dokploy-network:
    external: true
```

---

## 📋 DNS Configuration Required

### A Records to Configure

Point all domains to VPS IP: **194.238.16.237**

```dns
# Main Production Domains
bizoholic.com                A       194.238.16.237
www.bizoholic.com            A       194.238.16.237
coreldove.com                A       194.238.16.237
www.coreldove.com            A       194.238.16.237
thrillring.com               A       194.238.16.237
www.thrillring.com           A       194.238.16.237

# BizOSaaS Subdomains
bizosaas.com                 A       194.238.16.237
portal.bizosaas.com          A       194.238.16.237
admin.bizosaas.com           A       194.238.16.237
directory.bizosaas.com       A       194.238.16.237

# Staging Subdomains
stg.bizoholic.com            A       194.238.16.237
stg.coreldove.com            A       194.238.16.237
stg-portal.bizosaas.com      A       194.238.16.237
stg-admin.bizosaas.com       A       194.238.16.237
stg-business.bizosaas.com    A       194.238.16.237
stg-gaming.thrillring.com    A       194.238.16.237

# Optional (Admin/Monitoring Tools)
temporal.bizosaas.com        A       194.238.16.237
analytics.bizosaas.com       A       194.238.16.237
```

### Wildcard Option (Recommended)

```dns
*.bizosaas.com               A       194.238.16.237
```

---

## 🔐 SSL/TLS Certificate Configuration

### Let's Encrypt Auto-Renewal

Traefik will automatically request and renew certificates for all configured domains.

**Certificate Resolver Configuration** (in Dokploy/Traefik):
```yaml
certificatesResolvers:
  letsencrypt:
    acme:
      email: bizoholic.digital@gmail.com
      storage: /letsencrypt/acme.json
      httpChallenge:
        entryPoint: web
```

### Certificate Coverage

| Domain | Certificate | Status |
|--------|-------------|--------|
| bizoholic.com | Let's Encrypt | Auto-renewed |
| coreldove.com | Let's Encrypt | Auto-renewed |
| *.bizosaas.com | Let's Encrypt Wildcard | Auto-renewed |
| thrillring.com | Let's Encrypt | Auto-renewed |

---

## 🚀 Implementation Checklist

### Phase 1: DNS Configuration (30 minutes)
- [ ] Log into domain registrar (Cloudflare/Namecheap/etc.)
- [ ] Add A records for all production domains
- [ ] Add A records for staging subdomains
- [ ] Configure wildcard DNS for `*.bizosaas.com`
- [ ] Verify DNS propagation (use `dig` or online tools)

### Phase 2: Update Compose Files (15 minutes)
- [ ] Add Traefik labels to frontend compose file
- [ ] Configure certificate resolver email
- [ ] Set up proper domain routing rules
- [ ] Add www redirects where needed
- [ ] Commit and push changes to GitHub

### Phase 3: Deploy with Domains (30 minutes)
- [ ] Redeploy frontend services via Dokploy
- [ ] Wait for Traefik to detect labels
- [ ] Let's Encrypt will auto-request certificates
- [ ] Verify HTTPS working on all domains
- [ ] Test all frontend applications

### Phase 4: Verification (15 minutes)
- [ ] Test https://bizoholic.com
- [ ] Test https://coreldove.com
- [ ] Test https://portal.bizosaas.com
- [ ] Test https://admin.bizosaas.com
- [ ] Test https://directory.bizosaas.com
- [ ] Verify SSL certificates valid
- [ ] Test staging subdomain access

---

## 📊 Domain Priority Matrix

| Priority | Domain | Service | Action | Timeline |
|----------|--------|---------|--------|----------|
| 🔴 CRITICAL | bizoholic.com | Bizoholic Frontend | Configure NOW | Immediate |
| 🟠 HIGH | coreldove.com | CorelDove Frontend | Configure NOW | Immediate |
| 🟠 HIGH | portal.bizosaas.com | Client Portal | Configure NOW | Immediate |
| 🟠 HIGH | admin.bizosaas.com | Admin Dashboard | Configure NOW | Immediate |
| 🟡 MEDIUM | directory.bizosaas.com | Business Directory | Configure | Week 1 |
| 🟡 MEDIUM | thrillring.com | ThrillRing Gaming | Configure | Week 2 |
| 🟢 LOW | quanttrade.com | QuantTrade (disabled) | Future | When rebuilt |

---

## 💡 Best Practices

### 1. Domain Management
- Use Cloudflare for DNS + CDN (recommended)
- Enable DNSSEC for security
- Set TTL to 300 seconds during setup
- Use wildcard DNS for flexibility

### 2. SSL/TLS
- Let Traefik handle certificate management
- Monitor certificate expiry via Dokploy dashboard
- Use HSTS headers for security
- Redirect HTTP → HTTPS automatically

### 3. Traefik Configuration
- Use descriptive router names
- Group related middleware
- Enable access logs for debugging
- Set up health checks per service

### 4. Monitoring
- Check Traefik dashboard: `http://194.238.16.237:8080`
- Monitor certificate renewal logs
- Set up alerts for SSL expiry
- Track domain response times

---

## 🎯 Expected Results After Implementation

### Frontend Access
✅ https://bizoholic.com → Bizoholic Marketing Site
✅ https://coreldove.com → CorelDove E-commerce
✅ https://portal.bizosaas.com → Client Portal
✅ https://admin.bizosaas.com → Admin Dashboard
✅ https://directory.bizosaas.com → Business Directory

### Backend Access (Internal Only)
✅ http://bizosaas-brain-staging:8001 → AI Gateway
✅ All backend services via `/api/brain/*` routes

### Infrastructure (Internal Only)
✅ PostgreSQL, Redis, Vault - No public access
⚠️ Optional: Temporal UI, Superset on subdomains

---

**Status**: ✅ **READY FOR DNS & TRAEFIK CONFIGURATION**
**Next Action**: Configure DNS A records → Update compose files → Redeploy
**Estimated Time**: 1.5 hours total

**Last Updated**: October 15, 2025, 5:50 PM
