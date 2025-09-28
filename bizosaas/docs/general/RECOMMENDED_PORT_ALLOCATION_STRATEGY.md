# BizOSaaS Platform - Port Reorganization Strategy

## Security-First Port Allocation

### 🌐 PUBLIC ACCESS PORTS (Internet-facing)
These ports should be accessible to end users:

```
Port 80   - HTTP (Traefik Router) - Redirects to HTTPS
Port 443  - HTTPS (Traefik Router) - Main entry point
Port 3000 - Bizoholic Marketing Website (Static)
Port 3002 - CoreLDove E-commerce Frontend (Public)
```

### 🔒 AUTHENTICATED ACCESS PORTS (Login required)
These ports require authentication but are accessible through the unified dashboard:

```
Port 3005 - Unified Next.js Frontend (BizoSaaS Dashboard)
Port 3010 - Wagtail CMS Admin (Headless mode)
Port 3015 - Saleor GraphQL Admin Dashboard
Port 3020 - Business Directory Management Interface
```

### 🔐 ADMIN-ONLY PORTS (Internal access only)
These ports should only be accessible to system administrators:

```
Port 8200 - HashiCorp Vault (Secrets management)
Port 8090 - System Monitoring Dashboard
Port 8080 - Traefik Dashboard (Admin)
Port 9090 - Prometheus Metrics (if implemented)
Port 3000 - Grafana (if implemented)
```

### 🚫 PRIVATE/INTERNAL PORTS (Not exposed)
These ports should never be exposed to the internet:

```
Port 5432 - PostgreSQL Primary Database
Port 5433 - PostgreSQL Secondary Database  
Port 5434 - PostgreSQL Staging Database
Port 6379 - Redis Primary Cache
Port 6380 - Redis Secondary Cache
Port 6381 - Redis Session Store
```

### 🧪 DEVELOPMENT PORTS (Dev environment only)
These ports are only used during development:

```
Port 8007 - Wagtail Development Server
Port 3001 - Hot Reload/Dev Tools
Port 5173 - Vite Dev Server (if using Vite)
Port 4000 - Storybook (if implemented)
```

## Implementation Plan

### Phase 1: Immediate Security Fixes
1. **Block direct database access** - Remove public exposure of PostgreSQL ports
2. **Secure Redis instances** - Move Redis to internal network only
3. **Protect monitoring** - Move monitoring from 3001 to admin-only port
4. **Implement reverse proxy** - All admin access through Traefik with authentication

### Phase 2: Port Standardization
1. **Unified frontend** on port 3005 (already implemented)
2. **Admin interfaces** moved to 301X range with authentication
3. **Public websites** on standard ports (80/443 via Traefik)
4. **Development services** on 800X range, localhost only

### Phase 3: Domain-Based Routing
Instead of ports, use subdomains:
```
bizoholic.com           → Marketing website (port 3000)
app.bizosaas.com        → Unified dashboard (port 3005)
admin.bizosaas.com      → Wagtail CMS (port 3010)
shop.coreldove.com      → Saleor storefront (port 3002)
directory.bizosaas.com  → Business directory (port 3020)
```

## Security Measures

### 1. Network Segmentation
- **Public DMZ**: Ports 80, 443, 3000, 3002
- **Application Tier**: Ports 3005, 3010, 3015, 3020
- **Admin Tier**: Ports 8080, 8090, 8200
- **Database Tier**: Ports 5432+, 6379+ (no external access)

### 2. Authentication Requirements
- **Public ports**: No authentication required
- **Application ports**: JWT/Session authentication
- **Admin ports**: Multi-factor authentication required
- **Database ports**: VPN/internal network only

### 3. Firewall Rules
```bash
# Allow public access
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow application access (authenticated)
iptables -A INPUT -p tcp --dport 3005 -j ACCEPT

# Block database ports from external access
iptables -A INPUT -p tcp --dport 5432 -s 10.0.0.0/8 -j ACCEPT
iptables -A INPUT -p tcp --dport 5432 -j DROP

# Block Redis from external access  
iptables -A INPUT -p tcp --dport 6379 -s 10.0.0.0/8 -j ACCEPT
iptables -A INPUT -p tcp --dport 6379 -j DROP
```

### 4. SSL/TLS Requirements
- **All public ports**: SSL certificates required
- **Admin interfaces**: Client certificate authentication
- **Database connections**: TLS encryption mandatory
- **Internal APIs**: mTLS for service-to-service communication

## Current Issues to Fix

### Critical Security Issues
1. ❌ **PostgreSQL exposed on 5432-5434** - Direct database access from internet
2. ❌ **Redis exposed on 6379-6380** - Cache accessible from internet  
3. ❌ **Monitoring on 3001** - Admin interface publicly accessible
4. ❌ **No authentication on admin ports** - Direct access to admin interfaces

### Port Conflicts
1. ⚠️ **Wagtail on both 8006 and 8007** - Choose one port for production
2. ⚠️ **Multiple PostgreSQL instances** - Consolidate or clarify purpose
3. ⚠️ **Redis duplication** - Clarify primary vs secondary usage

## Recommended Next Steps

1. **Immediate**: Block dangerous ports (5432+, 6379+) from internet access
2. **Phase 1**: Implement Traefik authentication for admin interfaces  
3. **Phase 2**: Migrate to standardized port ranges
4. **Phase 3**: Implement domain-based routing with SSL
5. **Phase 4**: Add monitoring and alerting for unauthorized access attempts

## Environment-Specific Configuration

### Production
- Only ports 80/443 exposed to internet
- All admin access through VPN or bastion host
- Database connections encrypted and access-logged

### Staging  
- Limited port exposure for testing
- Authentication required for all non-public services
- Monitoring and logging enabled

### Development
- Localhost-only for dangerous services
- Development ports clearly separated
- Mock authentication for testing