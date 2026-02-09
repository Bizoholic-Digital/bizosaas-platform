<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if (isset($_GET['jobappliedjobappliedjobappliedjobapplied'])) {

    $job_applied_id = $_GET['jobappliedjobappliedjobappliedjobapplied'];
    $path = $_GET['path'];


    $listing_qry =
        "DELETE  FROM " . TBL . "job_applied  where job_applied_id='" . $job_applied_id . "'";

    $listing_res = mysqli_query($conn, $listing_qry);


    if ($listing_res) {

        $_SESSION['status_msg'] = $BIZBOOK['JOB_APPLIED_DELETE_SUCCESS_MESSAGE'];

        if ($path == 2) {
            header('Location: job-all-applied.php');
        } else {
            header('Location: job-applicant-profiles.php');
        }
    } else {

        $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

        if ($path == 2) {
            header('Location: job-all-applied.php');
        } else {
            header('Location: job-applicant-profiles.php');
        }
    }

}