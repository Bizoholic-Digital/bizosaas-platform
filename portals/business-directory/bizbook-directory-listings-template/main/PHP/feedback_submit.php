<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD']=='POST') {
//    Feedback Insert Part Starts

    $enquiry_name = $_POST["feedback_name"];
    $enquiry_email = $_POST["feedback_email"];
    $enquiry_mobile = $_POST["feedback_mobile"];
    $enquiry_message = $_POST["feedback_message"];


    $enquiry_qry = "INSERT INTO " . TBL . "messages 
					(sender_name, sender_email, sender_mobile,message,message_cdt) 
					VALUES 
					('$enquiry_name', '$enquiry_email', '$enquiry_mobile','$enquiry_message', '$curDate')";

    $enquiry_res = mysqli_query($conn,$enquiry_qry);

    $EnquiryID = mysqli_insert_id($conn);


    if ($enquiry_res) {
        $_SESSION['status_msg'] = $BIZBOOK['FEEDBACK_INSERT_SUCCESS_MESSAGE'];

        header('Location: feedback');
        exit();

    } else {
        $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

        header('Location: feedback');
        exit();
    }
}else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: feedback');
    exit();
}

//    Enquiry Insert Part Ends