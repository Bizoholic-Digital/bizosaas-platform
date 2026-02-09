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
//    Enquiry Update Part Starts

    $expert_id = $_POST["expert_id"];
    $expert_service_user_id = $_POST["expert_service_user_id"];
    $enquiry_id = $_POST["enquiry_id"];

    $cancel_reason = addslashes($_POST["cancel_message"]);

    $payment_status = "Pending";

    /*
     Closed = 100
     New = 200
     On the way = 300
     Pending = 400
     Done = 500  */

    $enquiry_status = 100;

    $enquiry_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "expert_enquiries WHERE enquiry_id = '$enquiry_id'");

    if (mysqli_num_rows($enquiry_fetch) > 0) {

        $enquiry_fetch_row = mysqli_fetch_array($enquiry_fetch);

        if ($enquiry_fetch_row['enquiry_sender_id'] != $expert_service_user_id) {

            echo 403403;  // Enquiried User Id and Current User Id is not Same
            exit();
        }


        $enquiry_res = mysqli_query($conn, "UPDATE  " . TBL . "expert_enquiries SET  enquiry_status='" . $enquiry_status . "'
     ,cancel_reason ='" . $cancel_reason . "'
     where enquiry_id='" . $enquiry_id . "'");

        if ($enquiry_res) {

            echo 50;


        } else {
            echo 500500;
        }
    } else {
        echo 500500;
    }
} else {

    header('Location: index');
    exit;
}

//    Enquiry Update Part Ends