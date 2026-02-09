<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['job_premium_submit'])) {

        $job_name_old = $_POST['job_name_old'];
        $job_name = $_POST['job_name'];
        $job_popular_id = $_POST['job_popular_id'];



//************ Listing Name Already Exist Check Starts ***************

        if($job_name_old != $job_name) {
            $listing_name_exist_check = mysqli_query($conn,"SELECT * FROM " . TBL . "job_popular WHERE job_name='" . $job_name . "' ");


            if (mysqli_num_rows($listing_name_exist_check) > 0) {


                $_SESSION['status_msg'] = "The Given Home page Premium Job is Already Exist Try Other!!!";

                header('Location: jobs-premium-edit.php?row=' . $job_popular_id);
                exit;


            }
        }

//************ Listing Name Already Exist Check Ends ***************


        $sql = mysqli_query($conn,"UPDATE  " . TBL . "job_popular SET job_name ='" . $job_name . "'
     where job_popular_id='" . $job_popular_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Home page Premium Job has been Updated Successfully!!!";


            header('Location: jobs-premium.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: jobs-premium-edit.php?row=' . $job_popular_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: jobs-premium.php');
    exit;
}
?>