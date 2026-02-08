#!/bin/bash
# Real-time deployment monitoring

VPS_IP="194.238.16.237"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

clear
echo "=========================================="
echo "Real-Time Deployment Monitor"
echo "Press Ctrl+C to stop"
echo "=========================================="
echo ""

while true; do
    # Count running services
    infra=0
    backend=0
    frontend=0
    
    for port in 5433 6380 8201 7234 8083 8088; do
        timeout 2 nc -zv $VPS_IP $port 2>&1 | grep -q succeeded && infra=$((infra + 1))
    done
    
    for port in {8000..8009}; do
        timeout 2 nc -zv $VPS_IP $port 2>&1 | grep -q succeeded && backend=$((backend + 1))
    done
    
    for port in 3000 3001 3002 3003 3004 3005; do
        timeout 2 nc -zv $VPS_IP $port 2>&1 | grep -q succeeded && frontend=$((frontend + 1))
    done
    
    total=$((infra + backend + frontend))
    percentage=$((total * 100 / 22))
    
    # Clear and display
    clear
    echo "=========================================="
    echo -e "${BLUE}Real-Time Deployment Monitor${NC}"
    echo "$(date '+%H:%M:%S')"
    echo "=========================================="
    echo ""
    echo -e "${YELLOW}Progress: $total/22 services ($percentage%)${NC}"
    echo ""
    echo -e "Infrastructure: ${GREEN}$infra/6${NC}"
    echo -e "Backend:        ${YELLOW}$backend/10${NC}"
    echo -e "Frontend:       ${YELLOW}$frontend/6${NC}"
    echo ""
    echo "=========================================="
    echo "Checking again in 10 seconds..."
    echo "Press Ctrl+C to stop"
    
    if [ $total -eq 22 ]; then
        echo ""
        echo -e "${GREEN}🎉 ALL 22 SERVICES RUNNING!${NC}"
        break
    fi
    
    sleep 10
done
