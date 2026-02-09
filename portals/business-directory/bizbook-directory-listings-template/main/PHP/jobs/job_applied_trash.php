<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if(file_exists('../config/user_authentication.php'))
{
    include('../config/user_authentication.php');
}

if(file_exists('job-config-info.php'))
{
    include "job-config-info.php";
}

if(isset($_GET['jobappliedjobappliedjobappliedjobapplied'])){

    $job_applied_id = $_GET['jobappliedjobappliedjobappliedjobapplied'];
    $code = $_GET['code'];


    $listing_qry =
        "DELETE  FROM " . TBL . "job_applied  where job_applied_id='" . $job_applied_id . "'";

    $listing_res = mysqli_query($conn,$listing_qry);



    if ($listing_res) {

        $_SESSION['status_msg'] = $BIZBOOK['JOB_APPLIED_DELETE_SUCCESS_MESSAGE'];

        header('Location: db-jobs-applicant-profile?code='.$code);
    } else {

        $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

        header('Location: db-jobs-applicant-profile?code='.$code);
    }

}