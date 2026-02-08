#!/bin/bash

# WSL Docker Cleanup and Maintenance Script
# This script helps maintain a clean WSL environment

set -e

echo "======================================"
echo "WSL Docker Cleanup & Maintenance"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

print_status "Docker is running"
echo ""

# Show current disk usage
echo "Current Docker Disk Usage:"
echo "=========================="
docker system df
echo ""

# Ask for confirmation
read -p "Do you want to proceed with cleanup? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Cleanup cancelled"
    exit 0
fi

echo ""
print_status "Starting cleanup..."
echo ""

# Stop all running containers (optional)
read -p "Stop all running containers? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    RUNNING=$(docker ps -q)
    if [ -n "$RUNNING" ]; then
        print_status "Stopping running containers..."
        docker stop $RUNNING
    else
        print_status "No running containers to stop"
    fi
fi
echo ""

# Remove stopped containers
print_status "Removing stopped containers..."
REMOVED_CONTAINERS=$(docker container prune -f 2>&1 | grep "Total reclaimed space" || echo "0B")
echo "  $REMOVED_CONTAINERS"
echo ""

# Remove unused images
print_status "Removing unused images..."
REMOVED_IMAGES=$(docker image prune -a -f 2>&1 | grep "Total reclaimed space" || echo "0B")
echo "  $REMOVED_IMAGES"
echo ""

# Remove unused volumes
print_status "Removing unused volumes..."
REMOVED_VOLUMES=$(docker volume prune -f 2>&1 | grep "Total reclaimed space" || echo "0B")
echo "  $REMOVED_VOLUMES"
echo ""

# Remove build cache
print_status "Removing build cache..."
REMOVED_CACHE=$(docker builder prune -a -f 2>&1 | grep "Total reclaimed space" || echo "0B")
echo "  $REMOVED_CACHE"
echo ""

# Remove unused networks
print_status "Removing unused networks..."
docker network prune -f > /dev/null 2>&1
echo ""

# Show final disk usage
echo "Final Docker Disk Usage:"
echo "========================"
docker system df
echo ""

# System information
echo "System Information:"
echo "==================="
echo "Disk Space:"
df -h / | tail -1
echo ""
echo "Memory Usage:"
free -h | grep "Mem:"
echo ""

# Check for zombie processes
ZOMBIES=$(ps aux | awk '$8 ~ /Z/ {print}' | wc -l)
if [ $ZOMBIES -gt 0 ]; then
    print_warning "Found $ZOMBIES zombie process(es) - usually harmless"
else
    print_status "No zombie processes found"
fi
echo ""

# Port usage
LISTENING_PORTS=$(ss -tulpn | grep LISTEN | wc -l)
print_status "Listening ports: $LISTENING_PORTS"
echo ""

print_status "Cleanup completed successfully!"
echo ""
echo "Recommendations:"
echo "================"
echo "1. Run this script monthly to keep your system clean"
echo "2. Monitor disk usage with: docker system df"
echo "3. Check running containers with: docker ps"
echo "4. View logs with: docker logs <container_name>"
echo ""
