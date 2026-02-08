#!/bin/bash

# BizOSaaS Platform - Complete VPS Deployment Script
# Target VPS: 194.238.16.237
# Dokploy Admin: bizoholic.digital@gmail.com
# Repository: https://github.com/Bizoholic-Digital/bizosaas-platform.git
# Date: October 9, 2025

set -e  # Exit on any error

echo "🚀 Starting BizOSaaS Platform VPS Deployment..."
echo "📅 Date: $(date)"
echo "🏗️ Target: 194.238.16.237 (Dokploy)"
echo "📋 Repository: Bizoholic-Digital/bizosaas-platform"
echo ""

# Configuration
VPS_IP="194.238.16.237"
REPO_URL="https://github.com/Bizoholic-Digital/bizosaas-platform.git"
DOKPLOY_EMAIL="bizoholic.digital@gmail.com"

# Phase 1: Prepare local images for VPS deployment
echo "🔧 Phase 1: Building and preparing Docker images for VPS deployment..."

# Build Bizoholic Frontend image
echo "📦 Building Bizoholic Frontend image..."
cd /home/alagiri/projects/bizoholic/bizosaas/frontend/apps/bizoholic-frontend
docker build -t bizosaas/bizoholic-frontend:latest .

# Build Brain Core API image
echo "📦 Building Brain Core API image..."
cd /home/alagiri/projects/bizoholic/bizosaas-platform/ai/services/bizosaas-brain
docker build -t bizosaas/brain:latest .

echo "✅ Phase 1 Complete - Docker images built locally"
echo ""

# Phase 2: Create deployment configuration
echo "🛠️ Phase 2: Creating VPS deployment configuration..."

# Create deployment directory
mkdir -p /tmp/bizosaas-vps-deploy

# Create docker-compose for Bizoholic complete stack
cat > /tmp/bizosaas-vps-deploy/docker-compose.bizoholic.yml << 'EOF'
# Complete Bizoholic Stack for VPS Deployment
# Phase 1: Essential services for immediate deployment

services:
  # ========================================================================================
  # POSTGRESQL DATABASE - Shared infrastructure
  # ========================================================================================
  postgres:
    image: postgres:15-alpine
    container_name: bizosaas-postgres
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_PASSWORD=BizOSaaS2025!SecureDB
      - POSTGRES_USER=postgres
      - POSTGRES_DB=bizosaas_main
      - POSTGRES_INITDB_ARGS=--auth-host=scram-sha-256
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    networks:
      - dokploy-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 5

  # ========================================================================================
  # REDIS CACHE - Shared infrastructure
  # ========================================================================================
  redis:
    image: redis:7-alpine
    container_name: bizosaas-redis
    ports:
      - "6379:6379"
    environment:
      - REDIS_PASSWORD=SecureRedis2025!BizOSaaS
    command: redis-server --requirepass SecureRedis2025!BizOSaaS
    volumes:
      - redis-data:/data
    networks:
      - dokploy-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5

  # ========================================================================================
  # BRAIN CORE API - Central FastAPI Hub (Port 8001)
  # ========================================================================================
  bizosaas-brain:
    image: bizosaas/brain:latest
    container_name: bizosaas-brain-api
    ports:
      - "8001:8001"
    environment:
      - POSTGRES_HOST=postgres
      - POSTGRES_PASSWORD=BizOSaaS2025!SecureDB
      - POSTGRES_USER=postgres
      - POSTGRES_DB=bizosaas_main
      - REDIS_HOST=redis
      - REDIS_PASSWORD=SecureRedis2025!BizOSaaS
      - JWT_SECRET_KEY=bizosaas-super-secret-jwt-key-production-2025-very-long-secure
OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - ENVIRONMENT=production
      - DEBUG=false
      - LOG_LEVEL=info
      - ALLOWED_HOSTS=api.bizoholic.com,localhost,127.0.0.1
    networks:
      - dokploy-network
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 5
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.bizosaas-brain.rule=Host(`api.bizoholic.com`)"
      - "traefik.http.services.bizosaas-brain.loadbalancer.server.port=8001"
      - "traefik.http.routers.bizosaas-brain.tls=true"
      - "traefik.http.routers.bizosaas-brain.tls.certresolver=letsencrypt"

  # ========================================================================================
  # BIZOHOLIC FRONTEND - Marketing website (Port 3000)
  # ========================================================================================
  bizoholic-frontend:
    image: bizosaas/bizoholic-frontend:latest
    container_name: bizoholic-frontend
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_BASE_URL=https://api.bizoholic.com
      - NEXT_PUBLIC_SITE_NAME=Bizoholic Digital
      - NEXT_PUBLIC_SITE_DESCRIPTION=AI-Powered Marketing Agency Platform
      - NEXT_PUBLIC_DOMAIN=bizoholic.com
      - PORT=3000
      - HOSTNAME=0.0.0.0
    networks:
      - dokploy-network
    depends_on:
      bizosaas-brain:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000/"]
      interval: 30s
      timeout: 10s
      retries: 5
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.bizoholic-frontend.rule=Host(`bizoholic.com`) || Host(`www.bizoholic.com`)"
      - "traefik.http.services.bizoholic-frontend.loadbalancer.server.port=3000"
      - "traefik.http.routers.bizoholic-frontend.tls=true"
      - "traefik.http.routers.bizoholic-frontend.tls.certresolver=letsencrypt"

volumes:
  postgres-data:
    name: bizosaas-postgres-data
  redis-data:
    name: bizosaas-redis-data

networks:
  dokploy-network:
    external: true
EOF

# Create database initialization script
cat > /tmp/bizosaas-vps-deploy/init-db.sql << 'EOF'
-- BizOSaaS Database Initialization Script
-- Create databases and extensions for the platform

-- Create databases
CREATE DATABASE wagtail_storage;
CREATE DATABASE saleor_storage;
CREATE DATABASE django_crm_storage;

-- Connect to main database and create extensions
\c bizosaas_main;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Connect to wagtail database and create extensions
\c wagtail_storage;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Connect to saleor database and create extensions
\c saleor_storage;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Connect to CRM database and create extensions
\c django_crm_storage;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE bizosaas_main TO postgres;
GRANT ALL PRIVILEGES ON DATABASE wagtail_storage TO postgres;
GRANT ALL PRIVILEGES ON DATABASE saleor_storage TO postgres;
GRANT ALL PRIVILEGES ON DATABASE django_crm_storage TO postgres;
EOF

echo "✅ Phase 2 Complete - Deployment configuration created"
echo ""

# Phase 3: Push Docker images to a registry (for VPS access)
echo "🐳 Phase 3: Preparing images for VPS deployment..."

# Tag images for deployment
docker tag bizosaas/bizoholic-frontend:latest bizosaas/bizoholic-frontend:vps-deploy
docker tag bizosaas/brain:latest bizosaas/brain:vps-deploy

echo "✅ Phase 3 Complete - Images tagged for deployment"
echo ""

# Phase 4: Generate deployment instructions
echo "📋 Phase 4: Generating deployment instructions..."

cat > /tmp/bizosaas-vps-deploy/DEPLOYMENT_INSTRUCTIONS.md << 'EOF'
# BizOSaaS VPS Deployment Instructions

## 🎯 Deployment Overview
This deployment includes:
- ✅ PostgreSQL Database (Port 5432)
- ✅ Redis Cache (Port 6379)
- ✅ Brain Core API (Port 8001) → api.bizoholic.com
- ✅ Bizoholic Frontend (Port 3000) → bizoholic.com

## 🚀 Dokploy Deployment Steps

### Step 1: Access Dokploy Dashboard
1. Navigate to: http://194.238.16.237:3000
2. Login with: bizoholic.digital@gmail.com

