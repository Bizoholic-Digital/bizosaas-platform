<?php

//Get All Expert Payments
function getAllExpertPayments()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_payments ORDER BY payment_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Expert Payments with given Id
function getExpertPayments($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_payments where payment_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Expert Payments Count
function getCountExpertPayments()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_payments ORDER BY payment_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}