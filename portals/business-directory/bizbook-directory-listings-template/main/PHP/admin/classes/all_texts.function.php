<?php

//Get All Texts
function getAllTexts()
{
    global $conn;

    $sql = "SELECT * FROM " . TBL . "all_texts WHERE all_text_id = 1";;
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);
    return $row;

}