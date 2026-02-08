<?php

//Get All Experts
function getAllExperts()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "experts ORDER BY expert_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Top Experts
function getAllTopExperts()
{
    global $conn;

    $sql = "SELECT T1.*, T2.enquiry_id, T2.enquiry_status, COUNT(T2.enquiry_id) as top  FROM " . TBL . "experts AS T1 LEFT JOIN " . TBL . "expert_enquiries AS T2 ON T1.expert_id = T2.expert_id WHERE T2.enquiry_status = 500 ORDER BY top DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Experts Limit
function getAllExpertsLimit($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "experts ORDER BY expert_id DESC LIMIT $arg ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Experts Limit
function getAllCategoryExpertsLimit($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "experts WHERE category_id= '$arg' AND expert_id !='" . $arg1 . "' ORDER BY expert_id DESC LIMIT 10";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Experts Limit 5
function getAllCategoryExpertsLimit5($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "experts WHERE category_id= '$arg' ORDER BY expert_id DESC LIMIT 5";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Experts Group By City
function getAllExpertsGroupByCity()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "experts GROUP BY city_id";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Experts Using Experts Code
function getExpert($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "experts WHERE expert_code='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Experts Using Experts Slug
function getSlugExpert($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "experts WHERE expert_slug='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Experts Using Experts Code
function getIdExpert($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "experts WHERE expert_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Experts with given User Id
function getExpertUser($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "experts  WHERE user_id= '$arg' ORDER BY expert_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Experts with given Category Id
function getAllExpertCategory($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "experts  WHERE category_id= '$arg' ORDER BY expert_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Experts with given User Id and Experts Id
function getAllExpertUserExperts($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "experts  WHERE user_id= '$arg' AND expert_id = '$arg1'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Experts Count
function getCountAllExperts()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "experts ORDER BY expert_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Top Experts Count
function getCountAllTopExperts()
{
    global $conn;

    //"SELECT T1.*, T2.* FROM " . TBL . "experts AS T1 LEFT JOIN " . TBL . "expert_enquiries AS T2 ON T1.expert_id = T2.expert_id WHERE T2. ORDER BY expert_id DESC";
    $sql = "SELECT T1.*, T2.enquiry_id, T2.enquiry_status, COUNT(T2.enquiry_id) as top  FROM " . TBL . "experts AS T1 LEFT JOIN " . TBL . "expert_enquiries AS T2 ON T1.expert_id = T2.expert_id WHERE T2.enquiry_status = 500 ORDER BY top DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Experts Count using User Id
function getCountUserExperts($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "experts WHERE user_id= '$arg' ORDER BY expert_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Experts Count using Category Id
function getCountCategoryExperts($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "experts WHERE category_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Experts Count using Category Id
function getCountSubCategoryExperts($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "experts WHERE sub_category_id = '$arg'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Experts except given event id
function getExceptExperts($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "experts WHERE expert_status= 'Active' AND expert_id !='" . $arg . "' LIMIT 3";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Experts with given Category Id and Expert Id
function getExceptExpertsCategoryExpert($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "experts WHERE category_id= '$arg' AND expert_id != '$arg1' ORDER BY expert_id DESC LIMIT 3";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Experts SEO Score using job id
function getExpertsSeoScore($arg)
{
    global $conn;

    $sql = "select ( case seo_title when '' then 0 else 1 end +
        case seo_description when '' then 0 else 1 end +
        case seo_keywords when '' then 0 else 1 end ) 
        * 100 / 3 as complete FROM " . TBL . "experts WHERE expert_id = $arg";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row[0];
}
?>