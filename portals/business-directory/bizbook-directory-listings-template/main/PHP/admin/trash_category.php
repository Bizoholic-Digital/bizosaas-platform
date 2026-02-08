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
        $category_image = $_POST['category_image_old'];

        $category_qry =
            " DELETE FROM  " . TBL . "categories  WHERE category_id='" . $category_id . "'";


        $category_res = mysqli_query($conn,$category_qry);


        if ($category_res) {
            unlink('../images/services/'.$category_image);  //Delete the category image
            //Query to delete the page view starts

            $page_view_qry = "DELETE FROM  " . TBL . "page_views where category_id='" . $category_id . "'";

            $page_view_res = mysqli_query($conn,$page_view_qry);

            //Query to delete the page view ends

            $_SESSION['status_msg'] = "Category has been Permanently Deleted!!!";


            header('Location: admin-all-category.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-category-delete.php?row=' . $category_id);
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-all-category.php');
}