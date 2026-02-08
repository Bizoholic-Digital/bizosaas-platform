<?php

//Get All Products
function getAllProduct()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "products ORDER BY product_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Trash Deleted Products
function getAllTrashProduct()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "products ORDER BY product_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Product Using Product Code
function getProduct($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "products WHERE product_code='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Product Using Product Slug
function getSlugProduct($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "products WHERE product_slug='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Product Using Product Code
function getIdProduct($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "products WHERE product_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Product with given User Id
function getAllProductUser($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "products  WHERE user_id= '$arg' ORDER BY product_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Product with given Category Id
function getAllProductCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "products  WHERE category_id= '$arg' ORDER BY product_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Product with given User Id and Product Id
function getAllProductUserProduct($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "products  WHERE user_id= '$arg' AND product_id = '$arg1'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Product with given User Id and Product Id
function getAllProductProduct($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "products  WHERE product_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Product Count
function getCountProduct()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "products ORDER BY product_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Product Count using User Id
function getCountUserProduct($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "products  WHERE user_id= '$arg' ORDER BY product_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Product Count using Category Id
function getCountCategoryProduct($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "products WHERE category_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Product Count using Country Id
function getCountCountryProduct($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "products WHERE country_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Product Count using City Id
function getCountCityProduct($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "products WHERE city_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Product Count using Category Id
function getCountSubCategoryProduct($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "products WHERE sub_category_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Products except given event id
function getExceptProduct($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "products WHERE product_status= 'Active' AND product_id !='" . $arg . "' LIMIT 3";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Product SEO Score using product id
function getProductSeoScore($arg)
{
    global $conn;

    $sql = "select ( case seo_title when '' then 0 else 1 end +
        case seo_description when '' then 0 else 1 end +
        case seo_keywords when '' then 0 else 1 end ) 
        * 100 / 3 as complete FROM " . TBL . "products WHERE product_id = $arg";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row[0];
}
?>