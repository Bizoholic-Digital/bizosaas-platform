<?php

//Get All Expert Areas
function getAllExpertAreas()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_areas ORDER BY city_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Expert Areas with given Area Id
function getExpertArea($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "expert_areas where city_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Expert Areas
function getAllExpertAreaCity($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_areas where state_id ='".$arg."' ORDER BY city_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Expert Areas Count
function getCountExpertArea()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_areas ORDER BY city_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Expert Areas Count
function getCountExpertAreaCity($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "expert_areas where state_id ='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}