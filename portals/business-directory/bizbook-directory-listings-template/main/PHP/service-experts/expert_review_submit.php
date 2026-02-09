<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('expert-config-info.php')) {
    include "expert-config-info.php";
}


//    Review Insert Part Starts

$expert_id = $_POST["expert_id"];
$expert_user_id = $_POST["expert_user_id"];
$review_user_id = $_POST["review_user_id"];


$expert_rating = $_POST["expert_rating"];
$expert_message = addslashes($_POST["expert_message"]);
$review_status = "Active";

if ($_POST["enquiry_id"] == 0 || $_POST["enquiry_id"] == '') {

    $expert_enquiry_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "expert_enquiries WHERE expert_id='" . $expert_id . "' AND expert_user_id='" . $expert_user_id . "'  AND enquiry_sender_id ='" . $review_user_id . "' ORDER BY enquiry_id DESC ");

    $expert_enquiry_fetch_row = mysqli_fetch_array($expert_enquiry_exist_check);

    $enquiry_id = $expert_enquiry_fetch_row['enquiry_id'];
} else {

    $enquiry_id = $_POST["enquiry_id"];
}


$expert_review_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "expert_reviews WHERE expert_id='" . $expert_id . "' AND expert_user_id='" . $expert_user_id . "'  AND review_user_id='" . $review_user_id . "'  AND enquiry_id='" . $enquiry_id . "' ");

if (mysqli_num_rows($expert_review_exist_check) > 0) {

    $expert_review_fetch_row = mysqli_fetch_array($expert_review_exist_check);

    $review_id = $expert_review_fetch_row['review_id'];

    $review_res = mysqli_query($conn, "UPDATE  " . TBL . "expert_reviews SET expert_rating='" . $expert_rating . "'
     , expert_message='" . $expert_message . "', review_status='" . $review_status . "', review_cdt ='" . $curDate . "'
       where review_id ='" . $review_id . "'");

} else {


    $review_qry = "INSERT INTO " . TBL . "expert_reviews
					(expert_id, expert_user_id, review_user_id, enquiry_id, expert_rating, expert_message, review_status, review_cdt)
					VALUES 
					('$expert_id', '$expert_user_id', '$review_user_id', '$enquiry_id', '$expert_rating', '$expert_message','$review_status',  '$curDate')";

    $review_res = mysqli_query($conn, $review_qry);
}

if ($review_res) {
    echo '1';
} else {
    echo '2';
}

//    Review Insert Part Ends