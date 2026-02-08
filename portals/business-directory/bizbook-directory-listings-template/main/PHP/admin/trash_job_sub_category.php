<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['sub_category_submit'])) {

        $sub_category_id = $_POST['sub_category_id'];
        $sub_category_name = $_POST['sub_category_name'];


        $sub_category_qry =
            " DELETE FROM  " . TBL . "job_sub_categories  WHERE sub_category_id='" . $sub_category_id . "'";


        $sub_category_res = mysqli_query($conn,$sub_category_qry);


        if ($sub_category_res) {

            $_SESSION['status_msg'] = "Sub Category has been Permanently Deleted!!!";


            header('Location: admin-all-job-sub-category.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-job-sub-category-delete.php?row=' . $sub_category_id);
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-job-sub-category.php');
}