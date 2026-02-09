<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['popular_tags_submit'])) {

        $popular_tags_id = $_POST["popular_tags_id"];

        $product_qry =
            "DELETE FROM  " . TBL . "popular_tags where popular_tags_id='" . $popular_tags_id . "'";


        $product_res = mysqli_query($conn,$product_qry);


        if ($product_res) {


            $_SESSION['status_msg'] = "Popular Tags has been Deleted Successfully!!!";

            header('Location: admin-footer-popular-tags.php');

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-footer-popular-tags.php');
        }

        //    Popular Tag Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-footer-popular-tags.php.php');
}