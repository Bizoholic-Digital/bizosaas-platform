<?php

//Get All Categories
function getAllNewsCategories()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news_categories ORDER BY category_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Categories order by position Id
function getAllNewsCategoriesPos()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news_categories ORDER BY category_filter_pos_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Active Categories order by position Id
function getAllActiveNewsCategoriesPos()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news_categories WHERE category_filter = 0 ORDER BY category_filter_pos_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Category using category id
function getNewsCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "news_categories where category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Category using category name
function getNameNewsCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "news_categories where category_name='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Category using category name
function getSlugNewsCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "news_categories where category_slug='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Category Name using category id
function getNewsCategoryName($arg)
{
    global $conn;

    $sql = "SELECT category_name FROM  " . TBL . "news_categories where category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row[0];

}

//Get particular Category Name using category id
function getNewsCategorySlug($arg)
{
    global $conn;

    $sql = "SELECT category_slug FROM  " . TBL . "news_categories where category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row[0];

}

//Get All Category Count
function getCountNewsCategory()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news_categories ORDER BY category_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Sub Category Count using Category Id
function getCountCategoryNewsCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news_categories WHERE category_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}