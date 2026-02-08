<?php

//Get All News Trending
function getAllNewsTrending()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news_trending ORDER BY trending_news_pos_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Trending News with given news Id
function getNewsTrending($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "news_trending where trending_news_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}


