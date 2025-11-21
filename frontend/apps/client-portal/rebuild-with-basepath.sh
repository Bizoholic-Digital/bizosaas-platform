#!/bin/bash
# rebuild-with-basepath.sh
# Rebuild client-portal with BASE_PATH=/portal and push to GHCR

set -e

echo "🔨 Rebuilding client-portal with BASE_PATH=/portal"
echo "=================================================="

# Configuration
IMAGE_NAME="ghcr.io/bizoholic-digital/bizosaas-client-portal"
NEW_VERSION="v2.2.16"
GITHUB_USERNAME="Bizoholic-Digital"

# Check if in correct directory
if [ ! -f "Dockerfile" ]; then
    echo "❌ Error: Dockerfile not found. Please run from client-portal directory."
    exit 1
fi

# Check if .env.production exists and has BASE_PATH
if [ ! -f ".env.production" ]; then
    echo "❌ Error: .env.production not found"
    exit 1
fi

if ! grep -q "BASE_PATH=/portal" .env.production; then
    echo "⚠️  Warning: BASE_PATH=/portal not found in .env.production"
    echo "Adding it now..."
    echo "" >> .env.production
    echo "# Critical for /portal routing" >> .env.production
    echo "BASE_PATH=/portal" >> .env.production
fi

echo "✅ .env.production has BASE_PATH=/portal"

# Build the image
echo ""
echo "📦 Building Docker image with BASE_PATH=/portal..."
echo "This may take 5-10 minutes..."

docker build \
    --build-arg NODE_ENV=production \
    --build-arg BASE_PATH=/portal \
    --build-arg NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com/api \
    --platform linux/amd64 \
    -t ${IMAGE_NAME}:${NEW_VERSION} \
    -t ${IMAGE_NAME}:latest \
    -f Dockerfile \
    .

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed!"
    exit 1
fi

# Check if logged into GHCR
echo ""
echo "🔐 Checking GitHub Container Registry login..."

# Prompt for GitHub token if not set
if [ -z "$GITHUB_TOKEN" ]; then
    echo ""
    echo "Please enter your GitHub Personal Access Token (PAT):"
    echo "(It will not be displayed as you type)"
    read -s GITHUB_TOKEN
    export GITHUB_TOKEN
fi

echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_USERNAME" --password-stdin

if [ $? -eq 0 ]; then
    echo "✅ Logged into GHCR"
else
    echo "❌ Login failed!"
    echo "Please check your GitHub token"
    exit 1
fi

# Push the image
echo ""
echo "📤 Pushing image to GitHub Container Registry..."

docker push ${IMAGE_NAME}:${NEW_VERSION}
docker push ${IMAGE_NAME}:latest

if [ $? -eq 0 ]; then
    echo "✅ Push successful!"
else
    echo "❌ Push failed!"
    exit 1
fi

echo ""
echo "=================================================="
echo "✅ SUCCESS! Image built and pushed"
echo ""
echo "New image: ${IMAGE_NAME}:${NEW_VERSION}"
echo ""
echo "Next steps:"
echo "1. Go to Dokploy: https://dk4.bizoholic.com/dashboard"
echo "2. Navigate to client-portal service"
echo "3. Ensure deployment method is 'Docker Image'"
echo "4. Update image to: ${IMAGE_NAME}:${NEW_VERSION}"
echo "5. Click 'Redeploy'"
echo "6. Wait 2-3 minutes"
echo "7. Test: curl -I https://stg.bizoholic.com/portal"
echo "   Expected: HTTP/2 200 (not 502)"
echo ""
echo "=================================================="
