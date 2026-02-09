<?php

//database configuration
if (file_exists('config/info.php')) {
    include('config/info.php');
}

$select_search = $_REQUEST['select_search'];
$select_city = $_REQUEST['select_city'];

//get matched data from cities table
$cities_qry = "SELECT * FROM " . TBL . "cities WHERE city_name = '$select_city'";
$cities_query = mysqli_query($conn,$cities_qry);
$cities_row = mysqli_fetch_array($cities_query);

$city_id = $cities_row['city_id'];


//get matched data from categories table
$categories_qry = "SELECT * FROM " . TBL . "categories WHERE category_name = '$select_search' ";
$categories_query = mysqli_query($conn,$categories_qry);

//get matched data from listings table
$listings_qry = "SELECT * FROM " . TBL . "listings WHERE listing_name = '$select_search' AND listing_status= 'Active' AND listing_is_delete != '2' ";
$listings_query = mysqli_query($conn,$listings_qry);

//get matched data from events table
$event_qry = "SELECT * FROM " . TBL . "events WHERE event_name = '$select_search' AND event_status= 'Active'";
$event_query = mysqli_query($conn,$event_qry);

//get matched data from blog table
$blog_qry = "SELECT * FROM " . TBL . "blogs WHERE blog_name = '$select_search' AND blog_status= 'Active'";
$blog_query = mysqli_query($conn,$blog_qry);

//get matched data from product table
$product_qry = "SELECT * FROM " . TBL . "products WHERE product_name = '$select_search' AND product_status= 'Active'";
$product_query = mysqli_query($conn,$product_qry);

//get matched data from job table
$job_qry = "SELECT * FROM " . TBL . "jobs WHERE job_title = '$select_search' AND job_status= 'Active'";
$job_query = mysqli_query($conn,$job_qry);

if (mysqli_num_rows($categories_query) > 0) {
    $categories_row = mysqli_fetch_array($categories_query);
    $category_name = $categories_row['category_name'];

    $p_category_name = preg_replace('/\s+/', '-', strtolower($category_name));
    $p_url = $ALL_LISTING_URL . urlModifier($p_category_name);

    header("location: $p_url");
    exit;

} elseif (mysqli_num_rows($categories_query) <= 0 && mysqli_num_rows($listings_query) > 0) {

        $listings_row = mysqli_fetch_array($listings_query);

        $listing_code = $listings_row['listing_code'];

        $listing_url = $LISTING_URL.urlModifier($listings_row['listing_slug']);

        header("location: $listing_url");
        exit;


}elseif (mysqli_num_rows($categories_query) <= 0 && mysqli_num_rows($listings_query) <= 0 && mysqli_num_rows($event_query) > 0 ) {

        $event_row = mysqli_fetch_array($event_query);

        $event_id = $event_row['event_id'];

        $event_url = $EVENT_URL.urlModifier($event_row['event_slug']);

        header("location: $event_url");
        exit;

}elseif (mysqli_num_rows($categories_query) <= 0 && mysqli_num_rows($listings_query) <= 0 && mysqli_num_rows($event_query) <= 0 && mysqli_num_rows($blog_query) > 0 ) {

    $blog_row = mysqli_fetch_array($blog_query);

    $blog_id = $blog_row['blog_id'];

    $blog_url = $BLOG_URL.urlModifier($blog_row['blog_slug']);

    header("location: $blog_url");
    exit;

}elseif (mysqli_num_rows($categories_query) <= 0 && mysqli_num_rows($listings_query) <= 0 && mysqli_num_rows($event_query) <= 0 && mysqli_num_rows($blog_query) <= 0 && mysqli_num_rows($product_query) > 0) {

    $product_row = mysqli_fetch_array($product_query);

    $product_code = $product_row['product_code'];

    $product_url = $PRODUCT_URL.urlModifier($product_row['product_slug']);

    header("location: $product_url");
    exit;

}elseif (mysqli_num_rows($categories_query) <= 0 && mysqli_num_rows($listings_query) <= 0 && mysqli_num_rows($event_query) <= 0 && mysqli_num_rows($blog_query) <= 0 && mysqli_num_rows($product_query) <= 0 && mysqli_num_rows($job_query) > 0) {

    $job_row = mysqli_fetch_array($job_query);

    $job_code = $job_row['job_code'];

    $job_url = $JOB_URL.urlModifier($job_row['job_slug']);

    header("location: $job_url");
    exit;

}else{
    
    header("location: search-results?q=$select_search");
    exit;
}

?>
