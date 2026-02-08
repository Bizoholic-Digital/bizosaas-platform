#!/bin/bash
set -e

echo "🔄 Local Development - Bizoholic"
echo "=================================="
echo ""
echo "Running in LOCAL MODE (no Docker for backends)"
echo "  ✓ Infrastructure via Docker"
echo "  ✓ Frontend via npm run dev"
echo ""

# 1. Ensure network exists
docker network create bizosaas-network 2>/dev/null || true

# 2. Start Infrastructure only
echo "📦 Starting Infrastructure..."
docker compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres redis vault

# 3. Check if frontend is already running
if lsof -Pi :3001 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port 3001 already in use. Bizoholic frontend may already be running."
    echo "   Check: http://localhost:3001"
else
    echo "🌐 Starting Bizoholic Frontend..."
    echo ""
    echo "   Run this command in a new terminal:"
    echo "   cd brands/bizoholic/frontend && PORT=3001 npm run dev"
    echo ""
fi

echo ""
echo "✅ Infrastructure Ready!"
echo ""
echo "📊 Running Services:"
echo "   Infrastructure:"
echo "     - Postgres:    localhost:5432"
echo "     - Redis:       localhost:6379"
echo "     - Vault:       localhost:8200"
echo ""
echo "   Bizoholic Frontend:"
echo "     - URL:         http://localhost:3001"
echo "     - Start with:  cd brands/bizoholic/frontend && PORT=3001 npm run dev"
echo ""
echo "💡 Backend services (Brain, Auth, CMS, CRM) need Dockerfiles."
echo "   For now, frontends will work in static mode without backend data."
echo ""
echo "🔧 To add backend services later:"
echo "   1. Restore Dockerfiles from archive"
echo "   2. Use ./scripts/start-bizoholic.sh (full Docker stack)"
