<?php

//Get All Categories
function getAllPlaceCategories()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "place_categories ORDER BY category_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Categories order by position Id
function getAllPlaceCategoriesPos()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "place_categories ORDER BY category_filter_pos_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Active Categories order by position Id
function getAllActivePlaceCategoriesPos()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "place_categories WHERE category_filter = 0 ORDER BY category_filter_pos_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Category using category id
function getPlaceCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "place_categories where category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Category using category name
function getNamePlaceCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "place_categories where category_name='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Category using category name
function getSlugPlaceCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "place_categories where category_slug='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Category Name using category id
function getPlaceCategoryName($arg)
{
    global $conn;

    $sql = "SELECT category_name FROM  " . TBL . "place_categories where category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row[0];

}

//Get particular Category Name using category id
function getPlaceCategorySlug($arg)
{
    global $conn;

    $sql = "SELECT category_slug FROM  " . TBL . "place_categories where category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row[0];

}

//Get All Category Count
function getCountPlaceCategory()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "place_categories ORDER BY category_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Sub Category Count using Category Id
function getCountCategoryPlaceCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "place_categories WHERE category_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}