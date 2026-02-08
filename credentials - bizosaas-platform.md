## Dokploy Access

Updated dokploy api key - dk4ixNgzxiGcZWrjlvocbOJqTLjlZsJUEgmTJjjXYvLVSwiUBUPARxklyNFyVQRDHBa

1. Admin username/password for Dokploy dashboard at dk.bizoholic.com - bizoholic.digital@gmail.com - 25IKC#1XiKABRo

3. Project access details for:

   * bizoholic-website (WordPress)
   * automation-hub (n8n)

WordPress Access

1. WordPress admin credentials for the bizoholic-website project
2. Database connection details (host, port, database name, username, password)
3. WordPress site URL/domain configuration - www.bizoholic.com
4. FTP/SFTP access or file management method for uploading custom plugins/themes

n8n Access

1. n8n admin credentials for b8d.bizoholic.com - bizoholic.com@gmail.com - EGEw887eU$l$pf
2. Webhook URLs and API keys for n8n workflow triggers -  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjOTNmMDc5My1jOGRjLTQwYjctOTY4MS1jMWRkN2U1MmUxMGEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYxNTU3ODA0fQ.qHD8m6IkJGNA793TFYxP12qR7-wFd4xUbI17zPax7dI

3. Database connection details if n8n has its own database - here is the environment variables setting from the n8n container

N8N\_HOST=automationhub-n8n-91feb0-194-238-16-237.traefik.me
N8N\_PORT=5678
N8N\_PROTOCOL=https
GENERIC\_TIMEZONE=Europe/Berlin
g
DB\_TYPE=postgresdb
DB\_POSTGRESDB\_HOST=postgres
DB\_POSTGRESDB\_PORT=5432
DB\_POSTGRESDB\_DATABASE=n8ndb
DB\_POSTGRESDB\_USER=n8n
DB\_POSTGRESDB\_PASSWORD=n8npass

N8N\_BASIC\_AUTH\_ACTIVE=false
WEBHOOK\_URL=https://automationhub-n8n-91feb0-194-238-16-237.traefik.me/

Database Access

1. PostgreSQL connection details for the shared database:

   * Host, port, database name
   * Username and password
   * Schema information

# Shared Database Infrastructure Environment Variables

# For Dokploy Deployment

# PostgreSQL Configuration

POSTGRES\_PASSWORD=SharedInfra2024!SuperSecure
POSTGRES\_DB=postgres
POSTGRES\_USER=postgres

# pgAdmin Configuration

PGADMIN\_EMAIL=admin@coreldove.com
PGADMIN\_PASSWORD=SharedPgAdmin2024!Secure

# Project Database Passwords (used in init scripts)

CORELDOVE\_DB\_PASSWORD=CorelDove2024!Secure
BIZOHOLIC\_DB\_PASSWORD=BizoHolic2024!Secure
THRILLRING\_DB\_PASSWORD=ThrillRing2024!Secure
ANALYTICS\_DB\_PASSWORD=SharedAnalytics2024!
READONLY\_DB\_PASSWORD=ReadOnly2024!Reports

# Backup Configuration

BACKUP\_RETENTION\_DAYS=30
BACKUP\_S3\_BUCKET=shared-infrastructure-backups

# Network Configuration

DOKPLOY\_NETWORK=dokploy-network

# Domain Configuration

PGADMIN\_DOMAIN=pgadmin.bizoholic.com
POSTGRES\_HOST=postgres

2. Dragonfly/Redis connection details

DRAGONFLY\_PASSWORD=SharedDragonfly2024!Secure

External API Keys

1. OpenRouter API key (for CrewAI LLM access) - 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
2. Marketing platform API keys (Google Ads, Facebook, LinkedIn)
3. Email service API keys (SendGrid, Mailchimp)

## GitHub/Git Access

1. GitHub credentials to create the repository
2. SSH keys or personal access tokens for Git operations

### GitHub GHCR Push Access
- **Personal Access Token**: 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 (BizOSaaS GHCR Push Access)  // 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
- **Username**: alagiri.rajesh@gmail.com
- **Password**: R!bmaM8E&FZh9m
- **Repository**: https://github.com/Bizoholic-Digital/bizosaas-platform

## SuperAdmin Credentials

