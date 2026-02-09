<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['news_category_submit'])) {

        $category_id = $_POST['category_id'];
        $category_name = $_POST['category_name'];
        $category_image = $_POST['category_image_old'];


        $category_qry =
            " DELETE FROM  " . TBL . "news_categories  WHERE category_id='" . $category_id . "'";


        $category_res = mysqli_query($conn,$category_qry);


        if ($category_res) {

            $_SESSION['status_msg'] = "News category has been Permanently Deleted!!!";


            header('Location: news-all-category.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: news-category-delete.php?row=' . $category_id);
        }

        //    News Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: news-all-category.php');
}