#!/bin/bash

# BizOSaaS Platform - Brain Gateway Integration Setup
# Configures all frontends to connect through the centralized Brain API Gateway
# Date: November 17, 2025

set -e

echo "=========================================="
echo "🧠 BizOSaaS Brain Gateway Integration Setup"
echo "=========================================="
echo ""
echo "This script will configure all 7 frontends to connect"
echo "through the centralized Brain API Gateway with 93+ CrewAI agents"
echo ""

# Base directory
BASE_DIR="/home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps"

# Brain Gateway configuration
BRAIN_GATEWAY_URL="https://api.bizoholic.com"
BRAIN_GATEWAY_URL_LOCAL="http://localhost:8001"

# Function to create .env.local for a frontend
create_env_local() {
    local app_name=$1
    local app_dir=$2
    local port=$3
    local platform_name=$4
    local app_url=$5
    local tenant_slug=$6
    local extra_config=$7

    echo "📝 Creating .env.local for $app_name..."

    cat > "$app_dir/.env.local" << EOF
# Brain Gateway Configuration
NEXT_PUBLIC_API_URL=$BRAIN_GATEWAY_URL
NEXT_PUBLIC_BRAIN_GATEWAY_URL=$BRAIN_GATEWAY_URL
NEXT_PUBLIC_AUTH_API_URL=$BRAIN_GATEWAY_URL/auth

# Local Development Brain Gateway
NEXT_PUBLIC_API_URL_LOCAL=$BRAIN_GATEWAY_URL_LOCAL
NEXT_PUBLIC_BRAIN_GATEWAY_URL_LOCAL=$BRAIN_GATEWAY_URL_LOCAL
NEXT_PUBLIC_AUTH_API_URL_LOCAL=$BRAIN_GATEWAY_URL_LOCAL/auth

# Frontend Configuration
NEXT_PUBLIC_APP_URL=$app_url
NEXT_PUBLIC_PLATFORM_NAME=$platform_name
NEXT_PUBLIC_TENANT_SLUG=$tenant_slug

# Development Port
PORT=$port

# Feature Flags
NEXT_PUBLIC_ENABLE_AI_AGENTS=true
NEXT_PUBLIC_ENABLE_HITL=true
NEXT_PUBLIC_ENABLE_ANALYTICS=true

$extra_config
EOF

    echo "✅ Created .env.local for $app_name"
}

# Configure Client Portal
create_env_local \
    "Client Portal" \
    "$BASE_DIR/client-portal" \
    "3003" \
    "client-portal" \
    "https://stg.bizoholic.com/portal" \
    "bizosaas" \
    "# Client Portal Specific
NEXT_PUBLIC_ENABLE_CRM=true
NEXT_PUBLIC_ENABLE_MARKETING=true
NEXT_PUBLIC_ENABLE_AUTOMATION=true"

# Configure Bizoholic Frontend
create_env_local \
    "Bizoholic Frontend" \
    "$BASE_DIR/bizoholic-frontend" \
    "3001" \
    "bizoholic-frontend" \
    "https://stg.bizoholic.com" \
    "bizoholic" \
    "# Bizoholic Specific
NEXT_PUBLIC_ENABLE_BLOG=true
NEXT_PUBLIC_ENABLE_SERVICES=true"

# Configure CoreLDove Storefront
create_env_local \
    "CoreLDove Storefront" \
    "$BASE_DIR/coreldove-storefront" \
    "3002" \
    "coreldove-storefront" \
    "https://stg.coreldove.com" \
    "coreldove" \
    "# Saleor E-commerce Specific
NEXT_PUBLIC_SALEOR_API_URL=$BRAIN_GATEWAY_URL/graphql
NEXT_PUBLIC_SALEOR_CHANNEL=default-channel
NEXT_PUBLIC_ENABLE_CHECKOUT=true"

# Configure BizOSaaS Admin
create_env_local \
    "BizOSaaS Admin" \
    "$BASE_DIR/bizosaas-admin" \
    "3005" \
    "bizosaas-admin" \
    "https://admin.bizoholic.com" \
    "bizosaas" \
    "# Admin Specific
NEXT_PUBLIC_ADMIN_API_URL=$BRAIN_GATEWAY_URL/admin
NEXT_PUBLIC_REQUIRED_ROLE=SUPER_ADMIN
NEXT_PUBLIC_ENABLE_MONITORING=true"

