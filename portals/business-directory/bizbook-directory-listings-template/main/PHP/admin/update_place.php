<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['place_submit'])) {

        $place_id = $_POST["place_id"];

        $place_banner_image_old = $_POST["place_banner_image_old"];
        $place_gallery_image_old = $_POST["place_gallery_image_old"];

        $place_name = $_POST["place_name"];
        $place_tags = $_POST["place_tags"];
        $place_fee = $_POST["place_fee"];

        $seo_title = $_POST["seo_title"];
        $seo_description = $_POST["seo_description"];
        $seo_keywords = $_POST["seo_keywords"];
        $place_status = $_POST["place_status"];

        $place_discover1 = $_POST["place_discover"];
        $prefix = $fruitList = '';
        foreach ($place_discover1 as $fruit) {
            $place_discover .= $prefix . $fruit;
            $prefix = ',';
        }

        $place_related1 = $_POST["place_related"];
        $prefix = $fruitList = '';
        foreach ($place_related1 as $fruit) {
            $place_related .= $prefix . $fruit;
            $prefix = ',';
        }

        $place_listings1 = $_POST["place_listings"];
        $prefix = $fruitList = '';
        foreach ($place_listings1 as $fruit) {
            $place_listings .= $prefix . $fruit;
            $prefix = ',';
        }

        $place_events1 = $_POST["place_events"];
        $prefix = $fruitList = '';
        foreach ($place_events1 as $fruit) {
            $place_events .= $prefix . $fruit;
            $prefix = ',';
        }

        $place_experts1 = $_POST["place_experts"];
        $prefix = $fruitList = '';
        foreach ($place_experts1 as $fruit) {
            $place_experts .= $prefix . $fruit;
            $prefix = ',';
        }

        $places_news1 = $_POST["places_news"];
        $prefix = $fruitList = '';
        foreach ($places_news1 as $fruit) {
            $places_news .= $prefix . $fruit;
            $prefix = ',';
        }

        $category_id = $_POST["category_id"];


// Place Timing Details
        $opening_time = $_POST["opening_time"];
        $closing_time = $_POST["closing_time"];
        $google_map = $_POST["google_map"];

// Place Other Information
        $place_info_question123 = $_POST["place_info_question"];
        $prefix1 = $fruitList = '';
        foreach ($place_info_question123 as $fruit1) {
            $place_info_question .= $prefix1 . $fruit1;
            $prefix1 = ',';
        }

        $place_info_answer123 = $_POST["place_info_answer"];
        $prefix1 = $fruitList = '';
        foreach ($place_info_answer123 as $fruit1) {
            $place_info_answer .= $prefix1 . $fruit1;
            $prefix1 = ',';
        }


        function checkPlaceSlug($link, $place_id, $counter = 1)
        {
            global $conn;
            $newLink = $link;
            do {
                $checkLink = mysqli_query($conn, "SELECT place_id FROM " . TBL . "places WHERE places_slug = '$newLink' AND place_id != '$place_id'");
                if (mysqli_num_rows($checkLink) > 0) {
                    $newLink = $link . '' . $counter;
                    $counter++;
                } else {
                    break;
                }
            } while (1);

            return $newLink;
        }


        $place_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $place_name));
        $place_slug = checkPlaceSlug($place_name1, $place_id);

         $place_banner_image = '';

// ************************  Gallery Image Upload starts  **************************

        $all_place_gallery_image = $_FILES['place_gallery_image'];
        $all_place_gallery_image23 = $_FILES['place_gallery_image']['name'];

        if (count(array_filter($_FILES['place_gallery_image']['name'])) <= 0) {
            $place_gallery_image = $place_gallery_image_old;
        } else {


            for ($k = 0; $k < count($all_place_gallery_image23); $k++) {


                if (!empty($all_place_gallery_image['name'][$k])) {
                    $file1 = rand(1000, 100000) . $all_place_gallery_image['name'][$k];
                    $file_loc1 = $all_place_gallery_image['tmp_name'][$k];
                    $file_size1 = $all_place_gallery_image['size'][$k];
                    $file_type1 = $all_place_gallery_image['type'][$k];
                    $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
                    if (in_array($file_type1, $allowed)) {
                        $folder1 = "../places/images/places/";
                        $new_size1 = $file_size1 / 1024;
                        $new_file_name1 = strtolower($file1);
                        $event_image1 = str_replace(' ', '-', $new_file_name1);
                        //move_uploaded_file($file_loc1, $folder1 . $event_image1);
                        $place_gallery_image1[] = compressImage($event_image1, $file_loc1, $folder1, $new_size1);
                    } else {
                        $place_gallery_image1[] = '';
                    }

                }


            }
            $place_gallery_image = implode(",", $place_gallery_image1);
        }

        // ************************  Gallery Image Upload ends  **************************


        $place_qry =
            "UPDATE  " . TBL . "places  SET category_id='" . $category_id . "'
            , place_name='" . $place_name . "'
            , place_tags='" . $place_tags . "', place_fee='" . $place_fee . "'
            , seo_title='" . $seo_title . "', seo_description='" . $seo_description . "'
            , seo_keywords='" . $seo_keywords . "', places_news='" . $places_news . "'
            , place_experts='" . $place_experts . "', place_events='" . $place_events . "'
            , place_listings='" . $place_listings . "', place_related='" . $place_related . "'
            , place_discover='" . $place_discover . "', place_banner_image='" . $place_banner_image . "'
            , place_gallery_image='" . $place_gallery_image . "', opening_time='" . $opening_time . "'
            , closing_time ='" . $closing_time . "', google_map ='" . $google_map . "', place_status ='" . $place_status . "'
            , place_info_question ='" . $place_info_question . "', place_info_answer ='" . $place_info_answer . "'
            , place_slug ='" . $place_slug . "' where place_id ='" . $place_id . "'";

        $place_res = mysqli_query($conn, $place_qry);

        if ($place_res) {

                $_SESSION['status_msg'] = "Your Places has been Updated Successfully!!!";

                header('Location: place-all.php');
                exit;


        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: place-edit.php?code=' . $place_id);
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: place-all.php');
    exit;
}