#!/bin/bash
# VPS Cleanup Script - Keep disk usage low
# Run this via cron or manually: 0 4 * * * /path/to/vps-cleanup.sh

echo "🧹 Starting VPS Cleanup..."
date

# 1. Prune unused images (dangling)
echo "🗑️  Pruning unused images..."
docker image prune -f

# 2. Prune stopped containers (older than 24h)
echo "🗑️  Pruning stopped containers..."
docker container prune -f --filter "until=24h"

# 3. Check disk usage
echo "📊 Disk Usage:"
df -h / | grep /

# 4. Alert if disk usage > 80% (Optional: add email/webhook)
USAGE=$(df / | grep / | awk '{ print $5 }' | sed 's/%//g')
if [ "$USAGE" -gt 80 ]; then
    echo "⚠️  WARNING: High Disk Usage ($USAGE%)"
    # Add your alert command here
fi

echo "✅ Cleanup complete."
