---
description: Deploy Lago Billing Engine to KVM8 VPS
---

# Deploy Lago Billing Engine to KVM8 Server

## Server Information
- **Server**: KVM8 (72.60.98.213)
- **Deployment Method**: Docker Compose (Standalone)
- **Location**: `/opt/lago-billing`

## Quick Deployment

### Automated Deployment (Recommended)

```bash
# From your local machine
cd /home/alagiri/projects/bizosaas-platform

# Run the deployment script
./scripts/deploy-lago-kvm8.sh
```

This script will:
1. ✅ Upload `docker-compose.lago.yml` and `.env.lago` to server
2. ✅ Create necessary Docker networks
3. ✅ Pull Lago images
4. ✅ Start all Lago services
5. ✅ Verify deployment

### Manual Deployment

If you prefer manual control:

```bash
# 1. SSH to KVM8 server
ssh root@72.60.98.213

# 2. Create deployment directory
mkdir -p /opt/lago-billing
cd /opt/lago-billing

# 3. Upload files (from local machine in another terminal)
scp docker-compose.lago.yml root@72.60.98.213:/opt/lago-billing/
scp .env.lago root@72.60.98.213:/opt/lago-billing/

# 4. Back on server - Create networks
docker network create brain-network || true
docker network create dokploy-network || true

# 5. Deploy Lago
docker compose -f docker-compose.lago.yml --env-file .env.lago up -d

# 6. Check status
docker compose -f docker-compose.lago.yml ps
```

## Environment Configuration

The `.env.lago` file contains:

```bash
LAGO_POSTGRES_DB=lago
LAGO_POSTGRES_USER=lago
LAGO_POSTGRES_PASSWORD=lago_password_2025
LAGO_SECRET_KEY_BASE=b871ed19c83665268c74149028bfdf3787727402660161421715423877960786
LAGO_RSA_PRIVATE_KEY="<multi-line RSA key>"
LAGO_ENCRYPTION_PRIMARY_KEY=b871ed19c83665268c74149028bfdf37
LAGO_ENCRYPTION_DETERMINISTIC_KEY=c4772099e0df28646077558667c29579
LAGO_ENCRYPTION_KEY_DERIVATION_SALT=5c72d9e685f02604297135317769532e
LAGO_API_URL=http://lago-api:3000
LAGO_FRONT_URL=http://localhost:8088
RAILS_ENV=production
```

**Note**: The RSA private key is already generated and included in `.env.lago`.

## DNS Configuration

Before accessing the dashboard, configure these DNS records:

| Subdomain | Type | Value | TTL |
|-----------|------|-------|-----|
| `billing.bizoholic.net` | A | `72.60.98.213` | 300 |
| `lago-api.bizoholic.net` | A | `72.60.98.213` | 300 |

## Verify Deployment

```bash
# SSH to server
ssh root@72.60.98.213

# Check all containers are running
docker ps --filter name=lago

# Expected output: 5 containers
# - lago-db (healthy)
# - lago-redis
# - lago-api
# - lago-worker  
# - lago-front

# Check logs
docker logs lago-api --tail 50
docker logs lago-front --tail 50
docker logs lago-migrate

# Test API endpoint (internal)
curl http://localhost:3010/health

# Test frontend (internal)
curl http://localhost:8088
```

## Post-Deployment Setup

### 1. Create Admin Account

1. Navigate to `https://billing.bizoholic.net`
2. Fill in the registration form (first user becomes admin)
3. Verify email if required

### 2. Generate API Key

