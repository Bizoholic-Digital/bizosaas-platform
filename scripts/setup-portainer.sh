#!/bin/bash
# Setup Portainer - Lightweight Docker Management UI
# Saves ~500MB RAM compared to Docker Desktop

set -e

echo "🚀 Setting up Portainer..."

# Check if already running
if docker ps | grep -q portainer; then
    echo "✅ Portainer is already running at http://localhost:9000"
    exit 0
fi

# Create volume
docker volume create portainer_data

# Remove existing container if it exists
docker rm -f portainer 2>/dev/null || true

# Deploy Portainer
docker run -d -p 9001:9000 -p 9443:9443 --name portainer --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v portainer_data:/data \
    portainer/portainer-ce:latest

echo ""
echo "✅ Portainer started successfully!"
echo "👉 Access at: http://localhost:9001"
echo "🔑 Set your admin password on first login."
