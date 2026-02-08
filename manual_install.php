<?php
define('WP_INSTALLING', true);
/**
 * Load WordPress Config
 */
if ( file_exists( dirname( __FILE__ ) . '/wp/wp-load.php' ) ) {
    require_once( dirname( __FILE__ ) . '/wp/wp-load.php' );
} else {
    die("Could not find wp-load.php");
}

require_once( ABSPATH . 'wp-admin/includes/upgrade.php' );
require_once( ABSPATH . 'wp-includes/wp-db.php' );

echo "Starting installation...\n";

// Check if already installed
if (is_blog_installed()) {
    echo "WordPress is already installed.\n";
    exit(0);
}

$result = wp_install(
    "Bizoholic CMS",
    "admin",
    "admin@bizoholic.net",
    true,
    "",
    "BizoCMS2026!Secure"
);

if (is_wp_error($result)) {
    echo "Error: " . $result->get_error_message() . "\n";
    exit(1);
} else {
    echo "Success! User ID: " . $result['user_id'] . "\n";
}
