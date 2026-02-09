<?php

//Get All Expert Cities
function getAllExpertCities()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_cities ORDER BY country_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Expert Cities with given city Id
function getExpertCity($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_cities where country_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Expert Cities Count
function getCountExpertCity()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_cities ORDER BY country_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

