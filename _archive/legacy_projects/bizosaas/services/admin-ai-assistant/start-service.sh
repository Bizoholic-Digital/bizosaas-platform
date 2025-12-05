#!/bin/bash

# BizOSaaS Admin AI Assistant Start Script
# Easy service management and monitoring

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Service configuration
SERVICE_NAME="BizOSaaS Admin AI Assistant"
SERVICE_PORT=8028
HEALTH_ENDPOINT="http://localhost:${SERVICE_PORT}/health"
DASHBOARD_URL="http://localhost:${SERVICE_PORT}/dashboard"

print_banner() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║        🤖 BizOSaaS Admin AI Assistant [P10]                 ║"
    echo "║        Comprehensive Platform Monitoring & Operations       ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    print_status "Checking dependencies..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi
    
    # Check pip
    if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
        print_error "pip is not installed"
        exit 1
    fi
    
    print_success "Dependencies check passed"
}

check_environment() {
    print_status "Checking environment configuration..."
    
    if [ ! -f .env ]; then
        print_warning ".env file not found, creating from template..."
        if [ -f .env.example ]; then
            cp .env.example .env
            print_warning "Please edit .env file with your configuration"
        else
            print_error ".env.example not found"
            exit 1
        fi
    fi
    
    print_success "Environment configuration ready"
}

install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    if [ -f requirements.txt ]; then
        pip install -r requirements.txt
    else
        print_error "requirements.txt not found"
        exit 1
    fi
    
    print_success "Dependencies installed successfully"
}

check_port() {
    print_status "Checking if port ${SERVICE_PORT} is available..."
    
    if netstat -tuln 2>/dev/null | grep -q ":${SERVICE_PORT} "; then
        print_warning "Port ${SERVICE_PORT} is already in use"
        
        # Try to find what's using the port
        PID=$(lsof -ti:${SERVICE_PORT} 2>/dev/null || echo "")
        if [ ! -z "$PID" ]; then
            PROCESS=$(ps -p $PID -o comm= 2>/dev/null || echo "unknown")
            print_warning "Process using port ${SERVICE_PORT}: $PROCESS (PID: $PID)"
            
            read -p "Kill the process and continue? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                kill $PID
                sleep 2
                print_success "Process killed"
            else
                print_error "Cannot start service on port ${SERVICE_PORT}"
                exit 1
            fi
        fi
    else
        print_success "Port ${SERVICE_PORT} is available"
    fi
}

start_service() {
    print_status "Starting ${SERVICE_NAME}..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Start the service in background
    nohup python main.py > service.log 2>&1 &
    SERVICE_PID=$!
    
    # Save PID to file
    echo $SERVICE_PID > service.pid
    
    print_success "Service started with PID: $SERVICE_PID"
    
    # Wait for service to be ready
    print_status "Waiting for service to be ready..."
    
    for i in {1..30}; do
        if curl -s -f "$HEALTH_ENDPOINT" > /dev/null 2>&1; then
            print_success "Service is ready!"
            break
        fi
        
        if [ $i -eq 30 ]; then
            print_error "Service failed to start within 30 seconds"
            print_error "Check service.log for details"
            exit 1
        fi
        
        echo -n "."
        sleep 1
    done
    echo
}

show_service_info() {
    echo
    echo -e "${GREEN}🎉 ${SERVICE_NAME} is now running!${NC}"
    echo
    echo -e "${BLUE}📊 Service Information:${NC}"
    echo "   Service PID:     $(cat service.pid 2>/dev/null || echo 'Unknown')"
    echo "   Port:           ${SERVICE_PORT}"
    echo "   Log file:       service.log"
    echo
    echo -e "${BLUE}🔗 Access URLs:${NC}"
    echo "   Dashboard:      ${DASHBOARD_URL}"
    echo "   API Docs:       http://localhost:${SERVICE_PORT}/docs"
    echo "   Health Check:   ${HEALTH_ENDPOINT}"
    echo "   Metrics API:    http://localhost:${SERVICE_PORT}/api/platform/metrics"
    echo
    echo -e "${BLUE}💬 AI Assistant Features:${NC}"
    echo "   • Real-time platform monitoring and health checks"
    echo "   • Intelligent chat assistant for troubleshooting"
    echo "   • Automated anomaly detection and alerting"
    echo "   • Performance analytics and optimization recommendations"
    echo "   • Cross-service coordination and monitoring"
    echo "   • WebSocket-based real-time updates"
    echo
    echo -e "${BLUE}🛠️  Management Commands:${NC}"
    echo "   Stop service:    ./stop-service.sh"
    echo "   View logs:       tail -f service.log"
    echo "   Check status:    curl ${HEALTH_ENDPOINT}"
    echo "   Restart:         ./stop-service.sh && ./start-service.sh"
    echo
}

create_stop_script() {
    cat > stop-service.sh << 'EOF'
#!/bin/bash

# Stop BizOSaaS Admin AI Assistant

if [ -f service.pid ]; then
    PID=$(cat service.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "Stopping service (PID: $PID)..."
        kill $PID
        sleep 2
        
        # Force kill if still running
        if ps -p $PID > /dev/null 2>&1; then
            echo "Force killing service..."
            kill -9 $PID
        fi
        
        rm -f service.pid
        echo "Service stopped successfully"
    else
        echo "Service is not running"
        rm -f service.pid
    fi
else
    echo "PID file not found. Service may not be running."
fi
EOF
    chmod +x stop-service.sh
}

create_status_script() {
    cat > status-service.sh << 'EOF'
#!/bin/bash

# Check BizOSaaS Admin AI Assistant status

if [ -f service.pid ]; then
    PID=$(cat service.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ Service is running (PID: $PID)"
        
        # Check health endpoint
        if curl -s -f "http://localhost:8028/health" > /dev/null 2>&1; then
            echo "✅ Health check passed"
        else
            echo "❌ Health check failed"
        fi
        
        # Show resource usage
        echo "📊 Resource usage:"
        ps -p $PID -o pid,ppid,pcpu,pmem,vsz,rss,tty,stat,start,time,command
    else
        echo "❌ Service is not running (stale PID file)"
        rm -f service.pid
    fi
else
    echo "❌ Service is not running (no PID file)"
fi
EOF
    chmod +x status-service.sh
}

main() {
    print_banner
    
    # Change to script directory
    cd "$(dirname "$0")"
    
    # Run checks and setup
    check_dependencies
    check_environment
    check_port
    install_dependencies
    
    # Start the service
    start_service
    
    # Create management scripts
    create_stop_script
    create_status_script
    
    # Show service information
    show_service_info
    
    print_status "Service startup completed successfully!"
    print_status "Monitor logs with: tail -f service.log"
}

# Handle script arguments
case "${1:-start}" in
    "start")
        main
        ;;
    "install")
        print_banner
        cd "$(dirname "$0")"
        check_dependencies
        check_environment
        install_dependencies
        print_success "Installation completed!"
        ;;
    "check")
        print_banner
        cd "$(dirname "$0")"
        check_dependencies
        check_environment
        check_port
        print_success "Environment check completed!"
        ;;
    "help"|"-h"|"--help")
        print_banner
        echo "Usage: $0 [command]"
        echo
        echo "Commands:"
        echo "  start     Start the service (default)"
        echo "  install   Install dependencies only"
        echo "  check     Check environment and dependencies"
        echo "  help      Show this help message"
        echo
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac