<?php


//Get All Footer Data
function getAllFooter()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "footer WHERE footer_id = 1";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}

