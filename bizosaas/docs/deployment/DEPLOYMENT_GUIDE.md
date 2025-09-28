# BizOSaaS Platform - Complete Deployment Guide

## 🎯 Overview

This guide covers the complete deployment process for the BizOSaaS Autonomous AI Agents Platform from local development to production staging on VPS using Dokploy.

## 📋 Prerequisites

### Local Development
- ✅ Python 3.10+ with virtual environment activated
- ✅ Docker and Docker Compose installed
- ✅ PostgreSQL and Redis containers running
- ✅ All dependencies installed in virtual environment

### VPS Requirements
- Ubuntu 20.04+ or similar Linux distribution
- 4GB+ RAM (8GB recommended)
- 50GB+ storage
- Dokploy installed and configured

## 🚀 Phase 1: Local Testing & Verification

### Step 1: Verify Local Environment
```bash
# Ensure you're in the correct directory
cd /home/alagiri/projects/bizoholic/bizosaas

# Test infrastructure connectivity
python test_platform_connectivity.py
```

**Expected Output:**
```
✅ PostgreSQL: Connected successfully
✅ Redis: Connected successfully
⚠️ Platform Status: INFRASTRUCTURE OK, SOME SERVICES DOWN
```

### Step 2: Install Missing Dependencies
```bash
# Ensure virtual environment is activated
source /home/alagiri/claude_workspace/venv/bin/activate

# Install any remaining dependencies
pip install aiohttp==3.9.1 psutil==5.9.6 email-validator

# Verify installation
pip list | grep -E "(fastapi|aiohttp|psutil)"
```

## 🐳 Phase 2: Containerization & Local Testing

### Step 1: Prepare Environment Configuration
```bash
# Copy staging environment template
cp .env.staging .env

# Edit with your actual API keys
nano .env
```

**Required Variables:**
- `OPENAI_API_KEY`: Your OpenAI API key
- `POSTGRES_PASSWORD`: Database password (already set)
- `DJANGO_SECRET_KEY`: Django security key (already set)

### Step 2: Build and Test Containers Locally
```bash
# Run the automated deployment script
./deploy-staging.sh
```

This script will:
1. Stop existing containers
2. Build all Docker images
3. Start infrastructure services (PostgreSQL, Redis)
4. Start application services
5. Run health checks
6. Display service URLs

### Step 3: Verify Container Health
```bash
# Check all containers are running
docker-compose -f docker-compose.staging.yml ps

# Test key endpoints
curl http://localhost:8080/health     # API Gateway
curl http://localhost:8001/health     # AI Agents
curl http://localhost:8003/health     # Business Directory

# View logs if needed
docker-compose -f docker-compose.staging.yml logs -f api-gateway
```

## 🌐 Phase 3: VPS Deployment with Dokploy

### Step 1: Prepare VPS
1. **Install Dokploy** on your VPS following [Dokploy documentation]
2. **Configure DNS** pointing to your VPS IP:
   - `api.bizosaas.staging.com` → VPS IP
   - `app.bizosaas.staging.com` → VPS IP
   - `admin.bizosaas.staging.com` → VPS IP

### Step 2: Configure Secrets in Dokploy
In the Dokploy web interface, add these secrets:

```bash
# Database
POSTGRES_PASSWORD=YourSecurePassword123!

# AI Services
OPENAI_API_KEY=sk-your-openai-key-here

# Application Security
DJANGO_SECRET_KEY=your-super-secret-django-key-here
WAGTAIL_SECRET_KEY=your-super-secret-wagtail-key-here
```

### Step 3: Deploy via Dokploy
1. **Create New Project** in Dokploy
2. **Upload** the `dokploy.yml` configuration
3. **Configure** the Git repository (or upload as ZIP)
4. **Start Deployment**

### Step 4: Monitor Deployment
```bash
# SSH into your VPS to monitor
ssh user@your-vps-ip

# Check Docker containers
docker ps | grep bizosaas

# View application logs
docker logs bizosaas-api-gateway-staging
docker logs bizosaas-ai-agents-staging
```

