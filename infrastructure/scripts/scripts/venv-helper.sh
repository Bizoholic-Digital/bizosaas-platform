#!/bin/bash

# Virtual Environment Helper Script
# Provides easy access to common virtual environment operations

SERVICES_DIR="/home/alagiri/projects/bizoholic/bizosaas/services"
SCRIPTS_DIR="${SERVICES_DIR}/../scripts"
VENV_BASE_DIR="${SERVICES_DIR}/.venvs"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo -e "${CYAN}======================================${NC}"
    echo -e "${CYAN}  BizOSaaS Virtual Environment Helper${NC}"
    echo -e "${CYAN}======================================${NC}"
    echo ""
}

print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

show_help() {
    print_header
    echo -e "${BLUE}Available Commands:${NC}"
    echo ""
    echo -e "${GREEN}Setup & Migration:${NC}"
    echo "  $0 setup                 - Create virtual environments for all services"
    echo "  $0 migrate               - Complete migration from global packages"
    echo ""
    echo -e "${GREEN}Service Management:${NC}"
    echo "  $0 start [service]       - Start all services or specific service"
    echo "  $0 stop                  - Stop all services"
    echo "  $0 restart [service]     - Restart all services or specific service"
    echo "  $0 status                - Check service status"
    echo ""
    echo -e "${GREEN}Development:${NC}"
    echo "  $0 activate <service>    - Show activation command for service"
    echo "  $0 list                  - List available services"
    echo "  $0 logs [service]        - View logs for all services or specific service"
    echo ""
    echo -e "${GREEN}Dependencies:${NC}"
    echo "  $0 deps update [service] - Update dependencies"
    echo "  $0 deps check [service]  - Check for outdated packages"
    echo "  $0 deps install <service> <package> - Install package to service"
    echo "  $0 deps report           - Generate dependency report"
    echo ""
    echo -e "${GREEN}Information:${NC}"
    echo "  $0 info                  - Show virtual environment information"
    echo "  $0 health                - Run health check on all services"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  $0 start ai-agents       # Start AI Agents service"
    echo "  $0 activate ai-agents    # Show how to activate AI Agents environment"
    echo "  $0 logs                  # View all service logs"
    echo "  $0 deps update           # Update all dependencies"
}

list_services() {
    print_status $BLUE "📦 Available Services:"
    if [[ -d "${VENV_BASE_DIR}" ]]; then
        for venv_dir in "${VENV_BASE_DIR}"/*; do
            if [[ -d "${venv_dir}" ]]; then
                service_name=$(basename "${venv_dir}")
                service_dir="${SERVICES_DIR}/${service_name}"
                if [[ -d "${service_dir}" ]]; then
                    print_status $GREEN "  ✅ ${service_name}"
                else
                    print_status $YELLOW "  ⚠️  ${service_name} (service directory missing)"
                fi
            fi
        done
    else
        print_status $RED "  No virtual environments found. Run: $0 setup"
    fi
}

show_info() {
    print_header
    print_status $BLUE "📊 Virtual Environment Information:"
    echo ""
    
    print_status $BLUE "📁 Directories:"
    echo "   Services: ${SERVICES_DIR}"
    echo "   Virtual Envs: ${VENV_BASE_DIR}"
    echo "   Scripts: ${SCRIPTS_DIR}"
    echo ""
    
    if [[ -d "${VENV_BASE_DIR}" ]]; then
        venv_count=$(find "${VENV_BASE_DIR}" -maxdepth 1 -type d | wc -l)
        venv_count=$((venv_count - 1))  # Subtract 1 for the base directory
        print_status $GREEN "🐍 Virtual Environments: ${venv_count} created"
    else
        print_status $RED "🐍 Virtual Environments: Not set up"
    fi
    
    print_status $BLUE "📋 Available Scripts:"
    if [[ -d "${SCRIPTS_DIR}" ]]; then
        ls -1 "${SCRIPTS_DIR}"/*.sh 2>/dev/null | while read -r script; do
            script_name=$(basename "${script}")
            echo "   - ${script_name}"
        done
    fi
}

run_health_check() {
    print_status $BLUE "🏥 Running Health Check..."
    echo ""
    
    # Check if virtual environments exist
    if [[ ! -d "${VENV_BASE_DIR}" ]]; then
        print_status $RED "❌ Virtual environments not set up"
        echo "   Run: $0 setup"
        return 1
    fi
    
    # Check scripts
    local scripts=("setup-virtual-environments.sh" "start-services-with-venv.sh" "check-service-status.sh")
    for script in "${scripts[@]}"; do
        if [[ -x "${SCRIPTS_DIR}/${script}" ]]; then
            print_status $GREEN "✅ ${script} is executable"
        else
            print_status $RED "❌ ${script} not found or not executable"
        fi
    done
    
    # Check key services
    local services=("ai-agents" "api-gateway" "business-directory")
    for service in "${services[@]}"; do
        if [[ -d "${VENV_BASE_DIR}/${service}" ]]; then
            print_status $GREEN "✅ ${service} virtual environment exists"
        else
            print_status $YELLOW "⚠️  ${service} virtual environment missing"
        fi
    done
    
    echo ""
    print_status $BLUE "🔍 For detailed status, run: $0 status"
}

# Main command processing
case "${1:-help}" in
    "setup")
        bash "${SCRIPTS_DIR}/setup-virtual-environments.sh"
        ;;
    "migrate")
        bash "${SCRIPTS_DIR}/venv-migration.sh"
        ;;
    "start")
        if [[ -n "$2" ]]; then
            bash "${SCRIPTS_DIR}/start-service.sh" "$2"
        else
            bash "${SCRIPTS_DIR}/start-services-with-venv.sh"
        fi
        ;;
    "stop")
        bash "${SCRIPTS_DIR}/stop-all-services.sh"
        ;;
    "restart")
        bash "${SCRIPTS_DIR}/stop-all-services.sh"
        sleep 2
        if [[ -n "$2" ]]; then
            bash "${SCRIPTS_DIR}/start-service.sh" "$2"
        else
            bash "${SCRIPTS_DIR}/start-services-with-venv.sh"
        fi
        ;;
    "status")
        bash "${SCRIPTS_DIR}/check-service-status.sh"
        ;;
    "activate")
        if [[ -n "$2" ]]; then
            print_status $BLUE "To activate ${2} virtual environment, run:"
            print_status $YELLOW "source scripts/activate-venv.sh ${2}"
        else
            print_status $RED "Usage: $0 activate <service-name>"
            list_services
        fi
        ;;
    "list")
        list_services
        ;;
    "logs")
        if [[ -n "$2" ]]; then
            log_file="${SERVICES_DIR}/../logs/${2}.log"
            if [[ -f "${log_file}" ]]; then
                print_status $BLUE "📋 Viewing logs for ${2}:"
                tail -f "${log_file}"
            else
                print_status $RED "❌ Log file not found: ${log_file}"
            fi
        else
            print_status $BLUE "📋 All service logs:"
            if [[ -d "${SERVICES_DIR}/../logs" ]]; then
                ls -la "${SERVICES_DIR}/../logs"/*.log 2>/dev/null || echo "No log files found"
            fi
        fi
        ;;
    "deps")
        shift
        bash "${SCRIPTS_DIR}/manage-dependencies.sh" "$@"
        ;;
    "info")
        show_info
        ;;
    "health")
        run_health_check
        ;;
    "help"|*)
        show_help
        ;;
esac