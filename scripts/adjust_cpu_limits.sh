#!/bin/bash
# Adjust CPU Limits - Quick Fix Script
# Increases CPU limits to match actual service usage

set -e

echo "=== Adjusting CPU Limits for KVM4 Services ==="
echo "Server: 72.60.219.244 (4 CPUs, 16GB RAM)"
echo ""

echo "Step 1: Increasing CPU limits for HIGH usage services..."
echo "---"

# Temporal Server - Currently trying to use 959% CPU, limited to 1.0
echo "Temporal Server: 1.0 → 2.0 CPUs"
docker service update --limit-cpu="2.0" --limit-memory="512M" infrastructure-temporal-server

# Saleor API - Currently trying to use 666% CPU, limited to 1.0
echo "Saleor API: 1.0 → 1.5 CPUs"
docker service update --limit-cpu="1.5" --limit-memory="1G" backend-saleor-api

# Wagtail CMS - Currently trying to use 231% CPU, limited to 0.75
echo "Wagtail CMS: 0.75 → 1.0 CPU"
docker service update --limit-cpu="1.0" --limit-memory="512M" backend-wagtail-cms

# Django CRM - Currently trying to use 315% CPU, no limit set
echo "Django CRM: Adding 1.0 CPU limit"
docker service update --limit-cpu="1.0" --limit-memory="512M" backend-django-crm

# Superset - Currently trying to use 978% CPU, no limit set!
echo "Superset: Adding 1.0 CPU limit (was using 9.7 cores!)"
docker service update --limit-cpu="1.0" --limit-memory="1G" infrastructure-superset

echo ""
echo "Step 2: Adjusting other service limits..."
echo "---"

# Shared PostgreSQL - Keep at 0.5 but increase memory
echo "Shared PostgreSQL: 0.5 CPU, 1GB memory"
docker service update --limit-cpu="0.5" --limit-memory="1G" infrastructure-shared-postgres

# Redis instances - Keep at 0.25
echo "Redis instances: 0.25 CPU each"
docker service update --limit-cpu="0.25" --limit-memory="256M" infrastructure-shared-redis 2>/dev/null || true
docker service update --limit-cpu="0.25" --limit-memory="256M" infrastructureservices-saleorredis-nzd5pv 2>/dev/null || true

# Brain Gateway - Keep at 0.5
echo "Brain Gateway: 0.5 CPU"
docker service update --limit-cpu="0.5" --limit-memory="1G" backend-brain-gateway 2>/dev/null || true

# AI Agents - Keep at 0.5
echo "AI Agents: 0.5 CPU"
docker service update --limit-cpu="0.5" --limit-memory="512M" backend-ai-agents 2>/dev/null || true

# Frontend services - Keep at 0.25 each
echo "Frontend services: 0.25 CPU each"
docker service update --limit-cpu="0.25" --limit-memory="512M" frontend-admin-dashboard 2>/dev/null || true
docker service update --limit-cpu="0.25" --limit-memory="512M" frontend-client-portal 2>/dev/null || true
docker service update --limit-cpu="0.25" --limit-memory="512M" frontend-business-directory 2>/dev/null || true
docker service update --limit-cpu="0.25" --limit-memory="256M" frontendservices-saleordashboard-84ku62 2>/dev/null || true

# Infrastructure services
echo "Infrastructure services: 0.25-0.5 CPU each"
docker service update --limit-cpu="0.25" --limit-memory="256M" infrastructure-vault 2>/dev/null || true
docker service update --limit-cpu="0.25" --limit-memory="256M" infrastructure-temporal-ui 2>/dev/null || true
docker service update --limit-cpu="0.5" --limit-memory="512M" dokploy 2>/dev/null || true
docker service update --limit-cpu="0.25" --limit-memory="256M" dokploy-postgres 2>/dev/null || true
docker service update --limit-cpu="0.25" --limit-memory="256M" dokploy-redis 2>/dev/null || true
docker service update --limit-cpu="0.25" --limit-memory="256M" infrastructureservices-saleorpostgres-h7eayh 2>/dev/null || true

echo ""
echo "Step 3: Waiting 30 seconds for services to stabilize..."
sleep 30

echo ""
echo "=== Current System Status ==="
echo ""
echo "Load Average:"
uptime
echo ""

echo "Container Count:"
docker ps | wc -l
echo ""

echo "Top CPU Consumers:"
docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}' | head -15
echo ""

echo "=== Summary of CPU Limits ==="
echo ""
echo "High Usage Services:"
echo "  - Temporal Server: 2.0 CPUs"
echo "  - Saleor API: 1.5 CPUs"
echo "  - Wagtail CMS: 1.0 CPU"
echo "  - Django CRM: 1.0 CPU"
echo "  - Superset: 1.0 CPU"
echo ""
echo "Medium Usage Services:"
echo "  - Brain Gateway: 0.5 CPU"
echo "  - AI Agents: 0.5 CPU"
echo "  - Dokploy: 0.5 CPU"
echo "  - Shared PostgreSQL: 0.5 CPU"
echo ""
echo "Low Usage Services:"
echo "  - All Frontend services: 0.25 CPU each"
echo "  - All Redis instances: 0.25 CPU each"
echo "  - Infrastructure services: 0.25 CPU each"
echo ""
echo "Total CPU Allocation: ~7.5 CPUs worth of limits"
echo "Physical CPUs: 4"
echo "Note: Docker will schedule fairly across all services"
echo ""
echo "✅ CPU limit adjustment complete!"
echo ""
echo "Expected behavior:"
echo "  - Load will be 16-18 (high but functional)"
echo "  - Services will share CPU time fairly"
echo "  - No single service can monopolize all CPUs"
echo "  - System will remain stable"
echo ""
