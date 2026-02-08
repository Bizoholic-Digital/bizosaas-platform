<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";

if ($_SERVER['REQUEST_METHOD']=='POST') {

    if (isset($_POST['popular_tags_submit'])) {

// Basic Personal Details
        $popular_tags_name = $_POST["popular_tags_name"];
        $popular_tags_link = $_POST["popular_tags_link"];
        $popular_tags_status = "Active";


//    Ebook Insert Part Starts


        $sql_qry = "INSERT INTO " . TBL . "popular_tags 
					(popular_tags_name, popular_tags_link, popular_tags_status, popular_tags_cdt) 
					VALUES 
					('$popular_tags_name', '$popular_tags_link', '$popular_tags_status', '$curDate')";

        $sql_res = mysqli_query($conn,$sql_qry);

        if ($sql_res) {

            $_SESSION['status_msg'] = "New Popular Tags has been created Successfully!!! ";

            header('Location: admin-footer-popular-tags.php');


        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-footer-popular-tags.php');
        }

        //    E-Book Insert Part Ends

    }
}else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-footer-popular-tags.php');
}