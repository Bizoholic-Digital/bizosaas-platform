# MinIO Object Storage - Deployment Configuration

**Date:** November 4, 2025
**Status:** 🚀 READY FOR DEPLOYMENT
**Service:** MinIO S3-Compatible Object Storage
**Project:** infrastructure-services

---

## 📋 DEPLOYMENT SPECIFICATION

### Service Configuration

```yaml
Project: infrastructure-services
Service Name: minio-storage
Service Type: Application (Docker Compose or Stack)
Image: minio/minio:RELEASE.2024-10-29T16-01-48Z
Replicas: 1

Command:
  server /data --console-address ":9001"

Ports:
  - 9000:9000  # S3 API
  - 9001:9001  # Web Console

Environment Variables:
  MINIO_ROOT_USER: bizosaas_admin
  MINIO_ROOT_PASSWORD: BizOSaaS2025@MinIO!Secure
  MINIO_BROWSER_REDIRECT_URL: https://minio.stg.bizoholic.com
  MINIO_SERVER_URL: https://s3.stg.bizoholic.com

Volumes:
  - Type: Named Volume or Bind Mount
  - Source: minio-data (or /mnt/minio-data)
  - Target: /data
  - Persistent: YES (CRITICAL)

Network:
  - dokploy-network

Health Check:
  - Test: curl -f http://localhost:9000/minio/health/live || exit 1
  - Interval: 30s
  - Timeout: 20s
  - Retries: 3
  - Start Period: 10s

Labels (Traefik):
  # S3 API endpoint
  traefik.enable: "true"
  traefik.http.routers.minio-api.rule: Host(`s3.stg.bizoholic.com`)
  traefik.http.routers.minio-api.entrypoints: websecure
  traefik.http.routers.minio-api.tls: "true"
  traefik.http.routers.minio-api.tls.certresolver: letsencrypt
  traefik.http.routers.minio-api.service: minio-api
  traefik.http.services.minio-api.loadbalancer.server.port: "9000"

  # Console endpoint
  traefik.http.routers.minio-console.rule: Host(`minio.stg.bizoholic.com`)
  traefik.http.routers.minio-console.entrypoints: websecure
  traefik.http.routers.minio-console.tls: "true"
  traefik.http.routers.minio-console.tls.certresolver: letsencrypt
  traefik.http.routers.minio-console.service: minio-console
  traefik.http.services.minio-console.loadbalancer.server.port: "9001"

Resource Limits:
  Memory Reservation: 256MB
  Memory Limit: 1GB
  CPU Reservation: 0.25
  CPU Limit: 1.0
```

---

## 🌐 DNS CONFIGURATION

### Required DNS Records (Cloudflare)

Add the following A records:

```
Type: A
Name: s3
Domain: stg.bizoholic.com
Value: 72.60.219.244
Proxy: Enabled (Cloudflare Proxied)
TTL: Auto

Type: A
Name: minio
Domain: stg.bizoholic.com
Value: 72.60.219.244
Proxy: Enabled (Cloudflare Proxied)
TTL: Auto
```

**Access URLs After Deployment:**
- **S3 API:** https://s3.stg.bizoholic.com
- **Web Console:** https://minio.stg.bizoholic.com

---

## 📦 BUCKET STRUCTURE

### Buckets to Create

```yaml
Buckets:
  1. bizoholic-media:
      Description: Media files for Bizoholic platform
      Access: Public Read (for marketing assets)
      Versioning: Enabled
      Lifecycle: 90 days retention

  2. coreldove-products:
      Description: Product images and assets for CoreLdove
      Access: Public Read
      Versioning: Enabled
      Lifecycle: No expiration (product catalog)

  3. thrillring-assets:
      Description: Gaming assets for ThrillRing
      Access: Public Read (for game resources)
      Versioning: Enabled
      Lifecycle: 180 days retention

  4. shared-documents:
      Description: Platform-wide documents (PDFs, reports)
      Access: Private (authenticated access only)
      Versioning: Enabled
      Lifecycle: 365 days retention

  5. user-uploads:
      Description: User-generated content uploads
      Access: Private with signed URLs
      Versioning: Enabled
      Lifecycle: 90 days retention

  6. backups:
      Description: Database and application backups
      Access: Private (admin only)
      Versioning: Enabled
      Lifecycle: 30 days retention

  7. temp-uploads:
      Description: Temporary file storage
      Access: Private
      Versioning: Disabled
      Lifecycle: 24 hours auto-delete
```

