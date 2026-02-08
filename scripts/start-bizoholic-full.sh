#!/bin/bash
# Start all Bizoholic services with proper resource limits
# This script starts infrastructure, backend services, Wagtail CMS, and frontend

set -e

echo "🚀 Starting Bizoholic Full Stack"
echo "================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Start Infrastructure
echo -e "\n${YELLOW}Step 1/5: Starting Infrastructure (Postgres, Redis, Vault)...${NC}"
docker-compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres redis vault
echo -e "${GREEN}✓ Infrastructure started${NC}"

# Wait for infrastructure to be ready
echo "Waiting for infrastructure to be ready..."
sleep 5

# Step 2: Start Backend Services (with resource limits)
echo -e "\n${YELLOW}Step 2/5: Starting Backend Services (Brain API, Auth, CRM, Wagtail)...${NC}"

# Check if services are already running and only restart if needed
echo "Checking for existing backend containers..."
RUNNING_SERVICES=$(docker ps --filter "name=bizosaas-brain-unified\|bizosaas-auth-unified\|bizosaas-django-crm\|bizosaas-wagtail-unified" --format "{{.Names}}" | wc -l)

if [ "$RUNNING_SERVICES" -gt 0 ]; then
    echo -e "${YELLOW}Found $RUNNING_SERVICES running services. Restarting them...${NC}"
    docker-compose -f shared/services/docker-compose.services.yml restart brain-gateway auth crm cms
else
    echo "Starting fresh backend services..."
    # Only stop and remove if they exist but are not running
    docker-compose -f shared/services/docker-compose.services.yml stop brain-gateway auth crm cms 2>/dev/null || true
    docker-compose -f shared/services/docker-compose.services.yml rm -f brain-gateway auth crm cms 2>/dev/null || true
    
    # Start backend services including Wagtail CMS
    DOCKER_BUILDKIT=0 docker-compose -f shared/services/docker-compose.services.yml up -d brain-gateway auth crm cms
fi

echo -e "${GREEN}✓ Backend services started${NC}"

# Wait for backend to initialize (Auth needs more time)
echo "Waiting for backend services to initialize..."
sleep 35  # Increased wait time for Auth and Wagtail

# Step 3: Start Frontend
echo -e "\n${YELLOW}Step 3/5: Starting Frontend (Bizoholic)...${NC}"
cd brands/bizoholic/frontend

# Kill any existing processes on port 3001 (including Next.js child processes)
echo "Checking for existing frontend processes..."
if ss -tlnp 2>/dev/null | grep -q :3001; then
    echo -e "${YELLOW}Port 3001 is in use. Stopping all related processes...${NC}"
    
    # Get all PIDs listening on port 3001 (including next-server children)
    PIDS=$(ss -tlnp 2>/dev/null | grep :3001 | grep -oP 'pid=\K[0-9]+' | sort -u)
    
    for PID in $PIDS; do
        if ps -p $PID > /dev/null 2>&1; then
            echo "  Killing process $PID and its children..."
            # Kill the entire process group
            pkill -9 -P $PID 2>/dev/null || true
            kill -9 $PID 2>/dev/null || true
        fi
    done
    
    sleep 3
    
    # Double-check port is free
    if ss -tlnp 2>/dev/null | grep -q :3001; then
        echo -e "${RED}Warning: Port 3001 still in use. Forcing cleanup...${NC}"
        # Nuclear option: kill anything with 'next' in the command
        pkill -9 -f "next.*3001" 2>/dev/null || true
        sleep 2
    fi
fi

# Clean up old PID file
if [ -f /tmp/bizoholic-frontend.pid ]; then
    OLD_PID=$(cat /tmp/bizoholic-frontend.pid)
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "Cleaning up old frontend process tree (PID: $OLD_PID)..."
        pkill -9 -P $OLD_PID 2>/dev/null || true
        kill -9 $OLD_PID 2>/dev/null || true
    fi
    rm /tmp/bizoholic-frontend.pid
fi

# Verify port is free
if ss -tlnp 2>/dev/null | grep -q :3001; then
    echo -e "${RED}ERROR: Unable to free port 3001. Please manually kill processes:${NC}"
    ss -tlnp | grep :3001
    exit 1
fi

echo -e "${GREEN}✓ Port 3001 is free${NC}"
echo "Starting frontend on port 3001..."
echo "  (This may take 60-90 seconds for Next.js to compile...)"

# Clean previous build if exists
if [ -f .next/BUILD_ID ]; then
    echo "Cleaning previous build..."
    rm -rf .next
fi

