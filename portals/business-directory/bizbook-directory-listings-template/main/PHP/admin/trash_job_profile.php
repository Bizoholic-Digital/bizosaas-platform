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

if(isset($_GET['jobprofilejobprofilejobprofilejobprofile'])){

    $job_profile_id = $_GET['jobprofilejobprofilejobprofilejobprofile'];


    $listing_qry =
        "DELETE  FROM " . TBL . "job_profile  where job_profile_id='" . $job_profile_id . "'";

    $listing_res = mysqli_query($conn,$listing_qry);



    if ($listing_res) {

        $_SESSION['status_msg'] = $BIZBOOK['JOB_PROFILE_DELETE_SUCCESS_MESSAGE'];

        header('Location: job-seeker-details.php');
    } else {

        $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

        header('Location: job-seeker-details.php');
    }

}