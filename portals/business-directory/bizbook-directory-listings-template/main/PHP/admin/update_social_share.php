<?php

include "config/info.php";

$id = $_REQUEST['idd'];
$value1 = $_REQUEST['value1'];


if(isset($_POST)){

    $product_qry = "UPDATE  " . TBL . "footer  SET $id ='" . $value1 . "' where footer_id = 1";

    $product_res = mysqli_query($conn,$product_qry);
}