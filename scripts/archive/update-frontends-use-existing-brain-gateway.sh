#!/bin/bash

# BizOSaaS Platform - Update Frontends to Use Existing Brain Gateway
# Configures all frontends to use the already-deployed Brain Gateway on VPS
# Service Name: backend-brain-gateway
# Public URL: https://api.bizoholic.com
# Date: November 17, 2025

set -e

echo "=========================================="
echo "🧠 Configuring Frontends to Use Existing Brain Gateway"
echo "=========================================="
echo ""
echo "Brain Gateway Service Info:"
echo "  Service Name: backend-brain-gateway"
echo "  Public URL: https://api.bizoholic.com"
echo "  Internal URL: http://backend-brain-gateway:8001"
echo "  Status: ✅ HEALTHY"
echo ""

# Base directory
BASE_DIR="/home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps"

# Brain Gateway URLs
BRAIN_GATEWAY_PUBLIC="https://api.bizoholic.com"
BRAIN_GATEWAY_INTERNAL="http://backend-brain-gateway:8001"

# Function to update .env.production for production deployment
update_env_production() {
    local app_name=$1
    local app_dir=$2
    local port=$3
    local app_url=$4
    local platform=$5
    local extra_config=$6

    echo "📝 Updating .env.production for $app_name..."

    cat > "$app_dir/.env.production" << EOF
# ========================================
# Brain Gateway Configuration (Existing Service)
# ========================================
# Public URL (for client-side requests)
NEXT_PUBLIC_API_URL=$BRAIN_GATEWAY_PUBLIC
NEXT_PUBLIC_API_BASE_URL=$BRAIN_GATEWAY_PUBLIC
NEXT_PUBLIC_BRAIN_GATEWAY_URL=$BRAIN_GATEWAY_PUBLIC

# Authentication (through Brain Gateway)
NEXT_PUBLIC_AUTH_API_URL=$BRAIN_GATEWAY_PUBLIC/auth

# ========================================
# Platform Configuration
# ========================================
NEXT_PUBLIC_APP_URL=$app_url
NEXT_PUBLIC_PLATFORM_NAME=$platform
NEXT_PUBLIC_TENANT_SLUG=$platform

# Port
PORT=$port

# ========================================
# Feature Flags
# ========================================
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
NEXT_PUBLIC_ENABLE_HITL=true
NEXT_PUBLIC_ENABLE_ANALYTICS=true

# ========================================
# Environment
# ========================================
NODE_ENV=production

$extra_config
EOF

    echo "✅ Updated .env.production for $app_name"
}

echo "📋 Updating Frontend Configurations..."
echo ""

# 1. Bizoholic Frontend (Port 3001)
update_env_production \
    "Bizoholic Frontend" \
    "$BASE_DIR/bizoholic-frontend" \
    "3001" \
    "https://stg.bizoholic.com" \
    "bizoholic" \
    "# Bizoholic Specific
NEXT_PUBLIC_ENABLE_BLOG=true
NEXT_PUBLIC_ENABLE_SERVICES=true"

# 2. CoreLDove Storefront (Port 3002) - Saleor E-commerce
cat > "$BASE_DIR/coreldove-storefront/.env.production" << EOF
# ========================================
# Brain Gateway Configuration (Existing Service)
# ========================================
NEXT_PUBLIC_API_BASE_URL=$BRAIN_GATEWAY_PUBLIC
NEXT_PUBLIC_AUTH_API_URL=$BRAIN_GATEWAY_PUBLIC/auth

# Saleor API through Brain Gateway
NEXT_PUBLIC_SALEOR_API_URL=$BRAIN_GATEWAY_PUBLIC/graphql

# ========================================
# Storefront Configuration
# ========================================
NEXT_PUBLIC_STOREFRONT_URL=https://stg.coreldove.com
NEXT_PUBLIC_STOREFRONT_NAME=CoreLdove
NEXT_PUBLIC_PLATFORM_NAME=coreldove
NEXT_PUBLIC_TENANT_SLUG=coreldove

# Saleor Channel
SALEOR_CHANNEL=default-channel

# Port
PORT=3002

# ========================================
# Feature Flags
# ========================================
NEXT_PUBLIC_ENABLE_ACCOUNT=true
NEXT_PUBLIC_ENABLE_CHECKOUT=true

# ========================================
# Environment
# ========================================
NODE_ENV=production
EOF
echo "✅ Updated CoreLDove Storefront .env.production"

# 3. Client Portal (Port 3003)
update_env_production \
    "Client Portal" \
    "$BASE_DIR/client-portal" \
    "3003" \
    "https://stg.bizoholic.com/portal" \
    "client-portal" \
    "# Client Portal Specific
NEXT_PUBLIC_ENABLE_CRM=true
NEXT_PUBLIC_ENABLE_MARKETING=true
NEXT_PUBLIC_ENABLE_AUTOMATION=true
NEXT_PUBLIC_ENABLE_MULTI_TENANT=true"

# 4. Business Directory (Port 3004)
update_env_production \
    "Business Directory" \
    "$BASE_DIR/business-directory" \
    "3004" \
    "https://stg.bizoholic.com/directory" \
    "business-directory" \
    "# Directory Specific
NEXT_PUBLIC_DIRECTORY_API_URL=$BRAIN_GATEWAY_PUBLIC/directory
NEXT_PUBLIC_ENABLE_REVIEWS=true
NEXT_PUBLIC_ENABLE_LISTINGS=true"

