<?php

//Get All Reviews
function getAllReviews()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "reviews ORDER BY review_cdt DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Saved Reviews
function getAllSavedReviews()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "reviews WHERE review_save = 1";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Reviews with Listing Id
function getAllListingReviews($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "reviews  WHERE listing_id = '$arg' AND review_status= 'Active' ORDER BY review_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Reviews with Listing Id
function getTenActiveReviews()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "reviews  WHERE review_status= 'Active' ORDER BY review_cdt DESC LIMIT 10";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Count of Review
function getCountListingReview($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "reviews  WHERE listing_id = '$arg' AND review_status= 'Active'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Received Reviews with User Id
function getAllReceivedReviews($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "reviews  WHERE listing_user_id = '$arg' AND review_status='Active' ORDER BY review_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Sent Reviews with User Id
function getAllSentReviews($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "reviews  WHERE review_user_id = '$arg' AND review_status='Active' ORDER BY review_cdt DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Count of Review
function getCountReview()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "reviews ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Count of Received Reviews
function getCountReceivedReview($arg)
{
    global $conn;

    $sql = $sql = "SELECT * FROM " . TBL . "reviews  WHERE listing_user_id = '$arg' AND review_status='Active'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Count of Sent Reviews
function getCountSentReview($arg)
{
    global $conn;

    $sql = $sql = "SELECT * FROM " . TBL . "reviews  WHERE review_user_id = '$arg' AND review_status='Active'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

// Listing Rating using Listing ID
function getListingReview($arg)
{
    global $conn;

    $sql = "SELECT COUNT(*) AS rate_cnt, SUM(price_rating) AS total_rate FROM " . TBL . "reviews WHERE listing_id = '$arg' AND review_status='Active'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $rs;

}

//Get All Received Reviews with User Id
function getAllUserListingDateReviews($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "reviews  WHERE listing_user_id = '$arg' AND review_status='Active' AND review_cdt > '$arg1'  ORDER BY review_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Received Reviews with User Id
function getCountAllUserListingDateReviews($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "reviews  WHERE listing_user_id = '$arg' AND review_status='Active' AND review_cdt > '$arg1'  ORDER BY review_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}