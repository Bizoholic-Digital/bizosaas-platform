#!/bin/bash

echo "=== BizOSaaS Authentication Diagnostic ==="
echo ""

echo "1. Checking Client Portal (Port 3003)..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3003/login | grep -q "200"; then
    echo "   ✓ Client Portal is running"
else
    echo "   ✗ Client Portal is NOT responding"
fi

echo ""
echo "2. Checking Brain Gateway (Port 8001)..."
if curl -s -o /dev/null -w "%{http_code}" --max-time 3 http://localhost:8001/health | grep -q "200"; then
    echo "   ✓ Brain Gateway is running"
    echo "   Response: $(curl -s http://localhost:8001/health)"
else
    echo "   ✗ Brain Gateway is NOT responding"
    echo "   This is likely causing the 404 error!"
fi

echo ""
echo "3. Checking Auth Service (Port 8008)..."
if curl -s -o /dev/null -w "%{http_code}" --max-time 3 http://localhost:8008/health | grep -q "200"; then
    echo "   ✓ Auth Service is running"
    echo "   Response: $(curl -s http://localhost:8008/health | jq -c .)"
else
    echo "   ✗ Auth Service is NOT responding"
fi

echo ""
echo "4. Checking if ports are listening..."
echo "   Port 3003 (Client Portal): $(lsof -i :3003 2>/dev/null | grep LISTEN | wc -l) process(es)"
echo "   Port 8001 (Brain Gateway): $(lsof -i :8001 2>/dev/null | grep LISTEN | wc -l) process(es)"
echo "   Port 8008 (Auth Service):  $(lsof -i :8008 2>/dev/null | grep LISTEN | wc -l) process(es)"

echo ""
echo "=== Diagnosis Complete ==="
echo ""
echo "If Brain Gateway or Auth Service show 0 processes, you need to restart them."
echo "Run these commands in separate terminals:"
echo ""
echo "Terminal 1 (Auth Service):"
echo "  cd /home/alagiri/projects/bizosaas-platform"
echo "  export DATABASE_URL=\"postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas\""
echo "  export REDIS_URL=\"redis://localhost:6379/0\""
echo "  cd shared/services/auth && uvicorn main:app --host 0.0.0.0 --port 8008 --reload"
echo ""
echo "Terminal 2 (Brain Gateway):"
echo "  cd /home/alagiri/projects/bizosaas-platform/shared/services/brain-gateway"
echo "  uvicorn main:app --host 0.0.0.0 --port 8001 --reload"
