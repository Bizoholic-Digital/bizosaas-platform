#!/bin/bash
# Monitor frontend deployment on VPS

VPS_IP="194.238.16.237"
VPS_USER="root"
VPS_PASSWORD="&k3civYG5Q6YPb"

echo "📊 Monitoring Frontend Deployment"
echo "=================================="
echo ""

while true; do
    clear
    echo "📊 Frontend Services Status - $(date)"
    echo "=================================="
    echo ""

    # Check frontend containers
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP 'docker ps --filter "name=frontend" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'

    echo ""
    echo "📊 All BizOSaaS Containers Count:"
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP 'docker ps --filter "name=bizosaas" | wc -l' | xargs echo "   Running:"

    echo ""
    echo "Expected Frontend Services (5):"
    echo "   1. Client Portal (port 3000)"
    echo "   2. Bizoholic Frontend (port 3001)"
    echo "   3. CorelDove Frontend (port 3002)"
    echo "   4. Business Directory Frontend (port 3003)"
    echo "   5. Admin Dashboard (port 3005)"

    echo ""
    echo "Press Ctrl+C to stop monitoring..."
    sleep 5
done
