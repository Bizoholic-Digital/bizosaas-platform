#!/bin/bash

# Service Startup Script with Virtual Environments
# Starts all services using their dedicated virtual environments

set -e

SERVICES_DIR="/home/alagiri/projects/bizoholic/bizosaas/services"
VENV_BASE_DIR="${SERVICES_DIR}/.venvs"
LOG_DIR="/home/alagiri/projects/bizoholic/bizosaas/logs"

# Create logs directory
mkdir -p "${LOG_DIR}"

echo "🚀 Starting BizOSaaS services with virtual environments..."

# Function to start a service with its virtual environment
start_service_with_venv() {
    local service_name=$1
    local port=$2
    local main_file=${3:-"main.py"}
    local additional_args=${4:-""}
    
    local service_dir="${SERVICES_DIR}/${service_name}"
    local venv_dir="${VENV_BASE_DIR}/${service_name}"
    local log_file="${LOG_DIR}/${service_name}.log"
    
    if [[ ! -d "${service_dir}" ]]; then
        echo "⚠️  Service directory not found: ${service_dir}"
        return 1
    fi
    
    if [[ ! -d "${venv_dir}" ]]; then
        echo "⚠️  Virtual environment not found for ${service_name}. Run setup-virtual-environments.sh first."
        return 1
    fi
    
    if [[ ! -f "${service_dir}/${main_file}" ]]; then
        echo "⚠️  Main file not found: ${service_dir}/${main_file}"
        return 1
    fi
    
    echo "🔄 Starting ${service_name} on port ${port}..."
    
    cd "${service_dir}"
    source "${venv_dir}/bin/activate"
    
    # Start service in background
    nohup python "${main_file}" ${additional_args} > "${log_file}" 2>&1 &
    local pid=$!
    
    echo "${pid}" > "${LOG_DIR}/${service_name}.pid"
    echo "✅ ${service_name} started (PID: ${pid})"
    
    deactivate
}

# Function to check if port is available
is_port_available() {
    local port=$1
    ! lsof -Pi :${port} -sTCP:LISTEN -t >/dev/null
}

# Stop existing services gracefully
echo "🛑 Stopping existing services..."
bash "${SERVICES_DIR}/../scripts/stop-all-services.sh" 2>/dev/null || true

# Wait a bit for services to stop
sleep 2

# Start services with their virtual environments
echo "🚀 Starting services with virtual environments..."

# Core services first
if is_port_available 8080; then
    start_service_with_venv "api-gateway" 8080
else
    echo "⚠️  Port 8080 is already in use, skipping api-gateway"
fi

sleep 1

if is_port_available 8001; then
    start_service_with_venv "ai-agents" 8001
else
    echo "⚠️  Port 8001 is already in use, skipping ai-agents"
fi

sleep 1

if is_port_available 8003; then
    start_service_with_venv "business-directory" 8003
else
    echo "⚠️  Port 8003 is already in use, skipping business-directory"
fi

sleep 1

# Authentication services
if is_port_available 8004; then
    start_service_with_venv "auth-service-v2" 8004
else
    echo "⚠️  Port 8004 is already in use, skipping auth-service-v2"
fi

sleep 1

# CMS services
if is_port_available 8006; then
    start_service_with_venv "wagtail-cms" 8006 "manage.py" "runserver 0.0.0.0:8006"
else
    echo "⚠️  Port 8006 is already in use, skipping wagtail-cms"
fi

sleep 1

# Additional services
if is_port_available 8005; then
    start_service_with_venv "crm-service-v2" 8005
else
    echo "⚠️  Port 8005 is already in use, skipping crm-service-v2"
fi

sleep 1

if is_port_available 8007; then
    start_service_with_venv "marketing-automation-service" 8007
else
    echo "⚠️  Port 8007 is already in use, skipping marketing-automation-service"
fi

echo ""
echo "🎉 Service startup complete!"
echo ""
echo "📊 Service Status:"
echo "   - API Gateway:     http://localhost:8080"
echo "   - AI Agents:       http://localhost:8001"
echo "   - Business Dir:    http://localhost:8003"
echo "   - Auth Service:    http://localhost:8004"
echo "   - CRM Service:     http://localhost:8005"
echo "   - Wagtail CMS:     http://localhost:8006"
echo "   - Marketing Auto:  http://localhost:8007"
echo ""
echo "📁 Logs: ${LOG_DIR}/"
echo "🔧 Management:"
echo "   - View logs: tail -f ${LOG_DIR}/<service>.log"
echo "   - Stop all: scripts/stop-all-services.sh"
echo "   - Check status: scripts/check-service-status.sh"