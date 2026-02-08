<?php

//Get All Events
function getAllEvents()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "events  WHERE event_type= 'All' ORDER BY event_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Active Events
function getAllActiveEvents()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "events WHERE event_status= 'Active' ORDER BY event_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Events with User Id

function getAllUserEvents($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "events  WHERE event_type= 'All' AND  user_id= '$arg' ORDER BY event_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}


//Get particular Event using event id
function getEvent($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "events where event_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get particular Event using event id
function getSlugEvent($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "events where event_slug='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

//Get All Events except given event id
function getExceptEvent($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "events WHERE event_status= 'Active' AND event_id !='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Active Events
function getAllTopViewsPremiumActiveEvents()
{
    global $conn;

    $sql = "SELECT *, COUNT(*) FROM " . TBL . "events AS t1 LEFT JOIN " . TBL . "users AS t4 ON t1.user_id = t4.user_id INNER JOIN `" . TBL . "page_views` AS t2  ON t1.event_id = t2.event_id WHERE t1.event_status= 'Active' AND t4.user_plan != 1 AND t4.user_plan != 2 GROUP BY t1.event_id ORDER BY COUNT(*) DESC, t4.user_plan DESC LIMIT 2";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Events Count
function getCountEvent()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "events ORDER BY event_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Event Count using User Id
function getCountUserEvent($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "events  WHERE event_type= 'All' AND  user_id= '$arg' ORDER BY event_id DESC";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get particular Event SEO Score using event id
function getEventSeoScore($arg)
{
    global $conn;

    $sql = "select ( case seo_title when '' then 0 else 1 end +
        case seo_description when '' then 0 else 1 end +
        case seo_keywords when '' then 0 else 1 end ) 
        * 100 / 3 as complete FROM " . TBL . "events WHERE event_id = $arg";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row[0];
}

?>
