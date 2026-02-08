#!/bin/bash

# BizOSaaS Development Environment Startup Script
# Optimized workflow for frontend-Brain API integration

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
BRAIN_API_PORT=8001
FRONTEND_PORT=3000
BRAIN_API_DIR="services/bizosaas-brain"
FRONTEND_DIR="frontend"

# PID files for process management
BRAIN_PID_FILE="/tmp/bizosaas-brain.pid"
FRONTEND_PID_FILE="/tmp/bizosaas-frontend.pid"

echo -e "${CYAN}🚀 BizOSaaS Development Environment Manager${NC}"
echo -e "${CYAN}================================================${NC}"

# Function to print status
print_status() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to check if port is in use
check_port() {
    local port=$1
    local service_name=$2
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        local pid=$(lsof -Pi :$port -sTCP:LISTEN -t)
        print_warning "$service_name already running on port $port (PID: $pid)"
        return 0
    else
        return 1
    fi
}

# Function to stop services
stop_services() {
    print_status "Stopping services..."
    
    # Stop Brain API
    if [ -f "$BRAIN_PID_FILE" ]; then
        local brain_pid=$(cat "$BRAIN_PID_FILE")
        if kill -0 "$brain_pid" 2>/dev/null; then
            kill "$brain_pid" && rm -f "$BRAIN_PID_FILE"
            print_success "Brain API stopped"
        fi
    fi
    
    # Stop Frontend
    if [ -f "$FRONTEND_PID_FILE" ]; then
        local frontend_pid=$(cat "$FRONTEND_PID_FILE")
        if kill -0 "$frontend_pid" 2>/dev/null; then
            kill "$frontend_pid" && rm -f "$FRONTEND_PID_FILE"
            print_success "Frontend stopped"
        fi
    fi
    
    # Kill any remaining processes
    pkill -f "simple_api.py" 2>/dev/null || true
    pkill -f "npm run dev" 2>/dev/null || true
    
    print_success "All services stopped"
}

# Function to start Brain API
start_brain_api() {
    print_status "Starting Brain API..."
    
    if check_port $BRAIN_API_PORT "Brain API"; then
        return 0
    fi
    
    cd "$BRAIN_API_DIR"
    
    # Start Brain API in background
    python3 simple_api.py > /tmp/brain-api.log 2>&1 &
    local brain_pid=$!
    echo $brain_pid > "$BRAIN_PID_FILE"
    
    # Wait for Brain API to start
    local attempts=0
    while [ $attempts -lt 10 ]; do
        if curl -s http://localhost:$BRAIN_API_PORT/health >/dev/null 2>&1; then
            print_success "Brain API started successfully (PID: $brain_pid)"
            return 0
        fi
        sleep 1
        ((attempts++))
    done
    
    print_error "Brain API failed to start"
    return 1
}

# Function to start Frontend
start_frontend() {
    print_status "Starting Frontend..."
    
    if check_port $FRONTEND_PORT "Frontend"; then
        return 0
    fi
    
    cd "../$FRONTEND_DIR"
    
    # Clear Next.js cache if it exists
    if [ -d ".next" ]; then
        print_status "Clearing Next.js cache..."
        rm -rf .next
    fi
    
    # Start frontend in background
    npm run dev > /tmp/frontend.log 2>&1 &
    local frontend_pid=$!
    echo $frontend_pid > "$FRONTEND_PID_FILE"
    
    # Wait for frontend to start
    local attempts=0
    while [ $attempts -lt 20 ]; do
        if curl -s http://localhost:$FRONTEND_PORT >/dev/null 2>&1; then
            print_success "Frontend started successfully (PID: $frontend_pid)"
            return 0
        fi
        sleep 1
        ((attempts++))
    done
    
    print_error "Frontend failed to start"
    return 1
}

