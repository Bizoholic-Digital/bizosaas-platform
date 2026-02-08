#!/bin/bash

# BizOSaaS Platform - Dokploy API Direct Deployment
# This script uses Dokploy API to deploy all services correctly

set -e

# ========================================
# CONFIGURATION
# ========================================
DOKPLOY_URL="https://dk.bizoholic.com"
API_KEY="agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi"
VPS_IP="194.238.16.237"

# GitHub Configuration
GITHUB_REPO="https://github.com/Bizoholic-Digital/bizosaas-platform.git"
GITHUB_BRANCH="main"

# Compose file paths (relative to repo root)
INFRASTRUCTURE_COMPOSE_PATH="dokploy-infrastructure-staging.yml"
BACKEND_COMPOSE_PATH="dokploy-backend-staging.yml"
FRONTEND_COMPOSE_PATH="dokploy-frontend-staging.yml"

# Existing Compose IDs (if any)
BACKEND_COMPOSE_ID="uimFISkhg1KACigb2CaGz"
FRONTEND_COMPOSE_ID="hU2yhYOqv3_ftKGGvcAiv"

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
# PROJECT MANAGEMENT
# ========================================
get_or_create_project() {
    local project_name=$1
    local project_description=$2

    log_info "Checking for project: $project_name"

    # Get all projects
    local projects=$(dokploy_api "GET" "/project.all")

    # Check if project exists
    local project_id=$(echo "$projects" | jq -r ".[] | select(.name == \"$project_name\") | .projectId" 2>/dev/null | head -1)

    if [ -n "$project_id" ] && [ "$project_id" != "null" ]; then
        log_success "Project exists: $project_name (ID: $project_id)"
        echo "$project_id"
    else
        log_info "Creating new project: $project_name"

        local data=$(cat <<EOF
{
  "name": "$project_name",
  "description": "$project_description"
}
EOF
)

        local response=$(dokploy_api "POST" "/project.create" "$data")
        project_id=$(echo "$response" | jq -r '.projectId')

        if [ -n "$project_id" ] && [ "$project_id" != "null" ]; then
            log_success "Project created: $project_name (ID: $project_id)"
            echo "$project_id"
        else
            log_error "Failed to create project"
            echo "Response: $response"
            return 1
        fi
    fi
}

# ========================================
# COMPOSE DEPLOYMENT
# ========================================
deploy_or_update_compose() {
    local project_id=$1
    local compose_name=$2
    local compose_path=$3
    local compose_id=$4

    log_section "Deploying: $compose_name"

    # Check if compose already exists
    if [ -n "$compose_id" ] && [ "$compose_id" != "null" ]; then
        log_info "Updating existing compose: $compose_name (ID: $compose_id)"

        # Update compose configuration
        local update_data=$(cat <<EOF
{
  "composeId": "$compose_id",
  "name": "$compose_name",
  "composePath": "$compose_path",
  "sourceType": "github",
  "repository": "$GITHUB_REPO",
  "branch": "$GITHUB_BRANCH"
}
EOF
)

        local update_response=$(dokploy_api "POST" "/compose.update" "$update_data")

        if echo "$update_response" | jq -e '.composeId' > /dev/null 2>&1; then
            log_success "Compose updated successfully"
        else
            log_warning "Compose update may have failed"
            echo "Response: $update_response"
        fi

        # Trigger deployment
        log_info "Triggering deployment..."

        local deploy_data=$(cat <<EOF
{
  "composeId": "$compose_id"
}
EOF
)

        local deploy_response=$(dokploy_api "POST" "/compose.deploy" "$deploy_data")

        if echo "$deploy_response" | jq -e '.deploymentId' > /dev/null 2>&1; then
            local deployment_id=$(echo "$deploy_response" | jq -r '.deploymentId')
            log_success "Deployment triggered: $deployment_id"
            echo "$compose_id"
        else
            log_error "Failed to trigger deployment"
            echo "Response: $deploy_response"
            return 1
        fi
    else
        log_info "Creating new compose: $compose_name"

        # Create new compose
        local create_data=$(cat <<EOF
{
  "projectId": "$project_id",
  "name": "$compose_name",
  "composePath": "$compose_path",
  "sourceType": "github",
  "repository": "$GITHUB_REPO",
  "branch": "$GITHUB_BRANCH",
  "autoDeploy": false
}
EOF
)

        local create_response=$(dokploy_api "POST" "/compose.create" "$create_data")
        local new_compose_id=$(echo "$create_response" | jq -r '.composeId')

        if [ -n "$new_compose_id" ] && [ "$new_compose_id" != "null" ]; then
            log_success "Compose created: $new_compose_id"

            # Trigger initial deployment
            local deploy_data=$(cat <<EOF
{
  "composeId": "$new_compose_id"
}
EOF
)

            local deploy_response=$(dokploy_api "POST" "/compose.deploy" "$deploy_data")

            if echo "$deploy_response" | jq -e '.deploymentId' > /dev/null 2>&1; then
                local deployment_id=$(echo "$deploy_response" | jq -r '.deploymentId')
                log_success "Initial deployment triggered: $deployment_id"
            fi

            echo "$new_compose_id"
        else
            log_error "Failed to create compose"
            echo "Response: $create_response"
            return 1
        fi
    fi
}

