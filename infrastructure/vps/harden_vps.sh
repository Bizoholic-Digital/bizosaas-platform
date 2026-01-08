#!/bin/bash

# BizOSaaS Platform - VPS Hardening & Optimization Script
# Target: Ubuntu 22.04 LTS (Hostinger KVM2)
# Version: 1.0

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Starting VPS Hardening & Optimization...${NC}"

# 1. Update and Upgrade
echo "Updating system packages..."
apt update && apt upgrade -y

# 2. Set Timezone to UTC
timedatectl set-timezone UTC

# 3. Security: Install Essential Security Tools
echo "Installing Fail2Ban and UFW..."
apt install -y fail2ban ufw unattended-upgrades

# 4. Configure Firewall (UFW)
echo "Configuring UFW..."
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow http
ufw allow https
ufw allow 3000/tcp # Dokploy
ufw allow 8080/tcp # Traefik Dashboard (Internal)
ufw allow 8200/tcp # HashiCorp Vault
echo "y" | ufw enable

# 5. Fail2Ban Configuration
echo "Configuring Fail2Ban..."
systemctl enable fail2ban
systemctl start fail2ban

# 6. Optimization: Increase File Descriptors
echo "Optimizing File Descriptors..."
cat <<EOF >> /etc/security/limits.conf
* soft nofile 65535
* hard nofile 65535
EOF

# 7. System Kernel Optimizations (sysctl)
echo "Optimizing Kernel Parameters..."
cat <<EOF > /etc/sysctl.d/99-bizosaas-optimizations.conf
# Maximize Networking Performance
net.core.somaxconn = 65535
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.tcp_fin_timeout = 15
net.ipv4.tcp_tw_reuse = 1
net.ipv4.ip_local_port_range = 1024 65000

# Virtual Memory Optimizations
vm.swappiness = 10
vm.max_map_count = 262144
EOF
sysctl --system

# 8. Install Docker (Required for Dokploy)
echo "Installing Docker..."
apt install -y ca-certificates curl gnupg lsb-release
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 9. Clean up
apt autoremove -y

echo -e "${GREEN}VPS Hardening & Optimization Complete!${NC}"
echo -e "Next Step: Run install_dokploy.sh"
