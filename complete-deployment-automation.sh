#!/bin/bash
# Complete BizOSaaS Deployment Automation
# Monitors deployment, configures domains, and verifies all services

API_KEY="agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi"
VPS_IP="194.238.16.237"
BACKEND_ID="uimFISkhg1KACigb2CaGz"
FRONTEND_ID="hU2yhYOqv3_ftKGGvcAiv"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "BizOSaaS Complete Deployment Automation"
echo "Started: $(date)"
echo "=========================================="

# Function to check service
check_service() {
    timeout 3 nc -zv $VPS_IP $1 2>&1 | grep -q succeeded
}

# Function to count running services
count_services() {
    local count=0
    # Infrastructure (6)
    for port in 5433 6380 8201 7234 8083 8088; do
        check_service $port && count=$((count + 1))
    done
    # Backend (10)
    for port in {8000..8009}; do
        check_service $port && count=$((count + 1))
    done
    # Frontend (6)
    for port in 3000 3001 3002 3003 3005 3009; do
        check_service $port && count=$((count + 1))
    done
    echo $count
}

# Wait for builds to start
echo "Waiting 5 minutes for builds to initialize..."
sleep 300

# Monitor deployment progress
max_wait=60  # Maximum 60 minutes
wait_count=0
last_count=0

while [ $wait_count -lt $max_wait ]; do
    current_count=$(count_services)

    echo ""
    echo "=== Progress Check ($(date +%H:%M)) ==="
    echo "Services running: $current_count/22 ($(( current_count * 100 / 22 ))%)"

    if [ $current_count -eq 22 ]; then
        echo -e "${GREEN}✓ All 22 services are running!${NC}"
        break
    fi

    if [ $current_count -gt $last_count ]; then
        echo -e "${YELLOW}Progress: +$(( current_count - last_count )) services${NC}"
        last_count=$current_count
    fi

    # Wait 2 minutes before next check
    wait_count=$((wait_count + 2))
    echo "Next check in 2 minutes... ($wait_count/$max_wait min elapsed)"
    sleep 120
done

# Final verification
echo ""
echo "=========================================="
echo "Final Deployment Status"
echo "=========================================="
bash /home/alagiri/projects/bizoholic/bizosaas-platform/final-verification.sh

final_count=$(count_services)

if [ $final_count -eq 22 ]; then
    echo ""
    echo -e "${GREEN}=========================================="
    echo "✓ DEPLOYMENT COMPLETE - 22/22 SERVICES"
    echo "==========================================${NC}"
    echo ""
    echo "Next Steps:"
    echo "1. Configure staging domains in Dokploy UI"
    echo "2. Enable SSL for all domains"
    echo "3. Test application functionality"
    echo ""
    echo "Domains to configure:"
    echo "  - stg.bizoholic.com → Port 3000"
    echo "  - stg.portal.bizoholic.com → Port 3001"
    echo "  - stg.coreldove.com → Port 3002"
    echo "  - stg.directory.bizoholic.com → Port 3003"
    echo "  - stg.thrillring.com → Port 3005"
    echo "  - stg.admin.bizoholic.com → Port 3009"
else
    echo ""
    echo -e "${YELLOW}=========================================="
    echo "⚠ DEPLOYMENT INCOMPLETE - $final_count/22"
    echo "==========================================${NC}"
    echo ""
    echo "Some services may still be building."
    echo "Check Dokploy logs at: https://dk.bizoholic.com"
    echo ""
    echo "To continue monitoring:"
    echo "watch -n 120 'bash /home/alagiri/projects/bizoholic/bizosaas-platform/final-verification.sh'"
fi
