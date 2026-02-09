<?php

if (file_exists('config/info.php')) {
    include('config/info.php');
}

$listing_id = isset($_POST['listing']) ? $_POST['listing'] : "";
$user_id = isset($_POST['user']) ? $_POST['user'] : "";
$listing_user_id = isset($_POST['listing_user']) ? $_POST['listing_user'] : "";

$check_listing_likes = mysqli_query($conn,"SELECT * FROM " . TBL . "listing_likes  WHERE listing_id = '$listing_id' AND user_id = '$user_id' ");
$check_listing_likes_no_of_rows = mysqli_num_rows($check_listing_likes);

if ($check_listing_likes_no_of_rows <= 0) {
    $insert_listing_likes = mysqli_query($conn,"INSERT INTO " . TBL . "listing_likes (`listing_id`, `listing_user_id`, `user_id`, `listing_likes_cdt`) values('$listing_id','$listing_user_id','$user_id',NOW())");

    echo 1;
} else {

    $listing_likes_row = mysqli_fetch_array($check_listing_likes);
    $listing_likes_id = $listing_likes_row['listing_likes_id'];

    $delete_listing_likes = mysqli_query($conn,"DELETE FROM " . TBL . "listing_likes WHERE listing_likes_id = '$listing_likes_id'");

    echo 0;
}