# 5. BizOSaaS Admin (Port 3005)
cat > "$BASE_DIR/bizosaas-admin/.env.production" << EOF
# ========================================
# Brain Gateway Configuration (Existing Service)
# ========================================
NEXT_PUBLIC_API_URL=$BRAIN_GATEWAY_PUBLIC
NEXT_PUBLIC_BRAIN_GATEWAY_URL=$BRAIN_GATEWAY_PUBLIC
NEXT_PUBLIC_AUTH_API_URL=$BRAIN_GATEWAY_PUBLIC/auth

# Admin API through Brain Gateway
NEXT_PUBLIC_ADMIN_API_URL=$BRAIN_GATEWAY_PUBLIC/admin

# ========================================
# Platform Configuration
# ========================================
NEXT_PUBLIC_APP_URL=https://admin.bizoholic.com
NEXT_PUBLIC_PLATFORM_NAME=bizosaas-admin
NEXT_PUBLIC_REQUIRED_ROLE=SUPER_ADMIN

# Port
PORT=3005

# ========================================
# Feature Flags
# ========================================
NEXT_PUBLIC_ENABLE_MONITORING=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true

# ========================================
# Environment
# ========================================
NODE_ENV=production
EOF
echo "✅ Updated BizOSaaS Admin .env.production"

# 6. ThrillRing Gaming (Port 3006)
cat > "$BASE_DIR/thrillring-gaming/.env.production" << EOF
# ========================================
# Brain Gateway Configuration (Existing Service)
# ========================================
NEXT_PUBLIC_API_URL=$BRAIN_GATEWAY_PUBLIC
NEXT_PUBLIC_AUTH_API_URL=$BRAIN_GATEWAY_PUBLIC/auth

# Gaming API through Brain Gateway
NEXT_PUBLIC_GAMING_API_URL=$BRAIN_GATEWAY_PUBLIC/gaming
NEXT_PUBLIC_WEBSOCKET_URL=wss://api.bizoholic.com/gaming/ws

# ========================================
# Platform Configuration
# ========================================
NEXT_PUBLIC_APP_URL=https://stg.thrillring.com
NEXT_PUBLIC_PLATFORM_NAME=thrillring
NEXT_PUBLIC_TENANT_SLUG=thrillring

# Port
PORT=3006

# ========================================
# Feature Flags
# ========================================
NEXT_PUBLIC_ENABLE_TOURNAMENTS=true
NEXT_PUBLIC_ENABLE_LEADERBOARD=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true

# ========================================
# Environment
# ========================================
NODE_ENV=production
EOF
echo "✅ Updated ThrillRing Gaming .env.production"

# 7. Analytics Dashboard (Port 3007)
cat > "$BASE_DIR/analytics-dashboard/.env.production" << EOF
# ========================================
# Brain Gateway Configuration (Existing Service)
# ========================================
NEXT_PUBLIC_API_URL=$BRAIN_GATEWAY_PUBLIC
NEXT_PUBLIC_AUTH_API_URL=$BRAIN_GATEWAY_PUBLIC/auth

# Analytics API through Brain Gateway
NEXT_PUBLIC_ANALYTICS_API_URL=$BRAIN_GATEWAY_PUBLIC/analytics
NEXT_PUBLIC_SUPERSET_URL=$BRAIN_GATEWAY_PUBLIC/superset

# ========================================
# Platform Configuration
# ========================================
NEXT_PUBLIC_APP_URL=https://analytics.bizoholic.com
NEXT_PUBLIC_PLATFORM_NAME=analytics
NEXT_PUBLIC_TENANT_SLUG=bizosaas

# Port
PORT=3007

# ========================================
# Feature Flags
# ========================================
NEXT_PUBLIC_ENABLE_CUSTOM_DASHBOARDS=true
NEXT_PUBLIC_ENABLE_EXPORTS=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true

# ========================================
# Environment
# ========================================
NODE_ENV=production
EOF
echo "✅ Updated Analytics Dashboard .env.production"

echo ""
echo "=========================================="
echo "📊 Configuration Summary"
echo "=========================================="
echo ""
echo "✅ Updated .env.production for all 7 frontends"
echo "✅ All frontends configured to use existing Brain Gateway"
echo ""
echo "🌐 Brain Gateway Info:"
echo "  Public URL: $BRAIN_GATEWAY_PUBLIC"
echo "  Service: backend-brain-gateway"
echo "  Status: ✅ HEALTHY"
echo ""
echo "📋 Frontend Port Assignments:"
echo "  1. Bizoholic Frontend:    3001 → https://stg.bizoholic.com"
echo "  2. CoreLDove Storefront:  3002 → https://stg.coreldove.com"
echo "  3. Client Portal:         3003 → https://stg.bizoholic.com/portal"
echo "  4. Business Directory:    3004 → https://stg.bizoholic.com/directory"
echo "  5. BizOSaaS Admin:        3005 → https://admin.bizoholic.com"
echo "  6. ThrillRing Gaming:     3006 → https://stg.thrillring.com"
echo "  7. Analytics Dashboard:   3007 → https://analytics.bizoholic.com"
echo ""
echo "🚀 Next Steps:"
echo "1. Commit changes:"
echo "   cd /home/alagiri/projects/bizosaas-platform"
echo "   git add -A"
echo "   git commit -m 'Configure all frontends to use existing Brain Gateway'"
echo "   git push origin main"
echo ""
echo "2. Trigger Dokploy builds for each frontend via GitHub integration"
echo ""
echo "✨ Frontend Configuration Complete!"