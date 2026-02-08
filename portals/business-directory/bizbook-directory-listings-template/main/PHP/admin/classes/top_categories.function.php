<?php

//Get All Top Categories
function getAllTopCategories()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "top_categories ORDER BY category_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Top Category with given category Id
function getTopCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "top_categories where category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}


