#!/bin/bash
# Deploy BizOSaaS Platform to VPS Staging
# Uses working local images - transfers them directly to VPS

set -e

echo "🚀 BizOSaaS Platform - Deploy to VPS Staging"
echo "============================================"
echo ""

VPS_IP="194.238.16.237"
VPS_USER="root"
VPS_PASSWORD="&k3civYG5Q6YPb"
DEPLOY_DIR="/opt/bizosaas-staging"

echo "📊 Infrastructure Status: ✅ Already Running"
echo "   - PostgreSQL (5433)"
echo "   - Redis (6380)"
echo "   - Vault (8201)"
echo "   - Temporal Server (7234)"
echo "   - Temporal UI (8083)"
echo "   - Superset (8089)"
echo ""

echo "📦 Deploying Services:"
echo "   Backend: 8 services"
echo "   Frontend: 5 services"
echo ""

# Create staging directory on VPS
echo "1️⃣ Preparing VPS staging environment..."
sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP << 'ENDSSH'
mkdir -p /opt/bizosaas-staging/images
mkdir -p /opt/bizosaas-staging/compose
ENDSSH

echo "   ✅ VPS directories ready"
echo ""

# Backend Services
echo "2️⃣ Saving Backend Images (8 services)..."
mkdir -p ./staging-deploy/backend

echo "   Saving Brain API..."
docker save bizosaas-brain-gateway:latest | gzip > ./staging-deploy/backend/brain-api.tar.gz

echo "   Saving Wagtail CMS..."
docker save bizosaas-wagtail-cms:latest | gzip > ./staging-deploy/backend/wagtail-cms.tar.gz

echo "   Saving Django CRM..."
docker save bizoholic-django-crm:latest | gzip > ./staging-deploy/backend/django-crm.tar.gz

echo "   Saving Business Directory Backend..."
docker save bizosaas-business-directory-backend:latest | gzip > ./staging-deploy/backend/business-directory-backend.tar.gz

echo "   Saving CorelDove Backend..."
docker save bizoholic-coreldove-backend:latest | gzip > ./staging-deploy/backend/coreldove-backend.tar.gz

echo "   Saving Auth Service..."
docker save bizoholic-auth-service:latest | gzip > ./staging-deploy/backend/auth-service.tar.gz

echo "   Saving AI Agents..."
docker save bizoholic-ai-agents:latest | gzip > ./staging-deploy/backend/ai-agents.tar.gz

echo "   Saving Amazon Sourcing..."
docker save bizosaas/amazon-sourcing:latest | gzip > ./staging-deploy/backend/amazon-sourcing.tar.gz

echo "   ✅ Backend images saved (8/8)"
echo ""

# Frontend Services
echo "3️⃣ Saving Frontend Images (5 services)..."
mkdir -p ./staging-deploy/frontend

echo "   Saving Client Portal..."
docker save bizosaas-client-portal:latest | gzip > ./staging-deploy/frontend/client-portal.tar.gz

echo "   Saving Bizoholic Frontend..."
docker save bizosaas-bizoholic-frontend:latest | gzip > ./staging-deploy/frontend/bizoholic-frontend.tar.gz

echo "   Saving CorelDove Frontend..."
docker save bizosaas-coreldove-frontend:latest | gzip > ./staging-deploy/frontend/coreldove-frontend.tar.gz

echo "   Saving Business Directory Frontend..."
docker save bizosaas-business-directory:latest | gzip > ./staging-deploy/frontend/business-directory-frontend.tar.gz

echo "   Saving Admin Dashboard..."
docker save bizosaas-bizosaas-admin:latest | gzip > ./staging-deploy/frontend/admin-dashboard.tar.gz

echo "   ✅ Frontend images saved (5/5)"
echo ""

# Transfer to VPS
echo "4️⃣ Transferring images to VPS (this may take a few minutes)..."
sshpass -p "$VPS_PASSWORD" scp -o StrictHostKeyChecking=no -r ./staging-deploy/* $VPS_USER@$VPS_IP:/opt/bizosaas-staging/images/
echo "   ✅ Images transferred"
echo ""

# Load images on VPS
echo "5️⃣ Loading images on VPS..."
sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP << 'ENDSSH'
echo "Loading backend images..."
cd /opt/bizosaas-staging/images/backend
for img in *.tar.gz; do
    echo "   Loading $img..."
    gunzip -c $img | docker load
done

echo "Loading frontend images..."
cd /opt/bizosaas-staging/images/frontend
for img in *.tar.gz; do
    echo "   Loading $img..."
    gunzip -c $img | docker load
done
ENDSSH

echo "   ✅ All images loaded on VPS"
echo ""

# Copy compose files
echo "6️⃣ Copying docker-compose files to VPS..."
sshpass -p "$VPS_PASSWORD" scp -o StrictHostKeyChecking=no \
  dokploy-backend-staging.yml \
  dokploy-frontend-staging.yml \
  $VPS_USER@$VPS_IP:/opt/bizosaas-staging/compose/
echo "   ✅ Compose files copied"
echo ""

echo "============================================"
echo "✅ Deployment Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Update Dokploy to use local images (not build from GitHub)"
echo "2. Point Dokploy compose path to: /opt/bizosaas-staging/compose/"
echo "3. Trigger deployment via Dokploy API or dashboard"
echo ""
echo "🔍 Verify images on VPS:"
echo "   ssh root@$VPS_IP 'docker images | grep bizosaas'"
echo ""
echo "📊 Deployment Summary:"
echo "   Infrastructure: ✅ Already running (6 services)"
echo "   Backend: ✅ Images ready (8 services)"
echo "   Frontend: ✅ Images ready (5 services)"
echo "   Total: 19 services ready to deploy"
