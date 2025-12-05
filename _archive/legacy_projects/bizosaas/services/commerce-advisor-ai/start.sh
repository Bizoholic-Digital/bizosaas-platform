#!/bin/bash

# BizOSaaS Commerce Advisor AI [P11] - Quick Start Script
# Simple deployment script for immediate testing and development

echo "🚀 Starting BizOSaaS Commerce Advisor AI [P11]"
echo "=============================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import fastapi, uvicorn, pydantic" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing required dependencies..."
    python3 -m pip install fastapi uvicorn pydantic jinja2 --break-system-packages
fi

# Create templates directory if it doesn't exist
if [ ! -d "templates" ]; then
    echo "📁 Creating templates directory..."
    mkdir -p templates
fi

# Check if dashboard template exists
if [ ! -f "templates/dashboard.html" ]; then
    echo "⚠️  Dashboard template missing - service will run but dashboard may not display properly"
fi

echo "✅ Dependencies ready"
echo ""
echo "🎯 Starting Commerce Advisor AI service..."
echo "   Service: Commerce Advisor AI [P11]"
echo "   Port: 8030"
echo "   Dashboard: http://localhost:8030"
echo "   API Docs: http://localhost:8030/docs"
echo "   Health Check: http://localhost:8030/health"
echo ""
echo "Press Ctrl+C to stop the service"
echo ""

# Start the service
if [ -f "main_production.py" ]; then
    python3 main_production.py
elif [ -f "main_simple.py" ]; then
    python3 main_simple.py
elif [ -f "main.py" ]; then
    python3 main.py
else
    echo "❌ No main Python file found"
    exit 1
fi