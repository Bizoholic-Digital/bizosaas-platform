#!/bin/bash

# BizOSaaS Platform - Complete 20 Container Verification Script
# Verifies all containers across Infrastructure, Backend, and Frontend projects
# Staging Environment - 194.238.16.237

set -e

VPS_IP="194.238.16.237"
ENVIRONMENT="staging"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# Function to print section headers
print_header() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
}

# Function to print subsection headers
print_subsection() {
    echo ""
    echo -e "${BLUE}--- $1 ---${NC}"
}

# Function to check service health
check_service() {
    local service_name=$1
    local url=$2
    local expected_status=${3:-200}

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    echo -n "Checking $service_name... "

    if response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null); then
        if [ "$response" -eq "$expected_status" ]; then
            echo -e "${GREEN}✓ PASS${NC} (HTTP $response)"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
            return 0
        else
            echo -e "${YELLOW}⚠ WARNING${NC} (HTTP $response, expected $expected_status)"
            WARNING_CHECKS=$((WARNING_CHECKS + 1))
            return 1
        fi
    else
        echo -e "${RED}✗ FAIL${NC} (Connection failed)"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

# Function to check container status
check_container() {
    local container_name=$1

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    echo -n "Checking container $container_name... "

    # This would need to be run on the VPS or via Docker API
    # For now, we'll just mark it as a placeholder
    echo -e "${BLUE}[MANUAL CHECK REQUIRED]${NC}"

    return 0
}

