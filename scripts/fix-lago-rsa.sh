#!/bin/bash
# Quick fix script for Lago RSA key issue on KVM8

echo "🔧 Fixing Lago RSA key issue on KVM8..."

# Find the docker-compose file
COMPOSE_FILE=$(docker inspect lago-api --format='{{index .Config.Labels "com.docker.compose.project.config_files"}}' 2>/dev/null)

if [ -z "$COMPOSE_FILE" ]; then
    echo "❌ Could not find docker-compose file location"
    exit 1
fi

echo "📁 Found compose file: $COMPOSE_FILE"

# Create backup
cp "$COMPOSE_FILE" "${COMPOSE_FILE}.backup"

# Remove LAGO_RSA_PRIVATE_KEY lines from the compose file
sed -i '/LAGO_RSA_PRIVATE_KEY/d' "$COMPOSE_FILE"

echo "✅ Removed LAGO_RSA_PRIVATE_KEY from compose file"

# Get the project directory
PROJECT_DIR=$(dirname "$COMPOSE_FILE")
cd "$PROJECT_DIR"

# Restart the services
echo "🔄 Restarting Lago services..."
docker-compose -f docker-compose.lago.yml restart lago-api lago-worker

echo "⏳ Waiting for services to stabilize..."
sleep 10

# Check status
docker ps --filter name=lago

echo "✅ Fix applied! Check logs with: docker logs lago-api"
