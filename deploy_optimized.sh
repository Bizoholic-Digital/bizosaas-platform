#!/bin/bash
set -e

# Define Dokploy Project Paths
PATH_INFRA="/etc/dokploy/compose/bizosaasinfra-infrastructure-ma0eo8/code"
PATH_LAGO="/etc/dokploy/compose/bizosaasbilling-lagos-4ur4py/code"
PATH_PLANE="/etc/dokploy/compose/bizosaasinfra-bizosaasplane-s8bv6u/code"
PATH_AUTH="/etc/dokploy/compose/bizosaasauthentik-authentik-bwgc5f/code"
PATH_CORE="/etc/dokploy/compose/bizosaascore-coreservices-cux333/code"

# Detect Docker Compose
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ Docker Compose not found"
    exit 1
fi

echo "🚀 Deploying with Resource Limits & Correct Environment Variables..."

deploy_stack() {
    local PATH_DIR="$1"
    local FILE="$2"
    local NAME="$3"

    if [ -d "$PATH_DIR" ]; then
        cd "$PATH_DIR"
        # Extract folder-based project name
        PARENT=$(dirname "$PATH_DIR")
        PROJECT_ID=$(basename "$PARENT")
        
        echo "=================================================="
        echo "📦 Deploying Stack: $NAME (Project: $PROJECT_ID)"
        echo "=================================================="
        
        cp "/root/$FILE" "$PATH_DIR/"
        
        # Deploy with explicit project name to prevent orphan conflicts
        $COMPOSE_CMD -p "$PROJECT_ID" -f "$FILE" up -d
    else
        echo "⚠️  Path not found for $NAME: $PATH_DIR"
    fi
}

# 1. Update & Deploy Infrastructure
deploy_stack "$PATH_INFRA" "dokploy-infrastructure-staging.yml" "Infrastructure"

# 2. Update & Deploy Lago
deploy_stack "$PATH_LAGO" "dokploy-lago-staging.yml" "Lago"

# 3. Update & Deploy Plane
deploy_stack "$PATH_PLANE" "dokploy-plane-staging.yml" "Plane"

# 4. Update & Deploy Authentik
deploy_stack "$PATH_AUTH" "dokploy-authentik-staging.yml" "Authentik"

# 5. Update & Deploy Core Services
# 5. Update & Deploy Core Services
deploy_stack "$PATH_CORE" "dokploy-backend-staging.yml" "Core Services"

# 6. Update & Deploy Client Portal
PATH_CLIENT="/etc/dokploy/compose/bizosaasfrontend-clientportal-r1a5il/code"
deploy_stack "$PATH_CLIENT" "dokploy-client-portal-staging.yml" "Client Portal"

# 7. Update & Deploy Admin Dashboard
PATH_ADMIN="/etc/dokploy/compose/bizosaasadmin-bizosaasadmindashboard-oeomlg/code"
deploy_stack "$PATH_ADMIN" "dokploy-admin-dashboard-staging.yml" "Admin Dashboard"


# 6. Check Health
echo "🏥 Checking Health..."
sleep 20
docker ps --filter "health=unhealthy" --format "table {{.Names}}\t{{.Status}}"
echo "✅ Deployment Sequence Complete!"

# 6. Check Health
echo "🏥 Checking Health..."
sleep 20
docker ps --filter "health=unhealthy" --format "table {{.Names}}\t{{.Status}}"
echo "✅ Deployment Sequence Complete!"
