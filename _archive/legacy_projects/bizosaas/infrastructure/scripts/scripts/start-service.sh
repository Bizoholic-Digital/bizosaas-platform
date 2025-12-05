#!/bin/bash

# Individual Service Startup Script with Virtual Environment
# Usage: bash scripts/start-service.sh <service-name> [port] [main-file]

set -e

SERVICES_DIR="/home/alagiri/projects/bizoholic/bizosaas/services"
VENV_BASE_DIR="${SERVICES_DIR}/.venvs"
LOG_DIR="/home/alagiri/projects/bizoholic/bizosaas/logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <service-name> [port] [main-file] [additional-args]"
    echo ""
    echo "Examples:"
    echo "  $0 ai-agents                    # Start ai-agents on default port with main.py"
    echo "  $0 ai-agents 8001               # Start ai-agents on port 8001"
    echo "  $0 wagtail-cms 8006 manage.py  # Start wagtail with Django management"
    echo ""
    echo "Available services:"
    if [[ -d "${VENV_BASE_DIR}" ]]; then
        ls -1 "${VENV_BASE_DIR}" 2>/dev/null | sed 's/^/  - /' || echo "  No virtual environments found"
    else
        echo "  No virtual environments found. Run setup-virtual-environments.sh first."
    fi
    exit 1
fi

SERVICE_NAME=$1
SERVICE_DIR="${SERVICES_DIR}/${SERVICE_NAME}"
VENV_DIR="${VENV_BASE_DIR}/${SERVICE_NAME}"
LOG_FILE="${LOG_DIR}/${SERVICE_NAME}.log"
PID_FILE="${LOG_DIR}/${SERVICE_NAME}.pid"

# Default values
DEFAULT_PORTS=(
    ["ai-agents"]=8001
    ["api-gateway"]=8080
    ["business-directory"]=8003
    ["auth-service-v2"]=8004
    ["crm-service-v2"]=8005
    ["wagtail-cms"]=8006
    ["marketing-automation-service"]=8007
)

PORT=${2:-${DEFAULT_PORTS[$SERVICE_NAME]}}
MAIN_FILE=${3:-"main.py"}
ADDITIONAL_ARGS=${4:-""}

# Create log directory
mkdir -p "${LOG_DIR}"

# Validation
if [[ ! -d "${SERVICE_DIR}" ]]; then
    print_status $RED "❌ Service directory not found: ${SERVICE_DIR}"
    exit 1
fi

if [[ ! -d "${VENV_DIR}" ]]; then
    print_status $RED "❌ Virtual environment not found for ${SERVICE_NAME}"
    print_status $YELLOW "   Run: bash scripts/setup-virtual-environments.sh"
    exit 1
fi

if [[ ! -f "${SERVICE_DIR}/${MAIN_FILE}" ]]; then
    print_status $RED "❌ Main file not found: ${SERVICE_DIR}/${MAIN_FILE}"
    exit 1
fi

# Check if service is already running
if [[ -f "${PID_FILE}" ]]; then
    OLD_PID=$(cat "${PID_FILE}")
    if ps -p "${OLD_PID}" > /dev/null 2>&1; then
        print_status $YELLOW "⚠️  Service ${SERVICE_NAME} is already running (PID: ${OLD_PID})"
        echo "   Stop it first with: kill ${OLD_PID}"
        exit 1
    else
        rm -f "${PID_FILE}"
    fi
fi

# Check if port is available
if [[ -n "${PORT}" ]] && lsof -Pi :${PORT} -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_status $YELLOW "⚠️  Port ${PORT} is already in use"
    EXISTING_PID=$(lsof -ti:${PORT} 2>/dev/null | head -1)
    echo "   Used by PID: ${EXISTING_PID}"
    exit 1
fi

print_status $BLUE "🚀 Starting ${SERVICE_NAME}..."
print_status $BLUE "   Service Dir: ${SERVICE_DIR}"
print_status $BLUE "   Virtual Env: ${VENV_DIR}"
print_status $BLUE "   Main File:   ${MAIN_FILE}"
print_status $BLUE "   Port:        ${PORT:-"default"}"
print_status $BLUE "   Log File:    ${LOG_FILE}"

# Change to service directory
cd "${SERVICE_DIR}"

# Activate virtual environment and start service
source "${VENV_DIR}/bin/activate"

# Special handling for different service types
case "${SERVICE_NAME}" in
    "wagtail-cms")
        if [[ "${MAIN_FILE}" == "manage.py" ]]; then
            print_status $BLUE "   Starting Django development server..."
            nohup python manage.py runserver "0.0.0.0:${PORT}" ${ADDITIONAL_ARGS} > "${LOG_FILE}" 2>&1 &
        else
            nohup python "${MAIN_FILE}" ${ADDITIONAL_ARGS} > "${LOG_FILE}" 2>&1 &
        fi
        ;;
    "ai-agents")
        # Check if uvicorn should be used
        if grep -q "uvicorn" "${SERVICE_DIR}/${MAIN_FILE}" 2>/dev/null; then
            nohup python "${MAIN_FILE}" ${ADDITIONAL_ARGS} > "${LOG_FILE}" 2>&1 &
        else
            nohup uvicorn main:app --host 0.0.0.0 --port "${PORT}" ${ADDITIONAL_ARGS} > "${LOG_FILE}" 2>&1 &
        fi
        ;;
    *)
        # Default FastAPI startup
        if [[ -f "${SERVICE_DIR}/main.py" ]] && grep -q "FastAPI\|app.*=.*FastAPI" "${SERVICE_DIR}/main.py" 2>/dev/null; then
            nohup uvicorn main:app --host 0.0.0.0 --port "${PORT}" ${ADDITIONAL_ARGS} > "${LOG_FILE}" 2>&1 &
        else
            nohup python "${MAIN_FILE}" ${ADDITIONAL_ARGS} > "${LOG_FILE}" 2>&1 &
        fi
        ;;
esac

SERVICE_PID=$!

# Save PID
echo "${SERVICE_PID}" > "${PID_FILE}"

deactivate

# Wait a moment and check if service started successfully
sleep 2

if ps -p "${SERVICE_PID}" > /dev/null 2>&1; then
    print_status $GREEN "✅ ${SERVICE_NAME} started successfully (PID: ${SERVICE_PID})"
    
    if [[ -n "${PORT}" ]]; then
        print_status $BLUE "🌐 Service available at: http://localhost:${PORT}"
        
        # Try to test endpoint after a moment
        sleep 2
        if curl -s -f "http://localhost:${PORT}/health" >/dev/null 2>&1 || \
           curl -s -f "http://localhost:${PORT}/" >/dev/null 2>&1 || \
           curl -s -f "http://localhost:${PORT}/docs" >/dev/null 2>&1; then
            print_status $GREEN "🎯 Service endpoint responding"
        else
            print_status $YELLOW "⚠️  Service started but endpoint not responding yet"
        fi
    fi
    
    print_status $BLUE "📋 Management:"
    echo "   View logs:    tail -f ${LOG_FILE}"
    echo "   Stop service: kill ${SERVICE_PID}"
    echo "   Check status: bash scripts/check-service-status.sh"
    
else
    print_status $RED "❌ ${SERVICE_NAME} failed to start"
    print_status $YELLOW "   Check logs: tail ${LOG_FILE}"
    rm -f "${PID_FILE}"
    exit 1
fi