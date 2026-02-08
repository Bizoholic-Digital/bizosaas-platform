<?php

//Get All News Social Media
function getAllNewsSocialMedia()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news_social_media ORDER BY social_media_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All News Social Media Active
function getAllNewsSocialMediaActive()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news_social_media WHERE social_media_status = 1 ORDER BY social_media_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Social Media News with given news Id
function getNewsSocialMedia($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "news_social_media where social_media_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All News Social Media Active
function getCountNewsSocialMediaActive()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news_social_media WHERE social_media_status = 1 ORDER BY social_media_id ASC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}
