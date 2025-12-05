#!/bin/bash

# BizOSaaS Platform - Current Setup Analysis Script
# Analyzes existing containers and port allocation

echo "🔍 BizOSaaS Platform - Current Setup Analysis"
echo "=============================================="

echo ""
echo "🐳 Currently Running Containers:"
echo "================================"
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}"

echo ""
echo "📊 Port Allocation Analysis:"
echo "============================"

# Check port 3000
echo -n "Port 3000: "
if docker ps | grep -q "3000->"; then
    CONTAINER_3000=$(docker ps --format "{{.Names}}: {{.Image}}" | grep $(docker ps | grep "3000->" | awk '{print $1}'))
    echo "🔴 OCCUPIED by $CONTAINER_3000 (should be BizOSaaS Admin)"
else
    echo "✅ AVAILABLE for BizOSaaS Admin"
fi

# Check port 3001  
echo -n "Port 3001: "
if docker ps | grep -q "3001->"; then
    CONTAINER_3001=$(docker ps --format "{{.Names}}: {{.Image}}" | grep $(docker ps | grep "3001->" | awk '{print $1}'))
    echo "🔴 OCCUPIED by $CONTAINER_3001 (should be Bizoholic Marketing)"
else
    echo "✅ AVAILABLE for Bizoholic Marketing"
fi

# Check port 3002
echo -n "Port 3002: "
if docker ps | grep -q "3002->"; then
    CONTAINER_3002=$(docker ps --format "{{.Names}}: {{.Image}}" | grep $(docker ps | grep "3002->" | awk '{print $1}'))
    echo "✅ CORRECT: $CONTAINER_3002 (CoreLDove E-commerce)"
else
    echo "❌ MISSING: CoreLDove E-commerce should be here"
fi

echo ""
echo "🔧 Backend Services Status:"
echo "==========================="

# Check essential backend services
SERVICES=(
    "8001:FastAPI Brain Gateway"
    "8007:Auth Service v2" 
    "8006:Wagtail CMS"
    "8010:Saleor Backend"
    "8088:Apache Superset"
    "5432:PostgreSQL Database"
    "6379:Redis Cache"
)

for service in "${SERVICES[@]}"; do
    PORT=$(echo $service | cut -d: -f1)
    NAME=$(echo $service | cut -d: -f2)
    
    echo -n "Port $PORT ($NAME): "
    if docker ps | grep -q "$PORT->"; then
        CONTAINER=$(docker ps | grep "$PORT->" | awk '{print $1}' | head -1)
        CONTAINER_NAME=$(docker ps --format "{{.Names}}" | grep $CONTAINER)
        echo "✅ RUNNING ($CONTAINER_NAME)"
    else
        echo "❌ MISSING"
    fi
done

echo ""
echo "🎯 Required Actions:"
echo "==================="

# Determine what needs to be done
WRONG_PORT_3000=$(docker ps | grep "3000->" | awk '{print $1}')
WRONG_PORT_3001=$(docker ps | grep "3001->" | awk '{print $1}')

if [ ! -z "$WRONG_PORT_3000" ]; then
    CONTAINER_NAME=$(docker inspect --format='{{.Name}}' $WRONG_PORT_3000 | sed 's/\///')
    if [ "$CONTAINER_NAME" != "bizosaas-admin-3000" ]; then
        echo "🔄 Need to move container on port 3000 to correct port"
    fi
fi

if [ ! -z "$WRONG_PORT_3001" ]; then
    CONTAINER_NAME=$(docker inspect --format='{{.Name}}' $WRONG_PORT_3001 | sed 's/\///')
    if [ "$CONTAINER_NAME" != "bizoholic-marketing-3001" ]; then
        echo "🔄 Need to move TailAdmin v2 from port 3001 to port 3000"
    fi
fi

# Check for missing backend services
if ! docker ps | grep -q "8001->"; then
    echo "🆕 Need to start FastAPI Brain Gateway (port 8001)"
fi

if ! docker ps | grep -q "8007->"; then
    echo "🆕 Need to start Auth Service v2 (port 8007)"
fi

if ! docker ps | grep -q "8088->"; then
    echo "🆕 Need to start Apache Superset (port 8088)"
fi

if ! docker ps | grep -q "8010->"; then
    echo "🆕 Need to start Saleor Backend (port 8010)"
fi

echo ""
echo "💡 Recommendations:"
echo "=================="
echo "1. Run './migrate-to-correct-ports.sh' to fix port allocation"
echo "2. This will ensure:"
echo "   - Port 3000: BizOSaaS Admin (TailAdmin v2)"
echo "   - Port 3001: Bizoholic Marketing"
echo "   - Port 3002: CoreLDove E-commerce"
echo "   - All backend services are running"

echo ""
echo "🌐 Target URLs after migration:"
echo "==============================="
echo "🔧 BizOSaaS Admin Dashboard: http://localhost:3000"
echo "📈 Bizoholic Marketing: http://localhost:3001"
echo "🛒 CoreLDove E-commerce: http://localhost:3002"

echo ""
echo "📋 To proceed with migration: ./migrate-to-correct-ports.sh"