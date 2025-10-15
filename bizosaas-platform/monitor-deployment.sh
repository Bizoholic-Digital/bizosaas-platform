#!/bin/bash
# Real-time deployment monitoring script

API_KEY="agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi"
BACKEND_ID="uimFISkhg1KACigb2CaGz"
FRONTEND_ID="hU2yhYOqv3_ftKGGvcAiv"
VPS_IP="194.238.16.237"

echo "=========================================="
echo "BizOSaaS Deployment Monitor"
echo "Started: $(date)"
echo "=========================================="

# Function to check service port
check_port() {
    local name=$1
    local port=$2
    timeout 3 nc -zv $VPS_IP $port 2>&1 | grep -q succeeded && echo "✓ $name ($port)" || echo "✗ $name ($port)"
}

echo ""
echo "Backend Services (Ports 8000-8009):"
for port in {8000..8009}; do
    check_port "Service" $port
done

echo ""
echo "Frontend Services (Ports 3000-3009):"
for port in 3000 3001 3002 3003 3005 3009; do
    check_port "Service" $port
done

echo ""
echo "=========================================="
echo "To monitor continuously, run:"
echo "watch -n 30 'bash monitor-deployment.sh'"
echo "=========================================="
