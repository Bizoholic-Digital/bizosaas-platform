<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['plan_type_submit'])) {


        $plan_type_id = $_POST['plan_type_id'];
        $plan_type_name = $_POST['plan_type_name'];
        $plan_type_price = $_POST['plan_type_price'];
        $plan_type_duration = $_POST['plan_type_duration'];
        $plan_type_points = $_POST['plan_type_points'];
        $plan_type_status = "Active";

        $plan_type_listing_count = $_POST['plan_type_listing_count'];
        $plan_type_product_count = $_POST['plan_type_product_count'];
        $plan_type_event_count = $_POST['plan_type_event_count'];
        $plan_type_blog_count = $_POST['plan_type_blog_count'];
        $plan_type_job_count = $_POST['plan_type_job_count'];

        $plan_type_direct_lead = $_POST['plan_type_direct_lead'];
        $plan_type_email_notification = $_POST['plan_type_email_notification'];
        $plan_type_verified = $_POST['plan_type_verified'];
        $plan_type_trusted = $_POST['plan_type_trusted'];



        $plan_type_description1 = $_POST['plan_type_description'];
        if($plan_type_description1 != NULL || !empty($plan_type_description1)){
            $plan_type_description = 1;
        }else{
            $plan_type_description = 1; //Default description to be enabled
        }

        $plan_type_contact1 = $_POST['plan_type_contact'];
        if($plan_type_contact1 != NULL || !empty($plan_type_contact1)){
            $plan_type_contact = 1;
        }else{
            $plan_type_contact = 1;
        }

        $plan_type_ratings = $_POST['plan_type_ratings'];


        $plan_type_social = $_POST['plan_type_social'];


        $plan_type_videos1 = $_POST['plan_type_videos'];
        if($plan_type_videos1 != NULL || !empty($plan_type_videos1)){
            $plan_type_videos = 1;
        }else{
            $plan_type_videos = 1;
        }

        $plan_type_maps1 = $_POST['plan_type_maps'];
        if($plan_type_maps1 != NULL || !empty($plan_type_maps1)){
            $plan_type_maps = 1;
        }else{
            $plan_type_maps = 1;
        }

        $plan_type_threedview1 = $_POST['plan_type_threedview'];
        if($plan_type_threedview1 != NULL || !empty($plan_type_threedview1)){
            $plan_type_threedview = 1;
        }else{
            $plan_type_threedview = 1;
        }

        $plan_type_services1 = $_POST['plan_type_services'];
        $plan_type_services_count1 = $_POST['plan_type_services_count'];
        if($plan_type_services1 != NULL || !empty($plan_type_services1)){
            $plan_type_services = 1;

            if($plan_type_services_count1 == NULL || empty($plan_type_services_count1)){
                $plan_type_services_count = 1;

            }else{
                $plan_type_services_count = $plan_type_services_count1;
            }

        }else{
            $plan_type_services = 1;
            $plan_type_services_count = 0;
        }


        $plan_type_offers = $_POST['plan_type_offers'];
        $plan_type_offers_count1 = $_POST['plan_type_offers_count'];
        if($plan_type_offers1 != NULL || !empty($plan_type_offers1)){
            $plan_type_offers = 1;

            if($plan_type_offers_count1 == NULL || empty($plan_type_offers_count1)){
                $plan_type_offers_count = 1;

            }else{
                $plan_type_offers_count = $plan_type_offers_count1;
            }

        }else{
            $plan_type_offers = 0;
            $plan_type_offers_count= 0;
        }

        $plan_type_photos1 = $_POST['plan_type_photos'];
        $plan_type_photos_count1 = $_POST['plan_type_photos_count'];
//        if($plan_type_photos1 != NULL || !empty($plan_type_photos1)){
            $plan_type_photos = 1;

            if($plan_type_photos_count1 == NULL || empty($plan_type_photos_count1)){
                $plan_type_photos_count = 1;

            }else{
                $plan_type_photos_count = $plan_type_photos_count1;
            }

//        }else{
//            $plan_type_photos = 1;
//        }

        $plan_type_videos1 = $_POST['plan_type_videos'];
        $plan_type_videos_count1 = $_POST['plan_type_videos_count'];
//        if($plan_type_videos1 != NULL || !empty($plan_type_videos1)){
        $plan_type_videos = 1;

        if($plan_type_videos_count1 == NULL || empty($plan_type_videos_count1)){
            $plan_type_videos_count = 1;

        }else{
            $plan_type_videos_count = $plan_type_videos_count1;
        }

//        }else{
//            $plan_type_videos = 1;
//        }




        $sql = mysqli_query($conn,"UPDATE  " . TBL . "plan_type SET plan_type_name='" . $plan_type_name . "', plan_type_price='" . $plan_type_price. "'
     , plan_type_duration='" . $plan_type_duration . "', plan_type_description='" . $plan_type_description . "', plan_type_contact='" . $plan_type_contact. "'
     , plan_type_listing_count='" . $plan_type_listing_count . "', plan_type_product_count='" . $plan_type_product_count . "', plan_type_event_count='" . $plan_type_event_count . "'
     , plan_type_blog_count='" . $plan_type_blog_count. "', plan_type_job_count='" . $plan_type_job_count. "'
     , plan_type_direct_lead='" . $plan_type_direct_lead . "', plan_type_email_notification='" . $plan_type_email_notification . "', plan_type_verified='" . $plan_type_verified. "'
     , plan_type_trusted='" . $plan_type_trusted . "', plan_type_points='" . $plan_type_points . "'
     , plan_type_ratings='" . $plan_type_ratings . "', plan_type_social='" . $plan_type_social . "', plan_type_videos='" . $plan_type_videos. "', plan_type_videos_count='" . $plan_type_videos_count. "'
     , plan_type_maps='" . $plan_type_maps . "', plan_type_threedview='" . $plan_type_threedview . "', plan_type_services='" . $plan_type_services. "'
     , plan_type_services_count='" . $plan_type_services_count . "' , plan_type_offers='" . $plan_type_offers . "', plan_type_offers_count='" . $plan_type_offers_count . "'
     , plan_type_photos='" . $plan_type_photos. "' , plan_type_photos_count='" . $plan_type_photos_count . "', plan_type_status='" . $plan_type_status . "'
     where plan_type_id='" . $plan_type_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Pricing Plan Type has been Updated Successfully!!!";


            header('Location: admin-price.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-price-edit.php?row=' . $plan_type_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-price.php');
    exit;
}
?>