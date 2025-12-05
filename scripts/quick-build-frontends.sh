#!/bin/bash
# Quick build script for frontend images with optimization

set -e

echo "🏗️  Quick Frontend Build (Optimized)"
echo "====================================="
echo ""

cd "$(dirname "$0")/bizosaas"

# Create .dockerignore files to reduce build context
echo "📝 Creating .dockerignore files..."

for app in bizoholic-frontend coreldove-frontend; do
  cat > "./frontend/apps/$app/.dockerignore" << 'EOF'
node_modules
.next
.git
*.md
.env*
*.log
.DS_Store
.cache
dist
build
coverage
.turbo
EOF
  echo "  ✓ Created .dockerignore for $app"
done

echo ""
echo "🎨 Building Bizoholic Frontend (simplified)..."
DOCKER_BUILDKIT=0 docker build \
  --no-cache \
  -t bizosaas-bizoholic:local \
  ./frontend/apps/bizoholic-frontend || echo "⚠️  Bizoholic build had issues"

echo ""
echo "🛒 Building CoreLDove Frontend (simplified)..."
DOCKER_BUILDKIT=0 docker build \
  --no-cache \
  -t bizosaas-coreldove:local \
  ./frontend/apps/coreldove-frontend || echo "⚠️  CoreLDove build had issues"

echo ""
echo "✅ Build Complete!"
echo ""
echo "📋 Available Images:"
docker images | grep -E "(bizosaas.*local|REPOSITORY)"

echo ""
echo "🚀 Ready to start:"
echo "  ./start-bizoholic.sh"
echo "  ./start-coreldove.sh"
echo ""
