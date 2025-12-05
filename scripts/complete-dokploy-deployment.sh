#!/bin/bash

# BizOSaaS Platform - Complete Dokploy Deployment & Fix Script
# This script will:
# 1. Check current deployment status
# 2. Analyze error causes (path, dependency, build issues)
# 3. Fix root causes and trigger redeployment
# 4. Monitor deployment progress
# 5. Configure domains with SSL
# 6. Verify all services are healthy

set -e

# ========================================
# CONFIGURATION
# ========================================
DOKPLOY_URL="https://dk.bizoholic.com"
API_KEY="agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi"
VPS_IP="194.238.16.237"

# Compose IDs
BACKEND_COMPOSE_ID="uimFISkhg1KACigb2CaGz"
FRONTEND_COMPOSE_ID="hU2yhYOqv3_ftKGGvcAiv"

# Compose file paths (relative to GitHub repo root)
BACKEND_COMPOSE_PATH="./dokploy-backend-staging.yml"
FRONTEND_COMPOSE_PATH="./dokploy-frontend-staging.yml"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
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
# STATUS CHECKING
# ========================================
check_compose_detailed() {
    local compose_id=$1
    local name=$2

    log_info "Fetching detailed status for $name..."

    local response=$(dokploy_api "GET" "/compose.one?composeId=$compose_id")

    # Extract key information
    local compose_status=$(echo "$response" | jq -r '.composeStatus // "unknown"')
    local app_name=$(echo "$response" | jq -r '.appName // "unknown"')
    local compose_path=$(echo "$response" | jq -r '.composePath // "unknown"')
    local source_type=$(echo "$response" | jq -r '.sourceType // "unknown"')

    echo -e "  Name: ${CYAN}$app_name${NC}"
    echo -e "  Status: ${YELLOW}$compose_status${NC}"
    echo -e "  Path: ${BLUE}$compose_path${NC}"
    echo -e "  Source: ${BLUE}$source_type${NC}"

    echo "$compose_status"
}

get_latest_deployment() {
    local compose_id=$1

    local deployments=$(dokploy_api "GET" "/deployment.all?composeId=$compose_id")
    echo "$deployments" | jq -r 'if type=="array" then .[0].deploymentId else empty end' 2>/dev/null || echo ""
}

check_deployment_logs() {
    local compose_id=$1
    local name=$2

    log_info "Checking deployment logs for $name..."

    local deployment_id=$(get_latest_deployment "$compose_id")

    if [ -n "$deployment_id" ] && [ "$deployment_id" != "null" ]; then
        local deployment=$(dokploy_api "GET" "/deployment.one?deploymentId=$deployment_id")

        local status=$(echo "$deployment" | jq -r '.status // "unknown"')
        local title=$(echo "$deployment" | jq -r '.title // "unknown"')
        local description=$(echo "$deployment" | jq -r '.description // "unknown"')

        echo -e "  Deployment ID: ${CYAN}$deployment_id${NC}"
        echo -e "  Status: ${YELLOW}$status${NC}"
        echo -e "  Title: $title"

        if [ "$description" != "null" ] && [ -n "$description" ]; then
            echo -e "  Description: ${RED}$description${NC}"
        fi

        # Check for common error patterns
        if echo "$description" | grep -qi "no such file"; then
            log_error "Path issue detected: Compose file not found in repository"
            return 1
        elif echo "$description" | grep -qi "failed to build"; then
            log_error "Build issue detected: Docker build failed"
            return 2
        elif echo "$description" | grep -qi "dependency"; then
            log_error "Dependency issue detected"
            return 3
        fi
    else
        log_warning "No deployment history found"
    fi

    return 0
}

# ========================================
# DEPLOYMENT FIXING
# ========================================
update_compose_config() {
    local compose_id=$1
    local compose_path=$2
    local name=$3

    log_info "Updating $name compose configuration..."

    local data=$(cat <<EOF
{
  "composeId": "$compose_id",
  "composePath": "$compose_path"
}
EOF
)

    local response=$(dokploy_api "POST" "/compose.update" "$data")

    if echo "$response" | jq -e '.composeId' > /dev/null 2>&1; then
        log_success "$name configuration updated"
        return 0
    else
        log_error "Failed to update $name configuration"
        echo "Response: $response"
        return 1
    fi
}

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
        log_success "$name deployment triggered"
        echo "  Deployment ID: $deployment_id"
        return 0
    else
        log_error "Failed to trigger $name deployment"
        echo "Response: $response"
        return 1
    fi
}

