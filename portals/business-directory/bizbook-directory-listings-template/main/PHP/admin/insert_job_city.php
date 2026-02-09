<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";
if (isset($_POST['city_submit'])) {

    $cnt = count($_POST['city_name']);

// *********** if Count of city name is zero means redirect starts ********

    if($cnt == 0){
        header('Location: admin-add-city.php');
        exit;
    }

// *********** if Count of city name is zero means redirect ends ********

    for ($i = 0; $i < $cnt; $i++) {

        $city_name = $_POST['city_name'][$i];


//************ city Name Already Exist Check Starts ***************


            $city_name_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "job_cities  WHERE city_name='" . $city_name . "' ");

            if (mysqli_num_rows($city_name_exist_check) > 0) {


                $_SESSION['status_msg'] = "The Given Job City name $city_name is Already Exist Try Other!!!";

                header('Location: admin-add-city.php');
                exit;


            }


//************ city Name Already Exist Check Ends ***************



        $sql = mysqli_query($conn, "INSERT INTO  " . TBL . "job_cities (city_name,city_cdt)
VALUES ('$city_name','$curDate')");



    }


    if ($sql) {

        $_SESSION['status_msg'] = "Job City(s) has been Added Successfully!!!";


        header('Location: admin-all-job-city.php');
        exit;

    } else {


        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: admin-add-job-city.php');
        exit;
    }

}
?>