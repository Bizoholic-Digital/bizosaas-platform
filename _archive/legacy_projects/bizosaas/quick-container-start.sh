#!/bin/bash

# Quick Container Start - Start essential services without full rebuild
set -e

echo "🚀 Quick Container Start for BizOSaaS Platform..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Start just the essential new services using existing infrastructure
print_status "Starting essential services only..."

# Start Brain Gateway if not running
if ! curl -s http://localhost:8001/health > /dev/null 2>&1; then
    print_status "Starting Brain Gateway..."
    docker-compose -f docker-compose.unified.yml up -d bizosaas-brain &
    sleep 15
else
    print_success "Brain Gateway already running ✅"
fi

# Start new services using Python directly (faster than Docker builds)
print_status "Starting Business Directory Service on port 8004..."
cd /home/alagiri/projects/bizoholic/bizosaas-platform/services/business-directory
python3 main.py &
BUSINESS_PID=$!

print_status "Starting SQLAdmin Dashboard Service on port 8005..."
cd /home/alagiri/projects/bizoholic/bizosaas-platform/services/sqladmin-dashboard
python3 main.py &
SQLADMIN_PID=$!

print_status "Starting Analytics Dashboard Service on port 3009..."
cd /home/alagiri/projects/bizoholic/bizosaas-platform/services/analytics-dashboard
python3 main.py &
ANALYTICS_PID=$!

# Wait for services to start
sleep 10

# Test services
print_status "Testing services..."
services=(
    "http://localhost:8001/health:Brain Gateway"
    "http://localhost:8004/health:Business Directory"
    "http://localhost:8005/health:SQLAdmin Dashboard"
    "http://localhost:3009/health:Analytics Dashboard"
)

all_healthy=true
for service in "${services[@]}"; do
    url="${service%:*}"
    name="${service#*:}"
    
    if curl -s -f "$url" > /dev/null 2>&1; then
        print_success "$name is healthy ✅"
    else
        echo "❌ $name is not responding"
        all_healthy=false
    fi
done

# Display summary
echo -e "\n${BLUE}=== QUICK START SUMMARY ===${NC}"
echo -e "${GREEN}Running Services:${NC}"
echo -e "  🧠 Brain Gateway: http://localhost:8001"
echo -e "  🗃️  Business Directory: http://localhost:8004"
echo -e "  🗂️  SQLAdmin Dashboard: http://localhost:8005"
echo -e "  📊 Analytics Dashboard: http://localhost:3009"

echo -e "\n${GREEN}Frontend Applications:${NC}"
echo -e "  🌐 Business Directory Frontend: http://localhost:3004"
echo -e "  ⚙️  BizOSaaS Admin Frontend: http://localhost:3005"

echo -e "\n${BLUE}Process IDs (for stopping):${NC}"
echo -e "  Business Directory: $BUSINESS_PID"
echo -e "  SQLAdmin Dashboard: $SQLADMIN_PID"
echo -e "  Analytics Dashboard: $ANALYTICS_PID"

echo -e "\n${BLUE}To stop services:${NC}"
echo -e "  kill $BUSINESS_PID $SQLADMIN_PID $ANALYTICS_PID"

if [ "$all_healthy" = true ]; then
    print_success "🎉 Quick container start complete!"
else
    echo "⚠️ Some services may need attention"
fi