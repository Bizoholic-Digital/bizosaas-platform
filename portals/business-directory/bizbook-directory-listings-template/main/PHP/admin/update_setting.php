<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['setting_submit'])) {

        $website_address = $_POST['website_address'];
        $admin_primary_email = $_POST['admin_primary_email'];
        $currency_symbol = $_POST['currency_symbol'];

        $admin_recovery_email = $_POST['admin_recovery_email']; // Admin Forget password recovery email

        $footer_id = $_POST['footer_id'];

        //Super Admin Data's
        $admin_id = 1;
        $admin_email = $_POST['admin_email'];
        $admin_name = $_POST['admin_name'];

        $admin_password_old = $_POST['admin_password_old'];

        if ($_POST["admin_password"] != NULL) {

            $admin_password = md5($_POST["admin_password"]);
        } else {
            $admin_password = $admin_password_old;
        }

        $admin_language = $_POST['admin_language'];
        $admin_photo_old = $_POST['admin_photo_old'];
        $home_page_fav_icon_old = $_POST['home_page_fav_icon_old'];
        $home_page_banner_old = $_POST['home_page_banner_old'];

        $admin_countries123 = $_POST["admin_countries"];

        $admin_seo_title = $_POST["admin_seo_title"];
        $admin_seo_description = $_POST["admin_seo_description"];
        $admin_seo_keywords = $_POST["admin_seo_keywords"];

        $admin_google_login = $_POST["admin_google_login"];
        $admin_facebook_login = $_POST["admin_facebook_login"];

        $admin_google_client_id = $_POST["admin_google_client_id"];
        $admin_google_client_secret = $_POST["admin_google_client_secret"];
        $admin_facebook_app_id = $_POST["admin_facebook_app_id"];

        $admin_geo_map_api = $_POST["admin_geo_map_api"];
        $admin_geo_default_latitude = $_POST["admin_geo_default_latitude"];
        $admin_geo_default_longitude = $_POST["admin_geo_default_longitude"];
        $admin_geo_default_zoom = $_POST["admin_geo_default_zoom"];

//        if($_POST["admin_listing_show"] == "on"){
            $admin_listing_show = 1;
//        }else{
//            $admin_listing_show = 0;
//        }

        if($_POST["admin_job_show"] == "on"){
            $admin_job_show = 1;
        }else{
            $admin_job_show = 0;
        }

        if($_POST["admin_expert_show"] == "on"){
            $admin_expert_show = 1;
        }else{
            $admin_expert_show = 0;
        }

        if($_POST["admin_product_show"] == "on"){
            $admin_product_show = 1;
        }else{
            $admin_product_show = 0;
        }

        if($_POST["admin_blog_show"] == "on"){
            $admin_blog_show = 1;
        }else{
            $admin_blog_show = 0;
        }

        if($_POST["admin_event_show"] == "on"){
            $admin_event_show = 1;
        }else{
            $admin_event_show = 0;
        }

        if($_POST["admin_news_show"] == "on"){
            $admin_news_show = 1;
        }else{
            $admin_news_show = 0;
        }

        if($_POST["admin_place_show"] == "on"){
            $admin_place_show = 1;
        }else{
            $admin_place_show = 0;
        }

        if($_POST["admin_coupon_show"] == "on"){
            $admin_coupon_show = 1;
        }else{
            $admin_coupon_show = 0;
        }

        $prefix = $fruitList = '';
        foreach ($admin_countries123 as $fruit) {
            $admin_countries .= $prefix . $fruit;
            $prefix = ',';
        }

        $_FILES['home_page_fav_icon']['name'];

        if (!empty($_FILES['home_page_fav_icon']['name'])) {
            $file = rand(1000, 100000) . $_FILES['home_page_fav_icon']['name'];
            $file_loc = $_FILES['home_page_fav_icon']['tmp_name'];
            $file_size = $_FILES['home_page_fav_icon']['size'];
            $file_type = $_FILES['home_page_fav_icon']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../images/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $home_page_fav_icon = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $home_page_fav_icon = $home_page_fav_icon_old;
            }
        } else {
            $home_page_fav_icon = $home_page_fav_icon_old;
        }

        $_FILES['home_page_banner']['name'];

        if (!empty($_FILES['home_page_banner']['name'])) {
            $file = rand(1000, 100000) . $_FILES['home_page_banner']['name'];
            $file_loc = $_FILES['home_page_banner']['tmp_name'];
            $file_size = $_FILES['home_page_banner']['size'];
            $file_type = $_FILES['home_page_banner']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../images/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $home_page_banner = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $home_page_banner = $home_page_banner_old;
            }
        } else {
            $home_page_banner = $home_page_banner_old;
        }

        $_FILES['admin_photo']['name'];

        if (!empty($_FILES['admin_photo']['name'])) {
            $file = rand(1000, 100000) . $_FILES['admin_photo']['name'];
            $file_loc = $_FILES['admin_photo']['tmp_name'];
            $file_size = $_FILES['admin_photo']['size'];
            $file_type = $_FILES['admin_photo']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../images/user/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $admin_photo = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $admin_photo = $admin_photo_old;
            }
        } else {
            $admin_photo = $admin_photo_old;
        }


        $sql = mysqli_query($conn, "UPDATE  " . TBL . "footer SET  website_address='" . $website_address . "'
        ,admin_primary_email='" . $admin_primary_email . "', currency_symbol='" . $currency_symbol . "'
        , admin_language='" . $admin_language . "', admin_countries='" . $admin_countries . "'
        , admin_google_client_id='" . $admin_google_client_id . "', admin_google_client_secret='" . $admin_google_client_secret . "'
        , admin_facebook_app_id='" . $admin_facebook_app_id . "', admin_seo_title='" . $admin_seo_title . "'
        , admin_seo_description='" . $admin_seo_description . "', admin_seo_keywords='" . $admin_seo_keywords . "'
        , home_page_fav_icon='" . $home_page_fav_icon . "', home_page_banner='" . $home_page_banner . "'
        , admin_google_login='" . $admin_google_login . "', admin_facebook_login='" . $admin_facebook_login . "'
        , admin_geo_map_api='" . $admin_geo_map_api . "', admin_geo_default_latitude='" . $admin_geo_default_latitude . "'
        , admin_geo_default_longitude='" . $admin_geo_default_longitude . "', admin_geo_default_zoom='" . $admin_geo_default_zoom . "'
        , admin_listing_show='" . $admin_listing_show . "', admin_job_show='" . $admin_job_show . "'
        , admin_expert_show='" . $admin_expert_show . "', admin_product_show='" . $admin_product_show . "'
        , admin_blog_show='" . $admin_blog_show . "', admin_event_show='" . $admin_event_show . "'
        , admin_news_show='" . $admin_news_show . "', admin_place_show='" . $admin_place_show . "'
        , admin_coupon_show='" . $admin_coupon_show . "'
        where footer_id='" . $footer_id . "'");

        $sql1 = mysqli_query($conn, "UPDATE  " . TBL . "admin SET admin_name='" . $admin_name . "', admin_email='" . $admin_email . "'
        , admin_password='" . $admin_password . "', admin_photo='" . $admin_photo . "' , admin_recovery_email='" . $admin_recovery_email . "'  where admin_id='" . $admin_id . "'");

        if ($sql && $sql1) {

            // Logic To Delete Other Countries/States/Cities Starts

//            if($admin_countries != NULL) {
//
//                $countryy_rs = mysqli_query($conn, "SELECT * FROM " . TBL . "countries WHERE country_id NOT IN ($admin_countries)");
//
//                while ($countryy_row = mysqli_fetch_array($countryy_rs)) {
//
//                    $countryy_id = $countryy_row['country_id'];
//
//                    $statee_rs = mysqli_query($conn, "SELECT * FROM " . TBL . "states WHERE country_id = $countryy_id");
//
//                    while ($statee_row = mysqli_fetch_array($statee_rs)) {
//
//                        $statee_id = $statee_row['state_id'];
//
//                        $cityy_rs_del = mysqli_query($conn,"DELETE FROM  " . TBL . "cities where state_id = $statee_id ");
//                    }
//
//                    $statee_rs_del = mysqli_query($conn,"DELETE FROM  " . TBL . "states  where country_id= $countryy_id ");
//                }
//
//                $countryy_rs_del = mysqli_query($conn,"DELETE FROM  " . TBL . "countries WHERE country_id NOT IN ($admin_countries)");
//
//            }

            // Logic To Delete Other Countries/States/Cities Ends

            $_SESSION['status_msg'] = "Setting Data has been Updated Successfully!!!";

            header('Location: admin-setting.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-setting.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-setting.php');
    exit;
}
?>