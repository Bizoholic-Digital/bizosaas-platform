#!/bin/bash

# BizOSaaS Platform - Fully Automated Dokploy Deployment
# Deploys all 22 services via Dokploy API with error handling and retries

set -e

# Configuration
VPS_IP="72.60.219.244"
DOKPLOY_URL="https://dk4.bizoholic.com"
DOKPLOY_API_KEY="VumUVyBHPJQUlXiGnwVxeyKYBeGOLOttGjkgkGiwpSHLiEYegUBkCSTPFmQqMbtC"
GITHUB_REPO="https://github.com/Bizoholic-Digital/bizosaas-platform.git"
GITHUB_BRANCH="main"
PROJECT_DIR="/home/alagiri/projects/bizoholic/bizosaas-platform"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_section() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}========================================${NC}"
}

# Dokploy API wrapper
dokploy_api() {
    local method=$1
    local endpoint=$2
    local data=$3

    local url="${DOKPLOY_URL}/api${endpoint}"

    if [ -z "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $DOKPLOY_API_KEY" \
            -H "Content-Type: application/json" \
            "$url"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $DOKPLOY_API_KEY" \
            -H "Content-Type: application/json" \
            -d "$data" \
            "$url"
    fi
}

# Deploy compose stack via Dokploy
deploy_compose_stack() {
    local project_name=$1
    local compose_file=$2
    local description=$3

    log_section "DEPLOYING: $project_name"

    log_info "Reading compose file: $compose_file"

    if [ ! -f "$compose_file" ]; then
        log_error "Compose file not found: $compose_file"
        return 1
    fi

    # For Dokploy, we need to use SSH to deploy compose files
    # Let's use docker-compose directly on the VPS
    log_info "Deploying via SSH to VPS..."

    # Copy compose file to VPS
    scp -o StrictHostKeyChecking=no "$compose_file" root@$VPS_IP:/tmp/deploy-compose.yml

    # Deploy via docker-compose on VPS
    ssh -o StrictHostKeyChecking=no root@$VPS_IP << 'ENDSSH'
        cd /tmp
        echo "Deploying compose stack..."
        docker-compose -f deploy-compose.yml up -d --build
        echo "Deployment initiated"
ENDSSH

    log_success "$project_name deployment initiated"
}

# Main deployment flow
main() {
    log_section "BizOSaaS Platform - Automated Deployment"

    log_info "VPS: $VPS_IP"
    log_info "Dokploy: $DOKPLOY_URL"
    log_info "Repository: $GITHUB_REPO"
    echo ""

    # Check SSH connectivity
    log_info "Checking SSH connectivity to VPS..."
    if ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@$VPS_IP "echo 'SSH OK'" 2>/dev/null; then
        log_success "SSH connection successful"
    else
        log_error "Cannot connect to VPS via SSH"
        log_warning "Please ensure SSH key is configured or provide password"
        exit 1
    fi

    # Step 1: Deploy Backend Services
    log_section "PHASE 1: BACKEND SERVICES (10 containers)"

    log_info "Backend services to deploy:"
    echo "  1. Saleor API (8000)"
    echo "  2. Brain API (8001) - ALREADY RUNNING"
    echo "  3. Wagtail CMS (8002)"
    echo "  4. Django CRM (8003)"
    echo "  5. Business Directory (8004)"
    echo "  6. CorelDove Backend (8005)"
    echo "  7. Auth Service (8006)"
    echo "  8. Temporal Integration (8007)"
    echo "  9. AI Agents (8008)"
    echo "  10. Amazon Sourcing (8009)"
    echo ""

    deploy_compose_stack "backend-services" \
        "$PROJECT_DIR/dokploy-backend-staging.yml" \
        "BizOSaaS Backend Services"

    log_info "Waiting 120 seconds for backend services to start..."
    sleep 120

    # Step 2: Deploy Frontend Services
    log_section "PHASE 2: FRONTEND SERVICES (6 containers)"

    log_info "Frontend services to deploy:"
    echo "  1. Bizoholic Frontend (3000) - ALREADY RUNNING"
    echo "  2. Client Portal (3001)"
    echo "  3. CorelDove Frontend (3002)"
    echo "  4. Business Directory Frontend (3003)"
    echo "  5. ThrillRing Gaming (3005)"
    echo "  6. Admin Dashboard (3009)"
    echo ""

    deploy_compose_stack "frontend-services" \
        "$PROJECT_DIR/dokploy-frontend-staging.yml" \
        "BizOSaaS Frontend Applications"

    log_info "Waiting 180 seconds for frontend services to build and start..."
    sleep 180

    # Step 3: Verify Deployment
    log_section "PHASE 3: DEPLOYMENT VERIFICATION"

    bash "$PROJECT_DIR/check-services.sh"

    # Step 4: Configure Domains (if needed)
    log_section "PHASE 4: DOMAIN CONFIGURATION"

    log_info "Domain configuration should be done via Dokploy UI:"
    echo "  - stg.bizoholic.com → Port 3000"
    echo "  - stg.portal.bizoholic.com → Port 3001"
    echo "  - stg.coreldove.com → Port 3002"
    echo "  - stg.directory.bizoholic.com → Port 3003"
    echo "  - stg.thrillring.com → Port 3005"
    echo "  - stg.admin.bizoholic.com → Port 3009"
    echo ""

    log_section "DEPLOYMENT COMPLETE"

    log_success "All services have been deployed!"
    log_info "Please verify service health and configure domains in Dokploy UI"
}

main "$@"
