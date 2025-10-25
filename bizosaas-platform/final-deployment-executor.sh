#!/bin/bash

# BizOSaaS Platform - Final Deployment Executor
# Executes deployment using available methods and iterates until success

set -e

VPS_IP="72.60.219.244"
DOKPLOY_URL="https://dk4.bizoholic.com"
PROJECT_DIR="/home/alagiri/projects/bizoholic/bizosaas-platform"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_section() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}========================================${NC}"
}

# Check current status
check_current_status() {
    log_section "CHECKING CURRENT STATUS"

    local total=0
    local running=0

    # Check infrastructure (ports 5433, 6380, 8201, 7234, 8083, 8088)
    for port in 5433 6380 8201 7234 8083 8088; do
        total=$((total + 1))
        if nc -z -w2 $VPS_IP $port 2>/dev/null; then
            running=$((running + 1))
        fi
    done

    # Check backend services (ports 8000-8009)
    for port in 8000 8001 8002 8003 8004 8005 8006 8007 8008 8009; do
        total=$((total + 1))
        if curl -f -s -o /dev/null --connect-timeout 2 "http://$VPS_IP:$port/health" 2>/dev/null || \
           curl -f -s -o /dev/null --connect-timeout 2 "http://$VPS_IP:$port/health/" 2>/dev/null; then
            running=$((running + 1))
        fi
    done

    # Check frontend services (ports 3000, 3001, 3002, 3003, 3005, 3009)
    for port in 3000 3001 3002 3003 3005 3009; do
        total=$((total + 1))
        if curl -f -s -o /dev/null --connect-timeout 2 "http://$VPS_IP:$port/api/health" 2>/dev/null || \
           curl -f -s -o /dev/null --connect-timeout 2 "http://$VPS_IP:$port/" 2>/dev/null; then
            running=$((running + 1))
        fi
    done

    log_info "Current Status: $running/$total services running ($(($running * 100 / $total))%)"

    echo "$running"
}

