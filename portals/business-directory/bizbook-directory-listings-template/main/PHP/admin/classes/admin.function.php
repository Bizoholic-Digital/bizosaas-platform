<?php

//Get All Super Admin
function getAllSuperAdmin()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "admin WHERE admin_type = 'Super Admin'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Sub Admins
function getAllSubAdmin()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "admin WHERE admin_type = 'Sub Admin' ORDER BY admin_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular admin using admin id
function getAdmin($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "admin where admin_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}