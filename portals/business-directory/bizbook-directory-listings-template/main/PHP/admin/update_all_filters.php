<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['all_filter_submit'])) {


        $all_listing_filter_id = 1;

        $service_filter = $_POST['service_filter'];
        $category_filter = $_POST['category_filter'];
        $feature_filter = $_POST['feature_filter'];
        $rating_filter = $_POST['rating_filter'];
        $city_filter = $_POST['city_filter'];
        $country_filter = $_POST['country_filter'];


        $sql = mysqli_query($conn,"UPDATE  " . TBL . "all_listing_filters SET service_filter='" . $service_filter. "'
        , category_filter='" . $category_filter . "', feature_filter='" . $feature_filter . "', rating_filter='" . $rating_filter . "'
        , city_filter='" . $city_filter. "' , country_filter='" . $country_filter. "'
         where all_listing_filter_id='" . $all_listing_filter_id . "'");



        if ($sql) {

            $_SESSION['status_msg'] = "All Filter Data has been Updated Successfully!!!";


            header('Location: admin-all-filters.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-all-filters.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-all-filters.php');
    exit;
}
?>