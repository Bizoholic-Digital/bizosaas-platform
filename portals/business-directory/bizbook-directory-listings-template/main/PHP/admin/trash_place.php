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
        $place_qry =
            " DELETE FROM  " . TBL . "places WHERE place_id='" . $place_id . "'";


        $place_res = mysqli_query($conn,$place_qry);


        if ($place_res) {
            unlink('../places/images/places/'.$place_banner_image_old);  //Delete the profile image

            $gallery_image_array = explode(',', $place_gallery_image_old);
            foreach ($gallery_image_array as $tuple) {
                unlink('../places/images/places/' . $tuple);  //Delete all the gallery image(s)
            }

            //Query to delete the page view starts

            $page_view_qry = "DELETE FROM  " . TBL . "page_views where place_id='" . $place_id . "'";

            $page_view_res = mysqli_query($conn,$page_view_qry);

            //Query to delete the page view ends


            $_SESSION['status_msg'] = "Place has been Permanently Deleted!!!";
            header('Location: place-all.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: place-delete.php?code=' . $place_id);
        }

        // Place Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: place-all.php');
}