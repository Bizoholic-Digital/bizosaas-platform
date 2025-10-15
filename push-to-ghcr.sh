#!/bin/bash
# Push working local images to GitHub Container Registry (GHCR)
# This allows Dokploy to pull tested images instead of building from source

set -e  # Exit on any error

echo "🚀 BizOSaaS Platform - Push Images to GHCR"
echo "=========================================="
echo ""

# Configuration
GITHUB_ORG="bizoholic-digital"
REGISTRY="ghcr.io"
TAG="staging"

# Check if logged in to GHCR
echo "📝 Checking GHCR authentication..."
if ! docker info 2>/dev/null | grep -q "ghcr.io"; then
    echo "⚠️  Not logged in to GHCR. Please run:"
    echo "   export GITHUB_TOKEN=your_token_here"
    echo "   echo \$GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_ORG --password-stdin"
    exit 1
fi

echo "✅ GHCR authentication verified"
echo ""

# Backend Services - Map local images to GHCR names
echo "📦 Backend Services:"
echo "-------------------"

# Brain API Gateway (AI Central Hub)
if docker image inspect bizosaas-brain-gateway:latest >/dev/null 2>&1; then
    echo "1. Pushing Brain API Gateway..."
    docker tag bizosaas-brain-gateway:latest $REGISTRY/$GITHUB_ORG/bizosaas-platform/brain-api:$TAG
    docker push $REGISTRY/$GITHUB_ORG/bizosaas-platform/brain-api:$TAG
    echo "   ✅ Brain API → $REGISTRY/$GITHUB_ORG/bizosaas-platform/brain-api:$TAG"
else
    echo "   ⚠️  Brain API image not found locally"
fi

# Wagtail CMS
if docker image inspect bizosaas-wagtail-cms:latest >/dev/null 2>&1; then
    echo "2. Pushing Wagtail CMS..."
    docker tag bizosaas-wagtail-cms:latest $REGISTRY/$GITHUB_ORG/bizosaas-platform/wagtail-cms:$TAG
    docker push $REGISTRY/$GITHUB_ORG/bizosaas-platform/wagtail-cms:$TAG
    echo "   ✅ Wagtail CMS → $REGISTRY/$GITHUB_ORG/bizosaas-platform/wagtail-cms:$TAG"
else
    echo "   ⚠️  Wagtail CMS image not found locally"
fi

# Business Directory Backend
if docker image inspect bizosaas-business-directory-backend:latest >/dev/null 2>&1; then
    echo "3. Pushing Business Directory Backend..."
    docker tag bizosaas-business-directory-backend:latest $REGISTRY/$GITHUB_ORG/bizosaas-platform/business-directory-backend:$TAG
    docker push $REGISTRY/$GITHUB_ORG/bizosaas-platform/business-directory-backend:$TAG
    echo "   ✅ Business Directory Backend → $REGISTRY/$GITHUB_ORG/bizosaas-platform/business-directory-backend:$TAG"
else
    echo "   ⚠️  Business Directory Backend image not found locally"
fi

# Amazon Sourcing
if docker image inspect bizosaas/amazon-sourcing:latest >/dev/null 2>&1; then
    echo "4. Pushing Amazon Sourcing..."
    docker tag bizosaas/amazon-sourcing:latest $REGISTRY/$GITHUB_ORG/bizosaas-platform/amazon-sourcing:$TAG
    docker push $REGISTRY/$GITHUB_ORG/bizosaas-platform/amazon-sourcing:$TAG
    echo "   ✅ Amazon Sourcing → $REGISTRY/$GITHUB_ORG/bizosaas-platform/amazon-sourcing:$TAG"
else
    echo "   ⚠️  Amazon Sourcing image not found locally"
fi

echo ""
echo "📦 Frontend Services:"
echo "--------------------"

# Client Portal
if docker image inspect bizosaas-client-portal:latest >/dev/null 2>&1; then
    echo "1. Pushing Client Portal..."
    docker tag bizosaas-client-portal:latest $REGISTRY/$GITHUB_ORG/bizosaas-platform/client-portal:$TAG
    docker push $REGISTRY/$GITHUB_ORG/bizosaas-platform/client-portal:$TAG
    echo "   ✅ Client Portal → $REGISTRY/$GITHUB_ORG/bizosaas-platform/client-portal:$TAG"
else
    echo "   ⚠️  Client Portal image not found locally"
fi

