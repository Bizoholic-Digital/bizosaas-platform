#!/bin/bash

# BizOSaas SSO System Startup Script
# Comprehensive Single Sign-On system deployment

set -e

echo "🚀 Starting BizOSaas Unified SSO System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Check if required files exist
check_requirements() {
    print_status "Checking requirements..."
    
    local required_files=(
        ".env"
        "docker-compose.sso.yml"
        "services/auth-service-v2/main.py"
        "shared/auth_system.py"
        "shared/auth_middleware.py"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            print_error "Required file missing: $file"
            exit 1
        fi
    done
    
    print_success "All requirements met"
}

# Setup environment variables
setup_environment() {
    print_status "Setting up environment..."
    
    if [[ ! -f .env ]]; then
        print_warning ".env file not found, creating from .env.example"
        if [[ -f .env.example ]]; then
            cp .env.example .env
        else
            print_error ".env.example not found"
            exit 1
        fi
    fi
    
    # Source environment variables
    source .env
    
    # Generate JWT secret if not set
    if [[ -z "${JWT_SECRET}" ]]; then
        JWT_SECRET=$(openssl rand -hex 32)
        echo "JWT_SECRET=${JWT_SECRET}" >> .env
        print_success "Generated JWT secret"
    fi
    
    # Generate Vault token if not set
    if [[ -z "${VAULT_TOKEN}" ]]; then
        VAULT_TOKEN=$(openssl rand -hex 16)
        echo "VAULT_TOKEN=${VAULT_TOKEN}" >> .env
        print_success "Generated Vault token"
    fi
    
    print_success "Environment configured"
}

# Create necessary directories
create_directories() {
    print_status "Creating directories..."
    
    local directories=(
        "logs"
        "database/init-scripts"
        "config/dynamicconfig"
        "shared"
    )
    
    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
    done
    
    print_success "Directories created"
}

# Create network if it doesn't exist
create_network() {
    print_status "Setting up Docker network..."
    
    if ! docker network ls | grep -q bizosaas-network; then
        docker network create bizosaas-network
        print_success "Created bizosaas-network"
    else
        print_success "bizosaas-network already exists"
    fi
}

# Initialize database schema
init_database() {
    print_status "Initializing database schema..."
    
    # Create init script for authentication tables
    cat > database/init-scripts/01-auth-schema.sql << 'EOF'
-- BizOSaas Authentication Schema
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgvector;

-- Tenants table
CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'trial',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    subscription_plan VARCHAR(50),
    subscription_status VARCHAR(20),
    trial_ends_at TIMESTAMP WITH TIME ZONE,
    allowed_platforms JSONB DEFAULT '["bizoholic"]',
    settings JSONB DEFAULT '{}'
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(320) UNIQUE NOT NULL,
    hashed_password VARCHAR(1024) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role VARCHAR(20) DEFAULT 'user',
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP WITH TIME ZONE,
    login_count INTEGER DEFAULT 0,
    preferences JSONB DEFAULT '{}',
    allowed_services JSONB DEFAULT '[]',
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE
);

-- User sessions table
CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    refresh_token VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    last_accessed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT,
    platform VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    logout_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_tenant_id ON users(tenant_id);
CREATE INDEX IF NOT EXISTS idx_tenants_slug ON tenants(slug);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token);

-- Create default super admin tenant
INSERT INTO tenants (id, name, slug, status, allowed_platforms) 
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'BizOSaas Platform',
    'bizosaas',
    'active',
    '["bizoholic", "coreldove", "temporal", "agent-monitor", "logging-service"]'
) ON CONFLICT (slug) DO NOTHING;

-- Create default super admin user (password: admin123)
INSERT INTO users (id, email, hashed_password, first_name, last_name, role, tenant_id, is_superuser, is_verified, allowed_services) 
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'admin@bizosaas.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeVMst13D2c8Tj6we',
    'Super',
    'Admin',
    'super_admin',
    '00000000-0000-0000-0000-000000000001',
    TRUE,
    TRUE,
    '["bizoholic", "coreldove", "temporal", "agent-monitor", "logging-service", "vault", "admin"]'
) ON CONFLICT (email) DO NOTHING;

COMMIT;
EOF

    print_success "Database initialization script created"
}

# Create Temporal configuration
create_temporal_config() {
    print_status "Creating Temporal configuration..."
    
    cat > config/dynamicconfig/development-sql.yaml << 'EOF'
system.forceSearchAttributesCacheRefreshOnRead:
  - value: true
    constraints: {}

system.enableReadFromClosedExecutionV2:
  - value: true
    constraints: {}

history.persistenceMaxQPS:
  - value: 3000
    constraints: {}

frontend.persistenceMaxQPS:
  - value: 3000
    constraints: {}
EOF

    print_success "Temporal configuration created"
}