---

## 🔐 ACCESS CREDENTIALS

### Root Admin Credentials

```
Username: bizosaas_admin
Password: BizOSaaS2025@MinIO!Secure
Console URL: https://minio.stg.bizoholic.com
```

**IMPORTANT:** These are root credentials. Create service accounts for each application.

### Service Accounts to Create

```yaml
Service Accounts:

  1. brain-gateway-service:
      Access Key: braingateway_access_2025
      Secret Key: BrainGateway@MinIO!Secret2025
      Permissions:
        - Read/Write: bizoholic-media, coreldove-products, thrillring-assets
        - Read/Write: shared-documents, user-uploads
        - Read: All buckets (for gateway routing)

  2. saleor-api-service:
      Access Key: saleor_api_access_2025
      Secret Key: SaleorAPI@MinIO!Secret2025
      Permissions:
        - Read/Write: coreldove-products
        - Read: bizoholic-media (for cross-platform assets)

  3. wagtail-cms-service:
      Access Key: wagtail_cms_access_2025
      Secret Key: WagtailCMS@MinIO!Secret2025
      Permissions:
        - Read/Write: bizoholic-media, shared-documents

  4. backup-service:
      Access Key: backup_service_access_2025
      Secret Key: BackupService@MinIO!Secret2025
      Permissions:
        - Read/Write: backups
        - Read: All buckets (for backup purposes)
```

---

## 🔧 BUCKET POLICIES

