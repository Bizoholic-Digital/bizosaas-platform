#!/bin/bash
# Push organized local images to GHCR (matching VPS project structure)
# Infrastructure: Already deployed, no push needed
# Backend: 8 services
# Frontend: 5 services

set -e

echo "🚀 BizOSaaS Platform - Organized GHCR Push"
echo "=========================================="
echo ""

REGISTRY="ghcr.io/bizoholic-digital/bizosaas-platform"
TAG="staging"

echo "📦 BACKEND SERVICES (8 images)"
echo "==============================="
echo ""

# 1. Brain API (AI Gateway)
echo "1/8 Brain API..."
docker tag bizosaas-brain-gateway:latest $REGISTRY/brain-api:$TAG
docker push $REGISTRY/brain-api:$TAG
echo "    ✅ Pushed $REGISTRY/brain-api:$TAG"

# 2. Wagtail CMS
echo "2/8 Wagtail CMS..."
docker tag bizosaas-wagtail-cms:latest $REGISTRY/wagtail-cms:$TAG
docker push $REGISTRY/wagtail-cms:$TAG
echo "    ✅ Pushed $REGISTRY/wagtail-cms:$TAG"

# 3. Django CRM
echo "3/8 Django CRM..."
docker tag bizoholic-django-crm:latest $REGISTRY/django-crm:$TAG
docker push $REGISTRY/django-crm:$TAG
echo "    ✅ Pushed $REGISTRY/django-crm:$TAG"

# 4. Business Directory Backend
echo "4/8 Business Directory Backend..."
docker tag bizosaas-business-directory-backend:latest $REGISTRY/business-directory-backend:$TAG
docker push $REGISTRY/business-directory-backend:$TAG
echo "    ✅ Pushed $REGISTRY/business-directory-backend:$TAG"

# 5. CorelDove Backend
echo "5/8 CorelDove Backend..."
docker tag bizoholic-coreldove-backend:latest $REGISTRY/coreldove-backend:$TAG
docker push $REGISTRY/coreldove-backend:$TAG
echo "    ✅ Pushed $REGISTRY/coreldove-backend:$TAG"

# 6. Auth Service
echo "6/8 Auth Service..."
docker tag bizoholic-auth-service:latest $REGISTRY/auth-service:$TAG
docker push $REGISTRY/auth-service:$TAG
echo "    ✅ Pushed $REGISTRY/auth-service:$TAG"

# 7. AI Agents
echo "7/8 AI Agents..."
docker tag bizoholic-ai-agents:latest $REGISTRY/ai-agents:$TAG
docker push $REGISTRY/ai-agents:$TAG
echo "    ✅ Pushed $REGISTRY/ai-agents:$TAG"

# 8. Amazon Sourcing
echo "8/8 Amazon Sourcing..."
docker tag bizosaas/amazon-sourcing:latest $REGISTRY/amazon-sourcing:$TAG
docker push $REGISTRY/amazon-sourcing:$TAG
echo "    ✅ Pushed $REGISTRY/amazon-sourcing:$TAG"

echo ""
echo "📱 FRONTEND SERVICES (5 images)"
echo "==============================="
echo ""

# 1. Client Portal
echo "1/5 Client Portal..."
docker tag bizosaas-client-portal:latest $REGISTRY/client-portal:$TAG
docker push $REGISTRY/client-portal:$TAG
echo "    ✅ Pushed $REGISTRY/client-portal:$TAG"

# 2. Bizoholic Frontend
echo "2/5 Bizoholic Frontend..."
docker tag bizosaas-bizoholic-frontend:latest $REGISTRY/bizoholic-frontend:$TAG
docker push $REGISTRY/bizoholic-frontend:$TAG
echo "    ✅ Pushed $REGISTRY/bizoholic-frontend:$TAG"

# 3. CorelDove Frontend
echo "3/5 CorelDove Frontend..."
docker tag bizosaas-coreldove-frontend:latest $REGISTRY/coreldove-frontend:$TAG
docker push $REGISTRY/coreldove-frontend:$TAG
echo "    ✅ Pushed $REGISTRY/coreldove-frontend:$TAG"

# 4. Business Directory Frontend
echo "4/5 Business Directory Frontend..."
docker tag bizosaas-business-directory:latest $REGISTRY/business-directory-frontend:$TAG
docker push $REGISTRY/business-directory-frontend:$TAG
echo "    ✅ Pushed $REGISTRY/business-directory-frontend:$TAG"

# 5. Admin Dashboard
echo "5/5 Admin Dashboard..."
docker tag bizosaas-bizosaas-admin:latest $REGISTRY/admin-dashboard:$TAG
docker push $REGISTRY/admin-dashboard:$TAG
echo "    ✅ Pushed $REGISTRY/admin-dashboard:$TAG"

echo ""
echo "=========================================="
echo "✅ All 13 images pushed successfully!"
echo ""
echo "📊 Summary:"
echo "   Backend: 8/8 ✅"
echo "   Frontend: 5/5 ✅"
echo "   Infrastructure: Already deployed ✅"
echo ""
echo "📋 Next Steps:"
echo "1. Update dokploy-backend-staging.yml"
echo "2. Update dokploy-frontend-staging.yml"
echo "3. git commit and push"
echo "4. Dokploy auto-deploys in ~2 minutes"
echo ""
echo "⚠️  Note: ThrillRing Gaming (3004) not included - container not built locally"
