<?php

//Get All Mail Templates
function getAllMailTemplates()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "mail  ORDER BY mail_id ASC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get Mail Template with given Mail Id
function getMailTemplate($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "mail where mail_id='" . $arg . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}