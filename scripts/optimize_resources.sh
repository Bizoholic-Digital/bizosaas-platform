#!/bin/bash
# Resource Optimization Script for KVM4
# Adds CPU/Memory limits and restarts all services

set -e

echo "=== BizOSaaS Platform Resource Optimization ==="
echo "Server: KVM4 (72.60.219.244)"
echo "CPUs: 4 cores, RAM: 16GB"
echo ""

# Function to update service with resource limits
update_service_limits() {
    local service=$1
    local cpu_limit=$2
    local mem_limit=$3
    local cpu_reserve=$4
    local mem_reserve=$5
    
    echo "Updating $service with limits: CPU=$cpu_limit, MEM=$mem_limit"
    docker service update \
        --limit-cpu="$cpu_limit" \
        --limit-memory="$mem_limit" \
        --reserve-cpu="$cpu_reserve" \
        --reserve-memory="$mem_reserve" \
        "$service" 2>/dev/null || echo "  ⚠️  Service $service not found or already configured"
}

echo "Step 1: Adding resource limits to HIGH CPU services..."
echo "---"

# Temporal Server - Currently using 182% CPU!
update_service_limits "infrastructure-temporal-server" "1.0" "512M" "0.25" "256M"

# Saleor API - Currently using 92% CPU
update_service_limits "backend-saleor-api" "1.0" "1G" "0.5" "512M"

# Wagtail CMS - Currently using 41% CPU
update_service_limits "backend-wagtail-cms" "0.75" "512M" "0.25" "256M"

# Shared PostgreSQL - Using 33% CPU
update_service_limits "infrastructure-shared-postgres" "0.5" "1G" "0.25" "512M"

# Redis instances - Using 33-35% CPU each
update_service_limits "infrastructure-shared-redis" "0.25" "256M" "0.1" "128M"
update_service_limits "infrastructureservices-saleorredis-nzd5pv" "0.25" "256M" "0.1" "128M"

echo ""
echo "Step 2: Adding resource limits to MEDIUM usage services..."
echo "---"

# Backend services
update_service_limits "backend-brain-gateway" "0.5" "1G" "0.25" "512M"
update_service_limits "backend-django-crm" "0.5" "512M" "0.25" "256M"
update_service_limits "backend-ai-agents" "0.5" "512M" "0.25" "256M"

# Frontend services
update_service_limits "frontend-admin-dashboard" "0.25" "256M" "0.1" "128M"
update_service_limits "frontend-client-portal" "0.25" "256M" "0.1" "128M"
update_service_limits "frontend-business-directory" "0.25" "256M" "0.1" "128M"
update_service_limits "frontendservices-saleordashboard-84ku62" "0.25" "256M" "0.1" "128M"

# Infrastructure
update_service_limits "infrastructure-vault" "0.25" "256M" "0.1" "128M"
update_service_limits "infrastructure-temporal-ui" "0.25" "256M" "0.1" "128M"
update_service_limits "dokploy" "0.5" "512M" "0.25" "256M"
update_service_limits "dokploy-postgres" "0.25" "256M" "0.1" "128M"
update_service_limits "dokploy-redis" "0.25" "256M" "0.1" "128M"

echo ""
echo "Step 3: Restarting ESSENTIAL services with resource limits..."
echo "---"

# Agent Workers - Essential for automation
echo "Restarting Agent Workers..."
docker service update \
    --limit-cpu="0.5" \
    --limit-memory="512M" \
    --reserve-cpu="0.25" \
    --reserve-memory="256M" \
    infrastructureservices-agentworkersmarketing-jltibj 2>/dev/null || true

docker service scale infrastructureservices-agentworkersmarketing-jltibj=1

docker service update \
    --limit-cpu="0.5" \
    --limit-memory="512M" \
    --reserve-cpu="0.25" \
    --reserve-memory="256M" \
    infrastructureservices-agentworkersorder-yeyxjf 2>/dev/null || true

docker service scale infrastructureservices-agentworkersorder-yeyxjf=1

