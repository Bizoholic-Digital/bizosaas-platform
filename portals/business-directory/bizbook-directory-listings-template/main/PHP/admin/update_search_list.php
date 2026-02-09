<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['search_list_submit'])) {

        $search_list_id = $_POST["search_list_id"];

        $search_title = $_POST["search_title"];

        $search_tag_line = $_POST["search_tag_line"];
        
        $search_list_link = $_POST["search_list_link"];


        $product_qry = "UPDATE  " . TBL . "search_list  SET search_title='" . $search_title . "', search_tag_line='" . $search_tag_line . "'
            ,search_list_link='" . $search_list_link . "' where search_list_id='" . $search_list_id . "'";


        $product_res = mysqli_query($conn,$product_qry);


        if ($product_res) {

                $_SESSION['status_msg'] = "Your Search List has been Updated Successfully!!!";

                header('Location: search-lists.php');
                exit;
            
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header("Location: search-lists-edit.php?row=$search_list_id");
        }

        //    Search Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: search-lists.php');
}