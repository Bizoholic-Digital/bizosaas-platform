<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['product-seo-submit'])) {

        $product_id = $_POST['product_id'];


        $seo_title = $_POST['seo_title'];
        $seo_keywords = $_POST['seo_keywords'];
        $seo_description = $_POST['seo_description'];


        $sql = mysqli_query($conn,"UPDATE  " . TBL . "products SET  seo_title='" . $seo_title. "'
        ,seo_keywords='" . $seo_keywords. "', seo_description='" . $seo_description . "'
        where product_id='" . $product_id . "'");


        if ($sql) {

            $_SESSION['status_msg'] = "Product SEO options has been Updated Successfully!!!";


            header('Location: seo-all-product-options.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: seo-all-product-options.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: seo-all-product-options.php');
    exit;
}
?>