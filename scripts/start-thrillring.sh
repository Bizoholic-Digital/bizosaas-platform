#!/bin/bash
set -e
export DOCKER_BUILDKIT=0

echo "🚀 ThrillRing Environment Starter"
echo "=================================="
echo ""

# Ensure network exists
docker network create bizosaas-network 2>/dev/null || true

# Start Infrastructure
echo "📦 Starting Infrastructure..."
docker compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres redis

# Check if Dockerfiles exist for full Docker mode
if [ -f "shared/services/brain-gateway/Dockerfile" ]; then
    echo ""
    echo "✅ Dockerfiles found - Starting FULL DOCKER MODE"
    echo ""
    
    # Start Brain Gateway
    echo "🧠 Starting Brain Gateway..."
    docker compose -f shared/services/docker-compose.services.yml up -d brain-gateway
    
    # Start ThrillRing Frontend
    echo "🎮 Starting ThrillRing Frontend (Docker)..."
    docker compose -f brands/docker-compose.brands.yml up -d thrillring-frontend
    
    echo ""
    echo "✅ Full Docker Stack Running!"
    echo ""
    echo "📊 Services:"
    echo "   Infrastructure:"
    echo "     - Postgres:    localhost:5432"
    echo "     - Redis:       localhost:6379"
    echo ""
    echo "   Backend Services:"
    echo "     - Brain API:   localhost:8001"
    echo ""
    echo "   ThrillRing:"
    echo "     - Frontend:    http://localhost:3005"
    
else
    echo ""
    echo "⚠️  Dockerfiles not found - Starting LOCAL DEV MODE"
    echo ""
    
    # Check if frontend is already running
    if lsof -Pi :3005 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "✅ Port 3005 already in use - Frontend may be running"
        echo "   Check: http://localhost:3005"
    else
        echo "📝 To start the frontend, run in a new terminal:"
        echo "   cd brands/thrillring/frontend && PORT=3005 npm run dev"
    fi
    
    echo ""
    echo "✅ Infrastructure Running!"
    echo ""
    echo "📊 Services:"
    echo "   Infrastructure:"
    echo "     - Postgres:    localhost:5432"
    echo "     - Redis:       localhost:6379"
    echo ""
    echo "   ThrillRing Frontend:"
    echo "     - URL:         http://localhost:3005"
    echo "     - Command:     cd brands/thrillring/frontend && PORT=3005 npm run dev"
    echo ""
    echo "💡 Backend services will be added when Dockerfiles are restored"
fi

echo ""
echo "🔧 Tip: Use Ctrl+C to stop, or run: docker compose down"
