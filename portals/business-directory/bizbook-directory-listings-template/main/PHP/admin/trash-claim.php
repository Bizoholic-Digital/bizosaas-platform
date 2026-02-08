<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if(isset($_GET['trashclaimrequesttrashclaimrequesttrashclaimrequesttrashclaimrequesttrashclaimrequest'])){

    $claim_listing_id = $_GET['trashclaimrequesttrashclaimrequesttrashclaimrequesttrashclaimrequesttrashclaimrequest'];
    $enquiry_image = $_GET['enquiry_image'];


    $listing_qry = "DELETE  FROM " . TBL . "claim_listings  where claim_listing_id ='" . $claim_listing_id . "'";

    $listing_res = mysqli_query($conn,$listing_qry);



    if ($listing_res) {

        unlink('../images/listings/'.$enquiry_image);  //Delete the claim image

        $_SESSION['status_msg'] = "Claim Request has been Deleted Successfully!!!";

        header('Location: admin-claim-listing.php');
    } else {

        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: admin-claim-listing.php');
    }


}else{
    header('Location: admin-claim-listing.php');
    exit();
}