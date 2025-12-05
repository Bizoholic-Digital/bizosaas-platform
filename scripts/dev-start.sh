#!/bin/bash
# Unified Development Startup Script
# Usage: ./scripts/dev-start.sh [profile]

PROFILE=${1:-minimal}

echo "🚀 Starting BizOSaaS Development Environment"
echo "   Profile: $PROFILE"
echo "============================================"

# Check for Portainer
if ! docker ps | grep -q portainer; then
    echo "💡 Tip: Run ./scripts/setup-portainer.sh for a lightweight GUI"
fi

# Set compose file
COMPOSE_FILE=".devcontainer/docker-compose.dev.yml"

echo "📦 Starting services..."

case $PROFILE in
    "minimal")
        # Just infrastructure
        docker-compose -f $COMPOSE_FILE up -d postgres redis vault
        ;;
    "backend")
        # Infra + Backend Services
        docker-compose -f $COMPOSE_FILE --profile backend up -d
        ;;
    "frontend")
        # Infra + Frontend (for backend API access)
        docker-compose -f $COMPOSE_FILE --profile frontend up -d
        ;;
    "full")
        # Everything (Warning for 16GB RAM)
        echo "⚠️  WARNING: Starting full stack. Monitor RAM usage!"
        docker-compose -f $COMPOSE_FILE --profile full up -d
        ;;
    *)
        echo "❌ Unknown profile: $PROFILE"
        echo "   Available: minimal, backend, frontend, full"
        exit 1
        ;;
esac

echo ""
echo "✅ Services started!"
echo "📊 Status:"
docker-compose -f $COMPOSE_FILE ps

echo ""
echo "📝 Logs:"
echo "   docker-compose -f $COMPOSE_FILE logs -f"
