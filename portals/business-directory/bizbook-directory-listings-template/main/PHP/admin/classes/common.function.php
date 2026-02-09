<?php


# Adding Zero Before single Digit Function #

function AddingZero_BeforeNumber($n)
{
    return ($n < 10) ? ("0" . $n) : $n;
}

# Finding Page/Listing Detail View Function #

function listingpageview($listing_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn, "SELECT * FROM " . TBL . "page_views  WHERE listing_id = '$listing_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn, "INSERT INTO " . TBL . "page_views (`listing_id`, `user_ip`, `page_view_cdt`) values('$listing_id','$user_ip',NOW())");

        return true;
    }
    return true;
}

# Finding Page/Event Detail View Function #

function eventpageview($event_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn, "SELECT * FROM " . TBL . "page_views  WHERE event_id = '$event_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn, "INSERT INTO " . TBL . "page_views (`event_id`, `user_ip`, `page_view_cdt`) values('$event_id','$user_ip',NOW())");

        return true;
    }
    return true;
}

# Finding Page/Blog Detail View Function #

function blogpageview($blog_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn, "SELECT * FROM " . TBL . "page_views  WHERE blog_id = '$blog_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn, "INSERT INTO " . TBL . "page_views (`blog_id`, `user_ip`, `page_view_cdt`) values('$blog_id','$user_ip',NOW())");

        return true;
    }
    return true;
}

# Finding Page/product Detail View Function #

function productpageview($product_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn, "SELECT * FROM " . TBL . "page_views  WHERE product_id = '$product_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn, "INSERT INTO " . TBL . "page_views (`product_id`, `user_ip`, `page_view_cdt`) values('$product_id','$user_ip',NOW())");

        return true;
    }
    return true;
}

# Finding Page/SEO Pages Detail View Function #

function seopageview($page_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn, "SELECT * FROM " . TBL . "page_views  WHERE page_id = '$page_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn, "INSERT INTO " . TBL . "page_views (`page_id`, `user_ip`, `page_view_cdt`) values('$page_id','$user_ip',NOW())");

        return true;
    }
    return true;
}

# Finding Page/Coupon Pages Detail View Function #

function couponpageview($coupon_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn, "SELECT * FROM " . TBL . "page_views  WHERE coupon_id = '$coupon_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn, "INSERT INTO " . TBL . "page_views (`coupon_id`, `user_ip`, `page_view_cdt`) values('$coupon_id','$user_ip',NOW())");

        return true;
    }
    return true;
}

# Finding All-listing/Category Pages Detail View Function #

function categorypageview($category_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn, "SELECT * FROM " . TBL . "page_views  WHERE category_id = '$category_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn, "INSERT INTO " . TBL . "page_views (`category_id`, `user_ip`, `page_view_cdt`) values('$category_id','$user_ip',NOW())");

        return true;
    }
    return true;
}

# Finding User Business Pages Detail View Function #

function businesspageview($user_business_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn, "SELECT * FROM " . TBL . "page_views  WHERE user_business_id = '$user_business_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn, "INSERT INTO " . TBL . "page_views (`user_business_id`, `user_ip`, `page_view_cdt`) values('$user_business_id','$user_ip',NOW())");

        return true;
    }
    return true;
}

# Finding Page/Job Detail View Function #

function jobpageview($job_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn, "SELECT * FROM " . TBL . "page_views  WHERE job_id = '$job_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn, "INSERT INTO " . TBL . "page_views (`job_id`, `user_ip`, `page_view_cdt`) values('$job_id','$user_ip',NOW())");

        return true;
    }
    return true;
}

# Finding Page/Job Profile Detail View Function #

function jobprofilepageview($job_profile_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn, "SELECT * FROM " . TBL . "page_views  WHERE job_profile_id = '$job_profile_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn, "INSERT INTO " . TBL . "page_views (`job_profile_id`, `user_ip`, `page_view_cdt`) values('$job_profile_id','$user_ip',NOW())");

        return true;
    }
    return true;
}


