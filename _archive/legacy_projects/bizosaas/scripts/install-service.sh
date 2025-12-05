#!/bin/bash
# BizOSaaS Platform Service Installation Script
# Sets up systemd service for automatic platform startup
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
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_error "This script should NOT be run as root"
        log "Run as the regular user (alagiri) and it will prompt for sudo when needed"
        exit 1
    fi
}

# Install systemd service
install_service() {
    local service_file="/home/alagiri/projects/bizoholic/bizosaas/scripts/bizosaas-platform.service"
    local target_file="/etc/systemd/system/bizosaas-platform.service"
    
    log "Installing BizOSaaS Platform systemd service..."
    
    # Copy service file
    sudo cp "$service_file" "$target_file"
    log_success "Service file copied to $target_file"
    
    # Reload systemd
    sudo systemctl daemon-reload
    log_success "Systemd daemon reloaded"
    
    # Enable service
    sudo systemctl enable bizosaas-platform.service
    log_success "Service enabled for automatic startup"
    
    log "Service installation completed!"
    log "You can now use:"
    log "  sudo systemctl start bizosaas-platform    # Start the platform"
    log "  sudo systemctl stop bizosaas-platform     # Stop the platform"
    log "  sudo systemctl restart bizosaas-platform  # Restart the platform"
    log "  sudo systemctl status bizosaas-platform   # Check status"
    log "  journalctl -u bizosaas-platform -f        # View logs"
}

# Uninstall systemd service
uninstall_service() {
    log "Uninstalling BizOSaaS Platform systemd service..."
    
    # Stop and disable service
    sudo systemctl stop bizosaas-platform.service 2>/dev/null || true
    sudo systemctl disable bizosaas-platform.service 2>/dev/null || true
    
    # Remove service file
    sudo rm -f /etc/systemd/system/bizosaas-platform.service
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    log_success "Service uninstalled successfully"
}

# Show service status
show_status() {
    log "BizOSaaS Platform Service Status:"
    echo
    
    if systemctl is-enabled bizosaas-platform.service >/dev/null 2>&1; then
        log_success "Service is installed and enabled"
        
        if systemctl is-active bizosaas-platform.service >/dev/null 2>&1; then
            log_success "Service is currently running"
        else
            log_warning "Service is installed but not running"
        fi
        
        echo
        systemctl status bizosaas-platform.service --no-pager || true
    else
        log_warning "Service is not installed"
        log "Run: $0 install"
    fi
}

# Add user to docker group
setup_docker_permissions() {
    log "Setting up Docker permissions..."
    
    if groups "$USER" | grep -q docker; then
        log_success "User $USER is already in the docker group"
    else
        log "Adding user $USER to docker group..."
        sudo usermod -aG docker "$USER"
        log_success "User added to docker group"
        log_warning "You need to log out and log back in for group changes to take effect"
        log "Or run: newgrp docker"
    fi
}

# Main installation function
main() {
    log "=== BizOSaaS Platform Service Installer ==="
    
    check_root
    
    case "${1:-help}" in
        "install")
            # Run dependency check first
            if /home/alagiri/projects/bizoholic/bizosaas/scripts/pre-startup-check.sh; then
                log_success "Dependency check passed"
                setup_docker_permissions
                install_service
            else
                log_error "Dependency check failed - please fix issues before installing"
                exit 1
            fi
            ;;
        "uninstall")
            uninstall_service
            ;;
        "status")
            show_status
            ;;
        "check")
            /home/alagiri/projects/bizoholic/bizosaas/scripts/pre-startup-check.sh
            ;;
        "permissions")
            setup_docker_permissions
            ;;
        "help"|"-h"|"--help")
            echo "BizOSaaS Platform Service Installer"
            echo
            echo "Usage: $0 [COMMAND]"
            echo
            echo "Commands:"
            echo "  install      Install systemd service and dependencies"
            echo "  uninstall    Remove systemd service"
            echo "  status       Show current service status"
            echo "  check        Run dependency check"
            echo "  permissions  Set up Docker permissions"
            echo "  help         Show this help message"
            echo
            echo "Examples:"
            echo "  $0 install     # Install the service"
            echo "  $0 status      # Check service status"
            echo "  $0 uninstall   # Remove the service"
            ;;
        *)
            log_error "Unknown command: $1"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

main "$@"