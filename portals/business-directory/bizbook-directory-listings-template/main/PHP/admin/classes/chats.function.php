<?php

//Get All Chats
function getAllChats()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "chats ORDER BY chat_cdt DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Chats with Chat Link Id
function getChat($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "chats  WHERE chat_id = '$arg' AND chat_status= 'Active' ORDER BY chat_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Chats with Chat Link Id given
function getAllChatLinkIdChats($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "chats  WHERE chat_link_id = '$arg' AND chat_status='Active' ORDER BY chat_cdt ASC ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get Last Chat Message with Chat Link Id given
function getLastChatMessageLinkIdChats($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "chats WHERE chat_link_id = '$arg' AND chat_status='Active' ORDER BY chat_cdt DESC LIMIT 1 ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Chats with Chat User Id given
function getAllChatUserIdChats($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "chats  WHERE chat_user_id = '$arg' AND chat_status='Active' ORDER BY chat_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Count of Chats
function getCountChats()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "chats ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Count of Received Chat
function getCountChatLinkIdChats($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "chats  WHERE chat_link_id = '$arg' AND chat_status='Active' ORDER BY chat_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}

//Get All Count of Sender Chat
function getCountChatUserIdChats($arg)
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "chats  WHERE chat_user_id = '$arg' AND chat_status='Active' ORDER BY chat_cdt DESC ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}



