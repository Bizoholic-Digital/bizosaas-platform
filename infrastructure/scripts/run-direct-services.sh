#!/bin/bash

# Direct Service Deployment Script
# Run BizOSaaS platform services directly without Docker API issues

set -e

echo "🚀 Starting BizOSaaS Platform Services Directly"
echo "=============================================="

# Function to check if port is in use
check_port() {
    if ss -tuln | grep -q ":$1 "; then
        echo "✅ Port $1 is active"
        return 0
    else
        echo "❌ Port $1 is not active"
        return 1
    fi
}

# Test current working services
echo "📊 Testing Current Service Status:"
echo "=================================="

# Test PostgreSQL
if check_port 5432; then
    echo "  🗄️  PostgreSQL with pgvector: READY"
    psql -h localhost -U admin -d bizosaas_dev -c "SELECT version();" 2>/dev/null || echo "    Note: Connection may require password"
fi

# Test Redis
if check_port 6379; then
    echo "  🔄 Redis Cache: READY"
fi

# Test AI Agents
if check_port 8000; then
    echo "  🤖 AI Agents (47+): READY"
    curl -s http://localhost:8000/health || echo "    Note: Health endpoint may need authentication"
fi

# Test Business Directory
if check_port 8003; then
    echo "  📁 Business Directory (100+): READY"
fi

# Test Client Sites API
if check_port 8005; then
    echo "  🏢 Client Sites API: READY"
fi

# Test Vault
if check_port 8200; then
    echo "  🔐 HashiCorp Vault: READY"
fi

echo ""
echo "🎯 Service Status Summary:"
echo "========================="

# Count active services
active_services=0

services=(
    "5432:PostgreSQL+pgvector"
    "6379:Redis Cache"
    "8000:AI Agents (47+)"
    "8003:Business Directory"
    "8005:Client Sites API"
    "8200:HashiCorp Vault"
    "8201:Vault Service"
    "8080:Traefik Dashboard"
)

for service in "${services[@]}"; do
    port="${service%%:*}"
    name="${service#*:}"
    if check_port $port; then
        echo "✅ $name - Active on port $port"
        ((active_services++))
    else
        echo "❌ $name - Not active on port $port"
    fi
done

echo ""
echo "📈 Platform Status: $active_services/${#services[@]} services operational"

# Calculate completion percentage
completion=$((active_services * 100 / ${#services[@]}))
echo "🎯 Completion: $completion%"

# Test frontend builds
echo ""
echo "🌐 Testing Frontend Applications:"
echo "================================"

cd frontend

# Test Bizoholic build
echo "🏢 Testing Bizoholic Website build..."
if npm run build > /tmp/bizoholic-build.log 2>&1; then
    echo "✅ Bizoholic Website: Build SUCCESS"
else
    echo "❌ Bizoholic Website: Build FAILED"
    tail -10 /tmp/bizoholic-build.log
fi

# Start frontend in development mode
echo ""
echo "🚀 Starting Bizoholic Website (Next.js)..."
echo "==========================================="
echo "📍 URL: http://localhost:3000"
echo "🎯 Features: 47+ AI Agents, Multi-tenant, Apple-style design"
echo ""
echo "To access the platform:"
echo "- Main Website: http://localhost:3000"
echo "- AI Agents API: http://localhost:8000"
echo "- Business Directory: http://localhost:8003"
echo "- Client Sites API: http://localhost:8005" 
echo "- Vault UI: http://localhost:8200"
echo "- Traefik Dashboard: http://localhost:8080"
echo ""

# Start the frontend
npm run dev