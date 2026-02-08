<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */


if (file_exists('config/info.php')) {
    include('config/info.php');
}

if (isset($_GET['reviewreviewreviewreviewreviewreview'])) {

    $review_id = $_GET['reviewreviewreviewreviewreviewreview'];
    $status = $_GET['status'];

    $path = $_GET['path'];

    if ($status == 1) {
        $new_status = 0;
    } else {
        $new_status = 1;
    }


    $sql = mysqli_query($conn, "UPDATE  " . TBL . "reviews SET  review_save='" . $new_status . "'
     where review_id='" . $review_id . "'");


    if ($sql) {
        if ($path == "saved") {
            header('Location: admin-saved-reviews.php');
        } else {
            header('Location: admin-all-reviews.php');
        }


    } else {

        if ($path == "saved") {
            header('Location: admin-saved-reviews.php');
        } else {
            header('Location: admin-all-reviews.php');
        }

    }

}