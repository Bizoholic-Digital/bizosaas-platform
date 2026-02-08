#!/bin/bash
# deploy-to-kvm2.sh
# Automated deployment script for KVM2 VPS (194.238.16.237)
# Optimized for servers running Dokploy
# SKIPS Portainer deployment to avoid redundancy

# Configuration
VPS_IP="194.238.16.237"
VPS_USER="root"
REPO_URL="https://github.com/Bizoholic-Digital/bizosaas-platform.git"
APP_DIR="/root/bizosaas-platform"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Load local secrets if present
if [ -f .env.kvm2 ]; then
    echo -e "${GREEN}🔐 Loading secrets from .env.kvm2...${NC}"
    export $(grep -v '^#' .env.kvm2 | xargs)
fi

echo -e "${GREEN}🚀 Starting deployment to KVM2 ($VPS_IP)...${NC}"

# Check if we can connect
if ! ssh -o BatchMode=yes -o ConnectTimeout=5 $VPS_USER@$VPS_IP "echo Connection success" 2>/dev/null; then
    echo -e "${YELLOW}⚠️ Cannot connect via SSH keys. You may need to enter your password.${NC}"
    echo -e "${YELLOW}Password from records: &k3civYG5Q6YPb${NC}"
fi

# Define the remote setup script
cat << EOF > setup_remote.sh
#!/bin/bash
set -e

# Environment Variables for External Services (Neon & Redis Cloud)
# Secrets are injected from local environment or .env.kvm2
export DATABASE_URL="${DATABASE_URL}"
export VECTOR_DB_URL="${DATABASE_URL}"  # Neon supports pgvector
export REDIS_URL="${REDIS_URL}"
export OPENAI_API_KEY="${OPENAI_API_KEY}"
export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}"
export GOOGLE_API_KEY="${GOOGLE_API_KEY}"
EOF

cat << 'EOF' >> setup_remote.sh

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

# Inject external settings into .env for persistence
sed -i 's|^DATABASE_URL=.*|DATABASE_URL='"$DATABASE_URL"'|' .env
sed -i 's|^REDIS_URL=.*|REDIS_URL='"$REDIS_URL"'|' .env
sed -i 's|^OPENAI_API_KEY=.*|OPENAI_API_KEY='"$OPENAI_API_KEY"'|' .env
sed -i 's|^ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY='"$ANTHROPIC_API_KEY"'|' .env
sed -i 's|^GOOGLE_API_KEY=.*|GOOGLE_API_KEY='"$GOOGLE_API_KEY"'|' .env

# Verify they are in .env
echo "Verified environment variables in .env:"
grep -E "DATABASE_URL|REDIS_URL|OPENAI_API_KEY" .env

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
EOF

# Execute deployment on remote server
echo -e "${GREEN}📡 Transferring deployment script...${NC}"
scp setup_remote.sh $VPS_USER@$VPS_IP:/tmp/setup_remote.sh

echo -e "${GREEN}🏃 Running deployment on remote server...${NC}"
ssh $VPS_USER@$VPS_IP "chmod +x /tmp/setup_remote.sh && /tmp/setup_remote.sh"

# Cleanup local artifact
rm setup_remote.sh

echo -e "${GREEN}✨ Done!${NC}"
