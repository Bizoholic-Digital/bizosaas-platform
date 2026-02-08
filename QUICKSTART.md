# BizOSaaS Platform - Quick Start Guide

## 🚀 Recommended Approach: Registry + CI/CD

This guide will help you set up BizOSaaS using Docker Registry and local domains for a production-like development environment.

---

## ⚠️ CRITICAL: Windows / WSL2 Users

If you are running this on Windows (via WSL2) and accessing from a Windows browser (Chrome/Edge):

**You MUST update your Windows Hosts File manually.**

1. Open **Notepad** as Administrator. with `Win+X` -> `Run` -> `notepad.exe` -> `Ctrl+Shift+Enter` (Run as Admin)
2. Open file: `C:\Windows\System32\drivers\etc\hosts`
3. Add these lines at the bottom:

```text
127.0.0.1    bizosaas.local
127.0.0.1    portal.bizosaas.local
127.0.0.1    api.bizosaas.local
127.0.0.1    auth.bizosaas.local
127.0.0.1    vault.bizosaas.local
127.0.0.1    temporal.bizosaas.local
127.0.0.1    grafana.bizosaas.local
127.0.0.1    prometheus.bizosaas.local
127.0.0.1    jaeger.bizosaas.local
```

4. Save the file.
5. Now your Windows browser can resolve `portal.bizosaas.local` to your locally running Docker containers.

---

## Prerequisites

- Docker & Docker Compose installed
- Git installed
- Sudo access (for /etc/hosts modification)
- 8GB RAM minimum
- 20GB free disk space

---

## Option 1: Automated Setup (Recommended)

### Single Command Deployment

```bash
cd /home/alagiri/projects/bizosaas-platform
./scripts/deploy-local.sh
```

This script will:
1. ✅ Check prerequisites
2. ✅ Configure local domains in /etc/hosts (Linux only)
3. ✅ Create Docker network
4. ✅ Build all Docker images
5. ✅ Push images to local registry
6. ✅ Deploy all services
7. ✅ Verify health checks

**Time**: ~10-15 minutes (first run)

---

## Option 2: Manual Setup

### Step 1: Configure Local Domains

```bash
sudo tee -a /etc/hosts << EOF

# BizOSaaS Local Development
127.0.0.1    bizosaas.local
127.0.0.1    portal.bizosaas.local
127.0.0.1    api.bizosaas.local
127.0.0.1    auth.bizosaas.local
127.0.0.1    vault.bizosaas.local
127.0.0.1    temporal.bizosaas.local
127.0.0.1    grafana.bizosaas.local
127.0.0.1    prometheus.bizosaas.local
127.0.0.1    jaeger.bizosaas.local
EOF
```

### Step 2: Create Docker Network

```bash
docker network create brain-network
```

### Step 5: Verify Deployment

```bash
docker-compose -f docker-compose.registry.yml ps
```

---

## Access Your Services

Once deployed, access services at:

| Service | URL | Credentials |
|---------|-----|-------------|
| **Client Portal** | http://portal.bizosaas.local | - |
| **API Documentation** | http://api.bizosaas.local/docs | - |
| **Auth Service** | http://auth.bizosaas.local/docs | - |
| **Vault UI** | http://vault.bizosaas.local | Token: `root` |
| **Temporal UI** | http://temporal.bizosaas.local | - |
| **Grafana** | http://grafana.bizosaas.local | admin/admin |
| **Prometheus** | http://prometheus.bizosaas.local | - |
| **Jaeger** | http://jaeger.bizosaas.local | - |
| **Portainer** | https://localhost:9443 | Your credentials |

---

## Development Workflow

### 1. Make Code Changes

Edit files in your IDE as normal.

### 2. Rebuild Specific Service

```bash
# Rebuild brain-gateway
cd bizosaas-brain-core/brain-gateway
docker build -t localhost:5000/bizosaas/brain-gateway:latest .
docker push localhost:5000/bizosaas/brain-gateway:latest

# Restart service
docker-compose -f ../../docker-compose.registry.yml restart brain-gateway
```

### 3. View Logs

```bash
# All services
docker-compose -f docker-compose.registry.yml logs -f

# Specific service
docker logs -f bizosaas-brain-gateway

# With Portainer
# Go to https://localhost:9443 → Containers → Select → Logs
```

### 4. Run Database Migrations

```bash
docker exec -it bizosaas-brain-gateway alembic upgrade head
```

### 5. Access Database

```bash
docker exec -it bizosaas-postgres psql -U postgres -d bizosaas
```

### 6. Access Redis

```bash
docker exec -it bizosaas-redis redis-cli
```

---

## Common Tasks

### Stop All Services

```bash
docker-compose -f docker-compose.registry.yml down
```

### Stop and Remove Volumes (Clean Slate)

```bash
docker-compose -f docker-compose.registry.yml down -v
```

### Rebuild All Images

```bash
./scripts/build-and-push.sh latest
```

### Update Single Service

```bash
# Example: Update client-portal
docker-compose -f docker-compose.registry.yml up -d --no-deps --build client-portal
```

### View Resource Usage

```bash
docker stats
```

### Backup Database

```bash
docker exec bizosaas-postgres pg_dump -U postgres bizosaas > backup.sql
```

### Restore Database

```bash
cat backup.sql | docker exec -i bizosaas-postgres psql -U postgres bizosaas
```

---

## Troubleshooting

### Issue: Can't access portal.bizosaas.local

**Solution**:
1. **Windows Users**: Did you update `C:\Windows\System32\drivers\etc\hosts`? (See top of this guide)
2. **Verify Traefik**: `docker ps | grep traefik`
3. **Verify App**: `docker logs bizosaas-client-portal` - did it crash?

### Issue: Images won't push to registry

**Solution**:
```bash
# Verify registry is running
docker ps | grep registry

# Test registry
curl http://localhost:5000/v2/_catalog

# Configure insecure registry
sudo tee /etc/docker/daemon.json << EOF
{
  "insecure-registries": ["localhost:5000"]
}
EOF

sudo systemctl restart docker
```

---

## CI/CD Pipeline Setup

### 1. Create GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/bizosaas-platform.git
git push -u origin main
```

### 2. Configure GitHub Secrets

Go to GitHub → Settings → Secrets and variables → Actions

Add these secrets:
- `STAGING_HOST` - Staging server IP
- `STAGING_USER` - SSH username
- `STAGING_SSH_KEY` - SSH private key
- `PROD_HOST` - Production server IP
- `PROD_USER` - SSH username
- `PROD_SSH_KEY` - SSH private key
- `SLACK_WEBHOOK` - (Optional) Slack webhook URL

### 3. Push to Trigger Pipeline

```bash
git push origin main
```

GitHub Actions will automatically:
1. Run tests
2. Build Docker images
3. Push to GitHub Container Registry
4. Deploy to staging (if on `develop` branch)
5. Deploy to production (if tagged with `v*`)

### 4. Create Release

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

This triggers production deployment.

---

## Summary

✅ **Recommended Setup**: Registry + Local Domains + CI/CD  
✅ **Deployment Time**: 10-15 minutes  
✅ **Production-Ready**: Yes  
✅ **Scalable**: Yes  

**Start Command**:
```bash
./scripts/deploy-local.sh
```

**Access Portal**:
```
http://portal.bizosaas.local
```

🚀 **You're ready to develop!**