* Login with:

  * Username: superadmin
  * Password: BizoSaaS2025!Admin

## Admin Credentials

* Login with:

  * Username: administrator
  * Password: Bizoholic2025!Admin

## User Credentials

* Login with:

  * Username: bizoholic\_user
  * Password: Bizoholic2025!User

## Hostinger

### KVM2 - 194.238.16.237

bizosaas api token - p1b5Jqk80lZnTJw74dVMPV6SUjRYQu2tPGR4eJ7ifcd06412
curl -X GET "https://developers.hostinger.com/api/vps/v1/virtual-machines" \
-H "Authorization: Bearer p1b5Jqk80lZnTJw74dVMPV6SUjRYQu2tPGR4eJ7ifcd06412" \
-H "Content-Type: application/json"

Root Access - ssh root@194.238.16.237
Password - &k3civYG5Q6YPb
Hostinger API token - xki5zwT4cvMXVY7OzqfJV8p1q77icPqGcf4G8PDN3abc2a2d
test your of the token with output - alagiri@ROG-Strix:~$ curl -X GET "https://developers.hostinger.com/api/vps/v1/virtual-machines"  
-H "Authorization: Bearer xki5zwT4cvMXVY7OzqfJV8p1q77icPqGcf4G8PDN3abc2a2d"  
-H "Content-Type: application/json"
\[{"id":894670,"firewall\_group\_id":null,"subscription\_id":"AzqiNQUpxs6rnw87","plan":"KVM 2","hostname":"srv894670.hstgr.cloud","state":"running","actions\_lock":"unlocked","cpus":2,"memory":8192,"disk":102400,"bandwidth":8192000,"ns1":"217.21.86.10","ns2":"1.1.1.1","ipv4":\[{"id":162899,"address":"194.238.16.237","ptr":"srv894670.hstgr.cloud"}],"ipv6":\[{"id":1339922,"address":"2a02:4780:12:9f00::1","ptr":"srv894670.hstgr.cloud"}],"template":{"id":1092,"name":"Ubuntu 24.04 with Dokploy","description":"Dokploy is a platform designed to streamline application deployment and management across various environments. It automates key DevOps tasks such as deployments and scaling, integrates with existing CI/CD pipelines, and supports multiple programming languages and frameworks. With its user-friendly interface, Dokploy helps teams enhance efficiency and maintain application performance effectively.","documentation":"https://docs.dokploy.com/docs/core"},"created\_at":"2025-07-04T07:35:42Z"}]alagiri@ROG-Strix:~$

## Telegram Bots

t.me/jonnyaibot - 7200437482:AAF8aE2uymF5ukm-ntlEnXx1hfhX1Obcfaw
t.me/BizoholicAIBot - 7767279872:AAGxwC7AcjSpkdF3xdvuLAw1gfXAplYLhMw
t.me/Deals4all\_bot - 1217910149:AAHZwP0RnxcaqMheU08so6hpyXL7H8tZfYw
t.me/BottraderAdmin\_bot - 7780097136:AAELAgYZsfmBCTuYxwHvqoITqwVjKZp-u0Y
t.me/go\_go\_fatherbot - 1011283832:AAHtpTljpQFhypOaQJwWei4z4Y5hgoMNSmk

## sellercentral.amazon.in login

* User - wahie.reema@outlook.com
* Password - QrDM474ckcbG87

### Github Token

Github personal access token - bizosaas - ghp\_SHGFTTTygl0XQaJhvNU1dUfNHkgtj03ntOAO

Github User Name - alagiri.rajesh@gmail.com
Github Password - R!bmaM8E\&FZh9m

#### Github Token With GHCR

Github personal access token - BizOSaaS GHCR Push Access - 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
Github User Name - alagiri.rajesh@gmail.com
Github Password - R!bmaM8E\&FZh9m

## API Keys

### AI Service Keys
OPENAI_API_KEY=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
OPENROUTER_API_KEY=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
GOOGLE_GEMINI_KEY=AIzaSyAYDIx5BI6DNLcMqwoyU8NUiytdBlwbYOE
ANTHROPIC_API_KEY=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
MOONSHOT_API_KEY=sk-MvKbgOXFKGjRDF1wCYSVz3zwEAIyHVTMaNrsdJDqYlGfTX99

