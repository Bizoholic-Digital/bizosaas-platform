<?php
/**
 * Plugin Name: BizoSaaS Connect
 * Plugin URI: https://bizosaas.com
 * Description: Securely connects your WordPress site to the BizoSaaS Brain, enabling AI Agents to manage content, plugins, and analytics.
 * Version: 1.0.0
 * Author: BizoSaaS Platform
 * Author URI: https://bizosaas.com
 * License: GPLv2 or later
 */

if (!defined('ABSPATH')) {
    exit;
}

class BizoSaaS_Connect {

    private $api_namespace = 'bizosaas/v1';
    private $api_key_option = 'bizosaas_api_key';

    public function __construct() {
        add_action('rest_api_init', array($this, 'register_routes'));
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('admin_init', array($this, 'register_settings'));
    }

    public function register_routes() {
        // GET /status - Publicly accessible status check (lightweight)
        register_rest_route($this->api_namespace, '/status', array(
            'methods' => 'GET',
            'callback' => array($this, 'get_status'),
            'permission_callback' => '__return_true', // Public but read-only low-risk data
        ));

        // POST /connect - Handshake to exchange keys
        register_rest_route($this->api_namespace, '/connect', array(
            'methods' => 'POST',
            'callback' => array($this, 'handle_connect'),
            'permission_callback' => '__return_true', // Open for initial handshake, protected by signature verification in future
        ));

        // POST /agent/action - Main Agent Interface
        register_rest_route($this->api_namespace, '/agent/action', array(
            'methods' => 'POST',
            'callback' => array($this, 'handle_agent_action'),
            'permission_callback' => array($this, 'check_permissions'),
        ));
    }

    public function get_status() {
        return new WP_REST_Response(array(
            'status' => 'active',
            'version' => '1.0.0',
            'site_name' => get_bloginfo('name'),
            'wp_version' => get_bloginfo('version'),
            'plugins_active' => count(get_option('active_plugins')),
            'connected' => !empty(get_option($this->api_key_option))
        ), 200);
    }

    public function handle_connect($request) {
        $params = $request->get_json_params();
        $key = isset($params['api_key']) ? sanitize_text_field($params['api_key']) : '';
        
        if (empty($key)) {
            return new WP_Error('missing_key', 'API Key is required', array('status' => 400));
        }

        // In a real scenario, validte the key against BizoSaaS API
        update_option($this->api_key_option, $key);

        return new WP_REST_Response(array(
            'success' => true,
            'message' => 'Connected successfully to BizoSaaS Platform'
        ), 200);
    }

    public function check_permissions($request) {
        $header_key = $request->get_header('X-BizoSaaS-Key');
        $stored_key = get_option($this->api_key_option);

        if (empty($stored_key) || $header_key !== $stored_key) {
             return new WP_Error('rest_forbidden', 'Invalid API Key', array('status' => 401));
        }
        return true;
    }

    public function handle_agent_action($request) {
        $params = $request->get_json_params();
        $action = isset($params['action']) ? $params['action'] : '';

        // Example Agent Actions
        switch ($action) {
            case 'list_plugins':
                 if (!function_exists('get_plugins')) { require_once ABSPATH . 'wp-admin/includes/plugin.php'; }
                 return new WP_REST_Response(get_plugins(), 200);
            
            case 'install_plugin':
                // Logic to install plugin via WP_Upgrader
                return new WP_REST_Response(array('message' => 'Plugin installation logic placeholder'), 200);

            default:
                return new WP_Error('invalid_action', 'Unknown action', array('status' => 400));
        }
    }

    public function add_admin_menu() {
        add_options_page(
            'BizoSaaS Connect',
            'BizoSaaS Connect',
            'manage_options',
            'bizosaas-connect',
            array($this, 'options_page_html')
        );
    }

    public function register_settings() {
        register_setting('bizosaas_options', $this->api_key_option);
    }

    public function options_page_html() {
        ?>
        <div class="wrap">
            <h1>BizoSaaS Connect</h1>
            <form action="options.php" method="post">
                <?php
                settings_fields('bizosaas_options');
                do_settings_sections('bizosaas_options');
                ?>
                <table class="form-table">
                    <tr valign="top">
                        <th scope="row">BizoSaaS API Key</th>
                        <td><input type="text" name="<?php echo $this->api_key_option; ?>" value="<?php echo esc_attr(get_option($this->api_key_option)); ?>" class="regular-text" /></td>
                    </tr>
                </table>
                <?php submit_button(); ?>
            </form>
            <hr>
            <h3>Connection Status</h3>
            <p>
                <?php if (get_option($this->api_key_option)) : ?>
                    <span style="color: green; font-weight: bold;">CONNECTED</span> to BizoSaaS Brain.
                <?php else : ?>
                    <span style="color: red; font-weight: bold;">DISCONNECTED</span>. Please enter your API Key found in the onboarding dashboard.
                <?php endif; ?>
            </p>
        </div>
        <?php
    }
}

new BizoSaaS_Connect();
