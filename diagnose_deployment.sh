#!/bin/bash

echo "=== Checking Postiz Container Logs ==="
docker logs postiz-app-modular 2>&1 | tail -100

echo ""
echo "=== Checking Latest Core-Stack Deployment Log ==="
cat /etc/dokploy/logs/compose-compress-wireless-alarm-sot3ld/compose-compress-wireless-alarm-sot3ld-2026-02-17:14:23:26.log 2>&1 | tail -100

echo ""
echo "=== Checking Latest Postiz-Stack Deployment Log ==="
cat /etc/dokploy/logs/compose-generate-haptic-transmitter-pltjdr/compose-generate-haptic-transmitter-pltjdr-2026-02-17:14:19:59.log 2>&1 | tail -100

echo ""
echo "=== Checking for any modular containers (running or stopped) ==="
docker ps -a | grep -E "(modular|brain-gateway|ai-agents)"

echo ""
echo "=== Checking Docker networks ==="
docker network ls | grep dokploy
