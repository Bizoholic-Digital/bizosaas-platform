<?php

//Get All News
function getAllNews()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news ORDER BY news_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Trash Deleted News
function getAllTrashNews()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news ORDER BY news_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular News Using News Code
function getNews($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "news WHERE news_code='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular News Using News Slug
function getSlugNews($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "news WHERE news_slug='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular News Using News Code
function getIdNews($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "news WHERE news_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All News with given User Id
function getAllNewsUser($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news  WHERE user_id= '$arg' ORDER BY news_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All News with given Category Id
function getAllNewsCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news  WHERE category_id= '$arg' ORDER BY news_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All News with given Category Id and News ID
function getAllNewsCategoryExceptNewsId($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news  WHERE category_id= '$arg' AND news_id !='" . $arg1 . "' ORDER BY news_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All News with given User Id and News Id
function getAllNewsUserNews($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news  WHERE user_id= '$arg' AND news_id = '$arg1'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All News with given User Id and News Id
function getAllNewsNews($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news  WHERE news_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All News Count
function getCountNews()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news ORDER BY news_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//News Count using User Id
function getCountUserNews($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news  WHERE user_id= '$arg' ORDER BY news_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//News Count using Category Id
function getCountCategoryNews($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news WHERE category_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//News Count using Country Id
function getCountCountryNews($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news WHERE country_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//News Count using City Id
function getCountCityNews($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news WHERE city_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//News Count using Category Id
function getCountSubCategoryNews($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "news WHERE sub_category_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All News except given event id
function getExceptNews($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "news WHERE news_status= 'Active' AND news_id !='" . $arg . "' ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Most viewed News limit 10
function getAllTopViewsPremiumActiveNews()
{
    global $conn;

    $sql = "SELECT t1.*, COUNT(*) AS total_count FROM " . TBL . "news AS t1 INNER JOIN `" . TBL . "page_views` AS t2  ON t1.news_id = t2.news_id WHERE t1.news_status= 'Active' GROUP BY t1.news_id ORDER BY COUNT(*) DESC LIMIT 10";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular News SEO Score using News id
function getNewsseoScore($arg)
{
    global $conn;

    $sql = "select ( case seo_title when '' then 0 else 1 end +
        case seo_description when '' then 0 else 1 end +
        case seo_keywords when '' then 0 else 1 end ) 
        * 100 / 3 as complete FROM " . TBL . "news WHERE news_id = $arg";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row[0];
}
?>