#!/bin/bash
# Setup Proper Deployment Workflow: Local → GHCR → GitHub → Dokploy
set -e

echo "🔧 Setting up proper deployment workflow"
echo "========================================"
echo ""

GITHUB_TOKEN="${GITHUB_TOKEN:-}"
REGISTRY="ghcr.io/bizoholic-digital/bizosaas-platform"
TAG="staging"

# Step 1: Login to GHCR with proper permissions
echo "1️⃣ Authenticating with GHCR..."
if [ -z "$GITHUB_TOKEN" ]; then
    echo "   ❌ Error: GITHUB_TOKEN environment variable not set"
    echo "   Please run: export GITHUB_TOKEN=your_token_here"
    exit 1
fi
echo "$GITHUB_TOKEN" | docker login ghcr.io -u bizoholic-digital --password-stdin

if [ $? -eq 0 ]; then
    echo "   ✅ GHCR authentication successful"
else
    echo "   ❌ GHCR authentication failed"
    exit 1
fi
echo ""

# Step 2: Push backend images to GHCR
echo "2️⃣ Pushing Backend Images to GHCR (7 services)..."
echo ""

echo "   1/7 Brain API..."
docker tag bizosaas-brain-gateway:latest $REGISTRY/brain-api:$TAG
docker push $REGISTRY/brain-api:$TAG

echo "   2/7 Wagtail CMS..."
docker tag bizosaas-wagtail-cms:latest $REGISTRY/wagtail-cms:$TAG
docker push $REGISTRY/wagtail-cms:$TAG

echo "   3/7 Django CRM..."
docker tag bizoholic-django-crm:latest $REGISTRY/django-crm:$TAG
docker push $REGISTRY/django-crm:$TAG

echo "   4/7 Business Directory Backend..."
docker tag bizosaas-business-directory-backend:latest $REGISTRY/business-directory-backend:$TAG
docker push $REGISTRY/business-directory-backend:$TAG

echo "   5/7 CorelDove Backend..."
docker tag bizoholic-coreldove-backend:latest $REGISTRY/coreldove-backend:$TAG
docker push $REGISTRY/coreldove-backend:$TAG

echo "   6/7 AI Agents..."
docker tag bizoholic-ai-agents:latest $REGISTRY/ai-agents:$TAG
docker push $REGISTRY/ai-agents:$TAG

echo "   7/7 Amazon Sourcing..."
docker tag bizosaas/amazon-sourcing:latest $REGISTRY/amazon-sourcing:$TAG
docker push $REGISTRY/amazon-sourcing:$TAG

echo ""
echo "   ✅ Backend images pushed (7/7)"
echo ""

# Step 3: Push frontend images to GHCR
echo "3️⃣ Pushing Frontend Images to GHCR (5 services)..."
echo ""

echo "   1/5 Client Portal..."
docker tag bizosaas-client-portal:latest $REGISTRY/client-portal:$TAG
docker push $REGISTRY/client-portal:$TAG

echo "   2/5 Bizoholic Frontend..."
docker tag bizosaas-bizoholic-frontend:latest $REGISTRY/bizoholic-frontend:$TAG
docker push $REGISTRY/bizoholic-frontend:$TAG

echo "   3/5 CorelDove Frontend..."
docker tag bizosaas-coreldove-frontend:latest $REGISTRY/coreldove-frontend:$TAG
docker push $REGISTRY/coreldove-frontend:$TAG

echo "   4/5 Business Directory Frontend..."
docker tag bizosaas-business-directory:latest $REGISTRY/business-directory-frontend:$TAG
docker push $REGISTRY/business-directory-frontend:$TAG

echo "   5/5 Admin Dashboard..."
docker tag bizosaas-bizosaas-admin:latest $REGISTRY/admin-dashboard:$TAG
docker push $REGISTRY/admin-dashboard:$TAG

echo ""
echo "   ✅ Frontend images pushed (5/5)"
echo ""

echo "========================================"
echo "✅ GHCR Workflow Setup Complete!"
echo ""
echo "📊 Images Pushed:"
echo "   Backend: 7/7 ✅"
echo "   Frontend: 5/5 ✅"
echo "   Total: 12/12 ✅"
echo ""
echo "🔗 View images at:"
echo "   https://github.com/orgs/bizoholic-digital/packages?repo_name=bizosaas-platform"
echo ""
echo "📋 Next Steps:"
echo "1. Update dokploy compose files to use GHCR images"
echo "2. Push compose files to GitHub"
echo "3. Trigger Dokploy deployment via API"
echo ""
