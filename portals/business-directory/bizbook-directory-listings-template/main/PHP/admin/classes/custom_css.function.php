<?php


//Get All Custom CSS Data
function getAllCustomCss()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "custom_css WHERE custom_css_id = 1";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}