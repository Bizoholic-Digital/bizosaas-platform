#!/bin/bash
# Optimize Docker Storage - Move data to HDD
# Usage: sudo ./scripts/optimize-docker-storage.sh /path/to/hdd/docker-data

set -e

if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root (sudo)"
  exit 1
fi

TARGET_DIR=$1

if [ -z "$TARGET_DIR" ]; then
    echo "⚠️  Usage: sudo $0 <path-to-new-docker-data-dir>"
    echo "   Example: sudo $0 /mnt/hdd/docker-data"
    exit 1
fi

# WSL2 Check
if grep -q "microsoft" /proc/version; then
    echo "⚠️  WSL2 Detected!"
    echo "   If your WSL2 VM is already on the HDD (e.g., D:\vm), you do NOT need to run this."
    echo "   Moving Docker data to a Windows mount (/mnt/d/...) causes SEVERE performance issues."
    echo ""
    read -p "❓ Are you SURE you want to proceed? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "🚀 Moving Docker data to $TARGET_DIR..."

# 1. Stop Docker
echo "🛑 Stopping Docker service..."
systemctl stop docker

# 2. Create target directory
echo "📂 Creating target directory..."
mkdir -p "$TARGET_DIR"

# 3. Configure daemon.json
echo "⚙️  Configuring /etc/docker/daemon.json..."
if [ ! -f /etc/docker/daemon.json ]; then
    echo "{}" > /etc/docker/daemon.json
fi

# Use jq or python to update json safely, or simple sed if jq not available
# Here we'll use a temporary python script for reliability
python3 -c "
import json
import os

config_path = '/etc/docker/daemon.json'
target_dir = '$TARGET_DIR'

try:
    with open(config_path, 'r') as f:
        data = json.load(f)
except Exception:
    data = {}

data['data-root'] = target_dir

with open(config_path, 'w') as f:
    json.dump(data, f, indent=4)
"

# 4. Sync data (Optional - ask user)
read -p "❓ Do you want to move existing images/containers to new location? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 Moving data (this may take a while)..."
    rsync -aqxP /var/lib/docker/ "$TARGET_DIR"
fi

# 5. Start Docker
echo "▶️  Starting Docker service..."
systemctl start docker

echo "✅ Docker storage moved to $TARGET_DIR"
docker info | grep "Docker Root Dir"
