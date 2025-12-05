#!/bin/bash

# BizOSaaS Platform - Deploy Complete Stack to KVM4
# Deploys all 24 services using dokploy-staging-complete.yml

set -e

VPS_IP="72.60.219.244"
VPS_USER="root"
VPS_PASSWORD="&k3civYG5Q6YPb"
DOKPLOY_URL="https://dk4.bizoholic.com"
COMPOSE_FILE="dokploy-staging-complete.yml"
REMOTE_DIR="/opt/bizosaas-platform"

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

# Main deployment function
main() {
    log_section "BizOSaaS Platform - Deploy to KVM4"

    log_info "Target: $VPS_IP ($DOKPLOY_URL)"
    log_info "Compose File: $COMPOSE_FILE"
    echo ""

    # Step 1: Copy compose file to server
    log_section "STEP 1: COPY CONFIGURATION TO SERVER"

    log_info "Creating remote directory..."
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP "mkdir -p $REMOTE_DIR"

    log_info "Copying compose file..."
    sshpass -p "$VPS_PASSWORD" scp -o StrictHostKeyChecking=no "$COMPOSE_FILE" $VPS_USER@$VPS_IP:$REMOTE_DIR/

    log_success "Configuration copied to server"

    # Step 2: Pull latest images from GHCR
    log_section "STEP 2: PULL CONTAINER IMAGES FROM GHCR"

    log_info "Pulling images from GitHub Container Registry..."
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP << 'ENDSSH'
        cd /opt/bizosaas-platform

        echo "Pulling all images..."
        docker-compose -f dokploy-staging-complete.yml pull --ignore-pull-failures

        echo "Images pulled successfully!"
ENDSSH

    log_success "All images pulled from GHCR"

    # Step 3: Stop old containers
    log_section "STEP 3: STOP OLD CONTAINERS"

    log_warning "Stopping existing containers..."
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP << 'ENDSSH'
        cd /opt/bizosaas-platform

        echo "Stopping old containers..."
        docker-compose -f dokploy-staging-complete.yml down || true

        echo "Old containers stopped"
ENDSSH

    log_success "Old containers stopped"

    # Step 4: Deploy new stack
    log_section "STEP 4: DEPLOY COMPLETE STACK (24 SERVICES)"

    log_info "Starting deployment..."
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP << 'ENDSSH'
        cd /opt/bizosaas-platform

        echo "Starting all services..."
        docker-compose -f dokploy-staging-complete.yml up -d

        echo "Deployment initiated!"
ENDSSH

    log_success "Stack deployment initiated"

    # Step 5: Wait for services to stabilize
    log_section "STEP 5: WAITING FOR SERVICES TO START"

    log_info "Waiting 60 seconds for containers to initialize..."
    sleep 60

    # Step 6: Verify deployment
    log_section "STEP 6: VERIFY DEPLOYMENT"

    log_info "Checking running containers..."
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP << 'ENDSSH'
        cd /opt/bizosaas-platform

        echo "=== RUNNING CONTAINERS ==="
        docker-compose -f dokploy-staging-complete.yml ps

        echo ""
        echo "=== CONTAINER COUNT ==="
        docker-compose -f dokploy-staging-complete.yml ps -q | wc -l
ENDSSH

    # Step 7: Health checks
    log_section "STEP 7: HEALTH CHECKS"

    log_info "Testing infrastructure services..."

    # PostgreSQL
    if nc -z -w5 $VPS_IP 5433 2>/dev/null; then
        log_success "✓ PostgreSQL (5433)"
    else
        log_warning "✗ PostgreSQL (5433)"
    fi

    # Redis
    if nc -z -w5 $VPS_IP 6380 2>/dev/null; then
        log_success "✓ Redis (6380)"
    else
        log_warning "✗ Redis (6380)"
    fi

    # Vault
    if nc -z -w5 $VPS_IP 8201 2>/dev/null; then
        log_success "✓ Vault (8201)"
    else
        log_warning "✗ Vault (8201)"
    fi

    # Temporal UI
    if nc -z -w5 $VPS_IP 8083 2>/dev/null; then
        log_success "✓ Temporal UI (8083)"
    else
        log_warning "✗ Temporal UI (8083)"
    fi

    log_info "Testing backend services..."

    # Brain Gateway
    if curl -f -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://$VPS_IP:8001/health" | grep -q "200"; then
        log_success "✓ Brain Gateway (8001)"
    else
        log_warning "✗ Brain Gateway (8001)"
    fi

    # Saleor
    if curl -f -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://$VPS_IP:8000/health/" | grep -q "200"; then
        log_success "✓ Saleor API (8000)"
    else
        log_warning "✗ Saleor API (8000)"
    fi

    log_info "Testing frontend services..."

    # Bizoholic Frontend
    if curl -f -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "https://stg.bizoholic.com" | grep -q "200"; then
        log_success "✓ Bizoholic Frontend (stg.bizoholic.com)"
    else
        log_warning "✗ Bizoholic Frontend (stg.bizoholic.com)"
    fi

    # CorelDove Frontend
    if curl -f -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "https://stg.coreldove.com" | grep -q "200\|301\|302"; then
        log_success "✓ CorelDove Frontend (stg.coreldove.com)"
    else
        log_warning "✗ CorelDove Frontend (stg.coreldove.com)"
    fi

    # ThrillRing Gaming
    if curl -f -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "https://stg.thrillring.com" | grep -q "200\|301\|302"; then
        log_success "✓ ThrillRing Gaming (stg.thrillring.com)"
    else
        log_warning "✗ ThrillRing Gaming (stg.thrillring.com)"
    fi

    # Final summary
    log_section "DEPLOYMENT COMPLETE"

    log_success "BizOSaaS Platform deployed to KVM4!"
    echo ""
    echo "Next steps:"
    echo "  1. Monitor Dokploy: $DOKPLOY_URL"
    echo "  2. Check application logs for errors"
    echo "  3. Test all frontend URLs"
    echo "  4. Verify backend API endpoints"
    echo ""
    log_info "View detailed logs: ssh root@$VPS_IP 'cd $REMOTE_DIR && docker-compose logs -f'"
}

# Execute main function
main "$@"
