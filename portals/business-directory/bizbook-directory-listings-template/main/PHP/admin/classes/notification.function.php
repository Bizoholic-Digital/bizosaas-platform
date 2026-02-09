<?php

//Get All Notification
function getAllNotification()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "notifications  ORDER BY notification_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get Notification with given notification Id
function getNotification($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "notifications where notification_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Notification with given notification user
function getAllUserNotification($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "notifications where notification_user in ($arg, $arg1,100) ORDER BY notification_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Notification with given notification user
function getAllUserNewNotification($arg,$arg1,$arg2)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "notifications where notification_user in ($arg, $arg1,100) AND notification_cdt > '$arg2' ORDER BY notification_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Notification Count
function getCountNotification()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "notifications ORDER BY notification_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Notification with given notification user
function getCountAllUserNewNotification($arg,$arg1,$arg2)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "notifications where notification_user in ($arg, $arg1,100) AND notification_cdt > '$arg2' ORDER BY notification_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}