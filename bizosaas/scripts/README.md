# BizOSaaS Platform System Restart Scripts

This directory contains scripts to ensure all required containers are up and running when the system restarts.

## Scripts Overview

### 1. `startup-system.sh` - Main Platform Control Script
**Purpose**: Controls the entire BizOSaaS platform startup, shutdown, and monitoring.

**Key Features**:
- Dependency-aware startup (starts services in correct order)
- Health monitoring and validation  
- Support for both production and development modes
- Comprehensive logging and status reporting
- Individual service log viewing

**Usage**:
```bash
# Start the platform (recommended)
./startup-system.sh start

# Start with development services
./startup-system.sh start-dev  

# Stop all services
./startup-system.sh stop

# Restart the platform
./startup-system.sh restart

# Check current status
./startup-system.sh status

# View logs for a specific service
./startup-system.sh logs bizosaas-brain-unified

# Perform health check
./startup-system.sh health
```

### 2. `pre-startup-check.sh` - Dependency Validation
**Purpose**: Validates all system dependencies before platform startup.

**Checks**:
- Docker installation and permissions
- Docker Compose availability
- PostgreSQL service status
- Redis service status
- Required directories and files
- System resources (disk space, memory)
- Network connectivity

**Usage**:
```bash
# Run dependency check
./pre-startup-check.sh
```

### 3. `install-service.sh` - System Service Setup
**Purpose**: Sets up BizOSaaS as a systemd service for automatic startup.

**Features**:
- Creates systemd service for automatic platform startup
- Sets up proper Docker permissions
- Enables/disables service management
- Service status monitoring

**Usage**:
```bash
# Install systemd service (run once)
./install-service.sh install

# Check service status
./install-service.sh status

# Uninstall service
./install-service.sh uninstall

# Set up Docker permissions
./install-service.sh permissions
```

### 4. `bizosaas-platform.service` - Systemd Service Configuration
**Purpose**: Systemd service definition for automatic platform management.

**Features**:
- Automatic startup on system boot
- Dependency management (requires Docker, PostgreSQL, Redis)
- Proper user and security settings
- Logging integration with systemd journal

## Service Architecture

### Startup Sequence
The platform starts services in dependency order:

1. **External Dependencies**: PostgreSQL, Redis (must be running on host)
2. **Core Infrastructure**: Database and cache containers
3. **Backend Services**: APIs, workers, and business logic services
4. **Frontend Services**: Web applications and user interfaces
5. **Development Services** (optional): Development tools and debugging services

### Service Groups

#### Core Infrastructure Services
- `bizosaas-saleor-db` - E-commerce database
- `bizosaas-saleor-redis` - E-commerce cache
- `bizosaas-superset-db` - Analytics database

#### Backend Services  
- `bizosaas-brain` - Central AI hub
- `bizosaas-auth-v2` - Authentication service
- `bizosaas-django-crm` - CRM system
- `bizosaas-wagtail-cms` - Content management
- `bizosaas-saleor-api` - E-commerce API
- `bizosaas-vault` - Secrets management
- `bizosaas-data-sync` - Data synchronization

#### Frontend Services
- `bizosaas-client-portal` - Client dashboard
- `bizosaas-coreldove-frontend` - E-commerce frontend
- `bizosaas-bizoholic-frontend` - Marketing frontend
- `bizosaas-admin` - Administration interface

#### Development Services (Optional)
- Various development containers for testing and debugging
- Amazon sourcing service
- Business directory services
- AI agents testing

## Installation & Setup

### Step 1: Run Dependency Check
```bash
cd /home/alagiri/projects/bizoholic/bizosaas/scripts
./pre-startup-check.sh
```

Fix any issues reported by the dependency check.

### Step 2: Test Manual Startup
```bash
# Test the startup script manually first
./startup-system.sh start

# Check if services started correctly
./startup-system.sh status
```

### Step 3: Install System Service (Optional)
```bash
# Install for automatic startup on system boot
./install-service.sh install

# Check service status
sudo systemctl status bizosaas-platform
```

## System Service Management

Once installed as a systemd service, you can manage the platform using standard systemctl commands:

```bash
# Start the platform
sudo systemctl start bizosaas-platform

# Stop the platform  
sudo systemctl stop bizosaas-platform

# Restart the platform
sudo systemctl restart bizosaas-platform

# Check service status
sudo systemctl status bizosaas-platform

# View service logs
journalctl -u bizosaas-platform -f

# Enable automatic startup (already done during install)
sudo systemctl enable bizosaas-platform

# Disable automatic startup
sudo systemctl disable bizosaas-platform
```

## Troubleshooting

### Common Issues

#### 1. Permission Denied Errors
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

#### 2. PostgreSQL Not Running
```bash
# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql  # Enable auto-start
```

#### 3. Redis Not Running
```bash
# Start Redis service  
sudo systemctl start redis
sudo systemctl enable redis  # Enable auto-start
```

#### 4. Port Conflicts
Check if required ports are available:
```bash
# Check port usage
netstat -tlnp | grep :8001
netstat -tlnp | grep :5432
netstat -tlnp | grep :6379
```

#### 5. Container Health Issues
```bash
# Check specific container logs
./startup-system.sh logs [container-name]

# Example: Check brain service logs
./startup-system.sh logs bizosaas-brain-unified
```

#### 6. Docker Compose File Issues
```bash
# Validate compose file syntax
docker-compose -f /home/alagiri/projects/bizoholic/bizosaas/docker-compose.bizosaas-platform.yml config
```

### Health Check Interpretation

The health check script provides color-coded output:
- **Green (✓)**: Component is healthy
- **Yellow (⚠)**: Warning - may need attention
- **Red (✗)**: Critical issue - must be fixed

### Log Analysis

View comprehensive logs for debugging:
```bash
# Platform service logs (if using systemd)
journalctl -u bizosaas-platform -f

# Individual container logs
docker logs bizosaas-brain-unified --tail 50

# All platform container logs
docker-compose -f docker-compose.bizosaas-platform.yml logs --tail 50
```

## Customization

### Environment Variables
Create `.env` file in the platform root with required variables:
```bash
JWT_SECRET=your-secret-key
OPENAI_API_KEY=your-openai-key
SALEOR_DB_PASSWORD=secure-password
# ... other variables
```

### Service Configuration
Modify `docker-compose.bizosaas-platform.yml` to:
- Change port mappings
- Add new services
- Modify resource limits
- Update environment variables

### Startup Script Customization
Edit `startup-system.sh` to:
- Modify service groups
- Change health check timeouts
- Add custom validation steps
- Adjust startup sequences

## Monitoring & Maintenance

### Regular Health Checks
```bash
# Run weekly health checks
./startup-system.sh health

# Check system resources
./pre-startup-check.sh
```

### Log Rotation
Systemd automatically handles log rotation for the platform service. For container logs:
```bash
# Configure Docker log rotation in daemon.json
sudo vim /etc/docker/daemon.json
```

### Updates and Maintenance
```bash
# Stop platform for maintenance
./startup-system.sh stop

# Update containers (rebuild images)
docker-compose -f docker-compose.bizosaas-platform.yml build --no-cache

# Restart platform
./startup-system.sh start
```

This comprehensive system ensures your BizOSaaS platform reliably starts and runs after system restarts, with proper dependency management and health monitoring.