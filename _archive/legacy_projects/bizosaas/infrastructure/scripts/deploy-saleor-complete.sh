#!/bin/bash
# Complete Saleor Infrastructure Deployment Script
# Deploys full Saleor e-commerce platform with GraphQL API for CoreLDove storefront

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  CoreLDove Saleor Infrastructure       ${NC}"
echo -e "${BLUE}  Complete E-commerce Platform          ${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed or not in PATH"
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed or not in PATH"
    exit 1
fi

# Set working directory
cd "$(dirname "$0")"

# Load environment variables
if [ -f .env.saleor ]; then
    print_status "Loading Saleor environment configuration..."
    export $(cat .env.saleor | grep -v '^#' | xargs)
else
    print_warning "No .env.saleor file found, using defaults"
fi

# Deployment function
deploy_saleor() {
    print_status "Deploying Saleor infrastructure..."
    
    # Check if ports are available
    print_status "Checking port availability..."
    
    if lsof -Pi :8024 -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port 8024 is in use. Attempting to stop conflicting service..."
        # Try to stop any existing saleor proxy
        pkill -f "saleor.*8024" || true
        pkill -f "saleor-proxy.py" || true
        sleep 2
    fi
    
    if lsof -Pi :9020 -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port 9020 is in use. This will cause dashboard conflicts."
    fi
    
    # Deploy services
    print_status "Starting Saleor services..."
    
    # Use environment file if available
    if [ -f .env.saleor ]; then
        docker-compose -f docker-compose.saleor-full.yml --env-file .env.saleor up -d
    else
        docker-compose -f docker-compose.saleor-full.yml up -d
    fi
    
    # Wait for services to be healthy
    print_status "Waiting for services to become healthy..."
    
    # Wait for PostgreSQL
    print_status "Waiting for PostgreSQL to be ready..."
    timeout 300 bash -c 'until docker-compose -f docker-compose.saleor-full.yml exec -T saleor-postgres pg_isready -U saleor -d saleor_coreldove; do sleep 5; done' || {
        print_error "PostgreSQL failed to start within timeout"
        return 1
    }
    
    # Wait for Redis
    print_status "Waiting for Redis to be ready..."
    timeout 120 bash -c 'until docker-compose -f docker-compose.saleor-full.yml exec -T saleor-redis redis-cli ping; do sleep 2; done' || {
        print_error "Redis failed to start within timeout"
        return 1
    }
    
    # Wait for Saleor API
    print_status "Waiting for Saleor API to be ready..."
    timeout 600 bash -c 'until curl -s http://localhost:8024/health/ > /dev/null; do echo "Waiting for Saleor API..."; sleep 10; done' || {
        print_error "Saleor API failed to start within timeout"
        print_status "Checking Saleor API logs..."
        docker-compose -f docker-compose.saleor-full.yml logs saleor-api | tail -50
        return 1
    }
    
    # Wait for Dashboard
    print_status "Waiting for Saleor Dashboard to be ready..."
    timeout 300 bash -c 'until curl -s http://localhost:9020/ > /dev/null; do echo "Waiting for Dashboard..."; sleep 5; done' || {
        print_warning "Dashboard may need more time to start"
    }
    
    print_status "Saleor infrastructure deployed successfully!"
    return 0
}

# Status check function
check_status() {
    print_status "Checking Saleor service status..."
    
    echo -e "\n${BLUE}Docker Services:${NC}"
    docker-compose -f docker-compose.saleor-full.yml ps
    
    echo -e "\n${BLUE}Service Health Checks:${NC}"
    
    # PostgreSQL
    if docker-compose -f docker-compose.saleor-full.yml exec -T saleor-postgres pg_isready -U saleor -d saleor_coreldove &>/dev/null; then
        echo -e "  PostgreSQL: ${GREEN}✓ Healthy${NC}"
    else
        echo -e "  PostgreSQL: ${RED}✗ Unhealthy${NC}"
    fi
    
    # Redis
    if docker-compose -f docker-compose.saleor-full.yml exec -T saleor-redis redis-cli ping &>/dev/null; then
        echo -e "  Redis: ${GREEN}✓ Healthy${NC}"
    else
        echo -e "  Redis: ${RED}✗ Unhealthy${NC}"
    fi
    
    # Saleor API
    if curl -s http://localhost:8024/health/ > /dev/null; then
        echo -e "  Saleor API: ${GREEN}✓ Healthy${NC} (http://localhost:8024)"
    else
        echo -e "  Saleor API: ${RED}✗ Unhealthy${NC}"
    fi
    
    # Dashboard
    if curl -s http://localhost:9020/ > /dev/null; then
        echo -e "  Dashboard: ${GREEN}✓ Healthy${NC} (http://localhost:9020)"
    else
        echo -e "  Dashboard: ${RED}✗ Unhealthy${NC}"
    fi
    
    echo -e "\n${BLUE}GraphQL Endpoints:${NC}"
    echo "  GraphQL API: http://localhost:8024/graphql/"
    echo "  GraphQL Playground: http://localhost:8024/graphql/"
    echo "  Admin Dashboard: http://localhost:9020/"
    echo "  GraphQL Introspection: Enabled"
}

