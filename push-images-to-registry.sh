#!/bin/bash

# Script to push all BizOSaaS custom images to GitHub Container Registry
# Usage: ./push-images-to-registry.sh

set -e

REGISTRY="ghcr.io/bizoholic-digital"
TAG="staging"

echo "=============================================="
echo "Pushing BizOSaaS Images to GitHub Registry"
echo "Registry: $REGISTRY"
echo "Tag: $TAG"
echo "=============================================="
echo ""

# Function to tag and push
tag_and_push() {
    local local_image=$1
    local remote_name=$2

    echo "📦 Processing: $local_image"
    echo "   → Tagging as: $REGISTRY/$remote_name:$TAG"
    docker tag "$local_image" "$REGISTRY/$remote_name:$TAG"

    echo "   → Pushing to registry..."
    docker push "$REGISTRY/$remote_name:$TAG"
    echo "   ✅ Done!"
    echo ""
}

# Backend Images (8 images)
echo "🔧 BACKEND IMAGES"
echo "=================="
tag_and_push "bizosaas-brain-gateway:latest" "brain-gateway"
tag_and_push "bizosaas-wagtail-cms:latest" "wagtail-cms"
tag_and_push "django-crm-django-crm:latest" "django-crm"
tag_and_push "bizosaas-business-directory-backend:latest" "business-directory-backend"
tag_and_push "coreldove-backend-coreldove-backend:latest" "coreldove-backend"
tag_and_push "bizosaas-platform-temporal-integration:latest" "temporal-integration"
tag_and_push "bizosaas-platform-bizosaas-brain-enhanced:latest" "ai-agents"
tag_and_push "bizosaas/amazon-sourcing:latest" "amazon-sourcing"

# Frontend Images (6 images)
echo "🎨 FRONTEND IMAGES"
echo "=================="
tag_and_push "bizoholic-frontend:dev" "bizoholic-frontend"
tag_and_push "bizosaas-client-portal:latest" "client-portal"
tag_and_push "bizosaas-coreldove-frontend:latest" "coreldove-frontend"
tag_and_push "bizosaas-business-directory:latest" "business-directory-frontend"
tag_and_push "bizosaas-bizosaas-admin:latest" "admin-dashboard"

# Note: thrillring-gaming-3005 uses node:20-alpine which is public, no need to push

echo "=============================================="
echo "✅ All 14 custom images pushed successfully!"
echo "=============================================="
echo ""
echo "Images are now available at:"
echo "  $REGISTRY/<image-name>:$TAG"
echo ""
echo "Ready to deploy to staging!"