# Bizoholic Frontend
if docker image inspect bizosaas-bizoholic-frontend:latest >/dev/null 2>&1; then
    echo "2. Pushing Bizoholic Frontend..."
    docker tag bizosaas-bizoholic-frontend:latest $REGISTRY/$GITHUB_ORG/bizosaas-platform/bizoholic-frontend:$TAG
    docker push $REGISTRY/$GITHUB_ORG/bizosaas-platform/bizoholic-frontend:$TAG
    echo "   ✅ Bizoholic Frontend → $REGISTRY/$GITHUB_ORG/bizosaas-platform/bizoholic-frontend:$TAG"
elif docker image inspect bizosaas/bizoholic-frontend:latest >/dev/null 2>&1; then
    echo "2. Pushing Bizoholic Frontend (alternative tag)..."
    docker tag bizosaas/bizoholic-frontend:latest $REGISTRY/$GITHUB_ORG/bizosaas-platform/bizoholic-frontend:$TAG
    docker push $REGISTRY/$GITHUB_ORG/bizosaas-platform/bizoholic-frontend:$TAG
    echo "   ✅ Bizoholic Frontend → $REGISTRY/$GITHUB_ORG/bizosaas-platform/bizoholic-frontend:$TAG"
else
    echo "   ⚠️  Bizoholic Frontend image not found locally"
fi

# CorelDove Frontend
if docker image inspect bizosaas-coreldove-frontend:latest >/dev/null 2>&1; then
    echo "3. Pushing CorelDove Frontend..."
    docker tag bizosaas-coreldove-frontend:latest $REGISTRY/$GITHUB_ORG/bizosaas-platform/coreldove-frontend:$TAG
    docker push $REGISTRY/$GITHUB_ORG/bizosaas-platform/coreldove-frontend:$TAG
    echo "   ✅ CorelDove Frontend → $REGISTRY/$GITHUB_ORG/bizosaas-platform/coreldove-frontend:$TAG"
else
    echo "   ⚠️  CorelDove Frontend image not found locally"
fi

# Business Directory Frontend
if docker image inspect bizosaas-business-directory:latest >/dev/null 2>&1; then
    echo "4. Pushing Business Directory Frontend..."
    docker tag bizosaas-business-directory:latest $REGISTRY/$GITHUB_ORG/bizosaas-platform/business-directory-frontend:$TAG
    docker push $REGISTRY/$GITHUB_ORG/bizosaas-platform/business-directory-frontend:$TAG
    echo "   ✅ Business Directory Frontend → $REGISTRY/$GITHUB_ORG/bizosaas-platform/business-directory-frontend:$TAG"
else
    echo "   ⚠️  Business Directory Frontend image not found locally"
fi

# Admin Dashboard
if docker image inspect bizosaas-bizosaas-admin:latest >/dev/null 2>&1; then
    echo "5. Pushing Admin Dashboard..."
    docker tag bizosaas-bizosaas-admin:latest $REGISTRY/$GITHUB_ORG/bizosaas-platform/admin-dashboard:$TAG
    docker push $REGISTRY/$GITHUB_ORG/bizosaas-platform/admin-dashboard:$TAG
    echo "   ✅ Admin Dashboard → $REGISTRY/$GITHUB_ORG/bizosaas-platform/admin-dashboard:$TAG"
else
    echo "   ⚠️  Admin Dashboard image not found locally"
fi

# ThrillRing Gaming (if exists)
if docker image inspect bizosaas-thrillring-gaming:latest >/dev/null 2>&1; then
    echo "6. Pushing ThrillRing Gaming..."
    docker tag bizosaas-thrillring-gaming:latest $REGISTRY/$GITHUB_ORG/bizosaas-platform/thrillring-gaming:$TAG
    docker push $REGISTRY/$GITHUB_ORG/bizosaas-platform/thrillring-gaming:$TAG
    echo "   ✅ ThrillRing Gaming → $REGISTRY/$GITHUB_ORG/bizosaas-platform/thrillring-gaming:$TAG"
else
    echo "   ⚠️  ThrillRing Gaming image not found locally (optional)"
fi

echo ""
echo "========================================"
echo "✅ Image push completed!"
echo ""
echo "📋 Next Steps:"
echo "1. Update dokploy-backend-staging.yml to use GHCR images"
echo "2. Update dokploy-frontend-staging.yml to use GHCR images"
echo "3. Commit and push changes to GitHub"
echo "4. Dokploy will auto-deploy with pre-built images"
echo ""
echo "📖 View pushed images at:"
echo "   https://github.com/orgs/bizoholic-digital/packages?repo_name=bizosaas-platform"
