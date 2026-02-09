<?php

include "config/info.php";

$isNum = false;

foreach( $_POST['sort'] as $key => $value ) {
    if ( ctype_digit($value) ) {
        $isNum = true;
    } else {
        $isNum = false;
    }
}

if( isset($_POST) && $isNum == true ){

    $orderArr = $_POST['sort'];
    $order = 0;

        foreach ( $orderArr as $item) {
            $product_qry = "UPDATE  " . TBL . "search_list  SET search_list_position='" . $order . "' where search_list_id='" . $item . "'";

            $product_res = mysqli_query($conn,$product_qry);

            $order++;
        }

    echo json_encode(  $orderArr );
}