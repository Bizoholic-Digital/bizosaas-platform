<?php

//database configuration
if (file_exists('places-config-info.php')) {
    include "places-config-info.php";
}

$select_search = $_REQUEST['select_search'];

if($select_search == 0){

    $home_path = $webpage_full_link.'places/';
    header("location: $home_path");
    exit;
}

//get matched data from place table
$place_qry = "SELECT * FROM " . TBL . "places WHERE place_id = '$select_search' ";
$place_query = mysqli_query($conn,$place_qry);

if (mysqli_num_rows($place_query) > 0) {
    $place_row = mysqli_fetch_array($place_query);
    $place_name = $place_row['place_name'];
    $place_slug = $place_row['place_slug'];

    $p_place_slug = preg_replace('/\s+/', '-', strtolower($place_slug));
    $p_url = $PLACE_DETAIL_URL . urlModifier($p_place_slug);

    header("location: $p_url");
    exit;

}else{

    header("location: ../search-results?q=$select_search");
    exit;
}

?>