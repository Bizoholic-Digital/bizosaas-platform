<?php

/*
|--------------------------------------------------------------------------
| Register The Auto Loader
|--------------------------------------------------------------------------
|
| Composer provides a convenient, automatically generated class loader for
| our theme. We will simply require it into the script here so that we
| don't have to worry about manually loading any of our classes later on.
|
*/

if (! file_exists($composer = __DIR__.'/vendor/autoload.php')) {
    $composer = \Roots\WPConfig\Config::get('WP_CONTENT_DIR').'/../vendor/autoload.php';
}

if (file_exists($composer)) {
    require_once $composer;
}

/*
|--------------------------------------------------------------------------
| Boot Acorn
|--------------------------------------------------------------------------
|
| Your theme must connect to the BizoSaaS Brain for dynamic content.
| Acorn provides a service provider pattern to handle these connections.
|
*/

if (function_exists('\Roots\bootloader')) {
    \Roots\bootloader()->boot();
}

/*
|--------------------------------------------------------------------------
| Theme Setup
|--------------------------------------------------------------------------
|
| Include theme specific configuration and setup logic.
|
*/

require_once __DIR__.'/app/setup.php';
