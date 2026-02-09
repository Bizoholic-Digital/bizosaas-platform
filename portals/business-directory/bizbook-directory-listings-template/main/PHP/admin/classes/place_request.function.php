<?php

//Get All Place Request
function getAllPlaceRequest()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "place_request ORDER BY place_request_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Place Request with given place request Id
function getPlaceRequest($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "place_request where place_request_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}