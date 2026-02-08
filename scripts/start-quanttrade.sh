#!/bin/bash
set -e
export DOCKER_BUILDKIT=0

echo "🚀 QuantTrade Environment Starter"
echo "=================================="
echo ""

# Ensure network exists
docker network create bizosaas-network 2>/dev/null || true

# Start Infrastructure
echo "📦 Starting Infrastructure..."
docker compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres redis

# Check if Dockerfiles exist for full Docker mode
if [ -f "brands/quanttrade/backend/Dockerfile" ]; then
    echo ""
    echo "✅ Dockerfiles found - Starting FULL DOCKER MODE"
    echo ""
    
    # Start QuantTrade Services
    echo "📈 Starting QuantTrade Frontend & Backend (Docker)..."
    docker compose -f brands/docker-compose.brands.yml up -d quanttrade-frontend quanttrade-backend
    
    echo ""
    echo "✅ Full Docker Stack Running!"
    echo ""
    echo "📊 Services:"
    echo "   Infrastructure:"
    echo "     - Postgres:    localhost:5432"
    echo "     - Redis:       localhost:6379"
    echo ""
    echo "   QuantTrade:"
    echo "     - Frontend:    http://localhost:3006"
    echo "     - Backend:     localhost:8006"
    
else
    echo ""
    echo "⚠️  Dockerfiles not found - Starting LOCAL DEV MODE"
    echo ""
    
    # Check if frontend is already running
    if lsof -Pi :3006 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "✅ Port 3006 already in use - Frontend may be running"
        echo "   Check: http://localhost:3006"
    else
        echo "📝 To start the frontend, run in a new terminal:"
        echo "   cd brands/quanttrade/frontend && PORT=3006 npm run dev"
    fi
    
    echo ""
    echo "✅ Infrastructure Running!"
    echo ""
    echo "📊 Services:"
    echo "   Infrastructure:"
    echo "     - Postgres:    localhost:5432"
    echo "     - Redis:       localhost:6379"
    echo ""
    echo "   QuantTrade Frontend:"
    echo "     - URL:         http://localhost:3006"
    echo "     - Command:     cd brands/quanttrade/frontend && PORT=3006 npm run dev"
    echo ""
    echo "💡 Backend services will be added when Dockerfiles are restored"
fi

echo ""
echo "🔧 Tip: Use Ctrl+C to stop, or run: docker compose down"
