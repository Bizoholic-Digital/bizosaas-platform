#!/bin/bash

# Business Directory Service Startup Script
# Manages both the main API service and the enhanced web UI

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================"
echo "🏢 BizOSaaS Business Directory Service"
echo "======================================"
echo "Starting directory service components..."
echo ""

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "Port $port is already in use"
        return 0
    else
        echo "Port $port is available"
        return 1
    fi
}

# Function to start a service
start_service() {
    local name=$1
    local command=$2
    local port=$3
    
    echo "Starting $name on port $port..."
    
    if check_port $port; then
        echo "⚠️  $name already running on port $port"
    else
        echo "🚀 Launching $name..."
        eval "$command" &
        local pid=$!
        sleep 2
        
        if kill -0 $pid 2>/dev/null; then
            echo "✅ $name started successfully (PID: $pid)"
        else
            echo "❌ Failed to start $name"
        fi
    fi
    echo ""
}

# Start main directory service (API + HTML Dashboard)
start_service "Main Directory Service" \
    "python3 -c 'import directory_service; import uvicorn; uvicorn.run(directory_service.app, host=\"0.0.0.0\", port=8003)'" \
    8003

# Start enhanced web UI
start_service "Enhanced Web Interface" \
    "python3 directory_web_ui.py" \
    8004

echo "======================================"
echo "📊 Service Status Summary"
echo "======================================"

# Test services
echo "Testing services..."
echo ""

# Test main service
if curl -s http://localhost:8003/health >/dev/null 2>&1; then
    echo "✅ Main API Service (port 8003): HEALTHY"
    echo "   📍 http://localhost:8003/"
    echo "   📄 http://localhost:8003/directories"
    echo "   📚 http://localhost:8003/docs"
else
    echo "❌ Main API Service (port 8003): NOT RESPONDING"
fi

# Test web UI
if curl -s http://localhost:8004/ >/dev/null 2>&1; then
    echo "✅ Enhanced Web UI (port 8004): HEALTHY"
    echo "   🎨 http://localhost:8004/"
else
    echo "❌ Enhanced Web UI (port 8004): NOT RESPONDING"
fi

echo ""
echo "======================================"
echo "🎯 Quick Access"
echo "======================================"
echo "Main Dashboard:     http://localhost:8003/"
echo "Enhanced Interface: http://localhost:8004/"
echo "JSON API:          http://localhost:8003/directories"
echo "API Documentation: http://localhost:8003/docs"
echo ""
echo "📋 To test all endpoints:"
echo "   python3 test_directory_service.py"
echo ""
echo "🛑 To stop services:"
echo "   pkill -f directory_service"
echo "   pkill -f directory_web_ui"
echo "======================================"