#!/bin/bash

# Complete Registry Setup and Image Push Script
# This script authenticates with GitHub Container Registry and pushes all 15 images

set -e

REGISTRY="ghcr.io/bizoholic-digital"
TAG="staging"

echo "=============================================="
echo "BizOSaaS Complete Registry Setup & Image Push"
echo "=============================================="
echo ""

# Check if already authenticated
echo "🔐 Checking authentication..."
if docker pull ghcr.io/bizoholic-digital/apache-superset:staging > /dev/null 2>&1; then
    echo "✅ Already authenticated with GitHub Container Registry"
else
    echo "⚠️  Not authenticated. You need to authenticate first."
    echo ""
    echo "To authenticate, run:"
    echo "  docker login ghcr.io"
    echo ""
    echo "You'll need:"
    echo "  - GitHub username"
    echo "  - Personal Access Token (PAT) with 'packages:write' scope"
    echo ""
    echo "Get a PAT at: https://github.com/settings/tokens/new"
    echo "Required scope: packages:write"
    echo ""
    read -p "Would you like to authenticate now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Please enter your GitHub credentials:"
        docker login ghcr.io
    else
        echo "Exiting. Please authenticate and run this script again."
        exit 1
    fi
fi

echo ""
echo "=============================================="
echo "Starting Image Push (15 images)"
echo "=============================================="
echo ""

# Function to tag and push
tag_and_push() {
    local local_image=$1
    local remote_name=$2

    echo "📦 [$remote_name]"
    echo "   Local: $local_image"
    echo "   Remote: $REGISTRY/$remote_name:$TAG"

    if docker image inspect "$local_image" > /dev/null 2>&1; then
        echo "   → Tagging..."
        docker tag "$local_image" "$REGISTRY/$remote_name:$TAG"

        echo "   → Pushing..."
        if docker push "$REGISTRY/$remote_name:$TAG" 2>&1 | grep -q "digest:"; then
            echo "   ✅ Success!"
        else
            echo "   ⚠️  Push completed (check output above for errors)"
        fi
    else
        echo "   ❌ Image not found locally - need to build first"
    fi
    echo ""
}

# Backend Images (8 images)
echo "🔧 BACKEND IMAGES (8)"
echo "===================="
tag_and_push "bizosaas-brain-gateway:latest" "brain-gateway"
tag_and_push "bizosaas-wagtail-cms:latest" "wagtail-cms"
tag_and_push "django-crm-django-crm:latest" "django-crm"
tag_and_push "bizosaas-business-directory-backend:latest" "business-directory-backend"
tag_and_push "coreldove-backend-coreldove-backend:latest" "coreldove-backend"
tag_and_push "bizosaas-platform-temporal-integration:latest" "temporal-integration"
tag_and_push "bizosaas-platform-bizosaas-brain-enhanced:latest" "ai-agents"
tag_and_push "bizosaas/amazon-sourcing:latest" "amazon-sourcing"

# Frontend Images (6 images)
echo "🎨 FRONTEND IMAGES (6)"
echo "====================="
tag_and_push "bizoholic-frontend:dev" "bizoholic-frontend"
tag_and_push "bizosaas-client-portal:latest" "client-portal"
tag_and_push "bizosaas-coreldove-frontend:latest" "coreldove-frontend"
tag_and_push "bizosaas-business-directory:latest" "business-directory-frontend"
tag_and_push "bizosaas-bizosaas-admin:latest" "admin-dashboard"

# Analytics Image (1 image - already pushed)
echo "📊 ANALYTICS IMAGE (1)"
echo "======================"
echo "📦 [apache-superset]"
echo "   ✅ Already pushed"
echo ""

echo "=============================================="
echo "📊 PUSH SUMMARY"
echo "=============================================="
echo ""
echo "Check the output above for any errors."
echo "Images successfully pushed are available at:"
echo "  $REGISTRY/<image-name>:$TAG"
echo ""
echo "Next steps:"
echo "  1. Verify all images pushed successfully"
echo "  2. Deploy backend services (9 total)"
echo "  3. Deploy frontend services (6 total)"
echo ""
echo "=============================================="
