<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if(!isset($_SESSION['user_code']) && empty($_SESSION['user_code']))
{
    header("Location: index");
}
    ?>
