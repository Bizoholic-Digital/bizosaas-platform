#!/bin/bash

# BizOSaaS Platform - Dokploy Installation Script
# Target: Ubuntu 22.04 LTS (Hostinger KVM2)
# Version: 1.0

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}BizOSaaS Platform - Dokploy Setup${NC}"

# Check for Docker
if ! [ -x "$(command -v docker)" ]; then
  echo 'Error: Docker is not installed. Please run harden_vps.sh first.' >&2
  exit 1
fi

# 1. Install Dokploy using the official script
echo "Installing Dokploy..."
curl -sSL https://dokploy.com/install.sh | sh

echo -e "${GREEN}Dokploy Installation initiated!${NC}"
echo -e "Wait a few moments, then access Dokploy at: http://YOUR_VPS_IP:3000"
echo -e "After initial setup, please configure Traefik in the Dokploy settings."
