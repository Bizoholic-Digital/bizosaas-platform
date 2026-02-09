<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['target_submit'])) {

        $page_id = $_POST["page_id"];

        $page_qry = "DELETE FROM  " . TBL . "pages where page_id='" . $page_id . "'";

        $page_res = mysqli_query($conn,$page_qry);


        if ($page_res) {

            //Query to delete the page view starts

            $page_view_qry = "DELETE FROM  " . TBL . "page_views where page_id='" . $page_id . "'";

            $page_view_res = mysqli_query($conn,$page_view_qry);

            //Query to delete the page view ends

            $_SESSION['status_msg'] = "Target Promotion page has been Deleted Successfully!!!";

            header('Location: seo-target-promotion-all-pages.php');

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: seo-target-promotion-all-pages.php');
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: seo-target-promotion-all-pages.php');
}