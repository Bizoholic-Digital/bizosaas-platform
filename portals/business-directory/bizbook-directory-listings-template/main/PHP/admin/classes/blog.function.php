<?php

//Get All Blogs
function getAllBlogs()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "blogs ORDER BY blog_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Blogs
function getAllActiveBlogs()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "blogs WHERE blog_status = 'Active' ORDER BY blog_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Blogs with given User ID

function getAllUserBlogs($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "blogs WHERE user_id= '$arg' ORDER BY blog_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Blog using blog id
function getBlog($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "blogs where blog_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Blog using blog Slug
function getSlugBlog($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "blogs where blog_slug='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Blogs except given event id
function getExceptBlog($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "blogs WHERE blog_status= 'Active' AND blog_id !='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Top view Active Premium Blogs
function getAllTopViewsPremiumActiveBlogs()
{
    global $conn;

    $sql = "SELECT *, COUNT(*) FROM " . TBL . "blogs AS t1 LEFT JOIN " . TBL . "users AS t4 ON t1.user_id = t4.user_id INNER JOIN `" . TBL . "page_views` AS t2  ON t1.blog_id = t2.blog_id WHERE t1.blog_status = 'Active' AND t4.user_plan != 1 AND t4.user_plan != 2 GROUP BY t1.blog_id ORDER BY COUNT(*) DESC, t4.user_plan DESC LIMIT 2";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Blog Count using User Id
function getCountUserBlog($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "blogs  WHERE user_id= '$arg' ORDER BY blog_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Blogs Count
function getCountBlog()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "blogs ORDER BY blog_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get particular Listing SEO Score using listing id
function getBlogSeoScore($arg)
{
    global $conn;

    $sql = "select ( case seo_title when '' then 0 else 1 end +
        case seo_description when '' then 0 else 1 end +
        case seo_keywords when '' then 0 else 1 end ) 
        * 100 / 3 as complete FROM " . TBL . "blogs WHERE blog_id = $arg";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row[0];
}
