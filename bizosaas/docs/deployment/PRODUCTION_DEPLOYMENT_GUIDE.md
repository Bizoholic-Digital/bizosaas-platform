# BizOSaaS Production Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the BizOSaaS platform to production with optimized performance, security, and monitoring.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Server Setup](#server-setup)
3. [Environment Configuration](#environment-configuration)
4. [SSL/TLS Setup](#ssltls-setup)
5. [Production Deployment](#production-deployment)
6. [Monitoring Setup](#monitoring-setup)
7. [Security Hardening](#security-hardening)
8. [Backup Strategy](#backup-strategy)
9. [Maintenance & Updates](#maintenance--updates)
10. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

**Minimum Production Server Specifications:**
- **CPU**: 8 cores (Intel Xeon or AMD EPYC)
- **RAM**: 32GB DDR4
- **Storage**: 500GB NVMe SSD (for database and application data)
- **Network**: 1Gbps connection with static IP
- **OS**: Ubuntu 22.04 LTS or CentOS 8+

**Recommended Production Server Specifications:**
- **CPU**: 16 cores (Intel Xeon or AMD EPYC)
- **RAM**: 64GB DDR4
- **Storage**: 1TB NVMe SSD + 2TB SSD for backups
- **Network**: 10Gbps connection with static IP
- **OS**: Ubuntu 22.04 LTS

### Required Software

- Docker Engine 24.0+
- Docker Compose 2.20+
- Git 2.30+
- Nginx (optional, for additional reverse proxy)
- UFW or iptables (firewall)

### Domain Requirements

You'll need the following domains configured:
- `bizoholic.com` (main website)
- `api.bizoholic.com` (API gateway)
- `admin.bizoholic.com` (admin dashboard)
- `portal.bizoholic.com` (client portal)
- `coreldove.bizoholic.com` (e-commerce platform)
- `cms.bizoholic.com` (content management)
- `monitoring.bizoholic.com` (monitoring dashboard)

## Server Setup

### 1. Initial Server Configuration

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y curl wget git ufw fail2ban htop iotop

# Configure firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Performance Optimizations

```bash
# Optimize system limits
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Optimize kernel parameters
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
echo "net.core.somaxconn=65535" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog=65535" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Configure swap (if not using SSD)
sudo swapoff -a
sudo dd if=/dev/zero of=/swapfile bs=1G count=8
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo "/swapfile swap swap defaults 0 0" | sudo tee -a /etc/fstab
```

## Environment Configuration

### 1. Clone Repository

```bash
# Clone the repository
git clone https://github.com/your-org/bizoholic.git
cd bizoholic/bizosaas

# Switch to production branch (if applicable)
git checkout production
```

### 2. Configure Environment Variables

```bash
# Copy production environment template
cp .env.production.secure .env.production

# Edit environment file with your production values
nano .env.production
```

**Critical Variables to Configure:**

```bash
# Domain Configuration
DOMAIN=your-domain.com
API_DOMAIN=api.your-domain.com

# Security Keys (Generate unique, secure keys)
JWT_SECRET=$(openssl rand -base64 64)
NEXTAUTH_SECRET=$(openssl rand -base64 32)
DJANGO_SECRET_KEY=$(openssl rand -base64 50)

# Database Credentials
POSTGRES_PASSWORD=$(openssl rand -base64 32)
POSTGRES_USER=bizosaas_prod

# API Keys
OPENAI_API_KEY=sk-your-openai-key
STRIPE_SECRET_KEY=sk_live_your-stripe-key

# Email Configuration
SMTP_HOST=smtp.your-provider.com
SMTP_USER=your-smtp-user
SMTP_PASSWORD=your-smtp-password
```

### 3. Generate SSL Configuration

```bash
# Create SSL configuration directory
mkdir -p ssl

# Edit SSL email in environment
echo "SSL_EMAIL=admin@your-domain.com" >> .env.production
```

## SSL/TLS Setup

### Option 1: Let's Encrypt (Automated)

The production docker-compose includes automatic SSL certificate generation via Let's Encrypt. Ensure your domains are properly configured to point to your server.

### Option 2: Custom SSL Certificates

If using custom SSL certificates:

```bash
# Create certificate directory
mkdir -p ssl/certs

# Copy your certificates
cp your-domain.crt ssl/certs/
cp your-domain.key ssl/certs/
cp ca-bundle.crt ssl/certs/

# Update docker-compose.production.optimized.yml
# Mount certificates in traefik service
```

## Production Deployment

### 1. Build Production Images

```bash
# Set build environment
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Build all production images
docker-compose -f docker-compose.production.optimized.yml build --no-cache

# Verify images
docker images | grep bizosaas
```

### 2. Initialize Database

```bash
# Start database only
docker-compose -f docker-compose.production.optimized.yml up -d bizosaas-postgres bizosaas-redis

# Wait for database to be ready
sleep 30

# Run database migrations
docker-compose -f docker-compose.production.optimized.yml exec bizosaas-postgres psql -U bizosaas_prod -d bizosaas_production -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Initialize application databases
docker-compose -f docker-compose.production.optimized.yml run --rm bizosaas-crm python manage.py migrate
docker-compose -f docker-compose.production.optimized.yml run --rm bizosaas-wagtail-cms python manage.py migrate
```

### 3. Deploy All Services

```bash
# Deploy complete production stack
docker-compose -f docker-compose.production.optimized.yml up -d

# Verify all services are running
docker-compose -f docker-compose.production.optimized.yml ps

# Check service health
docker-compose -f docker-compose.production.optimized.yml exec bizosaas-brain-api curl -f http://localhost:8000/health
```

### 4. Initial Setup

```bash
# Create admin users
docker-compose -f docker-compose.production.optimized.yml exec bizosaas-crm python manage.py createsuperuser
docker-compose -f docker-compose.production.optimized.yml exec bizosaas-wagtail-cms python manage.py createsuperuser

# Load initial data (if available)
docker-compose -f docker-compose.production.optimized.yml exec bizosaas-crm python manage.py loaddata initial_data.json
```

## Monitoring Setup

### 1. Verify Monitoring Services

```bash
# Check Prometheus
curl -f http://localhost:9090/api/v1/status/config

# Check Grafana
curl -f http://localhost:3003/api/health

# Import Grafana dashboards
docker-compose -f docker-compose.production.optimized.yml exec bizosaas-grafana \
  grafana-cli plugins install grafana-piechart-panel
```

### 2. Configure Alerts

```bash
# Create alerting rules directory
mkdir -p monitoring/rules

# Add custom alerting rules
cat > monitoring/rules/bizosaas.yml << EOF
groups:
  - name: bizosaas
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"

      - alert: DatabaseDown
        expr: up{job="postgres"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "PostgreSQL database is down"
EOF
```

## Security Hardening

### 1. Container Security

```bash
# Scan images for vulnerabilities (install trivy first)
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Scan production images
trivy image bizosaas/brain-api:latest
trivy image bizosaas/admin-frontend:latest
```

### 2. Network Security

```bash
# Configure additional firewall rules
sudo ufw deny 5432  # PostgreSQL
sudo ufw deny 6379  # Redis
sudo ufw deny 9090  # Prometheus (use reverse proxy)

# Allow only specific monitoring ports if needed
sudo ufw allow from your-monitoring-server-ip to any port 9090
```

### 3. Regular Security Updates

```bash
# Create update script
cat > update-security.sh << EOF
#!/bin/bash
# Security update script for BizOSaaS

# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Docker images
docker-compose -f docker-compose.production.optimized.yml pull

# Restart services with new images
docker-compose -f docker-compose.production.optimized.yml up -d --remove-orphans

# Clean up old images
docker image prune -f
EOF

chmod +x update-security.sh
```

## Backup Strategy

### 1. Database Backups

```bash
# Create backup script
cat > backup-database.sh << EOF
#!/bin/bash
# Database backup script

DATE=\$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/bizosaas/backups"
mkdir -p \$BACKUP_DIR

# PostgreSQL backup
docker-compose -f docker-compose.production.optimized.yml exec -T bizosaas-postgres \
  pg_dumpall -U bizosaas_prod > \$BACKUP_DIR/postgres_\$DATE.sql

# Compress backup
gzip \$BACKUP_DIR/postgres_\$DATE.sql

# Upload to S3 (if configured)
if [ ! -z "\$AWS_ACCESS_KEY_ID" ]; then
  aws s3 cp \$BACKUP_DIR/postgres_\$DATE.sql.gz s3://\$BACKUP_S3_BUCKET/database/
fi

# Keep only last 7 days of local backups
find \$BACKUP_DIR -name "postgres_*.sql.gz" -mtime +7 -delete
EOF

chmod +x backup-database.sh

# Add to crontab for daily backups
echo "0 2 * * * /opt/bizosaas/backup-database.sh" | sudo crontab -
```

### 2. Volume Backups

```bash
# Create volume backup script
cat > backup-volumes.sh << EOF
#!/bin/bash
# Volume backup script

DATE=\$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/bizosaas/backups/volumes"
mkdir -p \$BACKUP_DIR

# Backup Docker volumes
docker run --rm -v bizosaas_postgres_data_production:/data -v \$BACKUP_DIR:/backup \
  alpine tar czf /backup/postgres_data_\$DATE.tar.gz -C /data .

docker run --rm -v bizosaas_cms_media_production:/data -v \$BACKUP_DIR:/backup \
  alpine tar czf /backup/cms_media_\$DATE.tar.gz -C /data .

# Keep only last 3 days of volume backups
find \$BACKUP_DIR -name "*.tar.gz" -mtime +3 -delete
EOF

chmod +x backup-volumes.sh
```

## Maintenance & Updates

### 1. Rolling Updates

```bash
# Update application without downtime
./scripts/rolling-update.sh

# Manual rolling update process
docker-compose -f docker-compose.production.optimized.yml pull
docker-compose -f docker-compose.production.optimized.yml up -d --no-deps bizosaas-brain-api
docker-compose -f docker-compose.production.optimized.yml up -d --no-deps bizosaas-ai-agents
# Continue for each service...
```

### 2. Health Checks

```bash
# Create health check script
cat > health-check.sh << EOF
#!/bin/bash
# Production health check script

echo "=== BizOSaaS Production Health Check ==="
echo "Timestamp: \$(date)"
echo

# Check service status
docker-compose -f docker-compose.production.optimized.yml ps

# Check API endpoints
curl -f https://api.bizoholic.com/health || echo "❌ Brain API unhealthy"
curl -f https://bizoholic.com/api/health || echo "❌ Main website unhealthy"
curl -f https://admin.bizoholic.com/api/health || echo "❌ Admin panel unhealthy"

# Check database connectivity
docker-compose -f docker-compose.production.optimized.yml exec -T bizosaas-postgres \
  pg_isready -U bizosaas_prod -d bizosaas_production || echo "❌ Database unhealthy"

# Check Redis connectivity
docker-compose -f docker-compose.production.optimized.yml exec -T bizosaas-redis \
  redis-cli ping || echo "❌ Redis unhealthy"

echo "✅ Health check completed"
EOF

chmod +x health-check.sh

# Run health check every 5 minutes
echo "*/5 * * * * /opt/bizosaas/health-check.sh >> /var/log/bizosaas-health.log 2>&1" | sudo crontab -
```

## Troubleshooting

### Common Issues

#### 1. SSL Certificate Issues

```bash
# Check certificate status
docker-compose -f docker-compose.production.optimized.yml logs bizosaas-traefik | grep acme

# Force certificate renewal
docker-compose -f docker-compose.production.optimized.yml exec bizosaas-traefik \
  traefik healthcheck
```

#### 2. Database Connection Issues

```bash
# Check database logs
docker-compose -f docker-compose.production.optimized.yml logs bizosaas-postgres

# Test database connection
docker-compose -f docker-compose.production.optimized.yml exec bizosaas-postgres \
  psql -U bizosaas_prod -d bizosaas_production -c "SELECT version();"
```

#### 3. Memory Issues

```bash
# Check container memory usage
docker stats

# Increase memory limits in docker-compose.production.optimized.yml
# Restart affected services
docker-compose -f docker-compose.production.optimized.yml restart bizosaas-ai-agents
```

#### 4. Performance Issues

```bash
# Check slow queries
docker-compose -f docker-compose.production.optimized.yml exec bizosaas-postgres \
  psql -U bizosaas_prod -d bizosaas_production -c "SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"

# Monitor real-time performance
htop
iotop
```

### Emergency Procedures

#### 1. Emergency Rollback

```bash
# Rollback to previous version
git checkout HEAD~1
docker-compose -f docker-compose.production.optimized.yml down
docker-compose -f docker-compose.production.optimized.yml up -d
```

#### 2. Database Recovery

```bash
# Restore from backup
docker-compose -f docker-compose.production.optimized.yml stop bizosaas-postgres
docker volume rm bizosaas_postgres_data_production
docker-compose -f docker-compose.production.optimized.yml up -d bizosaas-postgres
docker-compose -f docker-compose.production.optimized.yml exec -T bizosaas-postgres \
  psql -U bizosaas_prod -d bizosaas_production < /opt/bizosaas/backups/postgres_YYYYMMDD_HHMMSS.sql
```

### Monitoring and Logs

```bash
# View all service logs
docker-compose -f docker-compose.production.optimized.yml logs -f

# View specific service logs
docker-compose -f docker-compose.production.optimized.yml logs -f bizosaas-brain-api

# Monitor resource usage
docker-compose -f docker-compose.production.optimized.yml top
```

## Support

For production support and issues:

1. Check the monitoring dashboard at `https://monitoring.your-domain.com`
2. Review application logs via Docker Compose
3. Check system resources with `htop` and `docker stats`
4. Contact support with specific error messages and logs

## Conclusion

This deployment guide provides a comprehensive foundation for running BizOSaaS in production. Regular monitoring, maintenance, and security updates are essential for optimal performance and security.

Remember to:
- Monitor system resources regularly
- Keep backups current and tested
- Apply security updates promptly
- Monitor application performance
- Review logs for any anomalies

The production deployment is now optimized for performance, security, and scalability to support your growing business needs.