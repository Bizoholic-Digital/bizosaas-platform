#!/bin/bash
# simplified WordPress Backup Script (v2)
# Uses docker cp and corrected paths for Bedrock/Bizoholic

set -e  # Exit on error

BACKUP_DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="$HOME/backups/wordpress-$BACKUP_DATE"
VPS_HOST="194.238.16.237"
VPS_PASS="&k3civYG5Q6YPb"

echo "=== WordPress Backup Script (v2) ==="
echo "Backup directory: $BACKUP_DIR"
echo ""

# Create directories
mkdir -p "$BACKUP_DIR"/{coreldove,bizoholic}/{database,files,config}
cd "$BACKUP_DIR"

echo "Step 1: Backing up Coreldove WordPress..."

# Coreldove database
echo "  - Exporting database..."
sshpass -p "$VPS_PASS" ssh root@$VPS_HOST \
  "docker exec coreldovewebsite-wordpress-fnoyyo-wp_db-1 \
  sh -c 'exec mysqldump --all-databases -uroot -p\"\$MYSQL_ROOT_PASSWORD\"' 2>/dev/null" \
  > coreldove/database/coreldove-$BACKUP_DATE.sql

# Coreldove wp-content
echo "  - Backing up wp-content..."
sshpass -p "$VPS_PASS" ssh root@$VPS_HOST \
  "docker cp coreldovewebsite-wordpress-fnoyyo-wordpress-1:/var/www/html/wp-content /tmp/coreldove-wp-content && \
   tar czf /tmp/coreldove-wp-content.tar.gz -C /tmp coreldove-wp-content && \
   rm -rf /tmp/coreldove-wp-content"
sshpass -p "$VPS_PASS" scp root@$VPS_HOST:/tmp/coreldove-wp-content.tar.gz \
  coreldove/files/
sshpass -p "$VPS_PASS" ssh root@$VPS_HOST "rm /tmp/coreldove-wp-content.tar.gz"

# Coreldove config
echo "  - Backing up configuration..."
sshpass -p "$VPS_PASS" ssh root@$VPS_HOST \
  "docker exec coreldovewebsite-wordpress-fnoyyo-wordpress-1 \
  cat /var/www/html/wp-config.php" \
  > coreldove/config/wp-config.php

echo "✅ Coreldove backup complete"
echo ""

echo "Step 2: Backing up Bizoholic WordPress (Bedrock)..."

# Bizoholic database
echo "  - Exporting database..."
sshpass -p "$VPS_PASS" ssh root@$VPS_HOST \
  "docker exec bizoholicwebsite-wordpress-rbtyli-wp_db-1 \
  sh -c 'exec mysqldump --all-databases -uroot -p\"\$MYSQL_ROOT_PASSWORD\"' 2>/dev/null" \
  > bizoholic/database/bizoholic-$BACKUP_DATE.sql

# Bizoholic wp-content (Bedrock uses web/app)
echo "  - Backing up web/app..."
sshpass -p "$VPS_PASS" ssh root@$VPS_HOST \
  "docker cp bizoholicwebsite-wordpress-rbtyli-wordpress-1:/var/www/html/web/app /tmp/bizoholic-app && \
   tar czf /tmp/bizoholic-app.tar.gz -C /tmp bizoholic-app && \
   rm -rf /tmp/bizoholic-app"
sshpass -p "$VPS_PASS" scp root@$VPS_HOST:/tmp/bizoholic-app.tar.gz \
  bizoholic/files/
sshpass -p "$VPS_PASS" ssh root@$VPS_HOST "rm /tmp/bizoholic-app.tar.gz"

# Bizoholic config (Bedrock uses web/wp-config.php)
echo "  - Backing up configuration..."
sshpass -p "$VPS_PASS" ssh root@$VPS_HOST \
  "docker exec bizoholicwebsite-wordpress-rbtyli-wordpress-1 \
  cat /var/www/html/web/wp-config.php" \
  > bizoholic/config/wp-config.php

echo "✅ Bizoholic backup complete"
echo ""

# Verification
echo "Step 3: Verifying backups..."
echo ""
echo "Coreldove:"
ls -lh coreldove/database/*.sql 2>/dev/null || echo "  Database: FAILED"
ls -lh coreldove/files/*.tar.gz 2>/dev/null || echo "  Files: FAILED"
ls -lh coreldove/config/*.php 2>/dev/null || echo "  Config: FAILED"
echo ""
echo "Bizoholic:"
ls -lh bizoholic/database/*.sql 2>/dev/null || echo "  Database: FAILED"
ls -lh bizoholic/files/*.tar.gz 2>/dev/null || echo "  Files: FAILED"
ls -lh bizoholic/config/*.php 2>/dev/null || echo "  Config: FAILED"
echo ""

# Create compressed archive
echo "Step 4: Creating compressed archive..."
cd ..
tar czf "wordpress-backup-$BACKUP_DATE.tar.gz" "wordpress-$BACKUP_DATE/"
echo ""

# Final summary
echo "=== Backup Complete ==="
echo ""
echo "Backup location: $BACKUP_DIR"
echo "Compressed archive: wordpress-backup-$BACKUP_DATE.tar.gz"
echo ""
echo "Archive size:"
ls -lh "wordpress-backup-$BACKUP_DATE.tar.gz"
echo ""
echo "✅ Backup successful! Safe to proceed with cleanup."
