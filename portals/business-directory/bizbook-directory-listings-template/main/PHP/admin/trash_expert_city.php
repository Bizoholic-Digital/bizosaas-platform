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
            " DELETE FROM  " . TBL . "expert_cities  WHERE country_id='" . $country_id . "'";


        $country_res = mysqli_query($conn,$country_qry);


        if ($country_res) {

            $_SESSION['status_msg'] = "Expert City has been Permanently Deleted!!!";


            header('Location: expert-all-city.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: expert-delete-city.php?row=' . $country_id);
        }



    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: expert-all-city.php');
}