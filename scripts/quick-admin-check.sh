#!/bin/bash
# Quick VPS Diagnostic - Run this on your VPS via SSH

echo "=== ADMIN DASHBOARD QUICK DIAGNOSTIC ==="
echo ""

echo "1. Container Status:"
docker ps -a | grep bizosaas-admin-dashboard
echo ""

echo "2. Container Logs (last 20 lines):"
docker logs bizosaas-admin-dashboard --tail 20
echo ""

echo "3. Health Check from Inside Container:"
docker exec bizosaas-admin-dashboard wget -qO- http://localhost:3004/api/health 2>&1 || echo "FAILED"
echo ""

echo "4. Container Networks:"
docker inspect bizosaas-admin-dashboard --format='{{range $key, $value := .NetworkSettings.Networks}}{{$key}}{{"\n"}}{{end}}'
echo ""

echo "5. Check if process is running inside container:"
docker exec bizosaas-admin-dashboard ps aux | grep node || echo "No node process found!"
echo ""

echo "=== END DIAGNOSTIC ==="
