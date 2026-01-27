#!/bin/bash
# deploy-to-dokploy.sh
# Uses the Dokploy API to trigger a deployment of the staging services.

DOKPLOY_URL="https://dk.bizoholic.com"
API_KEY="mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"

# Project IDs
PORTAL_COMPOSE_ID="zz6VpI3h8BFXPUTZZb01G"
ADMIN_COMPOSE_ID="NlDPTf6BZgSQilinf2YaU"
BRAIN_COMPOSE_ID="QiOdwXQi4ZQCM3Qg_KNcl"

deploy_service() {
    local name=$1
    local id=$2
    echo "🚀 Triggering deployment for $name (ID: $id)..."
    
    response=$(curl -s -X POST -H "X-API-Key: $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"composeId\": \"$id\"}" \
        "$DOKPLOY_URL/api/compose.deploy")
    
    if echo "$response" | grep -q '"success":true'; then
        echo "✅ Deployment for $name queued successfully."
    else
        echo "❌ Failed to queue deployment for $name."
        echo "Response: $response"
    fi
}

echo "══════════════════════════════════════════════════"
echo "   BizOSaaS Platform - Dokploy API Deployer"
echo "══════════════════════════════════════════════════"

deploy_service "Client Portal" "$PORTAL_COMPOSE_ID"
deploy_service "Admin Dashboard" "$ADMIN_COMPOSE_ID"
deploy_service "Brain Core" "$BRAIN_COMPOSE_ID"

echo ""
echo "Monitor progress at: $DOKPLOY_URL"
echo "Note: It may take 5-10 minutes for Next.js to rebuild."
echo "══════════════════════════════════════════════════"
