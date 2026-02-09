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
        $category_listing_qry = "UPDATE  " . TBL . "news_trending SET trending_news_pos_id='" . $order . "' where trending_news_id='" . $item . "'";

        $category_listing_res = mysqli_query($conn,$category_listing_qry);

        $order++;
    }

    echo json_encode(  $orderArr );
}