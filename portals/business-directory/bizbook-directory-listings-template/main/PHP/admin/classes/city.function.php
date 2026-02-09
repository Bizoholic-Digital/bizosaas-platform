<?php

//Get All Cities
function getAllCities()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "cities GROUP BY city_name ORDER BY city_id  DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All city with given city Id
function getCity($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "cities where city_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All City Count
function getCountCity()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "cities ORDER BY city_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}