# Configure Business Directory
create_env_local \
    "Business Directory" \
    "$BASE_DIR/business-directory" \
    "3004" \
    "business-directory" \
    "https://stg.bizoholic.com/directory" \
    "bizosaas" \
    "# Directory Specific
NEXT_PUBLIC_DIRECTORY_API_URL=$BRAIN_GATEWAY_URL/directory
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-google-maps-key
NEXT_PUBLIC_ENABLE_REVIEWS=true"

# Configure ThrillRing Gaming
create_env_local \
    "ThrillRing Gaming" \
    "$BASE_DIR/thrillring-gaming" \
    "3006" \
    "thrillring-gaming" \
    "https://stg.thrillring.com" \
    "thrillring" \
    "# Gaming Specific
NEXT_PUBLIC_GAMING_API_URL=$BRAIN_GATEWAY_URL/gaming
NEXT_PUBLIC_WEBSOCKET_URL=wss://api.bizoholic.com/gaming/ws
NEXT_PUBLIC_ENABLE_TOURNAMENTS=true
NEXT_PUBLIC_ENABLE_LEADERBOARD=true"

# Configure Analytics Dashboard
create_env_local \
    "Analytics Dashboard" \
    "$BASE_DIR/analytics-dashboard" \
    "3007" \
    "analytics-dashboard" \
    "https://analytics.bizoholic.com" \
    "bizosaas" \
    "# Analytics Specific
NEXT_PUBLIC_ANALYTICS_API_URL=$BRAIN_GATEWAY_URL/analytics
NEXT_PUBLIC_SUPERSET_URL=$BRAIN_GATEWAY_URL/superset
NEXT_PUBLIC_ENABLE_CUSTOM_DASHBOARDS=true
NEXT_PUBLIC_ENABLE_EXPORTS=true"

echo ""
echo "=========================================="
echo "🔧 Creating Middleware for Authentication"
echo "=========================================="
echo ""

# Function to create middleware.ts for each frontend
create_middleware() {
    local app_name=$1
    local app_dir=$2
    local public_routes=$3

    echo "🔐 Creating middleware.ts for $app_name..."

    cat > "$app_dir/middleware.ts" << 'EOF'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Define public routes that don't require authentication
const PUBLIC_ROUTES = [
EOF
    echo "  $public_routes" >> "$app_dir/middleware.ts"
    cat >> "$app_dir/middleware.ts" << 'EOF'
]

// Define API routes that should be proxied to Brain Gateway
const API_ROUTES = ['/api/']

export function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname
  const isPublicRoute = PUBLIC_ROUTES.some(route =>
    path === route || path.startsWith(`${route}/`)
  )
  const isApiRoute = API_ROUTES.some(route => path.startsWith(route))

  // Get auth token from cookies
  const token = request.cookies.get('access_token')?.value

  // Handle API routes - proxy to Brain Gateway
  if (isApiRoute) {
    const brainGatewayUrl = process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'https://api.bizoholic.com'
    const url = new URL(path, brainGatewayUrl)

    // Forward the request to Brain Gateway
    return NextResponse.rewrite(url)
  }

  // Redirect to login if accessing protected route without token
  if (!isPublicRoute && !token) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('returnUrl', path)
    return NextResponse.redirect(loginUrl)
  }

  // Allow access to public routes or authenticated users
  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files (public folder)
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\..*|manifest.json).*)',
  ],
}
EOF

    echo "✅ Created middleware.ts for $app_name"
}

# Create middleware for each frontend with appropriate public routes
create_middleware \
    "Client Portal" \
    "$BASE_DIR/client-portal" \
    "'/login', '/signup', '/forgot-password'"

create_middleware \
    "Bizoholic Frontend" \
    "$BASE_DIR/bizoholic-frontend" \
    "'/', '/about', '/services', '/contact', '/login', '/signup', '/forgot-password'"

create_middleware \
    "CoreLDove Storefront" \
    "$BASE_DIR/coreldove-storefront" \
    "'/', '/products', '/categories', '/cart', '/login', '/register'"

create_middleware \
    "BizOSaaS Admin" \
    "$BASE_DIR/bizosaas-admin" \
    "'/login', '/forgot-password'"

create_middleware \
    "Business Directory" \
    "$BASE_DIR/business-directory" \
    "'/', '/search', '/categories', '/listings', '/about', '/contact', '/login', '/register'"

