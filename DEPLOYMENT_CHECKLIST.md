# BizOSaaS Platform - Production Deployment Checklist

## Pre-Deployment Verification

### 1. Code Quality & Security
- [ ] All sensitive credentials removed from code
- [ ] Environment variables properly configured
- [ ] `.gitignore` updated and verified
- [ ] No hardcoded secrets in repository
- [ ] All API keys stored in Vault
- [ ] Docker images built and tested locally

### 2. Service Health Checks
- [ ] All core services start successfully
- [ ] Health endpoints respond correctly
- [ ] Database migrations completed
- [ ] Redis connectivity verified
- [ ] Vault initialized and unsealed

### 3. Authentication & Authorization
- [ ] Admin user created and tested
- [ ] SSO with Authentik working
- [ ] JWT token generation verified
- [ ] Role-based access control tested

### 4. Docker Cleanup
- [ ] Unused containers removed
- [ ] Dangling images cleaned
- [ ] Unused volumes pruned
- [ ] Unused networks removed
- [ ] Docker system optimized

## Oracle Cloud Setup (Always Free Tier)

### VM Configuration
- **Instance Type**: ARM-based Ampere A1
- **vCPUs**: 4 OCPUs
- **RAM**: 24 GB
- **Storage**: 200 GB Block Volume
- **OS**: Ubuntu 22.04 LTS

### Required Services
1. **Compute Instance** (Always Free)
   - 4 OCPUs ARM
   - 24GB RAM
   - Ubuntu 22.04

2. **Block Storage** (Always Free)
   - 200 GB total

3. **Networking** (Always Free)
   - 1 Public IP
   - Security Lists configured

### Port Configuration
```
Inbound Rules:
- 22 (SSH)
- 80 (HTTP)
- 443 (HTTPS)
- 3003 (Client Portal)
- 8000 (Brain Gateway)
- 9000 (Authentik)
- 9001 (Portainer)
```

## Deployment Steps

### 1. Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin -y

# Create deployment user
sudo useradd -m -s /bin/bash bizosaas
sudo usermod -aG docker bizosaas
```

### 2. Clone Repository
```bash
su - bizosaas
git clone https://github.com/YOUR_USERNAME/bizosaas-platform.git
cd bizosaas-platform
```

### 3. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env

# Required variables:
# - POSTGRES_PASSWORD
# - JWT_SECRET
# - NEXTAUTH_SECRET
# - VAULT_TOKEN
# - OPENAI_API_KEY (optional)
# - ANTHROPIC_API_KEY (optional)
# - GITHUB_TOKEN (for MCP)
```

### 4. Initialize Services
```bash
# Start core infrastructure
cd bizosaas-brain-core
docker compose up -d postgres redis vault

# Initialize Vault
../scripts/init-vault.sh

# Start remaining services
docker compose up -d

# Start Authentik
docker compose -f docker-compose.authentik.yml up -d

# Verify all services
docker ps
```

### 5. Seed Initial Data
```bash
# Create admin user
docker exec brain-auth python3 /app/seed_users_simple.py

# Verify login
curl -X POST http://localhost:8009/auth/sso/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@bizosaas.com","password":"Admin@123","platform":"bizoholic"}'
```

### 6. Configure Reverse Proxy (Nginx)
```bash
sudo apt install nginx -y

# Create Nginx config
sudo nano /etc/nginx/sites-available/bizosaas

# Enable site
sudo ln -s /etc/nginx/sites-available/bizosaas /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 7. SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Post-Deployment Verification

### Health Checks
```bash
# Check all services
curl http://localhost:8000/health  # Brain Gateway
curl http://localhost:8009/health  # Auth Service
curl http://localhost:3003         # Client Portal
curl http://localhost:9000         # Authentik
```

### Monitoring Setup
- [ ] Grafana dashboards configured
- [ ] Prometheus scraping metrics
- [ ] Loki collecting logs
- [ ] Jaeger tracing enabled

### Backup Configuration
- [ ] Database backup script created
- [ ] Vault backup configured
- [ ] Volume snapshots scheduled
- [ ] Offsite backup verified

## Rollback Plan
1. Stop all services: `docker compose down`
2. Restore database from backup
3. Restore Vault from backup
4. Restart services with previous version

## Production Checklist
- [ ] All services running and healthy
- [ ] SSL certificates installed
- [ ] Firewall rules configured
- [ ] Monitoring active
- [ ] Backups scheduled
- [ ] Documentation updated
- [ ] Team notified of deployment
