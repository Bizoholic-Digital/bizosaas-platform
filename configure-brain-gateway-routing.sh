#!/bin/bash

# BizOSaaS Platform - Configure Brain Gateway Routing
# Updates all frontends to properly route through the centralized Brain API Gateway
# Date: November 17, 2025

set -e

echo "=========================================="
echo "🧠 Configuring Brain Gateway Routing"
echo "=========================================="
echo ""
echo "This script will update all 7 frontends to properly route"
echo "through the centralized Brain API Gateway"
echo ""

# Base directory
BASE_DIR="/home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps"

# Brain Gateway configuration
BRAIN_GATEWAY_URL="http://localhost:8001"
BRAIN_GATEWAY_URL_PROD="https://api.bizoholic.com"

echo "📋 Configuration Plan:"
echo "----------------------"
echo "1. Update .env.local files to use Brain Gateway"
echo "2. Fix next.config.js API rewrites"
echo "3. Ensure middleware exists for auth"
echo ""

# Function to update .env.local for Brain Gateway routing
update_env_local() {
    local app_name=$1
    local app_dir=$2
    local port=$3

    echo "📝 Updating .env.local for $app_name..."

    # Backup existing .env.local if it exists
    if [ -f "$app_dir/.env.local" ]; then
        cp "$app_dir/.env.local" "$app_dir/.env.local.backup-$(date +%Y%m%d-%H%M%S)"
    fi

    # Create new .env.local with Brain Gateway configuration
    cat > "$app_dir/.env.local" << EOF
# Brain Gateway Configuration (ALL API calls go through here)
NEXT_PUBLIC_API_URL=$BRAIN_GATEWAY_URL
NEXT_PUBLIC_API_BASE_URL=$BRAIN_GATEWAY_URL
NEXT_PUBLIC_BRAIN_GATEWAY_URL=$BRAIN_GATEWAY_URL

# Production Brain Gateway
NEXT_PUBLIC_API_URL_PROD=$BRAIN_GATEWAY_URL_PROD
NEXT_PUBLIC_BRAIN_GATEWAY_URL_PROD=$BRAIN_GATEWAY_URL_PROD

# Authentication (through Brain Gateway)
NEXT_PUBLIC_AUTH_API_URL=$BRAIN_GATEWAY_URL/auth

# Platform Configuration
NEXT_PUBLIC_PLATFORM_NAME=$app_name
NEXT_PUBLIC_TENANT_SLUG=$app_name
PORT=$port

# Feature Flags
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
NEXT_PUBLIC_ENABLE_HITL=true
NEXT_PUBLIC_ENABLE_ANALYTICS=true

# Environment
NODE_ENV=development
EOF

    echo "✅ Updated .env.local for $app_name"
}

# Update Bizoholic Frontend
update_env_local "bizoholic" "$BASE_DIR/bizoholic-frontend" "3001"

# Update CoreLDove Storefront
cat > "$BASE_DIR/coreldove-storefront/.env.local" << EOF
# Brain Gateway Configuration
NEXT_PUBLIC_API_BASE_URL=$BRAIN_GATEWAY_URL
NEXT_PUBLIC_SALEOR_API_URL=$BRAIN_GATEWAY_URL/api/saleor/graphql
NEXT_PUBLIC_AUTH_API_URL=$BRAIN_GATEWAY_URL/auth

# Storefront Configuration
NEXT_PUBLIC_STOREFRONT_URL=https://stg.coreldove.com
NEXT_PUBLIC_STOREFRONT_NAME=CoreLdove
NEXT_PUBLIC_PLATFORM_NAME=coreldove
NEXT_PUBLIC_TENANT_SLUG=coreldove

# Saleor Channel
SALEOR_CHANNEL=default-channel

# Feature Flags
NEXT_PUBLIC_ENABLE_ACCOUNT=true
NEXT_PUBLIC_ENABLE_CHECKOUT=true

# Environment
NODE_ENV=development
PORT=3002
EOF
echo "✅ Updated CoreLDove Storefront .env.local"

# Update Client Portal (already has some config)
cat > "$BASE_DIR/client-portal/.env.local" << EOF
# Brain Gateway Configuration (Centralized API)
NEXT_PUBLIC_API_URL=$BRAIN_GATEWAY_URL/api
NEXT_PUBLIC_BRAIN_GATEWAY_URL=$BRAIN_GATEWAY_URL/api
NEXT_PUBLIC_AUTH_API_URL=$BRAIN_GATEWAY_URL/api/auth
BRAIN_API_BASE_URL=$BRAIN_GATEWAY_URL/api

