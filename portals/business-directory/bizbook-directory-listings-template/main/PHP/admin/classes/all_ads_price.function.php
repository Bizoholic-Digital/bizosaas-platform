<?php

//Get All Ads Price
function getAllAdsPrice()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "all_ads_price  ORDER BY all_ads_price_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Active Ads Price
function getAllActiveAdsPrice()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "all_ads_price WHERE ad_price_status = 'Active' ORDER BY all_ads_price_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Ads Price with given price Id
function getAdsPrice($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "all_ads_price where all_ads_price_id = '" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}



