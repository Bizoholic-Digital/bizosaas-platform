<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

//database configuration
if (file_exists('expert-config-info.php')) {
    include "expert-config-info.php";
}

if(isset($_GET['messageenquirymessageenquirymessageenquirymessageenquiry'])){

    $enquiry_id = $_GET['messageenquirymessageenquirymessageenquirymessageenquiry'];

    $return_url = $_GET['return-url'];


    $listing_qry =
        "DELETE  FROM " . TBL . "expert_enquiries where enquiry_id='" . $enquiry_id . "'";

    $listing_res = mysqli_query($conn,$listing_qry);



    if ($listing_res) {

        $_SESSION['status_msg'] = $BIZBOOK['SERVICE_EXPERT_ENQUIRY_DELETE_SUCCESS_MESSAGE'];

        header('Location: '.$return_url);
    } else {

        $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

        header('Location: '.$return_url);
    }

}