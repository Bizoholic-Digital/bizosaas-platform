#!/bin/bash

# Comprehensive Saleor Database Setup Script
# Creates database, applies migrations, and sets up initial data

set -e  # Exit on any error

echo "🚀 Starting Saleor database setup..."

# Configuration
DB_NAME="saleor_coreldove"
DB_USER="admin"
DB_HOST="localhost"
DB_PORT="5432"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if PostgreSQL is accessible
echo "🔍 Checking PostgreSQL connectivity..."
if ! timeout 10 bash -c "</dev/tcp/$DB_HOST/$DB_PORT"; then
    print_error "PostgreSQL is not accessible on $DB_HOST:$DB_PORT"
    exit 1
fi
print_status "PostgreSQL is accessible"

# Function to execute SQL commands
execute_sql() {
    local sql="$1"
    local database="${2:-postgres}"
    
    if command -v psql >/dev/null 2>&1; then
        # Use direct psql if available
        PGPASSWORD="BizoholicSecure2025" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$database" -c "$sql"
    else
        # Try to find a PostgreSQL container
        local postgres_containers=("bizoholic-postgres" "shared-postgres-dev" "postgres" "bizosaas-postgres")
        local container_found=false
        
        for container in "${postgres_containers[@]}"; do
            if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "^${container}$"; then
                print_status "Using PostgreSQL container: ${container}"
                docker exec -i "${container}" psql -U "$DB_USER" -d "$database" -c "$sql"
                container_found=true
                break
            fi
        done
        
        if [ "$container_found" = false ]; then
            print_error "No PostgreSQL container found and psql command not available"
            print_warning "Available containers:"
            docker ps --format "table {{.Names}}\t{{.Image}}" 2>/dev/null || echo "Docker not accessible"
            exit 1
        fi
    fi
}

# Create database if it doesn't exist
echo "🗄️  Creating Saleor database..."
execute_sql "SELECT 'CREATE DATABASE $DB_NAME OWNER $DB_USER;' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME');" | \
execute_sql "CREATE DATABASE $DB_NAME OWNER $DB_USER;" 2>/dev/null || print_warning "Database $DB_NAME might already exist"

# Set up required extensions
echo "🔌 Setting up database extensions..."
execute_sql "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";" "$DB_NAME" 2>/dev/null
execute_sql "CREATE EXTENSION IF NOT EXISTS \"btree_gin\";" "$DB_NAME" 2>/dev/null
execute_sql "CREATE EXTENSION IF NOT EXISTS \"btree_gist\";" "$DB_NAME" 2>/dev/null
execute_sql "CREATE EXTENSION IF NOT EXISTS \"pg_trgm\";" "$DB_NAME" 2>/dev/null
execute_sql "CREATE EXTENSION IF NOT EXISTS \"hstore\";" "$DB_NAME" 2>/dev/null

print_status "Database extensions configured"

# Grant permissions
echo "🔐 Setting up database permissions..."
execute_sql "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" "postgres" 2>/dev/null
execute_sql "ALTER USER $DB_USER CREATEDB;" "postgres" 2>/dev/null

print_status "Database permissions configured"

# Wait for Saleor API container to be ready
echo "⏳ Waiting for Saleor API container to be ready..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "saleor-api"; then
        print_status "Saleor API container is running"
        break
    fi
    
    echo "Waiting for Saleor API container... (attempt $attempt/$max_attempts)"
    sleep 5
    ((attempt++))
done

if [ $attempt -gt $max_attempts ]; then
    print_warning "Saleor API container not found, but continuing with setup"
fi

# Run database migrations
echo "🔄 Running database migrations..."
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "saleor-api"; then
    echo "Running migrations in Saleor container..."
    docker exec saleor-api python manage.py migrate || print_warning "Migrations may have failed"
    
    # Create initial data
    echo "📊 Creating initial data..."
    docker exec saleor-api python manage.py populatedb --createsuperuser || print_warning "Sample data creation may have failed"
    
    # Collect static files
    echo "📁 Collecting static files..."
    docker exec saleor-api python manage.py collectstatic --noinput || print_warning "Static files collection may have failed"
    
    print_status "Database setup completed successfully!"
    
    # Display admin credentials
    echo ""
    echo "🎯 Saleor Setup Complete!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🌐 Saleor GraphQL API: http://localhost:8024/graphql/"
    echo "🎨 Saleor Dashboard: http://localhost:9001/"
    echo "📊 GraphQL Playground: http://localhost:8024/graphql/"
    echo ""
    echo "👤 Default Admin Credentials:"
    echo "   Email: admin@example.com"
    echo "   Password: admin"
    echo ""
    echo "💡 Test the GraphQL endpoint:"
    echo "   curl -X POST http://localhost:8024/graphql/ \\"
    echo "        -H \"Content-Type: application/json\" \\"
    echo "        -d '{\"query\":\"{ shop { name description } }\"}'"
    echo ""
else
    print_status "Database created and configured successfully!"
    print_warning "Start the Saleor containers to complete the setup:"
    echo "   cd /home/alagiri/projects/bizoholic/bizosaas"
    echo "   docker-compose -f docker-compose.saleor-complete.yml up -d"
fi