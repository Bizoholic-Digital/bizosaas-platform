<?php

//Get All Security
function getAllSecurity()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "security ORDER BY security_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}