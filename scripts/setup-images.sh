#!/bin/bash
# Use existing GHCR images and build only what's missing

set -e

echo "🚀 Setting Up Images for Local Testing"
echo "======================================="
echo ""

echo "📥 Step 1: Tag existing GHCR images for local use..."
echo ""

# Backend services (already pulled)
echo "  ✓ Brain API (using GHCR image)"
docker tag ghcr.io/bizoholic-digital/bizosaas-brain:latest bizosaas-brain:local 2>/dev/null || \
  docker pull ghcr.io/bizoholic-digital/bizosaas-brain:latest && \
  docker tag ghcr.io/bizoholic-digital/bizosaas-brain:latest bizosaas-brain:local

echo "  ✓ Auth Service (using GHCR image)"
docker tag ghcr.io/bizoholic-digital/bizosaas-auth-service:latest bizosaas-auth:local 2>/dev/null || \
  docker pull ghcr.io/bizoholic-digital/bizosaas-auth-service:latest && \
  docker tag ghcr.io/bizoholic-digital/bizosaas-auth-service:latest bizosaas-auth:local

echo "  ✓ Django CRM (using GHCR image)"
docker tag ghcr.io/bizoholic-digital/django-crm:latest bizosaas-django-crm:local 2>/dev/null || \
  docker pull ghcr.io/bizoholic-digital/django-crm:latest && \
  docker tag ghcr.io/bizoholic-digital/django-crm:latest bizosaas-django-crm:local

# Admin frontend (already pulled)
echo "  ✓ Admin Dashboard (using GHCR image)"
docker tag ghcr.io/bizoholic-digital/bizosaas-admin:latest bizosaas-admin:local 2>/dev/null || echo "Already tagged"

echo ""
echo "🏗️  Step 2: Build missing frontend images..."
echo ""

cd "$(dirname "$0")/bizosaas"

# Build Bizoholic Frontend (small, simple)
echo "  🎨 Building Bizoholic Frontend..."
DOCKER_BUILDKIT=0 docker build -t bizosaas-bizoholic:local ./frontend/apps/bizoholic-frontend 2>&1 | grep -E "(Step|Successfully|Error)" || true

# Build CoreLDove Frontend (small, simple)  
echo "  🛒 Building CoreLDove Frontend..."
DOCKER_BUILDKIT=0 docker build -t bizosaas-coreldove:local ./frontend/apps/coreldove-frontend 2>&1 | grep -E "(Step|Successfully|Error)" || true

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📋 Available Images:"
docker images | grep -E "(bizosaas.*local|REPOSITORY)" | head -10

echo ""
echo "🚀 Ready to Start Services!"
echo ""
echo "Choose one:"
echo "  ./start-bizoholic.sh   # Start Bizoholic platform"
echo "  ./start-coreldove.sh   # Start CoreLDove platform"
echo ""
