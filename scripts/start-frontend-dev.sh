#!/bin/bash

# BizOSaaS Platform Frontend Development Startup Script
# Starts all three frontend applications with correct port allocation (PRD Compliant)

echo "🚀 Starting BizOSaaS Platform Frontend Development Environment"
echo "📋 Port Allocation (Current Reality):"
echo "   • Port 3000: Bizoholic Marketing Frontend (Digital Marketing Website)"  
echo "   • Port 3001: BizOSaaS Admin Dashboard (Multi-tenant Management)"
echo "   • Port 3002: CoreLDove E-commerce Frontend (E-commerce Platform)"
echo ""

# Check if node_modules exist
echo "🔍 Checking dependencies..."

# Function to install dependencies if needed
check_and_install() {
    local app_path=$1
    local app_name=$2
    
    if [ ! -d "$app_path/node_modules" ]; then
        echo "📦 Installing dependencies for $app_name..."
        cd "$app_path" && npm install
        cd - > /dev/null
    else
        echo "✅ Dependencies already installed for $app_name"
    fi
}

# Check dependencies for all apps
check_and_install "frontend/apps/bizoholic-frontend" "Bizoholic Marketing Frontend"  
check_and_install "frontend/apps/bizosaas-admin" "BizOSaaS Admin Dashboard"
check_and_install "frontend/apps/coreldove-frontend" "CoreLDove E-commerce Frontend"

echo ""
echo "🌐 Starting development servers..."

# Start all frontend applications in background
echo "📈 Starting Bizoholic Marketing Frontend (Port 3000)..."  
cd frontend/apps/bizoholic-frontend && npm run dev > ../../../logs/bizoholic-marketing.log 2>&1 &
BIZOHOLIC_PID=$!

echo "🔧 Starting BizOSaaS Admin Dashboard (Port 3001)..."
cd ../bizosaas-admin && npm run dev > ../../../logs/bizosaas-admin.log 2>&1 &
BIZOSAAS_ADMIN_PID=$!

echo "🛒 Starting CoreLDove E-commerce Frontend (Port 3002)..."
cd ../coreldove-frontend && npm run dev > ../../../logs/coreldove-ecommerce.log 2>&1 &
CORELDOVE_PID=$!

# Return to root directory
cd ../../..

# Create logs directory if it doesn't exist
mkdir -p logs

echo ""
echo "⏱️  Waiting for services to start..."
sleep 10

echo ""
echo "🎉 All frontend services started successfully!"
echo ""
echo "📱 Access your applications:"
echo "   📈 Bizoholic Marketing:         http://localhost:3000" 
echo "   🔧 BizOSaaS Admin Dashboard:    http://localhost:3001"
echo "   🛒 CoreLDove E-commerce:        http://localhost:3002"
echo ""
echo "📊 View logs:"
echo "   tail -f logs/bizosaas-admin.log"
echo "   tail -f logs/bizoholic-marketing.log"  
echo "   tail -f logs/coreldove-ecommerce.log"
echo ""
echo "🛑 To stop all services, run: ./scripts/stop-frontend-dev.sh"
echo "   Or press Ctrl+C to stop this script and kill background processes"

# Store PIDs for cleanup
echo "$BIZOSAAS_ADMIN_PID" > logs/bizosaas-admin.pid
echo "$BIZOHOLIC_PID" > logs/bizoholic-marketing.pid
echo "$CORELDOVE_PID" > logs/coreldove-ecommerce.pid

# Keep script running and handle Ctrl+C
cleanup() {
    echo ""
    echo "🛑 Stopping all frontend services..."
    kill $BIZOSAAS_ADMIN_PID 2>/dev/null || true
    kill $BIZOHOLIC_PID 2>/dev/null || true  
    kill $CORELDOVE_PID 2>/dev/null || true
    
    # Clean up PID files
    rm -f logs/*.pid
    
    echo "✅ All services stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for background processes
wait