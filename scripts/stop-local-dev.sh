#!/bin/bash

echo "🛑 Stopping BizOSaaS Local Development Services..."

# Stop all Node.js dev servers
for pid_file in /tmp/bizosaas-*.pid; do
    if [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        service_name=$(basename "$pid_file" .pid)
        echo "Stopping $service_name (PID: $pid)..."
        kill $pid 2>/dev/null || true
        rm "$pid_file"
    fi
done

# Stop infrastructure
echo "Stopping infrastructure containers..."
docker compose -f shared/infrastructure/docker-compose.infrastructure.yml down

echo "✅ All local development services stopped."
