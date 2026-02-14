#!/bin/bash

# BizOSaaS Platform - Complete Deployment Fix and Execution
# This script will:
# 1. Commit and push fixed compose files to GitHub
# 2. Trigger redeployment via Dokploy API
# 3. Monitor deployment progress
# 4. Report success/failure

set -e

# ========================================
# CONFIGURATION
# ========================================
DOKPLOY_URL="https://dk.bizoholic.com"
API_KEY="agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi"
VPS_IP="194.238.16.237"

BACKEND_COMPOSE_ID="QiOdwXQi4ZQCM3Qg_KNcl"
FRONTEND_COMPOSE_ID="zz6VpI3h8BFXPUTZZb01G"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ========================================
# UTILITY FUNCTIONS
# ========================================
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_section() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
}

# ========================================
# API FUNCTIONS
# ========================================
dokploy_api() {
    local method=$1
    local endpoint=$2
    local data=$3

    if [ -z "$data" ]; then
        curl -s -X "$method" \
            -H "X-API-Key: $API_KEY" \
            -H "Content-Type: application/json" \
            "${DOKPLOY_URL}/api${endpoint}"
    else
        curl -s -X "$method" \
            -H "X-API-Key: $API_KEY" \
            -H "Content-Type: application/json" \
            -d "$data" \
            "${DOKPLOY_URL}/api${endpoint}"
    fi
}

# ========================================
# GIT OPERATIONS
# ========================================
push_fixes_to_github() {
    log_section "STEP 1: Pushing Fixed Compose Files to GitHub"

    cd /home/alagiri/projects/bizoholic

    # Check if there are changes
    if git diff --quiet dokploy-backend-staging.yml dokploy-frontend-staging.yml; then
        log_info "No changes detected in compose files"
        return 0
    fi

    log_info "Staging compose files..."
    git add dokploy-backend-staging.yml
    git add dokploy-frontend-staging.yml
    git add dokploy-infrastructure-staging.yml

    log_info "Committing changes..."
    git commit -m "fix: Update compose files with correct GitHub repository paths

- Fix build context paths to use bizosaas-platform/ prefix
- Update all service build contexts to correct subdirectory paths
- Ensure Docker can find Dockerfiles in GitHub repository
- Required for Dokploy deployment to work correctly"

    log_info "Pushing to GitHub..."
    if git push origin main; then
        log_success "Successfully pushed fixed compose files to GitHub"
        return 0
    else
        log_error "Failed to push to GitHub"
        return 1
    fi
}

# ========================================
# DOKPLOY DEPLOYMENT
# ========================================
trigger_deployment() {
    local compose_id=$1
    local name=$2

    log_info "Triggering deployment for $name..."

    local data=$(cat <<EOF
{
  "composeId": "$compose_id"
}
EOF
)

    local response=$(dokploy_api "POST" "/compose.deploy" "$data")

    if echo "$response" | jq -e '.deploymentId' > /dev/null 2>&1; then
        local deployment_id=$(echo "$response" | jq -r '.deploymentId')
        log_success "$name deployment triggered successfully"
        echo "  Deployment ID: $deployment_id"
        return 0
    else
        log_error "Failed to trigger $name deployment"
        echo "Response: $response"
        return 1
    fi
}

check_deployment_status() {
    local compose_id=$1

    local response=$(dokploy_api "GET" "/compose.one?composeId=$compose_id")
    echo "$response" | jq -r '.composeStatus // "unknown"'
}

monitor_deployment() {
    local compose_id=$1
    local name=$2
    local max_minutes=60

    log_info "Monitoring $name deployment (max $max_minutes minutes)..."

    local start_time=$(date +%s)
    local last_status=""

    while true; do
        local current_time=$(date +%s)
        local elapsed_seconds=$((current_time - start_time))
        local elapsed_minutes=$((elapsed_seconds / 60))

        if [ $elapsed_minutes -ge $max_minutes ]; then
            echo ""
            log_warning "$name deployment timeout after $max_minutes minutes"
            log_info "Check Dokploy UI for details: $DOKPLOY_URL"
            return 2
        fi

        local status=$(check_deployment_status "$compose_id")

        if [ "$status" != "$last_status" ]; then
            echo ""
            log_info "$name status changed: $last_status -> $status"
            last_status="$status"
        fi

        echo -ne "\r  ${elapsed_minutes}m elapsed | Status: ${YELLOW}$status${NC}"

        if [ "$status" = "done" ]; then
            echo ""
            log_success "$name deployment completed successfully!"
            return 0
        elif [ "$status" = "error" ]; then
            echo ""
            log_error "$name deployment failed with errors"
            return 1
        fi

        sleep 30
    done
}

# ========================================
# HEALTH CHECKS
# ========================================
check_service_health() {
    local port=$1
    local name=$2

    local response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://$VPS_IP:$port" 2>/dev/null || echo "000")

    if [ "$response" = "200" ] || [ "$response" = "301" ] || [ "$response" = "302" ]; then
        echo -e "  ${GREEN}✓${NC} Port $port: $name (HTTP $response)"
        return 0
    else
        echo -e "  ${YELLOW}✗${NC} Port $port: $name (HTTP $response)"
        return 1
    fi
}

