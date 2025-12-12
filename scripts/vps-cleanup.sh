#!/bin/bash
# VPS Cleanup Script for Dokploy Server
# Run this on your VPS to free up disk space and memory

set -e

echo "🧹 BizOSaaS VPS Cleanup Script"
echo "================================"
echo ""

# Function to display disk usage
show_disk_usage() {
    echo "📊 Current Disk Usage:"
    df -h / | tail -1
    echo ""
}

# Function to display memory usage
show_memory_usage() {
    echo "💾 Current Memory Usage:"
    free -h | grep Mem
    echo ""
}

# Display initial stats
echo "BEFORE CLEANUP:"
show_disk_usage
show_memory_usage

# 1. Clean Docker System
echo "🐳 Step 1: Cleaning Docker system..."
echo "Removing stopped containers..."
docker container prune -f

echo "Removing unused images..."
docker image prune -a -f

echo "Removing unused volumes..."
docker volume prune -f

echo "Removing unused networks..."
docker network prune -f

echo "Removing build cache..."
docker builder prune -a -f

echo "✅ Docker cleanup complete"
echo ""

# 2. Clean APT cache
echo "📦 Step 2: Cleaning APT cache..."
apt-get clean
apt-get autoclean
apt-get autoremove -y
echo "✅ APT cleanup complete"
echo ""

# 3. Clean system logs (keep last 7 days)
echo "📝 Step 3: Cleaning old system logs..."
journalctl --vacuum-time=7d
echo "✅ Log cleanup complete"
echo ""

# 4. Clean old Dokploy build artifacts
echo "🗂️  Step 4: Cleaning old Dokploy build artifacts..."
if [ -d "/etc/dokploy/compose" ]; then
    echo "Checking Dokploy compose directories..."
    find /etc/dokploy/compose -type d -name "code" -mtime +7 -exec du -sh {} \; 2>/dev/null || true
    echo "Removing build directories older than 7 days..."
    find /etc/dokploy/compose -type d -name "code" -mtime +7 -exec rm -rf {} \; 2>/dev/null || true
fi
echo "✅ Dokploy cleanup complete"
echo ""

# 5. Clean temporary files
echo "🗑️  Step 5: Cleaning temporary files..."
rm -rf /tmp/*
rm -rf /var/tmp/*
echo "✅ Temp files cleanup complete"
echo ""

# 6. Find large files (for manual review)
echo "🔍 Step 6: Finding largest files (top 20)..."
echo "These files can be reviewed for manual deletion:"
find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null | awk '{ print $9 ": " $5 }' | sort -k2 -hr | head -20
echo ""

# 7. Find large directories
echo "📁 Step 7: Finding largest directories (top 10)..."
du -h --max-depth=2 / 2>/dev/null | sort -hr | head -10
echo ""

# Display final stats
echo ""
echo "AFTER CLEANUP:"
show_disk_usage
show_memory_usage

echo "✅ Cleanup complete!"
echo ""
echo "💡 Recommendations:"
echo "1. If disk usage is still high, review the large files/directories listed above"
echo "2. Consider upgrading VPS storage if consistently above 70%"
echo "3. Set up automated cleanup cron job (see below)"
echo ""
echo "To set up weekly automated cleanup, run:"
echo "echo '0 2 * * 0 /bin/bash $(pwd)/vps-cleanup.sh > /var/log/vps-cleanup.log 2>&1' | crontab -"
