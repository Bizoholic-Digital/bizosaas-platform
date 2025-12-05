#!/bin/bash
set -e

echo "🔄 Local Development - CoreLDove"
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
docker compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres redis

# 3. Check if frontend is already running
if lsof -Pi :3002 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port 3002 already in use. CoreLDove frontend may already be running."
    echo "   Check: http://localhost:3002"
else
    echo "🌐 Starting CoreLDove Frontend..."
    echo ""
    echo "   Run this command in a new terminal:"
    echo "   cd brands/coreldove/frontend && PORT=3002 npm run dev"
    echo ""
fi

echo ""
echo "✅ Infrastructure Ready!"
echo ""
echo "📊 Running Services:"
echo "   Infrastructure:"
echo "     - Postgres:    localhost:5432"
echo "     - Redis:       localhost:6379"
echo ""
echo "   CoreLDove Frontend:"
echo "     - URL:         http://localhost:3002"
echo "     - Start with:  cd brands/coreldove/frontend && PORT=3002 npm run dev"
echo ""
echo "💡 Backend services need Dockerfiles."
echo "   For now, frontend will work in static mode."
