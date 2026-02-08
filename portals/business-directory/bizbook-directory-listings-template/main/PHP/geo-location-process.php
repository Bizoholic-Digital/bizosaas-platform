<?php
//database configuration
if (file_exists('config/info.php')) {
    include('config/info.php');
}
session_start();

$_SESSION['latitude'] = $_REQUEST['latitude'];
$_SESSION['longitude'] = $_REQUEST['longitude'];

exit();