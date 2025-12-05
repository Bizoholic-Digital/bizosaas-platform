#!/bin/bash

# SQLAdmin Dashboard Startup Script
# Provides infrastructure management interface for SUPER_ADMIN users

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🗄️  Starting SQLAdmin Dashboard - Infrastructure Management${NC}"
echo "=================================================================="

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo -e "${RED}❌ Error: main.py not found. Please run from the sqladmin-dashboard directory${NC}"
    exit 1
fi

# Check for required dependencies
echo -e "${BLUE}📋 Checking dependencies...${NC}"

# Check if python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi

# Check if docker is available for database
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker not found - you'll need to configure external database${NC}"
fi

# Create .env from example if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}📝 Creating .env from .env.example${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please configure your .env file with the correct settings${NC}"
fi

# Check for required environment variables
source .env 2>/dev/null || true

required_vars=("DATABASE_URL" "UNIFIED_AUTH_URL" "SECRET_KEY")
missing_vars=()

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo -e "${RED}❌ Missing required environment variables:${NC}"
    printf '%s\n' "${missing_vars[@]}"
    echo -e "${YELLOW}Please configure these in your .env file${NC}"
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
    pip install -q -r requirements.txt
else
    echo -e "${YELLOW}⚠️  requirements.txt not found, skipping dependency installation${NC}"
fi

# Check auth service connectivity
echo -e "${BLUE}🔐 Checking unified auth service connectivity...${NC}"
if curl -s --max-time 5 "$UNIFIED_AUTH_BROWSER_URL/health" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Auth service is reachable at $UNIFIED_AUTH_BROWSER_URL${NC}"
else
    echo -e "${YELLOW}⚠️  Auth service not reachable at $UNIFIED_AUTH_BROWSER_URL${NC}"
    echo -e "${YELLOW}   Make sure the auth service is running at localhost:3002${NC}"
fi

# Check database connectivity
echo -e "${BLUE}🗄️  Checking database connectivity...${NC}"
python3 -c "
import os
import sys
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

async def check_db():
    try:
        engine = create_async_engine(os.getenv('DATABASE_URL'))
        async with engine.begin() as conn:
            await conn.execute('SELECT 1')
        await engine.dispose()
        print('✅ Database connection successful')
        return True
    except Exception as e:
        print(f'❌ Database connection failed: {e}')
        return False

result = asyncio.run(check_db())
sys.exit(0 if result else 1)
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Database is accessible${NC}"
else
    echo -e "${YELLOW}⚠️  Database connection issues - service may not function properly${NC}"
fi

# Display startup information
echo ""
echo -e "${GREEN}🚀 Starting SQLAdmin Dashboard...${NC}"
echo -e "${BLUE}   Service URL: http://localhost:5000${NC}"
echo -e "${BLUE}   Auth Service: $UNIFIED_AUTH_BROWSER_URL${NC}"
echo -e "${BLUE}   TailAdmin URL: $TAILADMIN_URL${NC}"
echo ""
echo -e "${YELLOW}📋 Important Notes:${NC}"
echo -e "${YELLOW}   • Only SUPER_ADMIN users can access this dashboard${NC}"
echo -e "${YELLOW}   • You'll be redirected to unified login if not authenticated${NC}"
echo -e "${YELLOW}   • Database admin interface available at /admin${NC}"
echo -e "${YELLOW}   • Dashboard switcher available for super admins${NC}"
echo ""
echo -e "${BLUE}🔍 Service Status:${NC}"
echo -e "${BLUE}   Health Check: http://localhost:5000/api/system/health${NC}"
echo -e "${BLUE}   System Stats: http://localhost:5000/api/system/stats${NC}"
echo -e "${BLUE}   Dashboard: http://localhost:5000/dashboard-switcher${NC}"
echo ""

# Start the application
echo -e "${GREEN}🎯 SQLAdmin Dashboard starting on port 5000...${NC}"
echo -e "${BLUE}Press Ctrl+C to stop the service${NC}"
echo ""

# Run the application
python3 main.py