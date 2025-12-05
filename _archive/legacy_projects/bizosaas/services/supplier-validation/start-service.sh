#!/bin/bash

# Quick start script for Supplier Validation Workflow [P9]
# This script sets up and starts the service for testing

set -e

echo "🚀 Starting Supplier Validation Workflow [P9]"
echo "============================================="

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run from service directory."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads logs templates static/css static/js

# Set up environment if not exists
if [ ! -f ".env" ]; then
    echo "📋 Setting up environment..."
    cp .env.example .env
    echo "⚠️  Please update .env file with your configuration"
fi

# Install Python dependencies (if not using Docker)
if command -v python3 &> /dev/null; then
    echo "🐍 Installing Python dependencies..."
    pip3 install -r requirements.txt 2>/dev/null || echo "Install requirements manually if needed"
fi

# Start with Docker if available
if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
    echo "🐳 Starting with Docker..."
    
    # Check if docker-compose or docker compose
    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
    else
        COMPOSE_CMD="docker compose"
    fi
    
    # Start services
    $COMPOSE_CMD up -d
    
    echo "⏳ Waiting for services to start..."
    sleep 10
    
    # Check health
    echo "🔍 Checking service health..."
    for i in {1..30}; do
        if curl -f http://localhost:8027/health &> /dev/null; then
            echo "✅ Service is healthy!"
            break
        fi
        if [ $i -eq 30 ]; then
            echo "❌ Service failed to start"
            exit 1
        fi
        sleep 2
    done
    
else
    echo "🚀 Starting with Python directly..."
    
    # Set basic environment
    export DATABASE_URL="sqlite:///supplier_validation.db"
    export REDIS_URL="redis://localhost:6379"
    export BRAIN_API_URL="http://localhost:8001"
    
    # Start the service
    python3 main.py &
    SERVICE_PID=$!
    
    echo "⏳ Waiting for service to start..."
    sleep 5
    
    # Check health
    if curl -f http://localhost:8027/health &> /dev/null; then
        echo "✅ Service started successfully!"
        echo "📝 Service PID: $SERVICE_PID"
    else
        echo "❌ Service failed to start"
        kill $SERVICE_PID 2>/dev/null || true
        exit 1
    fi
fi

echo ""
echo "🎉 Supplier Validation Workflow [P9] is ready!"
echo "============================================="
echo "📊 Dashboard: http://localhost:8027/dashboard"
echo "📚 API Docs: http://localhost:8027/docs"
echo "❤️  Health: http://localhost:8027/health"
echo ""
echo "🔧 Management commands:"
echo "  View logs: docker-compose logs -f (or check logs/ directory)"
echo "  Stop: docker-compose down (or kill process)"
echo ""
echo "🧪 Run tests: python3 test_supplier_validation.py"