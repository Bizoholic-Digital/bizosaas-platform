<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

//database configuration
if (file_exists('expert-config-info.php')) {
    include "expert-config-info.php";
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
//    Expert Manage Lead Update Part Starts

    $expert_id = $_POST["expert_user_id"];
    $enquiry_id = $_POST["enquiry_id"];
    $appointment_date1 = $_POST["appointment_date"];
    $appointment_time = $_POST["appointment_time"];
    $enquiry_status = $_POST["enquiry_status"];

    $appointment_date =  date("Y-m-d", strtotime($appointment_date1) );

    $enquiry_res = mysqli_query($conn, "UPDATE  " . TBL . "expert_enquiries SET  appointment_time ='" . $appointment_time . "'
     ,appointment_date ='" . $appointment_date . "'
     ,enquiry_status ='" . $enquiry_status . "'
     ,enquiry_udt = '$curDate'
     where enquiry_id='" . $enquiry_id . "'");

    if ($enquiry_res) {

        echo 50;

    } else {
        echo 500500;
    }

} else {

    header('Location: index');
    exit;
}

//    Expert Manage Lead Update Part Ends