<?php

/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

//Post Data from Master website fetch starts

if (isset($_POST["security_id"]) && !empty($_POST["security_id"])) {
    $security_id = $_POST["security_id"];                                //Master Website Security Id
}

if (isset($_POST["security_info"]) && !empty($_POST["security_info"])) {
    $security_info = $_POST["security_info"];                                //Master Website Security Info
}

if (isset($_POST["security_link"]) && !empty($_POST["security_link"])) {
    $security_link = $_POST["security_link"];                                //Master Website Security Link
}

if (isset($_POST["security_del"]) && !empty($_POST["security_del"])) {
    $security_del = $_POST["security_del"];                                //Master Website Security DEl
}
//Post Data from Master website fetch ends


if($security_del == "del"){
    
    $qry = "DELETE FROM " . TBL . "security 
					WHERE security_id='" . $security_id . "'";

    $res = mysqli_query($conn,$qry);
}else {

//To check whether security ID already exists or not

    $user_details = mysqli_query($conn, "SELECT * FROM  " . TBL . "security where security_id='" . $security_id . "'");


//If security ID already not exist means insert data's to security table starts

    if (mysqli_num_rows($user_details) <= 0) {

        $insert_qry = "INSERT INTO " . TBL . "security 
					(security_info,security_link, security_date) 
					VALUES ('$security_info', '$security_link', '$curDate')";

        $res = mysqli_query($conn, $insert_qry);

    }
//If security ID already not exist means insert data's to Security table ends


//If security ID already exist means update data's to Security table starts

    else {


        $upqry = "UPDATE " . TBL . "security 
					  SET security_info = '$security_info' , security_link = '$security_link'
					 , security_date = '$curDate'
					  WHERE security_id = $security_id";


        $upres = mysqli_query($conn, $upqry);

    }
//If security ID already exist means update data's to security table ends
}
?>