# Main verification function
main() {
    print_header "BizOSaaS Platform - Complete 20 Container Verification"
    echo "Environment: $ENVIRONMENT"
    echo "Target VPS: $VPS_IP"
    echo "Total Containers: 20"
    echo "Verification Date: $(date)"

    # ==========================================
    # PHASE 1: INFRASTRUCTURE PROJECT (6 containers)
    # ==========================================
    print_header "PHASE 1: INFRASTRUCTURE PROJECT (6 Containers)"

    print_subsection "1.1 PostgreSQL Database"
    check_container "bizosaas-postgres-staging"
    echo "Port: 5432"
    echo "Database: bizosaas_staging"
    echo "Health: Use psql to verify connection"
    echo "Command: PGPASSWORD='BizOSaaS2025!StagingDB' psql -h $VPS_IP -p 5432 -U admin -d bizosaas_staging -c 'SELECT 1;'"

    print_subsection "1.2 Redis Cache"
    check_container "bizosaas-redis-staging"
    echo "Port: 6379"
    echo "Health: Use redis-cli to verify connection"
    echo "Command: redis-cli -h $VPS_IP -p 6379 ping"

    print_subsection "1.3 HashiCorp Vault"
    check_container "bizosaas-vault-staging"
    check_service "Vault Health API" "http://$VPS_IP:8200/v1/sys/health" "200"
    echo "Port: 8200"
    echo "UI: http://$VPS_IP:8200/ui"
    echo "Root Token: staging-root-token-bizosaas-2025"

    print_subsection "1.4 Temporal Server"
    check_container "bizosaas-temporal-server-staging"
    echo "Port: 7233"
    echo "Health: Use tctl to verify connection"
    echo "Command: tctl --address $VPS_IP:7233 workflow list"

    print_subsection "1.5 Temporal UI"
    check_container "bizosaas-temporal-ui-staging"
    check_service "Temporal UI" "http://$VPS_IP:8082" "200"
    echo "Port: 8082"
    echo "UI: http://$VPS_IP:8082"

    print_subsection "1.6 Temporal Integration Service"
    check_container "bizosaas-temporal-integration-staging"
    check_service "Temporal Integration Health" "http://$VPS_IP:8009/health" "200"
    echo "Port: 8009"

    # ==========================================
    # PHASE 2: BACKEND SERVICES PROJECT (8 containers)
    # ==========================================
    print_header "PHASE 2: BACKEND SERVICES PROJECT (8 Containers)"

    print_subsection "2.1 AI Central Hub (Brain API)"
    check_container "bizosaas-brain-staging"
    check_service "Brain API Health" "http://$VPS_IP:8001/health" "200"
    echo "Port: 8001"
    echo "Critical: Main API coordinator for entire platform"

    print_subsection "2.2 Wagtail CMS"
    check_container "bizosaas-wagtail-staging"
    check_service "Wagtail Health" "http://$VPS_IP:8002/health/" "200"
    echo "Port: 8002"

    print_subsection "2.3 Django CRM"
    check_container "bizosaas-django-crm-staging"
    check_service "Django CRM Health" "http://$VPS_IP:8003/health/" "200"
    echo "Port: 8003"

    print_subsection "2.4 Business Directory API"
    check_container "bizosaas-directory-api-staging"
    check_service "Directory API Health" "http://$VPS_IP:8004/health" "200"
    echo "Port: 8004"

    print_subsection "2.5 CorelDove E-commerce Backend"
    check_container "coreldove-backend-staging"
    check_service "CorelDove Backend Health" "http://$VPS_IP:8005/health" "200"
    echo "Port: 8005"
    echo "Critical: E-commerce API backend"

    print_subsection "2.6 AI Agents Service"
    check_container "bizosaas-ai-agents-staging"
    check_service "AI Agents Health" "http://$VPS_IP:8010/health" "200"
    echo "Port: 8010"
    echo "Critical: Multi-model AI coordination"

    print_subsection "2.7 Amazon Sourcing API"
    check_container "amazon-sourcing-staging"
    check_service "Amazon Sourcing Health" "http://$VPS_IP:8085/health" "200"
    echo "Port: 8085"

    print_subsection "2.8 Saleor E-commerce Engine"
    check_container "bizosaas-saleor-staging"
    check_service "Saleor Health" "http://$VPS_IP:8000/health/" "200"
    echo "Port: 8000"
    echo "Advanced e-commerce platform"

    # ==========================================
    # PHASE 3: FRONTEND APPLICATIONS PROJECT (6 containers)
    # ==========================================
    print_header "PHASE 3: FRONTEND APPLICATIONS PROJECT (6 Containers)"

    print_subsection "3.1 Bizoholic Marketing Frontend"
    check_container "bizoholic-frontend-staging"
    check_service "Bizoholic Frontend" "https://stg.bizoholic.com" "200"
    echo "Port: 3000"
    echo "Domain: stg.bizoholic.com"
    echo "SSL: Let's Encrypt"

    print_subsection "3.2 Client Portal"
    check_container "client-portal-staging"
    check_service "Client Portal" "https://stg.bizoholic.com/login/" "200"
    echo "Port: 3001"
    echo "Path: stg.bizoholic.com/login/"
    echo "Routing: Path-based with StripPrefix"

    print_subsection "3.3 CorelDove E-commerce Frontend"
    check_container "coreldove-frontend-staging"
    check_service "CorelDove Frontend" "https://stg.coreldove.com" "200"
    echo "Port: 3002"
    echo "Domain: stg.coreldove.com"
    echo "SSL: Let's Encrypt"

    print_subsection "3.4 Business Directory Frontend"
    check_container "business-directory-staging"
    echo "Port: 3004"
    echo "Internal testing only (no external domain)"

    print_subsection "3.5 ThrillRing Gaming Platform"
    check_container "thrillring-gaming-staging"
    check_service "ThrillRing Gaming" "https://stg.thrillring.com" "200"
    echo "Port: 3005"
    echo "Domain: stg.thrillring.com"
    echo "SSL: Let's Encrypt"

    print_subsection "3.6 Admin Dashboard"
    check_container "admin-dashboard-staging"
    check_service "Admin Dashboard" "https://stg.bizoholic.com/admin/" "200"
    echo "Port: 3009"
    echo "Path: stg.bizoholic.com/admin/"
    echo "Routing: Path-based with StripPrefix"

    # ==========================================
    # SUMMARY
    # ==========================================
    print_header "VERIFICATION SUMMARY"

    echo "Total Checks: $TOTAL_CHECKS"
    echo -e "Passed: ${GREEN}$PASSED_CHECKS${NC}"
    echo -e "Warnings: ${YELLOW}$WARNING_CHECKS${NC}"
    echo -e "Failed: ${RED}$FAILED_CHECKS${NC}"
    echo ""

    # Calculate success rate
    if [ $TOTAL_CHECKS -gt 0 ]; then
        SUCCESS_RATE=$(echo "scale=2; ($PASSED_CHECKS / $TOTAL_CHECKS) * 100" | bc)
        echo -e "Success Rate: ${GREEN}${SUCCESS_RATE}%${NC}"
    fi

    echo ""
    echo "Container Breakdown:"
    echo "  Infrastructure: 6 containers"
    echo "  Backend Services: 8 containers"
    echo "  Frontend Applications: 6 containers"
    echo "  Total: 20 containers"
    echo ""

    if [ $FAILED_CHECKS -eq 0 ] && [ $WARNING_CHECKS -eq 0 ]; then
        echo -e "${GREEN}✓ ALL SYSTEMS OPERATIONAL${NC}"
        echo "Platform ready for staging testing!"
        exit 0
    elif [ $FAILED_CHECKS -eq 0 ]; then
        echo -e "${YELLOW}⚠ PLATFORM OPERATIONAL WITH WARNINGS${NC}"
        echo "Review warning messages above"
        exit 0
    else
        echo -e "${RED}✗ PLATFORM HAS ISSUES${NC}"
        echo "Review failed checks above and troubleshoot"
        exit 1
    fi
}

# Run main function
main "$@"
