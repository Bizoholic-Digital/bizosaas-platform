#!/bin/bash
# BizOSaaS Platform Pre-Startup Dependency Check
# Validates all required dependencies before starting the platform
# Author: Claude AI Assistant
# Created: 2025-09-29

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if service is running
service_running() {
    systemctl is-active --quiet "$1" 2>/dev/null
}

# Check if port is available
port_available() {
    nc -z localhost "$1" >/dev/null 2>&1
}

# Main dependency check
main() {
    log "=== BizOSaaS Platform Dependency Check ==="
    
    local issues=0
    
    # Check Docker
    log "Checking Docker..."
    if command_exists docker; then
        if service_running docker; then
            log_success "Docker service is running"
        else
            log_error "Docker service is not running"
            log "  Fix with: sudo systemctl start docker"
            issues=$((issues + 1))
        fi
        
        # Check Docker permissions
        if docker info >/dev/null 2>&1; then
            log_success "Docker permissions are correct"
        else
            log_error "Docker permissions issue - user may not be in docker group"
            log "  Fix with: sudo usermod -aG docker \$USER && newgrp docker"
            issues=$((issues + 1))
        fi
    else
        log_error "Docker is not installed"
        log "  Install with: curl -fsSL https://get.docker.com | sh"
        issues=$((issues + 1))
    fi
    
    # Check Docker Compose
    log "Checking Docker Compose..."
    if command_exists docker-compose; then
        log_success "Docker Compose is available"
    elif docker compose version >/dev/null 2>&1; then
        log_success "Docker Compose (plugin) is available"
    else
        log_error "Docker Compose is not available"
        log "  Install with: sudo apt install docker-compose-plugin"
        issues=$((issues + 1))
    fi
    
    # Check PostgreSQL
    log "Checking PostgreSQL..."
    if command_exists psql; then
        if service_running postgresql; then
            if port_available 5432; then
                log_success "PostgreSQL is running on port 5432"
            else
                log_error "PostgreSQL service is active but port 5432 is not available"
                issues=$((issues + 1))
            fi
        else
            log_error "PostgreSQL service is not running"
            log "  Fix with: sudo systemctl start postgresql"
            issues=$((issues + 1))
        fi
    else
        log_error "PostgreSQL is not installed"
        log "  Install with: sudo apt install postgresql postgresql-contrib"
        issues=$((issues + 1))
    fi
    
    # Check Redis
    log "Checking Redis..."
    if command_exists redis-cli; then
        if service_running redis; then
            if port_available 6379; then
                log_success "Redis is running on port 6379"
            else
                log_error "Redis service is active but port 6379 is not available"
                issues=$((issues + 1))
            fi
        else
            log_error "Redis service is not running"
            log "  Fix with: sudo systemctl start redis"
            issues=$((issues + 1))
        fi
    else
        log_error "Redis is not installed"
        log "  Install with: sudo apt install redis-server"
        issues=$((issues + 1))
    fi
    
    # Check required directories
    log "Checking required directories..."
    local required_dirs=(
        "/home/alagiri/projects/bizoholic/bizosaas"
        "/home/alagiri/projects/bizoholic/bizosaas/scripts"
    )
    
    for dir in "${required_dirs[@]}"; do
        if [ -d "$dir" ]; then
            log_success "Directory exists: $dir"
        else
            log_error "Missing directory: $dir"
            issues=$((issues + 1))
        fi
    done
    
    # Check Docker Compose file
    log "Checking Docker Compose configuration..."
    local compose_file="/home/alagiri/projects/bizoholic/bizosaas/docker-compose.bizosaas-platform.yml"
    if [ -f "$compose_file" ]; then
        log_success "Docker Compose file found"
        
        # Validate compose file
        if docker-compose -f "$compose_file" config >/dev/null 2>&1; then
            log_success "Docker Compose file is valid"
        else
            log_error "Docker Compose file has syntax errors"
            log "  Check with: docker-compose -f $compose_file config"
            issues=$((issues + 1))
        fi
    else
        log_error "Docker Compose file not found: $compose_file"
        issues=$((issues + 1))
    fi
    
    # Check environment variables
    log "Checking environment variables..."
    local required_env_vars=(
        "HOME"
        "USER"
    )
    
    for var in "${required_env_vars[@]}"; do
        if [ -n "${!var}" ]; then
            log_success "Environment variable set: $var"
        else
            log_warning "Environment variable not set: $var"
        fi
    done
    
    # Check network connectivity
    log "Checking network connectivity..."
    if ping -c 1 google.com >/dev/null 2>&1; then
        log_success "Internet connectivity is available"
    else
        log_warning "Internet connectivity may be limited"
    fi
    
    # Check disk space
    log "Checking disk space..."
    local available_gb=$(df -BG /home/alagiri/projects/bizoholic/bizosaas | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "$available_gb" -gt 10 ]; then
        log_success "Sufficient disk space available (${available_gb}GB)"
    else
        log_warning "Low disk space: ${available_gb}GB available"
        if [ "$available_gb" -lt 5 ]; then
            log_error "Critically low disk space - may cause startup issues"
            issues=$((issues + 1))
        fi
    fi
    
    # Check memory
    log "Checking memory..."
    local available_mb=$(free -m | awk 'NR==2{printf "%.0f", $7}')
    if [ "$available_mb" -gt 2048 ]; then
        log_success "Sufficient memory available (${available_mb}MB)"
    else
        log_warning "Low memory: ${available_mb}MB available"
        if [ "$available_mb" -lt 1024 ]; then
            log_error "Critically low memory - may cause startup issues"
            issues=$((issues + 1))
        fi
    fi
    
    # Final summary
    echo
    log "=== Dependency Check Summary ==="
    if [ $issues -eq 0 ]; then
        log_success "All dependencies are satisfied - platform is ready to start"
        exit 0
    else
        log_error "Found $issues issue(s) that need to be resolved"
        log "Please fix the above issues before starting the platform"
        exit 1
    fi
}

# Run the check
main "$@"