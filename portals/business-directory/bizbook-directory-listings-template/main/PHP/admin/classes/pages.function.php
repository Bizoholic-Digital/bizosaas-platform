<?php

//Get All Pages
function getAllPages()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "pages ORDER BY page_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Pages with page type
function getAllPagesType($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "pages where page_type = '" . $arg . "' ORDER BY page_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get Pages with given Pages Id
function getPage($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "pages where page_id = '" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Active Users Company using user ID
function getActivePageSlug($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "pages where page_slug='" . $arg1 . "' AND page_type='" . $arg . "' AND page_status = 'Publish'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Active Users Company using user ID
function getActivePageSlugwithoutStatus($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "pages where page_slug='" . $arg1 . "' AND page_type='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}