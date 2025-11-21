# MinIO Deployment - Recommendations & Decisions

**Date:** November 4, 2025
**Status:** 🎯 DECISION DOCUMENT
**Purpose:** Answer key deployment questions for MinIO

---

## 🤔 KEY QUESTIONS & ANSWERS

### Question 1: Use Dokploy Template or Manual Configuration?

**✅ RECOMMENDATION: Use Dokploy Template (If Available)**

**Reasons:**
1. **Pre-configured & tested** by Dokploy team
2. **Automatic updates** when template is updated
3. **Best practices** built-in
4. **Faster deployment** (one-click)
5. **Community support** for common issues

**How to Check if Template Exists:**
```bash
# In Dokploy UI:
1. Go to: Projects → infrastructure-services
2. Click: "Create Service"
3. Look for: "Templates" tab
4. Search: "MinIO"
```

**If Template Exists:**
- Use it directly
- Customize environment variables as needed
- Add Traefik labels for custom domains

**If Template NOT Available:**
- Use manual Docker Compose configuration (I've provided)
- Follow MINIO_DEPLOYMENT_CONFIG.md

---

### Question 2: Domain Structure - Subdomain vs Path-Based?

#### Option A: Subdomain (✅ RECOMMENDED)

```
MinIO Console: https://minio.stg.bizoholic.com
S3 API: https://s3.stg.bizoholic.com
```

**Advantages:**
- ✅ **S3-compatible** - Standard S3 clients expect subdomain format
- ✅ **SSL/TLS easier** - Each subdomain gets own certificate
- ✅ **No path conflicts** - Separate routing, no overlap
- ✅ **Better caching** - CDN can cache differently per subdomain
- ✅ **Industry standard** - AWS uses `s3.amazonaws.com`, `s3.us-east-1.amazonaws.com`
- ✅ **CORS friendly** - Easier cross-origin resource sharing
- ✅ **Traefik simpler** - Clean Host() rules

**Traefik Configuration:**
```yaml
# Clean and simple
traefik.http.routers.minio-api.rule=Host(`s3.stg.bizoholic.com`)
traefik.http.routers.minio-console.rule=Host(`minio.stg.bizoholic.com`)
```

#### Option B: Path-Based (❌ NOT RECOMMENDED)

```
MinIO Console: https://stg.bizoholic.com/minio
S3 API: https://stg.bizoholic.com/s3
```

**Disadvantages:**
- ❌ **S3 incompatibility** - Many S3 clients won't work
- ❌ **Path stripping needed** - Complex Traefik middleware
- ❌ **URL conflicts** - Could interfere with frontend routes
- ❌ **CORS issues** - Same origin complicates security
- ❌ **Not standard** - No major cloud provider uses paths

**Traefik Configuration (Complex):**
```yaml
# Requires path stripping middleware
traefik.http.routers.minio-api.rule=Host(`stg.bizoholic.com`) && PathPrefix(`/s3`)
traefik.http.middlewares.minio-strip.stripprefix.prefixes=/s3
traefik.http.routers.minio-api.middlewares=minio-strip
```

**DECISION: ✅ Use Subdomain Approach**

---

### Question 3: Storage Backend - VPS vs Cloud Storage?

#### Current Situation Analysis

**Available Storage:**
- VPS (KVM4 - 72.60.219.244): ~200GB SSD
- OneDrive: External cloud storage
- Google Drive: External cloud storage
- AWS S3: External S3 service (requires account)

#### Option A: VPS Local Storage (✅ RECOMMENDED FOR STAGING)

**Configuration:**
```yaml
Volumes:
  - /mnt/minio-data:/data (persistent bind mount)

Storage Path: /mnt/minio-data
Expected Size: 10-50GB (for staging)
```

**Advantages for Staging:**
- ✅ **No external costs** - Free with VPS
- ✅ **Fast access** - Local disk, low latency
- ✅ **Simple setup** - No API keys or credentials
- ✅ **Full control** - No rate limits, no quotas
- ✅ **Private** - Data stays on your infrastructure
- ✅ **Good for development** - Quick iteration

**Disadvantages:**
- ⚠️ **Limited space** - VPS disk size constraint (~200GB total)
- ⚠️ **Single point of failure** - No geographic redundancy
- ⚠️ **Backup responsibility** - Must implement own backups
- ⚠️ **No CDN** - Slower for global users

**Best For:**
- Staging environment ✅
- Small to medium file volumes
- Non-critical data
- Quick prototyping

#### Option B: MinIO Gateway to Cloud Storage (⚠️ COMPLEX)

**Configuration:**
```yaml
# MinIO as gateway to external storage
Command: gateway s3 https://s3.amazonaws.com
Environment:
  MINIO_ACCESS_KEY: <aws-access-key>
  MINIO_SECRET_KEY: <aws-secret-key>
```

**Advantages:**
- ✅ **Unlimited storage** - Cloud storage scales
- ✅ **Geographic redundancy** - Multi-region
- ✅ **CDN integration** - CloudFront, CloudFlare
- ✅ **Managed backups** - Provider handles it

**Disadvantages:**
- ❌ **Additional costs** - Pay for storage + API calls
- ❌ **Requires accounts** - AWS/Azure/GCP setup
- ❌ **Network latency** - External API calls
- ❌ **Complexity** - Multiple systems to manage
- ❌ **Vendor lock-in** - Dependent on cloud provider

**Best For:**
- Production environment with high traffic
- Large file volumes (>500GB)
- Geographic distribution needs
- Mission-critical data

#### Option C: Hybrid Approach (🎯 PRODUCTION RECOMMENDATION)

**Configuration:**
```yaml
MinIO on VPS (Primary):
  - Fast local caching
  - Immediate uploads
  - Quick access

S3 Backend (Backup):
  - Automatic replication
  - Long-term storage
  - Disaster recovery
```

**Implementation:**
```bash
# MinIO with automatic S3 replication
mc admin bucket remote add minio-local/coreldove-products \
  https://s3.amazonaws.com/backup-bucket \
  --access-key <key> --secret-key <secret>

mc admin replicate add minio-local/coreldove-products \
  --remote-bucket backup-bucket --replicate "delete,metadata"
```

**Best For:**
- Production environment
- Critical data
- Cost-effective scalability

**DECISION: ✅ Use VPS Local Storage for Staging**

**Rationale:**
1. Staging environment (not production)
2. Cost-effective (no cloud storage fees)
3. Simple setup and management
4. Sufficient for current needs (<50GB expected)
5. Can migrate to hybrid later if needed

---

## 📋 IMPLEMENTATION CHECKLIST

### Step 1: DNS Configuration (Cloudflare)

```bash
# Add these A records in Cloudflare:

Record 1:
  Type: A
  Name: s3
  Domain: stg.bizoholic.com
  Value: 72.60.219.244
  Proxy: Enabled (Orange cloud)
  TTL: Auto

Record 2:
  Type: A
  Name: minio
  Domain: stg.bizoholic.com
  Value: 72.60.219.244
  Proxy: Enabled (Orange cloud)
  TTL: Auto
```

**Verify DNS:**
```bash
nslookup s3.stg.bizoholic.com
nslookup minio.stg.bizoholic.com
# Both should resolve to 72.60.219.244 (via Cloudflare)
```

---

### Step 2: Prepare VPS Storage

```bash
# SSH to KVM4
ssh root@72.60.219.244

# Create MinIO data directory
sudo mkdir -p /mnt/minio-data
sudo chown -R 1000:1000 /mnt/minio-data
sudo chmod 755 /mnt/minio-data

# Check available disk space
df -h /mnt
# Should have at least 50GB free

# Verify permissions
ls -la /mnt/minio-data
# Should show: drwxr-xr-x 1000 1000
```

---

### Step 3: Deploy via Dokploy

#### Option A: Using Dokploy Template (Preferred)

```
1. In Dokploy UI:
   - Go to: infrastructure-services project
   - Click: "Create Service" → "Templates"
   - Search: "MinIO"
   - Select: MinIO template
   - Click: "Deploy Template"

2. Customize Configuration:
   - Service Name: minio-storage
   - Environment Variables: (see below)
   - Volumes: /mnt/minio-data:/data
   - Deploy
```

#### Option B: Manual Docker Compose

If template not available, create service with:

```yaml
version: '3.8'

services:
  minio:
    image: minio/minio:RELEASE.2024-10-29T16-01-48Z
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: bizosaas_admin
      MINIO_ROOT_PASSWORD: BizOSaaS2025@MinIO!Secure
      MINIO_BROWSER_REDIRECT_URL: https://minio.stg.bizoholic.com
      MINIO_SERVER_URL: https://s3.stg.bizoholic.com
    volumes:
      - /mnt/minio-data:/data
    ports:
      - "9000:9000"
      - "9001:9001"
    networks:
      - dokploy-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3
      start_period: 10s
    deploy:
      replicas: 1
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 256M
      labels:
        # S3 API
        - "traefik.enable=true"
        - "traefik.http.routers.minio-api.rule=Host(`s3.stg.bizoholic.com`)"
        - "traefik.http.routers.minio-api.entrypoints=websecure"
        - "traefik.http.routers.minio-api.tls=true"
        - "traefik.http.routers.minio-api.tls.certresolver=letsencrypt"
        - "traefik.http.routers.minio-api.service=minio-api"
        - "traefik.http.services.minio-api.loadbalancer.server.port=9000"

        # Console
        - "traefik.http.routers.minio-console.rule=Host(`minio.stg.bizoholic.com`)"
        - "traefik.http.routers.minio-console.entrypoints=websecure"
        - "traefik.http.routers.minio-console.tls=true"
        - "traefik.http.routers.minio-console.tls.certresolver=letsencrypt"
        - "traefik.http.routers.minio-console.service=minio-console"
        - "traefik.http.services.minio-console.loadbalancer.server.port=9001"

networks:
  dokploy-network:
    external: true
```

---

### Step 4: Required Information for Deployment

**Environment Variables (REQUIRED):**
```bash
MINIO_ROOT_USER=bizosaas_admin
MINIO_ROOT_PASSWORD=BizOSaaS2025@MinIO!Secure
MINIO_BROWSER_REDIRECT_URL=https://minio.stg.bizoholic.com
MINIO_SERVER_URL=https://s3.stg.bizoholic.com
```

**Ports (REQUIRED):**
```
9000 - S3 API (internal)
9001 - Web Console (internal)
```

**Volumes (REQUIRED):**
```
Source: /mnt/minio-data (on host)
Target: /data (in container)
Type: Bind Mount
```

**Network (REQUIRED):**
```
dokploy-network
```

**Traefik Labels (REQUIRED):**
```yaml
# Copy from docker-compose above
# Or configure in Dokploy UI under "Advanced" → "Labels"
```

**Resource Limits (RECOMMENDED):**
```yaml
Memory:
  Reservation: 256MB
  Limit: 1GB

CPU:
  Reservation: 0.25
  Limit: 1.0
```

---

### Step 5: Post-Deployment Configuration

**Access Console:**
```
URL: https://minio.stg.bizoholic.com
Username: bizosaas_admin
Password: BizOSaaS2025@MinIO!Secure
```

**Create Buckets (via Console or CLI):**
```bash
# Option 1: Via Web Console
1. Login to https://minio.stg.bizoholic.com
2. Go to "Buckets" → "Create Bucket"
3. Create each bucket with appropriate policies

# Option 2: Via CLI (mc - MinIO Client)
# Install mc: https://min.io/docs/minio/linux/reference/minio-mc.html
mc alias set bizosaas https://s3.stg.bizoholic.com bizosaas_admin 'BizOSaaS2025@MinIO!Secure'

# Create buckets
mc mb bizosaas/coreldove-products
mc mb bizosaas/bizoholic-media
mc mb bizosaas/thrillring-assets
mc mb bizosaas/shared-documents
mc mb bizosaas/user-uploads
mc mb bizosaas/backups
mc mb bizosaas/temp-uploads

# Set public read policy for product images
mc anonymous set download bizosaas/coreldove-products
mc anonymous set download bizosaas/bizoholic-media
mc anonymous set download bizosaas/thrillring-assets
```

**Create Service Accounts:**
```bash
# Via Console:
1. Go to "Identity" → "Service Accounts"
2. Create: "brain-gateway-service"
3. Assign policies: Read/Write to all public buckets
4. Save credentials

# Via CLI:
mc admin user add bizosaas braingateway_access_2025 'BrainGateway@MinIO!Secret2025'
mc admin policy set bizosaas readwrite user=braingateway_access_2025
```

---

## 🎯 FINAL RECOMMENDATIONS SUMMARY

### Infrastructure Decisions

| Question | Recommendation | Rationale |
|----------|---------------|-----------|
| **Template vs Manual** | ✅ Use Dokploy Template (if available) | Faster, pre-tested, best practices |
| **Domain Structure** | ✅ Subdomain (`s3.stg.bizoholic.com`) | S3-compatible, standard, simpler |
| **Storage Backend** | ✅ VPS Local Storage | Cost-effective for staging, sufficient space |
| **Backup Strategy** | ⏳ Manual backups initially | Implement automated backups later |

### DNS Setup

```
✅ s3.stg.bizoholic.com → 72.60.219.244 (A record, proxied)
✅ minio.stg.bizoholic.com → 72.60.219.244 (A record, proxied)
```

### Storage Path

```
✅ /mnt/minio-data (on VPS)
```

### Access URLs

```
✅ S3 API: https://s3.stg.bizoholic.com
✅ Console: https://minio.stg.bizoholic.com
```

---

## 📊 SPACE PLANNING

### Expected Storage Usage (Staging)

```
coreldove-products:     5-10 GB   (product images)
bizoholic-media:        2-5 GB    (marketing assets)
thrillring-assets:      3-7 GB    (game assets)
shared-documents:       1-3 GB    (PDFs, reports)
user-uploads:           2-5 GB    (user content)
backups:                5-10 GB   (database backups)
temp-uploads:           0.5-1 GB  (temporary files)

TOTAL ESTIMATED:        18-41 GB  (well within 200GB VPS capacity)
```

**Monitoring:**
```bash
# Check MinIO disk usage
mc admin info bizosaas

# Check VPS disk usage
df -h /mnt/minio-data
```

---

## ⚠️ MIGRATION TO PRODUCTION

When moving to production, consider:

1. **Upgrade to Cloud Storage Backend**
   - AWS S3, Google Cloud Storage, or Azure Blob
   - Better redundancy and scalability
   - CDN integration

2. **Implement Automatic Backups**
   - MinIO to S3 replication
   - Scheduled snapshots
   - Off-site backup copies

3. **Add Monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - Alert on disk usage >80%

4. **Enable Encryption**
   - Server-side encryption (SSE)
   - TLS for all connections
   - KMS integration

---

**Document Status:** DECISION COMPLETE
**Next Action:** Add DNS records and deploy MinIO
**Estimated Time:** 45-60 minutes total
**Last Updated:** November 4, 2025
