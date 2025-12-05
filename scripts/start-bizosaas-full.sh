#!/bin/bash
# Start all BizOSaaS services - Updated for Hybrid Auth Architecture
# Includes: Infrastructure, Backend Services, Bizoholic Frontend (3001), Client Portal (3003)

set -e

echo "🚀 Starting BizOSaaS Full Stack (Hybrid Auth)"
echo "=============================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Start Infrastructure
echo -e "\n${YELLOW}Step 1/6: Starting Infrastructure (Postgres, Redis)...${NC}"
docker-compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres redis
echo -e "${GREEN}✓ Infrastructure started${NC}"

# Wait for infrastructure
echo "Waiting for infrastructure to be ready..."
echo "Checking database connectivity..."

# Wait for Postgres to be ready (with retries)
MAX_RETRIES=10
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  if docker exec bizosaas-postgres-unified pg_isready -U postgres > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Database is ready${NC}"
    break
  fi
  RETRY_COUNT=$((RETRY_COUNT + 1))
  echo "  Waiting for database... (attempt $RETRY_COUNT/$MAX_RETRIES)"
  sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
  echo -e "${RED}✗ Database failed to start${NC}"
  echo "Checking container status..."
  docker ps | grep postgres
  exit 1
fi

# Step 2: Start Auth Service (Port 8008)
echo -e "\n${YELLOW}Step 2/6: Starting Auth Service (Port 8008)...${NC}"
cd shared/services/auth
if lsof -i :8008 > /dev/null 2>&1; then
    echo -e "${YELLOW}Port 8008 in use. Stopping existing process...${NC}"
    lsof -t -i :8008 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas"
export REDIS_URL="redis://localhost:6379/0"
nohup uvicorn main:app --host 0.0.0.0 --port 8008 --reload > /tmp/auth-service.log 2>&1 &
AUTH_PID=$!
echo $AUTH_PID > /tmp/auth-service.pid
echo -e "${GREEN}✓ Auth Service started (PID: $AUTH_PID)${NC}"
echo "  Log: /tmp/auth-service.log"
cd ../../..

# Step 3: Start Brain Gateway (Port 8001)
echo -e "\n${YELLOW}Step 3/6: Starting Brain Gateway (Port 8001)...${NC}"
cd shared/services/brain-gateway
if lsof -i :8001 > /dev/null 2>&1; then
    echo -e "${YELLOW}Port 8001 in use. Stopping existing process...${NC}"
    lsof -t -i :8001 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

nohup uvicorn main:app --host 0.0.0.0 --port 8001 --reload > /tmp/brain-gateway.log 2>&1 &
BRAIN_PID=$!
echo $BRAIN_PID > /tmp/brain-gateway.pid
echo -e "${GREEN}✓ Brain Gateway started (PID: $BRAIN_PID)${NC}"
echo "  Log: /tmp/brain-gateway.log"
cd ../../..

# Wait for backend services
echo "Waiting for backend services to initialize..."
echo "  (Auth Service needs time to connect to database...)"
sleep 15

# Step 4: Start Bizoholic Frontend (Port 3001)
echo -e "\n${YELLOW}Step 4/6: Starting Bizoholic Frontend (Port 3001)...${NC}"
cd brands/bizoholic/frontend

if lsof -i :3001 > /dev/null 2>&1; then
    echo -e "${YELLOW}Port 3001 in use. Stopping existing process...${NC}"
    lsof -t -i :3001 | xargs kill -9 2>/dev/null || true
    sleep 3
fi

PORT=3001 nohup npm run dev > /tmp/bizoholic-frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > /tmp/bizoholic-frontend.pid
echo -e "${GREEN}✓ Bizoholic Frontend started (PID: $FRONTEND_PID)${NC}"
echo "  Log: /tmp/bizoholic-frontend.log"
cd ../../..

# Step 5: Start Client Portal (Port 3003)
echo -e "\n${YELLOW}Step 5/6: Starting Client Portal (Port 3003)...${NC}"
cd portals/client-portal

if lsof -i :3003 > /dev/null 2>&1; then
    echo -e "${YELLOW}Port 3003 in use. Stopping existing process...${NC}"
    lsof -t -i :3003 | xargs kill -9 2>/dev/null || true
    sleep 3
fi

nohup npm run dev -- --port 3003 > /tmp/client-portal.log 2>&1 &
PORTAL_PID=$!
echo $PORTAL_PID > /tmp/client-portal.pid
echo -e "${GREEN}✓ Client Portal started (PID: $PORTAL_PID)${NC}"
echo "  Log: /tmp/client-portal.log"
cd ../..

# Step 6: Verify Services
echo -e "\n${YELLOW}Step 6/6: Verifying Services...${NC}"

# Function to check service
check_service() {
    local name=$1
    local url=$2
    local max_retries=30
    local retry=0
    
    while [ $retry -lt $max_retries ]; do
        if curl -s --max-time 3 "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ $name: Running${NC}"
            return 0
        fi
        retry=$((retry + 1))
        if [ $retry -lt $max_retries ]; then
            echo -n "."
            sleep 3
        fi
    done
    
    echo -e "\n${RED}✗ $name: Not responding${NC}"
    return 1
}

echo "Checking Auth Service..."
check_service "Auth Service (8008)" "http://localhost:8008/health"

echo "Checking Brain Gateway..."
check_service "Brain Gateway (8001)" "http://localhost:8001/health"

echo "Checking Bizoholic Frontend..."
check_service "Bizoholic Frontend (3001)" "http://localhost:3001"

echo "Checking Client Portal..."
check_service "Client Portal (3003)" "http://localhost:3003/login"

# Summary
echo -e "\n${GREEN}=============================================${NC}"
echo -e "${GREEN}✓ BizOSaaS Full Stack Started!${NC}"
echo -e "${GREEN}=============================================${NC}"
echo ""
echo "🌐 Services:"
echo "  Bizoholic Frontend:  http://localhost:3001"
echo "  Client Portal:       http://localhost:3003"
echo "  Client Portal Login: http://localhost:3003/login"
echo "  Brain Gateway:       http://localhost:8001"
echo "  Auth Service:        http://localhost:8008"
echo ""
echo "🔐 Login Credentials:"
echo "  Admin:  admin@bizoholic.com / AdminDemo2024!"
echo "  Client: client@bizosaas.com / ClientDemo2024!"
echo ""
echo "📊 Infrastructure:"
echo "  Postgres:  localhost:5432"
echo "  Redis:     localhost:6379"
echo ""
echo "📝 Logs:"
echo "  Auth Service:     tail -f /tmp/auth-service.log"
echo "  Brain Gateway:    tail -f /tmp/brain-gateway.log"
echo "  Bizoholic:        tail -f /tmp/bizoholic-frontend.log"
echo "  Client Portal:    tail -f /tmp/client-portal.log"
echo ""
echo "🛑 To stop all services:"
echo "  kill \$(cat /tmp/*.pid 2>/dev/null) 2>/dev/null || true"
echo "  docker-compose -f shared/infrastructure/docker-compose.infrastructure.yml down"
echo ""
