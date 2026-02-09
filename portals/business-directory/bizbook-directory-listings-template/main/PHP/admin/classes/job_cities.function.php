<?php

//Get All Job Cities
function getAllJobCities()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_cities ORDER BY city_name ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Job Cities
function getAllJobCitiesOrderId()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_cities ORDER BY city_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All job city with given city Id
function getJobCity($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "job_cities where city_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Job City Count
function getCountJobCity()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_cities ORDER BY city_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}