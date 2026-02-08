<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['sub_admin_submit'])) {

        $admin_id = $_POST['admin_id'];
        $admin_name = $_POST['admin_name'];


        $admin_qry =
            " DELETE FROM  " . TBL . "admin  WHERE admin_id='" . $admin_id . "'";


        $admin_res = mysqli_query($conn,$admin_qry);


        if ($admin_res) {

            $_SESSION['status_msg'] = "Sub Admin has been Permanently Deleted!!!";


            header('Location: admin-sub-admin-all.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-sub-admin-delete.php?row=' . $admin_id);
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-sub-admin-all.php');
}