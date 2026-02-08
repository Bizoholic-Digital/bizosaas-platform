<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('places-config-info.php')) {
    include "places-config-info.php";
}

if ($_SERVER['REQUEST_METHOD']=='POST') {
//    Add place request Insert Part Starts

    $place_name = $_POST["place_name"];
    $place_address = $_POST["place_address"];
    $place_request_sender_id = $_POST["enquiry_sender_id"];
    $place_description = addslashes($_POST["place_description"]);

    if($_POST["enquiry_name"] != NULL){

        $enquiry_name = $_POST["enquiry_name"];
    }else {

        $enquiry_name = 'N/A';
    }

    if($_POST["enquiry_email"] != NULL){

        $enquiry_email = $_POST["enquiry_email"];
    }else {

        $enquiry_email = 'N/A';
    }

    if($_POST["enquiry_mobile"] != NULL){

        $enquiry_mobile = $_POST["enquiry_mobile"];
    }else {

        $enquiry_mobile = 0;
    }

    $place_request_status = "Active";



    $enquiry_qry = "INSERT INTO " . TBL . "place_request
					(place_description,enquiry_name, enquiry_email, enquiry_mobile, place_name, place_address, place_request_status, place_request_sender_id, place_request_cdt)
					VALUES
					('$place_description','$enquiry_name', '$enquiry_email', '$enquiry_mobile', '$place_name', '$place_address', '$place_request_status', '$place_request_sender_id', '$curDate')";

    $enquiry_res = mysqli_query($conn,$enquiry_qry);

    $EnquiryID = mysqli_insert_id($conn);


    if ($enquiry_res) {

            echo '1';

    } else {
        echo '2';
    }
}else {

    header('Location: index');
    exit;
}

//    Add place request Insert Part Ends

