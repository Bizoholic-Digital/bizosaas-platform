#!/bin/bash
# BizOSaaS Platform - Immediate Security Fixes
# This script addresses critical security vulnerabilities in port exposure

set -e

echo "🔒 BIZOSAAS IMMEDIATE SECURITY FIXES"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Log function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

echo ""
echo "PHASE 1: AUDIT CURRENT EXPOSURES"
echo "================================"

# Check dangerous exposed ports
log "Checking for exposed database ports..."
EXPOSED_POSTGRES=$(docker ps --format "{{.Names}} {{.Ports}}" | grep postgres | grep "0.0.0.0" || echo "")
EXPOSED_REDIS=$(docker ps --format "{{.Names}} {{.Ports}}" | grep redis | grep "0.0.0.0" || echo "")

if [[ -n "$EXPOSED_POSTGRES" ]]; then
    error "CRITICAL: PostgreSQL instances exposed to internet:"
    echo "$EXPOSED_POSTGRES"
else
    log "✓ No PostgreSQL instances exposed publicly"
fi

if [[ -n "$EXPOSED_REDIS" ]]; then
    error "CRITICAL: Redis instances exposed to internet:"
    echo "$EXPOSED_REDIS"
else
    log "✓ No Redis instances exposed publicly"
fi

# Check monitoring exposure
EXPOSED_MONITORING=$(ss -tlnp | grep ":3001" || echo "")
if [[ -n "$EXPOSED_MONITORING" ]]; then
    error "CRITICAL: Monitoring service exposed on port 3001"
else
    log "✓ Monitoring service not exposed"
fi

echo ""
echo "PHASE 2: CREATE SECURE DOCKER COMPOSE"
echo "====================================="

# Create secure docker-compose configuration
SECURE_COMPOSE_FILE="docker-compose.secure.yml"
log "Creating secure Docker Compose configuration: $SECURE_COMPOSE_FILE"

cat > "$SECURE_COMPOSE_FILE" << 'EOF'
version: '3.8'

# BizOSaaS Secure Configuration
# Databases and caches are NOT exposed to the internet

networks:
  internal:
    driver: bridge
    internal: true
  web:
    driver: bridge

services:
  # =============================================================================
  # DATABASE SERVICES (INTERNAL ONLY)
  # =============================================================================
  
  postgres-primary:
    image: postgres:15
    container_name: bizosaas-postgres-secure
    networks:
      - internal
    # NO PORT MAPPING - Internal access only
    environment:
      POSTGRES_DB: bizosaas
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d bizosaas"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis-primary:
    image: redis:7-alpine
    container_name: bizosaas-redis-secure  
    networks:
      - internal
    # NO PORT MAPPING - Internal access only
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # =============================================================================
  # APPLICATION SERVICES (SECURE ACCESS)
  # =============================================================================
  
  wagtail-cms:
    build: ./services/wagtail-cms
    container_name: bizosaas-wagtail-secure
    networks:
      - internal
      - web
    ports:
      - "127.0.0.1:3010:8000"  # localhost only access
    environment:
      POSTGRES_HOST: postgres-primary
      REDIS_HOST: redis-primary
      REDIS_PASSWORD: ${REDIS_PASSWORD}
    depends_on:
      - postgres-primary
      - redis-primary
    restart: unless-stopped
    
  monitoring:
    image: prom/prometheus
    container_name: bizosaas-monitoring-secure
    networks:
      - internal
    ports:
      - "127.0.0.1:9090:9090"  # localhost only access
    restart: unless-stopped

  # =============================================================================
  # PUBLIC SERVICES (AUTHENTICATED ACCESS)
  # =============================================================================
  
  unified-frontend:
    build: ./frontend
    container_name: bizosaas-frontend-secure
    networks:
      - web
    ports:
      - "3005:3000"  # Public access through authentication
    environment:
      NODE_ENV: production
      DATABASE_URL: postgresql://admin:${POSTGRES_PASSWORD}@postgres-primary:5432/bizosaas
    restart: unless-stopped

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
EOF

log "✓ Secure Docker Compose configuration created"

echo ""
echo "PHASE 3: CREATE TRAEFIK SECURITY CONFIG"  
echo "======================================="

# Create Traefik configuration with authentication
mkdir -p traefik/config
cat > traefik/config/traefik.yml << 'EOF'
# Traefik Security Configuration
global:
  checkNewVersion: false
  sendAnonymousUsage: false

