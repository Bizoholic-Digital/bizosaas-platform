#!/bin/bash

# BizOSaaS Platform - Configure Frontends for VPS Deployment via Brain Gateway
# Updates all frontends to use production Brain Gateway on VPS
# Date: November 17, 2025

set -e

echo "=========================================="
echo "🚀 Configuring Frontends for VPS Deployment"
echo "=========================================="
echo ""
echo "This script configures all 7 frontends to use"
echo "the centralized Brain Gateway on production VPS"
echo ""

# Base directory
BASE_DIR="/home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps"

# VPS Production Configuration
BRAIN_GATEWAY_URL_PROD="https://api.bizoholic.com"
BRAIN_GATEWAY_URL_LOCAL="http://backend-brain-gateway:8001"

echo "📋 Configuration:"
echo "  Production Brain Gateway: $BRAIN_GATEWAY_URL_PROD"
echo "  Internal Service URL: $BRAIN_GATEWAY_URL_LOCAL"
echo ""

# Function to create production .env.production for each frontend
create_env_production() {
    local app_name=$1
    local app_dir=$2
    local port=$3
    local app_url=$4
    local platform=$5

    echo "📝 Creating .env.production for $app_name..."

    cat > "$app_dir/.env.production" << EOF
# Brain Gateway Configuration (Production VPS)
NEXT_PUBLIC_API_URL=$BRAIN_GATEWAY_URL_PROD
NEXT_PUBLIC_API_BASE_URL=$BRAIN_GATEWAY_URL_PROD
NEXT_PUBLIC_BRAIN_GATEWAY_URL=$BRAIN_GATEWAY_URL_PROD

# Authentication (through Brain Gateway)
NEXT_PUBLIC_AUTH_API_URL=$BRAIN_GATEWAY_URL_PROD/auth

# Platform Configuration
NEXT_PUBLIC_APP_URL=$app_url
NEXT_PUBLIC_PLATFORM_NAME=$platform
NEXT_PUBLIC_TENANT_SLUG=$platform

# Production Port
PORT=$port

# Feature Flags
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
NEXT_PUBLIC_ENABLE_HITL=true
NEXT_PUBLIC_ENABLE_ANALYTICS=true

# Environment
NODE_ENV=production
EOF

    echo "✅ Created .env.production for $app_name"
}

# 1. Bizoholic Frontend
create_env_production \
    "Bizoholic Frontend" \
    "$BASE_DIR/bizoholic-frontend" \
    "3001" \
    "https://stg.bizoholic.com" \
    "bizoholic"

# 2. CoreLDove Storefront (Saleor-based)
cat > "$BASE_DIR/coreldove-storefront/.env.production" << EOF
# Brain Gateway Configuration (Production)
NEXT_PUBLIC_API_BASE_URL=$BRAIN_GATEWAY_URL_PROD
NEXT_PUBLIC_SALEOR_API_URL=$BRAIN_GATEWAY_URL_PROD/graphql
NEXT_PUBLIC_AUTH_API_URL=$BRAIN_GATEWAY_URL_PROD/auth

# Storefront Configuration
NEXT_PUBLIC_STOREFRONT_URL=https://stg.coreldove.com
NEXT_PUBLIC_STOREFRONT_NAME=CoreLdove
NEXT_PUBLIC_PLATFORM_NAME=coreldove
NEXT_PUBLIC_TENANT_SLUG=coreldove

# Saleor Channel
SALEOR_CHANNEL=default-channel

# Feature Flags
NEXT_PUBLIC_ENABLE_ACCOUNT=true
NEXT_PUBLIC_ENABLE_CHECKOUT=true

# Environment
NODE_ENV=production
PORT=3002
EOF
echo "✅ Created CoreLDove Storefront .env.production"

# 3. Client Portal
create_env_production \
    "Client Portal" \
    "$BASE_DIR/client-portal" \
    "3003" \
    "https://stg.bizoholic.com/portal" \
    "client-portal"

# 4. Business Directory
create_env_production \
    "Business Directory" \
    "$BASE_DIR/business-directory" \
    "3004" \
    "https://stg.bizoholic.com/directory" \
    "business-directory"

# 5. BizOSaaS Admin
cat > "$BASE_DIR/bizosaas-admin/.env.production" << EOF
# Brain Gateway Configuration (Production)
NEXT_PUBLIC_API_URL=$BRAIN_GATEWAY_URL_PROD
NEXT_PUBLIC_BRAIN_GATEWAY_URL=$BRAIN_GATEWAY_URL_PROD
NEXT_PUBLIC_AUTH_API_URL=$BRAIN_GATEWAY_URL_PROD/auth

# Admin API
NEXT_PUBLIC_ADMIN_API_URL=$BRAIN_GATEWAY_URL_PROD/admin

