<?php

//Get All Chat Links
function getAllChatLinks()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "chat_links ORDER BY chat_link_cdt DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Chat Links with Chat Link Id
function getChatLink($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "chat_links  WHERE chat_link_id = '$arg' AND chat_link_status= 'Active' ORDER BY chat_link_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Given User Id Chat Links with both receiver and sender id
function getAllGivenIdChatLinks($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "chat_links  WHERE receiver_id = '$arg' OR sender_id = '$arg' AND chat_link_status='Active' ORDER BY chat_link_udt DESC ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Receiver Chat Links with both receiver and sender id
function getAllReceiverChatLinks($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "chat_links  WHERE receiver_id = '$arg' AND sender_id = '$arg1' AND chat_link_status='Active' ORDER BY chat_link_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Sender Chat Links with both sender and receiver id
function getAllSenderChatLinks($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "chat_links  WHERE sender_id = '$arg' AND receiver_id = '$arg1' AND chat_link_status='Active' ORDER BY chat_link_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Count of Chat Links
function getCountChatLinks()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "chat_links ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Count of Received Chat Links
function getCountReceiverChatLinks($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "chat_links  WHERE receiver_id = '$arg' AND sender_id = '$arg1' AND chat_link_status='Active' ORDER BY chat_link_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Count of Sender Chat Links
function getCountSenderChatLinks($arg,$arg1)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "chat_links  WHERE sender_id = '$arg' AND receiver_id = '$arg1' AND chat_link_status='Active' ORDER BY chat_link_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}



