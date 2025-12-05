#!/bin/bash

# BizOSaaS Platform - Docker Image Cleanup Script
# Removes old, duplicate, and unused Docker images
# Run with: bash scripts/cleanup-old-images.sh

set -e

echo "🧹 BizOSaaS Platform - Docker Image Cleanup"
echo "=========================================="
echo ""

echo "📊 Current Docker disk usage:"
docker system df
echo ""

echo "⚠️  This script will remove the following old/duplicate images:"
echo ""
echo "OLD FRONTEND IMAGES:"
echo "  - bizosaas-admin-ai-enhanced (duplicate)"
echo "  - bizosaas-admin-fixed-padding (duplicate)"
echo "  - bizosaas-client-portal:latest (if duplicate)"
echo "  - bizosaas-coreldove-frontend-dev (dev version)"
echo ""
echo "OLD BACKEND IMAGES:"
echo "  - bizosaas-platform-bizosaas-brain (old version)"
echo "  - bizosaas-platform-bizosaas-brain-enhanced (old version)"
echo "  - bizosaas-platform-wagtail-cms (old version)"
echo "  - bizosaas-auth-unified-fixed (old version)"
echo ""
echo "OLD ANALYTICS IMAGES:"
echo "  - bizosaas-platform-analytics-dashboard"
echo "  - bizosaas-platform-business-directory"
echo ""
echo "Estimated space to reclaim: ~8-10 GB"
echo ""

read -p "Continue with cleanup? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "🗑️  Removing old images..."
echo ""

# Function to safely remove image
remove_image() {
    local image=$1
    if docker images | grep -q "$image"; then
        echo "  Removing: $image"
        docker rmi "$image" 2>/dev/null || echo "    ⚠️  Could not remove (may be in use)"
    else
        echo "  ⊘ Not found: $image"
    fi
}

# Old frontend images
remove_image "bizosaas-admin-ai-enhanced"
remove_image "bizosaas-admin-fixed-padding"
remove_image "bizosaas-coreldove-frontend-dev"

# Old backend images
remove_image "bizosaas-platform-bizosaas-brain"
remove_image "bizosaas-platform-bizosaas-brain-enhanced"
remove_image "bizosaas-platform-wagtail-cms"
remove_image "bizosaas-auth-unified-fixed"

# Old analytics images
remove_image "bizosaas-platform-analytics-dashboard"
remove_image "bizosaas-platform-business-directory"

echo ""
echo "🧹 Removing dangling images..."
docker image prune -f

echo ""
echo "📊 New Docker disk usage:"
docker system df

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "To reclaim even more space, run:"
echo "  docker system prune -a --volumes  # ⚠️  WARNING: Removes ALL unused images and volumes"
