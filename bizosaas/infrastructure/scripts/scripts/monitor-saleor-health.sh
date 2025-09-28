#!/bin/bash

# Saleor Health Monitor Script
# Comprehensive monitoring of all Saleor services

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔍 $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${NC}"
}

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Function to check service health
check_service_health() {
    local service_name="$1"
    local url="$2"
    local expected_status="${3:-200}"
    
    echo -n "Checking $service_name... "
    
    if response=$(curl -s -w "%{http_code}" -o /dev/null "$url" 2>/dev/null); then
        if [ "$response" = "$expected_status" ]; then
            print_status "$service_name is healthy (HTTP $response)"
            return 0
        else
            print_warning "$service_name returned HTTP $response (expected $expected_status)"
            return 1
        fi
    else
        print_error "$service_name is not responding"
        return 2
    fi
}

# Function to check GraphQL endpoint
check_graphql_endpoint() {
    local url="$1"
    
    echo -n "Testing GraphQL endpoint... "
    
    local query='{"query":"{ shop { name description } }"}'
    if response=$(curl -s -X POST "$url" \
        -H "Content-Type: application/json" \
        -d "$query" 2>/dev/null); then
        
        if echo "$response" | grep -q '"data"'; then
            print_status "GraphQL endpoint is responding with valid data"
            return 0
        else
            print_warning "GraphQL endpoint responded but may have errors"
            echo "Response: $response"
            return 1
        fi
    else
        print_error "GraphQL endpoint is not responding"
        return 2
    fi
}

# Function to check container status
check_container_status() {
    local container_name="$1"
    
    echo -n "Checking container $container_name... "
    
    if docker ps --format '{{.Names}}' | grep -q "^${container_name}$"; then
        local status=$(docker inspect --format='{{.State.Status}}' "$container_name" 2>/dev/null)
        local health=$(docker inspect --format='{{.State.Health.Status}}' "$container_name" 2>/dev/null)
        
        if [ "$status" = "running" ]; then
            if [ "$health" = "healthy" ] || [ "$health" = "<no value>" ]; then
                print_status "$container_name is running and healthy"
                return 0
            else
                print_warning "$container_name is running but health status: $health"
                return 1
            fi
        else
            print_error "$container_name is not running (status: $status)"
            return 2
        fi
    else
        print_error "$container_name container not found"
        return 2
    fi
}

# Function to check database connectivity
check_database_connectivity() {
    echo -n "Checking PostgreSQL connectivity... "
    
    if timeout 5 bash -c "</dev/tcp/localhost/5432"; then
        print_status "PostgreSQL is accessible on localhost:5432"
        return 0
    else
        print_error "PostgreSQL is not accessible on localhost:5432"
        return 1
    fi
}

# Function to check Redis connectivity
check_redis_connectivity() {
    echo -n "Checking Redis connectivity... "
    
    if docker exec saleor-redis redis-cli ping >/dev/null 2>&1; then
        print_status "Redis is responding to ping"
        return 0
    else
        print_error "Redis is not responding"
        return 1
    fi
}

# Main monitoring function
main() {
    print_header "SALEOR INFRASTRUCTURE HEALTH CHECK"
    
    local overall_status=0
    
    # Check database connectivity
    check_database_connectivity || overall_status=1
    
    # Check container statuses
    echo ""
    print_info "Container Status:"
    check_container_status "saleor-redis" || overall_status=1
    check_container_status "saleor-api" || overall_status=1
    check_container_status "saleor-worker" || overall_status=1
    check_container_status "saleor-beat" || overall_status=1
    check_container_status "saleor-dashboard" || overall_status=1
    
    # Check Redis connectivity
    echo ""
    print_info "Service Connectivity:"
    check_redis_connectivity || overall_status=1
    
    # Check HTTP endpoints
    echo ""
    print_info "HTTP Endpoints:"
    check_service_health "Saleor API Health" "http://localhost:8024/health/" 200 || overall_status=1
    check_service_health "Saleor Dashboard" "http://localhost:9001/" 200 || overall_status=1
    
    # Check GraphQL endpoint
    echo ""
    print_info "GraphQL Endpoint:"
    check_graphql_endpoint "http://localhost:8024/graphql/" || overall_status=1
    
    # Display resource usage
    echo ""
    print_header "RESOURCE USAGE"
    
    if docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}" saleor-redis saleor-api saleor-worker saleor-beat saleor-dashboard 2>/dev/null; then
        print_status "Resource usage displayed above"
    else
        print_warning "Could not retrieve resource usage stats"
    fi
    
    # Display ports and services
    echo ""
    print_header "SERVICE ENDPOINTS"
    
    echo "🌐 Saleor GraphQL API: http://localhost:8024/graphql/"
    echo "🎨 Saleor Dashboard: http://localhost:9001/"
    echo "💾 Redis: localhost:6379"
    echo "🗄️  PostgreSQL: localhost:5432"
    
    # Final status
    echo ""
    if [ $overall_status -eq 0 ]; then
        print_header "OVERALL STATUS: HEALTHY"
        print_status "All Saleor services are running correctly"
    else
        print_header "OVERALL STATUS: ISSUES DETECTED"
        print_warning "Some services may need attention"
    fi
    
    return $overall_status
}

# Run monitoring
main "$@"