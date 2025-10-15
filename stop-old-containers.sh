#!/bin/bash
# Stop old containers that conflict with staging deployment

echo "=========================================="
echo "Stopping Old Containers Blocking Staging"
echo "=========================================="
echo ""

# List of containers to stop
CONTAINERS=(
  "bizosaas-brain-unified"
  "bizosaas-django-crm-8003"
  "bizosaas-business-directory-backend-8004"
  "coreldove-backend-8005"
  "bizosaas-temporal-unified"
  "business-directory-3004"
)

for container in "${CONTAINERS[@]}"; do
  if docker ps --format "{{.Names}}" | grep -q "^${container}$"; then
    echo "Stopping: $container"
    docker stop "$container"
  else
    echo "Not running: $container"
  fi
done

echo ""
echo "=========================================="
echo "Checking ports are now free..."
echo "=========================================="

for port in 8001 8003 8004 8005 8009 3004; do
  if nc -zv 127.0.0.1 $port 2>&1 | grep -q succeeded; then
    echo "⚠️  Port $port still in use!"
  else
    echo "✓ Port $port is free"
  fi
done

echo ""
echo "=========================================="
echo "Old containers stopped"
echo "Now you can redeploy in Dokploy UI"
echo "=========================================="
