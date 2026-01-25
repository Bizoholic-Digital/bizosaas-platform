#!/bin/bash
# Check if portals are actually running and listening

echo "🔍 Checking container status..."
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "portal|admin"

echo -e "\n🔍 Checking Client Portal (internal)..."
IP_CLIENT=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' client-portal)
if [ -n "$IP_CLIENT" ]; then
    echo "Client Portal IP: $IP_CLIENT"
    wget -qO- --timeout=2 http://$IP_CLIENT:3003/login | head -n 5
else
    echo "Client Portal container not found or no IP."
fi

echo -e "\n🔍 Checking Admin Portal (internal)..."
# Try both possible names
IP_ADMIN=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' admin-dashboard 2>/dev/null)
if [ -z "$IP_ADMIN" ]; then
    IP_ADMIN=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' bizosaas-admin-dashboard 2>/dev/null)
fi

if [ -n "$IP_ADMIN" ]; then
    echo "Admin Portal IP: $IP_ADMIN"
    wget -qO- --timeout=2 http://$IP_ADMIN:3004/login | head -n 5
else
    echo "Admin Portal container not found or no IP."
fi
