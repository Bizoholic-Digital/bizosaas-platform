<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */


if(file_exists('config/info.php'))
{
    include('config/info.php');
}

if(isset($_GET['code'])){

    $all_points_enquiry_id = $_GET['code'];


    $listing_qry = "DELETE  FROM " . TBL . "all_points_enquiry  where all_points_enquiry_id='" . $all_points_enquiry_id . "'";

    $listing_res = mysqli_query($conn,$listing_qry);



    if ($listing_res) {

        $_SESSION['status_msg'] = "Points History has been Deleted Successfully!!!";

        header('Location: admin-all-points.php');
    } else {

        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: admin-all-points.php');
    }


}