PORT=3001 npm run dev > /tmp/bizoholic-frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > /tmp/bizoholic-frontend.pid
echo -e "${GREEN}✓ Frontend process started (PID: $FRONTEND_PID)${NC}"
echo "  Log file: /tmp/bizoholic-frontend.log"
cd ../../..

# Step 4: Verify Services
echo -e "\n${YELLOW}Step 4/5: Verifying Services...${NC}"
# Robust Frontend Health Check
echo "Waiting for Frontend to be ready on port 3001..."
MAX_ATTEMPTS=60 # 60 * 2s = 120s max wait
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    # Check if process is still running
    if ! ps -p $FRONTEND_PID > /dev/null; then
        echo -e "${RED}✗ Frontend process died unexpectedly!${NC}"
        echo "Last 20 lines of log:"
        tail -n 20 /tmp/bizoholic-frontend.log
        exit 1
    fi

    # Check if port is listening
    if ss -tlnp 2>/dev/null | grep -q :3001; then
        echo -e "${GREEN}✓ Frontend is listening on port 3001${NC}"
        break
    fi

    ATTEMPT=$((ATTEMPT + 1))
    echo -n "."
    sleep 2
done

echo ""

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    echo -e "${RED}✗ Frontend failed to start within 120 seconds.${NC}"
    echo "Last 20 lines of log:"
    tail -n 20 /tmp/bizoholic-frontend.log
    # Don't exit, let user decide what to do
else
    # Verify HTTP response
    if curl -s --max-time 5 "http://localhost:3001" > /dev/null; then
        echo -e "${GREEN}✓ Frontend (3001): Responding to HTTP requests${NC}"
    else
        echo -e "${YELLOW}⚠ Frontend is listening but returned error/timeout. Check logs.${NC}"
    fi
fi
# Function to check service with retries
check_service() {
    local name=$1
    local url=$2
    local max_retries=5  # Increased to 5 retries
    local retry=0
    
    while [ $retry -lt $max_retries ]; do
        if curl -s --max-time 3 "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ $name: Running${NC}"
            return 0
        fi
        retry=$((retry + 1))
        if [ $retry -lt $max_retries ]; then
            sleep 3  # Increased to 3 seconds between retries
        fi
    done
    
    echo -e "${RED}✗ $name: Not responding (tried $max_retries times)${NC}"
    echo -e "${YELLOW}  Tip: Check logs with: docker logs ${name// */}${NC}"
    return 1
}

check_service "Brain API (8000)" "http://localhost:8000/health"
check_service "Auth (8007)" "http://localhost:8007/health"
check_service "CRM (8005)" "http://localhost:8005/health"
check_service "Wagtail CMS (8002)" "http://localhost:8002/health/"

# Step 5: Display Service Status
echo -e "\n${YELLOW}Step 5/5: Container Status...${NC}"
docker ps --filter "name=bizosaas" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "NAME|brain|auth|crm|wagtail|postgres|redis|vault"

# Summary
echo -e "\n${GREEN}=================================${NC}"
echo -e "${GREEN}✓ Bizoholic Full Stack Started!${NC}"
echo -e "${GREEN}=================================${NC}"
echo ""
echo "Services:"
echo "  Frontend:     http://localhost:3001  (Next.js Dev Server - Outside Container)"
echo "  Brain API:    http://localhost:8000  (Centralized Gateway)"
echo "  Auth:         http://localhost:8007  (FastAPI)"
echo "  CRM:          http://localhost:8005  (Django)"
echo "  Wagtail CMS:  http://localhost:8002  (Content Management)"
echo ""
echo "Admin Panels (Embedded in Portal):"
echo "  Wagtail:      http://localhost:3001/portal/dashboard/content"
echo "  CRM:          http://localhost:3001/portal/dashboard/crm"
echo ""
echo "Infrastructure:"
echo "  Postgres:  localhost:5432"
echo "  Redis:     localhost:6379"
echo "  Vault:     localhost:8200"
echo ""
echo "Resource Limits Enforced:"
echo "  Brain API: 1GB RAM, 0.8 CPU"
echo "  CRM:       512MB RAM, 0.3 CPU"
echo "  Auth:      256MB RAM, 0.2 CPU"
echo "  Wagtail:   512MB RAM, 0.3 CPU"
echo ""
echo "Notes:"
echo "  - Frontend runs OUTSIDE container for hot-reload during development"
echo "  - For production, frontend will be containerized"
echo "  - Admin panels are embedded in client portal (not accessed directly)"
echo ""
echo "To stop all services: ./scripts/stop-bizoholic-full.sh"
