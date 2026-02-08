<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if(file_exists('config/user_authentication.php'))
{
    include('config/user_authentication.php');
}

if(file_exists('config/info.php'))
{
    include('config/info.php');
}

if(isset($_GET['code'])){

    $all_points_enquiry_id = $_GET['code'];


    $listing_qry = "DELETE  FROM " . TBL . "all_points_enquiry  where all_points_enquiry_id='" . $all_points_enquiry_id . "'";

    $listing_res = mysqli_query($conn,$listing_qry);



    if ($listing_res) {

        $_SESSION['status_msg'] = $BIZBOOK['POINTS_DELETE_SUCCESS_MESSAGE'];

        header('Location: db-point-history');
    } else {

        $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

        header('Location: db-point-history');
    }


}