<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

//    Enquiry Update Part Starts


    $enquiry_sender_id = $_POST["enquiry_sender_id"];

    $is_general_id = 0; //General Enquiry Lead

    $enquiry_id = $_POST["enquiry_id"];
    $expert_id = $_POST["expert_id"];

    /*
     Closed = 100
     New = 200
     On the way = 300
     Pending = 400
     Done = 500  */

    $enquiry_status = 200;

    $expert_details = mysqli_query($conn, "SELECT * FROM  " . TBL . "experts where expert_id='" . $expert_id . "'");
    $expert_details_row = mysqli_fetch_array($expert_details);

    $expert_user_id = $expert_details_row['user_id'];  // Expert User Id


        if ($expert_user_id == $enquiry_sender_id) {

            echo 403403;  // Enquiring User Id and Owner Id is Same
            exit();
        }



    $enquiry_res = mysqli_query($conn, "UPDATE  " . TBL . "expert_enquiries SET expert_id='" . $expert_id . "'
    , expert_user_id='" . $expert_user_id . "', is_general_id='" . $is_general_id . "'
     where enquiry_id='" . $enquiry_id . "'");


    if ($enquiry_res) {

        echo $EnquiryID;


    } else {
        echo 500500;
    }
} else {

    header('Location: profile');
    exit;
}

//    Enquiry Update Part Ends