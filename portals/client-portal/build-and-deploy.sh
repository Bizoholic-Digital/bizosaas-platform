#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# Client Portal - Build and Deploy to GHCR & KVM4
# ═══════════════════════════════════════════════════════════════════════════
#
# This script builds the Client Portal Docker image and pushes it to GHCR
# for deployment on KVM4 Dokploy.
#
# Usage: ./build-and-deploy.sh [version]
# Example: ./build-and-deploy.sh v2.0.26
#
# Without version argument, uses v2.0.26-$(date +%Y%m%d-%H%M%S)
# ═══════════════════════════════════════════════════════════════════════════

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REGISTRY="ghcr.io"
OWNER="bizoholic-digital"
IMAGE_NAME="bizosaas-client-portal"
GITHUB_TOKEN="${GITHUB_TOKEN:-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}"

# Version handling
if [ -z "$1" ]; then
    VERSION="v2.0.26-$(date +%Y%m%d-%H%M%S)"
    echo -e "${YELLOW}No version specified, using: ${VERSION}${NC}"
else
    VERSION="$1"
fi

FULL_IMAGE="${REGISTRY}/${OWNER}/${IMAGE_NAME}:${VERSION}"
LATEST_IMAGE="${REGISTRY}/${OWNER}/${IMAGE_NAME}:latest"

# ═══════════════════════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════════════════════

log_step() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}\n"
}

log_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

log_error() {
    echo -e "${RED}✗ $1${NC}"
}

log_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════
# Pre-Build Checks
# ═══════════════════════════════════════════════════════════════════════════

log_step "Pre-Build Checks"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    log_error "Docker is not running. Please start Docker and try again."
    exit 1
fi
log_success "Docker is running"

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -f "Dockerfile" ]; then
    log_error "Must be run from the client-portal directory"
    log_info "Current directory: $(pwd)"
    log_info "Expected files: package.json, Dockerfile"
    exit 1
fi
log_success "Correct directory confirmed"

# Check for required files
REQUIRED_FILES=("next.config.js" ".dockerignore" "Dockerfile")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        log_error "Missing required file: $file"
        exit 1
    fi
done
log_success "All required files present"

# Display build information
log_info "Image: ${FULL_IMAGE}"
log_info "Also tagging as: ${LATEST_IMAGE}"
log_info "Registry: ${REGISTRY}"

# ═══════════════════════════════════════════════════════════════════════════
# GHCR Login
# ═══════════════════════════════════════════════════════════════════════════

log_step "Logging into GHCR"

if [ -z "$GITHUB_TOKEN" ]; then
    log_error "GITHUB_TOKEN environment variable not set"
    log_info "Please set it with: export GITHUB_TOKEN=your_token"
    exit 1
fi

echo "$GITHUB_TOKEN" | docker login ${REGISTRY} -u ${OWNER} --password-stdin > /dev/null 2>&1
if [ $? -eq 0 ]; then
    log_success "Successfully logged into GHCR"
else
    log_error "Failed to login to GHCR"
    exit 1
fi

# ═══════════════════════════════════════════════════════════════════════════
# Build Docker Image
# ═══════════════════════════════════════════════════════════════════════════

log_step "Building Docker Image"

log_info "Starting multi-stage build..."
log_info "This may take 3-5 minutes on first build"
log_info "Subsequent builds will be faster due to layer caching"

# Build with standard docker build (buildx not available)
docker build \
    --platform linux/amd64 \
    --tag ${FULL_IMAGE} \
    --tag ${LATEST_IMAGE} \
    --build-arg NODE_ENV=production \
    --build-arg NEXT_TELEMETRY_DISABLED=1 \
    .

if [ $? -eq 0 ]; then
    log_success "Docker image built successfully"
else
    log_error "Docker build failed"
    exit 1
fi

# Display image size
IMAGE_SIZE=$(docker images ${FULL_IMAGE} --format "{{.Size}}")
log_info "Image size: ${IMAGE_SIZE}"

# ═══════════════════════════════════════════════════════════════════════════
# Push to GHCR
# ═══════════════════════════════════════════════════════════════════════════

log_step "Pushing to GitHub Container Registry"

log_info "Pushing ${VERSION} tag..."
docker push ${FULL_IMAGE}
if [ $? -eq 0 ]; then
    log_success "Pushed ${VERSION} tag"
else
    log_error "Failed to push ${VERSION} tag"
    exit 1
fi

log_info "Pushing latest tag..."
docker push ${LATEST_IMAGE}
if [ $? -eq 0 ]; then
    log_success "Pushed latest tag"
else
    log_error "Failed to push latest tag"
    exit 1
fi

# ═══════════════════════════════════════════════════════════════════════════
# Verify on GHCR
# ═══════════════════════════════════════════════════════════════════════════

log_step "Verifying Image on GHCR"

log_info "Image URL: https://github.com/${OWNER}/bizosaas-platform/pkgs/container/${IMAGE_NAME}"
log_success "Image pushed successfully to GHCR"

# ═══════════════════════════════════════════════════════════════════════════
# Deployment Instructions
# ═══════════════════════════════════════════════════════════════════════════

log_step "Deployment Instructions"

echo -e "
${GREEN}✓ Build and Push Complete!${NC}

${YELLOW}Image Details:${NC}
  - Version: ${VERSION}
  - Full Image: ${FULL_IMAGE}
  - Latest: ${LATEST_IMAGE}
  - Size: ${IMAGE_SIZE}

${YELLOW}Next Steps - Deploy to KVM4:${NC}

${BLUE}Option 1: Via Dokploy UI (Recommended)${NC}
  1. Open https://dk4.bizoholic.com
  2. Navigate to Frontend Services project
  3. Find 'Client Portal' service
  4. Click 'Redeploy' or 'Update Image'
  5. Enter new image: ${FULL_IMAGE}
  6. Click 'Deploy'

${BLUE}Option 2: Via SSH to KVM4${NC}
  ssh root@72.60.219.244
  docker service update --image ${FULL_IMAGE} frontend-client-portal

${BLUE}Option 3: Update docker-compose.yml and redeploy${NC}
  1. SSH to KVM4: ssh root@72.60.219.244
  2. Edit compose file with new image version
  3. Run: docker stack deploy -c docker-compose.yml frontend

${YELLOW}Environment Variables for Dokploy:${NC}
  PORT=3000
  NODE_ENV=production
  NEXT_TELEMETRY_DISABLED=1
  NEXT_PUBLIC_API_BASE_URL=https://api.bizoholic.com
  NEXT_PUBLIC_BRAIN_API_URL=https://api.bizoholic.com
  NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com
  NEXTAUTH_URL=https://portal.bizoholic.com
  NEXTAUTH_SECRET=<your-secure-secret>
  NEXT_PUBLIC_ENABLE_SOURCING=true
  NEXT_PUBLIC_USE_MOCK_API=false

${YELLOW}Verify Deployment:${NC}
  # Check if service is running
  ssh root@72.60.219.244 'docker service ps frontend-client-portal'

  # Check logs
  ssh root@72.60.219.244 'docker service logs frontend-client-portal --tail 100'

  # Test endpoint
  curl https://portal.bizoholic.com

${GREEN}═══════════════════════════════════════════════════════${NC}
${GREEN}  Build completed at: $(date)${NC}
${GREEN}═══════════════════════════════════════════════════════${NC}
"

# ═══════════════════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════════════════

log_success "Script completed successfully!"
log_info "Image is ready for deployment on KVM4"
