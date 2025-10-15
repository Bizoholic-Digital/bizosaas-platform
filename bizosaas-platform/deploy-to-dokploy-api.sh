#!/bin/bash

# BizOSaaS Platform - Automated Dokploy API Deployment Script
# Deploys Backend Services (10 containers) and Frontend Applications (6 containers)
# Infrastructure (6 containers) assumed to be already running

set -e

# ========================================
# CONFIGURATION
# ========================================
VPS_IP="194.238.16.237"
DOKPLOY_URL="https://dk.bizoholic.com"
DOKPLOY_API_KEY="VumUVyBHPJQUlXiGnwVxeyKYBeGOLOttGjkgkGiwpSHLiEYegUBkCSTPFmQqMbtC"
GITHUB_REPO="https://github.com/Bizoholic-Digital/bizosaas-platform.git"
GITHUB_BRANCH="main"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

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
dokploy_api_call() {
    local method=$1
    local endpoint=$2
    local data=$3

    local url="${DOKPLOY_URL}/api/v1${endpoint}"

    log_info "API Call: $method $endpoint"

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

# ========================================
# PROJECT MANAGEMENT
# ========================================
list_projects() {
    log_info "Listing all Dokploy projects..."
    dokploy_api_call "GET" "/projects"
}

create_project() {
    local project_name=$1
    local project_description=$2

    log_info "Creating project: $project_name"

    local data=$(cat <<EOF
{
  "name": "$project_name",
  "description": "$project_description"
}
EOF
)

    dokploy_api_call "POST" "/projects" "$data"
}

get_project_id() {
    local project_name=$1

    local projects=$(list_projects)
    echo "$projects" | jq -r ".[] | select(.name == \"$project_name\") | .id"
}

# ========================================
# APPLICATION DEPLOYMENT
# ========================================
deploy_compose_application() {
    local project_id=$1
    local app_name=$2
    local compose_file_path=$3
    local compose_content=$4

    log_info "Deploying application: $app_name to project: $project_id"

    local data=$(cat <<EOF
{
  "name": "$app_name",
  "type": "compose",
  "composeFile": "$compose_content",
  "sourceProvider": "git",
  "repository": "$GITHUB_REPO",
  "branch": "$GITHUB_BRANCH",
  "composePath": "$compose_file_path"
}
EOF
)

    dokploy_api_call "POST" "/projects/$project_id/applications" "$data"
}

trigger_deployment() {
    local app_id=$1

    log_info "Triggering deployment for application: $app_id"

    dokploy_api_call "POST" "/applications/$app_id/deploy" ""
}

get_deployment_status() {
    local app_id=$1

    dokploy_api_call "GET" "/applications/$app_id/status"
}

# ========================================
# HEALTH CHECK FUNCTIONS
# ========================================
check_service_health() {
    local url=$1
    local service_name=$2
    local max_retries=${3:-30}
    local retry_interval=${4:-10}

    log_info "Checking health of $service_name at $url"

    for i in $(seq 1 $max_retries); do
        log_info "Attempt $i/$max_retries..."

        if curl -f -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$url" | grep -q "200"; then
            log_success "$service_name is healthy!"
            return 0
        fi

        if [ $i -lt $max_retries ]; then
            log_warning "$service_name not ready yet. Waiting $retry_interval seconds..."
            sleep $retry_interval
        fi
    done

    log_error "$service_name failed health check after $max_retries attempts"
    return 1
}

# ========================================
# DEPLOYMENT ORCHESTRATION
# ========================================
deploy_backend_services() {
    log_section "DEPLOYING BACKEND SERVICES (10 CONTAINERS)"

    # Check if project exists
    local project_name="backend-services"
    local project_id=$(get_project_id "$project_name")

    if [ -z "$project_id" ]; then
        log_info "Backend project not found. Creating..."
        create_project "$project_name" "BizOSaaS Backend Services - 10 Microservices APIs"
        project_id=$(get_project_id "$project_name")
        log_success "Backend project created with ID: $project_id"
    else
        log_info "Backend project already exists with ID: $project_id"
    fi

    # Read the compose file
    local compose_file="/home/alagiri/projects/bizoholic/bizosaas-platform/dokploy-backend-staging.yml"

    if [ ! -f "$compose_file" ]; then
        log_error "Backend compose file not found: $compose_file"
        return 1
    fi

    log_info "Backend compose file found. Preparing deployment..."

    # Note: Dokploy API might require actual file upload or direct compose content
    # This depends on the Dokploy API version. Adjust as needed.
    log_warning "Manual step required: Upload dokploy-backend-staging.yml via Dokploy UI"
    log_info "Project ID: $project_id"
    log_info "Compose file: $compose_file"

    echo ""
    echo "Backend Services to be deployed:"
    echo "  1. Saleor API (8000)"
    echo "  2. Brain API (8001)"
    echo "  3. Wagtail CMS (8002)"
    echo "  4. Django CRM (8003)"
    echo "  5. Business Directory (8004)"
    echo "  6. CorelDove Backend (8005)"
    echo "  7. Auth Service (8006)"
    echo "  8. Temporal Integration (8007)"
    echo "  9. AI Agents (8008)"
    echo "  10. Amazon Sourcing (8009)"
    echo ""
}

deploy_frontend_services() {
    log_section "DEPLOYING FRONTEND SERVICES (6 CONTAINERS)"

    # Check if project exists
    local project_name="frontend-services"
    local project_id=$(get_project_id "$project_name")

    if [ -z "$project_id" ]; then
        log_info "Frontend project not found. Creating..."
        create_project "$project_name" "BizOSaaS Frontend Applications - 6 Web Apps"
        project_id=$(get_project_id "$project_name")
        log_success "Frontend project created with ID: $project_id"
    else
        log_info "Frontend project already exists with ID: $project_id"
    fi

    # Read the compose file
    local compose_file="/home/alagiri/projects/bizoholic/bizosaas-platform/dokploy-frontend-staging.yml"

    if [ ! -f "$compose_file" ]; then
        log_error "Frontend compose file not found: $compose_file"
        return 1
    fi

    log_info "Frontend compose file found. Preparing deployment..."

    log_warning "Manual step required: Upload dokploy-frontend-staging.yml via Dokploy UI"
    log_info "Project ID: $project_id"
    log_info "Compose file: $compose_file"

    echo ""
    echo "Frontend Services to be deployed:"
    echo "  1. Bizoholic Frontend (3000)"
    echo "  2. Client Portal (3001)"
    echo "  3. CorelDove Frontend (3002)"
    echo "  4. Business Directory Frontend (3003)"
    echo "  5. ThrillRing Gaming (3005)"
    echo "  6. Admin Dashboard (3009)"
    echo ""
}

verify_infrastructure() {
    log_section "VERIFYING INFRASTRUCTURE (SHOULD BE RUNNING)"

    log_info "Checking infrastructure services..."

    # Check PostgreSQL
    log_info "Checking PostgreSQL availability..."
    if nc -z -w5 $VPS_IP 5433 2>/dev/null; then
        log_success "PostgreSQL is accessible on port 5433"
    else
        log_warning "PostgreSQL not accessible on port 5433"
    fi

    # Check Redis
    log_info "Checking Redis availability..."
    if nc -z -w5 $VPS_IP 6380 2>/dev/null; then
        log_success "Redis is accessible on port 6380"
    else
        log_warning "Redis not accessible on port 6380"
    fi

    # Check Vault
    log_info "Checking Vault availability..."
    if nc -z -w5 $VPS_IP 8201 2>/dev/null; then
        log_success "Vault is accessible on port 8201"
    else
        log_warning "Vault not accessible on port 8201"
    fi

    # Check Temporal Server
    log_info "Checking Temporal Server availability..."
    if nc -z -w5 $VPS_IP 7234 2>/dev/null; then
        log_success "Temporal Server is accessible on port 7234"
    else
        log_warning "Temporal Server not accessible on port 7234"
    fi

    # Check Temporal UI
    log_info "Checking Temporal UI availability..."
    if nc -z -w5 $VPS_IP 8083 2>/dev/null; then
        log_success "Temporal UI is accessible on port 8083"
    else
        log_warning "Temporal UI not accessible on port 8083"
    fi

    # Check Superset
    log_info "Checking Superset availability..."
    if nc -z -w5 $VPS_IP 8088 2>/dev/null; then
        log_success "Superset is accessible on port 8088"
    else
        log_warning "Superset not accessible on port 8088"
    fi
}

verify_deployment() {
    log_section "VERIFYING DEPLOYMENT"

    log_info "Waiting 60 seconds for services to start..."
    sleep 60

    # Backend health checks
    log_info "Checking backend services..."
    check_service_health "http://$VPS_IP:8001/health" "Brain API" 10 10
    check_service_health "http://$VPS_IP:8000/health/" "Saleor API" 10 10

    # Frontend health checks
    log_info "Checking frontend services..."
    check_service_health "http://$VPS_IP:3000/api/health" "Bizoholic Frontend" 10 10
    check_service_health "http://$VPS_IP:3002/api/health" "CorelDove Frontend" 10 10
}

# ========================================
# MAIN EXECUTION
# ========================================
main() {
    log_section "BizOSaaS Platform - Automated Dokploy Deployment"

    log_info "VPS: $VPS_IP"
    log_info "Dokploy: $DOKPLOY_URL"
    log_info "GitHub Repo: $GITHUB_REPO"
    log_info "GitHub Branch: $GITHUB_BRANCH"
    echo ""

    # Step 1: Verify infrastructure
    verify_infrastructure

    # Step 2: List existing projects
    log_section "CHECKING EXISTING PROJECTS"
    list_projects | jq '.'

    # Step 3: Deploy backend services
    deploy_backend_services

    # Step 4: Deploy frontend services
    deploy_frontend_services

    # Step 5: Provide manual deployment instructions
    log_section "MANUAL DEPLOYMENT STEPS"

    echo -e "${YELLOW}Since Dokploy API for compose file upload may require UI interaction,${NC}"
    echo -e "${YELLOW}please complete the deployment manually through Dokploy UI:${NC}"
    echo ""
    echo -e "${CYAN}1. Access Dokploy Dashboard:${NC}"
    echo "   URL: $DOKPLOY_URL"
    echo ""
    echo -e "${CYAN}2. For Backend Services Project:${NC}"
    echo "   - Navigate to 'backend-services' project"
    echo "   - Create new 'Docker Compose' application"
    echo "   - Upload: dokploy-backend-staging.yml"
    echo "   - Set environment variables (OPENAI_API_KEY, etc.)"
    echo "   - Click 'Deploy'"
    echo ""
    echo -e "${CYAN}3. For Frontend Services Project:${NC}"
    echo "   - Navigate to 'frontend-services' project"
    echo "   - Create new 'Docker Compose' application"
    echo "   - Upload: dokploy-frontend-staging.yml"
    echo "   - Click 'Deploy'"
    echo ""
    echo -e "${CYAN}4. Monitor Deployment:${NC}"
    echo "   - Watch build logs in Dokploy UI"
    echo "   - Expected build time: 60-75 minutes"
    echo "   - Total containers: 16 (10 backend + 6 frontend)"
    echo ""

    log_section "DEPLOYMENT SUMMARY"

    echo "Infrastructure Services: 6 containers (already running)"
    echo "Backend Services: 10 containers (to be deployed)"
    echo "Frontend Services: 6 containers (to be deployed)"
    echo "Total Platform: 22 containers"
    echo ""

    log_success "Deployment preparation complete!"
    echo ""
    echo "Next steps:"
    echo "  1. Complete manual deployment in Dokploy UI"
    echo "  2. Monitor deployment logs"
    echo "  3. Run verification script: ./verify-staging-deployment.sh"
    echo ""
}

# Execute main function
main "$@"
