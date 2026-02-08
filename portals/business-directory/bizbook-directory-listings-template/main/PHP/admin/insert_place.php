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


// Common Place Details
        $place_name = addslashes($_POST["place_name"]);
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


// Listing Timing Details
        $opening_time = $_POST["opening_time"];
        $closing_time = $_POST["closing_time"];
        $google_map = $_POST["google_map"];

//Place Other Information
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

// Place Status

        function checkPlaceSlug($link, $counter = 1)
        {
            global $conn;
            $newLink = $link;
            do {
                $checkLink = mysqli_query($conn, "SELECT place_id FROM " . TBL . "places WHERE place_slug = '$newLink'");
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
        $place_slug = checkPlaceSlug($place_name1);

        $place_banner_image = '';

// ************************  Gallery Image Upload starts  **************************

        $all_place_gallery_image = $_FILES['place_gallery_image'];
        $all_place_gallery_image23 = $_FILES['place_gallery_image']['name'];

        for ($k = 0; $k < count($all_place_gallery_image23); $k++) {


            if (!empty($all_place_gallery_image['name'][$k])) {
                $file1 = rand(1000, 100000) . $all_place_gallery_image['name'][$k];
                $file_loc1 = $all_place_gallery_image['tmp_name'][$k];
                $file_size1 = $all_place_gallery_image['size'][$k];
                $file_type1 = $all_place_gallery_image['type'][$k];
                $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
                if (in_array($file_type1, $allowed)) {
                    $folder1 = "../places/images/places/";
                    $new_size = $file_size1 / 1024;
                    $new_file_name1 = strtolower($file1);
                    $event_image1 = str_replace(' ', '-', $new_file_name1);
                    //move_uploaded_file($file_loc1, $folder1 . $event_image1);
                    $place_gallery_image1[] = compressImage($event_image1, $file_loc1, $folder1, $new_size);
                } else {
                    $place_gallery_image1[] = '';
                }
            }

        }
        $place_gallery_image = implode(",", $place_gallery_image1);

// ************************  Gallery Image Upload ends  **************************

//    Place Insert Part Starts

        $place_qry = "INSERT INTO " . TBL . "places
					(category_id, place_name, place_tags, place_fee
					, seo_title, seo_description
					, seo_keywords, places_news, place_experts
					, place_events, place_listings, place_related, place_discover
					, place_banner_image, place_gallery_image
					, opening_time, closing_time, google_map, place_status
					, place_info_question , place_info_answer, place_slug, place_cdt)
					VALUES
					('$category_id', '$place_name', '$place_tags', '$place_fee'
					, '$seo_title', '$seo_description'
					, '$seo_keywords', '$places_news', '$place_experts'
					, '$place_events', '$place_listings', '$place_related', '$place_discover'
					, '$place_banner_image', '$place_gallery_image'
					, '$opening_time', '$closing_time', '$google_map', '$place_status'
					, '$place_info_question', '$place_info_answer', '$place_slug', '$curDate')";

        $place_res = mysqli_query($conn, $place_qry);
        $PlaceID = mysqli_insert_id($conn);
        $placelastID = $PlaceID;

        switch (strlen($PlaceID)) {
            case 1:
                $PlaceID = '00' . $PlaceID;
                break;
            case 2:
                $PlaceID = '0' . $PlaceID;
                break;
            default:
                $PlaceID = $PlaceID;
                break;
        }

        $PlaceCode = 'PLACE' . $PlaceID;

        $placeupqry = "UPDATE " . TBL . "places
					  SET place_code = '$PlaceCode'
					  WHERE place_id = $placelastID";

        $placeupres = mysqli_query($conn, $placeupqry);


        if ($placeupres) {

            $_SESSION['status_msg'] = "New Place has been created Successfully!!!";

            header('Location: place-all.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: place-add-new.php');
        }

        //    Place Insert Part Ends

    } else {

        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: place-add-new.php');
    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: place-add-new.php');
}