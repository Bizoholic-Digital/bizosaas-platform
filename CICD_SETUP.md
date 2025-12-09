# CI/CD Pipeline & Registry Setup

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Development Workflow                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1. Code Push → GitHub                                           │
│  2. GitHub Actions Triggered                                     │
│  3. Build Docker Images                                          │
│  4. Push to Registry (localhost:5000 or Docker Hub)             │
│  5. Deploy to Environment (local/staging/production)            │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 1: Local Domain Setup (bizosaas.local)

### Step 1.1: Configure /etc/hosts

```bash
# Add local domains
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

### Step 1.2: Configure Traefik for Local Domains

Traefik is already running. Let's configure it properly:

```yaml
# File: traefik/traefik.yml

api:
  dashboard: true
  insecure: true

entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
    network: brain-network

certificatesResolvers:
  letsencrypt:
    acme:
      email: admin@bizosaas.local
      storage: /letsencrypt/acme.json
      httpChallenge:
        entryPoint: web
```

### Step 1.3: Update Stack with Traefik Labels

```yaml
# File: docker-compose.registry.yml

version: '3.8'

services:
  # Client Portal with Traefik routing
  client-portal:
    image: localhost:5000/bizosaas/client-portal:latest
    container_name: bizosaas-client-portal
    restart: unless-stopped
    environment:
      - NEXT_PUBLIC_API_URL=https://api.bizosaas.local
      - NEXTAUTH_URL=https://portal.bizosaas.local
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
    networks:
      - brain-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.portal.rule=Host(`portal.bizosaas.local`)"
      - "traefik.http.routers.portal.entrypoints=web"
      - "traefik.http.services.portal.loadbalancer.server.port=3000"
      - "com.bizosaas.service=frontend"

  # Brain Gateway API
  brain-gateway:
    image: localhost:5000/bizosaas/brain-gateway:latest
    container_name: bizosaas-brain-gateway
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/bizosaas
      - REDIS_URL=redis://redis:6379/0
      - VAULT_ADDR=http://vault:8200
      - VAULT_TOKEN=${VAULT_TOKEN}
    networks:
      - brain-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`api.bizosaas.local`)"
      - "traefik.http.routers.api.entrypoints=web"
      - "traefik.http.services.api.loadbalancer.server.port=8000"
      - "com.bizosaas.service=core"

  # Auth Service
  auth-service:
    image: localhost:5000/bizosaas/auth-service:latest
    container_name: bizosaas-auth
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:${POSTGRES_PASSWORD}@postgres:5432/bizosaas
      - REDIS_URL=redis://redis:6379/1
      - JWT_SECRET=${JWT_SECRET}
    networks:
      - brain-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.auth.rule=Host(`auth.bizosaas.local`)"
      - "traefik.http.routers.auth.entrypoints=web"
      - "traefik.http.services.auth.loadbalancer.server.port=8007"
      - "com.bizosaas.service=core"

  # Vault UI
  vault:
    image: hashicorp/vault:latest
    container_name: bizosaas-vault
    restart: unless-stopped
    environment:
      VAULT_DEV_ROOT_TOKEN_ID: ${VAULT_TOKEN:-root}
      VAULT_DEV_LISTEN_ADDRESS: "0.0.0.0:8200"
    networks:
      - brain-network
    cap_add:
      - IPC_LOCK
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.vault.rule=Host(`vault.bizosaas.local`)"
      - "traefik.http.routers.vault.entrypoints=web"
      - "traefik.http.services.vault.loadbalancer.server.port=8200"
      - "com.bizosaas.service=infrastructure"

  # Temporal UI
  temporal-ui:
    image: temporalio/ui:latest
    container_name: bizosaas-temporal-ui
    restart: unless-stopped
    environment:
      - TEMPORAL_ADDRESS=temporal:7233
      - TEMPORAL_CORS_ORIGINS=https://portal.bizosaas.local
    networks:
      - brain-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.temporal.rule=Host(`temporal.bizosaas.local`)"
      - "traefik.http.routers.temporal.entrypoints=web"
      - "traefik.http.services.temporal.loadbalancer.server.port=8080"
      - "com.bizosaas.service=workflow"

  # Grafana
  grafana:
    image: grafana/grafana:latest
    container_name: bizosaas-grafana
    restart: unless-stopped
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_SERVER_ROOT_URL=https://grafana.bizosaas.local
    networks:
      - brain-network
    volumes:
      - grafana-data:/var/lib/grafana
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.grafana.rule=Host(`grafana.bizosaas.local`)"
      - "traefik.http.routers.grafana.entrypoints=web"
      - "traefik.http.services.grafana.loadbalancer.server.port=3000"
      - "com.bizosaas.service=observability"

  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    container_name: bizosaas-prometheus
    restart: unless-stopped
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--web.external-url=https://prometheus.bizosaas.local'
    networks:
      - brain-network
    volumes:
      - ./observability/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.prometheus.rule=Host(`prometheus.bizosaas.local`)"
      - "traefik.http.routers.prometheus.entrypoints=web"
      - "traefik.http.services.prometheus.loadbalancer.server.port=9090"
      - "com.bizosaas.service=observability"

  # Jaeger
  jaeger:
    image: jaegertracing/all-in-one:latest
    container_name: bizosaas-jaeger
    restart: unless-stopped
    networks:
      - brain-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.jaeger.rule=Host(`jaeger.bizosaas.local`)"
      - "traefik.http.routers.jaeger.entrypoints=web"
      - "traefik.http.services.jaeger.loadbalancer.server.port=16686"
      - "com.bizosaas.service=observability"

