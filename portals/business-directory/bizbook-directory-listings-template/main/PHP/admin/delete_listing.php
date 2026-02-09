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

        $listing_is_delete = $_POST["listing_is_delete"];

        if($listing_is_delete == 2){
            $listing_delete_status = 0;
        }elseif($listing_is_delete == 0){
            $listing_delete_status = 2;
        }



        $listing_code = $_POST['listing_code'];


        $listing_qry =
            "UPDATE  " . TBL . "listings  SET listing_is_delete='" . $listing_delete_status . "', listing_delete_cdt ='" . $curDate. "'  where listing_id='" . $listing_id . "'";


        $listing_res = mysqli_query($conn,$listing_qry);


        if ($listing_res) {

            if($listing_is_delete == 2){
                $_SESSION['status_msg'] = "Listing has been Restored Successfully!!!";
            }elseif($listing_is_delete == 0){
                $_SESSION['status_msg'] = "Listing has been Deleted Successfully!!!";
            }


            header('Location: admin-all-listings.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-delete-listings.php?code=' . $listing_code);
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-all-listings.php');
}