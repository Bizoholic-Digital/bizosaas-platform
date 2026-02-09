<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */


if(file_exists('config/info.php'))
{
    include('config/info.php');
}

if(isset($_GET['placerequestplacerequestplacerequestplacerequestplacerequestplacerequestplacerequestplacerequest'])){

    $place_request_id = $_GET['placerequestplacerequestplacerequestplacerequestplacerequestplacerequestplacerequestplacerequest'];


    $place_request_qry =
        "DELETE  FROM " . TBL . "place_request where place_request_id='" . $place_request_id . "'";

    $place_request_res = mysqli_query($conn,$place_request_qry);



    if ($place_request_res) {

        $_SESSION['status_msg'] = "Place Request has been Deleted Successfully!!!";

        header('Location: place-request.php');
    } else {

        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: place-request.php');
    }


}