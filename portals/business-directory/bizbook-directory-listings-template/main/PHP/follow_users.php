<?php

if (file_exists('config/info.php')) {
    include('config/info.php');
}

$sender_user_id = isset($_POST['sender']) ? $_POST['sender'] : "";
$user_id = isset($_POST['user']) ? $_POST['user'] : "";

$check_user_followers = mysqli_query($conn, "SELECT * FROM " . TBL . "users  WHERE FIND_IN_SET('" . $sender_user_id . "',user_followers) AND user_id = '$user_id' ");
$check_user_followers_no_of_rows = mysqli_num_rows($check_user_followers);

if ($check_user_followers_no_of_rows <= 0) {
    
     //Add as Follower
    
    $comma_sender_user_id = ',' . $sender_user_id;

    $insert_user_followers = mysqli_query($conn, "UPDATE " . TBL . "users SET user_followers = IF (user_followers = '', $sender_user_id, CONCAT(user_followers, '$comma_sender_user_id')) WHERE find_in_set('$sender_user_id',user_followers) = 0  AND user_id = '$user_id'");

    echo 0;

} else {
    
   //Delete as Follower
    
    $delete_user_followers = mysqli_query($conn, "UPDATE " . TBL . "users SET user_followers = TRIM(BOTH ',' FROM REPLACE(REPLACE(user_followers, '$sender_user_id', ''), ',,', ',')) WHERE user_id = '$user_id'");

    echo 1;
}