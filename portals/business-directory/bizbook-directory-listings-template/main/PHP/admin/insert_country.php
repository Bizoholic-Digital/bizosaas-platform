<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";
if (isset($_POST['country_submit'])) {

    $cnt = count($_POST['country_name']);

// *********** if Count of country name is zero means redirect starts ********

    if ($cnt == 0) {
        header('Location: admin-add-country.php');
        exit;
    }

// *********** if Count of country name is zero means redirect ends ********

    for ($i = 0; $i < $cnt; $i++) {

        $country_name = $_POST['country_name'][$i];


//************ country Name Already Exist Check Starts ***************


        $country_name_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "countries  WHERE country_name='" . $country_name . "' ");

        if (mysqli_num_rows($country_name_exist_check) > 0) {


            $_SESSION['status_msg'] = "The Given country name $country_name is Already Exist Try Other!!!";

            header('Location: admin-add-new-country.php');
            exit;


        }

//************ country Name Already Exist Check Ends ***************


        $_FILES['country_image']['name'][$i];

        if (!empty($_FILES['country_image']['name'][$i])) {
            $file = rand(1000, 100000) . $_FILES['country_image']['name'][$i];
            $file_loc = $_FILES['country_image']['tmp_name'][$i];
            $file_size = $_FILES['country_image']['size'][$i];
            $file_type = $_FILES['country_image']['type'][$i];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../images/services/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $country_image = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $country_image = '';
            }
        }

        $sql = mysqli_query($conn, "INSERT INTO  " . TBL . "countries (country_name,country_cdt)
VALUES ('$country_name','$curDate')");

        $country_id = mysqli_insert_id($conn);

        $sql2 = mysqli_query($conn, "INSERT INTO  " . TBL . "states (state_name,country_id)
VALUES ('$country_name','$country_id')");


    }


    if ($sql) {

        $_SESSION['status_msg'] = "country(s) has been Added Successfully!!!";


        header('Location: admin-all-country.php');
        exit;

    } else {


        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: admin-add-country.php');
        exit;
    }

}
?>