docker service update \
    --limit-cpu="0.5" \
    --limit-memory="512M" \
    --reserve-cpu="0.25" \
    --reserve-memory="256M" \
    infrastructureservices-agentworkerssupport-7oyikb 2>/dev/null || true

docker service scale infrastructureservices-agentworkerssupport-7oyikb=1

# Auth Service - Essential for security
echo "Restarting Auth Service..."
docker service update \
    --limit-cpu="0.25" \
    --limit-memory="256M" \
    --reserve-cpu="0.1" \
    --reserve-memory="128M" \
    backendservices-authservice-ux07ss 2>/dev/null || true

docker service scale backendservices-authservice-ux07ss=1

# Amazon Sourcing - If needed
echo "Restarting Amazon Sourcing..."
docker service update \
    --limit-cpu="0.25" \
    --limit-memory="256M" \
    --reserve-cpu="0.1" \
    --reserve-memory="128M" \
    backend-amazon-sourcing 2>/dev/null || true

docker service scale backend-amazon-sourcing=1

echo ""
echo "Step 4: Restarting DEVELOPMENT services with resource limits (optional)..."
echo "---"

# Business Directory Backend
echo "Restarting Business Directory Backend..."
docker service update \
    --limit-cpu="0.25" \
    --limit-memory="256M" \
    --reserve-cpu="0.1" \
    --reserve-memory="128M" \
    backend-business-directory 2>/dev/null || true

docker service scale backend-business-directory=1

# CoreLdove Backend
echo "Restarting CoreLdove Backend..."
docker service update \
    --limit-cpu="0.25" \
    --limit-memory="256M" \
    --reserve-cpu="0.1" \
    --reserve-memory="128M" \
    backend-coreldove-backend 2>/dev/null || true

docker service scale backend-coreldove-backend=1

# GDPR Compliance
echo "Restarting GDPR Compliance Service..."
docker service update \
    --limit-cpu="0.25" \
    --limit-memory="256M" \
    --reserve-cpu="0.1" \
    --reserve-memory="128M" \
    backendservices-backendgdprcompliance-a4tbe2 2>/dev/null || true

docker service scale backendservices-backendgdprcompliance-a4tbe2=1

# Frontend services (if needed for development)
# Uncomment these if you need them:

# echo "Restarting ThrillRing Gaming..."
# docker service update \
#     --limit-cpu="0.25" \
#     --limit-memory="256M" \
#     --reserve-cpu="0.1" \
#     --reserve-memory="128M" \
#     frontend-thrillring-gaming 2>/dev/null || true
# docker service scale frontend-thrillring-gaming=1

# echo "Restarting CoreLdove Frontend..."
# docker service update \
#     --limit-cpu="0.25" \
#     --limit-memory="256M" \
#     --reserve-cpu="0.1" \
#     --reserve-memory="128M" \
#     frontend-coreldove-frontend 2>/dev/null || true
# docker service scale frontend-coreldove-frontend=1

# echo "Restarting Bizoholic Frontend..."
# docker service update \
#     --limit-cpu="0.25" \
#     --limit-memory="256M" \
#     --reserve-cpu="0.1" \
#     --reserve-memory="128M" \
#     frontend-bizoholic-frontend 2>/dev/null || true
# docker service scale frontend-bizoholic-frontend=1

echo ""
echo "=== Optimization Complete ==="
echo ""
echo "Waiting 30 seconds for services to stabilize..."
sleep 30

echo ""
echo "Current System Status:"
uptime
echo ""
docker ps --format 'table {{.Names}}\t{{.Status}}' | head -30
echo ""
echo "Total containers running:"
docker ps | wc -l

echo ""
echo "✅ Resource optimization complete!"
echo ""
echo "Next steps:"
echo "1. Monitor load: watch -n 60 'uptime'"
echo "2. Check container stats: docker stats --no-stream"
echo "3. If load is still high, uncomment frontend services in this script"
echo ""
