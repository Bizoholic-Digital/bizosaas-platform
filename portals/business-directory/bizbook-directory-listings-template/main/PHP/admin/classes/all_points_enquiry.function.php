<?php

//Get All Point Enquiry's
function getAllPointsEnquiry()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "all_points_enquiry ORDER BY all_points_enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get Point Enquiry's with given User Id
function getUserPointsEnquiry($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "all_points_enquiry where user_id = '" . $arg . "' ORDER BY all_points_enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}