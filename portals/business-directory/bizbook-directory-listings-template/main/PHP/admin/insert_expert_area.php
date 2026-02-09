<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";
if (isset($_POST['city_submit'])) {

    $cnt = count($_POST['city_name']);
    $country_id = $_POST['country_id'];

// *********** if Count of Area name is zero means redirect starts ********

    if ($cnt == 0) {
        header('Location: expert-add-new-area.php');
        exit;
    }

// *********** if Count of Area name is zero means redirect ends ********

    for ($i = 0; $i < $cnt; $i++) {

        $city_name = $_POST['city_name'][$i];


//************ Area Name Already Exist Check Starts ***************


            $city_name_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "expert_areas  WHERE city_name='" . $city_name . "' AND state_id='" . $country_id . "' ");

            if (mysqli_num_rows($city_name_exist_check) > 0) {


                $_SESSION['status_msg'] = "The Given Area name $city_name is Already Exist Try Other!!!";

                header('Location: expert-add-new-area.php');
                exit;


            }

//************ Area Name Already Exist Check Ends ***************


        $sql = mysqli_query($conn, "INSERT INTO  " . TBL . "expert_areas (city_name,state_id,city_cdt)
VALUES ('$city_name','$country_id','$curDate')");


    }


    if ($sql) {

        $_SESSION['status_msg'] = "Area(s) has been Added Successfully!!!";


        header('Location: expert-all-area.php');
        exit;

    } else {


        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location:  expert-add-new-area.php');
        exit;
    }

}
?>