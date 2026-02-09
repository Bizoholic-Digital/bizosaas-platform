<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

//if(($_SESSION['admin_id'] !="1") || empty($_SESSION['admin_id'])) {
if( empty($_SESSION['admin_id'])) {

    header("Location: index.php");
}
