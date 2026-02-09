<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['featured_filter_submit'])) {


        foreach ($_POST['all_featured_filter_id'] as $key => $id) {

            $all_featured_filter_id = $id;

            $all_featured_filter_status = $_POST['all_featured_filter_status'][$key];


            $sql = mysqli_query($conn, "UPDATE  " . TBL . "all_featured_filters SET all_featured_filter_status='" . $all_featured_filter_status . "'
            where all_featured_filter_id ='" . $all_featured_filter_id . "'");

        }

        if ($sql) {

            $_SESSION['status_msg'] = "Featured Filter Data has been Updated Successfully!!!";


            header('Location: admin-filter-features.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-filter-features.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-filter-features.php');
    exit;
}
?>