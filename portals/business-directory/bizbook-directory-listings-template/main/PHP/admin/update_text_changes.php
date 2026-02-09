<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['all_text_submit'])) {

        $all_text_id = 1;
        
        $banner_title = mysqli_real_escape_string($conn,$_POST['banner_title']);
        $banner_sub_title = mysqli_real_escape_string($conn,$_POST['banner_sub_title']);
        
        $explore_title = mysqli_real_escape_string($conn,$_POST['explore_title']);
        $explore_light_title = mysqli_real_escape_string($conn,$_POST['explore_light_title']);
        $explore_sub_title = mysqli_real_escape_string($conn,$_POST['explore_sub_title']);
        
        $service_title = mysqli_real_escape_string($conn,$_POST['service_title']);
        $service_light_title = mysqli_real_escape_string($conn,$_POST['service_light_title']);
        $service_sub_title = mysqli_real_escape_string($conn,$_POST['service_sub_title']);
        
        $branding_title = mysqli_real_escape_string($conn,$_POST['branding_title']);
        
        $feature_title = mysqli_real_escape_string($conn,$_POST['feature_title']);
        $feature_light_title = mysqli_real_escape_string($conn,$_POST['feature_light_title']);
        $feature_sub_title = mysqli_real_escape_string($conn,$_POST['feature_sub_title']);
        
        $quick_title = mysqli_real_escape_string($conn,$_POST['quick_title']);
        $quick_light_title = mysqli_real_escape_string($conn,$_POST['quick_light_title']);
        $quick_sub_title = mysqli_real_escape_string($conn,$_POST['quick_sub_title']);
        
        $world_title = mysqli_real_escape_string($conn,$_POST['world_title']);
        $world_sub_title = mysqli_real_escape_string($conn,$_POST['world_sub_title']);
        
        $footer_title = mysqli_real_escape_string($conn,$_POST['footer_title']);
        $footer_sub_title = mysqli_real_escape_string($conn,$_POST['footer_sub_title']);
        
        $price_title_1 = mysqli_real_escape_string($conn,$_POST['price_title_1']);
        $price_title_2 = mysqli_real_escape_string($conn,$_POST['price_title_2']);
        $price_sub_title = mysqli_real_escape_string($conn,$_POST['price_sub_title']);


        $sql = mysqli_query($conn,"UPDATE " . TBL . "all_texts SET banner_title='" . $banner_title . "'
        ,banner_sub_title='" . $banner_sub_title . "',explore_title='" . $explore_title . "',explore_light_title='" . $explore_light_title . "'
        ,explore_sub_title='" . $explore_sub_title . "',service_title='" . $service_title . "',service_light_title='" . $service_light_title . "'
        ,service_sub_title='" . $service_sub_title . "',branding_title='" . $branding_title . "'
        ,feature_title='" . $feature_title . "',feature_light_title='" . $feature_light_title . "',feature_sub_title='" . $feature_sub_title . "'
        ,quick_title='" . $quick_title . "',quick_light_title='" . $quick_light_title . "',quick_sub_title='" . $quick_sub_title . "'
        ,world_title='" . $world_title . "', world_sub_title='" . $world_sub_title . "'
        ,footer_title='" . $footer_title . "',footer_sub_title='" . $footer_sub_title . "',price_title_1='" . $price_title_1 . "'
        ,price_title_2='" . $price_title_2 . "',price_sub_title='" . $price_sub_title . "'
        WHERE all_text_id='" . $all_text_id . "'");
        

        if ($sql) {

            $_SESSION['status_msg'] = "Admin Text Change has been Updated Successfully!!!";


            header('Location: admin-text-changes.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-text-changes.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-text-changes.php');
    exit;
}
?>