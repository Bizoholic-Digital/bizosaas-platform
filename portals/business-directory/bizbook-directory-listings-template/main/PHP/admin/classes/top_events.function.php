<?php

//Get All Top Events
function getAllTopEvents()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "top_events ORDER BY event_pos_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Top Events
function getAllTopEventsLimit($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "top_events WHERE event_id >= $arg ORDER BY event_pos_id ASC LIMIT $arg1";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Top Event with given event Id
function getTopEvent($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "top_events where event_id='".$arg."'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}