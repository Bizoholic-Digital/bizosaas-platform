#!/bin/bash

# Autonomous Deployment Attempt
# Tries all possible automated deployment methods

set -e

VPS_IP="194.238.16.237"
DOKPLOY_URL="https://dk.bizoholic.com"
PROJECT_DIR="/home/alagiri/projects/bizoholic/bizosaas-platform"

echo "========================================="
echo "BizOSaaS Autonomous Deployment Attempt"
echo "========================================="
echo "VPS: $VPS_IP"
echo "Dokploy: $DOKPLOY_URL"
echo "Time: $(date)"
echo ""

# Method 1: Try SSH deployment
echo "METHOD 1: Attempting SSH deployment..."
if command -v ssh >/dev/null 2>&1; then
    echo "SSH available. Testing connection..."

    if timeout 10 ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$VPS_IP "echo 'SSH_OK'" 2>/dev/null | grep -q "SSH_OK"; then
        echo "✓ SSH connection successful!"

        echo "Deploying via SSH..."

        ssh root@$VPS_IP << 'ENDSSH'
            cd /tmp
            rm -rf bizosaas-platform
            git clone https://github.com/Bizoholic-Digital/bizosaas-platform.git
            cd bizosaas-platform/bizosaas-platform

            echo "Deploying backend services..."
            docker-compose -f dokploy-backend-staging.yml up -d --build

            echo "Waiting 60 seconds for backend to stabilize..."
            sleep 60

            echo "Deploying frontend services..."
            docker-compose -f dokploy-frontend-staging.yml up -d --build

            echo "Deployment complete via SSH!"
ENDSSH

        echo "✓ SSH deployment completed successfully!"
        exit 0
    else
        echo "✗ SSH connection failed or not configured"
    fi
else
    echo "✗ SSH not available"
fi

# Method 2: Try Docker Context
echo ""
echo "METHOD 2: Attempting Docker Context deployment..."

if docker context ls 2>/dev/null | grep -q "bizosaas-vps"; then
    echo "✓ Docker context 'bizosaas-vps' exists"

    docker context use bizosaas-vps

    echo "Deploying backend services..."
    docker-compose -f "$PROJECT_DIR/dokploy-backend-staging.yml" up -d --build

    echo "Waiting 60 seconds..."
    sleep 60

    echo "Deploying frontend services..."
    docker-compose -f "$PROJECT_DIR/dokploy-frontend-staging.yml" up -d --build

    echo "✓ Docker context deployment completed!"
    exit 0
else
    echo "✗ Docker context not configured"
    echo "  To create: docker context create bizosaas-vps --docker host=ssh://root@$VPS_IP"
fi

# Method 3: Try creating Docker context and deploying
echo ""
echo "METHOD 3: Creating Docker context and deploying..."

if command -v docker >/dev/null 2>&1; then
    echo "Creating Docker context..."

    if docker context create bizosaas-vps --docker host=ssh://root@$VPS_IP 2>/dev/null; then
        echo "✓ Docker context created"

        docker context use bizosaas-vps

        echo "Deploying backend services..."
        docker-compose -f "$PROJECT_DIR/dokploy-backend-staging.yml" up -d --build

        echo "Waiting 60 seconds..."
        sleep 60

        echo "Deploying frontend services..."
        docker-compose -f "$PROJECT_DIR/dokploy-frontend-staging.yml" up -d --build

        echo "✓ Deployment completed!"
        exit 0
    else
        echo "✗ Could not create Docker context (SSH key needed)"
    fi
else
    echo "✗ Docker not available"
fi

# Method 4: Try remote Docker daemon
echo ""
echo "METHOD 4: Attempting remote Docker daemon connection..."

export DOCKER_HOST="ssh://root@$VPS_IP"

if docker info >/dev/null 2>&1; then
    echo "✓ Connected to remote Docker daemon"

    echo "Deploying backend services..."
    docker-compose -f "$PROJECT_DIR/dokploy-backend-staging.yml" up -d --build

    echo "Waiting 60 seconds..."
    sleep 60

    echo "Deploying frontend services..."
    docker-compose -f "$PROJECT_DIR/dokploy-frontend-staging.yml" up -d --build

    echo "✓ Deployment completed!"
    exit 0
else
    echo "✗ Could not connect to remote Docker daemon"
fi

# All automated methods failed
echo ""
echo "========================================="
echo "AUTOMATED DEPLOYMENT NOT POSSIBLE"
echo "========================================="
echo ""
echo "All automated methods failed. Manual deployment required."
echo ""
echo "REQUIRED ACTION:"
echo "1. Configure SSH access to root@$VPS_IP"
echo "   OR"
echo "2. Deploy via Dokploy UI at $DOKPLOY_URL"
echo ""
echo "For Dokploy UI deployment, follow:"
echo "  cat $PROJECT_DIR/DEPLOYMENT_EXECUTION_NOW.md"
echo ""

exit 1
