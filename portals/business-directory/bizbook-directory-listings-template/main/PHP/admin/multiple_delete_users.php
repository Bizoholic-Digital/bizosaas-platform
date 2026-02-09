<?php

if (file_exists('config/info.php')) {
    include('config/info.php');
}

$request = $_POST['request'];

// Data table data

if ($request == 1) {
    $deleteids_arr = $_POST['deleteids_arr'];
    exit;
}

// Delete Users record

if ($request == 2) {

    $deleteids_arr = $_POST['deleteids_arr'];

    foreach ($deleteids_arr as $deleteid) {

        $sql =
            " DELETE FROM  " . TBL . "users  WHERE user_id='" . $deleteid . "'";

        $sql_res = mysqli_query($conn, $sql);

        //Delete user listings from listing table

        $list =
            " DELETE FROM  " . TBL . "listings  WHERE user_id='" . $deleteid . "'";

        $list_res = mysqli_query($conn, $list);

        //Delete user products from product table

        $product =
            " DELETE FROM  " . TBL . "products  WHERE user_id='" . $deleteid . "'";

        $product_res = mysqli_query($conn, $product);


        //Delete user Events from events table

        $events =
            " DELETE FROM  " . TBL . "events  WHERE user_id='" . $deleteid . "'";

        $events_res = mysqli_query($conn, $events);


        //Delete user Blogs from Blogs table

        $blogs =
            " DELETE FROM  " . TBL . "blogs  WHERE user_id='" . $deleteid . "'";

        $blogs_res = mysqli_query($conn, $blogs);

        //Delete user Jobs from jobs table

        $jobs =
            " DELETE FROM  " . TBL . "jobs  WHERE user_id='" . $deleteid . "'";

        $jobs_res = mysqli_query($conn, $jobs);

    }

    echo 1;
    exit;
}
// Delete Listings record

if ($request == 3) {

    $deleteids_arr = $_POST['deleteids_arr'];

    foreach ($deleteids_arr as $deleteid) {

        //Delete listings from listing table

        $list =
            " DELETE FROM  " . TBL . "listings  WHERE listing_id='" . $deleteid . "'";

        $list_res = mysqli_query($conn, $list);

        //Query to delete the page view starts

        $page_view_qry = "DELETE FROM  " . TBL . "page_views where listing_id='" . $deleteid . "'";

        $page_view_res = mysqli_query($conn, $page_view_qry);

        //Query to delete the page view ends

    }

    echo 1;
    exit;
}

if ($request == 4) {

    $deleteids_arr = $_POST['deleteids_arr'];

    foreach ($deleteids_arr as $deleteid) {

        //Delete user Events from events table

        $events =
            " DELETE FROM  " . TBL . "events  WHERE event_id='" . $deleteid . "'";

        $events_res = mysqli_query($conn, $events);

        //Query to delete the page view starts

        $page_view_qry = "DELETE FROM  " . TBL . "page_views where event_id='" . $deleteid . "'";

        $page_view_res = mysqli_query($conn, $page_view_qry);

        //Query to delete the page view ends

    }

    echo 1;
    exit;
}

if ($request == 5) {

    $deleteids_arr = $_POST['deleteids_arr'];

    foreach ($deleteids_arr as $deleteid) {

        //Delete user Blogs from events table

        $blogs =
            " DELETE FROM  " . TBL . "blogs  WHERE blog_id='" . $deleteid . "'";

        $blogs_res = mysqli_query($conn, $blogs);

        //Query to delete the page view starts

        $page_view_qry = "DELETE FROM  " . TBL . "page_views where blog_id='" . $deleteid . "'";

        $page_view_res = mysqli_query($conn, $page_view_qry);

        //Query to delete the page view ends

    }

    echo 1;
    exit;
}

if ($request == 6) {

    $deleteids_arr = $_POST['deleteids_arr'];

    foreach ($deleteids_arr as $deleteid) {

        //Delete user products from product table

        $product =
            " DELETE FROM  " . TBL . "products  WHERE product_id='" . $deleteid . "'";

        $product_res = mysqli_query($conn, $product);

        //Query to delete the page view starts

        $page_view_qry = "DELETE FROM  " . TBL . "page_views where product_id='" . $deleteid . "'";

        $page_view_res = mysqli_query($conn, $page_view_qry);

        //Query to delete the page view ends

    }

    echo 1;
    exit;
}

if ($request == 7) {

    $deleteids_arr = $_POST['deleteids_arr'];

    foreach ($deleteids_arr as $deleteid) {

        //Delete user Jobs from jobs table

        $job =
            " DELETE FROM  " . TBL . "jobs  WHERE job_id='" . $deleteid . "'";

        $job_res = mysqli_query($conn, $job);

        //Query to delete the page view starts

        $page_view_qry = "DELETE FROM  " . TBL . "page_views where job_id='" . $deleteid . "'";

        $page_view_res = mysqli_query($conn, $page_view_qry);

        //Query to delete the page view ends

    }

    echo 1;
    exit;
}

if ($request == 8) {

    $deleteids_arr = $_POST['deleteids_arr'];

    foreach ($deleteids_arr as $deleteid) {

        //Delete user News from News table

        $news =
            " DELETE FROM  " . TBL . "news  WHERE news_id='" . $deleteid . "'";

        $news_res = mysqli_query($conn, $news);

        //Query to delete the page view starts

        $page_view_qry = "DELETE FROM  " . TBL . "page_views where news_id='" . $deleteid . "'";

        $page_view_res = mysqli_query($conn, $page_view_qry);

        //Query to delete the page view ends

    }

    echo 1;
    exit;
}

if ($request == 9) {

    $deleteids_arr = $_POST['deleteids_arr'];

    foreach ($deleteids_arr as $deleteid) {

        //Delete Places from Places table

        $place =
            " DELETE FROM  " . TBL . "places WHERE place_id='" . $deleteid . "'";

        $place_res = mysqli_query($conn, $place);

        //Query to delete the page view starts

        $page_view_qry = "DELETE FROM  " . TBL . "page_views where place_id='" . $deleteid . "'";

        $page_view_res = mysqli_query($conn, $page_view_qry);

        //Query to delete the page view ends

    }

    echo 1;
    exit;
}