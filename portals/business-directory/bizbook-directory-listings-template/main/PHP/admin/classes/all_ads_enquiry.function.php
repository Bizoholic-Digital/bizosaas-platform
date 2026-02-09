<?php

//Get All Inactive Ads Enquiry

function getAllInactiveAdsEnquiry()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "all_ads_enquiry WHERE ad_enquiry_status = 'InActive' ORDER BY all_ads_enquiry_id DESC";;
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Active Ads Enquiry

function getAllActiveAdsEnquiry()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "all_ads_enquiry WHERE ad_enquiry_status = 'Active' ORDER BY all_ads_enquiry_id DESC";;
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Ads Enquiry with given user id

function getAllUserAdsEnquiry($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "all_ads_enquiry WHERE user_id = '" . $arg . "' ORDER BY all_ads_enquiry_id DESC";;
    $rs = mysqli_query($conn, $sql);
    return $rs;

}


//Get All Ads Enquiry with given ad enquiry Id
function getAdsEnquiry($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "all_ads_enquiry where all_ads_enquiry_id = '" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Ads Enquiry with given ad enquiry Id
function getAds($arg)
{
    global $conn;
    global $curDate;

    $curDate1 = strtotime($curDate);

    $date = date('Y-m-d', $curDate1);

    $sql = "SELECT * FROM " . TBL . "all_ads_enquiry where all_ads_price_id = '" . $arg . "' AND ad_start_date <= '". $date ."' AND ad_end_date >= '". $date ."' AND ad_enquiry_status = 'Active'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Ad Request Count
function getCountAds()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "all_ads_enquiry ORDER BY all_ads_enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}
