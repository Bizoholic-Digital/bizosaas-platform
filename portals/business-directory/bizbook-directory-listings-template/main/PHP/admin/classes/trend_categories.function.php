<?php

//Get All Trend Categories
function getAllTrendCategories()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "trend_categories ORDER BY category_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Trend Category with given category Id
function getTrendCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "trend_categories where category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}


