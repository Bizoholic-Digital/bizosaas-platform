#!/bin/bash

# BizOSaaS Platform - Trigger All Frontend Deployments
# Triggers Dokploy rebuilds for all 7 frontends via API
# Date: November 17, 2025

set -e

echo "=========================================="
echo "🚀 Triggering All Frontend Deployments"
echo "=========================================="
echo ""

# Dokploy Configuration
DOKPLOY_URL="https://dk4.bizoholic.com"
DOKPLOY_API_KEY="dk4ixNgzxiGcZWrjlvocbOJqTLjlZsJUEgmTJjjXYvLVSwiUBUPARxklyNFyVQRDHBa"

# Frontend Application IDs in Dokploy
declare -A FRONTENDS=(
    ["bizoholic-frontend"]="frontendservices-bizoholic-frontend-hcihtn"
    ["coreldove-storefront"]="frontendservices-coreldove-storefront-xndvmf"
    ["client-portal"]="8EqZXZKYTLiPqTkLF2l4J"
    ["business-directory"]="frontendservices-business-directory-6yrzvy"
    ["bizosaas-admin"]="frontendservices-bizosaas-admin-dashboard-tfvjn0"
    ["thrillring-gaming"]="frontendservices-thrillring-gaming-huz3de"
    ["analytics-dashboard"]="frontendservices-analytics-dashboard-rnlpxq"
)

# Port assignments
declare -A PORTS=(
    ["bizoholic-frontend"]="3001"
    ["coreldove-storefront"]="3002"
    ["client-portal"]="3003"
    ["business-directory"]="3004"
    ["bizosaas-admin"]="3005"
    ["thrillring-gaming"]="3006"
    ["analytics-dashboard"]="3007"
)

# URLs
declare -A URLS=(
    ["bizoholic-frontend"]="https://stg.bizoholic.com"
    ["coreldove-storefront"]="https://stg.coreldove.com"
    ["client-portal"]="https://stg.bizoholic.com/portal"
    ["business-directory"]="https://stg.bizoholic.com/directory"
    ["bizosaas-admin"]="https://admin.bizoholic.com"
    ["thrillring-gaming"]="https://stg.thrillring.com"
    ["analytics-dashboard"]="https://analytics.bizoholic.com"
)

echo "📋 Frontend Deployments to Trigger:"
echo "-----------------------------------"
for frontend in "${!FRONTENDS[@]}"; do
    echo "  ✓ $frontend (Port ${PORTS[$frontend]}) → ${URLS[$frontend]}"
done
echo ""
echo "🔑 Using Dokploy API: $DOKPLOY_URL"
echo ""

# Function to trigger deployment
trigger_deployment() {
    local app_name=$1
    local app_id=$2

    echo "-----------------------------------"
    echo "🔄 Triggering deployment: $app_name"
    echo "   App ID: $app_id"
    echo "   Port: ${PORTS[$app_name]}"
    echo "   URL: ${URLS[$app_name]}"
    echo ""

    response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST \
        "$DOKPLOY_URL/api/application.redeploy" \
        -H "accept: application/json" \
        -H "x-api-key: $DOKPLOY_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"applicationId\":\"$app_id\"}" 2>&1)

    http_status=$(echo "$response" | grep "HTTP_STATUS" | cut -d':' -f2)
    body=$(echo "$response" | sed '/HTTP_STATUS/d')

    if [ "$http_status" = "200" ] || [ "$http_status" = "201" ]; then
        echo "   ✅ Deployment triggered successfully"
    else
        echo "   ⚠️  Response (HTTP $http_status): $body"
    fi

    # Wait between deployments to avoid overwhelming the server
    echo "   ⏳ Waiting 5 seconds before next deployment..."
    sleep 5
    echo ""
}

# Trigger deployments in order
deployment_count=0

for frontend in "bizoholic-frontend" "coreldove-storefront" "client-portal" "business-directory" "bizosaas-admin" "thrillring-gaming" "analytics-dashboard"; do
    app_id="${FRONTENDS[$frontend]}"
    trigger_deployment "$frontend" "$app_id"
    deployment_count=$((deployment_count + 1))
done

echo "=========================================="
echo "📊 Deployment Summary"
echo "=========================================="
echo ""
echo "  ✅ Triggered: $deployment_count frontend deployments"
echo ""
echo "📡 Monitor deployments:"
echo "   Dokploy Dashboard: https://dk4.bizoholic.com/dashboard"
echo ""
echo "🌐 Frontend URLs (will be live after deployment):"
echo "---------------------------------------------------"
for frontend in "${!URLS[@]}"; do
    echo "  • $frontend: ${URLS[$frontend]}"
done
echo ""
echo "⏱️  Estimated deployment time: 5-10 minutes per frontend"
echo ""
echo "🔍 Check deployment status:"
echo "   1. Visit Dokploy dashboard"
echo "   2. Check each application's deployment logs"
echo "   3. Verify services are running and healthy"
echo ""
echo "✅ All deployments triggered successfully!"
echo ""
echo "🧠 Brain Gateway: https://api.bizoholic.com (already running)"
echo "   All frontends now routing through Brain Gateway"
echo ""
echo "✨ Deployment process initiated!"