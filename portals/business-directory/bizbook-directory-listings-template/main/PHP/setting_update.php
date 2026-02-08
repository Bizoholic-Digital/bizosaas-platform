<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['setting_update_submit'])) {


        $user_code = $_SESSION['user_code']; //Session User Code
        $user_id = $_SESSION['user_id']; //Session User Code

        // $first_name = $_POST["first_name"];
        $setting_user_status = $_POST["setting_user_status"];
        $setting_review = $_POST["setting_review"];
        $setting_share = $_POST["setting_share"];
        $setting_profile_show = $_POST["setting_profile_show"];
        $setting_guarantee_show = $_POST["setting_guarantee_show"];


        //if($_POST["setting_listing_show"] == "on"){
            $setting_listing_show = 1;
//        }else{
//            $setting_listing_show = 0;
//        }

        if($_POST["setting_job_show"] == "on"){
            $setting_job_show = 1;
        }else{
            $setting_job_show = 0;
        }

        if($_POST["setting_expert_show"] == "on"){
            $setting_expert_show = 1;
        }else{
            $setting_expert_show = 0;
        }

        if($_POST["setting_product_show"] == "on"){
            $setting_product_show = 1;
        }else{
            $setting_product_show = 0;
        }

        if($_POST["setting_blog_show"] == "on"){
            $setting_blog_show = 1;
        }else{
            $setting_blog_show = 0;
        }

        if($_POST["setting_event_show"] == "on"){
            $setting_event_show = 1;
        }else{
            $setting_event_show = 0;
        }

        if($_POST["setting_coupon_show"] == "on"){
            $setting_coupon_show = 1;
        }else{
            $setting_coupon_show = 0;
        }

        if ($setting_user_status == 2) {

            //Delete user from user table
            $user_sql =
                " DELETE FROM  " . TBL . "users  WHERE user_id='" . $user_id . "'";

            $user_sql_res = mysqli_query($conn,$user_sql);


            //Delete user listings from listing table

            $list =
                " DELETE FROM  " . TBL . "listings  WHERE user_id='" . $user_id . "'";

            $list_res = mysqli_query($conn,$list);

            //Delete user products from product table

            $product =
                " DELETE FROM  " . TBL . "products  WHERE user_id='" . $user_id . "'";

            $product_res = mysqli_query($conn,$product);


            //Delete user Events from events table

            $events =
                " DELETE FROM  " . TBL . "events  WHERE user_id='" . $user_id . "'";

            $events_res = mysqli_query($conn,$events);


            //Delete user Blogs from blogs table

            $blogs =
                " DELETE FROM  " . TBL . "blogs  WHERE user_id='" . $user_id . "'";

            $blogs_res = mysqli_query($conn,$blogs);

            //Delete user Jobs from jobs table

            $jobs =
                " DELETE FROM  " . TBL . "jobs  WHERE user_id='" . $user_id . "'";

            $jobs_res = mysqli_query($conn,$jobs);

            //Delete user Experts from Experts table

            $experts =
                " DELETE FROM  " . TBL . "experts WHERE user_id='" . $user_id . "'";

            $experts_res = mysqli_query($conn,$experts);

            
            if($user_sql_res){
                
                header('Location: logout');
                exit;
            }else{
                $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

                header('Location: db-setting');
                exit;
            }

        } else {


            $sql = mysqli_query($conn, "UPDATE  " . TBL . "users SET  setting_user_status='" . $setting_user_status . "'
     ,setting_review='" . $setting_review . "', setting_share='" . $setting_share . "', setting_profile_show='" . $setting_profile_show . "'
     ,setting_guarantee_show='" . $setting_guarantee_show . "', setting_listing_show='" . $setting_listing_show . "'
     ,setting_job_show='" . $setting_job_show . "', setting_expert_show='" . $setting_expert_show . "'
     ,setting_product_show='" . $setting_product_show . "', setting_blog_show='" . $setting_blog_show . "'
     ,setting_event_show='" . $setting_event_show . "', setting_coupon_show='" . $setting_coupon_show . "'
     where user_code='" . $user_code . "'");

            if ($sql) {

                $_SESSION['status_msg'] = $BIZBOOK['USER_SETTING_UPDATE_SUCCESS_MESSAGE'];


                header('Location: db-setting');
                exit;

            } else {

                $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

                header('Location: db-setting');
                exit;
            }

        }
    }
} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: db-setting');
    exit;
}
?>