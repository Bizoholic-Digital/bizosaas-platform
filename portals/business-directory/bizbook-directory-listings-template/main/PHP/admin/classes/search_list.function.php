<?php

//Get All search_list
function getAllSearch()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "search_list ORDER BY search_list_position ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Search with page type
function getAllSearchType($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "search_list where page_type = '" . $arg . "' ORDER BY search_list_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get Search with given Search Id
function getSearch($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "search_list where search_list_id = '" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}