<?php

//Get All Categories
function getAllExpertCategories()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_categories ORDER BY category_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Categories
function getAllExpertCategoriesOrderByExpertsTable()
{
    global $conn;

    $sql = "SELECT T1.*, COUNT(T2.category_id) AS views FROM " . TBL . "expert_categories AS T1 LEFT JOIN " . TBL . "jobs AS T2 ON T1.category_id = T2.category_id GROUP BY T1.category_id ORDER BY views DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Categories
function getAllExpertCategoriesOrderByExpertsTableLimit($arg)
{
    global $conn;

    $sql = "SELECT T1.*, COUNT(T2.category_id) AS views FROM " . TBL . "expert_categories AS T1 LEFT JOIN " . TBL . "jobs AS T2 ON T1.category_id = T2.category_id GROUP BY T1.category_id ORDER BY views DESC LIMIT $arg";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Categories Limit
function getAllExpertCategoriesLimit($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_categories ORDER BY category_id DESC LIMIT $arg";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Categories order by position Id
function getAllExpertCategoriesPos()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_categories ORDER BY category_filter_pos_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Active Categories order by position Id
function getAllActiveExpertCategoriesPos()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_categories WHERE category_filter = 0 ORDER BY category_filter_pos_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Category using category id
function getExpertCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_categories where category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Categories
function getExceptAllExpertCategories($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_categories  where category_id != '".$arg."' ORDER BY category_id DESC LIMIT 3";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Category using category name
function getNameExpertCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_categories where category_name='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Category using category name
function getSlugExpertCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_categories where category_slug='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Category Name using category id
function getExpertCategoryName($arg)
{
    global $conn;

    $sql = "SELECT category_name FROM  " . TBL . "expert_categories where category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row[0];

}

//Get particular Category Name using category id
function getExpertCategorySlug($arg)
{
    global $conn;

    $sql = "SELECT category_slug FROM  " . TBL . "expert_categories where category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row[0];

}

//Get All Category Count
function getCountExpertCategory()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_categories ORDER BY category_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Sub Category Count using Category Id
function getCountCategoryExpertCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_categories WHERE category_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}