create_middleware \
    "ThrillRing Gaming" \
    "$BASE_DIR/thrillring-gaming" \
    "'/', '/games', '/tournaments', '/leaderboard', '/about', '/login', '/register'"

create_middleware \
    "Analytics Dashboard" \
    "$BASE_DIR/analytics-dashboard" \
    "'/login', '/demo'"

echo ""
echo "=========================================="
echo "🚀 Creating API Service Configuration"
echo "=========================================="
echo ""

# Create a unified API service configuration file
cat > "$BASE_DIR/../../../api-service-config.ts" << 'EOF'
/**
 * Unified API Service Configuration
 * All API calls go through the Brain Gateway
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.bizoholic.com'

export const API_ENDPOINTS = {
  // Authentication
  auth: {
    login: `${API_BASE_URL}/auth/login`,
    logout: `${API_BASE_URL}/auth/logout`,
    register: `${API_BASE_URL}/auth/register`,
    refresh: `${API_BASE_URL}/auth/refresh`,
    profile: `${API_BASE_URL}/auth/profile`,
  },

  // CRM
  crm: {
    leads: `${API_BASE_URL}/crm/leads`,
    contacts: `${API_BASE_URL}/crm/contacts`,
    campaigns: `${API_BASE_URL}/crm/campaigns`,
  },

  // E-commerce
  commerce: {
    products: `${API_BASE_URL}/products`,
    orders: `${API_BASE_URL}/orders`,
    cart: `${API_BASE_URL}/cart`,
    checkout: `${API_BASE_URL}/checkout`,
  },

  // Content
  content: {
    pages: `${API_BASE_URL}/cms/pages`,
    posts: `${API_BASE_URL}/cms/posts`,
    media: `${API_BASE_URL}/cms/media`,
  },

  // Analytics
  analytics: {
    dashboard: `${API_BASE_URL}/analytics/dashboard`,
    reports: `${API_BASE_URL}/analytics/reports`,
    metrics: `${API_BASE_URL}/analytics/metrics`,
  },

  // AI Agents
  ai: {
    chat: `${API_BASE_URL}/ai/chat`,
    generate: `${API_BASE_URL}/ai/generate`,
    analyze: `${API_BASE_URL}/ai/analyze`,
    agents: `${API_BASE_URL}/ai/agents`,
  },

  // Admin
  admin: {
    users: `${API_BASE_URL}/admin/users`,
    tenants: `${API_BASE_URL}/admin/tenants`,
    services: `${API_BASE_URL}/admin/services`,
    logs: `${API_BASE_URL}/admin/logs`,
  },
}

// Request interceptor to add auth token
export const apiRequest = async (url: string, options: RequestInit = {}) => {
  const token = localStorage.getItem('access_token')

  const headers = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  }

  const response = await fetch(url, {
    ...options,
    headers,
  })

  if (response.status === 401) {
    // Token expired, try to refresh
    const refreshResponse = await fetch(API_ENDPOINTS.auth.refresh, {
      method: 'POST',
      credentials: 'include',
    })

    if (refreshResponse.ok) {
      const { access_token } = await refreshResponse.json()
      localStorage.setItem('access_token', access_token)

      // Retry original request
      return fetch(url, {
        ...options,
        headers: {
          ...headers,
          Authorization: `Bearer ${access_token}`,
        },
      })
    } else {
      // Refresh failed, redirect to login
      window.location.href = '/login'
    }
  }

  return response
}
EOF

echo "✅ Created unified API service configuration"

echo ""
echo "=========================================="
echo "📊 Summary"
echo "=========================================="
echo ""
echo "✅ Created .env.local files for all 7 frontends"
echo "✅ All frontends configured to use Brain Gateway"
echo "✅ Created authentication middleware for all frontends"
echo "✅ Created unified API service configuration"
echo ""
echo "🌐 Brain Gateway URL: $BRAIN_GATEWAY_URL"
echo "🔌 Local Development: $BRAIN_GATEWAY_URL_LOCAL"
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
echo "⚠️  Important Next Steps:"
echo "1. Ensure Brain Gateway is running on port 8001"
echo "2. Configure Brain Gateway with all service routes"
echo "3. Deploy CrewAI agents to handle AI operations"
echo "4. Test each frontend connection to Brain Gateway"
echo "5. Deploy to VPS via Dokploy"
echo ""
echo "✨ Brain Gateway Integration Setup Complete!"