<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */


if(file_exists('config/info.php'))
{
    include('config/info.php');
}

if(isset($_GET['messageenquirymessageenquirymessageenquirymessageenquiry'])){

    $enquiry_id = $_GET['messageenquirymessageenquirymessageenquirymessageenquiry'];

    $path = $_GET['path'];


    $listing_qry =
        "DELETE  FROM " . TBL . "expert_enquiries  where enquiry_id='" . $enquiry_id . "'";

    $listing_res = mysqli_query($conn,$listing_qry);



    if ($listing_res) {

        $_SESSION['status_msg'] = "Service Expert Booking has been Deleted Successfully!!!";

        if($path == 1){
            header('Location: expert-general-leads.php');
            exit();
        }else{
            header('Location: expert-leads.php');
            exit();
        }


    } else {

        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        if($path == 1){
            header('Location: expert-general-leads.php');
            exit();
        }else{
            header('Location: expert-leads.php');
            exit();
        }
    }


}