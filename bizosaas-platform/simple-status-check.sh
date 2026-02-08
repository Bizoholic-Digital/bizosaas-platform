#!/bin/bash

# Simple Status Check - BizOSaaS Platform
# Quick check of all 22 services

VPS_IP="194.238.16.237"

echo "==================================="
echo "BizOSaaS Platform Status Check"
echo "==================================="
echo "VPS: $VPS_IP"
echo "Time: $(date)"
echo ""

total=0
running=0

echo "INFRASTRUCTURE SERVICES:"
for port in 5433:PostgreSQL 6380:Redis 8201:Vault 7234:Temporal-Server 8083:Temporal-UI 8088:Superset; do
    IFS=':' read -r p name <<< "$port"
    total=$((total + 1))
    if nc -z -w2 $VPS_IP $p 2>/dev/null; then
        echo "  ✓ $name (port $p)"
        running=$((running + 1))
    else
        echo "  ✗ $name (port $p)"
    fi
done

echo ""
echo "BACKEND SERVICES:"
for port in 8000:Saleor 8001:Brain-API 8002:Wagtail 8003:Django-CRM 8004:Business-Dir 8005:CorelDove 8006:Auth 8007:Temporal-Int 8008:AI-Agents 8009:Amazon; do
    IFS=':' read -r p name <<< "$port"
    total=$((total + 1))
    if curl -f -s -o /dev/null --connect-timeout 2 "http://$VPS_IP:$p/health" 2>/dev/null || \
       curl -f -s -o /dev/null --connect-timeout 2 "http://$VPS_IP:$p/health/" 2>/dev/null || \
       curl -f -s -o /dev/null --connect-timeout 2 "http://$VPS_IP:$p/admin/login/" 2>/dev/null; then
        echo "  ✓ $name (port $p)"
        running=$((running + 1))
    else
        echo "  ✗ $name (port $p)"
    fi
done

echo ""
echo "FRONTEND SERVICES:"
for port in 3000:Bizoholic 3001:Client-Portal 3002:CorelDove 3003:Directory 3005:ThrillRing 3009:Admin; do
    IFS=':' read -r p name <<< "$port"
    total=$((total + 1))
    if curl -f -s -o /dev/null --connect-timeout 2 "http://$VPS_IP:$p/api/health" 2>/dev/null || \
       curl -f -s -o /dev/null --connect-timeout 2 "http://$VPS_IP:$p/" 2>/dev/null; then
        echo "  ✓ $name (port $p)"
        running=$((running + 1))
    else
        echo "  ✗ $name (port $p)"
    fi
done

echo ""
echo "==================================="
echo "SUMMARY: $running/$total services running"
percentage=$((running * 100 / total))
echo "Status: $percentage%"
echo "==================================="

if [ $running -eq 22 ]; then
    echo "✓ ALL SERVICES HEALTHY!"
    exit 0
elif [ $running -ge 15 ]; then
    echo "⚠ Most services running"
    exit 0
else
    echo "✗ More services needed"
    exit 1
fi
