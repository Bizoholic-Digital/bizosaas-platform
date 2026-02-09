<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['category_filter_submit'])) {


        foreach ($_POST['category_id'] as $key => $id) {

            $category_id = $id;

            $category_filter = $_POST['category_filter'][$key];
            $category_filter_pos_id = $_POST['category_filter_pos_id'][$key];


            $sql = mysqli_query($conn, "UPDATE  " . TBL . "categories SET category_filter='" . $category_filter . "'
        , category_filter_pos_id='" . $category_filter_pos_id . "' where category_id='" . $category_id . "'");

        }

        if ($sql) {

            $_SESSION['status_msg'] = "Category Filter Data has been Updated Successfully!!!";


            header('Location: admin-filter-category.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-filter-category.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-filter-category.php');
    exit;
}
?>