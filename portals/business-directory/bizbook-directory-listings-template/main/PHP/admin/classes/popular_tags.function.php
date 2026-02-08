<?php

//Get All Popular Tags
function getAllPopularTags()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "popular_tags ORDER BY popular_tags_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get Popular Tags with given Tag Id
function getPopularTags($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "popular_tags where popular_tags_id = '" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}