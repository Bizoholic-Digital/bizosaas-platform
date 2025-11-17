#!/bin/bash

# BizOSaaS Platform - Frontend Deployment Script
# Deploys all 7 frontends via Dokploy GitHub integration
# Date: November 17, 2025

set -e

echo "=========================================="
echo "🚀 BizOSaaS Frontend Deployment Script"
echo "=========================================="
echo ""
echo "This script will deploy all 7 frontends to Dokploy"
echo "Using GitHub integration for automatic builds"
echo ""

# Configuration
DOKPLOY_URL="https://dk4.bizoholic.com"
DOKPLOY_API_KEY="dk4ixNgzxiGcZWrjlvocbOJqTLjlZsJUEgmTJjjXYvLVSwiUBUPARxklyNFyVQRDHBa"

# Frontend services and their Dokploy application IDs
declare -A FRONTENDS=(
    ["bizoholic-frontend"]="frontendservices-bizoholic-frontend-hcihtn"
    ["coreldove-storefront"]="frontendservices-coreldove-storefront-xndvmf"
    ["client-portal"]="8EqZXZKYTLiPqTkLF2l4J"
    ["business-directory"]="frontendservices-business-directory-6yrzvy"
    ["bizosaas-admin"]="frontendservices-bizosaas-admin-dashboard-tfvjn0"
    ["thrillring-gaming"]="frontendservices-thrillring-gaming-huz3de"
    ["analytics-dashboard"]="frontendservices-analytics-dashboard-rnlpxq"
)

# Port assignments (for reference)
declare -A PORTS=(
    ["bizoholic-frontend"]="3001"
    ["coreldove-storefront"]="3002"
    ["client-portal"]="3003"
    ["business-directory"]="3004"
    ["bizosaas-admin"]="3005"
    ["thrillring-gaming"]="3006"
    ["analytics-dashboard"]="3007"
)

echo "📋 Frontend Port Assignments:"
echo "----------------------------"
for frontend in "${!PORTS[@]}"; do
    echo "  $frontend: Port ${PORTS[$frontend]}"
done
echo ""

# Function to trigger Dokploy rebuild
trigger_rebuild() {
    local app_name=$1
    local app_id=$2

    echo "🔄 Triggering rebuild for $app_name (ID: $app_id)..."

    response=$(curl -s -X POST "$DOKPLOY_URL/api/application.redeploy" \
        -H "accept: application/json" \
        -H "x-api-key: $DOKPLOY_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"applicationId\":\"$app_id\"}")

    if [[ $response == *"success"* ]] || [[ -z "$response" ]]; then
        echo "✅ $app_name deployment triggered successfully"
    else
        echo "⚠️  $app_name deployment response: $response"
    fi
}

# Function to check if changes exist for a frontend
check_changes() {
    local frontend=$1
    local path="bizosaas/frontend/apps/$frontend"

    # Check if there are any changes in the last commit for this frontend
    changes=$(git diff HEAD~1 HEAD --name-only | grep "^$path/" || true)

    if [[ -n "$changes" ]]; then
        return 0  # Changes found
    else
        return 1  # No changes
    fi
}

# Step 1: Ensure we're on the latest code
echo "📥 Pulling latest changes from GitHub..."
git pull origin main || true
echo ""

# Step 2: Check current branch
current_branch=$(git branch --show-current)
echo "📍 Current branch: $current_branch"
echo ""

# Step 3: Deploy each frontend
echo "🚀 Starting frontend deployments..."
echo "===================================="
echo ""

deployed_count=0
skipped_count=0

for frontend in "${!FRONTENDS[@]}"; do
    app_id="${FRONTENDS[$frontend]}"

    echo "-----------------------------------"
    echo "📦 Processing: $frontend"
    echo "-----------------------------------"

    # Check if there are changes for this frontend
    if check_changes "$frontend"; then
        echo "  ✓ Changes detected"
        trigger_rebuild "$frontend" "$app_id"
        deployed_count=$((deployed_count + 1))

        # Wait between deployments to avoid overwhelming the server
        echo "  ⏳ Waiting 10 seconds before next deployment..."
        sleep 10
    else
        echo "  ⏭️  No changes detected, skipping deployment"
        skipped_count=$((skipped_count + 1))
    fi

    echo ""
done

# Step 4: Summary
echo "=========================================="
echo "📊 Deployment Summary"
echo "=========================================="
echo "  ✅ Deployed: $deployed_count frontends"
echo "  ⏭️  Skipped: $skipped_count frontends (no changes)"
echo ""

# Step 5: Provide monitoring commands
echo "📡 Monitor deployments with these commands:"
echo "-------------------------------------------"
echo ""
echo "# Check all service status:"
echo "ssh root@72.60.219.244 'docker service ls | grep frontend'"
echo ""
echo "# View logs for a specific service:"
echo "ssh root@72.60.219.244 'docker service logs -f SERVICE_NAME'"
echo ""

# Step 6: Provide testing URLs
echo "🌐 Frontend URLs (once deployed):"
echo "---------------------------------"
echo "  Bizoholic Frontend:    https://stg.bizoholic.com"
echo "  CoreLDove Storefront:  https://stg.coreldove.com"
echo "  Client Portal:         https://stg.bizoholic.com/portal"
echo "  Business Directory:    https://stg.bizoholic.com/directory"
echo "  BizOSaaS Admin:        https://admin.bizoholic.com"
echo "  ThrillRing Gaming:     https://stg.thrillring.com"
echo "  Analytics Dashboard:   https://analytics.bizoholic.com"
echo ""

echo "✨ Deployment script completed!"
echo ""
echo "Note: Deployments are running in the background on Dokploy."
echo "Check the Dokploy dashboard for real-time status:"
echo "https://dk4.bizoholic.com"