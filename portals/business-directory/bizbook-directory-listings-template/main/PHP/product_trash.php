<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['product_submit'])) {

        $product_id = $_POST["product_id"];
        $gallery_image_old = $_POST["gallery_image_old"];

        $product_qry =
            "DELETE FROM  " . TBL . "products  where product_id='" . $product_id . "'";


        $product_res = mysqli_query($conn,$product_qry);


        if ($product_res) {

            unlink('images/products/'.$gallery_image_old);  //Delete the Product Gallery image
            //Query to delete the page view starts

            $page_view_qry = "DELETE FROM  " . TBL . "page_views where product_id='" . $product_id . "'";

            $page_view_res = mysqli_query($conn,$page_view_qry);

            //Query to delete the page view ends  

            $_SESSION['status_msg'] = $BIZBOOK['PRODUCT_DELETE_SUCCESS_MESSAGE'];

            header('Location: db-products');

        } else {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: db-products');
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: dashboard');
}