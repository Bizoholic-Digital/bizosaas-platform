<?php

//Get All Expert Reviews
function getAllExpertReviews()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_reviews ORDER BY review_cdt DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Saved Expert Reviews
function getAllSavedExpertReviews()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_reviews WHERE review_save = 1";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Expert Reviews with Expert Id
function getAllExpertExpertReviews($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_reviews  WHERE expert_id = '$arg' AND review_status= 'Active' ORDER BY review_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Expert Reviews with Enquiry Id And Expert Id
function getEnquiryExpertExpertReviews($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_reviews  WHERE enquiry_id = '$arg' AND expert_id = '$arg1' AND review_status= 'Active' ORDER BY review_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Expert Reviews with Listing Id
function getTenActiveExpertReviews()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_reviews  WHERE review_status= 'Active' ORDER BY review_cdt DESC LIMIT 10";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Count of Review
function getCountExpertExpertReview($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_reviews  WHERE expert_id = '$arg' AND review_status= 'Active'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Received Expert Reviews with User Id
function getAllReceivedExpertReviews($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_reviews  WHERE expert_user_id = '$arg' AND review_status='Active' ORDER BY review_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Sent Expert Reviews with User Id
function getAllSentExpertReviews($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_reviews  WHERE review_user_id = '$arg' AND review_status='Active' ORDER BY review_cdt DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Count of Review
function getCountExpertReview()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_reviews ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Count of Received Expert Reviews
function getCountReceivedExpertReview($arg)
{
    global $conn;

    $sql = $sql = "SELECT * FROM " . TBL . "expert_reviews  WHERE expert_user_id = '$arg' AND review_status='Active'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Count of Sent Expert Reviews
function getCountSentExpertReview($arg)
{
    global $conn;

    $sql = $sql = "SELECT * FROM " . TBL . "expert_reviews  WHERE review_user_id = '$arg' AND review_status='Active'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}


// Expert Rating using Listing ID
function getExpertReview($arg)
{
    global $conn;

    $sql = "SELECT COUNT(*) AS rate_cnt, SUM(expert_rating) AS total_rate FROM " . TBL . "expert_reviews WHERE expert_id = '$arg' AND review_status='Active'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $rs;

}