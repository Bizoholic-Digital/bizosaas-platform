<?php

//Get All Sub Categories
function getAllSubCategories()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "sub_categories ORDER BY sub_category_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Sub Category with given Category Id
function getCategorySubCategories($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "sub_categories where category_id='".$arg."' ORDER BY sub_category_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Category using category id
function getSubCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "sub_categories where sub_category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Sub Category using category name
function getNameSubCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "sub_categories where sub_category_name='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Sub Category using category slug
function getSlugSubCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "sub_categories where sub_category_slug='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Sub Category Count using Category Id
function getCountSubCategoryCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "sub_categories WHERE category_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

