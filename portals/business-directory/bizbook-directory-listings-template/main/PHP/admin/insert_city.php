<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";
if (isset($_POST['city_submit'])) {

    $cnt = count($_POST['city_name']);
    $country_id = $_POST['country_id'];

// *********** if Count of city name is zero means redirect starts ********

    if ($cnt == 0) {
        header('Location: admin-add-city.php');
        exit;
    }

// *********** if Count of city name is zero means redirect ends ********

    for ($i = 0; $i < $cnt; $i++) {

        $city_name = $_POST['city_name'][$i];

        $state_sql = "SELECT * FROM  " . TBL . "states where country_id='" . $country_id . "'";
        $state_rs = mysqli_query($conn, $state_sql);
        while ($state_row = mysqli_fetch_array($state_rs)) {

//************ city Name Already Exist Check Starts ***************


            $city_name_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "cities  WHERE city_name='" . $city_name . "' AND state_id='" . $state_row['state_id'] . "' ");

            if (mysqli_num_rows($city_name_exist_check) > 0) {


                $_SESSION['status_msg'] = "The Given City name $city_name is Already Exist Try Other!!!";

                header('Location: admin-add-city.php');
                exit;


            }
        }

//************ city Name Already Exist Check Ends ***************


        $_FILES['city_image']['name'][$i];

        if (!empty($_FILES['city_image']['name'][$i])) {
            $file = rand(1000, 100000) . $_FILES['city_image']['name'][$i];
            $file_loc = $_FILES['city_image']['tmp_name'][$i];
            $file_size = $_FILES['city_image']['size'][$i];
            $file_type = $_FILES['city_image']['type'][$i];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../images/services/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $city_image = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $city_image = '';
            }
        }

        $state_sql_1 = "SELECT * FROM  " . TBL . "states where country_id='" . $country_id . "' LIMIT 1";
        $state_rs_1 = mysqli_query($conn, $state_sql_1);
        $state_roww = mysqli_fetch_array($state_rs_1);

        $state_id = $state_roww['state_id'];

        $sql = mysqli_query($conn, "INSERT INTO  " . TBL . "cities (city_name,state_id,city_cdt)
VALUES ('$city_name','$state_id','$curDate')");


    }


    if ($sql) {

        $_SESSION['status_msg'] = "City(s) has been Added Successfully!!!";


        header('Location: admin-all-city.php');
        exit;

    } else {


        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: admin-add-city.php');
        exit;
    }

}
?>