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
        $country_id = $_POST['country_id'];


//************ city Name Already Exist Check Starts ***************


        $city_name_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "expert_areas  WHERE city_name='" . $city_name . "' AND city_id != $city_id  AND state_id != $country_id ");

        if (mysqli_num_rows($city_name_exist_check) > 0) {


            $_SESSION['status_msg'] = "The Given Expert Area name is Already Exist Try Other!!!";

            header('Location: expert-edit-area.php?row=' . $city_id);
            exit;


        }

//************ city Name Already Exist Check Ends ***************


        $sql = mysqli_query($conn, "UPDATE  " . TBL . "expert_areas SET city_name='" . $city_name . "',state_id ='" . $country_id . "'
     where city_id='" . $city_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Expert Area has been Updated Successfully!!!";


            header('Location: expert-all-area.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: expert-edit-area.php?row=' . $city_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: expert-all-area.php');
    exit;
}
?>