# Start the SSO system
start_services() {
    print_status "Starting BizOSaas SSO services..."
    
    # Pull latest images
    docker-compose -f docker-compose.sso.yml pull
    
    # Start infrastructure services first
    print_status "Starting infrastructure services..."
    docker-compose -f docker-compose.sso.yml up -d \
        shared-postgres-dev \
        shared-redis-dev \
        vault
    
    # Wait for infrastructure to be ready
    print_status "Waiting for infrastructure services..."
    sleep 15
    
    # Start Temporal services
    print_status "Starting Temporal services..."
    docker-compose -f docker-compose.sso.yml up -d \
        temporal-postgresql \
        temporal-elasticsearch
    sleep 10
    
    docker-compose -f docker-compose.sso.yml up -d \
        temporal \
        temporal-web
    sleep 10
    
    # Start authentication service
    print_status "Starting authentication service..."
    docker-compose -f docker-compose.sso.yml up -d auth-service
    sleep 5
    
    # Start application services
    print_status "Starting application services..."
    docker-compose -f docker-compose.sso.yml up -d \
        agent-monitor \
        logging-service \
        coreldove-sourcing \
        crewai-agents
    sleep 5
    
    # Start frontend services
    print_status "Starting frontend services..."
    docker-compose -f docker-compose.sso.yml up -d \
        bizosaas-frontend \
        coreldove-frontend
    
    print_success "All services started"
}

# Populate Vault with secrets
populate_vault() {
    print_status "Populating Vault with secrets..."
    
    # Wait for Vault to be ready
    sleep 5
    
    # Source environment
    source .env
    
    # Check if vault populate script exists
    if [[ -f "vault-populate-secrets.sh" ]]; then
        chmod +x vault-populate-secrets.sh
        ./vault-populate-secrets.sh
        print_success "Vault populated with secrets"
    else
        print_warning "vault-populate-secrets.sh not found, skipping Vault population"
    fi
}

# Health check
health_check() {
    print_status "Performing health checks..."
    
    local services=(
        "http://localhost:8003/health|Authentication Service"
        "http://localhost:8001/health|Agent Monitor"
        "http://localhost:8002/health|Logging Service"
        "http://localhost:8004/health|CoreLDove Sourcing"
        "http://localhost:8000/health|CrewAI Agents"
        "http://localhost:3000|BizOSaas Frontend"
        "http://localhost:3002|CoreLDove Frontend"
        "http://localhost:8088|Temporal Web UI"
    )
    
    for service_info in "${services[@]}"; do
        IFS="|" read -r url name <<< "$service_info"
        
        if curl -f -s "$url" > /dev/null 2>&1; then
            print_success "$name is healthy"
        else
            print_warning "$name is not responding"
        fi
        
        sleep 1
    done
}

# Display access information
display_access_info() {
    print_success "🎉 BizOSaas SSO System is running!"
    echo ""
    echo "📱 Access Information:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔐 Authentication Service:     http://localhost:8003"
    echo "📊 BizOSaas Dashboard:         http://localhost:3000"
    echo "🛒 CoreLDove Platform:         http://localhost:3002"
    echo "⚡ Temporal Dashboard:         http://localhost:8088"
    echo "🤖 Agent Monitor:              http://localhost:8001"
    echo "📋 Logging Service:            http://localhost:8002"
    echo "🎯 CrewAI Agents API:          http://localhost:8000"
    echo "🔑 Vault UI:                   http://localhost:8200"
    echo ""
    echo "🔑 Default Admin Credentials:"
    echo "   Email: admin@bizosaas.com"
    echo "   Password: admin123"
    echo ""
    echo "📚 API Documentation:"
    echo "   Auth Service: http://localhost:8003/auth/docs"
    echo "   Agent Monitor: http://localhost:8001/docs"
    echo "   Logging Service: http://localhost:8002/docs"
    echo ""
    echo "🐳 Docker Commands:"
    echo "   View logs: docker-compose -f docker-compose.sso.yml logs -f [service]"
    echo "   Stop system: docker-compose -f docker-compose.sso.yml down"
    echo "   Restart service: docker-compose -f docker-compose.sso.yml restart [service]"
    echo ""
    echo "✨ Features Enabled:"
    echo "   • Single Sign-On (SSO) across all platforms"
    echo "   • Multi-tenant architecture"
    echo "   • Role-based access control"
    echo "   • JWT token authentication"
    echo "   • Session management"
    echo "   • Audit logging"
    echo "   • Real-time monitoring"
    echo "   • Workflow orchestration"
    echo ""
}

# Main execution
main() {
    echo "🎯 BizOSaas Unified SSO System Setup"
    echo "════════════════════════════════════"
    
    check_requirements
    setup_environment
    create_directories
    create_network
    init_database
    create_temporal_config
    start_services
    populate_vault
    health_check
    display_access_info
    
    print_success "Setup completed successfully! 🚀"
}

# Run main function
main "$@"