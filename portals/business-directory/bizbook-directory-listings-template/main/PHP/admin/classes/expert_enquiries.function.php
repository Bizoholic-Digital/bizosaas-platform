<?php

//Get All Enquiry
function getAllExpertEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE is_general_id = 0 ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All General Enquiry
function getAllExpertGeneralEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE is_general_id = 1 ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Today Leads Enquiry
function getAllTodayExpertEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE DATE(enquiry_cdt) = CURDATE() AND is_general_id = 0 ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Finished Leads Enquiry
function getAllFinishedExpertEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE enquiry_status = 500 AND is_general_id = 0 ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Pending Leads Enquiry
function getAllPendingExpertEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE enquiry_status IN (400,300) AND is_general_id = 0 ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Cancel Leads Enquiry
function getAllCancelExpertEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE enquiry_status = 100 AND is_general_id = 0 ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Reported Leads Enquiry
function getAllReportedExpertEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE enquiry_status = 600 AND is_general_id = 0 ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Saved Enquiry
function getAllSavedExpertEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE payment_status='Pending' AND is_general_id = 0 AND enquiry_save = 1 OR payment_status=' ' ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Enquiry with given Enquiry Id
function getExpertEnquiries($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE enquiry_id = $arg  AND is_general_id = 0 AND payment_status='Pending' OR payment_status=' ' ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Enquiry with given user Id
function getUserExpertEnquiries($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE expert_user_id='" . $arg . "' AND is_general_id = 0 AND payment_status='Pending' OR payment_status=' ' ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Enquiry with given user Id
function getSenderUserExpertEnquiries($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE enquiry_sender_id='" . $arg . "' AND is_general_id = 0 AND payment_status='Pending' OR payment_status=' ' ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Enquiry Count
function getCountExpertEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE is_general_id = 0 ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Received Expert Enquiries Count using User Id
function getCountUserExpertEnquiries($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_enquiries  WHERE expert_user_id= '$arg' AND is_general_id = 0 ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Last Week Received Expert Enquiries Count using User Id
function getLastWeekCountUserExpertEnquiries($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_enquiries  WHERE expert_user_id= '$arg' AND is_general_id = 0 AND enquiry_cdt >= DATE(NOW()) - INTERVAL 7 DAY";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}


//Get All Enquiry
function getAllCountExpertEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE payment_status='Pending' OR payment_status=' ' AND is_general_id = 0 ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All General Enquiry
function getAllCountExpertGeneralEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE is_general_id = 1 ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}
//Get All Today Leads Enquiry
function getCountTodayExpertEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE date(enquiry_cdt) = CURDATE() AND is_general_id = 0 ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Finished Leads Enquiry
function getAllCountFinishedExpertEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE enquiry_status = 500 AND is_general_id = 0 ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Pending Leads Enquiry
function getAllCountPendingExpertEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE enquiry_status IN (400,300) AND is_general_id = 0 ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Cancel Leads Enquiry
function getAllCountCancelExpertEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE enquiry_status = 100 AND is_general_id = 0 ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Reported Leads Enquiry
function getAllCountReportedExpertEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE enquiry_status = 600 AND is_general_id = 0 ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Finished Leads Enquiry
function getIdCountFinishedExpertEnquiries($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE enquiry_status = 500 AND is_general_id = 0 AND expert_id= '$arg' ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Finished Leads for given category id Enquiry
function getCategoryCountFinishedExpertEnquiries($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries WHERE enquiry_status = 500 AND is_general_id = 0 AND enquiry_category= '$arg' ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Enquiry with given user Id and date
function getAllUserExpertDateExpertEnquiries($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries where expert_user_id='" . $arg . "' AND enquiry_cdt > '$arg1' AND payment_status='Pending' OR payment_status=' ' ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Enquiry with given user Id and date
function getCountAllUserExpertDateExpertEnquiries($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_enquiries where expert_user_id='" . $arg . "' AND enquiry_cdt > '$arg1' AND payment_status='Pending' OR payment_status=' '  ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}