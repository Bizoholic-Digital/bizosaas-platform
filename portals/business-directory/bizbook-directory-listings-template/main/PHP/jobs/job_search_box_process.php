<?php

//database configuration
if(file_exists('job-config-info.php'))
{
    include "job-config-info.php";
}

$select_search = $_REQUEST['select_search'];
$select_city = $_REQUEST['select_city'];

//get matched data from cities table
$cities_qry = "SELECT * FROM " . TBL . "job_cities WHERE city_id = '$select_city'";
$cities_query = mysqli_query($conn,$cities_qry);


//get matched data from job categories table
$categories_qry = "SELECT * FROM " . TBL . "job_categories WHERE category_id = '$select_search' ";
$categories_query = mysqli_query($conn,$categories_qry);

if (mysqli_num_rows($categories_query) > 0 && mysqli_num_rows($cities_query) > 0) {
    $categories_row = mysqli_fetch_array($categories_query);
    $category_name = $categories_row['category_name'];
    $category_slug = $categories_row['category_slug'];

    $p_category_slug = preg_replace('/\s+/', '-', strtolower($category_slug));
    $p_url = $ALL_JOBS_URL . urlModifier($p_category_slug)."?city=".$select_city;

    header("location: $p_url");
    exit;

}elseif (mysqli_num_rows($categories_query) <= 0 && mysqli_num_rows($cities_query) > 0) {

    $p_url = $ALL_JOBS_URL ."?city=".$select_city;;

    header("location: $p_url");
    exit;

}elseif (mysqli_num_rows($categories_query) > 0 && mysqli_num_rows($cities_query) <= 0) {
    $categories_row = mysqli_fetch_array($categories_query);
    $category_name = $categories_row['category_name'];
    $category_slug = $categories_row['category_slug'];

    $p_category_slug = preg_replace('/\s+/', '-', strtolower($category_slug));
    $p_url = $ALL_JOBS_URL . urlModifier($p_category_slug);

    header("location: $p_url");
    exit;

}else{

    header("location: ../search-results?q=$select_search");
    exit;
}

?>