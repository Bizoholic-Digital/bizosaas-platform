#!/bin/bash
set -e

# Generate sp-config.php if environment variables are provided
if [ -n "$DB_HOST" ] && [ -n "$DB_USER" ] && [ -n "$DB_PASS" ] && [ -n "$DB_NAME" ]; then
    echo "Generating sp-config.php from environment variables..."
    cat <<EOF > /var/www/html/config/sp-config.php
<?php
define("SP_WEBPATH", "https://seo.bizoholic.net");
define("DB_NAME", "$DB_NAME");
define("DB_USER", "$DB_USER");
define("DB_PASSWORD", "$DB_PASS");
define("DB_HOST", "$DB_HOST");
define("DB_ENGINE", "mysql");
define("SP_INSTALLED", "5.1.0");
define("SP_DEBUG", 0);
define("SP_TIMEOUT", 18000);
?>
EOF
    chown www-data:www-data /var/www/html/config/sp-config.php
    chmod 644 /var/www/html/config/sp-config.php
else
    echo "Missing database environment variables. Skipping sp-config.php generation."
fi

# Execute the original Apache entrypoint command
exec "$@"
