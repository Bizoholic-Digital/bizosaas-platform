#!/bin/bash

# BizOSaaS Platform - Dokploy Deployment Status Check & Fix Script
# Checks current deployment status and redeploys if needed

set -e

# ========================================
# CONFIGURATION
# ========================================
DOKPLOY_URL="https://dk.bizoholic.com"
API_KEY="agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi"
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
}

# ========================================
# API CALL FUNCTION
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
# CHECK DEPLOYMENT STATUS
# ========================================
check_compose_status() {
    local compose_id=$1
    local name=$2

    log_section "Checking $name Status"

    local status=$(dokploy_api "GET" "/compose.one?composeId=$compose_id")

    echo "$status" | jq -r '{
        composeId: .composeId,
        name: .name,
        appName: .appName,
        composeStatus: .composeStatus,
        createdAt: .createdAt
    }'

    local compose_status=$(echo "$status" | jq -r '.composeStatus')

    if [ "$compose_status" = "error" ]; then
        log_error "$name deployment has error status"
        return 1
    elif [ "$compose_status" = "done" ]; then
        log_success "$name deployment is done"
        return 0
    else
        log_warning "$name deployment status: $compose_status"
        return 2
    fi
}

# ========================================
# TRIGGER DEPLOYMENT
# ========================================
trigger_deployment() {
    local compose_id=$1
    local name=$2

    log_section "Triggering $name Deployment"

    local response=$(dokploy_api "POST" "/compose.deploy" "{\"composeId\":\"$compose_id\"}")

    if echo "$response" | jq -e '.deploymentId' > /dev/null 2>&1; then
        local deployment_id=$(echo "$response" | jq -r '.deploymentId')
        log_success "$name deployment triggered successfully"
        echo "Deployment ID: $deployment_id"
        return 0
    else
        log_error "$name deployment trigger failed"
        echo "Response: $response"
        return 1
    fi
}

# ========================================
# GET DEPLOYMENT LOGS
# ========================================
get_deployment_logs() {
    local compose_id=$1
    local name=$2

    log_section "Fetching $name Deployment Logs"

    # Get latest deployment
    local deployments=$(dokploy_api "GET" "/deployment.all?composeId=$compose_id")
    local latest_deployment=$(echo "$deployments" | jq -r '.[0].deploymentId')

    if [ "$latest_deployment" != "null" ] && [ -n "$latest_deployment" ]; then
        log_info "Latest deployment ID: $latest_deployment"

        local logs=$(dokploy_api "GET" "/deployment.one?deploymentId=$latest_deployment")
        echo "$logs" | jq -r '.logPath'
    else
        log_warning "No deployments found for $name"
    fi
}

# ========================================
# CHECK SERVICES HEALTH
# ========================================
check_services_health() {
    local compose_id=$1
    local name=$2

    log_section "Checking $name Services Health"

    # This would require the services list endpoint
    # For now, we'll check the compose status
    local status=$(dokploy_api "GET" "/compose.one?composeId=$compose_id")
    echo "$status" | jq -r '.services[]? | {name: .name, status: .status}'
}

# ========================================
# MAIN EXECUTION
# ========================================
main() {
    log_section "BizOSaaS Dokploy Deployment Status Check"

    log_info "Dokploy URL: $DOKPLOY_URL"
    log_info "Backend Compose ID: $BACKEND_COMPOSE_ID"
    log_info "Frontend Compose ID: $FRONTEND_COMPOSE_ID"
    echo ""

    # Check Backend Status
    if check_compose_status "$BACKEND_COMPOSE_ID" "Backend Services"; then
        log_success "Backend services are deployed successfully"
    else
        log_error "Backend services have issues. Checking logs..."
        get_deployment_logs "$BACKEND_COMPOSE_ID" "Backend Services"

        read -p "Do you want to trigger backend redeployment? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            trigger_deployment "$BACKEND_COMPOSE_ID" "Backend Services"
        fi
    fi

    echo ""

    # Check Frontend Status
    if check_compose_status "$FRONTEND_COMPOSE_ID" "Frontend Applications"; then
        log_success "Frontend applications are deployed successfully"
    else
        log_error "Frontend applications have issues. Checking logs..."
        get_deployment_logs "$FRONTEND_COMPOSE_ID" "Frontend Applications"

        read -p "Do you want to trigger frontend redeployment? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            trigger_deployment "$FRONTEND_COMPOSE_ID" "Frontend Applications"
        fi
    fi

    log_section "Deployment Summary"
    echo "Backend Compose: $BACKEND_COMPOSE_ID"
    echo "Frontend Compose: $FRONTEND_COMPOSE_ID"
    echo ""
    echo "To monitor deployment progress:"
    echo "  - Visit: $DOKPLOY_URL"
    echo "  - Or use: watch -n 10 'bash $0'"
    echo ""
}

# Execute
main "$@"
