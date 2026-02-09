<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */


if (file_exists('config/info.php')) {
    include('config/info.php');
}

if (isset($_GET['messageenquirymessageenquirymessageenquirymessageenquiry'])) {

    $enquiry_id = $_GET['messageenquirymessageenquirymessageenquirymessageenquiry'];
    $status = $_GET['status'];

    $path = $_GET['path'];

    if ($status == 1) {
        $new_status = 0;
    } else {
        $new_status = 1;
    }


    $sql = mysqli_query($conn, "UPDATE  " . TBL . "enquiries SET  enquiry_save='" . $new_status . "'
     where enquiry_id='" . $enquiry_id . "'");


    if ($sql) {
        if ($path == "saved") {

            header('Location: admin-all-enquiry.php');
        } else {
            header('Location: admin-all-enquiry.php');
        }


    } else {

        if ($path == "saved") {
            header('Location: admin-all-enquiry.php');
        } else {
            header('Location: admin-all-enquiry.php');
        }

    }

}