# Finding Page/Expert Profile Detail View Function #

function expertprofilepageview($expert_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn, "SELECT * FROM " . TBL . "page_views  WHERE expert_id = '$expert_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn, "INSERT INTO " . TBL . "page_views (`expert_id`, `user_ip`, `page_view_cdt`) values('$expert_id','$user_ip',NOW())");

        return true;
    }
    return true;
}

# Finding Page/News Detail View Function #

function newsdetailpageview($news_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn, "SELECT * FROM " . TBL . "page_views WHERE news_id = '$news_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn, "INSERT INTO " . TBL . "page_views (`news_id`, `user_ip`, `page_view_cdt`) values('$news_id','$user_ip',NOW())");

        return true;
    }
    return true;
}

# Finding Page/Place Detail View Function #

function placedetailpageview($news_id)
{
    global $conn;
    $user_ip = $_SERVER['REMOTE_ADDR'];

    $check_ip = mysqli_query($conn, "SELECT * FROM " . TBL . "page_views WHERE place_id = '$news_id' AND user_ip = '$user_ip' ");

    if (mysqli_num_rows($check_ip) <= 0) {
        $insertview = mysqli_query($conn, "INSERT INTO " . TBL . "page_views (`place_id`, `user_ip`, `page_view_cdt`) values('$news_id','$user_ip',NOW())");

        return true;
    }
    return true;
}

# Function for httpPost starts #

function httpPost($url, $params)
{
    $postData = '';
    foreach ($params as $k => $v) {
        $postData .= $k . '=' . $v . '&';
    }
    $postData = rtrim($postData, '&');

    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HEADER, false);
    curl_setopt($ch, CURLOPT_POST, count($postData));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);

    $output = curl_exec($ch);

    curl_close($ch);
    return $output;

}

# Getting Total Page/Listing Detail View Count Function #

function listing_pageview_count($listing_id)
{
    global $conn;
    $total_listing_view_count1 = mysqli_query($conn, "SELECT listing_id FROM " . TBL . "page_views  WHERE listing_id = '$listing_id' ");
    $total_listing_view_count = mysqli_num_rows($total_listing_view_count1);
    return $total_listing_view_count;
}

# Getting Total Event Page/Event Detail View Count Function #

function event_pageview_count($event_id)
{
    global $conn;
    $total_event_view_count1 = mysqli_query($conn, "SELECT event_id FROM " . TBL . "page_views  WHERE event_id = '$event_id' ");
    $total_event_view_count = mysqli_num_rows($total_event_view_count1);
    return $total_event_view_count;
}

# Getting Total Blog Page/Blog Detail View Count Function #

function blog_pageview_count($blog_id)
{
    global $conn;
    $total_blog_view_count1 = mysqli_query($conn, "SELECT blog_id FROM " . TBL . "page_views WHERE blog_id = '$blog_id' ");
    $total_blog_view_count = mysqli_num_rows($total_blog_view_count1);
    return $total_blog_view_count;
}

# Getting Total Product Page/Product Detail View Count Function #

function product_pageview_count($product_id)
{
    global $conn;
    $total_product_view_count1 = mysqli_query($conn, "SELECT product_id FROM " . TBL . "page_views  WHERE product_id = '$product_id' ");
    $total_product_view_count = mysqli_num_rows($total_product_view_count1);
    return $total_product_view_count;
}

# Getting Total Job Page/Job Detail View Count Function #

function job_pageview_count($job_id)
{
    global $conn;
    $total_job_view_count1 = mysqli_query($conn, "SELECT job_id FROM " . TBL . "page_views  WHERE job_id = '$job_id' ");
    $total_job_view_count = mysqli_num_rows($total_job_view_count1);
    return $total_job_view_count;
}

# Getting Total Job Page/Job Profile Detail View Count Function #