networks:
  brain-network:
    external: true

volumes:
  grafana-data:
  prometheus-data:
```

---

## Part 2: Docker Registry Setup

### Step 2.1: Verify Local Registry

```bash
# Check if registry is running
docker ps | grep registry

# Test registry
curl http://localhost:5000/v2/_catalog
```

### Step 2.2: Configure Docker to Use Insecure Registry

```bash
# Edit Docker daemon config
sudo tee /etc/docker/daemon.json << EOF
{
  "insecure-registries": ["localhost:5000"],
  "registry-mirrors": []
}
EOF

# Restart Docker
sudo systemctl restart docker
```

### Step 2.3: Build and Push Images Script

```bash
# File: scripts/build-and-push.sh

#!/bin/bash
set -e

REGISTRY="localhost:5000"
VERSION="${1:-latest}"

echo "Building and pushing BizOSaaS images to $REGISTRY..."

# Build Brain Gateway
echo "Building brain-gateway..."
cd bizosaas-brain-core/brain-gateway
docker build -t $REGISTRY/bizosaas/brain-gateway:$VERSION .
docker push $REGISTRY/bizosaas/brain-gateway:$VERSION
cd ../..

# Build Auth Service
echo "Building auth-service..."
cd bizosaas-brain-core/auth
docker build -t $REGISTRY/bizosaas/auth-service:$VERSION .
docker push $REGISTRY/bizosaas/auth-service:$VERSION
cd ../..

# Build Client Portal
echo "Building client-portal..."
cd portals/client-portal
docker build -f Dockerfile.prod -t $REGISTRY/bizosaas/client-portal:$VERSION .
docker push $REGISTRY/bizosaas/client-portal:$VERSION
cd ../..

echo "All images built and pushed successfully!"
echo "Images available at:"
echo "  - $REGISTRY/bizosaas/brain-gateway:$VERSION"
echo "  - $REGISTRY/bizosaas/auth-service:$VERSION"
echo "  - $REGISTRY/bizosaas/client-portal:$VERSION"
```

```bash
# Make executable
chmod +x scripts/build-and-push.sh

# Run
./scripts/build-and-push.sh v1.0.0
```

---

## Part 3: GitHub Actions CI/CD Pipeline

### Step 3.1: Create GitHub Actions Workflow

```yaml
# File: .github/workflows/ci-cd.yml

name: BizOSaaS CI/CD Pipeline

on:
  push:
    branches: [main, develop]
    tags:
      - 'v*'
  pull_request:
    branches: [main, develop]

env:
  REGISTRY: ghcr.io
  IMAGE_PREFIX: ${{ github.repository_owner }}/bizosaas