# Function to test integration
test_integration() {
    print_status "Testing integration..."
    
    # Test Brain API health
    local brain_health=$(curl -s -w "%{http_code}" -o /dev/null http://localhost:$BRAIN_API_PORT/health)
    if [ "$brain_health" == "200" ]; then
        print_success "Brain API health check: OK"
    else
        print_error "Brain API health check failed (HTTP $brain_health)"
        return 1
    fi
    
    # Test frontend-Brain API proxy
    local proxy_health=$(curl -s -w "%{http_code}" -o /dev/null http://localhost:$FRONTEND_PORT/api/brain/wagtail/homepage)
    if [ "$proxy_health" == "200" ]; then
        print_success "Frontend-Brain API proxy: OK"
    else
        print_error "Frontend-Brain API proxy failed (HTTP $proxy_health)"
        return 1
    fi
    
    print_success "Integration tests passed!"
}

# Function to show running services
show_status() {
    echo -e "${CYAN}📊 Service Status${NC}"
    echo -e "${CYAN}=================${NC}"
    
    # Brain API status
    if check_port $BRAIN_API_PORT "Brain API" >/dev/null; then
        local brain_pid=$(lsof -Pi :$BRAIN_API_PORT -sTCP:LISTEN -t)
        echo -e "Brain API:  ${GREEN}Running${NC} (Port $BRAIN_API_PORT, PID: $brain_pid)"
        echo -e "           Health: http://localhost:$BRAIN_API_PORT/health"
    else
        echo -e "Brain API:  ${RED}Stopped${NC}"
    fi
    
    # Frontend status
    if check_port $FRONTEND_PORT "Frontend" >/dev/null; then
        local frontend_pid=$(lsof -Pi :$FRONTEND_PORT -sTCP:LISTEN -t)
        echo -e "Frontend:   ${GREEN}Running${NC} (Port $FRONTEND_PORT, PID: $frontend_pid)"
        echo -e "           URL: http://localhost:$FRONTEND_PORT"
    else
        echo -e "Frontend:   ${RED}Stopped${NC}"
    fi
    
    echo ""
    echo -e "${CYAN}🔗 Quick Links:${NC}"
    echo -e "Frontend:        http://localhost:$FRONTEND_PORT"
    echo -e "Brain API Docs:  http://localhost:$BRAIN_API_PORT/docs"
    echo -e "Health Check:    http://localhost:$BRAIN_API_PORT/health"
}

# Function to show logs
show_logs() {
    local service=$1
    
    case $service in
        "brain"|"api")
            if [ -f "/tmp/brain-api.log" ]; then
                tail -f /tmp/brain-api.log
            else
                print_error "Brain API log file not found"
            fi
            ;;
        "frontend"|"fe")
            if [ -f "/tmp/frontend.log" ]; then
                tail -f /tmp/frontend.log
            else
                print_error "Frontend log file not found"
            fi
            ;;
        *)
            echo "Available log options: brain, frontend"
            ;;
    esac
}

# Main execution logic
case "${1:-start}" in
    "start")
        print_status "Starting BizOSaaS development environment..."
        
        # Start services
        if start_brain_api && start_frontend; then
            sleep 3
            test_integration
            echo ""
            show_status
            echo ""
            print_success "🎉 Development environment ready!"
            echo -e "${YELLOW}💡 Use '$0 status' to check service status${NC}"
            echo -e "${YELLOW}💡 Use '$0 logs <service>' to view logs${NC}"
            echo -e "${YELLOW}💡 Use '$0 stop' to stop all services${NC}"
        else
            print_error "Failed to start development environment"
            stop_services
            exit 1
        fi
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        stop_services
        sleep 2
        exec "$0" start
        ;;
    "status")
        show_status
        ;;
    "test")
        test_integration
        ;;
    "logs")
        show_logs "$2"
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  start    - Start all services (default)"
        echo "  stop     - Stop all services"
        echo "  restart  - Restart all services"
        echo "  status   - Show service status"
        echo "  test     - Test integration"
        echo "  logs     - Show logs (brain|frontend)"
        echo "  help     - Show this help"
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for available commands"
        exit 1
        ;;
esac