<?php

//Get All News Subscribers
function getAllNewsSubscribers()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news_subscribers ORDER BY news_subscribers_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get News Subscriber with given news Id
function getNewsSubscribers($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "news_subscribers where news_subscribers_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}