# ========================================
# MONITORING
# ========================================
monitor_compose() {
    local compose_id=$1
    local name=$2

    log_info "Monitoring $name deployment..."

    local max_checks=120  # 60 minutes (30 sec intervals)
    local check_count=0

    while [ $check_count -lt $max_checks ]; do
        local status=$(dokploy_api "GET" "/compose.one?composeId=$compose_id" | jq -r '.composeStatus // "unknown"')

        echo -ne "\r  Status: ${YELLOW}$status${NC} (Check $check_count/$max_checks)"

        if [ "$status" = "done" ]; then
            echo ""
            log_success "$name deployment completed successfully"
            return 0
        elif [ "$status" = "error" ]; then
            echo ""
            log_error "$name deployment failed"
            return 1
        fi

        sleep 30
        check_count=$((check_count + 1))
    done

    echo ""
    log_warning "$name deployment timeout after 60 minutes"
    return 2
}

# ========================================
# MAIN EXECUTION
# ========================================
main() {
    log_section "BizOSaaS Platform - Dokploy API Deployment"

    log_info "Configuration:"
    echo "  Dokploy URL: $DOKPLOY_URL"
    echo "  GitHub Repo: $GITHUB_REPO"
    echo "  Branch: $GITHUB_BRANCH"
    echo ""

    # Step 1: Ensure projects exist
    log_section "STEP 1: Managing Projects"

    INFRA_PROJECT_ID=$(get_or_create_project "bizosaas-infrastructure-staging" "BizOSaaS Infrastructure Services (6 containers)")
    BACKEND_PROJECT_ID=$(get_or_create_project "bizosaas-backend-staging" "BizOSaaS Backend Services (10 containers)")
    FRONTEND_PROJECT_ID=$(get_or_create_project "bizosaas-frontend-staging" "BizOSaaS Frontend Applications (6 containers)")

    echo ""
    log_info "Project IDs:"
    echo "  Infrastructure: $INFRA_PROJECT_ID"
    echo "  Backend: $BACKEND_PROJECT_ID"
    echo "  Frontend: $FRONTEND_PROJECT_ID"

    # Step 2: Deploy Infrastructure (if not already running)
    log_section "STEP 2: Infrastructure Deployment"

    log_info "Checking if infrastructure is already running..."

    if nc -z -w5 $VPS_IP 5433 2>/dev/null && nc -z -w5 $VPS_IP 6380 2>/dev/null; then
        log_success "Infrastructure appears to be running (PostgreSQL and Redis accessible)"
    else
        log_warning "Infrastructure may not be running. Consider deploying infrastructure first."
        read -p "Deploy infrastructure now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            INFRA_COMPOSE_ID=$(deploy_or_update_compose "$INFRA_PROJECT_ID" "infrastructure-staging" "$INFRASTRUCTURE_COMPOSE_PATH" "")
            log_info "Waiting for infrastructure to stabilize (2 minutes)..."
            sleep 120
        fi
    fi

    # Step 3: Deploy Backend Services
    log_section "STEP 3: Backend Services Deployment"

    BACKEND_COMPOSE_ID=$(deploy_or_update_compose "$BACKEND_PROJECT_ID" "backend-services-staging" "$BACKEND_COMPOSE_PATH" "$BACKEND_COMPOSE_ID")

    log_info "Backend Compose ID: $BACKEND_COMPOSE_ID"
    log_info "Backend services building (this will take 40-50 minutes)..."

    # Step 4: Deploy Frontend Applications
    log_section "STEP 4: Frontend Applications Deployment"

    FRONTEND_COMPOSE_ID=$(deploy_or_update_compose "$FRONTEND_PROJECT_ID" "frontend-apps-staging" "$FRONTEND_COMPOSE_PATH" "$FRONTEND_COMPOSE_ID")

    log_info "Frontend Compose ID: $FRONTEND_COMPOSE_ID"
    log_info "Frontend applications building (this will take 10-20 minutes)..."

    # Step 5: Monitor Deployments
    log_section "STEP 5: Monitoring Deployments"

    log_info "You can monitor progress at: $DOKPLOY_URL"
    echo ""
    echo "Compose IDs for reference:"
    echo "  Backend: $BACKEND_COMPOSE_ID"
    echo "  Frontend: $FRONTEND_COMPOSE_ID"
    echo ""

    read -p "Monitor deployments now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Monitoring backend deployment..."
        monitor_compose "$BACKEND_COMPOSE_ID" "Backend Services" &
        backend_pid=$!

        log_info "Monitoring frontend deployment..."
        monitor_compose "$FRONTEND_COMPOSE_ID" "Frontend Applications" &
        frontend_pid=$!

        wait $backend_pid
        backend_result=$?

        wait $frontend_pid
        frontend_result=$?

        if [ $backend_result -eq 0 ] && [ $frontend_result -eq 0 ]; then
            log_success "All deployments completed successfully!"
        else
            log_warning "Some deployments may have issues. Check Dokploy UI for details."
        fi
    fi

    # Step 6: Summary
    log_section "DEPLOYMENT SUMMARY"

    echo "Compose IDs (save these for future reference):"
    echo "  Backend Services: $BACKEND_COMPOSE_ID"
    echo "  Frontend Applications: $FRONTEND_COMPOSE_ID"
    echo ""
    echo "Next Steps:"
    echo "  1. Monitor deployment progress at: $DOKPLOY_URL"
    echo "  2. Configure staging domains via Dokploy UI"
    echo "  3. Run health checks: ./verify-staging-deployment.sh"
    echo ""
    echo "Expected completion time: 60-75 minutes"
    echo ""
}

# Execute
main "$@"