jobs:
  # Job 1: Lint and Test
  test:
    name: Lint and Test
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install Python dependencies
        run: |
          cd bizosaas-brain-core/brain-gateway
          pip install -r requirements.txt
          pip install pytest black flake8
      
      - name: Run Python linting
        run: |
          cd bizosaas-brain-core/brain-gateway
          black --check app/
          flake8 app/
      
      - name: Run Python tests
        run: |
          cd bizosaas-brain-core/brain-gateway
          pytest tests/ -v
      
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install Node dependencies
        run: |
          cd portals/client-portal
          npm ci
      
      - name: Run TypeScript linting
        run: |
          cd portals/client-portal
          npm run lint
      
      - name: Run TypeScript type check
        run: |
          cd portals/client-portal
          npm run type-check
      
      - name: Build Next.js
        run: |
          cd portals/client-portal
          npm run build

  # Job 2: Build and Push Docker Images
  build:
    name: Build and Push Images
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push'
    
    permissions:
      contents: read
      packages: write
    
    strategy:
      matrix:
        service:
          - name: brain-gateway
            context: ./bizosaas-brain-core/brain-gateway
            dockerfile: Dockerfile
          - name: auth-service
            context: ./bizosaas-brain-core/auth
            dockerfile: Dockerfile
          - name: client-portal
            context: ./portals/client-portal
            dockerfile: Dockerfile.prod
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}-${{ matrix.service.name }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: ${{ matrix.service.context }}
          file: ${{ matrix.service.context }}/${{ matrix.service.dockerfile }}
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      - name: Image digest
        run: echo ${{ steps.meta.outputs.digest }}

  # Job 3: Deploy to Staging
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Deploy to staging server
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.STAGING_HOST }}
          username: ${{ secrets.STAGING_USER }}
          key: ${{ secrets.STAGING_SSH_KEY }}
          script: |
            cd /opt/bizosaas
            docker-compose -f docker-compose.staging.yml pull
            docker-compose -f docker-compose.staging.yml up -d
            docker system prune -f

  # Job 4: Deploy to Production
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    if: startsWith(github.ref, 'refs/tags/v')
    environment:
      name: production
      url: https://portal.bizosaas.com
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Deploy to production server
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /opt/bizosaas
            docker-compose -f docker-compose.prod.yml pull
            docker-compose -f docker-compose.prod.yml up -d
            docker system prune -f
      
      - name: Run health checks
        run: |
          sleep 30
          curl -f https://api.bizosaas.com/health || exit 1
          curl -f https://portal.bizosaas.com || exit 1
      
      - name: Notify deployment
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Production deployment completed!'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
        if: always()
```

### Step 3.2: Create Production Dockerfile for Client Portal

```dockerfile
# File: portals/client-portal/Dockerfile.prod

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --only=production

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 3: Runner
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

### Step 3.3: Update next.config.js for Standalone Build

```javascript
// File: portals/client-portal/next.config.js

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  
  // Enable experimental features
  experimental: {
    optimizePackageImports: ['lucide-react'],
  },
  
  // Image optimization
  images: {
    domains: ['localhost', 'bizosaas.local', 'bizosaas.com'],
  },
  
  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
};

export default nextConfig;
```

---

## Part 4: Environment-Specific Configurations

### Step 4.1: Local Development (.env.local)

```bash
# File: .env.local

# Database
POSTGRES_DB=bizosaas
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Vault
VAULT_TOKEN=root
VAULT_ADDR=http://vault.bizosaas.local

# Auth
JWT_SECRET=local-dev-secret-change-in-production
NEXTAUTH_SECRET=local-nextauth-secret
NEXTAUTH_URL=http://portal.bizosaas.local

# APIs
NEXT_PUBLIC_API_URL=http://api.bizosaas.local
NEXT_PUBLIC_AUTH_URL=http://auth.bizosaas.local

# LLM Keys (optional for local dev)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

### Step 4.2: Staging (.env.staging)

```bash
# File: .env.staging

# Database
POSTGRES_DB=bizosaas_staging
POSTGRES_USER=bizosaas
POSTGRES_PASSWORD=${STAGING_DB_PASSWORD}