### Step 2: Create New Project
1. Click "Create Project"
2. Project name: `bizosaas-bizoholic`
3. Description: `Complete Bizoholic Platform - Phase 1`

### Step 3: Add Service Stack
1. Choose "Docker Compose"
2. Upload: `docker-compose.bizoholic.yml`
3. Upload: `init-db.sql` (place in same directory)

### Step 4: Configure Environment
Add these environment variables in Dokploy:
```
POSTGRES_PASSWORD=BizOSaaS2025!SecureDB
REDIS_PASSWORD=SecureRedis2025!BizOSaaS
JWT_SECRET_KEY=bizosaas-super-secret-jwt-key-production-2025-very-long-secure
OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
```

### Step 5: Configure Domains
In Dokploy domain settings:
- `bizoholic.com` → bizoholic-frontend (Port 3000)
- `www.bizoholic.com` → bizoholic-frontend (Port 3000)
- `api.bizoholic.com` → bizosaas-brain (Port 8001)

### Step 6: Deploy Stack
1. Click "Deploy"
2. Monitor deployment logs
3. Wait for all services to be healthy

### Step 7: Verify Deployment
Test these URLs:
- https://bizoholic.com (Marketing website)
- https://api.bizoholic.com/health (API health check)
- https://api.bizoholic.com (API documentation)

## 🔧 Post-Deployment Steps

### Initialize Database
The database will auto-initialize with the init-db.sql script.

### Update DNS Records
Point these domains to 194.238.16.237:
- bizoholic.com
- www.bizoholic.com
- api.bizoholic.com

### SSL Certificates
Dokploy will automatically generate Let's Encrypt SSL certificates.

## 📊 Monitoring

### Health Checks
All services include health checks:
- PostgreSQL: pg_isready
- Redis: redis-cli ping
- Brain API: curl /health
- Frontend: wget spider check

### Service Dependencies
- Frontend depends on Brain API
- Brain API depends on PostgreSQL + Redis
- Proper startup order enforced

## 🚨 Troubleshooting

### Common Issues
1. **Domain not resolving**: Check DNS propagation
2. **SSL certificate issues**: Wait 5-10 minutes for Let's Encrypt
3. **Database connection issues**: Check PostgreSQL logs
4. **Frontend 404 errors**: Verify Brain API is responding

### Logs Access
In Dokploy dashboard:
1. Go to Services → [service-name]
2. Click "Logs" tab
3. View real-time logs

### Service Restart
If a service fails:
1. Go to Services → [service-name]
2. Click "Restart"
3. Monitor health checks

## 📈 Next Phase
After successful deployment:
1. Deploy Wagtail CMS (bizosaas-storage project)
2. Deploy CorelDove e-commerce
3. Deploy client portal
4. Complete integration testing
EOF

echo "✅ Phase 4 Complete - Deployment instructions generated"
echo ""

# Phase 5: Create final deployment package
echo "📦 Phase 5: Creating final deployment package..."

cd /tmp/bizosaas-vps-deploy
tar -czf bizosaas-vps-deployment-$(date +%Y%m%d-%H%M%S).tar.gz *.yml *.sql *.md

echo "✅ Phase 5 Complete - Deployment package created"
echo ""

echo "🎉 BizOSaaS VPS Deployment Preparation Complete!"
echo ""
echo "📁 Deployment files created in: /tmp/bizosaas-vps-deploy/"
echo "📋 Next steps:"
echo "  1. Copy deployment files to VPS or use Dokploy dashboard"
echo "  2. Follow DEPLOYMENT_INSTRUCTIONS.md"
echo "  3. Deploy using docker-compose.bizoholic.yml"
echo "  4. Configure domains and SSL"
echo "  5. Test all endpoints"
echo ""
echo "🌐 Expected URLs after deployment:"
echo "  - https://bizoholic.com (Marketing website)"
echo "  - https://api.bizoholic.com (Central API)"
echo "  - https://api.bizoholic.com/health (Health check)"
echo ""
echo "✨ Happy deploying! 🚀"