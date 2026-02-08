<?php

//Get All Sub Categories
function getAllJobSubCategories()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_sub_categories ORDER BY sub_category_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Sub Category with given Category Id
function getCategoryJobSubCategories($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_sub_categories where category_id='".$arg."' ORDER BY sub_category_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Category using category id
function getJobSubCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "job_sub_categories where sub_category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Sub Category Count using Category Id
function getCountJobSubCategoryCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_sub_categories WHERE category_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}