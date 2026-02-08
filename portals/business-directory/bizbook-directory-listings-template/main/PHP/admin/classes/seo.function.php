<?php

//Get All SEO
function getAllSeo()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "seo ORDER BY seo_page_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get SEO with given seo Id
function getSeo($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "seo where seo_page_id = '" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}