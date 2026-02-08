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

        $product_qry = "DELETE FROM  " . TBL . "search_list where search_list_id='" . $search_list_id . "'";


        $product_res = mysqli_query($conn,$product_qry);


        if ($product_res) {


            $_SESSION['status_msg'] = "Search List has been Deleted Successfully!!!";

            header('Location: search-lists.php');

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: search-lists.php');
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: search-lists.php');
}