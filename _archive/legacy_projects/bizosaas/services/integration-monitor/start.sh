#!/bin/bash

# BizOSaaS Integration Monitor Startup Script
# Starts the integration monitoring service with proper configuration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 BizOSaaS Integration Monitor${NC}"
echo -e "${BLUE}================================${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}📝 Please edit .env with your configuration and API keys${NC}"
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo -e "${RED}❌ Python 3.11+ required. Found: $python_version${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python version: $python_version${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Install/update dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Check database connection
echo -e "${YELLOW}🔍 Checking database connection...${NC}"
python3 -c "
import asyncio
import sys
from database.connection import init_database, get_database_health

async def check_db():
    try:
        await init_database()
        health = await get_database_health()
        if health['status'] == 'healthy':
            print('✅ Database connection successful')
            return True
        else:
            print(f'❌ Database unhealthy: {health.get(\"error\", \"unknown\")}')
            return False
    except Exception as e:
        print(f'❌ Database connection failed: {e}')
        return False

if not asyncio.run(check_db()):
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Database connection failed. Please check your DATABASE_URL in .env${NC}"
    exit 1
fi

# Create necessary directories
mkdir -p logs data static

# Set proper permissions
chmod +x main.py

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down Integration Monitor...${NC}"
    exit 0
}

# Trap signals for graceful shutdown
trap cleanup SIGINT SIGTERM

# Start the service
echo -e "${GREEN}🚀 Starting Integration Monitor on port 8003...${NC}"
echo -e "${BLUE}📊 Dashboard: http://localhost:8003/dashboard${NC}"
echo -e "${BLUE}📚 API Docs: http://localhost:8003/docs${NC}"
echo -e "${BLUE}🏥 Health: http://localhost:8003/health${NC}"
echo -e "${BLUE}================================${NC}"

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Start the application
python3 main.py