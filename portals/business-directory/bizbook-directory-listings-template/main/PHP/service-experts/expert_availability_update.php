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
//    Expert Availability Update Part Starts

    $expert_id = $_POST["expert_id"];
    $expert_availability_status = $_POST["expert_availability_status"];
    $available_time_start = $_POST["available_time_start"];
    $available_time_end = $_POST["available_time_end"];



        $enquiry_res = mysqli_query($conn, "UPDATE  " . TBL . "experts SET  expert_availability_status='" . $expert_availability_status . "'
     ,available_time_start ='" . $available_time_start . "'
     ,available_time_end ='" . $available_time_end . "'
     ,expert_udt ='$curDate'
     where expert_id='" . $expert_id . "'");

        if ($enquiry_res) {

            echo 50;

        } else {
            echo 500500;
        }

} else {

    header('Location: index');
    exit;
}

//    Expert Availability Update Part Ends