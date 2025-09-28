#!/bin/bash

# Virtual Environment Setup Script for BizOSaaS Services
# Creates isolated Python environments for each service

set -e

SERVICES_DIR="/home/alagiri/projects/bizoholic/bizosaas/services"
VENV_BASE_DIR="${SERVICES_DIR}/.venvs"

echo "🚀 Setting up virtual environments for BizOSaaS services..."

# Create base directory for virtual environments
mkdir -p "${VENV_BASE_DIR}"

# List of Python services that need virtual environments
PYTHON_SERVICES=(
    "ai-agents"
    "api-gateway"
    "auth-service"
    "auth-service-v2"
    "business-directory"
    "wagtail-cms"
    "agent-monitor"
    "analytics-service"
    "byok-health-monitor"
    "campaign-management"
    "client-sites"
    "coreldove-bridge"
    "coreldove-bridge-saleor"
    "coreldove-sourcing"
    "coreldove-ai-sourcing"
    "crm-service"
    "crm-service-v2"
    "identity-service"
    "integration"
    "logging-service"
    "marketing-automation-service"
    "temporal-integration"
    "vault-integration"
)

# Function to create virtual environment for a service
create_service_venv() {
    local service_name=$1
    local service_dir="${SERVICES_DIR}/${service_name}"
    local venv_dir="${VENV_BASE_DIR}/${service_name}"
    
    if [[ ! -d "${service_dir}" ]]; then
        echo "⚠️  Service directory not found: ${service_dir}"
        return 1
    fi
    
    echo "📦 Creating virtual environment for ${service_name}..."
    
    # Create virtual environment
    python3 -m venv "${venv_dir}"
    
    # Activate and upgrade pip
    source "${venv_dir}/bin/activate"
    pip install --upgrade pip wheel setuptools
    
    # Install requirements if they exist
    if [[ -f "${service_dir}/requirements.txt" ]]; then
        echo "📋 Installing requirements for ${service_name}..."
        pip install -r "${service_dir}/requirements.txt"
    else
        echo "⚠️  No requirements.txt found for ${service_name}, installing common dependencies..."
        # Install common FastAPI stack
        pip install fastapi uvicorn sqlalchemy psycopg2-binary redis python-jose[cryptography] python-multipart
    fi
    
    deactivate
    echo "✅ Virtual environment created for ${service_name}"
}

# Create virtual environments for each service
for service in "${PYTHON_SERVICES[@]}"; do
    create_service_venv "$service"
done

echo ""
echo "🎉 Virtual environment setup complete!"
echo ""
echo "📁 Virtual environments location: ${VENV_BASE_DIR}"
echo ""
echo "🔧 Next steps:"
echo "   1. Run: chmod +x scripts/activate-venv.sh"
echo "   2. Use: scripts/activate-venv.sh <service-name> to activate a specific environment"
echo "   3. Use: scripts/start-services-with-venv.sh to start all services with their virtual environments"
echo ""