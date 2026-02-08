<?php

//Get All JobProfile
function getAllJobProfile()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_profile ORDER BY job_profile_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}


//Get All job_profile with given job_profile Id
function getJobProfile($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "job_profile where job_profile_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All job_profile with given job_profile Id
function getJobProfileCode($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "job_profile where job_profile_code='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get job profile with given job profile slug
function getJobProfileSlug($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "job_profile where job_profile_slug = '". $arg ."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All job_profile with given job_profile Id
function getUserJobProfile($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "job_profile where user_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Job Limit
function getAllCategoryJobProfileLimit($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_profile WHERE category_id= '$arg' AND job_profile_id !='" . $arg1 . "' ORDER BY job_id DESC LIMIT 5";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All JobProfile Count
function getCountJobProfile()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_profile ORDER BY job_profile_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}