#!/bin/bash
# BizOSaaS Platform - Start All Services with Virtual Environment
set -e

echo "🚀 Starting BizOSaaS Platform Services..."
echo "Virtual Environment: $VIRTUAL_ENV"

# Kill any existing processes
echo "🔄 Stopping existing services..."
pkill -f "python.*main.py" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true

# Wait for cleanup
sleep 2

echo "📦 Starting core services..."

# Start Event Bus Service
echo "🔗 Starting Event Bus Service (Port 8009)..."
cd /home/alagiri/projects/bizoholic/bizosaas/services/event-bus
python main.py > /tmp/event_bus.log 2>&1 &
echo "Event Bus PID: $!"

# Start Domain Repository Service  
echo "🗃️  Starting Domain Repository Service (Port 8011)..."
cd /home/alagiri/projects/bizoholic/bizosaas/services/domain-repository
python main.py > /tmp/domain_repo.log 2>&1 &
echo "Domain Repository PID: $!"

# Start API Gateway
echo "🌐 Starting API Gateway (Port 8080)..."
cd /home/alagiri/projects/bizoholic/bizosaas/services/api-gateway
python main_enhanced.py > /tmp/api_gateway.log 2>&1 &
echo "API Gateway PID: $!"

# Start AI Agents Service
echo "🤖 Starting AI Agents Service (Port 8001)..."
cd /home/alagiri/projects/bizoholic/bizosaas/services/ai-agents
python main.py > /tmp/ai_agents.log 2>&1 &
echo "AI Agents PID: $!"

echo "⏳ Waiting for services to start..."
sleep 10

echo "🔍 Testing service connectivity..."
python /home/alagiri/projects/bizoholic/bizosaas/test_platform_connectivity.py

echo "✅ Service startup complete!"
echo "📊 Service Logs:"
echo "  Event Bus: tail -f /tmp/event_bus.log"
echo "  Domain Repository: tail -f /tmp/domain_repo.log"  
echo "  API Gateway: tail -f /tmp/api_gateway.log"
echo "  AI Agents: tail -f /tmp/ai_agents.log"