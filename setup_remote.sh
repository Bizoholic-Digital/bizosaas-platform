#!/bin/bash
set -e

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}🔄 Updating system packages...${NC}"
export DEBIAN_FRONTEND=noninteractive
apt-get update && apt-get upgrade -y

echo -e "${GREEN}🐳 Checking Docker installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
else
    echo "Docker is already installed."
fi

# Clone or pull repository
echo -e "${GREEN}📦 Fetching application code...${NC}"
if [ -d "/root/bizosaas-platform" ]; then
    cd /root/bizosaas-platform
    echo "Repository exists. Pulling latest changes..."
    git config --global --add safe.directory /root/bizosaas-platform
    git reset --hard
    git pull origin staging --force
else
    cd /root
    echo "Cloning repository..."
    git clone -b staging https://github.com/Bizoholic-Digital/bizosaas-platform.git
fi

cd /root/bizosaas-platform

echo -e "${GREEN}⚙️ Configuring environment...${NC}"
if [ ! -f .env ]; then
    echo "Creating .env from example..."
    cp .env.example .env
fi

echo -e "${GREEN}🧹 Cleaning up old resources...${NC}"
chmod +x scripts/cleanup-docker-resources.sh 2>/dev/null || true
if [ -f scripts/cleanup-docker-resources.sh ]; then
    ./scripts/cleanup-docker-resources.sh
fi

echo -e "${GREEN}🚀 Starting services...${NC}"
# Use the robust startup script
# Note: We keep Portainer in the yaml but prevent it from binding if needed, 
# or we let it run on 9001 since Dokploy uses internal management.
# Our config maps Portainer to 9001/9444, so it won't conflict with Dokploy (usually port 3000).

./scripts/start-bizosaas-core-full.sh --wait

echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo "----------------------------------------"
echo "Client Portal: http://194.238.16.237:3003"
echo "Brain Gateway: http://194.238.16.237:8000"
echo "Auth Service:  http://194.238.16.237:8009"
echo "Authentik:     http://194.238.16.237:9000"
echo "Dokploy:       http://194.238.16.237:3000 (Existing)"
echo "----------------------------------------"
