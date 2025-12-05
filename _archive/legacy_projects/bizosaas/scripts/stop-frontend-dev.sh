#!/bin/bash

# BizOSaaS Platform Frontend Development Stop Script

echo "🛑 Stopping BizOSaaS Platform Frontend Development Environment"

# Function to kill process by PID file
kill_by_pid_file() {
    local pid_file=$1
    local service_name=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            echo "🔴 Stopping $service_name (PID: $pid)..."
            kill "$pid" 2>/dev/null || true
            sleep 2
            # Force kill if still running
            kill -9 "$pid" 2>/dev/null || true
        else
            echo "⚠️  $service_name was not running"
        fi
        rm -f "$pid_file"
    else
        echo "⚠️  No PID file found for $service_name"
    fi
}

# Kill services using PID files
kill_by_pid_file "logs/bizoholic-marketing.pid" "Bizoholic Marketing Frontend"
kill_by_pid_file "logs/bizosaas-admin.pid" "BizOSaaS Admin Dashboard"
kill_by_pid_file "logs/coreldove-ecommerce.pid" "CoreLDove E-commerce Frontend"

# Alternative: kill by port (fallback)
echo "🔍 Checking for any remaining processes on frontend ports..."

# Function to kill process by port
kill_by_port() {
    local port=$1
    local service_name=$2
    
    local pid=$(lsof -ti:$port 2>/dev/null || true)
    if [ -n "$pid" ]; then
        echo "🔴 Found $service_name process on port $port (PID: $pid), killing..."
        kill -9 "$pid" 2>/dev/null || true
    fi
}

kill_by_port 3000 "Bizoholic Marketing Frontend"
kill_by_port 3001 "BizOSaaS Admin Dashboard"
kill_by_port 3002 "CoreLDove E-commerce Frontend"

# Clean up log files (optional)
echo "🧹 Cleaning up..."
rm -f logs/*.pid

echo ""
echo "✅ All frontend services stopped successfully!"
echo "🚀 To restart, run: ./scripts/start-frontend-dev.sh"