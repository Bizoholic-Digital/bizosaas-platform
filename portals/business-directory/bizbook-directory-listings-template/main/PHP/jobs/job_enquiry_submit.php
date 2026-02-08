<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('job-config-info.php')) {
    include "job-config-info.php";
}

if ($_SERVER['REQUEST_METHOD']=='POST') {
//    Enquiry Insert Part Starts

    $job_id= $_POST["job_id"];
    $job_user_id = $_POST["job_user_id"];
    $enquiry_sender_id = $_POST["enquiry_sender_id"];

    $enquiry_name = $_POST["enquiry_name"];
    $enquiry_email = $_POST["enquiry_email"];
    $enquiry_mobile = $_POST["enquiry_mobile"];
    $enquiry_source = $_POST["enquiry_source"];

    $job_applied_status = "Active";

    if($job_user_id == $enquiry_sender_id){

        echo '3';  // Enquiring User Id and Owner Id is Same
        exit();
    }

    // To check if applying user has job profile starts

    $job_profile_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "job_profile  WHERE user_id = $enquiry_sender_id ");
    $job_profile_fetchrow = mysqli_fetch_array($job_profile_fetch);

    $job_profile_id = $job_profile_fetchrow['job_profile_id'];

    if($job_profile_id <= 0){

        echo '4';  // No Job profile for applying user
        exit();
    }

    // To check if applying user has job profile ends

    // To check if user already applied for job profile starts

    $same_job_profile_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "job_applied  WHERE job_profile_id = '$enquiry_sender_id' AND job_id = '$job_id' ");

    if(mysqli_num_rows($same_job_profile_fetch) > 0){

        echo '5';  // Already Applied
        exit();
    }

    // To check if user already applied for job profile ends

    $enquiry_qry = "INSERT INTO " . TBL . "job_applied
					(job_id, job_user_id, job_profile_id, job_applied_status, job_applied_cdt)
					VALUES
					('$job_id', '$job_user_id', '$enquiry_sender_id', '$job_applied_status', '$curDate')";

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

//    Enquiry Insert Part Ends