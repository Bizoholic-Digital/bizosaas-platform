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
            " DELETE FROM  " . TBL . "expert_areas  WHERE city_id='" . $city_id . "'";


        $city_res = mysqli_query($conn,$city_qry);


        if ($city_res) {

            $_SESSION['status_msg'] = "Expert Area has been Permanently Deleted!!!";


            header('Location: expert-all-area.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: expert-delete-area.php?row=' . $city_id);
        }


    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: expert-all-area.php');
}