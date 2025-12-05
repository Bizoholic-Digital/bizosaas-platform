#!/bin/bash

# Stop All Services Script
# Gracefully stops all running BizOSaaS services

SERVICES_DIR="/home/alagiri/projects/bizoholic/bizosaas/services"
LOG_DIR="/home/alagiri/projects/bizoholic/bizosaas/logs"

echo "🛑 Stopping all BizOSaaS services..."

# Function to stop service by PID file
stop_service_by_pid() {
    local service_name=$1
    local pid_file="${LOG_DIR}/${service_name}.pid"
    
    if [[ -f "${pid_file}" ]]; then
        local pid=$(cat "${pid_file}")
        if ps -p "${pid}" > /dev/null 2>&1; then
            echo "🔄 Stopping ${service_name} (PID: ${pid})"
            kill -TERM "${pid}"
            sleep 2
            
            # Force kill if still running
            if ps -p "${pid}" > /dev/null 2>&1; then
                echo "⚡ Force killing ${service_name} (PID: ${pid})"
                kill -KILL "${pid}"
            fi
            
            echo "✅ ${service_name} stopped"
        fi
        rm -f "${pid_file}"
    fi
}

# Stop services by PID files if they exist
if [[ -d "${LOG_DIR}" ]]; then
    for pid_file in "${LOG_DIR}"/*.pid; do
        if [[ -f "${pid_file}" ]]; then
            service_name=$(basename "${pid_file}" .pid)
            stop_service_by_pid "${service_name}"
        fi
    done
fi

# Stop services by port (fallback method)
echo "🔍 Checking for remaining services on known ports..."

PORTS=(8001 8003 8004 8005 8006 8007 8080)

for port in "${PORTS[@]}"; do
    pids=$(lsof -ti:${port} 2>/dev/null || true)
    if [[ -n "${pids}" ]]; then
        echo "🔄 Stopping services on port ${port}"
        echo "${pids}" | xargs -r kill -TERM
        sleep 1
        
        # Force kill if still running
        pids=$(lsof -ti:${port} 2>/dev/null || true)
        if [[ -n "${pids}" ]]; then
            echo "⚡ Force killing services on port ${port}"
            echo "${pids}" | xargs -r kill -KILL
        fi
    fi
done

# Stop any remaining python processes related to our services
echo "🧹 Cleaning up remaining service processes..."
pkill -f "python.*main\.py" 2>/dev/null || true
pkill -f "uvicorn.*main:" 2>/dev/null || true

echo ""
echo "✅ All services stopped"
echo "📁 Log files preserved in: ${LOG_DIR}/"