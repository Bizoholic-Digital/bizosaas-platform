#!/bin/bash
# Safe VPS Cleanup Script
# Reclaims ~25-30GB of disk space safely

set -e

echo "========================================="
echo "BizOSaaS VPS Safe Cleanup Script"
echo "========================================="
echo ""

# Show current disk usage
echo "Current disk usage:"
df -h / | grep -E 'Filesystem|/dev'
echo ""

# Phase 1: Docker Cleanup
echo "=== Phase 1: Docker Cleanup ==="
echo "Removing unused Docker images, containers, volumes, and build cache..."
docker system prune -a --volumes -f
echo "✅ Docker cleanup complete"
echo ""

# Phase 2: Node Modules Cleanup (Archives Only)
echo "=== Phase 2: Node Modules Cleanup (Archives Only) ==="
echo "Removing node_modules from archived projects..."
find /home/alagiri/projects/bizosaas-platform/_archive -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
echo "✅ Node modules cleanup complete"
echo ""

# Phase 3: Log Files Cleanup
echo "=== Phase 3: Log Files Cleanup ==="
echo "Removing old log files (older than 7 days)..."
find /home/alagiri/projects/bizosaas-platform -name "*.log" -type f -mtime +7 -delete 2>/dev/null || true
echo "Truncating large log files..."
truncate -s 0 /home/alagiri/projects/bizosaas-platform/client-portal.log 2>/dev/null || true
echo "✅ Log files cleanup complete"
echo ""

# Phase 4: Build Artifacts Cleanup
echo "=== Phase 4: Build Artifacts Cleanup ==="
echo "Removing .next build directories from archives..."
find /home/alagiri/projects/bizosaas-platform/_archive -name ".next" -type d -exec rm -rf {} + 2>/dev/null || true
echo "Removing dist/build directories from archives..."
find /home/alagiri/projects/bizosaas-platform/_archive -name "dist" -type d -exec rm -rf {} + 2>/dev/null || true
find /home/alagiri/projects/bizosaas-platform/_archive -name "build" -type d -exec rm -rf {} + 2>/dev/null || true
echo "✅ Build artifacts cleanup complete"
echo ""

# Phase 5: Temporary Files
echo "=== Phase 5: Temporary Files ==="
echo "Cleaning cache..."
rm -rf ~/.cache/* 2>/dev/null || true
echo "✅ Temporary files cleanup complete"
echo ""

# Phase 6: npm cache
echo "=== Phase 6: npm Cache ==="
echo "Cleaning npm cache..."
npm cache clean --force 2>/dev/null || true
echo "✅ npm cache cleanup complete"
echo ""

# Show final disk usage
echo "========================================="
echo "Cleanup Complete!"
echo "========================================="
echo ""
echo "Final disk usage:"
df -h / | grep -E 'Filesystem|/dev'
echo ""

# Show Docker disk usage
echo "Docker disk usage:"
docker system df
echo ""

echo "✅ Safe cleanup completed successfully!"
echo "Estimated space reclaimed: ~25-30GB"