# Show deployment instructions
show_instructions() {
    log_section "DEPLOYMENT INSTRUCTIONS"

    cat <<'EOF'
Since automated API deployment requires configuration, please complete deployment manually:

═══════════════════════════════════════════════════════════════════

STEP 1: DEPLOY BACKEND SERVICES (40 minutes)
═══════════════════════════════════════════════════════════════════

1. Open browser: https://dk4.bizoholic.com

2. Login to Dokploy

3. Click "Projects" → "Create New Project"
   Name: backend-services
   Description: BizOSaaS Backend Services

4. Inside project, click "Create Application"

5. Select "Docker Compose"

6. Configure:
   Name: backend-staging
   Source Type: Git Repository
   Repository: https://github.com/Bizoholic-Digital/bizosaas-platform.git
   Branch: main
   Compose File: bizosaas-platform/dokploy-backend-staging.yml

7. Add Environment Variables:
   OPENAI_API_KEY=<your-key>
   ANTHROPIC_API_KEY=<your-key>
   AMAZON_ACCESS_KEY=<your-key>
   AMAZON_SECRET_KEY=<your-key>

8. Click "Deploy" button

9. Wait for build to complete (~40 minutes)

═══════════════════════════════════════════════════════════════════

STEP 2: DEPLOY FRONTEND SERVICES (30 minutes)
═══════════════════════════════════════════════════════════════════

1. In Dokploy, click "Projects" → "Create New Project"
   Name: frontend-services
   Description: BizOSaaS Frontend Applications

2. Inside project, click "Create Application"

3. Select "Docker Compose"

4. Configure:
   Name: frontend-staging
   Source Type: Git Repository
   Repository: https://github.com/Bizoholic-Digital/bizosaas-platform.git
   Branch: main
   Compose File: bizosaas-platform/dokploy-frontend-staging.yml

5. Click "Deploy" button

6. Wait for build to complete (~30 minutes)

═══════════════════════════════════════════════════════════════════

STEP 3: CONFIGURE DOMAINS (15 minutes)
═══════════════════════════════════════════════════════════════════

After frontend deployment completes:

1. In Dokploy, go to each frontend application

2. Click "Domains" tab

3. Configure:
   - bizosaas-bizoholic-frontend-staging → stg.bizoholic.com
   - bizosaas-coreldove-frontend-staging → stg.coreldove.com
   - bizosaas-thrillring-gaming-staging → stg.thrillring.com
   - bizosaas-client-portal-staging → stg.portal.bizoholic.com
   - bizosaas-business-directory-frontend-staging → stg.directory.bizoholic.com
   - bizosaas-admin-dashboard-staging → stg.admin.bizoholic.com

4. Enable SSL (Let's Encrypt) for each domain

5. Wait 5-10 minutes for SSL generation

═══════════════════════════════════════════════════════════════════

EOF

    log_warning "After completing deployment, run:"
    echo "  ./verify-staging-deployment.sh"
    echo ""
}

# Monitor deployment progress
monitor_deployment() {
    log_section "MONITORING DEPLOYMENT PROGRESS"

    local max_iterations=50
    local iteration=0
    local last_count=$(check_current_status)

    log_info "Starting monitoring loop (max $max_iterations iterations)..."

    while [ $iteration -lt $max_iterations ]; do
        iteration=$((iteration + 1))

        sleep 60

        log_info "Check #$iteration: Verifying service status..."

        local current_count=$(check_current_status)

        if [ $current_count -gt $last_count ]; then
            log_success "Progress detected! ($last_count → $current_count services)"
            last_count=$current_count
        elif [ $current_count -eq 22 ]; then
            log_success "ALL 22 SERVICES ARE RUNNING!"
            return 0
        else
            log_warning "No change ($current_count services)"
        fi

        if [ $((iteration % 5)) -eq 0 ]; then
            log_info "Detailed status check..."
            bash "$PROJECT_DIR/check-services.sh"
        fi
    done

    log_warning "Monitoring loop completed. Final status: $last_count/22 services"
}

# Generate deployment report
generate_report() {
    log_section "GENERATING DEPLOYMENT REPORT"

    local report_file="$PROJECT_DIR/FINAL_DEPLOYMENT_REPORT_$(date +%Y%m%d_%H%M%S).md"

    cat > "$report_file" <<EOF
# BizOSaaS Platform - Final Deployment Report

**Generated**: $(date)
**Environment**: Staging
**VPS**: $VPS_IP
**Dokploy**: $DOKPLOY_URL

## Deployment Status

EOF

    # Run verification and append to report
    bash "$PROJECT_DIR/verify-staging-deployment.sh" >> "$report_file" 2>&1

    cat >> "$report_file" <<EOF

## Deployment Files

All configuration files:
- Backend: \`dokploy-backend-staging.yml\`
- Frontend: \`dokploy-frontend-staging.yml\`
- Verification: \`verify-staging-deployment.sh\`

## Next Steps

1. Verify all services are healthy
2. Configure domain DNS records
3. Test all application endpoints
4. Configure SSL certificates
5. Run integration tests

---

*Generated with BizOSaaS Deployment Automation*
EOF

    log_success "Report generated: $report_file"

    cat "$report_file"
}

# Main execution
main() {
    log_section "BizOSaaS Platform - Final Deployment Executor"

    log_info "VPS: $VPS_IP"
    log_info "Dokploy: $DOKPLOY_URL"
    log_info "Project Dir: $PROJECT_DIR"
    echo ""

    # Check current status
    local current_services=$(check_current_status)

    log_info "Current: $current_services/22 services running"
    log_info "Target: 22/22 services (100%)"
    log_info "Remaining: $((22 - current_services)) services to deploy"
    echo ""

    # Show deployment options
    echo "Choose execution mode:"
    echo ""
    echo "1. Show deployment instructions (manual via Dokploy UI)"
    echo "2. Monitor deployment progress (check status every minute)"
    echo "3. Run full verification and generate report"
    echo "4. Quick service status check"
    echo ""

    read -p "Select option (1-4): " choice

    case $choice in
        1)
            show_instructions
            ;;

        2)
            show_instructions
            echo ""
            read -p "Press ENTER to start monitoring deployment progress..."
            monitor_deployment
            generate_report
            ;;

        3)
            bash "$PROJECT_DIR/verify-staging-deployment.sh"
            generate_report
            ;;

        4)
            bash "$PROJECT_DIR/check-services.sh"
            ;;

        *)
            log_error "Invalid option"
            exit 1
            ;;
    esac

    log_section "EXECUTION COMPLETE"

    log_success "Deployment executor finished"
}

main "$@"