function job_profile_pageview_count($job_profile_id)
{
    global $conn;
    $total_job_view_count1 = mysqli_query($conn, "SELECT job_profile_id FROM " . TBL . "page_views  WHERE job_profile_id = '$job_profile_id' ");
    $total_job_view_count = mysqli_num_rows($total_job_view_count1);
    return $total_job_view_count;
}

# Getting Total Expert Profile Detail View Count Function #

function expert_profile_pageview_count($expert_id)
{
    global $conn;
    $total_expert_view_count1 = mysqli_query($conn, "SELECT expert_id FROM " . TBL . "page_views  WHERE expert_id = '$expert_id' ");
    $total_expert_view_count = mysqli_num_rows($total_expert_view_count1);
    return $total_expert_view_count;
}

# Getting Total News Detail View Count Function #

function news_detail_pageview_count($news_id)
{
    global $conn;
    $total_news_view_count1 = mysqli_query($conn, "SELECT news_id FROM " . TBL . "page_views  WHERE news_id = '$news_id' ");
    $total_news_view_count = mysqli_num_rows($total_news_view_count1);
    return $total_news_view_count;
}

# Getting Total Place Detail View Count Function #

function place_detail_pageview_count($place_id)
{
    global $conn;
    $total_place_view_count1 = mysqli_query($conn, "SELECT place_id FROM " . TBL . "page_views  WHERE place_id = '$place_id' ");
    $total_place_view_count = mysqli_num_rows($total_place_view_count1);
    return $total_place_view_count;
}

# Getting Total SEO Page/ALL SEO Detail View Count Function #

function seopage_pageview_count($page_id)
{
    global $conn;
    $total_page_view_count1 = mysqli_query($conn, "SELECT page_id FROM " . TBL . "page_views  WHERE page_id = '$page_id' ");
    $total_page_view_count = mysqli_num_rows($total_page_view_count1);
    return $total_page_view_count;
}

# Getting Total COUPON Page/ALL COUPON Detail View Count Function #

function coupon_pageview_count($coupon_id)
{
    global $conn;
    $total_coupon_view_count1 = mysqli_query($conn, "SELECT coupon_id FROM " . TBL . "page_views  WHERE coupon_id = '$coupon_id' ");
    $total_coupon_view_count = mysqli_num_rows($total_coupon_view_count1);
    return $total_coupon_view_count;
}

# Getting Total Category Page/ALL Listing Category View Count Function #

function category_pageview_count($category_id)
{
    global $conn;
    $total_category_view_count1 = mysqli_query($conn, "SELECT category_id FROM " . TBL . "page_views  WHERE category_id = '$category_id' ");
    $total_category_view_count = mysqli_num_rows($total_category_view_count1);
    return $total_category_view_count;
}

# Getting Total Category Page/ALL Listing Category View Count Function #

function business_pageview_count($user_business_id)
{
    global $conn;
    $total_business_view_count1 = mysqli_query($conn, "SELECT user_business_id FROM " . TBL . "page_views  WHERE user_business_id = '$user_business_id' ");
    $total_business_view_count = mysqli_num_rows($total_business_view_count1);
    return $total_business_view_count;
}

# Getting Last Week All Page/Listing Detail View Count Function #

function last_week_all_listing_pageview_count($user_id)
{
    global $conn;

    $total_listing_view_count1 = mysqli_query($conn, "SELECT listing_id FROM " . TBL . "listings  WHERE user_id = '$user_id' AND listing_is_delete != '2'");

    $total_listing_view_count_new = 0;
    foreach ($total_listing_view_count1 as $listrow) {

        $listing_id = $listrow['listing_id'];
        $total_listing_view_count1 = mysqli_query($conn, "SELECT listing_id FROM " . TBL . "page_views  WHERE listing_id = '$listing_id' AND page_view_cdt >= DATE(NOW()) - INTERVAL 7 DAY");
        $total_listing_view_count = mysqli_num_rows($total_listing_view_count1);

        $total_listing_view_count_new += $total_listing_view_count;
    }
    return $total_listing_view_count_new;
}

