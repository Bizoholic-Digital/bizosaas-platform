#!/bin/bash

# Docker Images Cleanup Script for BizOSaaS Platform
echo "🧹 BizOSaaS Docker Images Cleanup..."

# Function to safely remove images
safe_remove() {
    local image=$1
    local reason=$2
    
    echo -n "🗑️ Removing $image ($reason)... "
    
    if docker rmi "$image" 2>/dev/null; then
        echo "✅ REMOVED"
    else
        echo "⚠️ SKIPPED (in use or dependencies)"
    fi
}

echo ""
echo "🔍 Analyzing current images..."

# Check what's currently running
echo "📊 Currently running containers:"
docker ps --format "table {{.Image}}\t{{.Names}}\t{{.Status}}" | grep -v "CREATED"

echo ""
echo "🗑️ REMOVING UNNECESSARY IMAGES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Remove vector database (using pgvector instead)
safe_remove "qdrant/qdrant:latest" "using pgvector in PostgreSQL"

# Remove message queue (using Dragonfly + Temporal instead)
safe_remove "rabbitmq:3.12-management-alpine" "using Dragonfly for caching, Temporal for workflows"

# Remove duplicate CMS images
safe_remove "wordpress:6.4-php8.1-apache" "using Wagtail CMS"
safe_remove "wordpress:6.4-php8.2-apache" "using Wagtail CMS"

# Remove MariaDB (using PostgreSQL)
safe_remove "mariadb:10.11" "using PostgreSQL"

# Remove Adminer (using pgAdmin)
safe_remove "adminer:4.8.1" "using pgAdmin for database management"

# Remove duplicate n8n images (keep the enhanced one)
safe_remove "n8nio/n8n:latest" "duplicate of docker.n8n.io version"

echo ""
echo "📦 KEEPING THESE IMAGES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ BizOSaaS Services:"
echo "   • bizosaas/ai-agents:latest"
echo "   • bizosaas/business-directory:latest" 
echo "   • bizosaas/client-sites-api:latest"
echo "   • bizosaas/wagtail-cms:latest"
echo "   • bizosaas/crm:latest"
echo "   • bizosaas/vault-service:latest"

echo ""
echo "✅ Infrastructure Services:"
echo "   • postgres:15-alpine & postgres:15 (database)"
echo "   • redis:7-alpine (caching)"
echo "   • hashicorp/vault:1.15 (secrets)"
echo "   • temporalio/auto-setup:1.20.0 (workflows)"
echo "   • docker.dragonflydb.io/dragonflydb/dragonfly:latest (performance cache)"
echo "   • traefik:3.0 & traefik:v3.0 (routing)"
echo "   • nginx:alpine (static content)"

echo ""
echo "✅ Integration Ready:"
echo "   • claude-mobile-bot:test (Telegram integration)"
echo "   • ghcr.io/czlonkowski/n8n-mcp:latest (Enhanced n8n)"

echo ""
echo "✅ Future Use:"
echo "   • ghcr.io/saleor/saleor:latest (E-commerce for CoreLDove)"
echo "   • ghcr.io/saleor/saleor-dashboard:latest"
echo "   • fastapicrewai-analytics:latest (Reference/backup)"
echo "   • fastapicrewai-authentication:latest (Reference/backup)"

echo ""
echo "🧹 Cleanup completed!"
echo ""
echo "💾 Disk space recovered:"
docker system df

echo ""
echo "🚀 Next Steps:"
echo "1. Run: chmod +x integrate-claude-bot.sh && ./integrate-claude-bot.sh"
echo "2. Start platform: ./start-all-services.sh"
echo "3. Deploy to Dokploy: Use docker-compose.dokploy.yml"