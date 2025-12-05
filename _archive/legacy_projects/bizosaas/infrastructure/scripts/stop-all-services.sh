#!/bin/bash

# BizOSaaS Stop All Services Script
echo "🛑 Stopping BizOSaaS Platform Services..."

# List of ports used by services
PORTS=(3000 3001 8081 8002 8003 8004 8005 8008 8009)

for port in "${PORTS[@]}"; do
    echo "🔍 Checking port $port..."
    
    # Find process using the port
    PID=$(lsof -ti:$port 2>/dev/null)
    
    if [ ! -z "$PID" ]; then
        echo "🔥 Killing process $PID on port $port"
        kill -9 $PID 2>/dev/null
        sleep 1
    else
        echo "✅ Port $port is already free"
    fi
done

echo ""
echo "🧹 Cleaning up log files..."
rm -f /tmp/bizoholic-frontend.log
rm -f /tmp/coreldove-frontend.log
rm -f /tmp/api-gateway.log
rm -f /tmp/ai-agents.log
rm -f /tmp/business-directory.log
rm -f /tmp/payment-service.log
rm -f /tmp/wagtail-cms.log
rm -f /tmp/marketing-apis.log
rm -f /tmp/amazon-integration.log

echo "✅ All services stopped and logs cleaned up!"