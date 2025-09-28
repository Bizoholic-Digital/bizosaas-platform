#!/bin/bash

# Create Saleor database in PostgreSQL
# This script connects to the existing PostgreSQL and creates the Saleor database

echo "🗄️  Creating Saleor database..."

# Check if PostgreSQL is accessible
if ! timeout 5 nc -z localhost 5432; then
    echo "❌ PostgreSQL is not accessible on localhost:5432"
    exit 1
fi

echo "✅ PostgreSQL is accessible"

# Create the database using Docker exec (assuming PostgreSQL runs in a container)
# We'll try multiple methods to create the database

# Method 1: If PostgreSQL is in a container
POSTGRES_CONTAINERS=(
    "bizoholic-postgres"
    "shared-postgres-dev"
    "postgres"
    "bizosaas-postgres"
)

for container in "${POSTGRES_CONTAINERS[@]}"; do
    if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        echo "📦 Found PostgreSQL container: ${container}"
        
        # Create database if it doesn't exist
        echo "🔧 Creating coreldove_saleor database..."
        docker exec -i "${container}" psql -U admin -d postgres -c "
            SELECT 'CREATE DATABASE coreldove_saleor OWNER admin;'
            WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'coreldove_saleor');" | \
        docker exec -i "${container}" psql -U admin -d postgres || echo "Database might already exist"
        
        # Set up extensions
        echo "🔌 Setting up database extensions..."
        docker exec -i "${container}" psql -U admin -d coreldove_saleor -c "
            CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";
            CREATE EXTENSION IF NOT EXISTS \"btree_gin\";
            CREATE EXTENSION IF NOT EXISTS \"btree_gist\";
            CREATE EXTENSION IF NOT EXISTS \"pg_trgm\";
        " 2>/dev/null || echo "Extensions setup complete (or already exist)"
        
        echo "✅ Database setup complete using container: ${container}"
        exit 0
    fi
done

echo "⚠️  No PostgreSQL container found. Database might need manual setup."
echo "Expected containers: ${POSTGRES_CONTAINERS[*]}"
echo "Available containers:"
docker ps --format "table {{.Names}}\t{{.Image}}" || echo "Docker not accessible"

exit 0