1. Login to Lago dashboard
2. Go to **Developers** → **API Keys**
3. Click **Create API Key**
4. Copy the generated key (you'll need this for Brain Gateway)

### 3. Configure Payment Gateways

Go to **Settings** → **Integrations** and add:

#### Razorpay
- API Key ID: `<from credentials.md>`
- API Key Secret: `<from credentials.md>`

#### Stripe (Optional)
- Secret Key: `<your stripe secret>`
- Publishable Key: `<your stripe publishable>`

### 4. Create Subscription Plans

Go to **Plans** and create:

#### Starter Plan
- Name: `Starter`
- Code: `starter`
- Amount: `$29.00`
- Interval: `Monthly`
- Features: 1000 leads, 5GB storage, 1 agent

#### Professional Plan
- Name: `Professional`
- Code: `professional`
- Amount: `$99.00`
- Interval: `Monthly`
- Features: 10,000 leads, 50GB storage, 5 agents

#### Enterprise Plan
- Name: `Enterprise`
- Code: `enterprise`
- Amount: `$499.00`
- Interval: `Monthly`
- Features: Unlimited leads, 500GB storage, Unlimited agents

## Update Brain Gateway

After Lago is deployed, update Brain Gateway configuration:

```bash
# SSH to KVM8
ssh root@72.60.98.213

# Update Brain Gateway environment
# Add these to your Brain Gateway .env or docker-compose:
LAGO_API_KEY=<api-key-from-lago-dashboard>
LAGO_API_URL=http://lago-api:3000

# Restart Brain Gateway
docker restart bizosaas-brain-staging
```

## Service Management

### Start Services
```bash
cd /opt/lago-billing
docker compose -f docker-compose.lago.yml --env-file .env.lago up -d
```

### Stop Services
```bash
cd /opt/lago-billing
docker compose -f docker-compose.lago.yml down
```

### Restart Services
```bash
cd /opt/lago-billing
docker compose -f docker-compose.lago.yml restart
```

### View Logs
```bash
# All services
docker compose -f docker-compose.lago.yml logs -f

# Specific service
docker logs -f lago-api
docker logs -f lago-worker
docker logs -f lago-front
```

### Update Lago
```bash
cd /opt/lago-billing
docker compose -f docker-compose.lago.yml pull
docker compose -f docker-compose.lago.yml up -d
```

## Architecture on KVM8

```
┌─────────────────────────────────────────────────────────┐
│              KVM8 Server (72.60.98.213)                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │           Traefik (dokploy-traefik)              │  │
│  │  ┌────────────────┐  ┌────────────────┐         │  │
│  │  │ billing.       │  │ lago-api.      │         │  │
│  │  │ bizoholic.net  │  │ bizoholic.net  │         │  │
│  │  └────────┬───────┘  └────────┬───────┘         │  │
│  └───────────┼──────────────────┼──────────────────┘  │
│              │                  │                      │
│  ┌───────────▼──────┐  ┌────────▼──────┐             │
│  │   lago-front     │  │   lago-api    │             │
│  │   (Port 8088)    │  │   (Port 3010) │             │
│  └──────────────────┘  └───────┬───────┘             │
│                                │                      │
│  ┌─────────────────────────────▼──────────────────┐  │
│  │              lago-worker                        │  │
│  └─────────────────────────────┬──────────────────┘  │
│                                │                      │
│  ┌──────────────┐  ┌───────────▼──────────────────┐  │
│  │  lago-redis  │  │        lago-db               │  │
│  │  (Cache)     │  │  (PostgreSQL 14)             │  │
│  └──────────────┘  └──────────────────────────────┘  │
│                                                       │
│  Networks: brain-network, dokploy-network            │
└───────────────────────────────────────────────────────┘
```

## Resource Usage

Expected resource consumption on KVM8:

| Service | Memory Limit | CPU | Notes |
|---------|-------------|-----|-------|
| lago-db | 256MB | ~10% | PostgreSQL database |
| lago-redis | 128MB | ~5% | Cache layer |
| lago-api | 1GB | ~15% | Main API service |
| lago-worker | 1GB | ~10% | Background jobs |
| lago-front | 256MB | ~5% | Web dashboard |
| **Total** | **~2.6GB** | **~45%** | Estimated |

## Troubleshooting

### Lago API won't start

```bash
# Check RSA key format
docker exec lago-api env | grep LAGO_RSA

# Check database migrations
docker logs lago-migrate

# Restart API
docker restart lago-api
```

### Can't access dashboard

```bash
# Check Traefik routing
docker logs dokploy-traefik | grep lago

# Verify DNS
nslookup billing.bizoholic.net

# Check frontend logs
docker logs lago-front
```

### Database connection errors

```bash
# Check database health
docker exec lago-db pg_isready -U lago

# Check database logs
docker logs lago-db

# Verify connection string
docker exec lago-api env | grep DATABASE_URL
```

### Worker not processing jobs

```bash
# Check worker logs
docker logs lago-worker -f

# Check Redis connection
docker exec lago-worker redis-cli -h lago-redis ping

# Restart worker
docker restart lago-worker
```

## Backup and Restore

### Backup Database

```bash
# Create backup
docker exec lago-db pg_dump -U lago lago > lago-backup-$(date +%Y%m%d).sql

# Compress backup
gzip lago-backup-$(date +%Y%m%d).sql
```

### Restore Database

```bash
# Stop services
cd /opt/lago-billing
docker compose -f docker-compose.lago.yml down

# Restore backup
gunzip -c lago-backup-20260112.sql.gz | docker exec -i lago-db psql -U lago lago

# Start services
docker compose -f docker-compose.lago.yml up -d
```

## Security Considerations

1. **Change default passwords** in `.env.lago`
2. **Enable LAGO_DISABLE_SIGNUP=true** after creating admin account
3. **Rotate API keys** regularly
4. **Enable firewall** rules to restrict database access
5. **Regular backups** of database and configuration

## Support

- **Lago Documentation**: https://doc.getlago.com
- **Lago GitHub**: https://github.com/getlago/lago
- **Community**: https://getlago.com/slack
