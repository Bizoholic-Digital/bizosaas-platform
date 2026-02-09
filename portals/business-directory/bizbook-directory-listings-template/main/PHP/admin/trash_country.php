<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['country_submit'])) {

        $country_id = $_POST['country_id'];
        $country_name = $_POST['country_name'];


        $country_qry =
            " DELETE FROM  " . TBL . "countries  WHERE country_id='" . $country_id . "'";


        $country_res = mysqli_query($conn,$country_qry);


        if ($country_res) {

            $_SESSION['status_msg'] = "Country has been Permanently Deleted!!!";


            header('Location: admin-all-country.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-country-delete.php?row=' . $country_id);
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-all-country.php');
}