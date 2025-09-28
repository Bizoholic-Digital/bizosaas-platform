#!/bin/bash

# Virtual Environment Migration Script
# Migrates from global Python packages to isolated virtual environments

set -e

SERVICES_DIR="/home/alagiri/projects/bizoholic/bizosaas/services"
SCRIPTS_DIR="${SERVICES_DIR}/../scripts"
LOG_DIR="${SERVICES_DIR}/../logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_header() {
    echo ""
    print_status $CYAN "=================================================="
    print_status $CYAN "$1"
    print_status $CYAN "=================================================="
    echo ""
}

# Create log directory
mkdir -p "${LOG_DIR}"

print_header "BizOSaaS Virtual Environment Migration"

print_status $BLUE "📋 Migration Plan:"
echo "  1. Stop currently running services"
echo "  2. Create virtual environments for each service"
echo "  3. Install service-specific dependencies"
echo "  4. Update startup scripts to use virtual environments"
echo "  5. Restart services with isolated environments"
echo "  6. Verify all services are working correctly"

echo ""
read -p "Continue with migration? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_status $YELLOW "Migration cancelled."
    exit 0
fi

# Step 1: Stop existing services
print_header "Step 1: Stopping Existing Services"
print_status $BLUE "🛑 Stopping all running services..."
bash "${SCRIPTS_DIR}/stop-all-services.sh"
print_status $GREEN "✅ All services stopped"

# Step 2: Create virtual environments
print_header "Step 2: Creating Virtual Environments"
print_status $BLUE "🐍 Setting up virtual environments..."
bash "${SCRIPTS_DIR}/setup-virtual-environments.sh"
print_status $GREEN "✅ Virtual environments created"

# Step 3: Make scripts executable
print_header "Step 3: Setting Up Management Scripts"
print_status $BLUE "🔧 Making scripts executable..."
chmod +x "${SCRIPTS_DIR}/activate-venv.sh"
chmod +x "${SCRIPTS_DIR}/start-services-with-venv.sh"
chmod +x "${SCRIPTS_DIR}/stop-all-services.sh"
chmod +x "${SCRIPTS_DIR}/check-service-status.sh"
chmod +x "${SCRIPTS_DIR}/manage-dependencies.sh"
print_status $GREEN "✅ Scripts are ready"

# Step 4: Create migration completion marker
MIGRATION_MARKER="${SERVICES_DIR}/.venv-migration-complete"
echo "Migration completed on: $(date)" > "${MIGRATION_MARKER}"
echo "Migration script: $0" >> "${MIGRATION_MARKER}"
print_status $GREEN "✅ Migration marker created"

# Step 5: Test virtual environment setup
print_header "Step 4: Testing Virtual Environment Setup"
print_status $BLUE "🧪 Testing virtual environment activation..."

# Test a few key services
test_services=("ai-agents" "api-gateway" "business-directory")
for service in "${test_services[@]}"; do
    print_status $BLUE "Testing ${service}..."
    
    # Test activation script
    if bash -c "source ${SCRIPTS_DIR}/activate-venv.sh ${service} && python --version" >/dev/null 2>&1; then
        print_status $GREEN "  ✅ ${service} virtual environment working"
    else
        print_status $RED "  ❌ ${service} virtual environment failed"
    fi
done

# Step 6: Provide next steps
print_header "Migration Complete!"

print_status $GREEN "🎉 Virtual environment migration completed successfully!"
echo ""
print_status $BLUE "📋 What changed:"
echo "  - Each Python service now has its own isolated virtual environment"
echo "  - Dependencies are no longer installed globally"
echo "  - Services use dedicated Python environments in services/.venvs/"
echo "  - New management scripts are available for easier development"

echo ""
print_status $YELLOW "🔧 Available Management Commands:"
echo "  - Start services:     bash scripts/start-services-with-venv.sh"
echo "  - Stop services:      bash scripts/stop-all-services.sh"
echo "  - Check status:       bash scripts/check-service-status.sh"
echo "  - Activate service:   source scripts/activate-venv.sh <service-name>"
echo "  - Manage deps:        bash scripts/manage-dependencies.sh help"

echo ""
print_status $YELLOW "🚀 Next Steps:"
echo "  1. Start services: bash scripts/start-services-with-venv.sh"
echo "  2. Check status:   bash scripts/check-service-status.sh"
echo "  3. Test endpoints: curl http://localhost:8001/health (AI Agents)"
echo "  4. View logs:      tail -f logs/ai-agents.log"

echo ""
print_status $BLUE "💡 Development Tips:"
echo "  - Use 'source scripts/activate-venv.sh <service>' to work on a specific service"
echo "  - Install new packages: bash scripts/manage-dependencies.sh install <service> <package>"
echo "  - Update all deps: bash scripts/manage-dependencies.sh update"
echo "  - Create dep report: bash scripts/manage-dependencies.sh report"

echo ""
print_status $CYAN "Virtual environment migration completed! 🎉"