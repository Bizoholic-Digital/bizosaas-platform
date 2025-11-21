#!/bin/bash
# rebuild-native.sh - Faster native build without cross-platform emulation

set -e

echo "🔨 Rebuilding client-portal v2.2.17 (NATIVE BUILD - FASTER)"
echo "============================================================"

# Configuration
IMAGE_NAME="ghcr.io/bizoholic-digital/bizosaas-client-portal"
NEW_VERSION="v2.2.17"
GITHUB_USERNAME="Bizoholic-Digital"

# Check if in correct directory
if [ ! -f "Dockerfile" ]; then
    echo "❌ Error: Dockerfile not found"
    exit 1
fi

# Verify .env.production has BASE_PATH
if ! grep -q "BASE_PATH=/portal" .env.production; then
    echo "❌ Error: BASE_PATH=/portal not found in .env.production"
    exit 1
fi

echo "✅ .env.production has BASE_PATH=/portal"

# Build the image (NATIVE - NO --platform flag for speed)
echo ""
echo "📦 Building Docker image (native arch, BASE_PATH=/portal)..."
echo "This should take 8-12 minutes..."
echo ""

# Use legacy builder (BuildKit not available)
export DOCKER_BUILDKIT=0

docker build \
    --build-arg NODE_ENV=production \
    --build-arg BASE_PATH=/portal \
    --build-arg NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com/api \
    -t ${IMAGE_NAME}:${NEW_VERSION} \
    -t ${IMAGE_NAME}:latest \
    -f Dockerfile \
    .

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
else
    echo ""
    echo "❌ Build failed!"
    exit 1
fi

# Login to GHCR
echo "🔐 Logging into GitHub Container Registry..."

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN not set"
    exit 1
fi

echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_USERNAME" --password-stdin

if [ $? -ne 0 ]; then
    echo "❌ Login failed!"
    exit 1
fi

echo "✅ Logged into GHCR"

# Push the image
echo ""
echo "📤 Pushing ${NEW_VERSION} to GitHub Container Registry..."

docker push ${IMAGE_NAME}:${NEW_VERSION}
docker push ${IMAGE_NAME}:latest

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✅ SUCCESS! Image built and pushed"
    echo ""
    echo "Image: ${IMAGE_NAME}:${NEW_VERSION}"
    echo ""
    echo "Next steps:"
    echo "1. Go to Dokploy: https://dk4.bizoholic.com/dashboard"
    echo "2. Update client-portal image to: ${IMAGE_NAME}:${NEW_VERSION}"
    echo "3. Redeploy"
    echo "4. Test: curl -I https://stg.bizoholic.com/portal"
    echo ""
    echo "=================================================="
else
    echo "❌ Push failed!"
    exit 1
fi
