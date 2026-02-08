<?php

//Get All News Slider
function getAllNewsSlider()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news_slider ORDER BY news_slider_pos_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Slider News with given news Id
function getNewsSlider($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "news_slider where news_slider_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}