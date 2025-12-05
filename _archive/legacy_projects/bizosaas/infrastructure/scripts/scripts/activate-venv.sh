#!/bin/bash

# Virtual Environment Activation Script
# Usage: source scripts/activate-venv.sh <service-name>

SERVICES_DIR="/home/alagiri/projects/bizoholic/bizosaas/services"
VENV_BASE_DIR="${SERVICES_DIR}/.venvs"

if [[ $# -eq 0 ]]; then
    echo "Usage: source scripts/activate-venv.sh <service-name>"
    echo ""
    echo "Available services:"
    if [[ -d "${VENV_BASE_DIR}" ]]; then
        ls -1 "${VENV_BASE_DIR}" | sed 's/^/  - /'
    else
        echo "  No virtual environments found. Run scripts/setup-virtual-environments.sh first."
    fi
    return 1 2>/dev/null || exit 1
fi

SERVICE_NAME=$1
VENV_DIR="${VENV_BASE_DIR}/${SERVICE_NAME}"

if [[ ! -d "${VENV_DIR}" ]]; then
    echo "❌ Virtual environment not found for service: ${SERVICE_NAME}"
    echo "Run: bash scripts/setup-virtual-environments.sh"
    return 1 2>/dev/null || exit 1
fi

# Deactivate current environment if any
if [[ -n "${VIRTUAL_ENV}" ]]; then
    deactivate
fi

# Activate the service environment
source "${VENV_DIR}/bin/activate"
echo "🐍 Activated virtual environment for ${SERVICE_NAME}"
echo "📁 Environment: ${VENV_DIR}"
echo "🐍 Python: $(which python)"
echo "📦 Pip: $(which pip)"