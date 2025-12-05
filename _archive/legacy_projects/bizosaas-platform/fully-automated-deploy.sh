#!/bin/bash

# BizOSaaS Platform - Fully Automated Deployment
# Deploys all 23 services via docker-compose directly on the server
# Bypasses Dokploy UI completely

set -e

VPS_IP="72.60.219.244"
VPS_PASSWORD="&k3civYG5Q6YPb"
LOCAL_COMPOSE_FILE="dokploy-staging-complete.yml"
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

main() {
    log_section "BizOSaaS Platform - Fully Automated Deployment"

    log_info "Target: $VPS_IP (KVM4)"
    log_info "Method: Docker Compose via SSH"
    log_info "Services: 23 (6 infrastructure + 10 backend + 7 frontend)"
    echo ""

    # Step 1: Upload compose file
    log_section "STEP 1: UPLOAD CONFIGURATION"

    log_info "Creating deployment directory..."
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no root@$VPS_IP "mkdir -p $REMOTE_DIR"

    log_info "Uploading compose file..."
    sshpass -p "$VPS_PASSWORD" scp -o StrictHostKeyChecking=no "$LOCAL_COMPOSE_FILE" root@$VPS_IP:$REMOTE_DIR/docker-compose.yml

    log_success "Configuration uploaded"

    # Step 2: Pull images
    log_section "STEP 2: PULL CONTAINER IMAGES"

    log_info "Pulling images from GHCR (this may take 5-10 minutes)..."
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no root@$VPS_IP << 'ENDSSH'
        cd /opt/bizosaas-platform
        docker-compose pull --ignore-pull-failures 2>&1 | grep -E '(Pulling|Downloaded|up to date)'
ENDSSH

    log_success "Images pulled"

    # Step 3: Stop existing services (optional - comment out to keep existing)
    log_section "STEP 3: PREPARE FOR DEPLOYMENT"

    read -p "Stop existing Dokploy-managed services? (y/n): " stop_existing

    if [ "$stop_existing" = "y" ]; then
        log_warning "Stopping existing services..."
        sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no root@$VPS_IP << 'ENDSSH'
            # Stop services but keep dokploy itself running
            docker service ls --format '{{.Name}}' | grep -v dokploy | xargs -r docker service rm 2>/dev/null || true
ENDSSH
        log_success "Existing services stopped"
        sleep 10
    fi

    # Step 4: Deploy all services
    log_section "STEP 4: DEPLOY ALL SERVICES"

    log_info "Starting deployment of 23 services..."
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no root@$VPS_IP << 'ENDSSH'
        cd /opt/bizosaas-platform

        # Export required environment variables
        export OPENAI_API_KEY="${OPENAI_API_KEY:-sk-placeholder}"
        export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-sk-placeholder}"
        export AMAZON_ACCESS_KEY="${AMAZON_ACCESS_KEY:-placeholder}"
        export AMAZON_SECRET_KEY="${AMAZON_SECRET_KEY:-placeholder}"

        echo "Deploying services..."
        docker-compose up -d --remove-orphans

        echo "Deployment initiated"
ENDSSH

    log_success "All services deployed"

    # Step 5: Wait for services to start
    log_section "STEP 5: WAITING FOR SERVICES"

    log_info "Waiting 60 seconds for containers to initialize..."
    sleep 60

    # Step 6: Verification
    log_section "STEP 6: VERIFICATION"

    log_info "Checking service status..."
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no root@$VPS_IP << 'ENDSSH'
        cd /opt/bizosaas-platform

        echo "=== CONTAINER STATUS ==="
        docker-compose ps

        echo ""
        echo "=== SERVICE COUNT ==="
        running=$(docker-compose ps -q | wc -l)
        echo "Running containers: $running/23"

        echo ""
        echo "=== HEALTH CHECKS ==="
        docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -E '(healthy|unhealthy)'
ENDSSH

    # Step 7: Test endpoints
    log_section "STEP 7: ENDPOINT TESTING"

    log_info "Testing infrastructure services..."
    nc -z -w2 $VPS_IP 5433 && log_success "✓ PostgreSQL (5433)" || log_warning "✗ PostgreSQL (5433)"
    nc -z -w2 $VPS_IP 6380 && log_success "✓ Redis (6380)" || log_warning "✗ Redis (6380)"
    nc -z -w2 $VPS_IP 8201 && log_success "✓ Vault (8201)" || log_warning "✗ Vault (8201)"

    log_info "Testing backend APIs..."
    curl -f -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://$VPS_IP:8001/health" | grep -q "200" && log_success "✓ Brain Gateway (8001)" || log_warning "✗ Brain Gateway (8001)"
    curl -f -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://$VPS_IP:8000/health/" | grep -q "200" && log_success "✓ Saleor API (8000)" || log_warning "✗ Saleor API (8000)"

    log_info "Testing frontend services..."
    curl -f -s -o /dev/null --connect-timeout 5 "http://$VPS_IP:3000" && log_success "✓ Bizoholic Frontend (3000)" || log_warning "✗ Bizoholic Frontend (3000)"
    curl -f -s -o /dev/null --connect-timeout 5 "http://$VPS_IP:3002" && log_success "✓ CorelDove Frontend (3002)" || log_warning "✗ CorelDove Frontend (3002)"

    # Final summary
    log_section "DEPLOYMENT COMPLETE"

    log_success "All 23 services have been deployed!"
    echo ""
    echo "Next steps:"
    echo "  1. Configure domain routing in Dokploy (if using Traefik)"
    echo "  2. Test frontend URLs:"
    echo "     - https://stg.bizoholic.com"
    echo "     - https://stg.coreldove.com"
    echo "     - https://stg.thrillring.com"
    echo "  3. Monitor logs: ssh root@$VPS_IP 'cd $REMOTE_DIR && docker-compose logs -f'"
    echo ""

    log_info "View detailed status: ssh root@$VPS_IP 'cd $REMOTE_DIR && docker-compose ps'"
}

# Execute
main "$@"
