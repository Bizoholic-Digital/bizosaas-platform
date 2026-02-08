<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['category_submit'])) {

        $category_id = $_POST['category_id'];
        $category_name = $_POST['category_name'];


        $category_qry =
            " DELETE FROM  " . TBL . "job_skill WHERE category_id='" . $category_id . "'";


        $category_res = mysqli_query($conn,$category_qry);


        if ($category_res) {

            $_SESSION['status_msg'] = "Job Skill set has been Permanently Deleted!!!";


            header('Location: admin-all-job-skill-set.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-job-skill-set-delete.php?row=' . $category_id);
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-all-job-skill-set.php');
}