# ========================================
# DEPLOYMENT MONITORING
# ========================================
monitor_deployment() {
    local compose_id=$1
    local name=$2
    local max_wait=3600  # 60 minutes max

    log_info "Monitoring $name deployment..."

    local start_time=$(date +%s)
    local last_status=""

    while true; do
        local current_time=$(date +%s)
        local elapsed=$((current_time - start_time))

        if [ $elapsed -gt $max_wait ]; then
            log_error "$name deployment timeout after 60 minutes"
            return 1
        fi

        local status=$(check_compose_detailed "$compose_id" "$name")

        if [ "$status" != "$last_status" ]; then
            log_info "$name status changed: $status"
            last_status="$status"
        fi

        if [ "$status" = "done" ]; then
            log_success "$name deployment completed successfully"
            return 0
        elif [ "$status" = "error" ]; then
            log_error "$name deployment failed"
            check_deployment_logs "$compose_id" "$name"
            return 1
        fi

        # Show progress
        local minutes=$((elapsed / 60))
        echo -ne "\r  Elapsed time: ${minutes}m (status: $status)"

        sleep 30
    done
}

# ========================================
# DOMAIN CONFIGURATION
# ========================================
configure_domain() {
    local compose_id=$1
    local domain=$2
    local port=$3
    local service_name=$4

    log_info "Configuring domain $domain for $service_name..."

    # Note: Dokploy domain configuration API might be different
    # This is a placeholder - actual implementation depends on Dokploy API
    log_warning "Domain configuration may need to be done via Dokploy UI"
    echo "  Domain: $domain"
    echo "  Port: $port"
    echo "  Service: $service_name"
}

# ========================================
# HEALTH VERIFICATION
# ========================================
verify_service_health() {
    local url=$1
    local name=$2

    log_info "Checking health of $name at $url..."

    local response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 "$url" 2>/dev/null || echo "000")

    if [ "$response" = "200" ] || [ "$response" = "301" ] || [ "$response" = "302" ]; then
        log_success "$name is healthy (HTTP $response)"
        return 0
    else
        log_warning "$name returned HTTP $response"
        return 1
    fi
}

verify_all_services() {
    log_section "VERIFYING ALL SERVICES"

    local healthy=0
    local total=0

    # Backend Services
    log_info "Backend Services:"
    for port in 8000 8001 8002 8003 8004 8005 8010 8085; do
        total=$((total + 1))
        if verify_service_health "http://$VPS_IP:$port/health" "Service on port $port"; then
            healthy=$((healthy + 1))
        fi
    done

    # Frontend Services
    log_info "Frontend Services:"
    for port in 3000 3001 3002 3004 3005 3009; do
        total=$((total + 1))
        if verify_service_health "http://$VPS_IP:$port" "Service on port $port"; then
            healthy=$((healthy + 1))
        fi
    done

    # Infrastructure Services
    log_info "Infrastructure Services:"
    for port in 5433 6380 8201 7234 8083 8088; do
        total=$((total + 1))
        if verify_service_health "http://$VPS_IP:$port" "Service on port $port" 2>/dev/null || nc -z -w5 $VPS_IP $port 2>/dev/null; then
            healthy=$((healthy + 1))
            log_success "Service on port $port is accessible"
        else
            log_warning "Service on port $port is not accessible"
        fi
    done

    log_section "HEALTH SUMMARY"
    echo -e "Healthy Services: ${GREEN}$healthy${NC} / ${total}"
    echo -e "Progress: $((healthy * 100 / total))%"

    if [ $healthy -eq $total ]; then
        log_success "All services are healthy!"
        return 0
    else
        log_warning "$((total - healthy)) services need attention"
        return 1
    fi
}

