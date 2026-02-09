<?php

//Get All Users Company with Active status
function getAllUserCompany()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "user_company WHERE company_status = 'Active' ORDER BY user_company_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Users Company with Inactive status
function getAllInactiveUserCompany()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "user_company WHERE company_status = 'Inactive' ORDER BY user_company_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Users Company using user ID
function getUserCompany($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "user_company where user_company_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Users Company using user ID
function getUserCompanyUser($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "user_company where user_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Active Users Company using user ID
function getActiveUserCompany($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "user_company where company_slug='" . $arg . "' AND company_status = 'Active'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Count of Users Company
function getCountUserCompany()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "user_company ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get particular Users Company using user ID
function getCountUserCompanyUser($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "user_company where user_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}


?>