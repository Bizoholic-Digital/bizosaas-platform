<?php

//Get All Feedback Templates
function getAllMessages()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "messages ORDER BY message_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get Feedback with given Message Id
function getMessage($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "messages where message_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}