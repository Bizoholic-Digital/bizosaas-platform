#!/bin/bash
# Development Environment Shutdown

echo "🛑 Stopping BizOSaaS Development Environment..."

COMPOSE_FILE=".devcontainer/docker-compose.dev.yml"

docker-compose -f $COMPOSE_FILE down

echo "✅ All services stopped."