# Schema validation function
validate_schema() {
    print_status "Validating GraphQL schema completeness..."
    
    # Create temporary schema validation script
    cat > /tmp/schema_check.py << 'EOF'
import requests
import json

def check_schema():
    """Check if all required Saleor schema fields are available"""
    
    introspection_query = """
    query IntrospectionQuery {
      __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
        types {
          ...FullType
        }
      }
    }

    fragment FullType on __Type {
      kind
      name
      description
      fields(includeDeprecated: true) {
        name
        description
        args {
          ...InputValue
        }
        type {
          ...TypeRef
        }
        isDeprecated
        deprecationReason
      }
      inputFields {
        ...InputValue
      }
      interfaces {
        ...TypeRef
      }
      enumValues(includeDeprecated: true) {
        name
        description
        isDeprecated
        deprecationReason
      }
      possibleTypes {
        ...TypeRef
      }
    }

    fragment InputValue on __InputValue {
      name
      description
      type { ...TypeRef }
      defaultValue
    }

    fragment TypeRef on __Type {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    
    try:
        response = requests.post(
            'http://localhost:8024/graphql/',
            json={'query': introspection_query},
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            schema = response.json()
            
            # Check for required fields
            required_fields = [
                'channels', 'checkoutLinesAdd', 'products', 'productVariants',
                'orders', 'users', 'customers', 'categories', 'collections',
                'shippingZones', 'paymentGateways', 'warehouse', 'stocks'
            ]
            
            available_fields = []
            if 'data' in schema and '__schema' in schema['data']:
                types = schema['data']['__schema']['types']
                for type_def in types:
                    if type_def.get('fields'):
                        for field in type_def['fields']:
                            available_fields.append(field['name'])
            
            missing_fields = []
            for field in required_fields:
                if field not in available_fields:
                    missing_fields.append(field)
            
            print(f"✓ GraphQL schema loaded successfully")
            print(f"✓ Total available fields: {len(available_fields)}")
            
            if missing_fields:
                print(f"⚠ Missing fields: {', '.join(missing_fields)}")
                return False
            else:
                print(f"✓ All required e-commerce fields are available")
                return True
                
        else:
            print(f"✗ Failed to fetch schema: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Schema validation failed: {e}")
        return False

if __name__ == "__main__":
    if check_schema():
        exit(0)
    else:
        exit(1)
EOF
    
    # Run schema validation
    if python3 /tmp/schema_check.py; then
        print_status "Schema validation passed! ✓"
        return 0
    else
        print_error "Schema validation failed!"
        return 1
    fi
}

# Test storefront connection
test_storefront_integration() {
    print_status "Testing storefront integration..."
    
    # Test GraphQL query that storefront uses
    curl -X POST http://localhost:8024/graphql/ \
        -H "Content-Type: application/json" \
        -d '{
            "query": "{ shop { name description } channels { slug name } }"
        }' | jq . || print_warning "GraphQL test query failed"
    
    print_status "Integration test completed"
}

# Logs function
show_logs() {
    local service=${1:-""}
    
    if [ -n "$service" ]; then
        print_status "Showing logs for $service..."
        docker-compose -f docker-compose.saleor-full.yml logs -f "$service"
    else
        print_status "Showing logs for all services..."
        docker-compose -f docker-compose.saleor-full.yml logs -f
    fi
}

# Stop services
stop_services() {
    print_status "Stopping Saleor services..."
    docker-compose -f docker-compose.saleor-full.yml down
    print_status "Services stopped"
}

# Cleanup function
cleanup_all() {
    print_warning "This will remove all data! Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        print_status "Stopping and removing all Saleor services and data..."
        docker-compose -f docker-compose.saleor-full.yml down -v --remove-orphans
        docker volume prune -f
        print_status "Cleanup completed"
    else
        print_status "Cleanup cancelled"
    fi
}

# Usage function
show_usage() {
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  deploy       Deploy complete Saleor infrastructure"
    echo "  status       Check service status and health"
    echo "  validate     Validate GraphQL schema completeness"
    echo "  test         Test storefront integration"
    echo "  logs [svc]   Show logs for all services or specific service"
    echo "  stop         Stop all services"
    echo "  cleanup      Stop services and remove all data"
    echo "  help         Show this help message"
    echo
    echo "Examples:"
    echo "  $0 deploy                 # Deploy all services"
    echo "  $0 status                 # Check service status"
    echo "  $0 logs saleor-api        # Show API logs"
    echo "  $0 validate               # Validate GraphQL schema"
}

# Main script logic
case "${1:-deploy}" in
    "deploy")
        deploy_saleor
        if [ $? -eq 0 ]; then
            echo
            check_status
            echo
            print_status "Deployment completed successfully!"
            echo
            echo -e "${GREEN}Next steps:${NC}"
            echo "1. Access GraphQL API: http://localhost:8024/graphql/"
            echo "2. Access Admin Dashboard: http://localhost:9020/"
            echo "3. Configure your storefront to use: http://localhost:8024/graphql/"
            echo "4. Run './deploy-saleor-complete.sh validate' to verify schema"
        fi
        ;;
    "status")
        check_status
        ;;
    "validate")
        validate_schema
        ;;
    "test")
        test_storefront_integration
        ;;
    "logs")
        show_logs "$2"
        ;;
    "stop")
        stop_services
        ;;
    "cleanup")
        cleanup_all
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    *)
        print_error "Unknown command: $1"
        echo
        show_usage
        exit 1
        ;;
esac