#!/bin/bash

# Business Directory Frontend Startup Script
# This script sets up and starts the Next.js frontend application

set -e

echo "🚀 Starting BizBook Business Directory Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ to continue."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current version: $(node --version)"
    exit 1
fi

# Change to frontend directory
cd "$(dirname "$0")"

echo "📍 Working directory: $(pwd)"

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found. Make sure you're in the frontend directory."
    exit 1
fi

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "📝 Creating .env.local from .env.example..."
    cp .env.example .env.local
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
else
    echo "✅ Dependencies already installed"
fi

# Check if backend is running
echo "🔍 Checking if backend API is running..."
BACKEND_URL="http://localhost:8000"
if curl -s "$BACKEND_URL/api/status" > /dev/null 2>&1; then
    echo "✅ Backend API is running at $BACKEND_URL"
else
    echo "⚠️  Warning: Backend API is not responding at $BACKEND_URL"
    echo "   Please make sure the FastAPI backend is running on port 8000"
    echo "   You can start it with: python directory_service.py"
    echo ""
    echo "   Continuing with frontend startup..."
fi

# Build the application (optional, for production readiness check)
if [ "$1" = "--build" ]; then
    echo "🏗️  Building application..."
    npm run build
    echo "✅ Build completed successfully"
fi

# Start the development server
echo "🌟 Starting Next.js development server on port 3002..."
echo ""
echo "🎉 Frontend will be available at: http://localhost:3002"
echo "📡 Backend API endpoint: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
if [ "$1" = "--prod" ]; then
    echo "🚀 Starting production server..."
    npm run build && npm start
else
    npm run dev
fi