<?php

//Get All Transactions
function getAllTransaction()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "transactions  ORDER BY transaction_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Transactions with given User Id
function getAllUserTransaction($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "transactions  WHERE user_id = '$arg' ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get Transaction with given Transaction Code
function getTransaction($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "transactions  WHERE transaction_code = '$arg' ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get Transaction with given Transaction Code
function getIdTransaction($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "transactions  WHERE transaction_id = '$arg' ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Sum of transactions
function getSumTransaction()
{
    global $conn;

    $sql = "SELECT SUM(transaction_amount) as total FROM  " . TBL . "transactions";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Count of users for last 30 days
function getSumTransactionlast30days()
{
    global $conn;

    $sql = "SELECT SUM(transaction_amount) AS total FROM " . TBL . "transactions WHERE transaction_cdt BETWEEN NOW() - INTERVAL 30 DAY AND NOW()";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get Count of Transaction following with given count days
function getAllSumTransactionLast($arg)
{
    global $conn;

    $sql = "SELECT DATE_FORMAT(transaction_cdt, '%d/%m/%Y') AS Dates, SUM(transaction_amount) as count FROM " . TBL . "transactions
    WHERE transaction_cdt BETWEEN NOW() - INTERVAL $arg DAY AND NOW() GROUP BY Dates ORDER BY transaction_cdt DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}