# Vault
VAULT_TOKEN=${STAGING_VAULT_TOKEN}
VAULT_ADDR=https://vault.staging.bizosaas.com

# Auth
JWT_SECRET=${STAGING_JWT_SECRET}
NEXTAUTH_SECRET=${STAGING_NEXTAUTH_SECRET}
NEXTAUTH_URL=https://portal.staging.bizosaas.com

# APIs
NEXT_PUBLIC_API_URL=https://api.staging.bizosaas.com
NEXT_PUBLIC_AUTH_URL=https://auth.staging.bizosaas.com
```

### Step 4.3: Production (.env.production)

```bash
# File: .env.production

# Database
POSTGRES_DB=bizosaas_prod
POSTGRES_USER=bizosaas
POSTGRES_PASSWORD=${PROD_DB_PASSWORD}

# Vault
VAULT_TOKEN=${PROD_VAULT_TOKEN}
VAULT_ADDR=https://vault.bizosaas.com

# Auth
JWT_SECRET=${PROD_JWT_SECRET}
NEXTAUTH_SECRET=${PROD_NEXTAUTH_SECRET}
NEXTAUTH_URL=https://portal.bizosaas.com

# APIs
NEXT_PUBLIC_API_URL=https://api.bizosaas.com
NEXT_PUBLIC_AUTH_URL=https://auth.bizosaas.com

# Monitoring
SENTRY_DSN=${SENTRY_DSN}
```

---

## Part 5: Deployment Scripts

### Step 5.1: Local Deployment

```bash
# File: scripts/deploy-local.sh

#!/bin/bash
set -e

echo "Deploying BizOSaaS to local environment..."

# Build images
./scripts/build-and-push.sh latest

# Deploy with docker-compose
docker-compose -f docker-compose.registry.yml --env-file .env.local up -d

echo "Deployment complete!"
echo "Access services at:"
echo "  - Portal: http://portal.bizosaas.local"
echo "  - API: http://api.bizosaas.local/docs"
echo "  - Vault: http://vault.bizosaas.local"
echo "  - Grafana: http://grafana.bizosaas.local"
```

### Step 5.2: Production Deployment

```bash
# File: scripts/deploy-production.sh

#!/bin/bash
set -e

VERSION=$1

if [ -z "$VERSION" ]; then
  echo "Usage: ./deploy-production.sh <version>"
  exit 1
fi

echo "Deploying BizOSaaS v$VERSION to production..."

# Pull images from registry
docker-compose -f docker-compose.prod.yml pull

# Deploy
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d

# Health checks
sleep 30
curl -f https://api.bizosaas.com/health || exit 1
curl -f https://portal.bizosaas.com || exit 1

echo "Production deployment successful!"
```

---

## Part 6: Quick Start Guide

### For Local Development

```bash
# 1. Add local domains to /etc/hosts
sudo tee -a /etc/hosts << EOF
127.0.0.1    bizosaas.local portal.bizosaas.local api.bizosaas.local
EOF

# 2. Build and push to local registry
./scripts/build-and-push.sh latest

# 3. Deploy locally
docker-compose -f docker-compose.registry.yml --env-file .env.local up -d

# 4. Access services
open http://portal.bizosaas.local
```

### For Production

```bash
# 1. Tag release
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 2. GitHub Actions will automatically:
#    - Run tests
#    - Build images
#    - Push to GitHub Container Registry
#    - Deploy to production

# 3. Monitor deployment
#    - Check GitHub Actions tab
#    - Verify health checks
```

---

## Summary

**Recommended Approach**: ✅ **Docker Registry + CI/CD**

**Benefits**:
1. ✅ Automated testing before deployment
2. ✅ Versioned images in registry
3. ✅ Consistent deployments across environments
4. ✅ Easy rollbacks
5. ✅ Production-ready from day one

**Next Steps**:
1. Run `scripts/build-and-push.sh` to build images
2. Configure `/etc/hosts` for local domains
3. Deploy with `docker-compose.registry.yml`
4. Set up GitHub Actions secrets
5. Push to trigger CI/CD pipeline