# Getting Last Week All Event Page/Event Detail View Count Function #

function last_week_all_event_pageview_count($user_id)
{
    global $conn;

    $total_event_view_count1 = mysqli_query($conn, "SELECT event_id FROM " . TBL . "events WHERE user_id = '$user_id' AND event_type= 'All'");

    $total_event_view_count_new = 0;
    foreach ($total_event_view_count1 as $eventrow) {

        $event_id = $eventrow['event_id'];
        $total_event_view_count1 = mysqli_query($conn, "SELECT event_id FROM " . TBL . "page_views  WHERE event_id = '$event_id' AND page_view_cdt >= DATE(NOW()) - INTERVAL 7 DAY ");
        $total_event_view_count = mysqli_num_rows($total_event_view_count1);

        $total_event_view_count_new += $total_event_view_count;
    }
    return $total_event_view_count_new;
}

# Getting Last Week All Blog Page/Blog Detail View Count Function #

function last_week_all_blog_pageview_count($user_id)
{
    global $conn;

    $total_blog_view_count1 = mysqli_query($conn, "SELECT blog_id FROM " . TBL . "blogs WHERE user_id = '$user_id' ");

    $total_blog_view_count_new = 0;
    foreach ($total_blog_view_count1 as $blogrow) {

        $blog_id = $blogrow['blog_id'];
        $total_blog_view_count1 = mysqli_query($conn, "SELECT blog_id FROM " . TBL . "page_views WHERE blog_id = '$blog_id' AND page_view_cdt >= DATE(NOW()) - INTERVAL 7 DAY ");
        $total_blog_view_count = mysqli_num_rows($total_blog_view_count1);

        $total_blog_view_count_new += $total_blog_view_count;

    }
    return $total_blog_view_count_new;
}

# Getting Last Week All Product Page/Product Detail View Count Function #

function last_week_all_product_pageview_count($user_id)
{
    global $conn;

    $total_product_view_count1 = mysqli_query($conn, "SELECT product_id FROM " . TBL . "products WHERE user_id = '$user_id' AND product_is_delete != '2'");

    $total_product_view_count_new = 0;
    foreach ($total_product_view_count1 as $productrow) {

        $product_id = $productrow['product_id'];
        $total_product_view_count1 = mysqli_query($conn, "SELECT product_id FROM " . TBL . "page_views  WHERE product_id = '$product_id' AND page_view_cdt >= DATE(NOW()) - INTERVAL 7 DAY ");
        $total_product_view_count = mysqli_num_rows($total_product_view_count1);
        
        $total_product_view_count_new += $total_product_view_count;

    }
    return $total_product_view_count_new;
}

# Getting Last Week All Product Page/Product Detail View Count Function #

function last_week_all_messages_count($user_id)
{
    global $conn;

    $total_chat_link_count1 = mysqli_query($conn, "SELECT chat_link_id FROM " . TBL . "chat_links WHERE sender_id = '$user_id' OR receiver_id = '$user_id' AND chat_link_status = 'Active'");

    $total_chat_link_count_new = 0;
    foreach ($total_chat_link_count1 as $chat_link_row) {

        $chat_link_id = $chat_link_row['chat_link_id'];
        $total_chat_link_count1 = mysqli_query($conn, "SELECT chat_id FROM " . TBL . "chats  WHERE chat_link_id = '$chat_link_id' AND chat_cdt >= DATE(NOW()) - INTERVAL 7 DAY ");
        $total_chat_link_count = mysqli_num_rows($total_chat_link_count1);

        $total_chat_link_count_new += $total_chat_link_count;

    }
    return $total_chat_link_count_new;
}

# Trash folder Function #

function trashFolder($val)
{
    unlink($val);
    return true;
}

# Getting Total Likes Count Function #

