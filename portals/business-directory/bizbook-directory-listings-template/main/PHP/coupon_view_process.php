<?php

if (file_exists('config/info.php')) {
    include('config/info.php');
}

$coupon_id = isset($_POST['coupon_id']) ? $_POST['coupon_id'] : "";


couponpageview($coupon_id); //Function To Find Coupon Page View

//******* Add/Update the Coupon used members data starts **********

$coupon_sql = "SELECT * FROM  " . TBL . "coupons where coupon_id='" . $coupon_id . "'";
$coupon_rs = mysqli_query($conn, $coupon_sql);
$coupon_row = mysqli_fetch_array($coupon_rs);

$coupon_owner_user_id = $coupon_row['coupon_user_id'];
$current_session_user_id = $_SESSION['user_id'];


$coupon_use_members = $coupon_row['coupon_use_members'];

if($coupon_owner_user_id != $current_session_user_id ){

    if($coupon_use_members != NULL){

        $comma_sep_members = explode(',',$coupon_use_members);

        if (in_array($current_session_user_id, $comma_sep_members)) {
            return true;
        } else {

            $new_array_use_members = addtoCommaSeperatedString($coupon_use_members, $current_session_user_id);

            $coupon_update_qry ="UPDATE  " . TBL . "coupons SET coupon_use_members='" . $new_array_use_members . "' where coupon_id='" . $coupon_id . "'";

            $coupon_update_qry_res = mysqli_query($conn,$coupon_update_qry);
        }

    }else{

        $coupon_insert_qry = "UPDATE  " . TBL . "coupons SET coupon_use_members='" . $current_session_user_id . "' where coupon_id='" . $coupon_id . "'";

        $coupon_insert_qry_res = mysqli_query($conn,$coupon_insert_qry);

    }
}

//******* Add/Update the Coupon used members data ends **********