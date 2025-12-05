#!/bin/bash

# Dependency Management Script for BizOSaaS Services
# Manages Python dependencies across all virtual environments

set -e

SERVICES_DIR="/home/alagiri/projects/bizoholic/bizosaas/services"
VENV_BASE_DIR="${SERVICES_DIR}/.venvs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to update dependencies for a service
update_service_dependencies() {
    local service_name=$1
    local service_dir="${SERVICES_DIR}/${service_name}"
    local venv_dir="${VENV_BASE_DIR}/${service_name}"
    local requirements_file="${service_dir}/requirements.txt"
    
    if [[ ! -d "${service_dir}" ]]; then
        print_status $RED "⚠️  Service directory not found: ${service_dir}"
        return 1
    fi
    
    if [[ ! -d "${venv_dir}" ]]; then
        print_status $RED "⚠️  Virtual environment not found for ${service_name}. Run setup-virtual-environments.sh first."
        return 1
    fi
    
    if [[ ! -f "${requirements_file}" ]]; then
        print_status $YELLOW "⚠️  No requirements.txt found for ${service_name}, skipping..."
        return 0
    fi
    
    print_status $BLUE "📦 Updating dependencies for ${service_name}..."
    
    # Activate virtual environment
    source "${venv_dir}/bin/activate"
    
    # Upgrade pip first
    pip install --upgrade pip wheel setuptools
    
    # Install/update requirements
    pip install --upgrade -r "${requirements_file}"
    
    # Generate frozen requirements for reproducibility
    pip freeze > "${service_dir}/requirements-frozen.txt"
    
    deactivate
    
    print_status $GREEN "✅ Dependencies updated for ${service_name}"
}

# Function to check outdated packages
check_outdated_packages() {
    local service_name=$1
    local venv_dir="${VENV_BASE_DIR}/${service_name}"
    
    if [[ ! -d "${venv_dir}" ]]; then
        print_status $RED "⚠️  Virtual environment not found for ${service_name}"
        return 1
    fi
    
    print_status $BLUE "🔍 Checking outdated packages for ${service_name}..."
    
    source "${venv_dir}/bin/activate"
    outdated=$(pip list --outdated --format=freeze 2>/dev/null || true)
    
    if [[ -n "${outdated}" ]]; then
        print_status $YELLOW "📦 Outdated packages in ${service_name}:"
        echo "${outdated}" | while IFS='==' read -r package current; do
            echo "  - ${package}: ${current}"
        done
    else
        print_status $GREEN "✅ All packages up to date for ${service_name}"
    fi
    
    deactivate
}

# Function to install a package to specific service
install_package() {
    local service_name=$1
    local package_name=$2
    local venv_dir="${VENV_BASE_DIR}/${service_name}"
    local requirements_file="${SERVICES_DIR}/${service_name}/requirements.txt"
    
    if [[ ! -d "${venv_dir}" ]]; then
        print_status $RED "⚠️  Virtual environment not found for ${service_name}"
        return 1
    fi
    
    print_status $BLUE "📦 Installing ${package_name} in ${service_name}..."
    
    source "${venv_dir}/bin/activate"
    pip install "${package_name}"
    
    # Add to requirements.txt if it doesn't exist
    if [[ -f "${requirements_file}" ]] && ! grep -q "^${package_name%>=*}" "${requirements_file}"; then
        echo "${package_name}" >> "${requirements_file}"
        print_status $BLUE "📝 Added ${package_name} to requirements.txt"
    fi
    
    deactivate
    print_status $GREEN "✅ ${package_name} installed in ${service_name}"
}

# Function to create dependency report
create_dependency_report() {
    local report_file="${SERVICES_DIR}/../logs/dependency-report-$(date +%Y%m%d-%H%M%S).txt"
    
    mkdir -p "$(dirname "${report_file}")"
    
    print_status $BLUE "📊 Creating dependency report..."
    
    {
        echo "BizOSaaS Dependency Report"
        echo "=========================="
        echo "Generated on: $(date)"
        echo ""
        
        for venv_dir in "${VENV_BASE_DIR}"/*; do
            if [[ -d "${venv_dir}" ]]; then
                service_name=$(basename "${venv_dir}")
                echo "Service: ${service_name}"
                echo "$(printf '=%.0s' {1..40})"
                
                source "${venv_dir}/bin/activate" 2>/dev/null
                pip list --format=freeze 2>/dev/null || echo "Error reading packages"
                deactivate 2>/dev/null
                
                echo ""
            fi
        done
    } > "${report_file}"
    
    print_status $GREEN "✅ Dependency report created: ${report_file}"
}

# Main script logic
case "${1:-help}" in
    "update")
        if [[ -n "$2" ]]; then
            update_service_dependencies "$2"
        else
            print_status $BLUE "📦 Updating all service dependencies..."
            for venv_dir in "${VENV_BASE_DIR}"/*; do
                if [[ -d "${venv_dir}" ]]; then
                    service_name=$(basename "${venv_dir}")
                    update_service_dependencies "${service_name}"
                fi
            done
            print_status $GREEN "🎉 All dependencies updated!"
        fi
        ;;
    "check")
        if [[ -n "$2" ]]; then
            check_outdated_packages "$2"
        else
            print_status $BLUE "🔍 Checking all services for outdated packages..."
            for venv_dir in "${VENV_BASE_DIR}"/*; do
                if [[ -d "${venv_dir}" ]]; then
                    service_name=$(basename "${venv_dir}")
                    check_outdated_packages "${service_name}"
                fi
            done
        fi
        ;;
    "install")
        if [[ -n "$2" ]] && [[ -n "$3" ]]; then
            install_package "$2" "$3"
        else
            print_status $RED "❌ Usage: $0 install <service-name> <package-name>"
            exit 1
        fi
        ;;
    "report")
        create_dependency_report
        ;;
    "help"|*)
        echo "BizOSaaS Dependency Management Script"
        echo ""
        echo "Usage: $0 <command> [options]"
        echo ""
        echo "Commands:"
        echo "  update [service]     Update dependencies for all services or specific service"
        echo "  check [service]      Check for outdated packages in all services or specific service"
        echo "  install <service> <package>  Install a package to a specific service"
        echo "  report              Create a comprehensive dependency report"
        echo "  help                Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 update                    # Update all services"
        echo "  $0 update ai-agents          # Update only ai-agents service"
        echo "  $0 check                     # Check all services for outdated packages"
        echo "  $0 install api-gateway httpx # Install httpx in api-gateway service"
        echo "  $0 report                    # Generate dependency report"
        ;;
esac