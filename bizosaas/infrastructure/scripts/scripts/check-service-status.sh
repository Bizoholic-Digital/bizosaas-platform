#!/bin/bash

# Service Status Check Script
# Displays the status of all BizOSaaS services

SERVICES_DIR="/home/alagiri/projects/bizoholic/bizosaas/services"
LOG_DIR="/home/alagiri/projects/bizoholic/bizosaas/logs"
VENV_BASE_DIR="${SERVICES_DIR}/.venvs"

echo "📊 BizOSaaS Service Status Report"
echo "=================================="
echo ""

# Function to check service status
check_service_status() {
    local service_name=$1
    local port=$2
    local pid_file="${LOG_DIR}/${service_name}.pid"
    
    printf "%-20s " "${service_name}:"
    
    # Check if PID file exists and process is running
    if [[ -f "${pid_file}" ]]; then
        local pid=$(cat "${pid_file}")
        if ps -p "${pid}" > /dev/null 2>&1; then
            # Check if port is being used
            if lsof -Pi :${port} -sTCP:LISTEN -t >/dev/null 2>&1; then
                echo "✅ RUNNING (PID: ${pid}, Port: ${port})"
            else
                echo "⚠️  PROCESS RUNNING (PID: ${pid}) but port ${port} not listening"
            fi
        else
            echo "❌ STOPPED (stale PID file)"
            rm -f "${pid_file}"
        fi
    else
        # Check if something is running on the port
        if lsof -Pi :${port} -sTCP:LISTEN -t >/dev/null 2>&1; then
            local port_pid=$(lsof -ti:${port} 2>/dev/null | head -1)
            echo "⚠️  PORT ${port} IN USE (PID: ${port_pid}) - not managed by script"
        else
            echo "❌ STOPPED"
        fi
    fi
}

# Function to check virtual environment status
check_venv_status() {
    local service_name=$1
    local venv_dir="${VENV_BASE_DIR}/${service_name}"
    
    printf "%-20s " "${service_name} (venv):"
    
    if [[ -d "${venv_dir}" ]]; then
        echo "✅ READY"
    else
        echo "❌ MISSING - run setup-virtual-environments.sh"
    fi
}

echo "🐍 Virtual Environment Status:"
echo "------------------------------"
SERVICES=("ai-agents" "api-gateway" "auth-service-v2" "business-directory" "wagtail-cms" "crm-service-v2" "marketing-automation-service")

for service in "${SERVICES[@]}"; do
    check_venv_status "${service}"
done

echo ""
echo "🚀 Service Status:"
echo "------------------"
check_service_status "api-gateway" 8080
check_service_status "ai-agents" 8001
check_service_status "business-directory" 8003
check_service_status "auth-service-v2" 8004
check_service_status "crm-service-v2" 8005
check_service_status "wagtail-cms" 8006
check_service_status "marketing-automation-service" 8007

echo ""
echo "📈 System Resources:"
echo "--------------------"
echo "Memory usage: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
echo "CPU load: $(uptime | awk -F'load average:' '{print $2}')"

echo ""
echo "📁 Log Files:"
echo "-------------"
if [[ -d "${LOG_DIR}" ]] && [[ "$(ls -A ${LOG_DIR})" ]]; then
    for log_file in "${LOG_DIR}"/*.log; do
        if [[ -f "${log_file}" ]]; then
            local service_name=$(basename "${log_file}" .log)
            local file_size=$(du -h "${log_file}" | cut -f1)
            local last_modified=$(stat -c %y "${log_file}" | cut -d' ' -f1,2 | cut -d'.' -f1)
            printf "%-20s %s (%s)\n" "${service_name}:" "${file_size}" "${last_modified}"
        fi
    done
else
    echo "No log files found"
fi

echo ""
echo "🔧 Management Commands:"
echo "-----------------------"
echo "Start all:    bash scripts/start-services-with-venv.sh"
echo "Stop all:     bash scripts/stop-all-services.sh"
echo "Setup venvs:  bash scripts/setup-virtual-environments.sh"
echo "Activate:     source scripts/activate-venv.sh <service-name>"