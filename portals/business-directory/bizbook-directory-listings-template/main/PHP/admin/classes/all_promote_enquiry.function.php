<?php

//Get All Inactive Promote Enquiry

function getAllInactivePromoteEnquiry()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "all_promote_enquiry WHERE promote_enquiry_status = 'InActive' ORDER BY all_promote_enquiry_id DESC";;
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Active Promote Enquiry

function getAllActivePromoteEnquiry()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "all_promote_enquiry WHERE promote_enquiry_status = 'Active' ORDER BY all_promote_enquiry_id DESC";;
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Promote Enquiry 

function getAllPromoteEnquiry()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "all_promote_enquiry ORDER BY all_promote_enquiry_id DESC";;
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Promote Enquiry with given user id

function getAllUserPromoteEnquiry($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "all_promote_enquiry WHERE user_id = '" . $arg . "' ORDER BY all_promote_enquiry_id DESC";;
    $rs = mysqli_query($conn, $sql);
    return $rs;

}


//Get All Promote Enquiry with given ad enquiry Id
function getPromoteEnquiry($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "all_promote_enquiry where all_promote_enquiry_id = '" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Promote Enquiry with given ad enquiry Id
function getPromote($arg)
{
    global $conn;
    global $curDate;

    $curDate1 = strtotime($curDate);

    $date = date('Y-m-d', $curDate1);

    $sql = "SELECT * FROM " . TBL . "all_promote_enquiry where all_promote_price_id = '" . $arg . "' AND promote_start_date <= '". $date ."' AND promote_end_date >= '". $date ."' AND promote_enquiry_status = 'Active'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Ad Request Count
function getCountPromote()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "all_promote_enquiry ORDER BY all_promote_enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}
