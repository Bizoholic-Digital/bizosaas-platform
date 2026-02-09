<?php

//Get All Security
function getAllSlider()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "slider ORDER BY slider_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Slider with given slider Id
function getSlider($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "slider where slider_id = '" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}