### Public Read Policy (for product images)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"AWS": "*"},
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::coreldove-products/*"]
    }
  ]
}
```

### Private Bucket Policy (for documents)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam:::user/braingateway_access_2025"},
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": ["arn:aws:s3:::shared-documents/*"]
    }
  ]
}
```

---

## 🌐 BRAIN GATEWAY INTEGRATION

### Add MinIO Routes to Brain Gateway

```python
# backend/brain-gateway/app/routes/storage.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from minio import Minio
from minio.error import S3Error
import os

router = APIRouter(prefix="/api/storage", tags=["storage"])

# MinIO client configuration
minio_client = Minio(
    "infrastructure-minio-storage:9000",
    access_key=os.getenv("MINIO_ACCESS_KEY", "braingateway_access_2025"),
    secret_key=os.getenv("MINIO_SECRET_KEY", "BrainGateway@MinIO!Secret2025"),
    secure=False  # Internal connection, no SSL
)

@router.post("/upload/{bucket_name}")
async def upload_file(bucket_name: str, file: UploadFile = File(...)):
    """
    Upload file to MinIO bucket
    """
    try:
        # Read file content
        content = await file.read()

        # Upload to MinIO
        minio_client.put_object(
            bucket_name=bucket_name,
            object_name=file.filename,
            data=io.BytesIO(content),
            length=len(content),
            content_type=file.content_type
        )

        # Generate public URL for public buckets
        if bucket_name in ["coreldove-products", "bizoholic-media", "thrillring-assets"]:
            url = f"https://s3.stg.bizoholic.com/{bucket_name}/{file.filename}"
        else:
            # Generate presigned URL for private buckets
            url = minio_client.presigned_get_object(bucket_name, file.filename, expires=timedelta(hours=1))

        return {
            "success": True,
            "filename": file.filename,
            "bucket": bucket_name,
            "url": url
        }
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{bucket_name}/{object_name}")
async def download_file(bucket_name: str, object_name: str):
    """
    Get presigned URL for file download
    """
    try:
        url = minio_client.presigned_get_object(
            bucket_name,
            object_name,
            expires=timedelta(hours=1)
        )
        return {"url": url}
    except S3Error as e:
        raise HTTPException(status_code=404, detail="File not found")

@router.delete("/delete/{bucket_name}/{object_name}")
async def delete_file(bucket_name: str, object_name: str):
    """
    Delete file from bucket
    """
    try:
        minio_client.remove_object(bucket_name, object_name)
        return {"success": True, "message": "File deleted"}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 📝 SERVICE ENVIRONMENT VARIABLES

### Add to All Backend Services

```bash
# MinIO Configuration
MINIO_ENDPOINT=infrastructure-minio-storage:9000
MINIO_ACCESS_KEY=<service-specific-access-key>
MINIO_SECRET_KEY=<service-specific-secret-key>
MINIO_USE_SSL=false
MINIO_REGION=us-east-1

# Public URL for file access
MINIO_PUBLIC_URL=https://s3.stg.bizoholic.com
```

### Service-Specific Configuration

**Brain Gateway (Port 8001):**
```bash
MINIO_ACCESS_KEY=braingateway_access_2025
MINIO_SECRET_KEY=BrainGateway@MinIO!Secret2025
```

**Saleor API (Port 8000):**
```bash
MINIO_ACCESS_KEY=saleor_api_access_2025
MINIO_SECRET_KEY=SaleorAPI@MinIO!Secret2025
MINIO_BUCKET=coreldove-products
```

**Wagtail CMS (Port 4000):**
```bash
MINIO_ACCESS_KEY=wagtail_cms_access_2025
MINIO_SECRET_KEY=WagtailCMS@MinIO!Secret2025
MINIO_BUCKET=bizoholic-media
```

---

## 🧪 POST-DEPLOYMENT TESTING

### Test 1: Service Health Check

```bash
# From KVM4 server
curl -I https://s3.stg.bizoholic.com/minio/health/live
# Expected: HTTP/2 200 OK

curl -I https://minio.stg.bizoholic.com
# Expected: HTTP/2 200 OK (Console login page)
```

### Test 2: Console Access

```
1. Open: https://minio.stg.bizoholic.com
2. Login: bizosaas_admin / BizOSaaS2025@MinIO!Secure
3. Verify: Dashboard loads
```

### Test 3: Bucket Creation

```bash
# Using mc (MinIO Client)
mc alias set bizosaas https://s3.stg.bizoholic.com bizosaas_admin BizOSaaS2025@MinIO!Secure
mc mb bizosaas/coreldove-products
mc mb bizosaas/bizoholic-media
mc mb bizosaas/thrillring-assets
mc mb bizosaas/shared-documents
mc mb bizosaas/user-uploads
mc mb bizosaas/backups
mc mb bizosaas/temp-uploads
```

### Test 4: File Upload

```bash
# Create test file
echo "Test upload" > test.txt

# Upload via mc
mc cp test.txt bizosaas/coreldove-products/

# Verify via public URL
curl https://s3.stg.bizoholic.com/coreldove-products/test.txt
# Expected: "Test upload"
```

### Test 5: API Upload via Gateway

```bash
curl -X POST https://stg.bizoholic.com/api/storage/upload/coreldove-products \
  -F "file=@test.jpg" \
  -H "Authorization: Bearer <jwt-token>"

# Expected: {"success": true, "url": "https://s3.stg.bizoholic.com/..."}
```

---

## 📊 MONITORING & MAINTENANCE

### Health Checks

```bash
# Service status
docker service ps infrastructure-minio-storage

# Logs
docker service logs infrastructure-minio-storage --tail 50

# Disk usage
mc admin info bizosaas
```

### Backup Strategy

```bash
# Backup bucket metadata
mc admin config export bizosaas > minio-config-backup.json

# Backup bucket policies
mc admin policy list bizosaas

# Sync buckets to external storage (optional)
mc mirror bizosaas/backups s3-external/minio-backups/
```

### Performance Tuning

```yaml
Environment Variables for Performance:
  MINIO_API_REQUESTS_MAX: 10000
  MINIO_API_REQUESTS_DEADLINE: 10s
  MINIO_CACHE_DRIVES: /cache
  MINIO_CACHE_EXCLUDE: "*.tmp"
  MINIO_CACHE_QUOTA: 80
```

---

## 🔒 SECURITY BEST PRACTICES

1. **Change Root Password After Deployment**
   - Use MinIO console: Security → Change Password
   - Update credentials.md

2. **Enable Bucket Versioning**
   - Protects against accidental deletes
   - Allows rollback to previous versions

3. **Set Up Bucket Lifecycle Rules**
   - Auto-delete old files from temp-uploads (24 hours)
   - Archive old backups (30 days)
   - Transition infrequent data to cheaper storage

4. **Use Service Accounts**
   - Never share root credentials with applications
   - Create separate service accounts per service
   - Rotate keys every 90 days

5. **Enable Audit Logging**
   ```bash
   mc admin config set bizosaas logger_webhook:1 endpoint="https://logs.bizoholic.com/minio"
   ```

6. **Set Up Bucket Encryption**
   - Server-side encryption (SSE-S3)
   - Encrypt sensitive buckets: shared-documents, user-uploads, backups

---

## 📋 DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] DNS records created (s3.stg.bizoholic.com, minio.stg.bizoholic.com)
- [ ] Credentials documented in credentials.md
- [ ] Persistent volume planned (/mnt/minio-data or named volume)
- [ ] Resource limits defined

### Deployment
- [ ] Create service in Dokploy infrastructure-services project
- [ ] Configure environment variables
- [ ] Add Traefik labels for routing
- [ ] Set up persistent volume
- [ ] Deploy service

### Post-Deployment
- [ ] Verify service is running
- [ ] Access web console (https://minio.stg.bizoholic.com)
- [ ] Create buckets
- [ ] Set bucket policies
- [ ] Create service accounts
- [ ] Test file upload/download
- [ ] Update Brain Gateway with MinIO routes
- [ ] Update backend services with MinIO credentials
- [ ] Test integration with Saleor API
- [ ] Test integration with Wagtail CMS
- [ ] Document in credentials.md
- [ ] Update CENTRALIZED_API_GATEWAY_ARCHITECTURE.md

---

## 📄 CREDENTIALS TO ADD

### credentials.md Section

```markdown
## MinIO Object Storage

**Service:** infrastructure-minio-storage
**Status:** ✅ DEPLOYED (November 4, 2025)

**Console Access:**
- URL: https://minio.stg.bizoholic.com
- Username: bizosaas_admin
- Password: BizOSaaS2025@MinIO!Secure

**S3 API Endpoint:**
- URL: https://s3.stg.bizoholic.com
- Region: us-east-1

**Service Accounts:**

1. Brain Gateway:
   - Access Key: braingateway_access_2025
   - Secret Key: BrainGateway@MinIO!Secret2025

2. Saleor API:
   - Access Key: saleor_api_access_2025
   - Secret Key: SaleorAPI@MinIO!Secret2025

3. Wagtail CMS:
   - Access Key: wagtail_cms_access_2025
   - Secret Key: WagtailCMS@MinIO!Secret2025

4. Backup Service:
   - Access Key: backup_service_access_2025
   - Secret Key: BackupService@MinIO!Secret2025

**Buckets:**
- coreldove-products (Public Read)
- bizoholic-media (Public Read)
- thrillring-assets (Public Read)
- shared-documents (Private)
- user-uploads (Private)
- backups (Private)
- temp-uploads (Private, 24h auto-delete)
```

---

**Document Status:** READY FOR DEPLOYMENT
**Next Action:** Create MinIO service in Dokploy
**Estimated Time:** 30-45 minutes
**Last Updated:** November 4, 2025