# Platform Configuration
NEXT_PUBLIC_APP_URL=https://admin.bizoholic.com
NEXT_PUBLIC_PLATFORM_NAME=bizosaas-admin
NEXT_PUBLIC_REQUIRED_ROLE=SUPER_ADMIN

# Production Port
PORT=3005

# Environment
NODE_ENV=production
EOF
echo "✅ Created BizOSaaS Admin .env.production"

# 6. ThrillRing Gaming
cat > "$BASE_DIR/thrillring-gaming/.env.production" << EOF
# Brain Gateway Configuration (Production)
NEXT_PUBLIC_API_URL=$BRAIN_GATEWAY_URL_PROD
NEXT_PUBLIC_GAMING_API_URL=$BRAIN_GATEWAY_URL_PROD/gaming
NEXT_PUBLIC_AUTH_API_URL=$BRAIN_GATEWAY_URL_PROD/auth
NEXT_PUBLIC_WEBSOCKET_URL=wss://api.bizoholic.com/gaming/ws

# Platform Configuration
NEXT_PUBLIC_APP_URL=https://stg.thrillring.com
NEXT_PUBLIC_PLATFORM_NAME=thrillring
NEXT_PUBLIC_TENANT_SLUG=thrillring

# Production Port
PORT=3006

# Feature Flags
NEXT_PUBLIC_ENABLE_TOURNAMENTS=true
NEXT_PUBLIC_ENABLE_LEADERBOARD=true

# Environment
NODE_ENV=production
EOF
echo "✅ Created ThrillRing Gaming .env.production"

# 7. Analytics Dashboard
create_env_production \
    "Analytics Dashboard" \
    "$BASE_DIR/analytics-dashboard" \
    "3007" \
    "https://analytics.bizoholic.com" \
    "analytics"

echo ""
echo "=========================================="
echo "📄 Creating Dockerfiles for Production"
echo "=========================================="
echo ""

# Create Brain Gateway Dockerfile for production
cat > "$BASE_DIR/../../../ai/services/bizosaas-brain/Dockerfile.production" << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl gcc wget unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements-simple.txt .
RUN pip install --no-cache-dir -r requirements-simple.txt

# Copy application code
COPY . .

# Environment variables
ENV PYTHONPATH=/app
ENV BRAIN_API_URL=http://0.0.0.0:8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Run the Brain Gateway
EXPOSE 8001
CMD ["python", "-m", "uvicorn", "simple_api:app", "--host", "0.0.0.0", "--port", "8001"]
EOF
echo "✅ Created Brain Gateway Dockerfile.production"

echo ""
echo "=========================================="
echo "📦 Creating GitHub Actions for GHCR Deploy"
echo "=========================================="
echo ""

# Create GitHub Actions workflow for Brain Gateway
cat > "/home/alagiri/projects/bizosaas-platform/.github/workflows/deploy-brain-gateway.yml" << 'EOF'
name: Deploy Brain Gateway to GHCR

on:
  push:
    branches: [main]
    paths:
      - 'bizosaas/ai/services/bizosaas-brain/**'
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}-brain-gateway

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: ./bizosaas/ai/services/bizosaas-brain
          file: ./bizosaas/ai/services/bizosaas-brain/Dockerfile.production
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
EOF
echo "✅ Created GitHub Actions workflow for Brain Gateway"

echo ""
echo "=========================================="
echo "📊 Summary"
echo "=========================================="
echo ""
echo "✅ Created .env.production files for all 7 frontends"
echo "✅ All frontends configured to use Brain Gateway at: $BRAIN_GATEWAY_URL_PROD"
echo "✅ Created production Dockerfiles"
echo "✅ Created GitHub Actions workflow for GHCR deployment"
echo ""
echo "📋 Port Assignments (for Dokploy):"
echo "  - Brain Gateway:          8001 (backend)"
echo "  - Bizoholic Frontend:     3001"
echo "  - CoreLDove Storefront:   3002"
echo "  - Client Portal:          3003"
echo "  - Business Directory:     3004"
echo "  - BizOSaaS Admin:         3005"
echo "  - ThrillRing Gaming:      3006"
echo "  - Analytics Dashboard:    3007"
echo ""
echo "🚀 Next Steps:"
echo "1. Commit and push changes to trigger CI/CD:"
echo "   git add -A"
echo "   git commit -m 'Configure Brain Gateway routing for all frontends'"
echo "   git push origin main"
echo ""
echo "2. Deploy Brain Gateway on VPS:"
echo "   - Will be deployed via GHCR workflow"
echo "   - Configure in Dokploy to pull from ghcr.io"
echo ""
echo "3. Deploy Frontends via Dokploy:"
echo "   - Each frontend will be built on Dokploy"
echo "   - Using GitHub integration already configured"
echo ""
echo "✨ VPS Deployment Configuration Complete!"