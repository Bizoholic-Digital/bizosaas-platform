<?php

//Get All Job Popular
function getAllJobPopular()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_popular ORDER BY job_popular_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Job Popular with given job popular Id
function getJobPopular($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "job_popular where job_popular_id = '".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}