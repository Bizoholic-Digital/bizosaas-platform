<?php
if (file_exists('config/info.php')) {
    include('config/info.php');
}

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

$user_id = $_SESSION['user_id'];

if (isset($user_id)) {

    $user_details_row = getUser($user_id); //Fetch Logged In user data
    $user_plan = $user_details_row['user_plan']; //Fetch of Logged In user Plan

    $user_plan_type = getPlanType($user_plan); //Fetch Logged In User Plan details and data
}else{

    header('Location: index');
    exit;
}

$footer_row = getAllFooter(); //Fetch Footer Data


$user_code = $_SESSION['user_code'];  //User Code

// Update Billing details of user starts


$user_country = $_POST["user_country"];
$user_state = $_POST["user_state"];
$user_city = $_POST["user_city"];
$user_address = $_POST["user_address"];
$user_zip_code = $_POST["user_zip_code"];
$user_contact_name = $_POST["user_contact_name"];
$user_contact_mobile = $_POST["user_contact_mobile"];
$user_contact_email = $_POST["user_contact_email"];
$payment_status = "COD";

$upqry = "UPDATE " . TBL . "users  SET user_country = '$user_country'
        , user_state = '$user_state', user_city = '$user_city', user_address = '$user_address'
        , user_zip_code = '$user_zip_code', user_contact_name = '$user_contact_name'
        , user_contact_mobile = '$user_contact_mobile', user_contact_email = '$user_contact_email'
        , payment_status = '$payment_status' WHERE user_id = $user_id";

$upres = mysqli_query($conn,$upqry);

// Update Billing details of user ends
if($upres) {
    $_SESSION['status_msg'] = $BIZBOOK['COD_PAYMENT_SUCCESS_MESSAGE'];

    header('Location: db-invoice-all');
    exit();
}