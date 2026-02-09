<?php

//Get All Job Applied
function getAllJobApplied()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_applied ORDER BY job_applied_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Job Profile with given job applied Id
function getJobApplied($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "job_applied where job_applied_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Job Profile with given job Id
function getJobAppliedJob($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "job_applied where job_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Job Profile with given job Profile Id
function getJobAppliedJobProfile($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "job_applied where job_profile_id='".$arg."' ORDER BY job_applied_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Job Applied Count
function getCountJobAppliedJob($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_applied where job_id='".$arg."' ORDER BY job_applied_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Job Applied Count
function getCountJobAppliedProfile($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_applied where job_profile_id='".$arg."' ORDER BY job_applied_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Job Applied Count
function getCountJobAppliedProfileJob($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_applied where job_profile_id='".$arg."' AND job_id='".$arg1."' ORDER BY job_applied_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Job Applied Count
function getCountJobApplied()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_applied ORDER BY job_applied_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Job Profile with given job Profile Id
function getUserAppliedDateJobProfile($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "job_applied where job_user_id='".$arg."' AND job_applied_cdt > '$arg1' ORDER BY job_applied_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Job Profile with given job Profile Id
function getCountUserAppliedDateJobProfile($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "job_applied where job_user_id='".$arg."' AND job_applied_cdt > '$arg1' ORDER BY job_applied_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}