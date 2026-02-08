#!/bin/bash

# Enhanced SQLAdmin Dashboard Startup Script
# This script starts the SQLAdmin dashboard with comprehensive monitoring

set -e

echo "🚀 Starting Enhanced SQLAdmin Dashboard with Infrastructure Monitoring"
echo "=================================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed."
    exit 1
fi

# Set default environment variables
export DATABASE_URL=${DATABASE_URL:-"postgresql+asyncpg://bizosaas:bizosaas@host.docker.internal:5432/bizosaas"}
export REDIS_URL=${REDIS_URL:-"redis://host.docker.internal:6379/0"}
export UNIFIED_AUTH_URL=${UNIFIED_AUTH_URL:-"http://host.docker.internal:3002"}
export UNIFIED_AUTH_BROWSER_URL=${UNIFIED_AUTH_BROWSER_URL:-"http://localhost:3002"}
export TAILADMIN_URL=${TAILADMIN_URL:-"http://localhost:3001"}

# Monitoring configuration
export MONITORING_INTERVAL=${MONITORING_INTERVAL:-60}
export MONITORING_RETENTION_DAYS=${MONITORING_RETENTION_DAYS:-30}
export ENABLED_COLLECTORS=${ENABLED_COLLECTORS:-"database,redis,containers,api_endpoints"}

# Alert thresholds
export CPU_WARNING_THRESHOLD=${CPU_WARNING_THRESHOLD:-80.0}
export CPU_CRITICAL_THRESHOLD=${CPU_CRITICAL_THRESHOLD:-95.0}
export MEMORY_WARNING_THRESHOLD=${MEMORY_WARNING_THRESHOLD:-85.0}
export MEMORY_CRITICAL_THRESHOLD=${MEMORY_CRITICAL_THRESHOLD:-95.0}

echo "📋 Configuration:"
echo "   Database: ${DATABASE_URL}"
echo "   Redis: ${REDIS_URL}"
echo "   Auth Service: ${UNIFIED_AUTH_URL}"
echo "   Monitoring Interval: ${MONITORING_INTERVAL}s"
echo "   Enabled Collectors: ${ENABLED_COLLECTORS}"
echo ""

# Create necessary directories
mkdir -p logs data

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating default configuration..."
    cat > .env << EOF
# SQLAdmin Dashboard Configuration
DATABASE_URL=postgresql+asyncpg://bizosaas:bizosaas@host.docker.internal:5432/bizosaas
DATABASE_SYNC_URL=postgresql://bizosaas:bizosaas@host.docker.internal:5432/bizosaas
REDIS_URL=redis://host.docker.internal:6379/0

# Authentication URLs
UNIFIED_AUTH_URL=http://host.docker.internal:3002
UNIFIED_AUTH_BROWSER_URL=http://localhost:3002
TAILADMIN_URL=http://localhost:3001

# Monitoring Configuration
MONITORING_INTERVAL=60
MONITORING_RETENTION_DAYS=30
ENABLED_COLLECTORS=database,redis,containers,api_endpoints

# Alert Thresholds
CPU_WARNING_THRESHOLD=80.0
CPU_CRITICAL_THRESHOLD=95.0
MEMORY_WARNING_THRESHOLD=85.0
MEMORY_CRITICAL_THRESHOLD=95.0
RESPONSE_TIME_WARNING=2000
RESPONSE_TIME_CRITICAL=5000
ERROR_RATE_WARNING=5.0
ERROR_RATE_CRITICAL=10.0
CACHE_HIT_RATE_WARNING=80.0
EOF
    echo "   ✅ Created .env file with default values"
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down --remove-orphans

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

# Check PostgreSQL
if docker-compose exec -T postgresql pg_isready -U bizosaas -d bizosaas > /dev/null 2>&1; then
    echo "   ✅ PostgreSQL is ready"
else
    echo "   ❌ PostgreSQL is not ready"
fi

# Check Redis
if docker-compose exec -T redis redis-cli ping | grep -q PONG; then
    echo "   ✅ Redis is ready"
else
    echo "   ❌ Redis is not ready"
fi

# Check SQLAdmin Dashboard
if curl -s http://localhost:5000/api/system/health > /dev/null 2>&1; then
    echo "   ✅ SQLAdmin Dashboard is ready"
else
    echo "   ⏳ SQLAdmin Dashboard is starting up..."
    sleep 15
    if curl -s http://localhost:5000/api/system/health > /dev/null 2>&1; then
        echo "   ✅ SQLAdmin Dashboard is ready"
    else
        echo "   ❌ SQLAdmin Dashboard is not responding"
    fi
fi

echo ""
echo "🎉 Enhanced SQLAdmin Dashboard is now running!"
echo "=================================================================="
echo ""
echo "📊 Access URLs:"
echo "   • SQLAdmin Interface: http://localhost:5000/admin"
echo "   • Infrastructure Dashboard: http://localhost:5000/dashboard-switcher"
echo "   • API Health Check: http://localhost:5000/api/system/health"
echo "   • System Stats: http://localhost:5000/api/system/stats"
echo "   • Monitoring Data: http://localhost:5000/api/monitoring/dashboard"
echo "   • Traefik Dashboard: http://localhost:8080"
echo ""
echo "🔧 Management Commands:"
echo "   • View logs: docker-compose logs -f sqladmin-dashboard"
echo "   • Check status: docker-compose ps"
echo "   • Stop services: docker-compose down"
echo "   • Restart: docker-compose restart sqladmin-dashboard"
echo ""
echo "🔑 Authentication:"
echo "   • Requires SUPER_ADMIN role through unified auth system"
echo "   • Login via: ${UNIFIED_AUTH_BROWSER_URL}"
echo ""
echo "📈 Monitoring Features:"
echo "   • AI Agents Performance Tracking"
echo "   • Database Health Monitoring"
echo "   • Redis Cache Metrics"
echo "   • Container Resource Monitoring"
echo "   • API Endpoint Performance"
echo "   • Security Event Tracking"
echo "   • Business Operations Analytics"
echo "   • Intelligent Alerting System"
echo ""

# Show container status
echo "📋 Container Status:"
docker-compose ps

echo ""
echo "✨ Setup complete! Your enhanced infrastructure monitoring is ready."

# Optional: Open browser
if command -v xdg-open &> /dev/null; then
    echo ""
    read -p "🌐 Open dashboard in browser? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        xdg-open http://localhost:5000/dashboard-switcher
    fi
elif command -v open &> /dev/null; then
    echo ""
    read -p "🌐 Open dashboard in browser? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open http://localhost:5000/dashboard-switcher
    fi
fi

echo ""
echo "🎯 Next Steps:"
echo "   1. Login with SUPER_ADMIN credentials"
echo "   2. Explore the Infrastructure Dashboard"
echo "   3. Configure alert thresholds in .env file"
echo "   4. Set up notification channels for alerts"
echo "   5. Review monitoring data and performance metrics"
echo ""
echo "📚 Documentation: See README.md for detailed usage guide"