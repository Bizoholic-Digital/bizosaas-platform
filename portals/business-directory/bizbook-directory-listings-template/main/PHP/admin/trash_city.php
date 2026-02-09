<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['city_submit'])) {

        $city_id = $_POST['city_id'];
        $city_name = $_POST['city_name'];


        $city_qry =
            " DELETE FROM  " . TBL . "cities  WHERE city_id='" . $city_id . "'";


        $city_res = mysqli_query($conn,$city_qry);


        if ($city_res) {

            $_SESSION['status_msg'] = "city has been Permanently Deleted!!!";


            header('Location: admin-all-city.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-city-delete.php?row=' . $city_id);
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-all-city.php');
}