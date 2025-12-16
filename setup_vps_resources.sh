#!/bin/bash

# 1. Setup Swap (4GB) to prevent OOM
if [ ! -f /swapfile ]; then
    echo "Creating 4GB Swap file..."
    fallocate -l 4G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' | tee -a /etc/fstab
    echo "Swap created."
else
    echo "Swap file already exists."
fi

# 2. Adjust Swappiness (Use RAM mostly, swap only when needed)
sysctl vm.swappiness=10
echo 'vm.swappiness=10' | tee -a /etc/sysctl.conf

# 3. Clean Docker Build Cache
echo "Pruning Docker system to free space..."
docker system prune -af --volumes

echo "VPS Resource Optimization Complete."
free -h
