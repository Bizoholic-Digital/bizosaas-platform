<?php

function getAllPlanType()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "plan_type WHERE plan_type_status='Active' ORDER BY plan_type_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

function getPlanType($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "plan_type WHERE plan_type_status='Active' AND plan_type_id = '$arg' ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}



?>