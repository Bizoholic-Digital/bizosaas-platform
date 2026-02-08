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


       // $user_id = $_POST['user_id']; //Session data
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

//        if ($promote_start_date > $promote_end_date) {
//
//            $_SESSION['status_msg'] = "Oops!! Your Start date is greater than End Date!! Try Other!!!";
//            header('Location: ' . $url);
//            exit;
//        }


        $listing_details_sql = "SELECT * FROM  " . TBL . "listings where listing_id='" . $promote_type_id . "'";
        $listing_details_rs = mysqli_query($conn, $listing_details_sql);
        $listing_details_row = mysqli_fetch_array($listing_details_rs);

        $user_id = $listing_details_row['user_id'];

//        $existing_points = $user_details_row['user_points'];
//
//        $current_minus_points = $existing_points - $promote_total_cost;
//
//
//        if ($existing_points < $promote_total_cost) {
//
//            $_SESSION['status_msg'] = "Oops!! You don't have enough points to promote your listing!! Buy some points!!";
//
//            header('Location: ' . $url);
//            exit;
//        }


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

//                $traupqry = "UPDATE " . TBL . "users
//					  SET user_points = $current_minus_points
//					  WHERE user_id = $user_id";
//
//                $traupres = mysqli_query($conn, $traupqry);
//
//                if ($traupres) {

                    $_SESSION['status_msg'] = "The Listing has been promoted successfully!!!";

                    header('Location: admin-all-promotions.php');
                    exit;
//                }

            }
        } //to be deleted ends

        else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-all-listings.php');
            exit;
        }
    } else {

        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: admin-all-listings.php');
        exit;
    }

} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-all-listings.php');
    exit;
}
?>