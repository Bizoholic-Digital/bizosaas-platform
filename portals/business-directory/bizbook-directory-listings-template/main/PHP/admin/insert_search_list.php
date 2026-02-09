<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";

if ($_SERVER['REQUEST_METHOD']=='POST') {

    if (isset($_POST['search_list_submit'])) {

// Basic Details
        $search_title = $_POST["search_title"];
        $search_tag_line = $_POST["search_tag_line"];
        $search_list_link = $_POST["search_list_link"];
        $search_list_position = 0;

        $search_list_status = "Active";

//    Search List Insert Part Starts


        $event_qry = "INSERT INTO " . TBL . "search_list 
					(search_title, search_tag_line, search_list_link,search_list_position,search_list_status,search_list_cdt) 
					VALUES 
					('$search_title', '$search_tag_line', '$search_list_link', '$search_list_position', '$search_list_status', '$curDate')";

        $event_res = mysqli_query($conn,$event_qry);



        if ($event_res) {


                $_SESSION['status_msg'] = "New Event has been created Successfully!!! ";

                header('Location: search-lists.php');

          
                exit;
           
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: search-lists-add.php');
        }

        //    Search Insert Part Ends

    }
}else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: search-lists.php');
}