# ========================================
# MAIN EXECUTION
# ========================================
main() {
    log_section "BizOSaaS Platform Complete Deployment"

    log_info "Dokploy URL: $DOKPLOY_URL"
    log_info "VPS IP: $VPS_IP"
    log_info "Target: All 22 services"
    echo ""

    # Step 1: Check current status
    log_section "STEP 1: Checking Current Deployment Status"

    local backend_status=$(check_compose_detailed "$BACKEND_COMPOSE_ID" "Backend Services")
    echo ""
    local frontend_status=$(check_compose_detailed "$FRONTEND_COMPOSE_ID" "Frontend Applications")
    echo ""

    # Step 2: Analyze errors
    log_section "STEP 2: Analyzing Deployment Errors"

    local backend_error=0
    local frontend_error=0

    if [ "$backend_status" = "error" ] || [ "$backend_status" = "idle" ]; then
        check_deployment_logs "$BACKEND_COMPOSE_ID" "Backend Services"
        backend_error=$?
    fi

    if [ "$frontend_status" = "error" ] || [ "$frontend_status" = "idle" ]; then
        check_deployment_logs "$FRONTEND_COMPOSE_ID" "Frontend Applications"
        frontend_error=$?
    fi

    # Step 3: Fix and redeploy
    log_section "STEP 3: Fixing Issues and Redeploying"

    if [ "$backend_status" != "done" ]; then
        if [ $backend_error -eq 1 ]; then
            log_info "Fixing backend compose path..."
            update_compose_config "$BACKEND_COMPOSE_ID" "$BACKEND_COMPOSE_PATH" "Backend Services"
        fi

        trigger_deployment "$BACKEND_COMPOSE_ID" "Backend Services"
    fi

    if [ "$frontend_status" != "done" ]; then
        if [ $frontend_error -eq 1 ]; then
            log_info "Fixing frontend compose path..."
            update_compose_config "$FRONTEND_COMPOSE_ID" "$FRONTEND_COMPOSE_PATH" "Frontend Applications"
        fi

        trigger_deployment "$FRONTEND_COMPOSE_ID" "Frontend Applications"
    fi

    # Step 4: Monitor deployment
    log_section "STEP 4: Monitoring Deployment Progress"

    if [ "$backend_status" != "done" ]; then
        monitor_deployment "$BACKEND_COMPOSE_ID" "Backend Services" &
        backend_pid=$!
    fi

    if [ "$frontend_status" != "done" ]; then
        monitor_deployment "$FRONTEND_COMPOSE_ID" "Frontend Applications" &
        frontend_pid=$!
    fi

    # Wait for all deployments
    if [ -n "$backend_pid" ]; then
        wait $backend_pid
    fi

    if [ -n "$frontend_pid" ]; then
        wait $frontend_pid
    fi

    # Step 5: Configure domains
    log_section "STEP 5: Configuring Staging Domains"

    log_warning "Domain configuration should be done via Dokploy UI:"
    echo ""
    echo "Frontend Domains to Configure:"
    echo "  - stg.bizoholic.com → Port 3000"
    echo "  - stg.portal.bizoholic.com → Port 3001"
    echo "  - stg.coreldove.com → Port 3002"
    echo "  - stg.directory.bizoholic.com → Port 3003"
    echo "  - stg.thrillring.com → Port 3005"
    echo "  - stg.admin.bizoholic.com → Port 3009"
    echo ""
    echo "Enable SSL (Let's Encrypt) for all domains"
    echo ""

    # Step 6: Verify all services
    log_section "STEP 6: Verifying All Services"

    sleep 60  # Wait for services to stabilize

    verify_all_services

    # Final summary
    log_section "DEPLOYMENT COMPLETE"

    echo "Deployment Status:"
    echo "  Backend Services: $(check_compose_detailed "$BACKEND_COMPOSE_ID" "Backend" | tail -1)"
    echo "  Frontend Applications: $(check_compose_detailed "$FRONTEND_COMPOSE_ID" "Frontend" | tail -1)"
    echo ""
    echo "Next Steps:"
    echo "  1. Verify service health: http://$VPS_IP:8001/health"
    echo "  2. Configure domains in Dokploy UI: $DOKPLOY_URL"
    echo "  3. Test staging URLs: https://stg.bizoholic.com"
    echo ""
    echo "Monitor deployments at: $DOKPLOY_URL"
}

# Execute
main "$@"
