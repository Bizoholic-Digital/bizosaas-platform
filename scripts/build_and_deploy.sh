#!/bin/bash
set -e

REPO_DIR="/root/bizosaas-platform"
REPO_URL="https://github.com/Bizoholic-Digital/bizosaas-platform.git"

print_msg() {
    echo "============================================================"
    echo "$1"
    echo "============================================================"
}

if [ ! -d "$REPO_DIR" ]; then
    print_msg "Cloning repository..."
    git clone -b staging "$REPO_URL" "$REPO_DIR"
else
    print_msg "Updating repository..."
    cd "$REPO_DIR"
    git fetch origin
    git reset --hard origin/staging
fi

cd "$REPO_DIR"

print_msg "Building Brain Gateway..."
docker build -t ghcr.io/bizoholic-digital/bizosaas-platform/brain-gateway:staging ./bizosaas-brain-core/brain-gateway

declare -A MCPS=(
    ["brave-search"]="brave-search-mcp"
    ["filesystem"]="filesystem-mcp"
    ["github"]="github-mcp"
    ["google-ads"]="google-ads-mcp"
    ["google-drive"]="google-drive-mcp"
    ["s3-storage"]="s3-storage-mcp"
    ["slack"]="slack-mcp"
    ["fluent-crm"]="fluentcrm-mcp"
)

for dir in "${!MCPS[@]}"; do
    image_name="${MCPS[$dir]}"
    print_msg "Building MCP: $dir -> $image_name"
    if [ -d "./mcp-servers/$dir" ]; then
        docker build -t ghcr.io/bizoholic-digital/bizosaas-platform/$image_name:staging ./mcp-servers/$dir
    else
        echo "Warning: Directory mcp-servers/$dir not found"
    fi
done

print_msg "Deploying services via Dokploy..."
if [ -f "scripts/deploy_all_services.py" ]; then
    pip3 install requests || true
    python3 scripts/deploy_all_services.py
else
    echo "Error: Deployment script not found!"
    exit 1
fi

print_msg "Success!"
