#!/bin/bash
# VPS Emergency Cleanup Script
# Run this on the VPS to free disk space immediately

set -e

echo "=================================================="
echo "VPS Emergency Cleanup Script"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root (use: sudo bash cleanup.sh)"
    exit 1
fi

# 1. Show current disk usage
echo "=== Current Disk Usage ==="
df -h /
echo ""

BEFORE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
print_warning "Disk usage BEFORE cleanup: ${BEFORE}%"
echo ""

# 2. Clean Docker
echo "=== Cleaning Docker Resources ==="
print_status "Removing unused Docker images, containers, and volumes..."
docker system prune -a --volumes -f 2>&1 | tail -5
echo ""

# 3. Remove dangling images
print_status "Removing dangling images..."
docker images -f "dangling=true" -q | xargs -r docker rmi -f 2>/dev/null || true
echo ""

# 4. Clean build cache
print_status "Cleaning Docker build cache..."
docker builder prune -a -f 2>&1 | tail -3
echo ""

# 5. Clean system logs
echo "=== Cleaning System Logs ==="
print_status "Vacuuming journal logs (keeping last 7 days)..."
journalctl --vacuum-time=7d 2>&1 | tail -3
journalctl --vacuum-size=500M 2>&1 | tail -3
echo ""

# 6. Clean APT cache
echo "=== Cleaning APT Cache ==="
print_status "Cleaning package manager cache..."
apt-get clean -y 2>&1 | tail -3
apt-get autoclean -y 2>&1 | tail -3
apt-get autoremove -y 2>&1 | tail -5
echo ""

# 7. Clean temporary files
echo "=== Cleaning Temporary Files ==="
print_status "Removing old temporary files..."
find /tmp -type f -atime +7 -delete 2>/dev/null || true
find /var/tmp -type f -atime +7 -delete 2>/dev/null || true
echo ""

# 8. Show final disk usage
echo "=== Final Disk Usage ==="
df -h /
echo ""

AFTER=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
FREED=$((BEFORE - AFTER))

print_status "Disk usage AFTER cleanup: ${AFTER}%"
print_status "Space freed: ${FREED}%"
echo ""

# 9. Show largest directories (for manual review)
echo "=== Largest Directories (Top 10) ==="
du -h --max-depth=1 /var/lib 2>/dev/null | sort -hr | head -10
echo ""

# 10. Docker stats
echo "=== Docker Disk Usage ==="
docker system df
echo ""

# 11. Recommendations
echo "=================================================="
echo "Cleanup Complete!"
echo "=================================================="
echo ""

if [ $AFTER -gt 80 ]; then
    print_error "WARNING: Disk usage still above 80%"
    echo "Consider:"
    echo "  1. Upgrading VPS disk space"
    echo "  2. Removing old Docker images manually"
    echo "  3. Checking for large log files: du -sh /var/log/*"
elif [ $AFTER -gt 70 ]; then
    print_warning "Disk usage is moderate (${AFTER}%)"
    echo "Monitor regularly and consider upgrading soon"
else
    print_status "Disk usage is healthy (${AFTER}%)"
fi

echo ""
echo "Next steps:"
echo "  1. Restart services if needed: systemctl restart docker"
echo "  2. Check service status: docker ps"
echo "  3. Monitor disk: watch -n 5 'df -h /'"
echo ""
