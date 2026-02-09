<?php

include "config/info.php";

$id = $_REQUEST['idd'];
$value1 = $_REQUEST['value1'];


if(isset($_POST)){

    $product_qry = "UPDATE  " . TBL . "listings  SET listing_open ='" . $value1 . "' where listing_id = '" . $id . "'";

    $product_res = mysqli_query($conn,$product_qry);
}