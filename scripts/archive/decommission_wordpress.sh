#!/bin/bash
# WordPress Decommissioning Script
# Removes Coreldove and Bizoholic WordPress containers after backup

echo "=== WordPress Decommissioning ==="
echo ""

# 1. Stop and remove Coreldove
echo "Removing Coreldove containers..."
docker stop coreldovewebsite-wordpress-fnoyyo-wordpress-1 coreldovewebsite-wordpress-fnoyyo-wp_db-1
docker rm coreldovewebsite-wordpress-fnoyyo-wordpress-1 coreldovewebsite-wordpress-fnoyyo-wp_db-1
echo "✅ Coreldove removed"
echo ""

# 2. Stop and remove Bizoholic
echo "Removing Bizoholic containers..."
docker stop bizoholicwebsite-wordpress-rbtyli-wordpress-1 bizoholicwebsite-wordpress-rbtyli-wp_db-1
docker rm bizoholicwebsite-wordpress-rbtyli-wordpress-1 bizoholicwebsite-wordpress-rbtyli-wp_db-1
echo "✅ Bizoholic removed"
echo ""

# 3. Remove Volumes (Optional - user already has backup)
echo "Removing WordPress volumes..."
docker volume rm coreldove-wordpress-data coreldove-mysql-data bizoholic-wordpress-data bizoholic-mysql-data 2>/dev/null || echo "Some volumes not found (already removed?)"
echo "✅ Volumes cleaned"
echo ""

# 4. Remove Images
echo "Removing unused images..."
docker rmi mysql:8.4 mysql:8.0 wordpress:latest bizoholicwebsite-wordpress-rbtyli-wordpress:latest code-wordpress:latest 2>/dev/null || echo "Some images in use or not found"
docker image prune -a -f
echo "✅ Images cleaned"
echo ""

# 5. Check Disk Space
echo "Final Disk Usage:"
df -h / | grep -v Filesystem
echo ""

echo "=== Decommissioning Complete ==="
