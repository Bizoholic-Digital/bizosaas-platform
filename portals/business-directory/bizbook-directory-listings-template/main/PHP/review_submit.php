<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}


//    Review Insert Part Starts

$listing_id = $_POST["listing_id"];
$listing_user_id = $_POST["listing_user_id"];
$review_user_id = $_POST["review_user_id"];

$price_rating = $_POST["price_rating"];
$customer_service_rating = $_POST["customer_service_rating"];
$staff_rating = $_POST["staff_rating"];
$overall_rating = $_POST["overall_rating"];
$review_name = $_POST["review_name"];
$review_email = $_POST["review_email"];
$review_mobile = $_POST["review_mobile"];
$review_city = $_POST["review_city"];
$review_message = addslashes($_POST["review_message"]);
$review_status = "Active";


$review_qry = "INSERT INTO " . TBL . "reviews 
					(listing_id, listing_user_id, review_user_id, price_rating, customer_service_rating, staff_rating, overall_rating, review_name, review_email, review_mobile, review_city, review_message, review_status, review_cdt) 
					VALUES 
					('$listing_id', '$listing_user_id', '$review_user_id','$price_rating','$customer_service_rating','$staff_rating','$overall_rating','$review_name', '$review_email', '$review_mobile', '$review_city', '$review_message','$review_status',  '$curDate')";

$review_res = mysqli_query($conn,$review_qry);

if ($review_res) {
    echo '1';
} else {
    echo '2';
}

//    Review Insert Part Ends

