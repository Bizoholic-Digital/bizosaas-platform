#!/bin/bash
# Stop all Bizoholic services

set -e

echo "🛑 Stopping Bizoholic Full Stack"
echo "================================="

# Stop Frontend
echo "Stopping frontend..."

# First try to stop using PID file
if [ -f /tmp/bizoholic-frontend.pid ]; then
    PID=$(cat /tmp/bizoholic-frontend.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "  Stopping frontend process tree (PID: $PID)..."
        # Kill all children first
        pkill -9 -P $PID 2>/dev/null || true
        # Then kill the parent
        kill -9 $PID 2>/dev/null || true
    fi
    rm /tmp/bizoholic-frontend.pid
fi

# Also kill any processes on port 3001 (including Next.js child processes)
if ss -tlnp 2>/dev/null | grep -q :3001; then
    echo "  Cleaning up processes on port 3001..."
    
    # Get all PIDs listening on port 3001
    PIDS=$(ss -tlnp 2>/dev/null | grep :3001 | grep -oP 'pid=\K[0-9]+' | sort -u)
    
    for PID in $PIDS; do
        if ps -p $PID > /dev/null 2>&1; then
            echo "    Killing process $PID and its children..."
            pkill -9 -P $PID 2>/dev/null || true
            kill -9 $PID 2>/dev/null || true
        fi
    done
    
    # Nuclear option if still running
    pkill -9 -f "next.*3001" 2>/dev/null || true
fi

# Clean up log file
if [ -f /tmp/bizoholic-frontend.log ]; then
    rm /tmp/bizoholic-frontend.log
fi

echo "✓ Frontend stopped"

# Stop Backend Services
echo "Stopping backend services..."
docker-compose -f shared/services/docker-compose.services.yml stop brain-gateway auth crm cms

# Stop Infrastructure (optional - comment out if you want to keep it running)
# echo "Stopping infrastructure..."
# docker-compose -f shared/infrastructure/docker-compose.infrastructure.yml stop postgres redis vault

echo "✓ Bizoholic services stopped"
echo ""
echo "Note: Infrastructure (Postgres, Redis, Vault) is still running."
echo "To stop infrastructure: docker-compose -f shared/infrastructure/docker-compose.infrastructure.yml stop"
