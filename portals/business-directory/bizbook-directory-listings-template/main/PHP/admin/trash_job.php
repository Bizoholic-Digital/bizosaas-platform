<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['job_submit'])) {

        $job_id = $_POST["job_id"];
        $company_logo_old = $_POST["company_logo_old"];

        $job_qry = "DELETE FROM  " . TBL . "jobs where job_id='" . $job_id . "'";

        $job_res = mysqli_query($conn,$job_qry);


        if ($job_res) {

            unlink('../jobs/images/jobs/'.$company_logo_old);  //Delete the Job Company image
            //Query to delete the page view starts

            $page_view_qry = "DELETE FROM  " . TBL . "page_views where job_id='" . $job_id . "'";

            $page_view_res = mysqli_query($conn,$page_view_qry);

            //Query to delete the page view ends  

            $_SESSION['status_msg'] = "Job has been Deleted Successfully!!!";

            header('Location: job-all.php');

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: job-all.php');
        }

        //    Jobs Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: job-all.php');
}