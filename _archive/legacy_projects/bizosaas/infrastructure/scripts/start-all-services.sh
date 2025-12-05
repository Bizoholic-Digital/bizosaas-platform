#!/bin/bash

# BizOSaaS Local Development Startup Script
echo "🚀 Starting BizOSaaS Platform Services..."

# Check if virtual environment exists
if [ ! -d "/home/alagiri/claude_workspace/venv" ]; then
    echo "❌ Virtual environment not found. Please create it first."
    exit 1
fi

# Activate virtual environment
source /home/alagiri/claude_workspace/venv/bin/activate

# Function to start service in background
start_service() {
    local service_name=$1
    local service_path=$2
    local service_port=$3
    local service_script=$4
    
    echo "🔄 Starting $service_name on port $service_port..."
    
    cd "$service_path"
    
    # Kill existing process on port if any
    lsof -ti:$service_port | xargs kill -9 2>/dev/null || true
    
    # Start the service
    if [ "$service_script" = "npm" ]; then
        npm run dev > "/tmp/${service_name}.log" 2>&1 &
    else
        python "$service_script" > "/tmp/${service_name}.log" 2>&1 &
    fi
    
    local pid=$!
    echo "✅ $service_name started (PID: $pid) - logs: /tmp/${service_name}.log"
    sleep 2
}

# Start all services
echo "📂 Current directory: $(pwd)"

# Frontend Services
start_service "bizoholic-frontend" "/home/alagiri/projects/bizoholic/bizosaas/frontend" 3000 "npm"
start_service "coreldove-frontend" "/home/alagiri/projects/bizoholic/bizosaas/services/coreldove-frontend" 3003 "npm"

# Backend Services
start_service "api-gateway" "/home/alagiri/projects/bizoholic/bizosaas/services/api-gateway" 8081 "main.py"
start_service "ai-agents" "/home/alagiri/projects/bizoholic/bizosaas/services/ai-agents" 8002 "simple_main.py"
start_service "business-directory" "/home/alagiri/projects/bizoholic/bizosaas/services/business-directory" 8003 "directory_service.py"
start_service "payment-service" "/home/alagiri/projects/bizoholic/bizosaas/services/payment-service" 8004 "main.py"
start_service "wagtail-cms" "/home/alagiri/projects/bizoholic/bizosaas/services/wagtail-cms" 8005 "manage.py runserver 0.0.0.0:8005"
start_service "marketing-apis" "/home/alagiri/projects/bizoholic/bizosaas/services/marketing-apis-service" 8008 "main.py"
start_service "amazon-integration" "/home/alagiri/projects/bizoholic/bizosaas/services/amazon-integration-service" 8009 "main.py"

echo ""
echo "🎉 All services started successfully!"
echo ""
echo "📊 Service Access URLs:"
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ FRONTEND SERVICES                                           │"
echo "├─────────────────────────────────────────────────────────────┤"
echo "│ 🌐 Bizoholic Frontend    → http://localhost:3000            │"
echo "│ 🌐 CoreLDove Frontend    → http://localhost:3003            │"
echo "├─────────────────────────────────────────────────────────────┤"
echo "│ BACKEND API SERVICES                                        │"
echo "├─────────────────────────────────────────────────────────────┤"
echo "│ 🔌 API Gateway           → http://localhost:8081            │"
echo "│ 🤖 AI Agents             → http://localhost:8002            │"
echo "│ 📁 Business Directory    → http://localhost:8003            │"
echo "│ 💳 Payment Service       → http://localhost:8004            │"
echo "│ 📝 Wagtail CMS           → http://localhost:8005            │"
echo "│ 📢 Marketing APIs        → http://localhost:8008            │"
echo "│ 🛒 Amazon Integration    → http://localhost:8009            │"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""
echo "🔍 Health Check Commands:"
echo "curl http://localhost:8081/health  # API Gateway"
echo "curl http://localhost:8004/health  # Payment Service"
echo "curl http://localhost:8008/health  # Marketing APIs"
echo "curl http://localhost:8009/health  # Amazon Integration"
echo ""
echo "📋 View Logs:"
echo "tail -f /tmp/SERVICE-NAME.log"
echo ""
echo "🛑 Stop All Services:"
echo "./stop-all-services.sh"
# Claude Telegram Bot
start_service "claude-telegram-bot" "/home/alagiri/projects/bizoholic/bizosaas/services/claude-telegram-bot" 8010 "main.py"
