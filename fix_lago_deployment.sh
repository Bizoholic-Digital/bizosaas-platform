#!/bin/bash

echo "=== Lago Deployment Diagnostic & Fix Script ==="
echo ""

echo "Step 1: Checking logs of failing containers..."
echo "--- lago-api logs (last 50 lines) ---"
docker logs --tail 50 bizosaasbraingateway-lagobilling-g0n3if-lago-api-1 2>&1
echo ""
echo "--- lago-worker logs (last 50 lines) ---"
docker logs --tail 50 bizosaasbraingateway-lagobilling-g0n3if-lago-worker-1 2>&1
echo ""

echo "Step 2: Stopping and removing old conflicting containers..."
docker stop lago-api lago-front lago-worker lago-db lago-redis 2>/dev/null
docker rm lago-api lago-front lago-worker lago-db lago-redis 2>/dev/null
echo "Old containers cleaned up."
echo ""

echo "Step 3: Checking if new containers are still restarting..."
docker ps | grep "bizosaasbraingateway-lagobilling-g0n3if"
echo ""

echo "=== Next Steps ==="
echo "1. Review the logs above to identify the error"
echo "2. If you see database connection errors, redeploy via Dokploy UI to pick up latest .env.lago changes"
echo "3. If you see RSA key errors, the key format needs adjustment"
echo ""
