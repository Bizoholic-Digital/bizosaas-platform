<?php

//Get All Enquiry
function getAllEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "enquiries where payment_status='Pending' OR payment_status=' ' ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Enquiry
function getAllSavedEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "enquiries where payment_status='Pending' AND enquiry_save = 1 OR payment_status=' ' ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Enquiry with given user Id
function getUserEnquiries($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "enquiries where listing_user_id='" . $arg . "' AND payment_status='Pending' OR payment_status=' ' ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Enquiry Count
function getCountEnquiries()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "enquiries ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Count of users for last 30 days
function getCountEnquirieslast30days()
{
    global $conn;

    $sql = "SELECT  * FROM " . TBL . "enquiries WHERE enquiry_cdt BETWEEN NOW() - INTERVAL 30 DAY AND NOW()";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Received Enquiries Count using User Id
function getCountUserEnquiries($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "enquiries  WHERE listing_user_id= '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Last Week Received Enquiries Count using User Id
function getLastWeekCountUserEnquiries($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "enquiries  WHERE listing_user_id= '$arg' AND enquiry_cdt >= DATE(NOW()) - INTERVAL 7 DAY";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get Count of Enquiries following with given count days
function getAllCountEnquiriesLast($arg)
{
    global $conn;

    $sql = "SELECT DATE_FORMAT(enquiry_cdt, '%d/%m/%Y') AS Dates, count(*) as count FROM " . TBL . "enquiries
    WHERE enquiry_cdt BETWEEN NOW() - INTERVAL $arg DAY AND NOW() GROUP BY Dates ORDER BY enquiry_cdt DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Enquiry with given user Id and date
function getAllUserListingDateEnquiries($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "enquiries where listing_user_id='" . $arg . "' AND listing_id != 0 AND enquiry_cdt > '$arg1' AND payment_status='Pending' OR payment_status=' ' ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Enquiry with given user Id and date
function getAllUserEventDateEnquiries($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "enquiries where listing_user_id='" . $arg . "' AND event_id != 0 AND enquiry_cdt > '$arg1' AND payment_status='Pending' OR payment_status=' ' ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Enquiry with given user Id and date
function getAllUserBlogDateEnquiries($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "enquiries where listing_user_id='" . $arg . "' AND blog_id != 0 AND enquiry_cdt > '$arg1' AND payment_status='Pending' OR payment_status=' ' ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Enquiry with given user Id and date
function getAllUserProductDateEnquiries($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "enquiries where listing_user_id='" . $arg . "' AND product_id != 0 AND enquiry_cdt > '$arg1' AND payment_status='Pending' OR payment_status=' ' ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}


//Get All Enquiry with given user Id and date
function getCountAllUserListingDateEnquiries($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "enquiries where listing_user_id='" . $arg . "' AND listing_id != 0 AND enquiry_cdt > '$arg1' AND payment_status='Pending' OR payment_status=' 'ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Enquiry with given user Id and date
function getCountAllUserEventDateEnquiries($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "enquiries where listing_user_id='" . $arg . "' AND event_id != 0 AND enquiry_cdt > '$arg1' AND payment_status='Pending' OR payment_status=' ' ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Enquiry with given user Id and date
function getCountAllUserBlogDateEnquiries($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "enquiries where listing_user_id='" . $arg . "' AND blog_id != 0 AND enquiry_cdt > '$arg1' AND payment_status='Pending' OR payment_status=' '  ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Enquiry with given user Id and date
function getCountAllUserProductDateEnquiries($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "enquiries where listing_user_id='" . $arg . "' AND product_id != 0 AND enquiry_cdt > '$arg1' AND payment_status='Pending' OR payment_status=' '  ORDER BY enquiry_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}