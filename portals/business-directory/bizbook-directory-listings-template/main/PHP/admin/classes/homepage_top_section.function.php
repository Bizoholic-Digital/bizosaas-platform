<?php

//Get All HomePage Top Section

function getAllHomePageTopSection()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "homepage_top_section ORDER BY top_section_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular HomePage Top Section Using Top Section id

function getHomePageTopSection($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "homepage_top_section where top_section_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}