### Payment Gateway Keys
STRIPE_SECRET_KEY=sk_test_key
PAYPAL_CLIENT_ID=sandbox_id
PAYPAL_CLIENT_SECRET=sandbox_secret

### Amazon API Keys
AMAZON_ACCESS_KEY=staging_key
AMAZON_SECRET_KEY=staging_key

### Django Secret Keys
DJANGO_SECRET_KEY=staging-secret
DJANGO_CRM_SECRET_KEY=staging-crm-secret
SALEOR_SECRET_KEY=staging-saleor-secret
JWT_SECRET=staging-secret

### Trading API Keys (Staging/Sandbox)
ALPACA_API_KEY=staging_alpaca_key
ALPACA_SECRET_KEY=staging_alpaca_secret
ALPACA_BASE_URL=https://paper-api.alpaca.markets

## BizOSaaS Platform Services - Dokploy Environment Variables

### Infrastructure Services (Database Connections)
```
# Shared PostgreSQL
POSTGRES_HOST=infrastructureservices-sharedpostgres-3cwdm6
POSTGRES_PORT=5432
POSTGRES_DB=bizosaas_staging
POSTGRES_USER=admin
POSTGRES_PASSWORD=BizOSaaS2025@StagingDB
DATABASE_URL=postgresql://admin:BizOSaaS2025@StagingDB@infrastructureservices-sharedpostgres-3cwdm6:5432/bizosaas_staging

# Backup PostgreSQL
BACKUP_POSTGRES_HOST=infrastructureservices-sharedpostgresbackup-scigsr
BACKUP_POSTGRES_PORT=5432
BACKUP_POSTGRES_DB=bizosaas_backup
BACKUP_DATABASE_URL=postgresql://admin:BizOSaaS2025@BackupDB@infrastructureservices-sharedpostgresbackup-scigsr:5432/bizosaas_backup

# Saleor PostgreSQL
SALEOR_POSTGRES_HOST=infrastructureservices-saleorpostgres-h7eayh
SALEOR_POSTGRES_PORT=5432
SALEOR_POSTGRES_DB=saleor
SALEOR_POSTGRES_USER=saleor
SALEOR_POSTGRES_PASSWORD=SaleorDB2025@Staging
SALEOR_DATABASE_URL=postgresql://saleor:SaleorDB2025@Staging@infrastructureservices-saleorpostgres-h7eayh:5432/saleor

# BizOSaaS Redis
REDIS_HOST=infrastructureservices-bizosaasredis-w0gw3g
REDIS_PORT=6379
REDIS_PASSWORD=BizOSaaS2025@redis
REDIS_URL=redis://:BizOSaaS2025@redis@infrastructureservices-bizosaasredis-w0gw3g:6379

# Saleor Redis
SALEOR_REDIS_HOST=infrastructureservices-saleorredis-nzd5pv
SALEOR_REDIS_PORT=6379
SALEOR_REDIS_PASSWORD=SaleorRedis2025@Staging
CELERY_BROKER_URL=redis://:SaleorRedis2025@Staging@infrastructureservices-saleorredis-nzd5pv:6379/1
CACHE_URL=redis://:SaleorRedis2025@Staging@infrastructureservices-saleorredis-nzd5pv:6379/0
```

### Backend Services Requiring API Key Updates (6 services)

**1. brain-gateway (Port 8001)**
- Needs: AI keys (OpenAI, OpenRouter, Anthropic) + Payment keys (Stripe, PayPal)

**2. saleor-platform (Port 8000)**
- Needs: Payment keys only (Stripe, PayPal)

**3. ai-agents (Port 8008)**
- Needs: AI keys (OpenAI, OpenRouter, Anthropic) + Telegram Bot Token

**4. django-crm (Port 8003)**
- Needs: Telegram Bot Token only

**5. quanttrade-backend (Port 8009)**
- Needs: AI keys (OpenAI) + Trading API (Alpaca staging keys)

**6. amazon-sourcing (Port 8010)**
- Needs: Amazon Seller API + OpenAI key

### Services NOT Requiring Additional API Keys
- temporal-ui (internal only)
- wagtail-cms (database + redis only)
- business-directory (database + redis only)
- coreldove-backend (database + redis only)
- All 6 frontend services (NEXT_PUBLIC_API_URL already configured)
- shared-components (no external APIs)

