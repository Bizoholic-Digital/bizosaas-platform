#!/bin/bash
# Automated monitoring and deployment completion script

API_KEY="agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi"
VPS_IP="194.238.16.237"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to count running services
count_services() {
    local count=0
    # Infrastructure
    for port in 5433 6380 8201 7234 8083 8088; do
        timeout 3 nc -zv $VPS_IP $port 2>&1 | grep -q succeeded && count=$((count + 1))
    done
    # Backend
    for port in {8000..8009}; do
        timeout 3 nc -zv $VPS_IP $port 2>&1 | grep -q succeeded && count=$((count + 1))
    done
    # Frontend - NEW PORTS
    for port in 3000 3001 3002 3003 3004 3005; do
        timeout 3 nc -zv $VPS_IP $port 2>&1 | grep -q succeeded && count=$((count + 1))
    done
    echo $count
}

echo "=========================================="
echo "BizOSaaS Automated Deployment Monitor"
echo "Started: $(date)"
echo "=========================================="

# Monitor loop
max_iterations=30  # 30 iterations x 2 min = 60 minutes max
iteration=0
last_count=0

while [ $iteration -lt $max_iterations ]; do
    current_count=$(count_services)
    percentage=$((current_count * 100 / 22))

    echo ""
    echo -e "${BLUE}=== Check #$((iteration + 1)) ($(date +%H:%M)) ===${NC}"
    echo -e "Services: ${YELLOW}$current_count/22${NC} (${percentage}%)"

    if [ $current_count -eq 22 ]; then
        echo -e "${GREEN}"
        echo "=========================================="
        echo "✓ ALL 22 SERVICES RUNNING!"
        echo "=========================================="
        echo -e "${NC}"

        # Run final verification
        bash /home/alagiri/projects/bizoholic/bizosaas-platform/final-verification.sh

        echo ""
        echo -e "${GREEN}Next Steps: Domain Configuration${NC}"
        echo "Configure these domains in Dokploy:"
        echo "1. stg.bizoholic.com → Port 3000 (Client Portal)"
        echo "2. stg.marketing.bizoholic.com → Port 3001 (Bizoholic)"
        echo "3. stg.admin.bizoholic.com → Port 3005 (Admin)"
        echo "4. stg.coreldove.com → Port 3002 (E-commerce)"
        echo "5. stg.directory.bizoholic.com → Port 3003 (Directory)"
        echo "6. stg.thrillring.com → Port 3004 (Gaming)"
        echo ""
        echo "Enable SSL (Let's Encrypt) for all domains at:"
        echo "https://dk.bizoholic.com"

        exit 0
    fi

    if [ $current_count -gt $last_count ]; then
        echo -e "${GREEN}+$((current_count - last_count)) services came online${NC}"
        last_count=$current_count
    elif [ $current_count -lt $last_count ]; then
        echo -e "${RED}⚠ $((last_count - current_count)) services went offline${NC}"
        last_count=$current_count
    else
        echo "No change from last check"
    fi

    iteration=$((iteration + 1))

    if [ $iteration -lt $max_iterations ]; then
        echo "Next check in 2 minutes..."
        sleep 120
    fi
done

echo ""
echo -e "${YELLOW}=========================================="
echo "Maximum monitoring time reached (60 min)"
echo "==========================================${NC}"
echo ""
echo "Final status: $current_count/22 services"
echo ""
echo "Some services may still be building."
echo "Check build logs at: https://dk.bizoholic.com"
