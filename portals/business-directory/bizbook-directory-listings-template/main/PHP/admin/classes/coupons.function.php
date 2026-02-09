<?php

//Get All Coupons
function getAllCoupons()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "coupons ORDER BY coupon_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Active Coupons
function getAllActiveCoupons()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "coupons WHERE coupon_status= 'Active' ORDER BY coupon_id ASC";;
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Coupons with User Id

function getAllUserCoupons($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "coupons  WHERE coupon_user_id= '$arg' ORDER BY coupon_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Coupons with User Id with used members

function getAllUserCouponsUsed($arg)
{
    global $conn;
    
    $sql = "SELECT coupon_name,coupon_user_id,SUBSTRING_INDEX(SUBSTRING_INDEX(t.coupon_use_members, ',', n.n), ',', -1) coupon_use_members
  FROM vv_coupons as t CROSS JOIN 
  (
   SELECT a.N + b.N * 10 + 1 n
     FROM 
    (SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) a
   ,(SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) b
    ORDER BY n 
   ) n
 WHERE n.n <= 1 + (LENGTH(t.coupon_use_members) - LENGTH(REPLACE(t.coupon_use_members, ',', '')))
 AND coupon_user_id= '$arg' AND coupon_use_members is not null ORDER BY coupon_id DESC";

    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get particular Coupons using Coupons id
function getCoupon($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "coupons where coupon_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Coupons with start date is greater than equal to today

function getAllCurrentCoupons()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "coupons  WHERE  coupon_start_date <= CURDATE() ORDER BY coupon_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Coupons except given Coupons id
function getExceptCoupon($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "coupons WHERE coupon_status= 'Active' AND coupon_id !='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Coupons Count
function getCountCoupon()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "coupons ORDER BY coupon_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Coupons Count using User Id
function getCountUserCoupon($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "coupons  WHERE coupon_user_id= '$arg' ORDER BY coupon_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}