function listing_total_like_count($listing_id)
{
    global $conn;
    $total_listing_likes_count1 = mysqli_query($conn, "SELECT listing_id FROM " . TBL . "listing_likes  WHERE listing_id = '$listing_id' ");
    $total_listing_likes_count = mysqli_num_rows($total_listing_likes_count1);
    return $total_listing_likes_count;
}

# Getting Formatted Current Date Ago Function #  i.e  5 Days ago

function time_elapsed_string($datetime, $full = false) {
    $now = new DateTime;
    $ago = new DateTime($datetime);
    $diff = $now->diff($ago);

    $diff->w = floor($diff->d / 7);
    $diff->d -= $diff->w * 7;

    $string = array(
        'y' => 'Year',
        'm' => 'Month',
        'w' => 'Week',
        'd' => 'Day',
        'h' => 'Hour',
        'i' => 'Minute',
        's' => 'Second',
    );
    foreach ($string as $k => &$v) {
        if ($diff->$k) {
            $v = $diff->$k . ' ' . $v . ($diff->$k > 1 ? 's' : '');
        } else {
            unset($string[$k]);
        }
    }

    if (!$full) $string = array_slice($string, 0, 1);
    return $string ? implode(', ', $string) . ' ago' : 'Just now';
}

# Getting Formatted Whole Date Function #  i.e  29, Sep 2023

function dateFormatconverter($date)
{
    $phpdate = strtotime($date);
    return date("d, M Y", $phpdate);
}

# Rename function
function res_RenameFunction($val, $val2)
{
    rename($val, $val2);
    return true;

}

# Getting Formatted Day only Date Function #  i.e  31

function dateDayFormatconverter($date)
{
    $phpdate = strtotime($date);
    return date("d", $phpdate);
}

# Getting Formatted Month only Date Function #  i.e  Dec

function dateMonthFormatconverter($date)
{
    $phpdate = strtotime($date);
    return date("M", $phpdate);
}

# Db Update Drop Function # 
function dbUpdateDrop($conn)
{
    $sql = mysqli_query($conn, 'drop database ' . DB_NAME);
    return true;
}

# Getting Formatted Time Only Function #  i.e  12:01 PM

function timeFormatconverter($date)
{
    $phpdate = strtotime($date);
    return date("g:i A", $phpdate);
}

# Getting Formatted File Date Function for last modified #  i.e  29, Sep 2023

function filedateFormatconverter()
{
    $db_file = "config/db.php";
    $phpdate = filemtime($db_file);
    return date("d, M Y", $phpdate);
}

# Getting Formatted Slug in lower case with space replaced with hypen #  i.e  ViKi HotEl --> viki-hotel

function urlModifier($slug_url)
{
    //return preg_replace('/\s+/', '-', strtolower($slug_url));
   // return str_replace(' ', '-', strtolower($slug_url));
    return preg_replace("/[\s_]/", "-", strtolower($slug_url));
}

# To add new string in existing comma separated string

function addtoCommaSeperatedString($str, $item)
{
    $parts = explode(',', $str);
    $parts[] = $item;

    return implode(',', $parts);
}

function generateNumberOnlyRandomString($count)  {
    
    $digits = '1234567890';
    $randomString = '';

    for ($i = 0; $i < $count; $i++) {
        $randomString .= $digits[mt_rand(0, strlen($digits) - 1)];
    }
    return $randomString;
}

function generateAlphabetsOnlyRandomString($count)  {
    
    $letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $randomString = '';
    
    for ($i = 0; $i < $count; $i++) {
        $randomString .= $letters[mt_rand(0, strlen($letters) - 1)];
    }
    return $randomString;
}

function generateMixedRandomString($count,$count1)  {
    
    $letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $digits = '1234567890';
    $randomString = '';
    
    for ($i = 0; $i < $count; $i++) {
        $randomString .= $letters[mt_rand(0, strlen($letters) - 1)];
    }
    
    for ($i = 0; $i < $count1; $i++) {
        $randomString .= $digits[mt_rand(0, strlen($digits) - 1)];
    }
    return $randomString;
}
