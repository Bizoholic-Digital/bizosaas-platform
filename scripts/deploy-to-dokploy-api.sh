#!/bin/bash

# Configuration
DOKPLOY_URL="https://dk.bizoholic.com"
API_KEY="mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
VPS_IP="194.238.16.237"

# GitHub Configuration
GITHUB_ID="QZnupLM5a8IgYpTloLpdZ"
GITHUB_REPO="bizosaas-platform"
GITHUB_BRANCH="staging"

# Project/Compose Info
INFRA_ID="p4fmYaVZ_iDFDH4XSDnOU:j5ifoftZ7sMPQCpcSUBE3" # platform-core
BACKEND_ID="p4fmYaVZ_iDFDH4XSDnOU:j5ifoftZ7sMPQCpcSUBE3" # platform-core
FRONTEND_ID="WfVYVHpPQh_h5s4GpyDdW:KwC-1m4Iyih1qSw7A4pFS" # portals

# Existing Compose IDs
INFRA_COMPOSE_ID="osD7Up5T4VcZzok5yLyXo" # vault
BACKEND_COMPOSE_ID="QiOdwXQi4ZQCM3Qg_KNcl" # core-stack
FRONTEND_COMPOSE_ID="zz6VpI3h8BFXPUTZZb01G" # client-portal (updating to portals-apps)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper Functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1" >&2; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1" >&2; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1" >&2; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }
log_section() {
    echo -e "\n${CYAN}========================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}========================================${NC}"
}

dokploy_api() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    if [ "$method" == "GET" ]; then
        curl -s -X GET "$DOKPLOY_URL/api$endpoint" \
            -H "X-API-Key: $API_KEY"
    else
        curl -s -X "$method" "$DOKPLOY_URL/api$endpoint" \
            -H "X-API-Key: $API_KEY" \
            -H "Content-Type: application/json" \
            -d "$data"
    fi
}

deploy_github_compose() {
    local compose_id=$1
    local compose_name=$2
    local compose_path=$3
    
    log_info "Updating $compose_name (ID: $compose_id) using GITHUB mode..."
    
    local update_data=$(cat <<EOF
{
  "composeId": "$compose_id",
  "name": "$compose_name",
  "composePath": "$compose_path",
  "sourceType": "github",
  "githubId": "$GITHUB_ID",
  "owner": "$GITHUB_OWNER",
  "repository": "$GITHUB_REPO",
  "branch": "$GITHUB_BRANCH"
}
EOF
)
    
    local update_response=$(dokploy_api "POST" "/compose.update" "$update_data")
    
    if echo "$update_response" | jq -e '.composeId' > /dev/null 2>&1; then
        log_success "$compose_name configuration updated"
        
        log_info "Triggering deployment..."
        local deploy_response=$(dokploy_api "POST" "/compose.deploy" "{\"composeId\": \"$compose_id\"}")
        
        if echo "$deploy_response" | jq -e '.deploymentId or .success == true' > /dev/null 2>&1; then
            log_success "Deployment triggered successfully"
        else
            log_error "Failed to trigger deployment"
            echo "Response: $deploy_response"
        fi
    else
        log_error "Failed to update $compose_name"
        echo "Response: $update_response"
    fi
}

main() {
    log_section "BizOSaaS Platform - GitHub CI/CD Deployment"
    
    # Step 1: Deploy Infrastructure (Vault)
    log_section "STEP 1: Vault (Infrastructure)"
    deploy_github_compose "$INFRA_COMPOSE_ID" "vault" "dokploy-infrastructure-staging.yml"
    
    # Step 2: Deploy Backend Services (Core Stack)
    log_section "STEP 2: Core Stack (Backend Services)"
    deploy_github_compose "$BACKEND_COMPOSE_ID" "core-stack" "dokploy-backend-staging.yml"
    
    # Step 3: Deploy Frontend Applications (Portals)
    log_section "STEP 3: Portals Apps (Frontend)"
    deploy_github_compose "$FRONTEND_COMPOSE_ID" "portals-apps" "dokploy-frontend-staging.yml"
    
    echo -e "\n${GREEN}Deployment processes initiated via GitHub.${NC}"
    echo "Check progress at: $DOKPLOY_URL"
}

main