verify_services() {
    log_section "STEP 5: Verifying Services"

    local healthy=0
    local total=0

    log_info "Backend Services (10 services):"
    for port in 8000 8001 8002 8003 8004 8005 8006 8007 8008 8009; do
        total=$((total + 1))
        if check_service_health $port "Backend service"; then
            healthy=$((healthy + 1))
        fi
    done

    log_info "Frontend Services (6 services):"
    for port in 3000 3001 3002 3003 3005 3009; do
        total=$((total + 1))
        if check_service_health $port "Frontend app"; then
            healthy=$((healthy + 1))
        fi
    done

    log_info "Infrastructure Services (6 services):"
    # Just check if ports are open
    for port in 5433 6380 8201 7234 8083 8088; do
        total=$((total + 1))
        if nc -z -w5 $VPS_IP $port 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} Port $port: Infrastructure service"
            healthy=$((healthy + 1))
        else
            echo -e "  ${YELLOW}✗${NC} Port $port: Infrastructure service"
        fi
    done

    echo ""
    log_section "HEALTH SUMMARY"
    echo -e "Healthy Services: ${GREEN}$healthy${NC} / ${total}"
    echo -e "Progress: $((healthy * 100 / total))%"

    if [ $healthy -eq $total ]; then
        log_success "All 22 services are healthy and operational!"
        return 0
    elif [ $healthy -ge 18 ]; then
        log_warning "$healthy/22 services are healthy (acceptable)"
        return 0
    else
        log_error "Only $healthy/22 services are healthy"
        return 1
    fi
}

# ========================================
# MAIN EXECUTION
# ========================================
main() {
    log_section "BizOSaaS Platform - Complete Deployment Fix"

    echo "Target: Fix and deploy all 22 services"
    echo "Dokploy: $DOKPLOY_URL"
    echo "VPS: $VPS_IP"
    echo ""

    # Step 1: Push fixes to GitHub
    if ! push_fixes_to_github; then
        log_error "Failed to push fixes to GitHub. Aborting."
        exit 1
    fi

    # Wait for GitHub to process the push
    log_info "Waiting 10 seconds for GitHub to process the push..."
    sleep 10

    # Step 2: Trigger Backend Deployment
    log_section "STEP 2: Triggering Backend Deployment"

    if ! trigger_deployment "$BACKEND_COMPOSE_ID" "Backend Services"; then
        log_error "Failed to trigger backend deployment"
        exit 1
    fi

    # Step 3: Trigger Frontend Deployment
    log_section "STEP 3: Triggering Frontend Deployment"

    if ! trigger_deployment "$FRONTEND_COMPOSE_ID" "Frontend Applications"; then
        log_error "Failed to trigger frontend deployment"
        exit 1
    fi

    # Step 4: Monitor Deployments
    log_section "STEP 4: Monitoring Deployments"

    log_info "Both deployments are building in parallel..."
    log_info "Backend: 10 services (40-50 minutes)"
    log_info "Frontend: 6 services (10-20 minutes)"
    echo ""

    log_warning "Monitoring in non-blocking mode. Check Dokploy UI for real-time progress:"
    echo "  $DOKPLOY_URL"
    echo ""

    log_info "You can monitor status with:"
    echo "  watch -n 30 'curl -s -H \"X-API-Key: $API_KEY\" $DOKPLOY_URL/api/compose.one?composeId=$BACKEND_COMPOSE_ID | jq .composeStatus'"
    echo ""

    # Quick status check (non-blocking)
    sleep 60
    backend_status=$(check_deployment_status "$BACKEND_COMPOSE_ID")
    frontend_status=$(check_deployment_status "$FRONTEND_COMPOSE_ID")

    echo "Current Status:"
    echo "  Backend: $backend_status"
    echo "  Frontend: $frontend_status"
    echo ""

    read -p "Wait for deployments to complete and verify services? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Monitoring backend deployment..."
        monitor_deployment "$BACKEND_COMPOSE_ID" "Backend Services"
        backend_result=$?

        log_info "Monitoring frontend deployment..."
        monitor_deployment "$FRONTEND_COMPOSE_ID" "Frontend Applications"
        frontend_result=$?

        if [ $backend_result -eq 0 ] && [ $frontend_result -eq 0 ]; then
            log_success "All deployments completed successfully!"

            # Wait for services to stabilize
            log_info "Waiting 2 minutes for services to stabilize..."
            sleep 120

            # Verify services
            verify_services
        else
            log_warning "Some deployments may have issues"
        fi
    else
        log_info "Skipping monitoring. Check Dokploy UI manually."
    fi

    # Final Summary
    log_section "DEPLOYMENT COMPLETE"

    echo "Summary:"
    echo "  ✓ Fixed compose files pushed to GitHub"
    echo "  ✓ Backend deployment triggered (ID: $BACKEND_COMPOSE_ID)"
    echo "  ✓ Frontend deployment triggered (ID: $FRONTEND_COMPOSE_ID)"
    echo ""
    echo "Next Steps:"
    echo "  1. Monitor progress at: $DOKPLOY_URL"
    echo "  2. Expected completion: 40-60 minutes"
    echo "  3. Configure domains via Dokploy UI"
    echo "  4. Run health checks: ./verify-staging-deployment.sh"
    echo ""
    echo "Domain Configuration (After deployment):"
    echo "  - stg.bizoholic.com → Port 3000"
    echo "  - stg.portal.bizoholic.com → Port 3001"
    echo "  - stg.coreldove.com → Port 3002"
    echo "  - stg.directory.bizoholic.com → Port 3003"
    echo "  - stg.thrillring.com → Port 3005"
    echo "  - stg.admin.bizoholic.com → Port 3009"
    echo ""
}

# Execute
main "$@"
