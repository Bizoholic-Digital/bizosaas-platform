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
