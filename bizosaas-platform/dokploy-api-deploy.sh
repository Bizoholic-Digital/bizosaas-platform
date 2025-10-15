#!/bin/bash

# BizOSaaS Platform - Dokploy API-Based Deployment
# Uses Dokploy REST API to trigger deployments programmatically

set -e

# Configuration
VPS_IP="194.238.16.237"
DOKPLOY_URL="https://dk.bizoholic.com"
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

    local url="${DOKPLOY_URL}${endpoint}"

    if [ -z "$data" ]; then
        curl -s -w "\nHTTP_CODE:%{http_code}" -X "$method" \
            -H "Authorization: Bearer $DOKPLOY_API_KEY" \
            -H "Content-Type: application/json" \
            "$url"
    else
        curl -s -w "\nHTTP_CODE:%{http_code}" -X "$method" \
            -H "Authorization: Bearer $DOKPLOY_API_KEY" \
            -H "Content-Type: application/json" \
            -d "$data" \
            "$url"
    fi
}

# Check Dokploy connectivity
check_dokploy() {
    log_section "CHECKING DOKPLOY CONNECTIVITY"

    log_info "Testing connection to Dokploy..."

    local response=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X GET \
        -H "Authorization: Bearer $DOKPLOY_API_KEY" \
        "${DOKPLOY_URL}/api/health" 2>&1)

    local http_code=$(echo "$response" | grep "HTTP_CODE" | cut -d: -f2)

    if [ "$http_code" == "200" ] || [ "$http_code" == "404" ]; then
        log_success "Dokploy is accessible"
        return 0
    else
        log_error "Cannot connect to Dokploy (HTTP $http_code)"
        return 1
    fi
}

# List projects
list_projects() {
    log_info "Listing Dokploy projects..."

    local response=$(dokploy_api "GET" "/api/project.all" "")

    echo "$response" | grep -v "HTTP_CODE" | jq '.' 2>/dev/null || echo "$response"
}

# Create project via Dokploy API
create_project() {
    local project_name=$1
    local description=$2

    log_info "Creating project: $project_name"

    local data="{\"name\":\"$project_name\",\"description\":\"$description\"}"

    local response=$(dokploy_api "POST" "/api/project.create" "$data")

    echo "$response" | grep -v "HTTP_CODE"
}

# Create compose application
create_compose_app() {
    local project_id=$1
    local app_name=$2
    local compose_path=$3

    log_info "Creating compose application: $app_name"

    local data=$(cat <<EOF
{
  "name": "$app_name",
  "projectId": "$project_id",
  "sourceType": "git",
  "repository": "$GITHUB_REPO",
  "branch": "$GITHUB_BRANCH",
  "composePath": "$compose_path",
  "buildType": "dockerfile"
}
EOF
)

    local response=$(dokploy_api "POST" "/api/compose.create" "$data")

    echo "$response" | grep -v "HTTP_CODE"
}

# Deploy via docker-compose directly to Dokploy server
deploy_via_docker_cli() {
    local compose_file=$1
    local project_name=$2

    log_section "DEPLOYING: $project_name"

    if [ ! -f "$compose_file" ]; then
        log_error "Compose file not found: $compose_file"
        return 1
    fi

    log_info "Deploying $project_name via Docker CLI..."

    # Use docker context or direct connection
    log_info "Checking if Docker context for VPS exists..."

    if docker context ls | grep -q "bizosaas-vps"; then
        log_success "Using existing Docker context: bizosaas-vps"
        docker context use bizosaas-vps
    else
        log_warning "Docker context not found. Will use local Docker."
        log_info "To deploy to VPS, create context with:"
        echo "  docker context create bizosaas-vps --docker host=ssh://root@$VPS_IP"
    fi

    # Deploy using docker-compose
    log_info "Deploying containers..."
    docker-compose -f "$compose_file" -p "$project_name" up -d --build

    log_success "$project_name deployment initiated"
}

# Trigger deployment via webhook (if configured)
trigger_webhook_deploy() {
    local webhook_url=$1
    local service_name=$2

    log_info "Triggering webhook deployment for: $service_name"

    curl -X POST "$webhook_url"

    log_success "Webhook triggered for $service_name"
}

# Check service health
check_service() {
    local url=$1
    local name=$2
    local max_attempts=${3:-10}

    log_info "Checking $name health at $url"

    for i in $(seq 1 $max_attempts); do
        if curl -f -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$url" | grep -q "200"; then
            log_success "$name is healthy"
            return 0
        fi

        if [ $i -lt $max_attempts ]; then
            log_warning "Attempt $i/$max_attempts failed. Retrying in 10s..."
            sleep 10
        fi
    done

    log_error "$name failed health check"
    return 1
}

# Main deployment orchestration
main() {
    log_section "BizOSaaS Platform - Automated Dokploy Deployment"

    log_info "VPS: $VPS_IP"
    log_info "Dokploy: $DOKPLOY_URL"
    log_info "Repository: $GITHUB_REPO"
    echo ""

    # Step 1: Check Dokploy connectivity
    check_dokploy

    # Step 2: List existing projects
    log_section "EXISTING PROJECTS"
    list_projects

    # Step 3: Provide deployment options
    log_section "DEPLOYMENT OPTIONS"

    echo "Choose deployment method:"
    echo ""
    echo "1. Docker CLI Deployment (requires docker context to VPS)"
    echo "2. Manual Dokploy UI Deployment (recommended)"
    echo "3. Show deployment instructions"
    echo ""

    read -p "Select option (1-3): " choice

    case $choice in
        1)
            log_info "Deploying via Docker CLI..."

            # Deploy backend services
            deploy_via_docker_cli \
                "$PROJECT_DIR/dokploy-backend-staging.yml" \
                "backend-services-staging"

            sleep 60

            # Deploy frontend services
            deploy_via_docker_cli \
                "$PROJECT_DIR/dokploy-frontend-staging.yml" \
                "frontend-services-staging"

            log_section "DEPLOYMENT INITIATED"
            log_info "Waiting for services to start..."
            sleep 120

            # Verify deployment
            bash "$PROJECT_DIR/check-services.sh"
            ;;

        2)
            log_section "MANUAL DEPLOYMENT VIA DOKPLOY UI"

            echo "Please follow these steps in Dokploy UI:"
            echo ""
            echo "1. Access: $DOKPLOY_URL"
            echo "2. Create project: 'backend-services'"
            echo "3. Add Docker Compose application:"
            echo "   - Repo: $GITHUB_REPO"
            echo "   - Branch: $GITHUB_BRANCH"
            echo "   - Compose: bizosaas-platform/dokploy-backend-staging.yml"
            echo "4. Deploy and wait for completion"
            echo "5. Repeat for 'frontend-services' with dokploy-frontend-staging.yml"
            echo ""

            read -p "Press ENTER after completing deployment in UI..."

            # Verify deployment
            bash "$PROJECT_DIR/check-services.sh"
            ;;

        3)
            log_section "DEPLOYMENT INSTRUCTIONS"
            cat "$PROJECT_DIR/QUICK_DEPLOYMENT_GUIDE.md"
            ;;

        *)
            log_error "Invalid option"
            exit 1
            ;;
    esac

    log_section "DEPLOYMENT COMPLETE"

    log_success "All deployment tasks completed"
    log_info "Run verification: ./verify-staging-deployment.sh"
}

main "$@"
