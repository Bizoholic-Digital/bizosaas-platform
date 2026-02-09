<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['listing_submit'])) {

        $listing_id = $_POST["listing_id"];


        $listing_code = $_POST['listing_code'];

        $profile_image_old = $_POST["profile_image_old"];
        $cover_image_old = $_POST["cover_image_old"];
        $gallery_image_old = $_POST["gallery_image_old"];
        $service_image_old = $_POST["service_image_old"];
        $service_1_image_old = $_POST["service_1_image_old"];

        $listing_qry =
            " DELETE FROM  " . TBL . "listings WHERE listing_id='" . $listing_id . "'";


        $listing_res = mysqli_query($conn,$listing_qry);


        if ($listing_res) {
            unlink('../images/listings/'.$profile_image_old);  //Delete the profile image
            unlink('../images/listing-ban/'.$cover_image_old);  //Delete the Cover image

            $gallery_image_array = explode(',', $gallery_image_old);
            foreach ($gallery_image_array as $tuple) {
                unlink('../images/listings/' . $tuple);  //Delete all the gallery image(s)
            }

            $service_image_array = explode(',', $service_image_old);
            foreach ($service_image_array as $tuple) {
                unlink('../images/services/' . $tuple);  //Delete all the Service image(s)
            }

            $service_1_image_array = explode(',', $service_1_image_old);
            foreach ($service_1_image_array as $tuple) {
                unlink('../images/services/' . $tuple);  //Delete all the offer image(s)
            }

            //Query to delete the page view starts

            $page_view_qry = "DELETE FROM  " . TBL . "page_views where listing_id='" . $listing_id . "'";

            $page_view_res = mysqli_query($conn,$page_view_qry);

            //Query to delete the page view ends


            $_SESSION['status_msg'] = "Listing has been Permanently Deleted!!!";
            header('Location: admin-trash-listing.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-delete-listings.php?path=trash&code=' . $listing_code);
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-trash-listing.php');
}