# Frontend Domain Configuration Guide
## Complete DNS, SSL, and Traefik Setup for Staging Domains

**Version**: 1.0.0
**Environment**: Staging
**Last Updated**: October 10, 2025

---

## Table of Contents

1. [Overview](#overview)
2. [DNS Configuration](#dns-configuration)
3. [SSL Certificate Setup](#ssl-certificate-setup)
4. [Traefik Reverse Proxy Configuration](#traefik-reverse-proxy-configuration)
5. [Path-Based Routing](#path-based-routing)
6. [Domain Testing](#domain-testing)
7. [Troubleshooting](#troubleshooting)

---

## Overview

### Staging Domain Architecture

The BizOSaaS frontend deployment uses three primary staging domains with path-based routing:

```
stg.bizoholic.com
    ├── / (root)              → bizoholic-frontend (marketing site)
    ├── /login/*              → client-portal (client dashboard)
    └── /admin/*              → admin-dashboard (admin panel)

stg.coreldove.com
    └── / (all paths)         → coreldove-frontend (e-commerce)

stg.thrillring.com
    └── / (all paths)         → thrillring-gaming (gaming platform)
```

### Domain Routing Summary

| Domain/Path | Container | Port | Purpose |
|-------------|-----------|------|---------|
| stg.bizoholic.com | bizoholic-frontend-3000 | 3000 | Marketing website |
| stg.bizoholic.com/login/* | bizosaas-client-portal-3001 | 3001 | Client portal |
| stg.bizoholic.com/admin/* | bizosaas-admin-3009 | 3009 | Admin dashboard |
| stg.coreldove.com | coreldove-frontend-3002 | 3002 | E-commerce site |
| stg.thrillring.com | thrillring-gaming-3005 | 3005 | Gaming platform |

### Key Features

- **HTTPS Everywhere**: All domains use automatic Let's Encrypt SSL
- **Reverse Proxy**: Traefik handles all routing and SSL termination
- **Path-Based Routing**: Multiple applications on single domain
- **Priority Routing**: High-priority paths evaluated first
- **Middleware**: Path prefix stripping for clean URLs

---

## DNS Configuration

### Step-by-Step DNS Setup

#### 1. Access Your DNS Provider

Common DNS providers:
- **Cloudflare**: https://dash.cloudflare.com
- **Namecheap**: https://www.namecheap.com/myaccount/
- **GoDaddy**: https://dcc.godaddy.com/manage/dns
- **Google Domains**: https://domains.google.com
- **Route 53 (AWS)**: https://console.aws.amazon.com/route53/

#### 2. Add A Records

For each staging domain, add an A record:

**Record 1: stg.bizoholic.com**
```
Type:  A
Name:  stg (or stg.bizoholic.com depending on provider)
Value: 194.238.16.237
TTL:   300 (5 minutes)
```

**Record 2: stg.coreldove.com**
```
Type:  A
Name:  stg (or stg.coreldove.com depending on provider)
Value: 194.238.16.237
TTL:   300 (5 minutes)
```

**Record 3: stg.thrillring.com**
```
Type:  A
Name:  stg (or stg.thrillring.com depending on provider)
Value: 194.238.16.237
TTL:   300 (5 minutes)
```

#### 3. Verify DNS Records

After adding records, verify they're configured correctly:

```bash
# Check stg.bizoholic.com
nslookup stg.bizoholic.com

# Expected output:
# Server:  [DNS Server]
# Address: [DNS Server IP]
#
# Name:    stg.bizoholic.com
# Address: 194.238.16.237

# Check stg.coreldove.com
nslookup stg.coreldove.com

# Check stg.thrillring.com
nslookup stg.thrillring.com

# Alternative: use dig
dig stg.bizoholic.com +short
# Expected: 194.238.16.237

# Check from multiple DNS servers
dig @8.8.8.8 stg.bizoholic.com +short  # Google DNS
dig @1.1.1.1 stg.bizoholic.com +short  # Cloudflare DNS
```

#### 4. Wait for DNS Propagation

**Typical Propagation Times**:
- Local/Same Network: Instant to 5 minutes
- Same Country: 5-30 minutes
- Global: 30 minutes to 2 hours
- Maximum: Up to 48 hours (rare with low TTL)

**Check Propagation Status**:
```bash
# Use online tools
# https://www.whatsmydns.net/#A/stg.bizoholic.com

# Or check manually from different locations
# Ask colleagues in different regions to run:
nslookup stg.bizoholic.com
```

### DNS Configuration by Provider

#### Cloudflare

1. Log in to Cloudflare dashboard
2. Select your domain
3. Click **DNS** in left sidebar
4. Click **Add record**
5. Configure:
   - Type: `A`
   - Name: `stg`
   - IPv4 address: `194.238.16.237`
   - Proxy status: **DNS only** (gray cloud, NOT proxied)
   - TTL: `Auto` or `300`
6. Click **Save**
7. Repeat for other domains

**Important**: Disable Cloudflare proxy (orange cloud) for staging domains to allow Let's Encrypt validation.

#### Namecheap

1. Log in to Namecheap account
2. Navigate to **Domain List**
3. Click **Manage** next to your domain
4. Go to **Advanced DNS** tab
5. Click **Add New Record**
6. Configure:
   - Type: `A Record`
   - Host: `stg`
   - Value: `194.238.16.237`
   - TTL: `5 min` or `Automatic`
7. Click **Save All Changes**
8. Repeat for other domains

#### GoDaddy

1. Log in to GoDaddy account
2. Click **My Products**
3. Find your domain and click **DNS**
4. Click **Add** in Records section
5. Configure:
   - Type: `A`
   - Name: `stg`
   - Value: `194.238.16.237`
   - TTL: `600` (10 minutes) or `Custom: 300`
6. Click **Save**
7. Repeat for other domains

#### AWS Route 53

1. Log in to AWS Console
2. Navigate to Route 53
3. Select your hosted zone
4. Click **Create Record**
5. Configure:
   - Record name: `stg`
   - Record type: `A`
   - Value: `194.238.16.237`
   - TTL: `300`
   - Routing policy: `Simple routing`
6. Click **Create records**
7. Repeat for other domains

### DNS Best Practices

1. **Use Low TTL for Staging**: Set TTL to 300 seconds (5 minutes) for quick updates
2. **No CNAME for Root**: Don't create CNAME records for `stg.bizoholic.com`, use A records
3. **No Proxy Initially**: Disable CDN/proxy for initial SSL certificate generation
4. **Verify Before Deployment**: Ensure DNS resolves correctly before deploying frontends
5. **Document Changes**: Keep record of DNS changes for rollback if needed

---

## SSL Certificate Setup

### Automatic SSL with Let's Encrypt

Dokploy's Traefik automatically handles SSL certificate generation and renewal.

#### How It Works

1. **Container Starts**: Frontend container starts with Traefik labels
2. **Traefik Detects**: Traefik sees `tls=true` and `certresolver=letsencrypt`
3. **First HTTPS Request**: When browser visits https://stg.bizoholic.com
4. **ACME Challenge**: Traefik requests certificate from Let's Encrypt
5. **HTTP-01 Validation**: Let's Encrypt validates you control the domain
6. **Certificate Issued**: Certificate issued and installed automatically
7. **HTTPS Serving**: Site now serves over HTTPS with valid certificate

#### Timeline

| Event | Time |
|-------|------|
| Container starts | 0 seconds |
| First HTTPS request | User-initiated |
| ACME challenge begins | +5 seconds |
| Domain validation | +10-30 seconds |
| Certificate issued | +30-60 seconds |
| HTTPS active | +60-120 seconds |

**Total**: 1-2 minutes after first HTTPS request

#### Certificate Details

- **Certificate Authority**: Let's Encrypt
- **Certificate Type**: Domain Validation (DV)
- **Validity Period**: 90 days
- **Renewal**: Automatic at 60 days
- **Wildcard**: No (individual certs per domain)
- **Chain**: Full chain included

### Manual Certificate Verification

#### Check Certificate Status

```bash
# View certificate for stg.bizoholic.com
echo | openssl s_client -connect stg.bizoholic.com:443 -servername stg.bizoholic.com 2>/dev/null | openssl x509 -noout -text

# View certificate dates (issue and expiry)
echo | openssl s_client -connect stg.bizoholic.com:443 -servername stg.bizoholic.com 2>/dev/null | openssl x509 -noout -dates

# Example output:
# notBefore=Oct 10 12:00:00 2025 GMT
# notAfter=Jan  8 12:00:00 2026 GMT

# Check certificate is valid for domain
echo | openssl s_client -connect stg.bizoholic.com:443 -servername stg.bizoholic.com 2>/dev/null | openssl x509 -noout -subject -issuer

# Example output:
# subject=CN = stg.bizoholic.com
# issuer=C = US, O = Let's Encrypt, CN = R3
```

#### Browser Verification

1. **Visit Domain**: Navigate to https://stg.bizoholic.com
2. **Check Lock Icon**: Green/gray lock icon in address bar
3. **View Certificate**: Click lock icon → Certificate
4. **Verify Details**:
   - Issued to: stg.bizoholic.com
   - Issued by: Let's Encrypt Authority X3 or R3
   - Valid from: (today's date)
   - Valid to: (90 days from issue)
   - Certificate Status: Valid

#### Automated Certificate Check

```bash
# Check all staging domains
for domain in stg.bizoholic.com stg.coreldove.com stg.thrillring.com; do
    echo "Checking $domain..."
    echo | openssl s_client -connect $domain:443 -servername $domain 2>/dev/null | openssl x509 -noout -dates
    echo ""
done
```

### Troubleshooting SSL Issues

#### Issue 1: Certificate Not Generating

**Symptoms**: Browser shows "Not Secure" or certificate error after 5 minutes

**Causes and Solutions**:

1. **DNS Not Resolving**
   ```bash
   # Check DNS
   nslookup stg.bizoholic.com
   # Should return: 194.238.16.237

   # Solution: Wait for DNS propagation or fix DNS record
   ```

2. **Port 80 Not Accessible**
   ```bash
   # Test port 80
   curl http://stg.bizoholic.com/.well-known/acme-challenge/test

   # Solution: Check firewall allows port 80 inbound
   sudo ufw allow 80/tcp
   ```

3. **Traefik Not Running**
   ```bash
   # Check Traefik
   docker ps | grep traefik

   # Solution: Start Traefik via Dokploy
   ```

4. **Wrong Domain Configuration**
   ```bash
   # Check Traefik labels
   docker inspect bizoholic-frontend-3000 | grep -i host

   # Solution: Verify Host() rule matches actual domain
   ```

#### Issue 2: Certificate Expired

**Symptoms**: Browser shows "Certificate expired" error

**Causes and Solutions**:

1. **Auto-Renewal Failed**
   ```bash
   # Check Traefik logs for renewal errors
   docker logs traefik | grep -i renew

   # Solution: Restart Traefik to force renewal
   docker restart traefik
   ```

2. **Certificate > 90 Days Old**
   ```bash
   # Check certificate age
   echo | openssl s_client -connect stg.bizoholic.com:443 2>/dev/null | openssl x509 -noout -dates

   # Solution: Delete old certificate and request new one
   # Traefik will automatically request new cert on next HTTPS request
   ```

#### Issue 3: Wrong Certificate (Default/Self-Signed)

**Symptoms**: Browser shows certificate is for wrong domain or self-signed

**Causes and Solutions**:

1. **Traefik Using Default Certificate**
   ```bash
   # Check certificate subject
   echo | openssl s_client -connect stg.bizoholic.com:443 2>/dev/null | openssl x509 -noout -subject

   # Solution: Verify Traefik labels include certresolver
   # Should have: traefik.http.routers.NAME.tls.certresolver=letsencrypt
   ```

2. **SNI Not Working**
   ```bash
   # Test with SNI
   curl -v --resolve stg.bizoholic.com:443:194.238.16.237 https://stg.bizoholic.com

   # Solution: Ensure Host() rule matches ServerName
   ```

### Certificate Renewal

#### Automatic Renewal

Let's Encrypt certificates are valid for 90 days. Traefik automatically renews them 30 days before expiration.

**Renewal Process**:
1. Traefik checks certificate expiry daily
2. At 60 days old (30 days before expiry), renewal begins
3. New certificate requested via ACME
4. Old certificate replaced seamlessly
5. No downtime during renewal

**Monitor Renewal**:
```bash
# Check Traefik logs for renewal activity
docker logs traefik | grep -i "renew\|certificate"

# Check certificate expiry date
echo | openssl s_client -connect stg.bizoholic.com:443 2>/dev/null | openssl x509 -noout -enddate
```

#### Manual Renewal (if needed)

```bash
# Option 1: Restart Traefik
docker restart traefik

# Option 2: Restart frontend container
docker restart bizoholic-frontend-3000

# Option 3: Force renewal via Traefik API (if enabled)
curl -X POST http://localhost:8080/api/providers/acme/certificates/renew
```

---

## Traefik Reverse Proxy Configuration

### Traefik Overview

Traefik is the reverse proxy that:
- Routes requests to correct containers based on domain/path
- Handles SSL certificate generation and renewal
- Provides load balancing
- Manages HTTP to HTTPS redirects
- Strips path prefixes for clean routing

### Traefik Labels Explained

Each frontend container has Traefik labels that configure routing:

#### Basic Routing Labels

```yaml
labels:
  # Enable Traefik for this container
  - "traefik.enable=true"

  # Define routing rule (domain-based)
  - "traefik.http.routers.bizoholic-staging-main.rule=Host(`stg.bizoholic.com`)"

  # Enable TLS/HTTPS
  - "traefik.http.routers.bizoholic-staging-main.tls=true"

  # Use Let's Encrypt for certificate
  - "traefik.http.routers.bizoholic-staging-main.tls.certresolver=letsencrypt"
```

#### Path-Based Routing Labels

```yaml
labels:
  # Route specific path to container
  - "traefik.http.routers.portal-staging.rule=Host(`stg.bizoholic.com`) && PathPrefix(`/login`)"

  # Set high priority (evaluated first)
  - "traefik.http.routers.portal-staging.priority=10"

  # Apply middleware to strip /login from path
  - "traefik.http.routers.portal-staging.middlewares=portal-staging-stripprefix"

  # Define the middleware
  - "traefik.http.middlewares.portal-staging-stripprefix.stripprefix.prefixes=/login"

  # Enable TLS
  - "traefik.http.routers.portal-staging.tls=true"
  - "traefik.http.routers.portal-staging.tls.certresolver=letsencrypt"
```

#### Main Site Exclusion Labels

```yaml
labels:
  # Route all paths EXCEPT /login and /admin
  - "traefik.http.routers.bizoholic-staging-main.rule=Host(`stg.bizoholic.com`) && !PathPrefix(`/login`) && !PathPrefix(`/admin`)"

  # Set low priority (evaluated last)
  - "traefik.http.routers.bizoholic-staging-main.priority=1"
```

### Routing Priority System

Traefik evaluates routes in priority order (highest first):

| Priority | Route | Target |
|----------|-------|--------|
| 10 | `Host(stg.bizoholic.com) && PathPrefix(/login)` | Client Portal |
| 10 | `Host(stg.bizoholic.com) && PathPrefix(/admin)` | Admin Dashboard |
| 1 | `Host(stg.bizoholic.com) && !PathPrefix(/login) && !PathPrefix(/admin)` | Main Site |

**Why Priority Matters**:
- Without priority, routes are evaluated in random order
- Could result in main site capturing /login and /admin requests
- High priority ensures specific paths are matched first
- Catch-all route has lowest priority

### Middleware: Path Prefix Stripping

**Problem**: User visits `https://stg.bizoholic.com/login/dashboard`

**Without StripPrefix**:
- Request forwarded to container as `/login/dashboard`
- Container expects `/dashboard`
- Result: 404 error

**With StripPrefix**:
- Middleware strips `/login` from path
- Request forwarded as `/dashboard`
- Container handles request correctly
- Result: Page loads successfully

**Configuration**:
```yaml
# Define middleware
- "traefik.http.middlewares.portal-staging-stripprefix.stripprefix.prefixes=/login"

# Apply middleware to router
- "traefik.http.routers.portal-staging.middlewares=portal-staging-stripprefix"
```

### Traefik Debugging

#### View Active Routers

```bash
# If Traefik API enabled
curl http://localhost:8080/api/http/routers | jq

# View specific router
curl http://localhost:8080/api/http/routers/portal-staging | jq
```

#### Check Traefik Logs

```bash
# View all Traefik logs
docker logs traefik

# Filter for specific domain
docker logs traefik | grep bizoholic

# Filter for routing decisions
docker logs traefik | grep -i "route\|router"

# Filter for SSL/ACME
docker logs traefik | grep -i "acme\|certificate"

# Follow logs in real-time
docker logs -f traefik
```

#### Test Routing

```bash
# Test routing with Host header
curl -H "Host: stg.bizoholic.com" http://194.238.16.237/

# Test path-based routing
curl -H "Host: stg.bizoholic.com" http://194.238.16.237/login/

# Test with HTTPS
curl -v https://stg.bizoholic.com/login/
```

---

## Path-Based Routing

### Understanding Path-Based Routing

Path-based routing allows multiple applications to coexist on a single domain:

```
stg.bizoholic.com/           → Marketing Site (bizoholic-frontend)
stg.bizoholic.com/login/     → Client Portal (client-portal)
stg.bizoholic.com/admin/     → Admin Dashboard (admin-dashboard)
```

### Configuration Example

#### Client Portal (/login/)

```yaml
client-portal:
  # ... other config ...
  labels:
    - "traefik.enable=true"
    # Match requests to /login and all sub-paths
    - "traefik.http.routers.portal-staging.rule=Host(`stg.bizoholic.com`) && PathPrefix(`/login`)"
    # High priority to match before main site
    - "traefik.http.routers.portal-staging.priority=10"
    # Strip /login so app receives clean path
    - "traefik.http.routers.portal-staging.middlewares=portal-staging-stripprefix"
    - "traefik.http.middlewares.portal-staging-stripprefix.stripprefix.prefixes=/login"
    # Enable HTTPS
    - "traefik.http.routers.portal-staging.tls=true"
    - "traefik.http.routers.portal-staging.tls.certresolver=letsencrypt"
```

#### Admin Dashboard (/admin/)

```yaml
admin-dashboard:
  # ... other config ...
  labels:
    - "traefik.enable=true"
    # Match requests to /admin and all sub-paths
    - "traefik.http.routers.admin-staging.rule=Host(`stg.bizoholic.com`) && PathPrefix(`/admin`)"
    # High priority to match before main site
    - "traefik.http.routers.admin-staging.priority=10"
    # Strip /admin so app receives clean path
    - "traefik.http.routers.admin-staging.middlewares=admin-staging-stripprefix"
    - "traefik.http.middlewares.admin-staging-stripprefix.stripprefix.prefixes=/admin"
    # Enable HTTPS
    - "traefik.http.routers.admin-staging.tls=true"
    - "traefik.http.routers.admin-staging.tls.certresolver=letsencrypt"
```

#### Main Marketing Site (catch-all)

```yaml
bizoholic-frontend:
  # ... other config ...
  labels:
    - "traefik.enable=true"
    # Match all requests EXCEPT /login and /admin
    - "traefik.http.routers.bizoholic-staging-main.rule=Host(`stg.bizoholic.com`) && !PathPrefix(`/login`) && !PathPrefix(`/admin`)"
    # Low priority so specific paths match first
    - "traefik.http.routers.bizoholic-staging-main.priority=1"
    # Enable HTTPS
    - "traefik.http.routers.bizoholic-staging-main.tls=true"
    - "traefik.http.routers.bizoholic-staging-main.tls.certresolver=letsencrypt"
```

### Request Flow Example

**Scenario 1: User visits https://stg.bizoholic.com/login/dashboard**

1. Request arrives at Traefik
2. Traefik evaluates routes by priority:
   - Priority 10: `/login` route matches ✓
   - Priority 10: `/admin` route doesn't match
   - Priority 1: Main site not evaluated (match already found)
3. StripPrefix middleware removes `/login`
4. Request forwarded to client-portal as `/dashboard`
5. Client portal handles `/dashboard` route
6. Response returned to user

**Scenario 2: User visits https://stg.bizoholic.com/about**

1. Request arrives at Traefik
2. Traefik evaluates routes by priority:
   - Priority 10: `/login` route doesn't match
   - Priority 10: `/admin` route doesn't match
   - Priority 1: Main site matches ✓
3. No middleware applied
4. Request forwarded to bizoholic-frontend as `/about`
5. Marketing site handles `/about` route
6. Response returned to user

### Testing Path-Based Routing

```bash
# Test main site
curl -I https://stg.bizoholic.com/
# Should: 200 OK, marketing content

# Test client portal
curl -I https://stg.bizoholic.com/login/
# Should: 200 OK, portal login page

# Test admin dashboard
curl -I https://stg.bizoholic.com/admin/
# Should: 200 OK, admin login page

# Test sub-paths
curl -I https://stg.bizoholic.com/login/dashboard
# Should: 200 OK, portal dashboard

curl -I https://stg.bizoholic.com/admin/users
# Should: 200 OK, admin users page

# Verify prefix stripping (check response headers/content)
curl -v https://stg.bizoholic.com/login/ 2>&1 | grep -i location
# Should NOT redirect to /login/login
```

---

## Domain Testing

### Pre-Deployment Testing

```bash
# 1. DNS Resolution
nslookup stg.bizoholic.com
nslookup stg.coreldove.com
nslookup stg.thrillring.com

# 2. DNS Propagation
dig @8.8.8.8 stg.bizoholic.com +short
dig @1.1.1.1 stg.bizoholic.com +short

# 3. Port Accessibility
telnet 194.238.16.237 80
telnet 194.238.16.237 443

# 4. HTTP Accessibility
curl -I http://194.238.16.237
```

### Post-Deployment Testing

```bash
# 1. HTTPS Accessibility
curl -I https://stg.bizoholic.com
curl -I https://stg.coreldove.com
curl -I https://stg.thrillring.com

# 2. Path-Based Routes
curl -I https://stg.bizoholic.com/login/
curl -I https://stg.bizoholic.com/admin/

# 3. SSL Certificates
echo | openssl s_client -connect stg.bizoholic.com:443 -servername stg.bizoholic.com 2>/dev/null | openssl x509 -noout -dates

# 4. HTTP to HTTPS Redirect
curl -I http://stg.bizoholic.com

# 5. Content Verification
curl -s https://stg.bizoholic.com | grep -o "<title>.*</title>"
```

### Browser Testing

1. **Chrome/Edge**:
   - Visit https://stg.bizoholic.com
   - Press F12 → Network tab
   - Verify:
     - Status: 200
     - Protocol: h2 (HTTP/2)
     - Scheme: https
     - No mixed content warnings

2. **Firefox**:
   - Visit https://stg.bizoholic.com
   - Press F12 → Network tab
   - Click lock icon → Connection secure
   - Verify certificate details

3. **Safari** (if available):
   - Visit https://stg.bizoholic.com
   - Safari → Preferences → Advanced → Show Develop menu
   - Develop → Show Web Inspector
   - Verify HTTPS and certificate

### Automated Testing

```bash
# Run verification script
./verify-frontend-deployment.sh

# Expected output:
# ✓ DNS Resolution
# ✓ HTTPS Accessibility
# ✓ SSL Certificates
# ✓ Path-Based Routing
# ✓ Backend Connectivity
```

---

## Troubleshooting

### Common Issues and Solutions

#### DNS Not Resolving

**Symptoms**:
```bash
nslookup stg.bizoholic.com
# Server can't find stg.bizoholic.com: NXDOMAIN
```

**Solutions**:
1. Verify DNS record exists in provider dashboard
2. Wait for propagation (5-30 minutes)
3. Clear local DNS cache:
   ```bash
   # Linux
   sudo systemctl restart systemd-resolved

   # macOS
   sudo dscacheutil -flushcache

   # Windows
   ipconfig /flushdns
   ```
4. Test with external DNS:
   ```bash
   dig @8.8.8.8 stg.bizoholic.com +short
   ```

#### SSL Certificate Not Generating

**Symptoms**: Browser shows "Not Secure" after 5 minutes

**Solutions**:
1. Verify DNS resolves to correct IP
2. Check port 80 accessible:
   ```bash
   curl http://stg.bizoholic.com/.well-known/acme-challenge/test
   ```
3. Check Traefik logs:
   ```bash
   docker logs traefik | grep -i acme
   ```
4. Verify Traefik labels correct
5. Restart Traefik:
   ```bash
   docker restart traefik
   ```
6. Wait 2 minutes and retry

#### Path Routing Not Working

**Symptoms**: /login or /admin returns 404 or shows main site

**Solutions**:
1. Verify router priority:
   ```bash
   docker inspect bizosaas-client-portal-3001 | grep priority
   # Should show: priority=10
   ```
2. Check StripPrefix middleware:
   ```bash
   docker inspect bizosaas-client-portal-3001 | grep stripprefix
   ```
3. Test routing directly:
   ```bash
   curl -v https://stg.bizoholic.com/login/
   ```
4. Check Traefik logs:
   ```bash
   docker logs traefik | grep "login\|admin"
   ```

#### Domain Shows Wrong Application

**Symptoms**: stg.bizoholic.com shows portal instead of marketing site

**Solutions**:
1. Verify Host() rules:
   ```bash
   docker inspect bizoholic-frontend-3000 | grep -i "Host"
   ```
2. Check priority values (higher = first match)
3. Verify exclusion rules on main site:
   ```bash
   # Should have: !PathPrefix(`/login`) && !PathPrefix(`/admin`)
   ```
4. Restart affected containers

---

## Summary

### Quick Setup Checklist

- [ ] DNS A records created for all 3 domains
- [ ] DNS propagation verified (nslookup returns 194.238.16.237)
- [ ] Ports 80 and 443 accessible on VPS
- [ ] Containers deployed with correct Traefik labels
- [ ] HTTPS accessible for all domains
- [ ] SSL certificates valid (check browser lock icon)
- [ ] Path-based routing working (/login and /admin)
- [ ] All domains tested in browser

### Key Takeaways

1. **DNS First**: Always configure DNS before deployment
2. **Wait for SSL**: First HTTPS request triggers certificate generation (1-2 min)
3. **Priority Matters**: Path-based routes need priority=10
4. **StripPrefix Essential**: Required for clean URLs in path-based routing
5. **Test Thoroughly**: Verify each domain and path combination

### Support

For issues not covered here, refer to:
- Main deployment guide: `PHASE3_FRONTEND_DEPLOYMENT.md`
- Quick reference: `PHASE3_QUICK_REFERENCE.md`
- Troubleshooting guide: `frontend-troubleshooting.md`

---

**Domain Configuration Guide Complete**

**Last Updated**: October 10, 2025
**Version**: 1.0.0
