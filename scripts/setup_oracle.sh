#!/bin/bash
# Oracle Cloud & Coolify Setup Script
# Version 1.0

set -e

echo "Starting BizOSaaS Server Setup on Oracle Cloud (ARM64)..."

# 1. System Updates
echo "Updating System..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git wget unzip htop
echo "iptables-persistent iptables-persistent/autosave_v4 boolean true" | sudo debconf-set-selections
echo "iptables-persistent iptables-persistent/autosave_v6 boolean true" | sudo debconf-set-selections
sudo DEBIAN_FRONTEND=noninteractive apt install -y iptables-persistent netfilter-persistent

# 2. Firewall Configuration (Oracle iptables)
echo "Configuring Firewall..."
# Allow HTTP, HTTPS, SSH, Coolify (8000), Portal (3003), Auth (8008)
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 22 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8000 -j ACCEPT # Coolify UI
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 6001 -j ACCEPT # Coolify Webhooks
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 3003 -j ACCEPT # Client Portal
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8008 -j ACCEPT # Auth Service
sudo netfilter-persistent save || echo "netfilter-persistent not found, please ensure rules are saved."

# 3. Install Docker (Coolify needs it, but Coolify installer also does it. We do it to be safe)
echo "Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    sudo usermod -aG docker ubuntu
    echo "Docker installed."
else
    echo "Docker already installed."
fi

# 4. Install Coolify
echo "Installing Coolify..."
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash

echo "-----------------------------------------------------"
echo "Setup Complete!"
echo "You can access Coolify at: http://$(curl -s ifconfig.me):8000"
echo "Please register your admin account immediately."
echo "-----------------------------------------------------"