## 📊 Phase 4: Verification & Testing

### Production URLs
After successful deployment, test these endpoints:

```bash
# API Services
https://api.bizosaas.staging.com/health
https://api.bizosaas.staging.com/metrics

# Web Application
https://app.bizosaas.staging.com

# Admin Interface
https://admin.bizosaas.staging.com/admin
```

### Health Check Script
Create a monitoring script to verify all services:

```bash
#!/bin/bash
# production-health-check.sh

services=(
    "https://api.bizosaas.staging.com/health"
    "https://app.bizosaas.staging.com"
    "https://admin.bizosaas.staging.com/admin"
)

for service in "${services[@]}"; do
    if curl -f -s "$service" > /dev/null; then
        echo "✅ $service is healthy"
    else
        echo "❌ $service is down"
    fi
done
```

## 🔧 Platform Architecture

### Core Services
- **API Gateway** (Port 8080): FastAPI centralized brain with multi-tenant routing
- **AI Agents** (Port 8001): 46+ CrewAI agents for autonomous operations
- **Django CRM** (Port 8007): Customer relationship management
- **Wagtail CMS** (Port 8010): Content management system
- **Business Directory** (Port 8003): Business listings and directory services

### Infrastructure
- **PostgreSQL**: Multi-database setup (bizosaas, django_crm, wagtail_cms)
- **Redis**: Multi-database caching and session management
- **Docker**: Containerized deployment
- **Dokploy**: CI/CD and deployment management

### Next.js Frontends
- **Bizoholic Website** (Port 3000): Main marketing and application interface
- **Monitoring Dashboard** (Port 3001): Platform health and metrics

## 🚨 Troubleshooting

### Common Issues

**1. Database Connection Errors**
```bash
# Check PostgreSQL container
docker exec bizosaas-postgres-staging psql -U postgres -d bizosaas -c "SELECT 1;"

# Verify credentials in .env file
grep POSTGRES .env
```

**2. Service Not Starting**
```bash
# Check container logs
docker-compose -f docker-compose.staging.yml logs service-name

# Restart specific service
docker-compose -f docker-compose.staging.yml restart service-name
```

**3. Port Conflicts**
```bash
# Check what's using a port
lsof -i :8080

# Stop conflicting services
sudo systemctl stop service-name
```

### Recovery Commands
```bash
# Complete restart
docker-compose -f docker-compose.staging.yml down
docker-compose -f docker-compose.staging.yml up -d

# Reset database (WARNING: Data loss)
docker-compose -f docker-compose.staging.yml down -v
docker volume rm bizosaas-staging_postgres_data
```

## 📈 Performance Optimization

### Resource Allocation
- **API Gateway**: 1GB RAM, 1 CPU core
- **AI Agents**: 2GB RAM, 2 CPU cores (AI-intensive)
- **PostgreSQL**: 1GB RAM, 1 CPU core
- **Redis**: 512MB RAM

### Scaling Recommendations
- Use load balancer for multiple API Gateway instances
- Separate AI Agents into specialized containers
- Implement horizontal pod autoscaling for high traffic

## ✅ Success Criteria

The deployment is successful when:
1. ✅ All health checks return 200 OK
2. ✅ PostgreSQL and Redis are accessible
3. ✅ AI Agents respond with 46+ available agents
4. ✅ Frontend applications load without errors
5. ✅ SSL certificates are valid and working
6. ✅ Monitoring and logging are functional

## 🎉 Next Steps

After successful staging deployment:
1. **Load Testing**: Use tools like k6 or Apache Bench
2. **Security Audit**: Run security scans and penetration tests
3. **Backup Testing**: Verify backup and restore procedures
4. **Production Deployment**: Repeat process for production environment
5. **CI/CD Pipeline**: Set up automated deployments from Git

---

*This deployment guide ensures a reliable, secure, and scalable deployment of the BizOSaaS Autonomous AI Agents Platform.*