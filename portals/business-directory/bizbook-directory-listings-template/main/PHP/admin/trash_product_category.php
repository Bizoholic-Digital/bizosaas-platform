<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['category_submit'])) {

        $category_id = $_POST['category_id'];
        $category_name = $_POST['category_name'];


        $category_qry =
            " DELETE FROM  " . TBL . "product_categories  WHERE category_id='" . $category_id . "'";


        $category_res = mysqli_query($conn,$category_qry);


        if ($category_res) {

            $_SESSION['status_msg'] = "Product Category has been Permanently Deleted!!!";


            header('Location: admin-all-product-category.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-product-category-delete.php?row=' . $category_id);
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-all-product-category.php');
}