# Application
NEXT_PUBLIC_APP_NAME="BizOSaaS Client Portal"
NEXT_PUBLIC_APP_URL=http://localhost:3003
NEXT_PUBLIC_PLATFORM_NAME=client-portal
NEXT_PUBLIC_TENANT_SLUG=bizosaas
NODE_ENV=development
PORT=3003

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
NEXT_PUBLIC_ENABLE_GAMIFICATION=true
NEXT_PUBLIC_ENABLE_REVIEWS=true
NEXT_PUBLIC_ENABLE_BILLING=true
NEXT_PUBLIC_ENABLE_MULTI_TENANT=true
NEXT_PUBLIC_DEFAULT_TENANT=demo-tenant

# Security
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_EXPIRY=7d
NEXTAUTH_SECRET=your-nextauth-secret-key-change-in-production
NEXTAUTH_URL=http://localhost:3003
EOF
echo "✅ Updated Client Portal .env.local"

# Update Business Directory
update_env_local "business-directory" "$BASE_DIR/business-directory" "3004"

# Update BizOSaaS Admin
update_env_local "bizosaas-admin" "$BASE_DIR/bizosaas-admin" "3005"

# Update ThrillRing Gaming
update_env_local "thrillring" "$BASE_DIR/thrillring-gaming" "3006"

# Update Analytics Dashboard
update_env_local "analytics" "$BASE_DIR/analytics-dashboard" "3007"

echo ""
echo "=========================================="
echo "🔧 Updating next.config.js Files"
echo "=========================================="
echo ""

# Function to create standardized next.config.js with Brain Gateway routing
create_next_config() {
    local app_name=$1
    local app_dir=$2

    echo "📝 Updating next.config.js for $app_name..."

    # Backup existing next.config.js
    if [ -f "$app_dir/next.config.js" ]; then
        cp "$app_dir/next.config.js" "$app_dir/next.config.js.backup-$(date +%Y%m%d-%H%M%S)"
    fi

    # Create new next.config.js with Brain Gateway routing
    cat > "$app_dir/next.config.js" << 'EOF'
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,

  // API Rewrites - ALL requests go through Brain Gateway
  async rewrites() {
    const brainGatewayUrl = process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8001'

    return [
      // All API requests go to Brain Gateway
      {
        source: '/api/:path*',
        destination: `${brainGatewayUrl}/api/:path*`,
      },
      // Auth requests
      {
        source: '/auth/:path*',
        destination: `${brainGatewayUrl}/auth/:path*`,
      },
    ]
  },

  // Security headers
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
        ],
      },
    ]
  },

  // Image optimization
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
      },
      {
        protocol: 'https',
        hostname: 'api.bizoholic.com',
      },
    ],
  },
}

module.exports = nextConfig
EOF

    echo "✅ Updated next.config.js for $app_name"
}

# Update next.config.js for frontends that need it
create_next_config "Bizoholic Frontend" "$BASE_DIR/bizoholic-frontend"
create_next_config "Business Directory" "$BASE_DIR/business-directory"
create_next_config "BizOSaaS Admin" "$BASE_DIR/bizosaas-admin"
create_next_config "ThrillRing Gaming" "$BASE_DIR/thrillring-gaming"
create_next_config "Analytics Dashboard" "$BASE_DIR/analytics-dashboard"

# Note: Client Portal and CoreLDove Storefront already have custom configs

echo ""
echo "=========================================="
echo "📊 Configuration Summary"
echo "=========================================="
echo ""
echo "✅ Updated .env.local files for all 7 frontends"
echo "✅ All frontends now route through Brain Gateway"
echo "✅ Updated next.config.js files with API rewrites"
echo ""
echo "🌐 Brain Gateway URLs:"
echo "  Development: $BRAIN_GATEWAY_URL"
echo "  Production:  $BRAIN_GATEWAY_URL_PROD"
echo ""
echo "📋 Port Assignments:"
echo "  - Bizoholic Frontend:    3001"
echo "  - CoreLDove Storefront:  3002"
echo "  - Client Portal:         3003"
echo "  - Business Directory:    3004"
echo "  - BizOSaaS Admin:        3005"
echo "  - ThrillRing Gaming:     3006"
echo "  - Analytics Dashboard:   3007"
echo ""
echo "⚠️  Next Steps:"
echo "1. Ensure Brain Gateway is running on port 8001"
echo "2. Restart all frontend services"
echo "3. Test API calls through Brain Gateway"
echo "4. Verify authentication flow works"
echo ""
echo "✨ Brain Gateway Routing Configuration Complete!"