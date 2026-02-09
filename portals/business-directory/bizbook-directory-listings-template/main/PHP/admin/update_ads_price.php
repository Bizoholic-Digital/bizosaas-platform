<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['ad_price_submit'])) {

        $all_ads_price_id = $_POST['all_ads_price_id'];
        $ad_price_name = $_POST['ad_price_name'];

        $ad_price_photo_old = $_POST['ad_price_photo_old'];
        $ad_price_size = $_POST['ad_price_size'];
        $ad_price_cost = $_POST['ad_price_cost'];
        $ad_price_status = $_POST['ad_price_status'];

        $_FILES['ad_price_photo']['name'];

        if (!empty($_FILES['ad_price_photo']['name'])) {
            $file = rand(1000, 100000) . $_FILES['ad_price_photo']['name'];
            $file_loc = $_FILES['ad_price_photo']['tmp_name'];
            $file_size = $_FILES['ad_price_photo']['size'];
            $file_type = $_FILES['ad_price_photo']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../images/ads/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $ad_price_photo = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $ad_price_photo = $ad_price_photo_old;
            }
        } else {
            $ad_price_photo = $ad_price_photo_old;
        }


        $sql = mysqli_query($conn, "UPDATE  " . TBL . "all_ads_price SET ad_price_name='" . $ad_price_name . "'
        , ad_price_size='" . $ad_price_size . "', ad_price_cost='" . $ad_price_cost . "'
        , ad_price_status='" . $ad_price_status . "', ad_price_photo='" . $ad_price_photo . "'
     where all_ads_price_id='" . $all_ads_price_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Ads Price has been Updated Successfully!!!";


            header('Location: admin-ads-price.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-ads-price-edit.php?row=' . $all_ads_price_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-ads-price.php');
    exit;
}
?>