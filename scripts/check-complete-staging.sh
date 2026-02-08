#!/bin/bash

# BizOSaaS Complete Staging Health Check
# Checks all 21 containers across Infrastructure, Backend, and Frontend

VPS_IP="194.238.16.237"
VPS_PASS="&k3civYG5Q6YPb"

echo "========================================"
echo "   BizOSaaS Staging Health Check"
echo "========================================"
echo ""
echo "Deployment Target: $VPS_IP"
echo "Checking: $(date)"
echo ""

# Function to count running containers
count_containers() {
    local filter=$1
    sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no root@$VPS_IP \
        "docker ps $filter --format '{{.Names}}' | wc -l"
}

# Function to show container status
show_status() {
    local title=$1
    local filter=$2
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  $title"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no root@$VPS_IP \
        "docker ps $filter --format 'table {{.Names}}\t{{.Status}}' | head -20"
    echo ""
}

# Infrastructure Services (6 expected)
echo "📊 INFRASTRUCTURE SERVICES"
show_status "PostgreSQL, Redis, Vault, Temporal, Superset" \
    "--filter 'name=bizosaas-postgres-staging' --filter 'name=bizosaas-redis-staging' --filter 'name=bizosaas-vault-staging' --filter 'name=bizosaas-temporal' --filter 'name=bizosaas-superset-staging'"

INFRA_COUNT=$(count_containers "--filter 'name=bizosaas-postgres-staging' --filter 'name=bizosaas-redis-staging' --filter 'name=bizosaas-vault-staging' --filter 'name=bizosaas-temporal' --filter 'name=bizosaas-superset-staging'")

# Backend Services (9 expected)
echo "🔧 BACKEND SERVICES"
show_status "APIs on ports 8000-8009" \
    "--filter 'name=bizosaas-saleor-staging' --filter 'name=bizosaas-brain-staging' --filter 'name=bizosaas-wagtail-staging' --filter 'name=bizosaas-django-crm-staging' --filter 'name=bizosaas-business-directory-staging' --filter 'name=bizosaas-coreldove-backend-staging' --filter 'name=bizosaas-temporal-integration-staging' --filter 'name=bizosaas-ai-agents-staging' --filter 'name=bizosaas-amazon-sourcing-staging'"

BACKEND_COUNT=$(count_containers "--filter 'name=bizosaas-saleor-staging' --filter 'name=bizosaas-brain-staging' --filter 'name=bizosaas-wagtail-staging' --filter 'name=bizosaas-django-crm-staging' --filter 'name=bizosaas-business-directory-staging' --filter 'name=bizosaas-coreldove-backend-staging' --filter 'name=bizosaas-temporal-integration-staging' --filter 'name=bizosaas-ai-agents-staging' --filter 'name=bizosaas-amazon-sourcing-staging'")

# Frontend Services (6 expected)
echo "🎨 FRONTEND SERVICES"
show_status "Web apps on ports 3000-3009" \
    "--filter 'name=bizosaas-bizoholic-frontend-staging' --filter 'name=bizosaas-client-portal-staging' --filter 'name=bizosaas-coreldove-frontend-staging' --filter 'name=bizosaas-business-directory-frontend-staging' --filter 'name=bizosaas-thrillring-gaming-staging' --filter 'name=bizosaas-admin-dashboard-staging'"

FRONTEND_COUNT=$(count_containers "--filter 'name=bizosaas-bizoholic-frontend-staging' --filter 'name=bizosaas-client-portal-staging' --filter 'name=bizosaas-coreldove-frontend-staging' --filter 'name=bizosaas-business-directory-frontend-staging' --filter 'name=bizosaas-thrillring-gaming-staging' --filter 'name=bizosaas-admin-dashboard-staging'")

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📈 DEPLOYMENT SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Infrastructure:  $INFRA_COUNT/6   $([ $INFRA_COUNT -eq 6 ] && echo '✅' || echo '⚠️')"
echo "Backend:         $BACKEND_COUNT/9   $([ $BACKEND_COUNT -eq 9 ] && echo '✅' || echo '⚠️')"
echo "Frontend:        $FRONTEND_COUNT/6   $([ $FRONTEND_COUNT -eq 6 ] && echo '✅' || echo '⚠️')"
echo ""

TOTAL=$((INFRA_COUNT + BACKEND_COUNT + FRONTEND_COUNT))
PERCENTAGE=$((TOTAL * 100 / 21))

echo "Total:           $TOTAL/21  ($PERCENTAGE%)"
echo ""

if [ $TOTAL -eq 21 ]; then
    echo "🎉 SUCCESS! All 21 containers deployed and running!"
elif [ $TOTAL -ge 15 ]; then
    echo "🟡 PARTIAL: Most services running, check failed containers above"
elif [ $TOTAL -ge 6 ]; then
    echo "🟠 IN PROGRESS: Continue with deployment phases"
else
    echo "🔴 STARTING: Begin with infrastructure deployment"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Service URLs Quick Reference
if [ $TOTAL -gt 0 ]; then
    echo "🔗 Quick Access URLs:"
    echo ""

    if [ $INFRA_COUNT -gt 0 ]; then
        echo "Infrastructure:"
        echo "  • Superset:     http://$VPS_IP:8088 (admin / Bizoholic2024Admin)"
        echo "  • Temporal UI:  http://$VPS_IP:8083"
        echo "  • Vault:        http://$VPS_IP:8201"
        echo ""
    fi

    if [ $BACKEND_COUNT -gt 0 ]; then
        echo "Backend APIs:"
        echo "  • Brain API:    http://$VPS_IP:8001/health"
        echo "  • Saleor:       http://$VPS_IP:8000/health/"
        echo "  • Wagtail:      http://$VPS_IP:8002/admin/"
        echo "  • Django CRM:   http://$VPS_IP:8003/admin/"
        echo ""
    fi

    if [ $FRONTEND_COUNT -gt 0 ]; then
        echo "Frontend Apps:"
        echo "  • Bizoholic:    http://$VPS_IP:3000"
        echo "  • Portal:       http://$VPS_IP:3001"
        echo "  • CorelDove:    http://$VPS_IP:3002"
        echo "  • Admin:        http://$VPS_IP:3009"
        echo ""
    fi
fi

echo "========================================"
echo "  Checked at: $(date)"
echo "========================================"
