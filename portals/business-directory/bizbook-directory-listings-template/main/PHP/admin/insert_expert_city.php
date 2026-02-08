<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";
if (isset($_POST['country_submit'])) {

    $cnt = count($_POST['country_name']);

// *********** if Count of Expert City name is zero means redirect starts ********

    if ($cnt == 0) {
        header('Location: expert-add-new-city.php');
        exit;
    }

// *********** if Count of Expert City name is zero means redirect ends ********

    for ($i = 0; $i < $cnt; $i++) {

        $country_name = $_POST['country_name'][$i];


//************ Expert City Name Already Exist Check Starts ***************


        $country_name_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "expert_cities  WHERE country_name='" . $country_name . "' ");

        if (mysqli_num_rows($country_name_exist_check) > 0) {


            $_SESSION['status_msg'] = "The Given Expert City name $country_name is Already Exist Try Other!!!";

            header('Location: expert-add-new-city.php');
            exit;


        }

//************ Expert City Name Already Exist Check Ends ***************


        $sql = mysqli_query($conn, "INSERT INTO  " . TBL . "expert_cities (country_name,country_cdt)
VALUES ('$country_name','$curDate')");

    }


    if ($sql) {

        $_SESSION['status_msg'] = "Expert City(s) has been Added Successfully!!!";


        header('Location: expert-all-city.php');
        exit;

    } else {


        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: expert-add-new-city.php');
        exit;
    }

}
?>