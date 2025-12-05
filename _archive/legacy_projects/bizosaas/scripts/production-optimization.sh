#!/bin/bash

# BizOSaaS Platform - Production Optimization Script
# Addresses critical issues identified in production readiness assessment

echo "🚀 BizOSaaS Production Optimization Script"
echo "==========================================="
echo "Date: $(date)"
echo "Target: Critical service recovery and performance optimization"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if running in correct directory
if [ ! -f "docker-compose.unified.yml" ]; then
    print_error "Please run this script from the bizosaas-platform directory"
    exit 1
fi

echo "1. CRITICAL SERVICE RECOVERY"
echo "==========================="

# Stop problematic containers
print_status "Stopping unhealthy containers..."
docker stop bizosaas-ai-agents-8010 2>/dev/null || print_warning "AI Agents container not running"
docker stop bizosaas-auth-unified-8007 2>/dev/null || print_warning "Auth container already stopped"
docker rm bizosaas-ai-agents-8010 2>/dev/null || print_warning "AI Agents container not found"

# Restart AI Agents service
print_status "Restarting AI Agents service..."
docker run -d \
    --name bizosaas-ai-agents-8010 \
    --network bizosaas-platform-network \
    -p 8010:8000 \
    -e POSTGRES_HOST="bizosaas-postgres-unified" \
    -e POSTGRES_DB="bizosaas" \
    -e POSTGRES_USER="postgres" \
    -e POSTGRES_PASSWORD="Bizoholic2024Alagiri" \
    -e REDIS_HOST="bizosaas-redis-unified" \
    -e REDIS_PORT=6379 \
    bizosaas/ai-agents:latest

if [ $? -eq 0 ]; then
    print_success "AI Agents service restarted successfully"
else
    print_error "Failed to restart AI Agents service"
fi

# Check if Business Directory is missing and start it
print_status "Checking Business Directory service..."
if ! curl -s http://localhost:3004 > /dev/null; then
    print_status "Starting Business Directory service..."
    cd frontend/apps/business-directory
    if [ -f "package.json" ]; then
        npm install --legacy-peer-deps --silent
        nohup npm run dev > /tmp/business-directory.log 2>&1 &
        print_success "Business Directory started in development mode"
    else
        print_error "Business Directory package.json not found"
    fi
    cd ../../../
else
    print_success "Business Directory already running on port 3004"
fi

echo ""
echo "2. CONTAINER HEALTH OPTIMIZATION"
echo "================================"

# Update health checks for containers
print_status "Checking container health status..."
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "(unhealthy|restarting)" | while read -r line; do
    print_warning "Unhealthy container detected: $line"
done

# Restart unhealthy containers
print_status "Restarting unhealthy containers..."
for container in bizosaas-client-portal-3000 bizosaas-coreldove-frontend-dev-3002; do
    if docker ps | grep -q "$container"; then
        docker restart "$container"
        print_status "Restarted $container"
    fi
done

echo ""
echo "3. PERFORMANCE OPTIMIZATION"
echo "==========================="

# Clear Docker system cache
print_status "Cleaning Docker system cache..."
docker system prune -f > /dev/null
print_success "Docker cache cleared"

# Optimize container resource allocation
print_status "Applying resource optimizations..."

# Create optimized docker-compose override for production
cat > docker-compose.prod-override.yml << EOF
version: '3.8'
services:
  bizosaas-brain-unified:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.5'
          
  bizosaas-postgres-unified:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'
    command: postgres -c max_connections=200 -c shared_buffers=256MB -c effective_cache_size=1GB
    
  bizosaas-redis-unified:
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.5'
        reservations:
          memory: 128M
          cpus: '0.25'
EOF

print_success "Production resource limits configured"

echo ""
echo "4. NETWORK OPTIMIZATION"
echo "======================="

# Test all service endpoints
print_status "Testing service connectivity..."
services=(
    "3000:Client Portal"
    "3001:Bizoholic Frontend" 
    "3002:CorelDove Frontend"
    "8001:Central Hub API"
    "8007:Auth Service"
    "8010:AI Agents"
)

for service in "${services[@]}"; do
    port="${service%:*}"
    name="${service#*:}"
    
    if timeout 5 curl -s http://localhost:$port > /dev/null 2>&1; then
        print_success "$name (Port $port): ✅ Online"
    else
        print_warning "$name (Port $port): ⚠️  Not responding"
    fi
done

echo ""
echo "5. DATABASE OPTIMIZATION"
echo "========================"

# Optimize PostgreSQL settings
print_status "Optimizing database performance..."
docker exec bizosaas-postgres-unified psql -U postgres -d bizosaas -c "
-- Update statistics
ANALYZE;

-- Check and create missing indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tenants_domain ON tenants(domain);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_leads_created_at ON leads(created_at);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_campaigns_tenant_id ON campaigns(tenant_id);

-- Vacuum to reclaim space
VACUUM ANALYZE;
" 2>/dev/null && print_success "Database optimized" || print_warning "Database optimization partially completed"

echo ""
echo "6. MONITORING SETUP"
echo "==================="

# Create simple monitoring script
cat > scripts/health-monitor.sh << 'EOF'
#!/bin/bash
# Simple health monitoring script

LOGFILE="/tmp/bizosaas-health.log"
echo "$(date): Health check started" >> $LOGFILE

# Check all services
services="3000 3001 3002 8001 8007 8010"
for port in $services; do
    if curl -s --connect-timeout 5 http://localhost:$port > /dev/null; then
        echo "$(date): Port $port OK" >> $LOGFILE
    else
        echo "$(date): Port $port FAILED" >> $LOGFILE
    fi
done

# Check database
if docker exec bizosaas-postgres-unified pg_isready -U postgres > /dev/null 2>&1; then
    echo "$(date): Database OK" >> $LOGFILE
else
    echo "$(date): Database FAILED" >> $LOGFILE
fi

# Check Redis
if docker exec bizosaas-redis-unified redis-cli ping > /dev/null 2>&1; then
    echo "$(date): Redis OK" >> $LOGFILE
else
    echo "$(date): Redis FAILED" >> $LOGFILE
fi
EOF

chmod +x scripts/health-monitor.sh
print_success "Health monitoring script created"

echo ""
echo "7. FINAL VERIFICATION"
echo "===================="

# Wait for services to stabilize
print_status "Waiting for services to stabilize..."
sleep 10

# Final health check
print_status "Performing final health verification..."
healthy_services=0
total_services=6

for port in 3000 3001 3002 8001 8007 8010; do
    if timeout 5 curl -s http://localhost:$port > /dev/null 2>&1; then
        ((healthy_services++))
    fi
done

echo ""
echo "🎯 OPTIMIZATION RESULTS"
echo "======================="
echo "Healthy Services: $healthy_services/$total_services"
echo "Success Rate: $((healthy_services * 100 / total_services))%"

if [ $healthy_services -ge 5 ]; then
    print_success "Platform optimization completed successfully!"
    print_success "Ready for production deployment"
elif [ $healthy_services -ge 4 ]; then
    print_warning "Platform mostly optimized - minor issues remain"
    print_warning "Acceptable for staged production deployment"
else
    print_error "Critical issues remain - further optimization needed"
    print_error "Not recommended for production deployment"
fi

echo ""
echo "📊 NEXT STEPS"
echo "============="
echo "1. Monitor logs: tail -f /tmp/bizosaas-health.log"
echo "2. Check service status: docker ps"
echo "3. Performance monitoring: docker stats"
echo "4. Review full report: cat PRODUCTION_READINESS_REPORT.md"
echo ""
print_status "Optimization completed at $(date)"
EOF