## Saleor Dashboard Access (CoreLdove E-Commerce)

**Dashboard URL:** https://stg.coreldove.com/dashboard/
**API URL:** https://api.coreldove.com/graphql/

**Status:** ✅ FULLY OPERATIONAL (November 4, 2025)
- Dashboard Container: `frontendservices-saleordashboard-84ku62`
- API Container: `backend-saleor-api`
- PostgreSQL: `infrastructureservices-saleorpostgres-h7eayh`
- Redis: `infrastructureservices-saleorredis-nzd5pv`
- Dashboard Image: `ghcr.io/saleor/saleor-dashboard:latest`
- API Image: `ghcr.io/saleor/saleor:3.20`

**Admin Credentials:**
- Email: admin@coreldove.com
- Password: CoreLDove2025!Admin
- Status: ✅ Superuser created and active (November 4, 2025)
- Last Password Reset: November 8, 2025

**Infrastructure Credentials:**
- PostgreSQL Password: SaleorDB2025@Staging
- Redis Password: SaleorRedis2025@Staging

**Service Status:**
- ✅ PostgreSQL: Running (PostgreSQL 16.10, connectivity verified)
- ✅ Redis: Running (PONG response, password protected)
- ✅ Saleor API: Running (all migrations applied)
- ✅ Dashboard: Running (connected to public API)
- ✅ Public API: Accessible via HTTPS with Cloudflare
- ✅ CORS: Configured for stg.coreldove.com
- ✅ SSL/TLS: Enabled via Let's Encrypt

**Webhook Integration:**
- Status: PLANNED (documentation complete, implementation pending)
- Integration: CrewAI agents via Brain Gateway webhooks
- Documentation: `SALEOR_WEBHOOK_CREWAI_INTEGRATION_PLAN.md`

## MinIO Object Storage (Shared Infrastructure)

**Service:** infrastructure-services → minio-storage
**Status:** ✅ FULLY OPERATIONAL (November 4, 2025)
**Deployment:** Docker Compose on KVM4 (72.60.219.244)

**Console Access:**
- URL: https://minio.stg.bizoholic.com
- Username: bizosaas_admin
- Password: BizOSaaS2025@MinIO!Secure

**S3 API Endpoint:**
- URL: https://s3.stg.bizoholic.com
- Region: us-east-1
- Protocol: S3-compatible

**Storage Backend:**
- Type: VPS Local Storage
- Path: /mnt/minio-data
- Available Space: ~168GB

**Service Accounts:** (To be created)
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

**Buckets:** (To be created)
- coreldove-products (Public Read)
- bizoholic-media (Public Read)
- thrillring-assets (Public Read)
- shared-documents (Private)
- user-uploads (Private)
- backups (Private)
- temp-uploads (Private, 24h auto-delete)

**SSL Certificates:**
- ✅ Let's Encrypt certificates active
- ✅ s3.stg.bizoholic.com (valid until Feb 2, 2026)
- ✅ minio.stg.bizoholic.com (valid until Feb 2, 2026)
- ✅ Cloudflare proxy re-enabled

**Container Details:**
- Image: minio/minio:RELEASE.2024-10-29T16-01-48Z
- Container: infrastructureservices-minio-ce59dx-minio-1
- Network: dokploy-network
- Ports: 9000 (S3 API), 9001 (Console)

## Cloudflare

- User API Token - 8O_3_FRsFFbibnRQDeKpmRnqBz8WbrwWEEyy3H_g

curl "https://api.cloudflare.com/client/v4/user/tokens/verify" \
-H "Authorization: Bearer 8O_3_FRsFFbibnRQDeKpmRnqBz8WbrwWEEyy3H_g"

## Meta Credentials
- meta catalog api - EAAZAnKGXBra8BP8LMSDQH0QUjt44ufftxKVVgeXewy8jBZBno1TfLepXHIeBAD71Glk7umrSiKR62F01Ym0X6NqDzMxXCx5A12wlZBcUaT04bIZBOu7DDvkDZBqTjmFyRYqNQwrZBhpZB4zy9jRtIop8mvTPOOvcORcPyZBjPem5gsDEbhehz7uii7JuNSQ6OAZDZD