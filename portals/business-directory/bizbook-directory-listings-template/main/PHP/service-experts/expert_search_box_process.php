<?php

//database configuration
if (file_exists('expert-config-info.php')) {
    include "expert-config-info.php";
}

$select_search = $_REQUEST['select_search'];

//get matched data from expert categories table
$categories_qry = "SELECT * FROM " . TBL . "expert_categories WHERE category_id = '$select_search' ";
$categories_query = mysqli_query($conn,$categories_qry);

if (mysqli_num_rows($categories_query) > 0) {
    $categories_row = mysqli_fetch_array($categories_query);
    $category_name = $categories_row['category_name'];
    $category_slug = $categories_row['category_slug'];

    $p_category_slug = preg_replace('/\s+/', '-', strtolower($category_slug));
    $p_url = $ALL_EXPERTS_URL . urlModifier($p_category_slug);

    header("location: $p_url");
    exit;

}else{

    header("location: ../search-results?q=$select_search");
    exit;
}

?>