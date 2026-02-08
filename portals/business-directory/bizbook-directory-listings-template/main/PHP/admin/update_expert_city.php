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


//************ Expert City Name Already Exist Check Starts ***************


        $country_name_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "expert_cities  WHERE country_name='" . $country_name . "' AND country_id != $country_id ");

        if (mysqli_num_rows($country_name_exist_check) > 0) {


            $_SESSION['status_msg'] = "The Given country name is Already Exist Try Other!!!";

            header('Location: expert-edit-city.php?row=' . $country_id);
            exit;


        }

//************ Expert City Name Already Exist Check Ends ***************

        $sql = mysqli_query($conn, "UPDATE  " . TBL . "expert_cities SET country_name='" . $country_name . "'
     where country_id='" . $country_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Expert City has been Updated Successfully!!!";


            header('Location: expert-all-city.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: expert-edit-city.php?row=' . $country_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: expert-all-city.php');
    exit;
}
?>