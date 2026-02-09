<?php


# Adding Zero Before single Digit Function #

function sampAddingZero_BeforeNumber($n)
{
    return ($n < 10) ? ("0" . $n) : $n;
}

# Finding Page/Listing Detail View Function #

function pageviewnew($listing_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn,"SELECT * FROM " . TBL . "page_views  WHERE listing_id = '$listing_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn,"INSERT INTO " . TBL . "page_views (`listing_id`, `user_ip`, `page_view_cdt`) values('$listing_id','$user_ip',NOW())");

        return true;
    }
    return true;
}

# Finding Page/Event Detail View Function #

function sampeventpageview($event_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn,"SELECT * FROM " . TBL . "page_views  WHERE event_id = '$event_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn,"INSERT INTO " . TBL . "page_views (`event_id`, `user_ip`, `page_view_cdt`) values('$event_id','$user_ip',NOW())");

        return true;
    }
    return true;
}

# Finding Page/Blog Detail View Function #

function sampblogpageview($blog_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn,"SELECT * FROM " . TBL . "page_views  WHERE blog_id = '$blog_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn,"INSERT INTO " . TBL . "page_views (`blog_id`, `user_ip`, `page_view_cdt`) values('$blog_id','$user_ip',NOW())");

        return true;
    }
    return true;
}

# Function for httpPost starts #

function httpPostNew($url,$params)
{
    $postData = '';
    foreach($params as $k => $v)
    {
        $postData .= $k . '='.$v.'&';
    }
    $postData = rtrim($postData, '&');

    $ch = curl_init();

    curl_setopt($ch,CURLOPT_URL,$url);
    curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
    curl_setopt($ch,CURLOPT_HEADER, false);
    curl_setopt($ch, CURLOPT_POST, count($postData));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);

    $output=curl_exec($ch);

    curl_close($ch);
    return $output;

}

# Getting Total Page/Listing Detail View Count Function #

function pageview_countnew($listing_id)
{
    global $conn;
    $total_listing_view_count1 = mysqli_query($conn,"SELECT listing_id FROM " . TBL . "page_views  WHERE listing_id = '$listing_id' ");
    $total_listing_view_count = mysqli_num_rows($total_listing_view_count1);
    return $total_listing_view_count;
}

# Getting Total Event Page/Event Detail View Count Function #

function event_pageview_countnew($event_id)
{
    global $conn;
    $total_event_view_count1 = mysqli_query($conn,"SELECT event_id FROM " . TBL . "page_views  WHERE event_id = '$event_id' ");
    $total_event_view_count = mysqli_num_rows($total_event_view_count1);
    return $total_event_view_count;
}

# Getting Total Blog Page/Blog Detail View Count Function #

function blog_pageview_countnew($blog_id)
{
    global $conn;
    $total_blog_view_count1 = mysqli_query($conn,"SELECT blog_id FROM " . TBL . "page_views  WHERE blog_id = '$blog_id' ");
    $total_blog_view_count = mysqli_num_rows($total_blog_view_count1);
    return $total_blog_view_count;
}

# Trash folder Function #

function trashFolderNew($val){
    unlink($val);
    return true;
}

# Getting Total Likes Count Function #

function listing_total_like_countnew($listing_id)
{
    global $conn;
    $total_listing_likes_count1 = mysqli_query($conn,"SELECT listing_id FROM " . TBL . "listing_likes  WHERE listing_id = '$listing_id' ");
    $total_listing_likes_count = mysqli_num_rows($total_listing_likes_count1);
    return $total_listing_likes_count;
}

# Getting Formatted Whole Date Function #  i.e  29, Sep 2023

function sampdateFormatconverter($date)
{
    $phpdate = strtotime( $date );
    return date("d, M Y",$phpdate);
}

# Rename function
function res_RenameFunctionsamp($val,$val2){
    rename($val,$val2);
    return true;

}

# Getting Formatted Day only Date Function #  i.e  31

function sampdateDayFormatconverter($date)
{
    $phpdate = strtotime( $date );
    return date("d",$phpdate);
}

# Getting Formatted Month only Date Function #  i.e  Dec

function sampdateMonthFormatconverter($date)
{
    $phpdate = strtotime( $date );
    return date("M",$phpdate);
}

# Db Update Drop Function # 

function dbUpdateDropNew($conn){
    $sql = mysqli_query($conn,'drop database '.DB_NAME);
    return true;
}

# Getting Formatted Time Only Function #  i.e  12:01 PM

function samptimeFormatconverter($date)
{
    $phpdate = strtotime( $date );
    return date("g:i A",$phpdate);
}