api:
  dashboard: true
  debug: true

entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https

  websecure:
    address: ":443"
    http:
      tls:
        options: default

certificatesResolvers:
  letsencrypt:
    acme:
      tlsChallenge: {}
      email: admin@bizosaas.com
      storage: /letsencrypt/acme.json
      httpChallenge:
        entryPoint: web

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
    network: web

# Security headers
http:
  middlewares:
    auth:
      basicAuth:
        users:
          - "admin:$2y$10$2b2cu0PfgAEQwkV8rMWQGu8P4dVQVJ4z4p4R7j8LvW8fMZCn8fJ2O"
    
    security-headers:
      headers:
        frameDeny: true
        sslRedirect: true
        browserXssFilter: true
        contentTypeNosniff: true
        forceSTSHeader: true
        stsIncludeSubdomains: true
        stsPreload: true
        stsSeconds: 31536000
        customRequestHeaders:
          X-Forwarded-Proto: https
EOF

log "✓ Traefik security configuration created"

echo ""
echo "PHASE 4: CREATE ENVIRONMENT TEMPLATE"
echo "==================================="

cat > .env.secure.example << 'EOF'
# BizOSaaS Secure Environment Configuration

# Database Configuration
POSTGRES_PASSWORD=your-secure-postgres-password-here
POSTGRES_USER=admin
POSTGRES_DB=bizosaas

# Redis Configuration  
REDIS_PASSWORD=your-secure-redis-password-here

# Application Security
JWT_SECRET=your-jwt-secret-256-bits-minimum-here
ENCRYPTION_KEY=your-encryption-key-here

# External Service API Keys (Optional)
OPENAI_API_KEY=your-openai-key
STRIPE_SECRET_KEY=your-stripe-key

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-admin-password

# Domain Configuration
PRIMARY_DOMAIN=bizosaas.com
WAGTAIL_DOMAIN=admin.bizosaas.com
SALEOR_DOMAIN=shop.coreldove.com
EOF

log "✓ Secure environment template created"

echo ""
echo "PHASE 5: FIREWALL RULES (OPTIONAL)"
echo "================================="

# Create firewall script (not executed automatically for safety)
cat > setup-firewall.sh << 'EOF'
#!/bin/bash
# FIREWALL CONFIGURATION - REVIEW BEFORE EXECUTING
# This script configures UFW (Uncomplicated Firewall)

# WARNING: This can lock you out if not configured properly!
# Make sure you have console access before running

echo "Setting up firewall rules..."

# Reset to defaults
sudo ufw --force reset

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (CRITICAL - don't lock yourself out)
sudo ufw allow ssh

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow unified frontend (authenticated)
sudo ufw allow 3005/tcp

# Allow localhost access to admin interfaces
sudo ufw allow from 127.0.0.1 to any port 3010
sudo ufw allow from 127.0.0.1 to any port 9090

# Block dangerous ports explicitly
sudo ufw deny 5432/tcp
sudo ufw deny 5433/tcp  
sudo ufw deny 5434/tcp
sudo ufw deny 6379/tcp
sudo ufw deny 6380/tcp

# Enable firewall
sudo ufw --force enable

echo "Firewall configured. Check with: sudo ufw status verbose"
EOF

chmod +x setup-firewall.sh
warn "Firewall script created but NOT executed. Review setup-firewall.sh before running!"

echo ""
echo "RECOMMENDED NEXT STEPS"
echo "===================="
echo ""
echo "1. 🔄 IMMEDIATE (Critical Security):"
echo "   - Copy .env.secure.example to .env and configure passwords"
echo "   - Stop current containers: docker-compose down"
echo "   - Start secure containers: docker-compose -f docker-compose.secure.yml up -d"
echo ""
echo "2. 🔒 WITHIN 24 HOURS (Network Security):"  
echo "   - Review and run: ./setup-firewall.sh"
echo "   - Configure SSL certificates for domains"
echo "   - Set up VPN access for admin interfaces"
echo ""
echo "3. 🛡️  WITHIN 1 WEEK (Advanced Security):"
echo "   - Implement monitoring and alerting"
echo "   - Set up automated backups"
echo "   - Configure log aggregation"
echo "   - Implement intrusion detection"
echo ""

echo "🔒 Security audit complete. Review the generated files before proceeding."
EOF