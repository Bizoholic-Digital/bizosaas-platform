<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if(file_exists('config/db.php'))
{
    include('config/db.php');
}

if(file_exists('config/config.php'))
{
    include('config/config.php');
}


$current_page = basename($_SERVER['PHP_SELF']);
?>