<?php

//Get All Skill
function getAllJobSkill()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_skill ORDER BY category_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Skill order by position Id
function getAllJobSkillPos()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_skill ORDER BY category_filter_pos_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Active Skill order by position Id
function getAllActiveJobSkillPos()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_skill WHERE category_filter = 0 ORDER BY category_filter_pos_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Skill using category id
function getJobSkill($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "job_skill where category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Skill using category name
function getNameJobSkill($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "job_skill where category_name='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Skill using category name
function getSlugJobSkill($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "job_skill where category_slug='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Skill Name using category id
function getJobSkillName($arg)
{
    global $conn;

    $sql = "SELECT category_name FROM  " . TBL . "job_skill where category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row[0];

}

//Get particular Skill Name using category id
function getJobSkillSlug($arg)
{
    global $conn;

    $sql = "SELECT category_slug FROM  " . TBL . "job_skill where category_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row[0];

}

//Get All Skill Count
function getCountJobSkill()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "job_skill ORDER BY category_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}