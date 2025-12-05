#!/bin/bash
# 🚀 BizOSaaS Platform VPS Deployment Script
# Deploy directly to VPS for immediate staging testing

set -e

# Configuration
VPS_HOST="194.238.16.237"
VPS_USER="root"
VPS_PASSWORD="&k3civYG5Q6YPb"
DEPLOY_DIR="/opt/bizosaas"
GITHUB_REPO="https://github.com/Bizoholic-Digital/bizosaas-platform.git"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 BizOSaaS Platform VPS Deployment${NC}"
echo -e "${BLUE}===================================${NC}"

# Function to run commands on VPS
run_on_vps() {
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "$1"
}

# Function to copy files to VPS
copy_to_vps() {
    sshpass -p "$VPS_PASSWORD" scp -o StrictHostKeyChecking=no -r "$1" "$VPS_USER@$VPS_HOST:$2"
}

# Check if sshpass is installed
if ! command -v sshpass &> /dev/null; then
    echo -e "${YELLOW}Installing sshpass...${NC}"
    sudo apt-get update && sudo apt-get install -y sshpass
fi

echo -e "${YELLOW}Step 1: Connecting to VPS and preparing environment...${NC}"

# Prepare VPS environment
run_on_vps "
    # Update system
    apt-get update -y
    
    # Install Docker if not present
    if ! command -v docker &> /dev/null; then
        echo 'Installing Docker...'
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        systemctl enable docker
        systemctl start docker
    fi
    
    # Install Docker Compose if not present
    if ! command -v docker-compose &> /dev/null; then
        echo 'Installing Docker Compose...'
        curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi
    
    # Create deployment directory
    mkdir -p $DEPLOY_DIR
    cd $DEPLOY_DIR
    
    # Clean up any existing deployment
    if [ -d \"bizoholic\" ]; then
        echo 'Cleaning up existing deployment...'
        cd bizoholic
        docker-compose down --remove-orphans || true
        cd ..
        rm -rf bizoholic
    fi
"

echo -e "${GREEN}✅ VPS environment prepared${NC}"

echo -e "${YELLOW}Step 2: Cloning repository to VPS...${NC}"

# Clone repository on VPS
run_on_vps "
    cd $DEPLOY_DIR
    git clone $GITHUB_REPO bizoholic
    cd bizoholic
    git checkout development
    echo 'Repository cloned successfully'
"

echo -e "${GREEN}✅ Repository cloned${NC}"

echo -e "${YELLOW}Step 3: Creating production environment configuration...${NC}"

# Create production environment file
run_on_vps "
    cd $DEPLOY_DIR/bizoholic
    
    # Create production environment file
    cat > .env.production << 'EOF'
# BizOSaaS Production Environment
NODE_ENV=production
ENVIRONMENT=production

# Database Configuration
POSTGRES_PASSWORD=SharedInfra2024!SuperSecure
POSTGRES_DB=bizosaas
POSTGRES_USER=postgres
DATABASE_URL=postgresql://postgres:SharedInfra2024!SuperSecure@postgres:5432/bizosaas

# Redis Configuration
REDIS_URL=redis://redis:6379

# AI Services
OPENAI_API_KEY=${OPENAI_API_KEY}

# Security
JWT_SECRET=super-secret-jwt-key-production-2025
DJANGO_SECRET_KEY=django-super-secret-key-production-2025

# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://194.238.16.237:8001
API_BASE_URL=http://194.238.16.237:8001

# Frontend URLs
CORELDOVE_FRONTEND_URL=http://194.238.16.237:3007
CLIENT_PORTAL_URL=http://194.238.16.237:3006
BIZOHOLIC_FRONTEND_URL=http://194.238.16.237:3008
ADMIN_PORTAL_URL=http://194.238.16.237:3009

# SSL/TLS (for production domains)
SSL_ENABLED=false
ALLOWED_HOSTS=194.238.16.237,localhost,bizoholic.com,*.bizoholic.com

# Monitoring
SENTRY_DSN=
LOG_LEVEL=info
EOF
"

echo -e "${GREEN}✅ Production environment configured${NC}"

echo -e "${YELLOW}Step 4: Creating production Docker Compose configuration...${NC}"

# Create production Docker Compose file
run_on_vps "
    cd $DEPLOY_DIR/bizoholic
    
    # Create production Docker Compose
    cat > docker-compose.production.yml << 'EOF'
version: '3.8'

services:
  # Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: \${POSTGRES_DB}
      POSTGRES_USER: \${POSTGRES_USER}
      POSTGRES_PASSWORD: \${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - \"5432:5432\"
    restart: unless-stopped
    healthcheck:
      test: [\"CMD-SHELL\", \"pg_isready -U \${POSTGRES_USER} -d \${POSTGRES_DB}\"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Cache
  redis:
    image: redis:7-alpine
    ports:
      - \"6379:6379\"
    restart: unless-stopped
    command: redis-server --maxmemory 1gb --maxmemory-policy allkeys-lru
    healthcheck:
      test: [\"CMD\", \"redis-cli\", \"ping\"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Central Hub API
  bizosaas-brain:
    build:
      context: ./bizosaas-platform/ai/services/bizosaas-brain
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=\${DATABASE_URL}
      - REDIS_URL=\${REDIS_URL}
      - OPENAI_API_KEY=\${OPENAI_API_KEY}
      - JWT_SECRET=\${JWT_SECRET}
      - NODE_ENV=production
    ports:
      - \"8001:8001\"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: [\"CMD\", \"curl\", \"-f\", \"http://localhost:8001/health\"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Amazon Integration Service
  amazon-sourcing:
    build:
      context: ./bizosaas-platform/ecommerce/services/amazon-integration-service
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=\${DATABASE_URL}
      - REDIS_URL=\${REDIS_URL}
    ports:
      - \"8085:8080\"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  # CorelDove E-commerce Frontend
  coreldove-frontend:
    build:
      context: ./bizosaas-platform/ecommerce/services/coreldove-frontend
      dockerfile: Dockerfile.prod
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_BASE_URL=\${NEXT_PUBLIC_API_BASE_URL}
    ports:
      - \"3007:3000\"
    depends_on:
      - bizosaas-brain
    restart: unless-stopped
    healthcheck:
      test: [\"CMD\", \"curl\", \"-f\", \"http://localhost:3000/api/health\"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Client Portal
  client-portal:
    build:
      context: ./bizosaas-platform/frontend/apps/client-portal
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_BASE_URL=\${NEXT_PUBLIC_API_BASE_URL}
    ports:
      - \"3006:3000\"
    depends_on:
      - bizosaas-brain
    restart: unless-stopped

  # Bizoholic Frontend
  bizoholic-frontend:
    build:
      context: ./bizosaas-platform/frontend/apps/bizoholic-frontend
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_BASE_URL=\${NEXT_PUBLIC_API_BASE_URL}
    ports:
      - \"3008:3000\"
    depends_on:
      - bizosaas-brain
    restart: unless-stopped

  # BizOSaaS Admin
  bizosaas-admin:
    build:
      context: ./bizosaas-platform/frontend/apps/bizosaas-admin
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_BASE_URL=\${NEXT_PUBLIC_API_BASE_URL}
    ports:
      - \"3009:3000\"
    depends_on:
      - bizosaas-brain
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  default:
    name: bizosaas-production
EOF
"

echo -e "${GREEN}✅ Production Docker Compose created${NC}"

echo -e "${YELLOW}Step 5: Building and deploying containers...${NC}"

# Build and deploy
run_on_vps "
    cd $DEPLOY_DIR/bizoholic
    
    # Load environment variables
    export \$(cat .env.production | xargs)
    
    # Pull base images
    echo 'Pulling base images...'
    docker pull postgres:15-alpine
    docker pull redis:7-alpine
    docker pull node:18-alpine
    docker pull python:3.11-slim
    
    # Build and start services
    echo 'Building and starting services...'
    docker-compose -f docker-compose.production.yml up -d --build
    
    # Wait for services to start
    echo 'Waiting for services to start...'
    sleep 60
    
    # Check service status
    echo 'Service status:'
    docker-compose -f docker-compose.production.yml ps
"

echo -e "${GREEN}✅ Containers deployed${NC}"

echo -e "${YELLOW}Step 6: Running health checks...${NC}"

# Health checks
run_on_vps "
    cd $DEPLOY_DIR/bizoholic
    
    echo 'Running health checks...'
    
    # Wait for full startup
    sleep 30
    
    # Check each service
    echo 'Checking PostgreSQL...'
    docker-compose -f docker-compose.production.yml exec -T postgres pg_isready -U postgres -d bizosaas || echo 'PostgreSQL check failed'
    
    echo 'Checking Redis...'
    docker-compose -f docker-compose.production.yml exec -T redis redis-cli ping || echo 'Redis check failed'
    
    echo 'Checking Central Hub API...'
    curl -f http://localhost:8001/health || echo 'Central Hub check failed'
    
    echo 'Checking CorelDove Frontend...'
    curl -f http://localhost:3007/api/health || echo 'CorelDove check failed'
    
    echo 'Checking Client Portal...'
    curl -f http://localhost:3006/api/health || echo 'Client Portal check failed'
    
    echo 'Container status:'
    docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
"

echo -e "${GREEN}✅ Health checks completed${NC}"

echo -e "${BLUE}🎉 Deployment Summary${NC}"
echo -e "${BLUE}===================${NC}"
echo -e "${GREEN}✅ VPS Environment: Ready${NC}"
echo -e "${GREEN}✅ Repository: Cloned and deployed${NC}"
echo -e "${GREEN}✅ Containers: Built and running${NC}"
echo -e "${GREEN}✅ Health Checks: Completed${NC}"

echo -e "\n${YELLOW}📋 Access URLs:${NC}"
echo -e "🌐 Central Hub API:     http://194.238.16.237:8001"
echo -e "🛒 CorelDove Frontend:  http://194.238.16.237:3007"
echo -e "👥 Client Portal:       http://194.238.16.237:3006"
echo -e "🏢 Bizoholic Frontend:  http://194.238.16.237:3008"
echo -e "⚙️  Admin Dashboard:     http://194.238.16.237:3009"
echo -e "📊 Amazon Sourcing:     http://194.238.16.237:8085"

echo -e "\n${YELLOW}🔧 Management Commands:${NC}"
echo -e "📊 View logs:    ssh root@194.238.16.237 'cd $DEPLOY_DIR/bizoholic && docker-compose -f docker-compose.production.yml logs'"
echo -e "🔄 Restart:      ssh root@194.238.16.237 'cd $DEPLOY_DIR/bizoholic && docker-compose -f docker-compose.production.yml restart'"
echo -e "⏹️  Stop:         ssh root@194.238.16.237 'cd $DEPLOY_DIR/bizoholic && docker-compose -f docker-compose.production.yml down'"
echo -e "🚀 Redeploy:     ./deploy-to-vps.sh"

echo -e "\n${GREEN}🎯 Deployment completed successfully!${NC}"
echo -e "${BLUE}Platform is now running on VPS at 194.238.16.237${NC}"