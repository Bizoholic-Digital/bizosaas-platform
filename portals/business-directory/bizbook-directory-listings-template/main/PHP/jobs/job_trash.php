<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('job-config-info.php')) {
    include "job-config-info.php";
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['job_submit'])) {

        $job_id = $_POST["job_id"];
        $company_logo_old = $_POST["company_logo_old"];

        $job_qry = "DELETE FROM  " . TBL . "jobs where job_id='" . $job_id . "'";
        
        $job_res = mysqli_query($conn,$job_qry);


        if ($job_res) {

            unlink('images/jobs/'.$company_logo_old);  //Delete the Job Company image
            //Query to delete the page view starts

            $page_view_qry = "DELETE FROM  " . TBL . "page_views where job_id='" . $job_id . "'";

            $page_view_res = mysqli_query($conn,$page_view_qry);

            //Query to delete the page view ends  

            $_SESSION['status_msg'] = $BIZBOOK['JOB_DELETE_SUCCESS_MESSAGE'];

            header('Location: db-jobs');

        } else {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: db-jobs');
        }

        //    Jobs Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: ../dashboard');
}