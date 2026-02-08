<?php

//Get All Top Service Providers
function getAllTopServiceProviders()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "top_service_providers ORDER BY top_service_provider_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}


//Get All Top Service Providers with given category Id
function getCategoryTopServiceProviders($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "top_service_providers where top_service_provider_category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}