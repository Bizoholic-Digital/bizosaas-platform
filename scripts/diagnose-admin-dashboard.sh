#!/bin/bash
# Admin Dashboard Diagnostic Script
# Run this on your VPS to diagnose the 404 error

echo "=========================================="
echo "Admin Dashboard Diagnostic Report"
echo "=========================================="
echo ""

echo "1. Container Status:"
echo "-------------------"
docker ps -a | grep bizosaas-admin-dashboard
echo ""

echo "2. Container Health:"
echo "-------------------"
docker inspect bizosaas-admin-dashboard --format='{{.State.Health.Status}}'
echo ""

echo "3. Container Logs (Last 30 lines):"
echo "-----------------------------------"
docker logs bizosaas-admin-dashboard --tail 30
echo ""

echo "4. Health Check from Inside Container:"
echo "---------------------------------------"
docker exec bizosaas-admin-dashboard wget -qO- http://localhost:3004/api/health 2>&1 || echo "Health check failed"
echo ""

echo "5. Container Networks:"
echo "---------------------"
docker inspect bizosaas-admin-dashboard --format='{{range $key, $value := .NetworkSettings.Networks}}{{$key}}: {{$value.IPAddress}}{{"\n"}}{{end}}'
echo ""

echo "6. Container Port Bindings:"
echo "---------------------------"
docker port bizosaas-admin-dashboard
echo ""

echo "7. Traefik Logs (Admin Dashboard related):"
echo "-------------------------------------------"
docker logs traefik 2>&1 | grep -i admin | tail -20
echo ""

echo "8. Traefik Routers (via API):"
echo "-----------------------------"
curl -s http://localhost:8080/api/http/routers | jq '.[] | select(.name | contains("admin"))' 2>/dev/null || echo "Traefik API not accessible or jq not installed"
echo ""

echo "9. Test Direct Container Access:"
echo "--------------------------------"
CONTAINER_IP=$(docker inspect bizosaas-admin-dashboard --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' | head -1)
echo "Container IP: $CONTAINER_IP"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://$CONTAINER_IP:3004/api/health 2>&1 || echo "Direct access failed"
echo ""

echo "10. Environment Variables (Sensitive data masked):"
echo "---------------------------------------------------"
docker exec bizosaas-admin-dashboard env | grep -E "PORT|NODE_ENV|NEXTAUTH_URL" | sed 's/=.*/=***/'
echo ""

echo "11. Process Inside Container:"
echo "-----------------------------"
docker exec bizosaas-admin-dashboard ps aux | grep node
echo ""

echo "12. Check if Port 3004 is Listening Inside Container:"
echo "------------------------------------------------------"
docker exec bizosaas-admin-dashboard netstat -tlnp 2>/dev/null | grep 3004 || docker exec bizosaas-admin-dashboard ss -tlnp 2>/dev/null | grep 3004 || echo "netstat/ss not available"
echo ""

echo "=========================================="
echo "Diagnostic Complete"
echo "=========================================="
