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


//************ city Name Already Exist Check Starts ***************


        $city_name_exist_check = mysqli_query($conn,"SELECT * FROM " . TBL . "cities  WHERE city_name='" . $city_name . "' AND city_id != $city_id ");

        if (mysqli_num_rows($city_name_exist_check) > 0) {


            $_SESSION['status_msg'] = "The Given job city name is Already Exist Try Other!!!";

            header('Location: admin-job-city-edit.php?row=' . $city_id);
            exit;


        }

//************ city Name Already Exist Check Ends ***************
        

        $sql = mysqli_query($conn,"UPDATE  " . TBL . "cities SET city_name='" . $city_name . "'
     where city_id='" . $city_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Job City has been Updated Successfully!!!";


            header('Location: admin-all-job-city.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-city-job-edit.php?row=' . $city_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-all-job-city.php');
    exit;
}
?>