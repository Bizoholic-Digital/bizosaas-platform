<?php

//Get All Jobs
function getAllJob()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "jobs ORDER BY job_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Job Limit
function getAllJobLimit($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "jobs ORDER BY job_id DESC LIMIT $arg ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Job Limit
function getAllCategoryJobLimit($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "jobs WHERE category_id= '$arg' AND job_id !='" . $arg1 . "' ORDER BY job_id DESC LIMIT 10";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Job Limit 5
function getAllCategoryJobLimit5($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "jobs WHERE category_id= '$arg' ORDER BY job_id DESC LIMIT 5";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Job Group By City
function getAllJobGroupByCity()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "jobs GROUP BY job_location";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Job Using Job Code
function getJob($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "jobs WHERE job_code='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Job Using Job Slug
function getSlugJob($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "jobs WHERE job_slug='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Job Using Job Code
function getIdJob($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "jobs WHERE job_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Job with given User Id
function getAllJobUser($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "jobs  WHERE user_id= '$arg' ORDER BY job_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Job with given Category Id
function getAllJobCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "jobs  WHERE category_id= '$arg' ORDER BY job_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Job with given User Id and Job Id
function getAllJobUserJob($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "jobs  WHERE user_id= '$arg' AND job_id = '$arg1'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Job with given User Id and Job Id
function getAllJobJob($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "jobs  WHERE job_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Job Count
function getCountJob()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "jobs ORDER BY job_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Job Count
function getCountJobCompanyName()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "jobs GROUP BY job_company_name";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Job Count using User Id
function getCountUserJob($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "jobs  WHERE user_id= '$arg' ORDER BY job_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Job Count using Category Id
function getCountCategoryJob($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "jobs WHERE category_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Job Count using Category Id
function getCountSubCategoryJob($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "jobs WHERE sub_category_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Jobs except given event id
function getExceptJob($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "jobs WHERE job_status= 'Active' AND job_id !='" . $arg . "' LIMIT 3";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Job SEO Score using job id
function getJobSeoScore($arg)
{
    global $conn;

    $sql = "select ( case seo_title when '' then 0 else 1 end +
        case seo_description when '' then 0 else 1 end +
        case seo_keywords when '' then 0 else 1 end ) 
        * 100 / 3 as complete FROM " . TBL . "jobs WHERE job_id = $arg";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row[0];
}
?>