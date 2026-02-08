<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['create_promote_submit'])) {


        $user_id = $_SESSION['user_id']; //Session data
        $all_promote_price_id = $_POST["all_ads_price_id"];
        $url = $_POST["url"];

        $promote_start_date_old = $_POST["ad_start_date"];
        $timestamp1 = strtotime($promote_start_date_old);
        $promote_start_date = date('Y-m-d H:i:s', $timestamp1);

        $promote_end_date_old = $_POST["ad_end_date"];
        $timestamp = strtotime($promote_end_date_old);
        $promote_end_date = date('Y-m-d H:i:s', $timestamp);

        $promote_total_days = $_POST["ad_total_days"];
        $promote_cost_per_day = $_POST["ad_cost_per_day"];
        $promote_total_cost = $_POST["ad_total_cost"];
        $promote_type_value = $_POST["type_value"];
        $promote_type_id = $_POST["type_id"];

        $display_position = 101;  //Position Id

        if ($promote_start_date > $promote_end_date) {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_START_DATE_IS_GREATER'];
            header('Location: ' . $url);
            exit;
        }


        $user_details_sql = "SELECT * FROM  " . TBL . "users where user_id='" . $_SESSION['user_id'] . "'";
        $user_details_rs = mysqli_query($conn, $user_details_sql);
        $user_details_row = mysqli_fetch_array($user_details_rs);

        $existing_points = $user_details_row['user_points'];

        $current_minus_points = $existing_points - $promote_total_cost;


        if ($existing_points < $promote_total_cost) {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_DONT_HAVE_ENOUGH_POINTS_BUY_SOME_POINTS'];

            header('Location: ' . $url);
            exit;
        }


        $promote_enquiry_status = "Active";


        $qry = "INSERT INTO " . TBL . "all_promote_enquiry 
					(user_id,all_promote_price_id, promote_start_date, promote_end_date, promote_type_id, promote_type_value
					,promote_total_days, promote_cost_per_day, promote_total_cost, promote_enquiry_status, promote_enquiry_cdt) 
					VALUES ('$user_id', '$all_promote_price_id', '$promote_start_date', '$promote_end_date', '$promote_type_id' , '$promote_type_value'
					, '$promote_total_days', '$promote_cost_per_day', '$promote_total_cost', '$promote_enquiry_status', '$curDate')";

        $res = mysqli_query($conn, $qry);
        $promote_id = mysqli_insert_id($conn);


        if ($res) {

            //to be deleted starts


            $lisupqry = "UPDATE " . TBL . "listings 
					  SET display_position = $display_position
					  ,start_date = '$promote_start_date',end_date = '$promote_end_date'
					  ,payment = 1
					  WHERE listing_id = $promote_type_id";

            $lisupres = mysqli_query($conn, $lisupqry);

            if ($lisupres) {

                $traupqry = "UPDATE " . TBL . "users 
					  SET user_points = $current_minus_points
					  WHERE user_id = $user_id";

                $traupres = mysqli_query($conn, $traupqry);

                if ($traupres) {

                    $_SESSION['status_msg'] = $BIZBOOK['LISTING_PROMOTE_SUCCESS_MESSAGE'];

                    header('Location: db-promote');
                    exit;
                }

            }

//to be deleted ends


        } else {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: db-promote');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: db-promote');
    exit;
}
?>